# =========================================================
# paths_config.py — Central path configuration
# Import this in every script: from paths_config import ROOT, LATEX_DIR, ...
#
# One place decides where things go, so no script hardcodes a path and a reader can see the whole layout at once.
# Add a project's own data files, result files and parameters below the directories; keep anything a script would
# otherwise hardcode here, including thresholds and seeds, so that changing one is one edit.
# =========================================================
import os

# Project root = parent of the scripts/ folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR    = os.path.join(ROOT, "data")       # inputs, never written by a script
RESULTS_DIR = os.path.join(ROOT, "results")    # CSVs a later step reads
LATEX_DIR   = os.path.join(ROOT, "latex")      # generated macros and tables the manuscript reads
FIGURES_DIR = os.path.join(ROOT, "figures")    # generated figures the manuscript includes
LOGS_DIR    = os.path.join(ROOT, "logs")       # one log per step, kept so a run can be audited

# A second run must never overwrite the first. Set PAPER_OUT_DIR to redirect everything a step writes.
if os.environ.get("PAPER_OUT_DIR"):
    _out = os.environ["PAPER_OUT_DIR"]
    RESULTS_DIR, LATEX_DIR, FIGURES_DIR, LOGS_DIR = (
        os.path.join(_out, d) for d in ("results", "latex", "figures", "logs"))

RANDOM_STATE = 42

for _d in (RESULTS_DIR, LATEX_DIR, FIGURES_DIR, LOGS_DIR):
    os.makedirs(_d, exist_ok=True)
