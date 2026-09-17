#!/usr/bin/env python3
"""Build the descriptive B01-B36 operator matrix and Figure 3.

The source catalog is generated from preserved historical filenames/scripts. The
matrix is descriptive workflow evidence, not action telemetry or a performance
metric. Absence of a named stage does not imply absence of reasoning or failure.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

HERE = Path(__file__).resolve().parent
ASTRABUILD = HERE.parent
CATALOG = ASTRABUILD / "release" / "process_catalog.json"
DATA_DIR = HERE / "data"
FIG_DIR = HERE / "figures"

# Raw catalog stage -> reader-facing row. Interactive review is derived from the
# preserved original review HTML rather than the optional review script stage.
ROWS = [
    ("Fit", lambda d: "fit" in d["stages"]),
    ("Measure", lambda d: "measure" in d["stages"]),
    ("Inspect", lambda d: "inspect" in d["stages"]),
    ("Plan", lambda d: "plan" in d["stages"]),
    ("Refine", lambda d: "refine" in d["stages"]),
    ("Audit", lambda d: "audit" in d["stages"]),
    ("Interactive review", lambda d: bool(d.get("review_page"))),
    ("Discover / features", lambda d: any(x in d["stages"] for x in ("discover", "features"))),
    ("Collision", lambda d: "collision" in d["stages"]),
]

BANDS = [
    (1, 6, "Local fitted structures"),
    (7, 19, "Repeated equipment"),
    (20, 30, "Connected systems"),
    (31, 36, "Site closure"),
]


def load_batches() -> list[dict]:
    catalog = json.loads(CATALOG.read_text())
    batches = []
    for d in catalog["dossiers"]:
        bid = d.get("batch", "")
        if re.fullmatch(r"B\d\d", bid) and 1 <= int(bid[1:]) <= 36:
            batches.append(d)
    batches.sort(key=lambda d: int(d["batch"][1:]))
    assert [d["batch"] for d in batches] == [f"B{i:02d}" for i in range(1, 37)]
    return batches


def write_csv(batches: list[dict], matrix: np.ndarray) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "operator_matrix_b01_b36.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["operator", *[d["batch"] for d in batches]])
        for (label, _), row in zip(ROWS, matrix):
            w.writerow([label, *row.astype(int).tolist()])


def draw(batches: list[dict], matrix: np.ndarray) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(15.2, 5.6))
    # Empty cells carry the band tint; filled cells stay crisp ink. Build the
    # RGB array directly so tints never wash over the ink cells.
    def hex2rgb(h):
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (1, 3, 5))
    BAND_TINTS = ["#EAF1FA", "#F0EDF7", "#FAF1E5", "#EAF6F3"]
    INK_CELL = hex2rgb("#253347")
    rgb = np.zeros((len(ROWS), 36, 3))
    for col in range(36):
        tint = next(hex2rgb(t) for (a, b, _), t in zip(BANDS, BAND_TINTS) if a - 1 <= col <= b - 1)
        rgb[:, col, :] = tint
    rgb[matrix == 1] = INK_CELL
    ax.imshow(rgb, aspect="auto", interpolation="nearest")
    ax.set_yticks(range(len(ROWS)))
    ax.set_yticklabels([r[0] for r in ROWS], fontsize=10.5)
    ax.set_xticks(range(36))
    ax.set_xticklabels([d["batch"] for d in batches], rotation=90, fontsize=8.5)
    ax.set_xlabel("Sequential reconstruction batch", fontsize=10.5)
    for i, (label, _) in enumerate(ROWS):
        ax.text(36.0, i, f"{int(matrix[i].sum())}/36", ha="left", va="center",
                fontsize=9.5, color="#5F6B7A", clip_on=False)

    # Thin cell boundaries improve readability without turning the figure into a table.
    ax.set_xticks(np.arange(-0.5, 36, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(ROWS), 1), minor=True)
    ax.grid(which="minor", linewidth=0.25, alpha=0.28)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Mark descriptive target-band boundaries and label them above the heatmap.
    for start, end, label in BANDS:
        x0 = start - 1
        x1 = end - 1
        if start > 1:
            ax.axvline(x0 - 0.5, linewidth=1.15, color="black")
        xc = (x0 + x1) / 2
        ax.text(xc, -1.00, label, ha="center", va="bottom", fontsize=10.5, fontweight="bold", clip_on=False)

    ax.set_title(
        "B01-B36 operator portfolio reconstructed from preserved workflow artifacts",
        fontsize=13.5,
        pad=34,
    )
    fig.subplots_adjust(left=0.12, right=0.94, top=0.84, bottom=0.20)
    fig.savefig(FIG_DIR / "fig03_operator_portfolio_b01_b36.svg", bbox_inches="tight")
    fig.savefig(FIG_DIR / "fig03_operator_portfolio_b01_b36.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "fig03_operator_portfolio_b01_b36.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    batches = load_batches()
    matrix = np.array([[fn(d) for d in batches] for _, fn in ROWS], dtype=int)
    write_csv(batches, matrix)
    draw(batches, matrix)
    print("operator matrix:", DATA_DIR / "operator_matrix_b01_b36.csv")
    print("figure:", FIG_DIR / "fig03_operator_portfolio_b01_b36.svg")
    print("rows:", {label: int(row.sum()) for (label, _), row in zip(ROWS, matrix)})


if __name__ == "__main__":
    main()
