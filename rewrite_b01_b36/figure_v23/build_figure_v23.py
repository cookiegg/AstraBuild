#!/usr/bin/env python3
"""Build Figure v2.3 hybrid SVG/PDF/PNG assets.

v2.3 restyles v2.2 after the GPT-image design references: vector icons, lifted dark renders, lane labels. It keeps the empirical content and B01--B36 provenance from figure_v2 while
improving typography, hierarchy, spacing, and transition-label readability.
Text, panels, arrows, and statistics remain vector SVG. Complex engineering
imagery is embedded from preserved historical artifacts.
"""
from __future__ import annotations

import base64
import html
import io
import textwrap
from pathlib import Path

from PIL import Image, ImageChops
import cairosvg

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HIST = REPO / "media" / "historical" / "output"
FIELD = REPO / "media" / "field_gis.jpg"
SVG_DIR = HERE / "hybrid_svg"
PDF_DIR = HERE / "hybrid_pdf"
PNG_DIR = HERE / "preview_png"
for d in (SVG_DIR, PDF_DIR, PNG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Paper-wide visual system.
BG = "#fbfcfe"
TITLE = "#1f2a44"
BODY = "#2f3b52"
MUTED = "#5b6b84"
GRID = "#cfd8e3"
ARROW = "#6f7f95"
BLUE, PURPLE, ORANGE, TEAL, RED = "#4d87d7", "#8f70da", "#db8b33", "#4aa39d", "#d86c6c"
SOFT_BLUE, SOFT_PURPLE, SOFT_ORANGE, SOFT_TEAL, SOFT_RED = "#edf4ff", "#f4efff", "#fff3e8", "#edf9f7", "#fff3f3"
SANS = "Helvetica,Arial,sans-serif"
SERIF = "Georgia,Times New Roman,serif"


def hist(rel: str) -> Path:
    p = HIST / rel
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def trim_white(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    bg = Image.new("RGB", im.size, "white")
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0)
    bbox = diff.getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    pad = max(6, int(min(im.size) * 0.012))
    bbox = (max(0, x0-pad), max(0, y0-pad), min(im.width, x1+pad), min(im.height, y1+pad))
    if (bbox[2]-bbox[0]) < im.width * 0.97 or (bbox[3]-bbox[1]) < im.height * 0.97:
        return im.crop(bbox)
    return im


def relight_dark(im: Image.Image, bg_target=(241, 243, 248), bg_tol=42, gamma=0.62) -> Image.Image:
    """Re-light dark Blender viewport renders for a light page.

    Two strategies, chosen from the image itself:
    - low-saturation content (white/gray wireframe on dark): invert, so the
      linework becomes dark ink on a light ground;
    - saturated content (cyan/colored overlays): replace the uniform dark
      viewport background with a light canvas and gamma-lift the content,
      preserving hue (important for Clean/Overlay color semantics).
    """
    import numpy as np
    a = np.asarray(im.convert("RGB"), dtype=float) / 255.0
    corners = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3),
                              a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    if bg.mean() > 0.55:  # already light; nothing to do
        return im.convert("RGB")
    dist = np.abs(a - bg).sum(axis=2)
    content = a[dist >= bg_tol / 255.0 * 3]
    sat = float(np.abs(content.max(axis=1) - content.min(axis=1)).mean()) if content.size else 0.0
    if sat < 0.03:
        return Image.fromarray(((1.0 - a) * 255).astype("uint8"))
    mask = dist < bg_tol / 255.0 * 3
    out = np.power(a, gamma)
    out[mask] = np.array(bg_target) / 255.0
    return Image.fromarray((out * 255).astype("uint8"))


def embed(path: Path, max_px: int = 1500, trim: bool = False, light: bool = False) -> str:
    im = Image.open(path).convert("RGB")
    if light:
        im = relight_dark(im)
    if trim:
        im = trim_white(im)
    if max(im.size) > max_px:
        r = max_px / max(im.size)
        lanczos = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.ANTIALIAS)
        im = im.resize((int(im.width*r), int(im.height*r)), lanczos)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=91, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def icon(name: str, cx: float, cy: float, r: float, color: str, sw: float = 2.2) -> str:
    """Minimal stroke-style vector icons, centered at (cx, cy) with radius r."""
    c = color
    parts = []
    if name == "doc":
        parts.append(f'<path d="M{cx-r*0.7} {cy-r} H{cx+r*0.25} L{cx+r*0.7} {cy-r*0.55} V{cy+r} H{cx-r*0.7} Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
        parts.append(f'<path d="M{cx+r*0.25} {cy-r} V{cy-r*0.55} H{cx+r*0.7}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        for i in range(3):
            yy = cy - r*0.2 + i*r*0.45
            parts.append(f'<line x1="{cx-r*0.4}" y1="{yy}" x2="{cx+r*0.35}" y2="{yy}" stroke="{c}" stroke-width="{sw*0.8}" stroke-linecap="round"/>')
    elif name == "layers":
        for i, dy in enumerate((-r*0.55, 0, r*0.55)):
            parts.append(f'<path d="M{cx} {cy+dy-r*0.45} L{cx+r*0.85} {cy+dy} L{cx} {cy+dy+r*0.45} L{cx-r*0.85} {cy+dy} Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
    elif name == "branch":
        parts.append(f'<rect x="{cx-r*0.35}" y="{cy-r}" width="{r*0.7}" height="{r*0.55}" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        for dx in (-r*0.55, r*0.55):
            parts.append(f'<rect x="{cx+dx-r*0.35}" y="{cy+r*0.45}" width="{r*0.7}" height="{r*0.55}" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/>')
            parts.append(f'<path d="M{cx} {cy-r*0.45+0.0} V{cy} H{cx+dx} V{cy+r*0.45}" fill="none" stroke="{c}" stroke-width="{sw*0.85}"/>')
    elif name == "code":
        parts.append(f'<path d="M{cx-r*0.25} {cy-r*0.6} L{cx-r*0.95} {cy} L{cx-r*0.25} {cy+r*0.6}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append(f'<path d="M{cx+r*0.25} {cy-r*0.6} L{cx+r*0.95} {cy} L{cx+r*0.25} {cy+r*0.6}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append(f'<line x1="{cx+r*0.1}" y1="{cy-r*0.75}" x2="{cx-r*0.1}" y2="{cy+r*0.75}" stroke="{c}" stroke-width="{sw*0.85}" stroke-linecap="round"/>')
    elif name == "chat":
        parts.append(f'<rect x="{cx-r}" y="{cy-r*0.8}" width="{2*r}" height="{r*1.35}" rx="{r*0.3}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        parts.append(f'<path d="M{cx-r*0.35} {cy+r*0.55} V{cy+r*0.95} L{cx+r*0.15} {cy+r*0.55}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
        for dx in (-r*0.45, 0, r*0.45):
            parts.append(f'<circle cx="{cx+dx}" cy="{cy-r*0.12}" r="{sw*0.62}" fill="{c}"/>')
    elif name == "sliders":
        for i, dy in enumerate((-r*0.6, 0, r*0.6)):
            parts.append(f'<line x1="{cx-r*0.85}" y1="{cy+dy}" x2="{cx+r*0.85}" y2="{cy+dy}" stroke="{c}" stroke-width="{sw*0.85}" stroke-linecap="round"/>')
            knob = cx + (-r*0.25, r*0.4, -r*0.05)[i]
            parts.append(f'<circle cx="{knob}" cy="{cy+dy}" r="{r*0.22}" fill="white" stroke="{c}" stroke-width="{sw*0.85}"/>')
    elif name == "cube":
        parts.append(f'<path d="M{cx} {cy-r} L{cx+r*0.87} {cy-r*0.5} V{cy+r*0.5} L{cx} {cy+r} L{cx-r*0.87} {cy+r*0.5} V{cy-r*0.5} Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
        parts.append(f'<path d="M{cx-r*0.87} {cy-r*0.5} L{cx} {cy} L{cx+r*0.87} {cy-r*0.5} M{cx} {cy} V{cy+r}" fill="none" stroke="{c}" stroke-width="{sw*0.85}"/>')
    elif name == "image":
        parts.append(f'<rect x="{cx-r}" y="{cy-r*0.8}" width="{2*r}" height="{r*1.6}" rx="3" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        parts.append(f'<circle cx="{cx-r*0.4}" cy="{cy-r*0.25}" r="{r*0.18}" fill="{c}"/>')
        parts.append(f'<path d="M{cx-r} {cy+r*0.5} L{cx-r*0.2} {cy-r*0.1} L{cx+r*0.3} {cy+r*0.35} L{cx+r*0.6} {cy+r*0.05} L{cx+r} {cy+r*0.35}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
    elif name == "check-square":
        parts.append(f'<rect x="{cx-r*0.9}" y="{cy-r*0.9}" width="{r*1.8}" height="{r*1.8}" rx="3" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        parts.append(f'<path d="M{cx-r*0.45} {cy} L{cx-r*0.08} {cy+r*0.4} L{cx+r*0.5} {cy-r*0.35}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    elif name == "shield":
        parts.append(f'<path d="M{cx} {cy-r} L{cx+r*0.8} {cy-r*0.55} V{cy+r*0.1} C{cx+r*0.8} {cy+r*0.62} {cx+r*0.4} {cy+r*0.88} {cx} {cy+r} C{cx-r*0.4} {cy+r*0.88} {cx-r*0.8} {cy+r*0.62} {cx-r*0.8} {cy+r*0.1} V{cy-r*0.55} Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
        parts.append(f'<path d="M{cx-r*0.35} {cy-r*0.02} L{cx-r*0.05} {cy+r*0.32} L{cx+r*0.4} {cy-r*0.3}" fill="none" stroke="{c}" stroke-width="{sw*0.9}" stroke-linecap="round" stroke-linejoin="round"/>')
    elif name == "database":
        parts.append(f'<ellipse cx="{cx}" cy="{cy-r*0.6}" rx="{r*0.85}" ry="{r*0.35}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        parts.append(f'<path d="M{cx-r*0.85} {cy-r*0.6} V{cy+r*0.6} A{r*0.85} {r*0.35} 0 0 0 {cx+r*0.85} {cy+r*0.6} V{cy-r*0.6}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
        parts.append(f'<path d="M{cx-r*0.85} {cy} A{r*0.85} {r*0.35} 0 0 0 {cx+r*0.85} {cy}" fill="none" stroke="{c}" stroke-width="{sw*0.85}"/>')
    return "".join(parts)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def rect(x, y, w, h, fill="white", stroke=GRID, sw=1.7, rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(s, x, y, width, size=18, weight="400", fill=BODY, anchor="middle", family=SANS, line_height=1.18):
    chars = max(8, int(width / (size * 0.56)))
    lines: list[str] = []
    for para in s.split("\n"):
        lines.extend(textwrap.wrap(para, width=chars, break_long_words=False) or [""])
    tspans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else size * line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}">' + "".join(tspans) + "</text>"


def image(x, y, w, h, href, opacity=1.0):
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" opacity="{opacity}" href="{href}" preserveAspectRatio="xMidYMid meet"/>'


def arrow(x1, y1, x2, y2, stroke=ARROW, sw=2.2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" marker-end="url(#arrow)"/>'


def dashed_rule(y, width):
    return f'<line x1="20" y1="{y}" x2="{width-20}" y2="{y}" stroke="{GRID}" stroke-width="1.2" stroke-dasharray="6 8"/>'


def defs():
    return ('<defs>'
            '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M0,0 L8,4 L0,8 z" fill="{ARROW}"/></marker>'
            '</defs>')


def header(svg, title, subtitle=None, width=1600, title_y=46, title_size=30):
    svg.append(text(title, width/2, title_y, width-100, title_size, "700", fill=TITLE, family=SERIF))
    if subtitle:
        svg.append(text(subtitle, width/2, title_y+36, width-140, 17, fill=MUTED, family=SANS))


def panel(svg, x, y, w, h, title_s, tint, stroke, title_size=17, header_h=48):
    svg.append(rect(x, y, w, h, "white", stroke, 1.8, 18))
    svg.append(f'<path d="M{x+18},{y} H{x+w-18} Q{x+w},{y} {x+w},{y+18} V{y+header_h} H{x} V{y+18} Q{x},{y} {x+18},{y} Z" fill="{tint}"/>')
    svg.append(text(title_s, x+w/2, y+31, w-24, title_size, "700", fill=TITLE, family=SANS))


def pill(svg, x, y, w, h, s, fill="#f5f7fb", stroke="#c5cfdd", size=12):
    svg.append(rect(x, y, w, h, fill, stroke, 1.25, h/2))
    svg.append(text(s, x+w/2, y+h*0.62, w-16, size, "700", fill=BODY, family=SANS, line_height=1.04))


def build_fig1():
    W, H = 1680, 980
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(), f'<rect width="100%" height="100%" fill="{BG}"/>']
    header(svg, "From Registered Evidence to a Persistent Engineering Model",
           "A persistent evidence–program–validation loop with an explicit division of labor.", W, 46, 34)

    p1=(30,108,400,414); p2=(454,108,354,402); p3=(830,108,382,402); p4=(1238,108,410,402)
    panel(svg,*p1,"1. Physical evidence + prior state",SOFT_BLUE,BLUE,19,54)
    panel(svg,*p2,"2. GPT-6 Astra / Codex",SOFT_PURPLE,PURPLE,21,54)
    panel(svg,*p3,"3. Deterministic tools",SOFT_ORANGE,ORANGE,21,54)
    panel(svg,*p4,"4. Validated editable state",SOFT_TEAL,TEAL,21,54)

    field = embed(FIELD, 900)
    ref = embed(hist("installation_B17/r3/307_B17_4B77_Side_Reference.png"), 900, True, True)
    svg += [image(52,170,165,118,field), image(240,170,165,118,ref),
            text("field imagery",132,307,150,17), text("registered coarse geometry",322,307,160,17)]
    svg += [rect(75,340,80,66,"#f8fafc",GRID,1.8,5),
            '<line x1="91" y1="357" x2="140" y2="357" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="373" x2="140" y2="373" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="389" x2="130" y2="389" stroke="#718096" stroke-width="3"/>',
            text("engineering records",115,432,140,16),
            rect(274,343,76,60,"#f8fafc",GRID,1.8,5),
            '<path d="M287 380 L312 352 L337 366 L312 394 Z" fill="none" stroke="#8f70da" stroke-width="3"/>',
            text("inherited Blender state",312,432,150,16),
            text("field imagery, registered geometry, engineering records, and accepted prior state",230,470,340,17,fill=MUTED)]

    bullets2=[
        ("doc", "select evidence and scope the comparison domain"),
        ("layers", "choose or revise the representation"),
        ("branch", "decompose the reconstruction task"),
        ("code", "write or revise executable procedures"),
        ("chat", "interpret validator feedback and decide the next revision"),
    ]
    for i,(ic,s) in enumerate(bullets2):
        yy=190+i*58
        svg.append(icon(ic,492,yy-6,12,PURPLE))
        svg.append(text(s,524,yy,245,18,anchor="start",family=SANS))

    bullets3=[
        ("sliders", "fit, transform, or spline geometry"),
        ("cube", "construct geometry in Blender"),
        ("image", "render fixed diagnostic views"),
        ("check-square", "run endpoint and contact checks"),
        ("shield", "run coverage, collision, and preservation checks"),
    ]
    for i,(ic,s) in enumerate(bullets3):
        yy=190+i*58
        svg.append(icon(ic,864,yy-6,12,ORANGE))
        svg.append(text(s,898,yy,275,18,anchor="start",family=SANS))

    station=embed(hist("installation_B36/r3_previews/757_B36_Station_Clean.png"),1200,light=True)
    svg += [image(1262,170,360,246,station),
            text("accepted components, interfaces, connections, and provenance become the next batch context",1443,456,335,17,fill=MUTED)]
    svg += [arrow(430,286,452,286),arrow(808,286,828,286),arrow(1212,286,1236,286)]
    svg.append(f'<path d="M1485 530 C1340 568, 1045 570, 790 524" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round" marker-end="url(#arrow)"/>')
    svg.append(text("accepted state feeds the next batch",1125,590,340,17,fill="#2e746f"))
    svg.append(dashed_rule(608,W))
    svg.append(text("Main longitudinal result",30,650,520,30,"700",fill=TITLE,anchor="start",family=SERIF))

    bottom=[
        (30,674,372,242,"Local fit","comparison domain, pose, and primitive parameters",SOFT_BLUE,BLUE,hist("installation_B01/B01_front_overlay.jpg")),
        (430,674,372,242,"Reusable scope","shared MASTER assets versus site-specific geometry",SOFT_PURPLE,PURPLE,hist("installation_B08/42_B08_Transformer_Pair_r2.png")),
        (830,674,372,242,"Connected representation","ports, routes, continuity, and path class",SOFT_ORANGE,ORANGE,hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png")),
        (1230,674,410,242,"State-constrained integration","coverage, review, preservation, and interference",SOFT_TEAL,TEAL,hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png")),
    ]
    for x,y,w,h,t,foot,tint,stroke,p in bottom:
        panel(svg,x,y,w,h,t,tint,stroke,19,50)
        svg.append(image(x+18,y+60,w-36,126,embed(p,1100,True,True)))
        svg.append(text(foot,x+w/2,y+216,w-34,17,fill=MUTED))
    svg += [arrow(402,794,428,794),arrow(802,794,828,794),arrow(1202,794,1228,794)]
    svg.append('</svg>')
    (SVG_DIR/"fig01_overview_v23.svg").write_text("".join(svg),encoding="utf-8")


def build_fig4():
    W,H=1456,1112
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),f'<rect width="100%" height="100%" fill="{BG}"/>']
    header(svg,"Why the Reconstruction Loop Broadens: Three Structural Transitions",
           "Each row shows how a new dependency changes the engineering decision and therefore the operator choice.",W,42,29)

    rows=[
        (110,"A · Fit → reusable scope",BLUE,[
            ("B01: local fit","define a local comparison domain, then fit pose and size",hist("installation_B01/B01_front_overlay.jpg"),SOFT_BLUE,BLUE),
            ("B08: shared equipment","two installations reuse one shared MASTER",hist("installation_B08/42_B08_Transformer_Pair_r2.png"),SOFT_PURPLE,PURPLE),
            ("B15: revise reuse boundary","finite site geometry moves outside the shared asset",hist("installation_B15/B15_profiles.png"),SOFT_TEAL,TEAL)],
         ["repetition → invariance","reuse boundary becomes testable"]),
        (426,"B · Object → connected representation",PURPLE,[
            ("B20: ports and routes","existing equipment ends become explicit ports",hist("installation_B20/4100_route_diagnostic.png"),SOFT_BLUE,BLUE),
            ("B23: change representation","the connection is reformulated from straight to curved",hist("installation_B23/B23_measurement_profiles.png"),SOFT_ORANGE,ORANGE),
            ("B29: relational constraints","continuity and endpoint constraints scale across subsystems",hist("installation_B29/B29_crossline_fits.png"),SOFT_TEAL,TEAL)],
         ["relationships appear","endpoint/topology constraints"]),
        (742,"C · Addition → state-driven closure",TEAL,[
            ("B25: unexplained geometry","large unexplained structures remain in the scene",hist("installation_B25/B25_source_height_map.png"),SOFT_BLUE,BLUE),
            ("B26: reconstruct selected gaps","coverage selects which missing structures to reconstruct next",hist("installation_B26/543_B26_Structure_Overlay.png"),SOFT_PURPLE,PURPLE),
            ("B36: state-constrained insertion","new geometry must fit inherited endpoints and occupied space",hist("installation_B36/B36_busbar_plan_overlay.png"),SOFT_TEAL,TEAL)],
         ["coverage → task selection","fit the inherited world"]),
    ]
    panel_x=[176,610,1044]
    panel_w=344
    for r,(y,row_title,row_stroke,cards,links) in enumerate(rows):
        # full-height lane label in the row color (design follows the GPT-image reference)
        lane_tint = SOFT_BLUE if r==0 else (SOFT_PURPLE if r==1 else SOFT_TEAL)
        svg.append(rect(20,y+6,132,264,lane_tint,row_stroke,1.8,16))
        svg.append(text(row_title,86,y+116,116,16,"700",fill=row_stroke,family=SANS,line_height=1.25))
        for c,(title_s,foot,p,tint,stroke) in enumerate(cards):
            x=panel_x[c]
            panel(svg,x,y,panel_w,276,title_s,tint,stroke,20,48)
            svg.append(image(x+20,y+64,panel_w-40,146,embed(p,1100,True,True)))
            svg.append(text(foot,x+panel_w/2,y+242,panel_w-30,17,fill=MUTED))
        # Thin paper-style connectors. Labels float above the line, without bubbles.
        x1a, x2a = panel_x[0]+panel_w, panel_x[1]-4
        svg.append(arrow(x1a,y+150,x2a,y+150,sw=2.1))
        svg.append(text(links[0],(x1a+x2a)/2,y+126,132,15,"700",fill=MUTED))
        x1b, x2b = panel_x[1]+panel_w, panel_x[2]-4
        svg.append(arrow(x1b,y+150,x2b,y+150,sw=2.1))
        svg.append(text(links[1],(x1b+x2b)/2,y+126,140,15,"700",fill=MUTED))
        if r<2:
            svg.append(dashed_rule(y+300,W))
    svg.append(text("Descriptive evidence from the B01–B36 record. The figure explains how the reconstruction problem changes; it does not propose a universal complexity taxonomy.",W/2,1072,W-140,14,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig04_transitions_v23.svg").write_text("".join(svg),encoding="utf-8")


def build_fig5():
    W,H=1456,1140
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),f'<rect width="100%" height="100%" fill="{BG}"/>']
    header(svg,"Persistent State Enables Cross-Batch Composition—and Propagates Errors",
           "Later batches consume earlier masters, terminals, and endpoints; B15 shows the same mechanism propagating a wrong shared abstraction.",W,38,30)

    top=[
        (20,118,330,"B08","shared transformer MASTER + persistent terminal state","one reusable component structure; T1 / T2 are rigid site instances",hist("installation_B08/42_B08_Transformer_Pair_r2.png"),SOFT_BLUE,BLUE),
        (382,118,300,"B23","connection uses an existing transformer terminal","new lead geometry is defined relative to a B08 interface",hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png"),SOFT_PURPLE,PURPLE),
        (724,118,300,"B29","conductors reuse prior clamps and endpoints","jumpers and crossyard conductors connect previously modeled subsystems",hist("installation_B29/600_B29_G220_OUT_Detail_Overlay.png"),SOFT_ORANGE,ORANGE),
        (1066,118,370,"B36","late bus-rack closure uses preserved stubs and occupied space","new routes close onto inherited interfaces without rebuilding them",hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png"),SOFT_TEAL,TEAL),
    ]
    for x,y,w,bid,sub,foot,p,tint,stroke in top:
        panel(svg,x,y,w,410,bid,tint,stroke,20,48)
        svg.append(text(sub,x+w/2,y+80,w-34,17,"700",fill=BODY))
        svg.append(image(x+16,y+116,w-32,198,embed(p,1100,True,True)))
        svg.append(text(foot,x+w/2,y+372,w-30,16,fill=MUTED))

    for x1,label,x2 in [
        (350,"uses B08 terminal",382),
        (682,"extends endpoint graph",724),
        (1024,"closes onto preserved stubs",1066),
    ]:
        svg.append(arrow(x1,324,x2-3,324,sw=2.1))
        svg.append(text(label,(x1+x2)/2,292,150,15,"700",fill=MUTED))
    svg.append(dashed_rule(552,W))

    # B15 risk is a separate evidence panel below the chain.
    x,y,w,h=20,602,850,352
    panel(svg,x,y,w,h,"B15: inherited abstraction can propagate an error",SOFT_RED,RED,20,50)
    svg.append(image(44,672,350,205,embed(hist("installation_B15/r3/227_B15R2_756_Side_Overlay.png"),1200,True,True)))
    risk=("An early reusable representation gave multiple GIS installations the same finite bus-spool extent. "
          "The shared assumption produced overlaps where actual site separations differed. Recovery revised the MASTER/site boundary: reusable equipment stayed shared, while finite pipe sections and supports moved to site-specific scope.")
    svg.append(text(risk,430,690,390,18,anchor="start",fill=BODY))
    svg.append(f'<path d="M146 552 L146 602" stroke="{PURPLE}" stroke-width="2" stroke-linecap="round" stroke-dasharray="6 7" marker-end="url(#arrow)"/>')
    svg.append(text("shared abstraction inherited across installations",188,580,255,15,"700",anchor="start",fill=MUTED))

    x,y,w,h=900,602,536,352
    panel(svg,x,y,w,h,"B36 preservation burden",SOFT_TEAL,TEAL,20,50)
    stats=[("doc","36,615","previous objects unchanged"),("cube","7,114","previous station transforms unchanged"),("shield","2,798","protected files unchanged"),("database","36,812","objects in the final B36 file")]
    for i,(ic,num,lab) in enumerate(stats):
        yy=698+i*58
        svg.append(icon(ic,949,yy-6,13,"#276477"))
        svg.append(text(num,992,yy,90,20,"700",fill="#12677f",anchor="start"))
        svg.append(text(lab,1092,yy,290,17,anchor="start",fill=BODY))
    svg.append(f'<line x1="930" y1="876" x2="1404" y2="876" stroke="{GRID}" stroke-width="1.6"/>')
    svg.append(text("State-scale descriptors, not counts of independently verified physical assets.",1168,909,425,16,fill=MUTED))
    svg.append(dashed_rule(996,W))
    svg.append(text("The dependency chain documents composition through explicit external engineering state. No stateless control run is available, so the figure does not claim that persistence by itself improves accuracy.",W/2,1038,W-140,16,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig05_persistence_v23.svg").write_text("".join(svg),encoding="utf-8")


def export():
    figs=["fig01_overview_v23","fig04_transitions_v23","fig05_persistence_v23"]
    for stem in figs:
        src=SVG_DIR/f"{stem}.svg"
        cairosvg.svg2pdf(url=str(src), write_to=str(PDF_DIR/f"{stem}.pdf"))
        cairosvg.svg2png(url=str(src), write_to=str(PNG_DIR/f"{stem}.png"), output_width=1600)


def main():
    build_fig1(); build_fig4(); build_fig5(); export()
    for p in sorted(SVG_DIR.glob("*.svg")):
        print(p.relative_to(REPO))


if __name__ == "__main__":
    main()
