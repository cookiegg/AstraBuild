#!/usr/bin/env python3
"""Build figure-v2 hybrid SVG assets.

Design source: GPT Image prototypes generated during paper review.
Evidence source: only preserved AstraBuild B01--B36 artifacts already available
inside the publication project. Text, panels, arrows and statistics are vector
SVG; complex engineering imagery is embedded as raster evidence.
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

INK = "#172033"
MUTED = "#56677f"
GRID = "#cbd4df"
BLUE, PURPLE, ORANGE, TEAL, RED = "#4d85c8", "#8a68cf", "#d7882f", "#3d9994", "#c95b5b"
SOFT_BLUE, SOFT_PURPLE, SOFT_ORANGE, SOFT_TEAL, SOFT_RED = "#eaf2fc", "#f1ecfb", "#fff1e4", "#eaf7f5", "#fff0f0"


def hist(rel: str) -> Path:
    p = HIST / rel
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def trim_white(im: Image.Image) -> Image.Image:
    """Trim only substantial white borders from diagnostics."""
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
    im.save(buf, "JPEG", quality=90, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def rect(x, y, w, h, fill="white", stroke=GRID, sw=2, rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(s, x, y, width, size=22, weight="normal", fill=INK, anchor="middle", family="Georgia", line_height=1.18):
    # Width is in SVG user units; deliberately wrap earlier than browser rendering.
    chars = max(8, int(width / (size * 0.57)))
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


def arrow(x1, y1, x2, y2, stroke="#78879a", sw=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" marker-end="url(#arrow)"/>'


def defs():
    return ('<defs>'
            '<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
            '<path d="M0,0 L12,6 L0,12 z" fill="#78879a"/></marker>'
            '</defs>')


def header(svg, title, subtitle=None, width=1600, title_y=42, title_size=34):
    svg.append(text(title, width/2, title_y, width-100, title_size, "700"))
    if subtitle:
        svg.append(text(subtitle, width/2, title_y+42, width-140, 17, fill=MUTED))


def panel(svg, x, y, w, h, title_s, tint, stroke, title_size=20):
    svg.append(rect(x, y, w, h, "white", stroke, 2, 13))
    svg.append(f'<path d="M{x+13},{y} H{x+w-13} Q{x+w},{y} {x+w},{y+13} V{y+53} H{x} V{y+13} Q{x},{y} {x+13},{y} Z" fill="{tint}"/>')
    svg.append(text(title_s, x+w/2, y+34, w-24, title_size, "700"))


def build_fig1():
    W, H = 1672, 941
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(), '<rect width="100%" height="100%" fill="white"/>']
    header(svg, "From Registered Evidence to a Persistent Engineering Model", width=W)

    p1=(30,88,400,400); p2=(460,88,360,400); p3=(846,88,360,400); p4=(1232,88,408,400)
    panel(svg,*p1,"1. Physical evidence + prior state",SOFT_BLUE,BLUE,20)
    panel(svg,*p2,"2. GPT-6 Astra / Codex",SOFT_PURPLE,PURPLE,20)
    panel(svg,*p3,"3. Deterministic tools",SOFT_ORANGE,ORANGE,20)
    panel(svg,*p4,"4. Validated editable state",SOFT_TEAL,TEAL,20)

    # Real evidence images in panel 1.
    field = embed(FIELD, 900)
    ref = embed(hist("installation_B17/r3/307_B17_4B77_Side_Reference.png"), 900, True)
    svg += [image(50,155,165,120,field), image(240,155,165,120,ref),
            text("field imagery",132,295,150,16), text("registered coarse geometry",322,295,160,16)]
    # Vector record/state icons, avoiding generated decorative icons.
    svg += [rect(75,330,80,70,"#f7f9fb",GRID,2,4),
            '<line x1="91" y1="349" x2="140" y2="349" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="365" x2="140" y2="365" stroke="#718096" stroke-width="3"/>',
            '<line x1="91" y1="381" x2="130" y2="381" stroke="#718096" stroke-width="3"/>',
            text("engineering records",115,425,140,15),
            rect(274,333,76,64,"#f7f9fb",GRID,2,5),
            '<path d="M287 375 L312 347 L337 361 L312 389 Z" fill="none" stroke="#8a68cf" stroke-width="3"/>',
            text("inherited Blender state",312,425,150,15),
            text("registered geometry, images, records, accepted prior state",230,462,340,15,fill=MUTED)]

    bullets2=["select evidence / domain","choose representation","decompose task","write or revise program","interpret validator feedback"]
    for i,s in enumerate(bullets2):
        yy=177+i*58
        svg.append(f'<circle cx="498" cy="{yy-7}" r="6" fill="{PURPLE}"/>')
        svg.append(text(s,540,yy,245,16,anchor="start"))
    bullets3=["fit / transform / spline","construct geometry","render fixed views","endpoint / contact checks","coverage / collision / preservation checks"]
    for i,s in enumerate(bullets3):
        yy=177+i*58
        svg.append(f'<rect x="880" y="{yy-18}" width="16" height="16" fill="none" stroke="{ORANGE}" stroke-width="2"/>')
        svg.append(text(s,922,yy,245,16,anchor="start"))

    station=embed(hist("installation_B36/r3_previews/757_B36_Station_Clean.png"),1200)
    svg += [image(1260,150,352,270,station), text("components, interfaces, connections, provenance",1436,460,330,15,fill=MUTED)]
    svg += [arrow(430,285,458,285),arrow(820,285,844,285),arrow(1206,285,1230,285)]
    svg.append(f'<path d="M1455 505 C1320 565, 990 565, 780 505" fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#arrow)"/>')
    svg.append(text("accepted state becomes context for the next batch",1110,548,430,15,fill="#2e746f"))
    svg.append('<line x1="20" y1="585" x2="1650" y2="585" stroke="#c4cdd7" stroke-width="2" stroke-dasharray="8 8"/>')
    svg.append(text("Main longitudinal result",30,628,450,28,"700",anchor="start"))

    bottom=[
        (30,650,370,230,"Local fit","comparison domain, pose, primitive",SOFT_BLUE,BLUE,hist("installation_B01/B01_front_overlay.jpg")),
        (430,650,370,230,"Reusable scope","shared MASTER vs site-specific geometry",SOFT_PURPLE,PURPLE,hist("installation_B08/42_B08_Transformer_Pair_r2.png")),
        (830,650,370,230,"Connected representation","ports, routes, continuity, path class",SOFT_ORANGE,ORANGE,hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png")),
        (1230,650,410,230,"State-constrained integration","coverage, review, preservation, interference",SOFT_TEAL,TEAL,hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png")),
    ]
    for x,y,w,h,t,foot,tint,stroke,p in bottom:
        panel(svg,x,y,w,h,t,tint,stroke,17)
        svg.append(image(x+18,y+55,w-36,125,embed(p,1100,True)))
        svg.append(text(foot,x+w/2,y+207,w-35,14,fill=MUTED))
    svg += [arrow(400,765,428,765),arrow(800,765,828,765),arrow(1200,765,1228,765)]
    svg.append('</svg>')
    (SVG_DIR/"fig01_overview_v2.svg").write_text("".join(svg),encoding="utf-8")


def build_fig4():
    W,H=1448,1086
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),'<rect width="100%" height="100%" fill="white"/>']
    header(svg,"Why the Reconstruction Loop Broadens: Three Structural Transitions",
           "Each row shows how a new dependency changes the engineering decision, not just the fitted parameters.",W,37,29)

    rows=[
        (100,"A. Local fit → reusable scope",SOFT_BLUE,BLUE,[
            ("B01: local fit","define a local comparison domain, then fit pose and size",hist("installation_B01/B01_front_overlay.jpg")),
            ("B08: shared equipment","two installations reuse one shared MASTER",hist("installation_B08/42_B08_Transformer_Pair_r2.png")),
            ("B15: revise reuse boundary","finite site geometry moves outside the shared asset",hist("installation_B15/B15_profiles.png"))],
         ["repetition introduces invariance","reuse boundary becomes testable"]),
        (418,"B. Object geometry → connected representation",SOFT_PURPLE,PURPLE,[
            ("B20: ports and routes","existing equipment ends become explicit ports",hist("installation_B20/4100_route_diagnostic.png")),
            ("B23: change representation","the connection is reformulated from straight to curved",hist("installation_B23/B23_measurement_profiles.png")),
            ("B29: relational constraints","continuity and endpoint constraints scale across subsystems",hist("installation_B29/B29_crossline_fits.png"))],
         ["relationship constraints appear","endpoint / topology constraints scale"]),
        (736,"C. Scheduled addition → gap/state-driven closure",SOFT_TEAL,TEAL,[
            ("B25: unexplained geometry","large unexplained structures remain in the scene",hist("installation_B25/B25_source_height_map.png")),
            ("B26: reconstruct selected gaps","coverage drives which missing structures to reconstruct next",hist("installation_B26/543_B26_Structure_Overlay.png")),
            ("B36: state-constrained insertion","new geometry must fit inherited endpoints and occupied space",hist("installation_B36/B36_busbar_plan_overlay.png"))],
         ["coverage becomes a task signal","new geometry must fit the existing world"]),
    ]
    panel_x=[182,620,1058]
    panel_w=350
    for r,(y,row_title,tint,row_stroke,cards,links) in enumerate(rows):
        # Horizontal row label: more readable in a paper than vertical broken text.
        svg.append(rect(20,y+15,142,245,"white",row_stroke,2,12))
        svg.append(f'<rect x="20" y="{y+15}" width="142" height="245" rx="12" fill="{tint}" stroke="{row_stroke}" stroke-width="2"/>')
        svg.append(text(row_title,91,y+95,116,19,"700",line_height=1.12))
        for c,(title_s,foot,p) in enumerate(cards):
            x=panel_x[c]
            stroke=[BLUE,PURPLE,TEAL][c] if r==0 else ([BLUE,ORANGE,TEAL][c] if r==1 else [BLUE,PURPLE,TEAL][c])
            tt=[SOFT_BLUE,SOFT_PURPLE,SOFT_TEAL][c] if r==0 else ([SOFT_BLUE,SOFT_ORANGE,SOFT_TEAL][c] if r==1 else [SOFT_BLUE,SOFT_PURPLE,SOFT_TEAL][c])
            panel(svg,x,y,panel_w,275,title_s,tt,stroke,18)
            svg.append(image(x+15,y+58,panel_w-30,145,embed(p,1100,True)))
            svg.append(text(foot,x+panel_w/2,y+238,panel_w-35,14,fill=MUTED))
        svg.append(arrow(panel_x[0]+panel_w,y+140,panel_x[1]-4,y+140))
        svg.append(text(links[0],(panel_x[0]+panel_w+panel_x[1])/2,y+120,76,13,fill="#385070"))
        svg.append(arrow(panel_x[1]+panel_w,y+140,panel_x[2]-4,y+140))
        svg.append(text(links[1],(panel_x[1]+panel_w+panel_x[2])/2,y+120,84,13,fill="#385070"))
        if r<2:
            svg.append(f'<line x1="20" y1="{y+298}" x2="1428" y2="{y+298}" stroke="#c4cdd7" stroke-width="2" stroke-dasharray="8 8"/>')
    svg.append(text("Descriptive evidence from the B01–B36 record; the figure explains the changing reconstruction problem rather than proposing a universal complexity taxonomy.",724,1048,1320,15,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig04_transitions_v2.svg").write_text("".join(svg),encoding="utf-8")


def build_fig5():
    W,H=1448,1086
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),'<rect width="100%" height="100%" fill="white"/>']
    svg.append(text("Persistent External State Turns Local Reconstructions into a Connected Engineering System",
                    W/2, 28, W-90, 26, "700"))
    svg.append(text("Later batches explicitly consume earlier masters, terminals, and endpoints; the same mechanism can also propagate a wrong shared abstraction until it is revised.",
                    W/2, 91, W-120, 16, fill=MUTED))
    top=[
        (20,110,330,"B08","shared transformer MASTER + persistent terminal state","one reusable component structure; T1 / T2 are rigid site instances",hist("installation_B08/42_B08_Transformer_Pair_r2.png"),SOFT_BLUE,BLUE),
        (386,110,300,"B23","connection uses an existing transformer terminal","new lead geometry is defined relative to a B08 interface",hist("installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png"),SOFT_PURPLE,PURPLE),
        (726,110,300,"B29","conductors reuse prior clamps and endpoints","jumpers and crossyard conductors connect previously modeled subsystems",hist("installation_B29/600_B29_G-B_OUT_Detail_Overlay.png"),SOFT_ORANGE,ORANGE),
        (1066,110,360,"B36","late bus-rack closure uses preserved stubs and occupied space","new routes close onto inherited transformer interfaces without rebuilding them",hist("installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png"),SOFT_TEAL,TEAL),
    ]
    for x,y,w,bid,sub,foot,p,tint,stroke in top:
        panel(svg,x,y,w,410,bid,tint,stroke,19)
        svg.append(text(sub,x+w/2,y+78,w-30,15,"700",fill="#31415f"))
        svg.append(image(x+14,y+112,w-28,210,embed(p,1100,True)))
        svg.append(text(foot,x+w/2,y+370,w-30,14,fill=MUTED))
    for x1,label,x2 in [(350,"uses B08 terminal",386),(686,"extends prior endpoint graph",726),(1026,"closes onto preserved stubs",1066)]:
        svg.append(arrow(x1,315,x2-3,315)); svg.append(text(label,(x1+x2)/2,290,92,12,fill="#385070"))
    svg.append('<line x1="20" y1="550" x2="1428" y2="550" stroke="#c4cdd7" stroke-width="2" stroke-dasharray="8 8"/>')

    # B15 risk panel uses an actual preserved overlay instead of a synthetic before/after cartoon.
    x,y,w,h=20,590,850,345
    panel(svg,x,y,w,h,"B15: inherited abstraction can propagate an error",SOFT_RED,RED,18)
    svg.append(image(42,660,360,210,embed(hist("installation_B15/r3/227_B15R2_756_Side_Overlay.png"),1200,True)))
    risk=("An early reusable representation gave multiple GIS installations the same finite bus-spool extent. "
          "The shared assumption produced overlaps where actual site separations differed. Recovery revised the MASTER/site boundary: reusable equipment stayed shared, while finite pipe sections and supports moved to site-specific scope.")
    svg.append(text(risk,440,682,385,16,anchor="start",fill="#33445f"))
    svg.append(f'<path d="M150 550 L150 590" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#arrow)"/>')
    svg.append(text("shared abstraction propagates",180,574,210,12,anchor="start",fill="#385070"))

    # B36 preservation burden.
    x,y,w,h=900,590,526,345
    panel(svg,x,y,w,h,"B36 preservation burden",SOFT_TEAL,TEAL,18)
    stats=[("36,615","previous objects unchanged"),("7,114","previous station transforms unchanged"),("2,798","protected files unchanged"),("36,812","objects in the final B36 file")]
    for i,(num,lab) in enumerate(stats):
        yy=685+i*54
        svg.append(f'<rect x="940" y="{yy-18}" width="22" height="22" fill="none" stroke="#276477" stroke-width="2"/>')
        svg.append(text(num,995,yy,90,17,"700",fill="#12677f",anchor="start"))
        svg.append(text(lab,1110,yy,270,15,anchor="start",fill="#33445f"))
    svg.append('<line x1="930" y1="875" x2="1392" y2="875" stroke="#c0c9d0" stroke-width="2"/>')
    svg.append(text("State-scale descriptors, not counts of independently verified physical assets.",1160,908,420,14,fill=MUTED))
    svg.append('<line x1="20" y1="975" x2="1428" y2="975" stroke="#c4cdd7" stroke-width="2" stroke-dasharray="8 8"/>')
    svg.append(text("The dependency chain documents composition through explicit external engineering state. No stateless control run is available, so the figure does not claim that persistence by itself improves accuracy.",724,1028,1330,14,fill=MUTED))
    svg.append('</svg>')
    (SVG_DIR/"fig05_persistence_v2.svg").write_text("".join(svg),encoding="utf-8")


def export():
    figs=["fig01_overview_v2","fig04_transitions_v2","fig05_persistence_v2"]
    for stem in figs:
        src=SVG_DIR/f"{stem}.svg"
        pdf=PDF_DIR/f"{stem}.pdf"
        png=PNG_DIR/f"{stem}.png"
        cairosvg.svg2pdf(url=str(src), write_to=str(pdf))
        cairosvg.svg2png(url=str(src), write_to=str(png), output_width=1600)


def main():
    build_fig1(); build_fig4(); build_fig5(); export()
    for p in sorted(SVG_DIR.glob("*.svg")):
        print(p.relative_to(REPO))

if __name__ == "__main__":
    main()
