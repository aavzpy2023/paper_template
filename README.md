# paper-template

One manuscript, several journal layouts, and no number ever typed by hand.

The text lives once in `sections/`. Every figure and every number lives once in `latex/`, written there by a script.
A root `.tex` per journal says only how that publisher wants the same facts arranged. Switching journal is writing
one of those files; it is never editing the manuscript.

## Starting a new paper

```bash
git clone <this repo> my-paper && cd my-paper && rm -rf .git && git init
bash logs/build.sh        # four PDFs, before a word has been written
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
bash logs/build.sh                 # every root .tex that declares a \documentclass
bash logs/build.sh paper_reading   # just that one
```

Auxiliary files stay in `build/`; only the PDFs are copied to the root, where they are versioned. Everything goes
through `latexmk` so that `.latexmkrc` applies — calling `pdflatex` directly litters the root and skips the
bibliography passes.

The script reports `errors=` and `undefined=` per document, read from TeX's log of the **last** pass. A large
`undefined=` that no source change explains is almost always a second LaTeX process compiling the same document (an
editor building on save): it leaves a newer `build/<doc>.pdf`, latexmk then considers the document up to date and
skips the final pass, and the stale count persists across rebuilds. Delete `build/<doc>.pdf` and build that one
document alone.

## Layouts

| File | Class | What it is for |
|---|---|---|
| `paper_reading.tex` | `article` | Reading copy: figures and tables next to the text that cites them. Not for submission. |
| `paper_elsevier.tex` | `cas-sc` | Elsevier single column. The class ships with TeX Live; nothing is vendored. |
| `paper_springer.tex` | `sn-jnl` | Springer Nature. Class and `.bst` files vendored in `templates/springer/`. |
| `supplementary.tex` | `article` | Its own PDF, reading the same `latex/` as the manuscript. Items numbered S1, S2, … |

**Adding a journal** is one new root `.tex`. It supplies the class, the bibliography style, and renderers for three
project macros:

```latex
\newcommand{\projtable}[1]{\input{#1}}                        % how a generated table is typeset
\newcommand{\projdeclaration}[2]{\section*{#1}\input{#2}}     % how a declaration gets its heading
\newcommand{\projauthor}[6]{...}                              % initials, given, family, email, orcid, roles
\newcommand{\projauthorcorr}[6]{...}                          % the same, for the corresponding author
```

Then `\input` the metadata and the variables, and `\input{sections/manuscript_body.tex}`. Nothing in `sections/` is
touched, and `logs/build.sh` and the tests pick the new document up on their own.

The author renderers exist because no two classes agree: one wants `\author[1]{Name}` with `\ead` and `\credit`
after it and the address as key-value pairs, another wants `\fnm{}`/`\sur{}` split and `\author*` for the
corresponding author, and the reading copy wants one `\and`-separated line. The facts are stated once; each class
arranges them its own way. Note that `sn-jnl` expands the running title immediately, so its metadata `\input` has
to sit in the preamble, before `\begin{document}`.

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
sections/     the manuscript, by hand. No journal is named here.
latex/        macros and tables, written by scripts. Never edited.
figures/      figures, written by scripts.
scripts/      one numbered script per step; qsartools/ holds the reusable pieces.
data/         inputs, never written by a script.
results/      CSVs a later step reads.
logs/         one log per step, and build.sh.
templates/    vendored journal classes.
build/        auxiliary files; not versioned.
*.tex         one root document per layout.
```

`scripts/paths_config.py` decides every path; no script hardcodes one. Set `PAPER_OUT_DIR` to send a second run's
output elsewhere so it cannot overwrite the first.
