#!/usr/bin/env python3
"""Build Xiaohongshu (RED) carousel cards introducing the AstraBuild work.

Seven 1080x1440 portrait cards, Chinese, light visual system aligned with the
paper figures. Output: social/xiaohongshu/card_NN.png
"""
from __future__ import annotations

import base64
import html
import io
import sys
import unicodedata
from pathlib import Path

import cairosvg
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "rewrite_b01_b36" / "figure_v24"))
from build_figure_v24 import relight_dark
OUT = HERE / "xiaohongshu"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1440

BG = "#fbfcfe"
INK = "#1f2a44"
BODY = "#37455e"
MUTED = "#5b6b84"
LINE = "#d7dfe9"
BLUE, PURPLE, ORANGE, TEAL, RED = "#4d87d7", "#8f70da", "#db8b33", "#3d9a92", "#d86c6c"
SOFT_BLUE, SOFT_PURPLE, SOFT_ORANGE, SOFT_TEAL, SOFT_RED = "#edf4ff", "#f4efff", "#fff3e8", "#e9f7f5", "#fff1f1"
SANS = "Noto Sans CJK SC"
SERIF = "Noto Serif CJK SC"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text_width_em(s: str) -> float:
    w = 0.0
    for ch in s:
        w += 1.0 if unicodedata.east_asian_width(ch) in ("W", "F") else 0.56
    return w


def wrap_cjk(s: str, max_em: float) -> list[str]:
    lines, cur, cur_w = [], "", 0.0
    for ch in s:
        if ch == "\n":
            lines.append(cur)
            cur, cur_w = "", 0.0
            continue
        cw = 1.0 if unicodedata.east_asian_width(ch) in ("W", "F") else 0.56
        if cur_w + cw > max_em and cur:
            lines.append(cur)
            cur, cur_w = "", 0.0
        cur += ch
        cur_w += cw
    lines.append(cur)
    return lines


def text(s, x, y, width, size=28, weight="400", fill=BODY, anchor="start", family=SANS, line_height=1.35, spacing=None):
    max_em = width / size
    lines = []
    for para in s.split("\n"):
        lines.extend(wrap_cjk(para, max_em))
    tspans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else size * line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}"{ls}>' + "".join(tspans) + "</text>",
            len(lines))


def rect(x, y, w, h, fill="white", stroke=LINE, sw=2, rx=20, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def img_b64(path: Path, max_px=1400, light=False) -> str:
    im = Image.open(path).convert("RGB")
    if light:
        im = relight_dark(im)
    if max(im.size) > max_px:
        r = max_px / max(im.size)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


_clip_id = [0]


def image(path, x, y, w, h, rx=16, light=False):
    _clip_id[0] += 1
    cid = f"clip{_clip_id[0]}"
    href = img_b64(Path(path), light=light)
    return (f'<defs><clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#e9edf3"/>'
            f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{href}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')


def chip(s, x, y, color=BLUE, soft=SOFT_BLUE, size=24):
    w = text_width_em(s) * size + 44
    return (rect(x, y, w, 52, soft, color, 2, 26) +
            text(s, x + w / 2, y + 35, w - 20, size, "700", color, "middle")[0]), w


def page_no(n, total=7):
    return text(f"{n} / {total}", W - 60, H - 44, 100, 22, "700", MUTED, "end")[0]


def brand():
    return (f'<circle cx="72" cy="70" r="14" fill="{TEAL}"/>' +
            text("AstraBuild", 100, 82, 400, 34, "800", INK, family=SERIF)[0])


def card(title_parts):
    """Start a card: background + optional kicker/title block. Returns svg list."""
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append(rect(-10, -10, W + 20, H + 20, BG, "none", 0, 0))
    return svg


def save(name, svg):
    svg.append("</svg>")
    out_svg = OUT / f"{name}.svg"
    out_svg.write_text("".join(svg), encoding="utf-8")
    png_dir = OUT / "png"
    png_dir.mkdir(exist_ok=True)
    cairosvg.svg2png(url=str(out_svg), write_to=str(png_dir / f"{name}.png"), output_width=W, output_height=H)
    print(png_dir / f"{name}.png")


STATION = REPO / "media/cases/station_side.png"
FIELD = REPO / "media/field_gis.jpg"
GIS = REPO / "media/cases/gis220.png"
B15_BEFORE = REPO / "media/cases/b15_before.png"
B15_AFTER = REPO / "media/cases/b15_after.png"


def card01_cover():
    svg = card(None)
    svg.append(brand())
    svg.append(text("研究实录 · 工业三维重建", 100, 140, 500, 26, "700", TEAL, spacing="0.12em")[0])
    svg.append(text("让 GPT-6 重建一座", 84, 320, 920, 96, "900", INK, family=SANS)[0])
    svg.append(text("220 kV 变电站", 84, 436, 920, 96, "900", INK, family=SANS)[0])
    svg.append(text("36 批连续作业，通用推理智能体的工业数字孪生实录", 86, 512, 900, 36, "400", MUTED)[0])
    svg.append(image(STATION, 84, 600, 912, 540, 24))
    x = 84
    for s, c, sf in [("GPT-6 Astra / Codex", BLUE, SOFT_BLUE), ("Blender 可执行程序", PURPLE, SOFT_PURPLE), ("摄影测量证据", TEAL, SOFT_TEAL)]:
        csvg, cw = chip(s, x, 1200, c, sf, 25)
        svg.append(csvg)
        x += cw + 20
    svg.append(text("论文 + 数据 + 视频全公开", 86, 1330, 700, 28, "700", BODY)[0])
    svg.append(page_no(1))
    save("card_01_cover", svg)


def stat(svg, x, y, w, num, label, color):
    svg.append(text(num, x + w / 2, y, w, 64, "900", color, "middle", family=SANS)[0])
    svg.append(text(label, x + w / 2, y + 42, w, 25, "400", MUTED, "middle")[0])


def card02_what():
    svg = card(None)
    svg.append(brand())
    svg.append(text("我们做了什么", 84, 160, 700, 26, "700", TEAL, spacing="0.12em")[0])
    svg.append(text("一座真实变电站的\n36 批重建实录", 84, 250, 920, 62, "900", INK, line_height=1.28)[0])
    y = 470
    stat(svg, 84, y, 280, "36", "重建批次 B01–B36", BLUE)
    stat(svg, 400, y, 280, "4", "四个描述阶段", PURPLE)
    stat(svg, 716, y, 280, "36,812", "最终工程对象", TEAL)
    svg.append(image(FIELD, 84, 620, 444, 320, 20))
    svg.append(image(GIS, 552, 620, 444, 320, 20, light=True))
    svg.append(text("现场影像证据", 306, 990, 400, 26, "700", MUTED, "middle")[0])
    svg.append(text("重建部件模型", 774, 990, 400, 26, "700", MUTED, "middle")[0])
    svg.append(rect(84, 1050, 912, 200, "white", LINE, 2, 20))
    svg.append(text("输入：注册摄影测量几何、现场照片、工程记录，以及上一批留下的 Blender 状态。\n输出：可编辑、可验证、可持续演化的工程三维模型。", 120, 1118, 840, 30, "400", BODY, line_height=1.5)[0])
    svg.append(page_no(2))
    save("card_02_what", svg)


def loop_step(svg, y, idx, title_s, desc, color, soft):
    svg.append(rect(104, y, 872, 150, soft, color, 2.5, 22))
    svg.append(f'<circle cx="170" cy="{y+75}" r="34" fill="{color}"/>')
    svg.append(text(str(idx), 170, y + 87, 60, 38, "900", "white", "middle")[0])
    svg.append(text(title_s, 232, y + 60, 700, 34, "800", INK)[0])
    svg.append(text(desc, 232, y + 108, 710, 26, "400", BODY)[0])


def card03_how():
    svg = card(None)
    svg.append(brand())
    svg.append(text("工作方式", 84, 160, 700, 26, "700", TEAL, spacing="0.12em")[0])
    svg.append(text("模型做决策\n代码做计算", 84, 250, 920, 62, "900", INK, line_height=1.28)[0])
    steps = [
        ("证据 + 继承状态", "摄影测量粗模、现场影像、上一批的工程状态", BLUE, SOFT_BLUE),
        ("模型编写可执行程序", "选证据、选表示、写 Blender/Python 操作", PURPLE, SOFT_PURPLE),
        ("确定性工具构建与验证", "拟合、变换、端点检查、碰撞检查全在代码里", ORANGE, SOFT_ORANGE),
        ("被接受的结果成为新状态", "命名 collection、端口、端点供后续批次寻址", TEAL, SOFT_TEAL),
    ]
    y = 470
    for i, (t, d, c, sf) in enumerate(steps, 1):
        loop_step(svg, y, i, t, d, c, sf)
        if i < 4:
            svg.append(f'<path d="M540,{y+154} V{y+196}" stroke="{MUTED}" stroke-width="4" stroke-linecap="round" marker-end="url(#dn)"/>')
        y += 200
    svg.append('<defs><marker id="dn" markerWidth="9" markerHeight="9" refX="4.5" refY="7" orient="auto"><path d="M0,0 L9,0 L4.5,8 z" fill="' + MUTED + '"/></marker></defs>')
    svg.append(rect(84, 1258, 912, 96, SOFT_TEAL, TEAL, 2, 18))
    svg.append(text("厘米级一致性来自确定性几何代码，不是模型的“手感”", 540, 1318, 860, 30, "800", INK, "middle")[0])
    svg.append(page_no(3))
    save("card_03_how", svg)


def ladder(svg, y, title_s, status, desc, color, soft, w=912):
    svg.append(rect(84, y, w, 158, soft, color, 2.5, 22))
    svg.append(text(title_s, 124, y + 56, 560, 36, "800", INK)[0])
    svg.append(text(desc, 124, y + 104, 560, 25, "400", BODY)[0])
    svg.append(rect(700, y + 46, 260, 64, "white", color, 2.5, 32))
    svg.append(text(status, 830, y + 88, 240, 27, "800", color, "middle")[0])


def rate(svg, y, label, num, den, color, soft):
    svg.append(text(label, 104, y, 420, 27, "700", INK)[0])
    svg.append(text(f"{num}/{den}", 956, y, 100, 26, "700", MUTED, "end")[0])
    bar_y = y + 16
    svg.append(rect(104, bar_y, 852, 34, "#eef1f6", LINE, 1.5, 17))
    bw = max(40, 852 * num / den)
    svg.append(rect(104, bar_y, bw, 34, soft, color, 2, 17))
    pct = f"{num/den:.0%}"
    svg.append(text(pct, 104 + bw - 16, bar_y + 25, 80, 24, "800", color, "end")[0])


def card04_finding1():
    svg = card(None)
    svg.append(brand())
    svg.append(text("发现一", 84, 160, 700, 26, "700", ORANGE, spacing="0.12em")[0])
    svg.append(text("难的不是画图\n是想清楚要画什么", 84, 250, 920, 60, "900", INK, line_height=1.28)[0])
    y = 460
    ladder(svg, y, "① 几何拟合", "始终成立", "36 批全程在线，零拟合失败记录", TEAL, SOFT_TEAL)
    ladder(svg, y + 182, "② 问题定义", "就地修订", "比较域、复用边界、表示、任务选择", ORANGE, SOFT_ORANGE)
    ladder(svg, y + 364, "③ 跨批次抽象", "传播风险", "B15 共享母线节把错误带进多个安装位", RED, SOFT_RED)
    svg.append(text("多轮修订批次占比（按阶段）", 84, 1080, 700, 30, "800", INK)[0])
    bands = [("B01–06 局部拟合", 4, 6, BLUE, SOFT_BLUE), ("B07–19 重复设备", 13, 13, PURPLE, SOFT_PURPLE),
             ("B20–30 连接系统", 5, 11, ORANGE, SOFT_ORANGE), ("B31–36 整站收尾", 5, 6, TEAL, SOFT_TEAL)]
    y = 1130
    for label, n, d, c, sf in bands:
        rate(svg, y, label, n, d, c, sf)
        y += 68
    svg.append(page_no(4))
    save("card_04_finding1", svg)


def duel(svg, x, w, title_s, color, soft, lines):
    svg.append(rect(x, 480, w, 500, soft, color, 2.5, 22))
    svg.append(text(title_s, x + w / 2, 540, w - 40, 36, "900", color, "middle")[0])
    y = 620
    for ln in lines:
        t, n = text("· " + ln, x + 36, y, w - 72, 27, "400", BODY, line_height=1.45)
        svg.append(t)
        y += n * 27 * 1.45 + 22


def card05_finding2():
    svg = card(None)
    svg.append(brand())
    svg.append(text("发现二", 84, 160, 700, 26, "700", TEAL, spacing="0.12em")[0])
    svg.append(text("持续状态是\n一把双刃剑", 84, 250, 920, 60, "900", INK, line_height=1.28)[0])
    duel(svg, 84, 444, "组合", TEAL, SOFT_TEAL,
         ["B23 的新引线直接接到 B08 建好的端子上",
          "B29 的导线挂到既有线夹端点",
          "B36 在 36,615 个既有对象、7,114 个变换之上收尾"])
    duel(svg, 552, 444, "传播", RED, SOFT_RED,
         ["B15 的共享母线节范围出错",
          "同一通道把错误带进每个复用安装位",
          "直到“复用边界”本身被修订才止住"])
    svg.append(rect(84, 1060, 912, 250, "white", LINE, 2, 20))
    svg.append(text("没有持续状态，36 步的长链条根本不可能；\n但上游的一个抽象决定，也会成为下游问题的一部分。", 540, 1150, 830, 32, "700", INK, "middle", line_height=1.6)[0])
    svg.append(page_no(5))
    save("card_05_finding2", svg)


def card06_compare():
    svg = card(None)
    svg.append(brand())
    svg.append(text("现场直击", 84, 160, 700, 26, "700", PURPLE, spacing="0.12em")[0])
    svg.append(text("同一机位\n修订前 vs 修订后", 84, 250, 920, 60, "900", INK, line_height=1.28)[0])
    svg.append(image(B15_BEFORE, 84, 470, 444, 340, 20))
    svg.append(image(B15_AFTER, 552, 470, 444, 340, 20))
    svg.append(rect(84, 830, 444, 60, SOFT_RED, RED, 2, 14))
    svg.append(text("修订前：共享模型重叠", 306, 870, 400, 27, "800", RED, "middle")[0])
    svg.append(rect(552, 830, 444, 60, SOFT_TEAL, TEAL, 2, 14))
    svg.append(text("修订后：站点各自建模", 774, 870, 400, 27, "800", TEAL, "middle")[0])
    svg.append(rect(84, 950, 912, 400, "white", LINE, 2, 20))
    body = ("B15 批次里，智能体发现“所有安装位共享同一母线节模型”与现场物理间距不符。\n\n"
            "它没有硬调参数，而是重新划定复用边界：有限管节与支撑移出共享主模型，改为站点各自建模。\n\n测量问题本身，才是工程决策。")
    svg.append(text(body, 120, 1020, 840, 29, "400", BODY, line_height=1.55)[0])
    svg.append(page_no(6))
    save("card_06_compare", svg)


def link_row(svg, y, label, value, color, soft):
    svg.append(rect(84, y, 912, 92, soft, color, 2, 18))
    svg.append(text(label, 124, y + 58, 200, 30, "800", color)[0])
    svg.append(text(value, 340, y + 58, 620, 28, "700", INK)[0])


def card07_end():
    svg = card(None)
    svg.append(brand())
    svg.append(text("完整记录已公开", 84, 250, 920, 66, "900", INK)[0])
    svg.append(text("12 页论文 · 36 批次档案 · 同机位对比视频", 86, 330, 900, 32, "400", MUTED)[0])
    svg.append(image(STATION, 84, 420, 912, 460, 24))
    y = 960
    link_row(svg, y, "项目网站", "cookiegg.github.io/AstraBuild", BLUE, SOFT_BLUE)
    link_row(svg, y + 116, "开源仓库", "github.com/cookiegg/AstraBuild", PURPLE, SOFT_PURPLE)
    link_row(svg, y + 232, "论文 PDF", "站内 Paper (PDF) 直达", TEAL, SOFT_TEAL)
    svg.append(text("AstraBuild · 2026", 540, 1370, 600, 26, "700", MUTED, "middle")[0])
    svg.append(page_no(7))
    save("card_07_end", svg)


def main():
    card01_cover()
    card02_what()
    card03_how()
    card04_finding1()
    card05_finding2()
    card06_compare()
    card07_end()


if __name__ == "__main__":
    main()
