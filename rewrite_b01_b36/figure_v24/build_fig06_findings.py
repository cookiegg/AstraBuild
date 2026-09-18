#!/usr/bin/env python3
"""Build Figure 6 (Findings): decision-layer ladder + per-band multi-revision rates.

Reuses the v2.4 visual system from build_figure_v24. Content:
- left: three decision layers (fitting strong / problem definition revised in
  place / cross-batch abstraction propagation risk);
- right: share of batches with >=2 visible revision tags per descriptive band
  (4/6, 13/13, 5/11, 5/6 from release/behavior_analysis.json).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cairosvg
from build_figure_v24 import (  # noqa: E402
    BG, TITLE, BODY, MUTED, GRID, ARROW,
    BLUE, PURPLE, ORANGE, TEAL, RED,
    SOFT_BLUE, SOFT_PURPLE, SOFT_ORANGE, SOFT_TEAL, SOFT_RED,
    SANS, SERIF, SVG_DIR, PDF_DIR, PNG_DIR, REPO,
    text, rect, defs, header, panel, pill,
)

W, H = 1600, 700

BANDS = [
    ("B01–B06", "local fits", 4, 6, BLUE, SOFT_BLUE),
    ("B07–B19", "repeated equipment", 13, 13, PURPLE, SOFT_PURPLE),
    ("B20–B30", "connected systems", 5, 11, ORANGE, SOFT_ORANGE),
    ("B31–B36", "site closure", 5, 6, TEAL, SOFT_TEAL),
]

LAYERS = [
    ("1 · Geometric fitting", "STRONG · 36/36", TEAL, SOFT_TEAL,
     "fit + validate run in every batch; no documented fitting failure"),
    ("2 · Problem definition", "REVISED IN PLACE · 5 episodes", ORANGE, SOFT_ORANGE,
     "comparison domain · reuse boundary · representation · task selection"),
    ("3 · Cross-batch abstraction", "PROPAGATION RISK", RED, SOFT_RED,
     "B15 shared spool carried a wrong extent into later installations"),
]


def ladder_card(svg, x, y, w, h, title_s, status, color, soft, desc):
    svg.append(rect(x, y, w, h, soft, color, 1.8, 16))
    svg.append(text(title_s, x + 26, y + 38, w - 220, 21, "700", fill=TITLE, anchor="start", family=SANS))
    pw = 300
    pill(svg, x + w - pw - 20, y + 18, pw, 34, status, fill="white", stroke=color, size=13)
    svg.append(text(desc, x + 26, y + 68, w - 52, 14.5, fill=BODY, anchor="start", family=SANS))


def down_arrow(svg, cx, y1, y2, color=ARROW, dash=False):
    dash_attr = ' stroke-dasharray="7 7"' if dash else ""
    marker = "arrowRed" if color == RED else "arrow"
    svg.append(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-linecap="round"{dash_attr} marker-end="url(#{marker})"/>')


def rate_bar(svg, x, y, w, band, label, num, den, color, soft):
    rate = num / den
    svg.append(text(f"{band} · {label}", x, y, w, 16, "700", fill=TITLE, anchor="start", family=SANS))
    svg.append(text(f"{num}/{den}", x + w, y, 120, 15, "700", fill=MUTED, anchor="end", family=SANS))
    bar_y = y + 12
    svg.append(rect(x, bar_y, w, 30, "#f2f5fa", GRID, 1.2, 15))
    bw = max(34, w * rate)
    svg.append(rect(x, bar_y, bw, 30, soft, color, 1.8, 15))
    pct = f"{rate:.0%}"
    if bw > 90:
        svg.append(text(pct, x + bw - 14, bar_y + 21, 60, 16, "800", fill=color, anchor="end", family=SANS))
    else:
        svg.append(text(pct, x + bw + 14, bar_y + 21, 60, 16, "800", fill=color, anchor="start", family=SANS))


def build_fig6():
    svg: list[str] = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append(defs())
    svg.append('<defs><marker id="arrowRed" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">'
               f'<path d="M0,0 L8,4 L0,8 z" fill="{RED}"/></marker></defs>')
    svg.append(rect(0, 0, W, H, BG, "none", 0, 0))
    header(svg, "The bottleneck migrates from fitting to problem definition",
           "no documented fitting failure in 36 batches · revision concentrates where new abstractions are defined")

    # Left: decision-layer ladder
    lx, ly, lw, lh = 40, 116, 880, 500
    panel(svg, lx, ly, lw, lh, "Decision layers", "#f4f7fb", GRID)
    card_h, gap = 112, 30
    cy = ly + 62
    for i, (title_s, status, color, soft, desc) in enumerate(LAYERS):
        ladder_card(svg, lx + 32, cy, lw - 64, card_h, title_s, status, color, soft, desc)
        if i < 2:
            down_arrow(svg, lx + lw / 2, cy + card_h + 2, cy + card_h + gap - 4,
                       color=(RED if i == 1 else ARROW), dash=(i == 1))
        cy += card_h + gap

    # Right: per-band multi-revision rates
    rx, ry, rw, rh = 960, 116, 600, 500
    panel(svg, rx, ry, rw, rh, "Batches with ≥2 revisions, by band", "#f4f7fb", GRID)
    by = ry + 92
    bar_w = rw - 64
    for band, label, num, den, color, soft in BANDS:
        rate_bar(svg, rx + 32, by, bar_w, band, label, num, den, color, soft)
        by += 88
    svg.append(text("visible _rN tags · filename-based lower bound, read as a distribution",
                    rx + rw / 2, ry + rh - 24, rw - 48, 13, fill=MUTED, family=SANS))

    svg.append("</svg>")
    out = SVG_DIR / "fig06_findings_v24.svg"
    out.write_text("".join(svg), encoding="utf-8")
    cairosvg.svg2pdf(url=str(out), write_to=str(PDF_DIR / "fig06_findings_v24.pdf"))
    cairosvg.svg2png(url=str(out), write_to=str(PNG_DIR / "fig06_findings_v24.png"), output_width=W)
    print(out.relative_to(REPO))


if __name__ == "__main__":
    build_fig6()
