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

EN = {
    "title": "Documented failures concentrate at the problem-definition layer",
    "subtitle": "no documented fitting failure in 36 batches · revision concentrates where new abstractions are defined",
    "left": "Decision layers",
    "right": "Batches with ≥2 revisions, by band",
    "foot": "visible _rN tags · filename-based lower bound, read as a distribution",
    "bands": BANDS,
    "layers": LAYERS,
    "sans": SANS,
    "serif": SERIF,
    "stem": "fig06_findings_v24",
}

ZH_BANDS = [
    ("B01–B06", "局部拟合", 4, 6, BLUE, SOFT_BLUE),
    ("B07–B19", "重复设备", 13, 13, PURPLE, SOFT_PURPLE),
    ("B20–B30", "连接系统", 5, 11, ORANGE, SOFT_ORANGE),
    ("B31–B36", "整站收尾", 5, 6, TEAL, SOFT_TEAL),
]

ZH_LAYERS = [
    ("1 · 几何拟合", "始终成立 · 36/36", TEAL, SOFT_TEAL,
     "fit + validate 贯穿每批；无拟合失败记录"),
    ("2 · 问题定义", "就地修订 · 5 例", ORANGE, SOFT_ORANGE,
     "比较域 · 复用边界 · 表示 · 任务选择"),
    ("3 · 跨批次抽象", "传播风险", RED, SOFT_RED,
     "B15 共享母线节把错误范围带入后续安装位"),
]

ZH = {
    "title": "有记录的失败集中在问题定义层",
    "subtitle": "36 批次无一例拟合失败记录 · 修订集中在新抽象被定义之处",
    "left": "决策层",
    "right": "多轮修订批次占比（按分段）",
    "foot": "可见 _rN 标签 · 基于文件名的下界，按分布解读",
    "bands": ZH_BANDS,
    "layers": ZH_LAYERS,
    "sans": "Noto Sans CJK SC",
    "serif": "Noto Serif CJK SC",
    "stem": "fig06_findings_v24_zh",
}


def ladder_card(svg, x, y, w, h, title_s, status, color, soft, desc, font=SANS):
    svg.append(rect(x, y, w, h, soft, color, 1.8, 16))
    svg.append(text(title_s, x + 26, y + 38, w - 220, 21, "700", fill=TITLE, anchor="start", family=font))
    pw = 300
    svg.append(rect(x + w - pw - 20, y + 18, pw, 34, "white", color, 1.25, 17))
    svg.append(text(status, x + w - pw / 2 - 20, y + 40, pw - 16, 13, "700", fill=BODY, family=font, line_height=1.04))
    svg.append(text(desc, x + 26, y + 68, w - 52, 14.5, fill=BODY, anchor="start", family=font))


def down_arrow(svg, cx, y1, y2, color=ARROW, dash=False):
    dash_attr = ' stroke-dasharray="7 7"' if dash else ""
    marker = "arrowRed" if color == RED else "arrow"
    svg.append(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-linecap="round"{dash_attr} marker-end="url(#{marker})"/>')


def rate_bar(svg, x, y, w, band, label, num, den, color, soft, font=SANS):
    rate = num / den
    svg.append(text(f"{band} · {label}", x, y, w, 16, "700", fill=TITLE, anchor="start", family=font))
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


def build_fig6(T=EN):
    font, serif = T["sans"], T["serif"]
    svg: list[str] = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append(defs())
    svg.append('<defs><marker id="arrowRed" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">'
               f'<path d="M0,0 L8,4 L0,8 z" fill="{RED}"/></marker></defs>')
    svg.append(rect(0, 0, W, H, BG, "none", 0, 0))
    svg.append(text(T["title"], W / 2, 46, W - 100, 30, "700", fill=TITLE, family=serif))
    svg.append(text(T["subtitle"], W / 2, 82, W - 140, 17, fill=MUTED, family=font))

    # Left: decision-layer ladder
    lx, ly, lw, lh = 40, 116, 880, 500
    panel(svg, lx, ly, lw, lh, T["left"], "#f4f7fb", GRID)
    card_h, gap = 112, 30
    cy = ly + 62
    for i, (title_s, status, color, soft, desc) in enumerate(T["layers"]):
        ladder_card(svg, lx + 32, cy, lw - 64, card_h, title_s, status, color, soft, desc, font=font)
        if i < 2:
            down_arrow(svg, lx + lw / 2, cy + card_h + 2, cy + card_h + gap - 4,
                       color=(RED if i == 1 else ARROW), dash=(i == 1))
        cy += card_h + gap

    # Right: per-band multi-revision rates
    rx, ry, rw, rh = 960, 116, 600, 500
    panel(svg, rx, ry, rw, rh, T["right"], "#f4f7fb", GRID)
    by = ry + 92
    bar_w = rw - 64
    for band, label, num, den, color, soft in T["bands"]:
        rate_bar(svg, rx + 32, by, bar_w, band, label, num, den, color, soft, font=font)
        by += 88
    svg.append(text(T["foot"], rx + rw / 2, ry + rh - 24, rw - 48, 13, fill=MUTED, family=font))

    svg.append("</svg>")
    stem = T["stem"]
    out = SVG_DIR / f"{stem}.svg"
    out.write_text("".join(svg), encoding="utf-8")
    cairosvg.svg2pdf(url=str(out), write_to=str(PDF_DIR / f"{stem}.pdf"))
    cairosvg.svg2png(url=str(out), write_to=str(PNG_DIR / f"{stem}.png"), output_width=W)
    print(out.relative_to(REPO))


if __name__ == "__main__":
    build_fig6(EN)
    if len(sys.argv) > 1 and sys.argv[1] == "zh":
        build_fig6(ZH)
