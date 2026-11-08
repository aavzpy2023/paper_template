# Ready-made root documents

Copy one of these into the project root when you need it, then `bash logs/build.sh`. It is discovered from there:
the build script and the tests find every `*.tex` in the root that declares a `\documentclass`, so nothing has to be
registered anywhere.

| File | Class | Notes |
|---|---|---|
| `paper_springer.tex` | `sn-jnl` | Springer Nature. The class and its `.bst` files are vendored in `../springer/`, and `.latexmkrc` already puts that directory on `TEXINPUTS`. The class option picks the bibliography style: `sn-vancouver-num` for a numbered journal, `sn-basic` or `sn-vancouver-ay` for author–year. |
| `paper_elsevier.tex` | `cas-sc` | Elsevier single column; `cas-dc` for a double-column journal. The class ships with TeX Live as `els-cas-templates`, so nothing is vendored. |
| `supplementary.tex` | `article` | A second PDF for the material that supports the paper without being part of its argument. It reads the same `latex/` as the manuscript, so its numbers are the ones the pipeline produced. Cross-document references do not resolve, so the manuscript refers to its items as "Table S1" in plain text and their order here is what that depends on. |

Each one supplies the class, the bibliography style, and renderers for the project's four macros — `\projauthor`,
`\projauthorcorr`, `\projtable` and `\projdeclaration`. Nothing in `sections/` changes when you add one; that is the
whole point of keeping the facts and the markup apart.

**Writing one for a new journal** is the same job: start from the publisher's own template, strip its sample content,
and define those four macros in its notation. `paper_springer.tex` and `paper_elsevier.tex` are the two worked
examples, and they differ enough to show the range — one wants the given and family names in separate commands and
the address broken into fields, the other wants a single name with the address as key–value pairs.

One trap, found the hard way: `sn-jnl` expands the optional (running title) argument of `\title` immediately, so its
`\input{sections/manuscript_metadata.tex}` has to sit in the preamble, before `\begin{document}`.
