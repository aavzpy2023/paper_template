"""
99_demo_variables.py — The one example of how a number reaches the manuscript.

No number is ever typed into the text. A step computes it, writes it here as a LaTeX macro, and the manuscript
names the macro; scripts/11_check_manuscript.py then fails the build if the text names one that no step produced.
That is the whole contract, and this file is its smallest possible instance. Copy it for a real step, number the
copy for its place in the pipeline, and delete this one once the pipeline has a step of its own.

A LaTeX macro name holds letters only, which is why a result called "R2" is spelled RTwo; qsartools.latex raises
rather than writing a name that would not compile.

Run: python scripts/99_demo_variables.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from paths_config import LATEX_DIR, LOGS_DIR
from logger_utils import setup_logger, explain
from qsartools.latex import CENTERED_X, format_macros, tabular_close, tabular_open


def main():
    setup_logger(os.path.join(LOGS_DIR, "99_demo_variables.log"))
    explain("What this step does", """
        Stands in for a real analysis step. It writes the two macros the placeholder abstract uses and one example
        table, so that a fresh checkout builds and the check step passes before any science exists.
    """)

    # In a real step these come from the analysis, not from literals.
    rows = [("First", "An example row, generated from data rather than typed", 0.74),
            ("Second", "The next one", 0.71)]
    n_samples = 859

    macros = {"DemoHeadline": f"{rows[0][2]:.2f}", "DemoNSamples": n_samples}
    header = "Written by scripts/99_demo_variables.py. Do not edit: the next run overwrites it."
    write(os.path.join(LATEX_DIR, "demo_variables.tex"), format_macros(macros, header=header))

    colspec = f"l{CENTERED_X} r"
    table = [tabular_open(colspec), r"\toprule", r"Method & What it does & Score \\", r"\midrule"]
    table += [f"{name} & {what} & {score:.2f} " + r"\\" for name, what, score in rows]
    table += [r"\bottomrule", tabular_close(colspec)]
    write(os.path.join(LATEX_DIR, "demo_table.tex"),
          "% Written by scripts/99_demo_variables.py. Do not edit: the next run overwrites it.\n"
          + "\n".join(table) + "\n")

    print(f"[OK] wrote {len(macros)} macros and 1 table to {LATEX_DIR}", flush=True)


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"[WRITE] {path}", flush=True)


if __name__ == "__main__":
    main()
