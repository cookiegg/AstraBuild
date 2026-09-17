#!/usr/bin/env python3
"""Build Figure v2.1 hybrid SVG/PDF/PNG assets.

v2.1 keeps the empirical content and B01--B36 provenance from figure_v2 while
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


def embed(path: Path, max_px: int = 1500, trim: bool = False) -> str:
    im = Image.open(path).convert("RGB")
    if trim:
        im = trim_white(im)
    if max(im.size) > max_px:
        r = max_px / max(im.size)
        lanczos = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.ANTIALIAS)
        im = im.resize((int(im.width*r), int(im.height*r)), lanczos)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=91, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


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


def arrow(x1, y1, x2, y2, stroke=ARROW, sw=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" marker-end="url(#arrow)"/>'


def dashed_rule(y, width):
    return f'<line x1="20" y1="{y}" x2="{width-20}" y2="{y}" stroke="{GRID}" stroke-width="1.6" stroke-dasharray="7 7"/>'


def defs():
    return ('<defs>'
            '<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
            f'<path d="M0,0 L12,6 L0,12 z" fill="{ARROW}"/></marker>'
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
           "A persistent evidence–program–validation loop with an explicit division of labor.", W, 46, 31)

    p1=(30,108,400,414); p2=(454,108,354,402); p3=(830,108,382,402); p4=(1238,108,410,402)
    panel(svg,*p1,"1. Physical evidence + prior state",SOFT_BLUE,BLUE,18,52)
    panel(svg,*p2,"2. GPT-6 Astra / Codex",SOFT_PURPLE,PURPLE,18,52)
    panel(svg,*p3,"3. Deterministic tools",SOFT_ORANGE,ORANGE,18,52)
    panel(svg,*p4,"4. Validated editable state",SOFT_TEAL,TEAL,18,52)

    field = embed(FIELD, 900)
    ref = embed(hist("installation_B17/r3/307_B17_4B77_Side_Reference.png"), 900, True)
    svg += [image(52,170,165,118,field), image(240,170,165,118,ref),
            text("field imagery",132,307,150,15), text("registered coarse geometry",322,307,160,15)]
    svg += [rect(75,340,80,66,"#f8fafc",GRID,1.8,5),
            '<line x1="91" y1="357" x2="140" y2="357" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="373" x2="140" y2="373" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="389" x2="130" y2="389" stroke="#718096" stroke-width="3"/>',
            text("engineering records",115,432,140,14),
            rect(274,343,76,60,"#f8fafc",GRID,1.8,5),
            '<path d="M287 380 L312 352 L337 366 L312 394 Z" fill="none" stroke="#8f70da" stroke-width="3"/>',
            text("inherited Blender state",312,432,150,14),
            text("field imagery, registered geometry, engineering records, and accepted prior state",230,470,340,15,fill=MUTED)]

    bullets2=[
        "select evidence and scope the comparison domain",
        "choose or revise the representation",
        "decompose the reconstruction task",
        "write or revise executable procedures",
        "interpret validator feedback and decide the next revision",
    ]
    for i,s in enumerate(bullets2):
        yy=190+i*58
        svg.append(f'<circle cx="490" cy="{yy-6}" r="6" fill="{PURPLE}"/>')
        svg.append(text(s,528,yy,245,15,anchor="start",family=SANS))

    bullets3=[
        "fit, transform, or spline geometry",
        "construct geometry in Blender",
        "render fixed diagnostic views",
        "run endpoint and contact checks",
        "run coverage, collision, and preservation checks",
    ]
    for i,s in enumerate(bullets3):
        yy=190+i*58
        svg.append(f'<rect x="856" y="{yy-17}" width="15" height="15" fill="none" stroke="{ORANGE}" stroke-width="2"/>')
        svg.append(text(s,898,yy,275,15,anchor="start",family=SANS))

    station=embed(hist("installation_B36/r3_previews/757_B36_Station_Clean.png"),1200)
    svg += [image(1262,170,360,246,station),
            text("accepted components, interfaces, connections, and provenance become the next batch context",1443,456,335,15,fill=MUTED)]
    svg += [arrow(430,286,452,286),arrow(808,286,828,286),arrow(1212,286,1236,286)]
    svg.append(f'<path d="M1485 530 C1340 585, 1035 588, 785 526" fill="none" stroke="{TEAL}" stroke-width="3.5" marker-end="url(#arrow)"/>')
    svg.append(text("accepted state feeds the next batch",1125,570,310,15,fill="#2e746f"))
    svg.append(dashed_rule(608,W))
    svg.append(text("Main longitudinal result",30,650,520,27,"700",fill=TITLE,anchor="start",family=SERIF))

    bottom=[
        (30,674,372,242,"Local fit","comparison domain, pose, and primitive parameters",SOFT_BLUE,BLUE,hist("installation_B01/B01_front_overlay.jpg")),
        (430,674,372,242,"Reusable scope","shared MASTER assets versus site-specific geometry",SOFT_PURPLE,PURPLE,hist("installation_B08/42_B08_Transformer_Pair_r2.png")),
        (830,674,372,242,"Connected representation","ports, routes, continuity, and path class",SOFT_ORANGE,ORANGE,hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png")),
        (1230,674,410,242,"State-constrained integration","coverage, review, preservation, and interference",SOFT_TEAL,TEAL,hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png")),
    ]
    for x,y,w,h,t,foot,tint,stroke,p in bottom:
        panel(svg,x,y,w,h,t,tint,stroke,16,48)
        svg.append(image(x+18,y+58,w-36,128,embed(p,1100,True)))
        svg.append(text(foot,x+w/2,y+216,w-34,14,fill=MUTED))
    svg += [arrow(402,794,428,794),arrow(802,794,828,794),arrow(1202,794,1228,794)]
    svg.append('</svg>')
    (SVG_DIR/"fig01_overview_v21.svg").write_text("".join(svg),encoding="utf-8")


def build_fig4():
    W,H=1456,1112
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),f'<rect width="100%" height="100%" fill="{BG}"/>']
    header(svg,"Why the Reconstruction Loop Broadens: Three Structural Transitions",
           "Each row shows how a new dependency changes the engineering decision and therefore the operator choice.",W,42,29)

    rows=[
        (110,"A · Local fit → reusable scope",BLUE,[
            ("B01: local fit","define a local comparison domain, then fit pose and size",hist("installation_B01/B01_front_overlay.jpg"),SOFT_BLUE,BLUE),
            ("B08: shared equipment","two installations reuse one shared MASTER",hist("installation_B08/42_B08_Transformer_Pair_r2.png"),SOFT_PURPLE,PURPLE),
            ("B15: revise reuse boundary","finite site geometry moves outside the shared asset",hist("installation_B15/B15_profiles.png"),SOFT_TEAL,TEAL)],
         ["repetition introduces\ninvariance","reuse boundary becomes\ntestable"]),
        (426,"B · Object geometry → connected representation",PURPLE,[
            ("B20: ports and routes","existing equipment ends become explicit ports",hist("installation_B20/4100_route_diagnostic.png"),SOFT_BLUE,BLUE),
            ("B23: change representation","the connection is reformulated from straight to curved",hist("installation_B23/B23_measurement_profiles.png"),SOFT_ORANGE,ORANGE),
            ("B29: relational constraints","continuity and endpoint constraints scale across subsystems",hist("installation_B29/B29_crossline_fits.png"),SOFT_TEAL,TEAL)],
         ["relationship constraints\nappear","endpoint and topology\nconstraints scale"]),
        (742,"C · Scheduled addition → gap/state-driven closure",TEAL,[
            ("B25: unexplained geometry","large unexplained structures remain in the scene",hist("installation_B25/B25_source_height_map.png"),SOFT_BLUE,BLUE),
            ("B26: reconstruct selected gaps","coverage selects which missing structures to reconstruct next",hist("installation_B26/543_B26_Structure_Overlay.png"),SOFT_PURPLE,PURPLE),
            ("B36: state-constrained insertion","new geometry must fit inherited endpoints and occupied space",hist("installation_B36/B36_busbar_plan_overlay.png"),SOFT_TEAL,TEAL)],
         ["coverage becomes a\ntask signal","new geometry must fit the\nexisting world"]),
    ]
    panel_x=[176,610,1044]
    panel_w=344
    for r,(y,row_title,row_stroke,cards,links) in enumerate(rows):
        # compact horizontal row tag: no vertical fragmented typography
        pill(svg,20,y+105,132,58,row_title,
             SOFT_BLUE if r==0 else (SOFT_PURPLE if r==1 else SOFT_TEAL),
             row_stroke,13)
        for c,(title_s,foot,p,tint,stroke) in enumerate(cards):
            x=panel_x[c]
            panel(svg,x,y,panel_w,276,title_s,tint,stroke,16,44)
            svg.append(image(x+20,y+58,panel_w-40,150,embed(p,1100,True)))
            svg.append(text(foot,x+panel_w/2,y+240,panel_w-30,14,fill=MUTED))
        # transition labels sit above the arrow rather than inside it
        svg.append(arrow(panel_x[0]+panel_w,y+142,panel_x[1]-4,y+142,sw=3))
        pill(svg,panel_x[0]+panel_w+8,y+104,82,48,links[0],"#f5f7fb","#c5cfdd",11)
        svg.append(arrow(panel_x[1]+panel_w,y+142,panel_x[2]-4,y+142,sw=3))
        pill(svg,panel_x[1]+panel_w+8,y+104,92,48,links[1],"#f5f7fb","#c5cfdd",11)
        if r<2:
            svg.append(dashed_rule(y+300,W))
    svg.append(text("Descriptive evidence from the B01–B36 record. The figure explains how the reconstruction problem changes; it does not propose a universal complexity taxonomy.",W/2,1072,W-140,14,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig04_transitions_v21.svg").write_text("".join(svg),encoding="utf-8")


def build_fig5():
    W,H=1456,1140
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),f'<rect width="100%" height="100%" fill="{BG}"/>']
    header(svg,"Persistent External State Turns Local Reconstructions into a Connected Engineering System",
           "Later batches explicitly consume earlier masters, terminals, and endpoints. The same mechanism can also propagate a wrong shared abstraction until it is revised.",W,35,25)

    top=[
        (20,118,330,"B08","shared transformer MASTER + persistent terminal state","one reusable component structure; T1 / T2 are rigid site instances",hist("installation_B08/42_B08_Transformer_Pair_r2.png"),SOFT_BLUE,BLUE),
        (382,118,300,"B23","connection uses an existing transformer terminal","new lead geometry is defined relative to a B08 interface",hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png"),SOFT_PURPLE,PURPLE),
        (724,118,300,"B29","conductors reuse prior clamps and endpoints","jumpers and crossyard conductors connect previously modeled subsystems",hist("installation_B29/600_B29_G220_OUT_Detail_Overlay.png"),SOFT_ORANGE,ORANGE),
        (1066,118,370,"B36","late bus-rack closure uses preserved stubs and occupied space","new routes close onto inherited interfaces without rebuilding them",hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png"),SOFT_TEAL,TEAL),
    ]
    for x,y,w,bid,sub,foot,p,tint,stroke in top:
        panel(svg,x,y,w,410,bid,tint,stroke,18,44)
        svg.append(text(sub,x+w/2,y+74,w-34,14,"700",fill=BODY))
        svg.append(image(x+16,y+108,w-32,205,embed(p,1100,True)))
        svg.append(text(foot,x+w/2,y+370,w-30,14,fill=MUTED))

    for x1,label,x2,label_w in [
        (350,"uses B08\nterminal",382,112),
        (682,"extends prior\nendpoint graph",724,118),
        (1024,"closes onto\npreserved stubs",1066,120),
    ]:
        svg.append(arrow(x1,320,x2-3,320,sw=3))
        pill(svg,(x1+x2-label_w)/2,278,label_w,44,label,"#f5f7fb","#c5cfdd",11)
    svg.append(dashed_rule(552,W))

    # B15 risk is a separate evidence panel below the chain.
    x,y,w,h=20,602,850,352
    panel(svg,x,y,w,h,"B15: inherited abstraction can propagate an error",SOFT_RED,RED,17,48)
    svg.append(image(44,672,350,205,embed(hist("installation_B15/r3/227_B15R2_756_Side_Overlay.png"),1200,True)))
    risk=("An early reusable representation gave multiple GIS installations the same finite bus-spool extent. "
          "The shared assumption produced overlaps where actual site separations differed. Recovery revised the MASTER/site boundary: reusable equipment stayed shared, while finite pipe sections and supports moved to site-specific scope.")
    svg.append(text(risk,430,690,390,15,anchor="start",fill=BODY))
    svg.append(f'<path d="M146 552 L146 602" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#arrow)"/>')
    svg.append(text("shared abstraction inherited across installations",188,578,235,12,"700",anchor="start",fill=MUTED))

    x,y,w,h=900,602,536,352
    panel(svg,x,y,w,h,"B36 preservation burden",SOFT_TEAL,TEAL,17,48)
    stats=[("36,615","previous objects unchanged"),("7,114","previous station transforms unchanged"),("2,798","protected files unchanged"),("36,812","objects in the final B36 file")]
    for i,(num,lab) in enumerate(stats):
        yy=698+i*58
        svg.append(f'<rect x="938" y="{yy-16}" width="22" height="22" fill="none" stroke="#276477" stroke-width="2"/>')
        svg.append(text(num,992,yy,90,17,"700",fill="#12677f",anchor="start"))
        svg.append(text(lab,1092,yy,290,14,anchor="start",fill=BODY))
    svg.append(f'<line x1="930" y1="876" x2="1404" y2="876" stroke="{GRID}" stroke-width="1.6"/>')
    svg.append(text("State-scale descriptors, not counts of independently verified physical assets.",1168,909,425,14,fill=MUTED))
    svg.append(dashed_rule(996,W))
    svg.append(text("The dependency chain documents composition through explicit external engineering state. No stateless control run is available, so the figure does not claim that persistence by itself improves accuracy.",W/2,1038,W-140,14,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig05_persistence_v21.svg").write_text("".join(svg),encoding="utf-8")


def export():
    figs=["fig01_overview_v21","fig04_transitions_v21","fig05_persistence_v21"]
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
