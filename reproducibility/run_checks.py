"""Regenerate public outputs and run the complete 76-check Python–Excel QA."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

for script in ("run_analysis.py", "make_charts.py", "qa_reconcile.py"):
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)

