"""Common set-up for the analysis scripts: import path, seeds and a CSV writer."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from naivesum.style import FIG_DIR  # noqa: E402

SEED = 20261010
DISTRIBUTIONS = {
    "U(0,1)": (0.0, 1.0),    # all terms positive: condition number 1
    "U(-1,1)": (-1.0, 1.0),  # mean zero, as in version 1: large condition number
}


def save_table(rows, name):
    """Write a list of dicts as figures/<name>.csv."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(FIG_DIR / f"{name}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote figures/{name}.csv ({len(rows)} rows)")
