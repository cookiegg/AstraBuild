#!/usr/bin/env python3
"""Build Figure 7: session anatomy of the 22.5 h B01-B36 conversation run.

Lanes: batch timeline bands, reasoning tokens per batch, human interventions
(with the three trajectory-changing messages highlighted and the 17.8 h
unattended span bracketed), and 24 context-compaction ticks.
Data: release/conversation_batch_metrics.json (+ frozen intervention facts).
EN default; `zh` argument builds the Chinese variant.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cairosvg
from build_figure_v24 import (  # noqa: E402
    BG, TITLE, BODY, MUTED, GRID, ARROW,
    BLUE, PURPLE, ORANGE, TEAL, RED,
    SOFT_BLUE, SOFT_PURPLE, SOFT_ORANGE, SOFT_TEAL, SOFT_RED,
    SANS, SERIF, SVG_DIR, PDF_DIR, PNG_DIR, REPO,
    text, rect, defs,
)

W, H = 1600, 880
X0, X1 = 90, 1560

METRICS = json.loads((REPO / "release" / "conversation_batch_metrics.json").read_text())


def minutes(ts: str) -> float:
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return t.timestamp() / 60.0


T0 = minutes("2026-09-12T08:16:45Z")
T1 = minutes("2026-09-13T06:44:55Z")


def fx(ts: str) -> float:
    return X0 + (X1 - X0) * (minutes(ts) - T0) / (T1 - T0)


BAND_OF = {}
for b in [f"B{i:02d}" for i in range(1, 7)]:
    BAND_OF[b] = (BLUE, SOFT_BLUE)
for b in [f"B{i:02d}" for i in range(7, 20)]:
    BAND_OF[b] = (PURPLE, SOFT_PURPLE)
for b in [f"B{i:02d}" for i in range(20, 31)]:
    BAND_OF[b] = (ORANGE, SOFT_ORANGE)
for b in [f"B{i:02d}" for i in range(31, 37)]:
    BAND_OF[b] = (TEAL, SOFT_TEAL)

HUMAN = [
    ("2026-09-12T08:16:45Z", False, "start"),
    ("2026-09-12T08:21:00Z", False, ""),
    ("2026-09-12T08:52:00Z", True, "wall"),
    ("2026-09-12T09:02:00Z", False, ""),
    ("2026-09-12T10:19:00Z", False, ""),
    ("2026-09-12T10:58:00Z", False, ""),
    ("2026-09-12T11:00:00Z", True, "reuse"),
    ("2026-09-12T11:45:00Z", False, ""),
    ("2026-09-13T05:35:00Z", True, "omission"),
    ("2026-09-13T06:07:00Z", False, ""),
]

EN = {
    "title": "22.5 hours, 36 batches, one persistent state",
    "subtitle": "the preserved conversation run: 12 human messages, 3 of which changed the trajectory",
    "batch_lane": "batches (first mention in log)",
    "reason_lane": "reasoning tokens / batch",
    "human_lane": "human messages",
    "unattended": "17.8 h unattended (19 auto-continuations)",
    "wall": "wall geometry review",
    "reuse": "reuse authorization (B08)",
    "omission": "omission report (B36)",
    "compactions": "24 context compactions",
    "peak12": "B12: first GIS family",
    "peak25": "B25: coverage audit",
    "sans": SANS, "serif": SERIF, "stem": "fig07_session_anatomy_v24",
}
ZH = {
    "title": "22.5 小时，36 个批次，一份持续状态",
    "subtitle": "保存的会话实录：12 条人工消息，其中 3 条改变了轨迹",
    "batch_lane": "批次（日志中首次提及）",
    "reason_lane": "每批 reasoning token",
    "human_lane": "人工消息",
    "unattended": "17.8 小时无人值守（19 次自动续跑）",
    "wall": "围墙几何复核",
    "reuse": "复用授权（B08）",
    "omission": "遗漏报告（B36）",
    "compactions": "24 次上下文压缩",
    "peak12": "B12：首个 GIS 设备族",
    "peak25": "B25：覆盖审计",
    "sans": "Noto Sans CJK SC", "serif": "Noto Serif CJK SC", "stem": "fig07_session_anatomy_v24_zh",
}

LABEL_BATCHES = {"B01", "B07", "B08", "B12", "B15", "B20", "B23", "B25", "B29", "B31", "B36"}


def build(T=EN):
    font, serif = T["sans"], T["serif"]
    batches = METRICS["batches"]
    starts = [(b, batches[b]["first_mention"]) for b in sorted(batches) if batches[b]["first_mention"]]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append(defs())
    svg.append(rect(0, 0, W, H, BG, "none", 0, 0))
    svg.append(text(T["title"], W / 2, 52, W - 100, 34, "700", fill=TITLE, family=serif))
    svg.append(text(T["subtitle"], W / 2, 92, W - 140, 18, fill=MUTED, family=font))

    # Lane A: batch bands
    ay, ah = 150, 86
    svg.append(text(T["batch_lane"], X0, ay - 14, 500, 15, "700", fill=MUTED, anchor="start", family=font))
    for i, (b, st) in enumerate(starts):
        en = starts[i + 1][1] if i + 1 < len(starts) else "2026-09-13T06:44:55Z"
        x_a, x_b = fx(st), fx(en)
        color, soft = BAND_OF[b]
        svg.append(rect(x_a, ay, max(2.0, x_b - x_a - 1.5), ah, soft, "none", 0, 3))
        if b in LABEL_BATCHES:
            if b == "B01":
                svg.append(text(b, X0, ay + ah / 2 + 6, 60, 15, "800", fill=color, anchor="start", family=font))
            else:
                svg.append(text(b, (x_a + x_b) / 2, ay + ah / 2 + 6, x_b - x_a + 30, 15, "800", fill=color, family=font))
    # unattended bracket
    ua, ub = fx("2026-09-12T11:45:00Z"), fx("2026-09-13T05:35:00Z")
    svg.append(f'<path d="M{ua},{ay+ah+10} V{ay+ah+22} H{ub} V{ay+ah+10}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5"/>')
    svg.append(text(T["unattended"], (ua + ub) / 2, ay + ah + 44, ub - ua, 15, "700", fill=RED, family=font))
    # compaction ticks
    cy = ay + ah + 66
    for c in METRICS["compactions"]:
        x = fx(c)
        svg.append(f'<line x1="{x}" y1="{cy}" x2="{x}" y2="{cy+12}" stroke="{MUTED}" stroke-width="1.6"/>')
    svg.append(text(T["compactions"], fx("2026-09-12T08:20:00Z"), cy + 32, 400, 13.5, fill=MUTED, anchor="start", family=font))

    # Lane B: reasoning tokens
    ry, rh = 400, 200
    svg.append(text(T["reason_lane"], X0, ry - 14, 500, 15, "700", fill=MUTED, anchor="start", family=font))
    max_r = max(v["reasoning_tokens"] for v in batches.values())
    for i, (b, st) in enumerate(starts):
        en = starts[i + 1][1] if i + 1 < len(starts) else "2026-09-13T06:44:55Z"
        x_a, x_b = fx(st), fx(en)
        v = batches[b]["reasoning_tokens"]
        bh = rh * v / max_r
        color, soft = BAND_OF[b]
        svg.append(f'<rect x="{x_a}" y="{ry + rh - bh}" width="{max(2.0, x_b - x_a - 1.5)}" height="{bh}" rx="2" fill="{color}" opacity="0.82"/>')
    svg.append(f'<line x1="{X0}" y1="{ry+rh}" x2="{X1}" y2="{ry+rh}" stroke="{GRID}" stroke-width="1.5"/>')
    for b, lab, dx in [("B12", T["peak12"], 0), ("B25", T["peak25"], 0)]:
        st = batches[b]["first_mention"]
        x = fx(st) + 8
        bh = rh * batches[b]["reasoning_tokens"] / max_r
        svg.append(text(lab, x, ry + rh - bh - 12, 320, 14, "700", fill=BODY, anchor="start", family=font))

    # Lane C: human messages
    hy = 720
    svg.append(text(T["human_lane"], X0, hy - 26, 400, 15, "700", fill=MUTED, anchor="start", family=font))
    svg.append(f'<line x1="{X0}" y1="{hy}" x2="{X1}" y2="{hy}" stroke="{GRID}" stroke-width="1.5"/>')
    for ts, major, key in HUMAN:
        x = fx(ts)
        if major:
            svg.append(f'<path d="M{x},{hy-12} L{x+9},{hy} L{x},{hy+12} L{x-9},{hy} Z" fill="{RED}"/>')
            svg.append(f'<line x1="{x}" y1="{hy-12}" x2="{x}" y2="{ry+rh+8}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="4 5"/>')
            anch, tx = (("middle", max(170, x)) if key == "wall" else
                        (("end", x - 14) if key == "omission" else ("start", x + 14)))
            svg.append(text(T[key], tx, hy + 34, 250, 14.5, "700", fill=RED, anchor=anch, family=font))
        else:
            svg.append(f'<circle cx="{x}" cy="{hy}" r="5" fill="{MUTED}"/>')
    # time axis labels
    for i, lab in enumerate(["09-12 16:16", "20:00", "00:00", "04:00", "09-13 06:44"]):
        frac = i / 4
        anch = "start" if i == 0 else ("end" if i == 4 else "middle")
        svg.append(text(lab, X0 + (X1 - X0) * frac, H - 26, 160, 13.5, fill=MUTED, anchor=anch, family=font))

    svg.append("</svg>")
    stem = T["stem"]
    out = SVG_DIR / f"{stem}.svg"
    out.write_text("".join(svg), encoding="utf-8")
    cairosvg.svg2pdf(url=str(out), write_to=str(PDF_DIR / f"{stem}.pdf"))
    cairosvg.svg2png(url=str(out), write_to=str(PNG_DIR / f"{stem}.png"), output_width=W)
    print(out.relative_to(REPO))


if __name__ == "__main__":
    build(EN)
    if len(sys.argv) > 1 and sys.argv[1] == "zh":
        build(ZH)
