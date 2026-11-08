#!/usr/bin/env bash
# Build one of the manuscript layouts, or all of them. They share sections/ and latex/ and differ only in the class,
# the author block and the bibliography style, so adding a journal means adding one root .tex and nothing else.
#
#   ./build.sh                    every document
#   ./build.sh paper              just that one
#
# Everything is driven through latexmk so that .latexmkrc applies: the auxiliary files stay in build/ and only the
# PDF is copied back to the root, where it is versioned. Calling pdflatex directly bypasses that and litters the root.
#
# With no argument the documents are discovered the same way scripts/11_check_manuscript.py discovers them: every
# *.tex in the root that declares a \documentclass. A new layout is therefore built as soon as it exists.
cd "$(dirname "$0")" || exit 1
mkdir -p build
# The search paths for the vendored class and its styles are set in .latexmkrc, so the editor finds them too.

if [ "$#" -gt 0 ]; then
  DOCS=$*
else
  DOCS=$(grep -l '^[^%]*\\documentclass' ./*.tex | sed 's|^\./||; s|\.tex$||' | sort)
fi
[ -n "$DOCS" ] || { echo "No root .tex (one with \\documentclass) found"; exit 1; }

STATUS=0
for doc in $DOCS; do
  if ! latexmk -pdf -interaction=nonstopmode "$doc.tex" > "build/${doc}_build.log" 2>&1; then
    printf "  %-22s LATEXMK FAILED, see build/%s_build.log\n" "$doc" "$doc"
    tail -5 "build/${doc}_build.log" | sed 's/^/      /'
    STATUS=1
    continue
  fi
  # .latexmkrc copies the PDF back only after a build it considered necessary, and latexmk removes a stale copy
  # from the root, so a document that was already up to date would lose its PDF. Copy unconditionally.
  [ -f "build/$doc.pdf" ] && cp -u "build/$doc.pdf" "$doc.pdf"
  log="build/${doc}.log"
  errors=$(grep -cE '^! ' "$log" 2>/dev/null); errors=${errors:-0}
  undefined=$(grep -cE 'Citation .* undefined|Reference .* undefined' "$log" 2>/dev/null); undefined=${undefined:-0}
  pages=$(pdfinfo "$doc.pdf" 2>/dev/null | awk '/^Pages/{print $2" pages"}')
  printf "  %-22s errors=%-3s undefined=%-3s %s\n" "$doc" "$errors" "$undefined" "$pages"
  # These counts are read from TeX's own log of the LAST pass. A second LaTeX process compiling the same document
  # (an editor's build-on-save) leaves a newer build/$doc.pdf, latexmk then skips the final pass, and the counts
  # freeze with the intermediate state. A large undefined= that no source change explains is usually that: delete
  # build/$doc.pdf and build this one document alone.
  if [ "$errors" != "0" ] || [ "$undefined" != "0" ]; then STATUS=1; fi
done
exit $STATUS
