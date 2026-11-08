# paper-template

One manuscript, several journal layouts, and no number ever typed by hand.

The text lives once in `sections/`. Every figure and every number lives once in `latex/`, written there by a script.
`paper.tex` is the document you write and review in. When a journal is chosen, its layout is a second root `.tex`
that says only how that publisher wants the same facts arranged — never an edit to the manuscript.

## Starting a new paper

```bash
git clone <this repo> my-paper && cd my-paper && rm -rf .git && git init
bash ./build.sh        # paper.pdf, before a word has been written
```

Then, in this order:

1. **`sections/manuscript_metadata.tex`** — title, authors, e-mails, ORCIDs, CRediT roles, affiliation. This is the
   only file in the project that holds any of them. A test fails if another file repeats a family name, an e-mail or
   an ORCID.
2. **`sections/06_1_Data_Available.tex`, `06_3_Funding.tex`, `06_5_Acknowledgements.tex`** — the three declarations
   that carry real text. The other three are standard and usually stay as they are.
3. **`sections/01Introduction.tex` … `05Conclusions.tex`** — the manuscript. Rename and renumber them freely; the
   order of `sections/manuscript_body.tex` is the order of the paper.
4. **`scripts/`** — one script per analysis step, numbered in the order they run. Each one ends by writing its
   results to `latex/<step>_variables.tex`, and `sections/manuscript_variables.tex` lists those files.
   `scripts/99_demo_variables.py` is the smallest complete example; delete it once a real step exists.
5. **`references.bib`** — replace the example entry.
6. **`sections/00abstract.tex` and `00keywords.tex`** — last.

## The rule that makes it work

A number that is typed into the text stops being true the moment the analysis is re-run, and nobody notices.
So: a script computes it, writes it as a LaTeX macro, and the text names the macro.

```python
from qsartools.latex import format_macros
write(os.path.join(LATEX_DIR, "07_variables.tex"),
      format_macros({"MorganRTwoMean": f"{score:.3f}"}, header="Written by scripts/07_....py"))
```

```latex
Morgan fingerprints reached $R^2 = \MorganRTwoMean$.
```

`python scripts/11_check_manuscript.py` then follows every `\input`, `\projtable` and `\projdeclaration` from each
root document and **fails** if the text names a macro or a figure that no script produced. Run it before every
submission; it is the step that catches a stale number.

Macro names hold letters only, so `R2` is spelled `RTwo`. `qsartools.latex.newcommand` raises rather than writing a
name that would not compile.

## Building

```bash
bash ./build.sh                 # every root .tex that declares a \documentclass
bash ./build.sh paper           # just that one
```

Auxiliary files stay in `build/`; only the PDFs are copied to the root, where they are versioned. Everything goes
through `latexmk` so that `.latexmkrc` applies — calling `pdflatex` directly litters the root and skips the
bibliography passes.

The script reports `errors=` and `undefined=` per document, read from TeX's log of the **last** pass. A large
`undefined=` that no source change explains is almost always a second LaTeX process compiling the same document (an
editor building on save): it leaves a newer `build/<doc>.pdf`, latexmk then considers the document up to date and
skips the final pass, and the stale count persists across rebuilds. Delete `build/<doc>.pdf` and build that one
document alone.

`.vscode/settings.json` sets `latex-workshop.latex.autoBuild.run` to `never` for exactly that reason, and
`.vscode/tasks.json` makes `./build.sh` the default build task (Ctrl+Shift+B). Leave it off: `onFileChange` is
what produced the corrupt PDF the paragraph above describes.

## Layouts

`paper.tex` is the only document, and the one you work in: plain `article`, figures and tables next to the text that
cites them. It is not a submission layout, and it stays whatever journal you end up with — a publisher's class
deliberately collects the figures at the end, which is right for a submission and useless for reading a draft.

**When a journal appears**, copy its layout out of `templates/documents/` into the root:

```bash
cp templates/documents/paper_springer.tex .     # or paper_elsevier.tex, or supplementary.tex
bash ./build.sh
```

`./build.sh` and the tests find every `*.tex` in the root that declares a `\documentclass`, so the new document
is built and checked from the moment it is there; nothing has to be registered. `templates/documents/README.md` says
what each one is and what to watch for.

**Writing one for a journal that has none yet** is one file. It supplies the class, the bibliography style, and
renderers for four project macros:

```latex
\newcommand{\projtable}[1]{\input{#1}}                        % how a generated table is typeset
\newcommand{\projdeclaration}[2]{\section*{#1}\input{#2}}     % how a declaration gets its heading
\newcommand{\projauthor}[6]{...}                              % initials, given, family, email, orcid, roles
\newcommand{\projauthorcorr}[6]{...}                          % the same, for the corresponding author
```

Then it `\input`s the metadata and the variables and `\input`s `sections/manuscript_body.tex`. Nothing in
`sections/` is touched.

The author renderers exist because no two classes agree: one wants `\author[1]{Name}` with `\ead` and `\credit`
after it and the address as key-value pairs, another wants `\fnm{}`/`\sur{}` split and `\author*` for the
corresponding author, and `paper.tex` wants one `\and`-separated line. The facts are stated once; each class
arranges them its own way.

## Tests

```bash
python -m pytest -q
```

They check the structure, not the science:

- nothing in `latex/` pulls in another file — it holds build products only;
- every document reads the body and the variables from the one list, and none repeats it;
- the lists match what is on disk, and the numbered sections are in reading order;
- every declaration file exists, carries no heading of its own, and is printed by every layout;
- **no file in `sections/` names a publisher or a class** — this is the rule that keeps the manuscript portable, and
  the one that breaks first when a statement is written for a particular journal;
- the metadata holds no class-specific command, every layout defines both author renderers, exactly one author
  corresponds, and the contributions are rendered from the same list rather than written out again.

Add the project's own tests under `tests/`; `tests/qsartools/` mirrors `scripts/qsartools/`.

## Layout of the repository

```
build.sh                builds every root document. The only way they are built.
paper.tex               the document you write and review in.
sections/               the manuscript, by hand. No journal is named here.
latex/                  macros and tables, written by scripts. Never edited.
figures/                figures, written by scripts.
scripts/                one numbered script per step; qsartools/ holds the reusable pieces.
data/                   inputs, never written by a script.
results/                CSVs a later step reads.
logs/                   one log per step, written by the scripts. Nothing is run from here.
templates/documents/    root documents to copy into the root when a journal is chosen.
templates/springer/     the vendored sn-jnl class and its bibliography styles.
.vscode/                autoBuild off, and a build task. See the warning under Building.
build/                  auxiliary files; not versioned.
```

`scripts/paths_config.py` decides every path; no script hardcodes one. Set `PAPER_OUT_DIR` to send a second run's
output elsewhere so it cannot overwrite the first.
