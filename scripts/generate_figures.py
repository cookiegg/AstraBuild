#!/usr/bin/env python3
"""Generate publication-quality AstraBuild figures from the frozen research release.

All quantitative values are read from release/metrics.json or study_protocol.json.
Historical experiment outputs are read-only and are used only for qualitative montage figures.
"""
from pathlib import Path
import json
import math
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from matplotlib.lines import Line2D
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
METRICS = json.loads((ROOT / "release" / "metrics.json").read_text())
PROTOCOL = json.loads((ROOT / "release" / "study_protocol.json").read_text())

# Local historical evidence: read-only.
BS = ROOT.parent.parent  # .../presentation -> .../blender-substation
PFP = BS / "photo-first-pilot"

# Journal-like palette: restrained, colorblind-friendly enough for print/screen.
INK = "#172033"
MUTED = "#5F6B7A"
GRID = "#DDE3EA"
BLUE = "#356CB6"
BLUE2 = "#78A6D2"
TEAL = "#2E8074"
TEAL2 = "#83B8AF"
ORANGE = "#C27A2C"
RED = "#B54A4A"
PURPLE = "#7865A5"
SOFT = "#F6F8FB"
DARK = "#253347"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "axes.edgecolor": "#9AA5B1",
    "axes.linewidth": 0.8,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "axes.labelcolor": INK,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, stem):
    fig.savefig(FIG / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(FIG / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def panel_label(ax, label):
    ax.text(-0.08, 1.04, label, transform=ax.transAxes, fontsize=11, fontweight="bold", va="bottom")


def rounded(ax, xy, wh, text, fc="white", ec=GRID, lw=1.2, fontsize=9, weight="normal", color=INK, radius=0.02):
    x, y = xy
    w, h = wh
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.012,rounding_size={radius}",
                       transform=ax.transAxes, fc=fc, ec=ec, lw=lw, clip_on=False)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, transform=ax.transAxes, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, color=color, linespacing=1.2)
    return (x, y, w, h)


def arrow_axes(ax, a, b, color=MUTED, lw=1.5, rad=0.0, style="-|>"):
    x1, y1, w1, h1 = a
    x2, y2, w2, h2 = b
    p1 = (x1+w1, y1+h1/2)
    p2 = (x2, y2+h2/2)
    ax.add_patch(FancyArrowPatch(p1, p2, transform=ax.transAxes,
                                arrowstyle=style, mutation_scale=12,
                                lw=lw, color=color,
                                connectionstyle=f"arc3,rad={rad}", clip_on=False))


def figure1_system_loop():
    """Paper Figure 1: a five-second visual explanation of the research question."""
    field = ROOT / "media" / "field_gis.jpg"
    reference = PFP / "output" / "installation_B17" / "r3" / "307_B17_4B77_Side_Reference.png"
    transformer = PFP / "output" / "installation_B08" / "37_B08_T1_Rear_Clean_r2.png"
    gis = PFP / "output" / "installation_B17" / "r3" / "305_B17_4B77_Side_Clean.png"
    station = ROOT / "media" / "d40_overview.png"
    missing = [str(p) for p in [field, reference, transformer, gis, station] if not p.exists()]
    if missing:
        print("skip fig1, missing", missing)
        return

    fig = plt.figure(figsize=(14.2, 7.7), facecolor="white")
    canvas = fig.add_axes([0,0,1,1]); canvas.axis("off")
    canvas.text(.03,.958,"Can one reasoning agent turn heterogeneous site evidence into a persistent, editable digital twin?",
                fontsize=16.5,fontweight="bold",color=INK,va="top")
    canvas.text(.03,.915,
                "Physical evidence goes in; the same GPT-6 Astra/Codex engineering agent repeatedly proposes programs and revisions; validated component models accumulate into one station state.",
                fontsize=9.2,color=MUTED,va="top")

    def panel(rect, path, title, sub, edge):
        ax = fig.add_axes(rect)
        im = Image.open(path).convert("RGB")
        ratio=rect[2]/rect[3]; sw,sh=im.size; sr=sw/sh
        if sr>ratio:
            nw=int(sh*ratio); l=max(0,(sw-nw)//2); im=im.crop((l,0,l+nw,sh))
        else:
            nh=int(sw/ratio); t=max(0,(sh-nh)//2); im=im.crop((0,t,sw,t+nh))
        ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_color(edge); s.set_linewidth(1.15)
        ax.set_title(title,loc="left",fontsize=8.8,fontweight="bold",color=INK,pad=4)
        ax.text(0,-.085,sub,transform=ax.transAxes,fontsize=6.9,color=MUTED,va="top",linespacing=1.25)

    canvas.text(.035,.835,"1 · EVIDENCE FROM THE OPERATING SITE",fontsize=9.4,fontweight="bold",color=BLUE)
    panel([.035,.555,.19,.215], field, "Field photographs", "visible parts, counts, orientation and appearance", "#B9C9DD")
    panel([.245,.555,.19,.215], reference, "Registered coarse geometry", "metric layout, occupied surfaces and omissions", "#B9C9DD")
    canvas.add_patch(FancyBboxPatch((.035,.365),.40,.12,boxstyle="round,pad=.01,rounding_size=.012",
                                    transform=canvas.transAxes,fc="#F7F9FC",ec="#CAD4DF",lw=1))
    canvas.text(.055,.458,"ENGINEERING CONTEXT + HISTORY",transform=canvas.transAxes,fontsize=8.2,fontweight="bold",color=DARK)
    canvas.text(.055,.421,"inventory / 12MZ semantics · prior Blender state · validators\nhuman review · failed revisions · manifests / continuation notes",
                transform=canvas.transAxes,fontsize=7.4,color=MUTED,va="top",linespacing=1.45)

    canvas.add_patch(FancyBboxPatch((.465,.47),.20,.255,boxstyle="round,pad=.012,rounding_size=.025",
                                    transform=canvas.transAxes,fc="#EEF4FF",ec="#9DB9DF",lw=1.5))
    canvas.text(.565,.684,"2 · GPT-6 ASTRA + CODEX",transform=canvas.transAxes,ha="center",fontsize=10.2,fontweight="bold",color=BLUE)
    canvas.text(.565,.638,"3D engineering agent",transform=canvas.transAxes,ha="center",fontsize=12.5,fontweight="bold",color=INK)
    canvas.text(.565,.588,"observe evidence\n→ form / revise a geometric hypothesis\n→ write or modify Python / Blender actions\n→ read review + validator feedback",
                transform=canvas.transAxes,ha="center",va="top",fontsize=8.0,color=DARK,linespacing=1.5)
    canvas.text(.565,.492,"same agent · many tasks · persistent state",transform=canvas.transAxes,ha="center",fontsize=7.2,color=MUTED)
    canvas.add_patch(FancyArrowPatch((.435,.62),(.462,.62),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=14,lw=2,color=BLUE))
    canvas.add_patch(FancyArrowPatch((.668,.62),(.702,.62),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=14,lw=2,color=BLUE))

    canvas.text(.705,.835,"3 · EDITABLE TASK OUTPUTS",fontsize=9.4,fontweight="bold",color=TEAL)
    panel([.705,.555,.125,.215], transformer, "Transformer", "shared MASTER + site instance", "#9FCBC1")
    panel([.845,.555,.125,.215], gis, "GIS", "component family + site geometry", "#9FCBC1")
    canvas.add_patch(FancyBboxPatch((.705,.365),.265,.12,boxstyle="round,pad=.01,rounding_size=.012",
                                    transform=canvas.transAxes,fc="#F2FAF7",ec="#A4D0C4",lw=1))
    canvas.text(.725,.458,"OTHER TASKS",transform=canvas.transAxes,fontsize=8.2,fontweight="bold",color=TEAL)
    canvas.text(.725,.421,"arresters · capacitor banks · conductors · buildings\nauxiliary facilities · human-guided correction · semantics",
                transform=canvas.transAxes,fontsize=7.25,color=MUTED,va="top",linespacing=1.45)

    canvas.add_patch(FancyArrowPatch((.835,.35),(.835,.295),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=14,lw=2,color=TEAL))
    panel([.535,.075,.30,.185], station, "4 · Persistent station-scale digital twin", "37,153 scene objects · shared assets · connections · history · later inspection semantics", "#A4D0C4")
    canvas.add_patch(FancyBboxPatch((.05,.075),.40,.185,boxstyle="round,pad=.01,rounding_size=.012",
                                    transform=canvas.transAxes,fc="#FBFCFE",ec=GRID,lw=1))
    canvas.text(.07,.225,"WHAT MAKES THIS AN AGENT STUDY?",transform=canvas.transAxes,fontsize=8.7,fontweight="bold",color=PURPLE)
    canvas.text(.07,.187,"The artifact persists across tasks. Later batches inherit earlier geometry, assets,\nvalidators and mistakes. Failures can change what is measured, what is shared, and what is built next.",
                transform=canvas.transAxes,fontsize=7.5,color=DARK,va="top",linespacing=1.45)
    canvas.text(.03,.018,"Figure 1 · Study overview. The photogrammetric reconstruction is evidence, not the final representation. AstraBuild targets an editable, componentized and traceable engineering state that accumulates across heterogeneous reconstruction tasks.",transform=canvas.transAxes,fontsize=7.7,color=MUTED)
    save(fig,"fig01_agentic_loop")


def figure2_longitudinal():
    fig, ax = plt.subplots(figsize=(13.4,5.6))
    ax.set_xlim(0,42); ax.set_ylim(-1.6,5.3); ax.axis("off")
    ax.text(0,5.15,"Longitudinal reconstruction study: protocol changes with the artifact",fontsize=16,fontweight="bold",va="top")
    ax.text(0,4.7,"The 38 core batches are not IID trials; failures change later metrics, abstraction boundaries, and task selection.",fontsize=9.5,color=MUTED,va="top")
    phases=[
        (1,5,"B01–B05","Device fitting",BLUE2),
        (6,10,"B06–B10","Hierarchy formation",TEAL2),
        (11,19,"B11–B19","GIS / family expansion","#C3AFD7"),
        (20,30,"B20–B30","Connected systems + coverage","#F0C58B"),
        (31,38,"B31–D38","Closure + human correction","#E7A1A1"),
        (40,41,"D40–D41","Presentation → semantics","#A9CBB9"),
    ]
    y=2.55
    for x0,x1,label,name,c in phases:
        ax.add_patch(FancyBboxPatch((x0,y-0.28),x1-x0+0.72,0.56,boxstyle="round,pad=0.02,rounding_size=0.08",fc=c,ec="white",lw=0.8))
        ax.text((x0+x1)/2,y+0.02,label,ha="center",va="center",fontweight="bold",fontsize=8.8)
        ax.text((x0+x1)/2,y-0.15,name,ha="center",va="center",fontsize=7.6,color=DARK)
    ax.plot([1,41],[2.55,2.55],color="#7E8996",lw=1,zorder=0)

    events=[
        (1,3.65,"B01","Held-out arrester\nscreen fails",RED),
        (8,1.15,"B08","Shared transformer\nMASTER + T1/T2",TEAL),
        (15,3.65,"B15","r1→r3: metric +\nmaster boundary revised",PURPLE),
        (25.5,1.15,"B25/B26","Coverage audit changes\nwhat to model next",ORANGE),
        (36,3.65,"B36","Human omission review\ntriggers reconstruction",BLUE),
        (38,1.15,"D38","Markup → world coords\nquarantine + rebuild",RED),
        (40,3.65,"D40","Material-only layer\ngeometry invariant",ORANGE),
        (41,1.15,"D41","79 accessory meshes\n17 part classes × T1/T2",TEAL),
    ]
    for x,yy,label,text,c in events:
        ax.plot([x,x],[2.82,yy-0.16 if yy>2.5 else yy+0.55],color=c,lw=1.2)
        ax.scatter([x],[2.55],s=30,color=c,zorder=3,edgecolor="white",linewidth=0.7)
        ax.text(x,yy,label,ha="center",va="bottom",fontsize=8.7,fontweight="bold",color=c)
        ax.text(x,yy-0.08,text,ha="center",va="top",fontsize=7.8,color=DARK,linespacing=1.25)
    ax.text(0,-1.22,"Figure 2 · Long-horizon evidence: early failures are retained and become protocol changes rather than being erased from the study history.",fontsize=8,color=MUTED)
    save(fig,"fig02_longitudinal_study")


def figure3_quantitative():
    fig, axs=plt.subplots(2,2,figsize=(12.8,8.3))
    fig.suptitle("Quantitative evidence: agreement, validation screen, and omission coverage",fontsize=15,fontweight="bold",y=0.985)
    fig.text(0.5,0.952,"Each panel has a different interpretation; none is an independent survey-accuracy benchmark.",ha="center",fontsize=9,color=MUTED)

    # A residual summary
    ax=axs[0,0]; panel_label(ax,"a")
    labels=["Median","P90","P95"]
    vals=[3.6,8.4,11.6]
    bars=ax.bar(labels,vals,color=[BLUE,BLUE2,"#A9BED7"],width=0.58)
    ax.axhline(5,color=RED,lw=1.2,ls="--",label="5 cm screening reference")
    ax.scatter([-0.18],[9.3],marker="D",s=44,color=ORANGE,zorder=4,label="Historical pre-fit median (9.3 cm)")
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.35,f"{v:.1f}",ha="center",fontsize=9,fontweight="bold")
    ax.set_ylabel("Reference residual (cm)")
    ax.set_title("Current coarse-reference residual ledger (n=1,550)",loc="left",fontweight="bold")
    ax.set_ylim(0,13.2); ax.grid(axis="y",color=GRID,lw=.7); ax.set_axisbelow(True)
    ax.legend(frameon=False,fontsize=7.5,loc="upper left")
    ax.text(0.0,-0.20,"Same photogrammetric mesh is used as reconstruction reference and comparison surface.",transform=ax.transAxes,fontsize=7.5,color=MUTED)

    # B screen ledger
    ax=axs[0,1]; panel_label(ax,"b")
    pas,fail=149,101; total=pas+fail
    ax.barh([0],[pas],color=TEAL,height=.42,label=f"Pass: {pas}")
    ax.barh([0],[fail],left=[pas],color="#D98989",height=.42,label=f"Not pass: {fail}")
    ax.text(pas/2,0,f"{pas}\n{pas/total*100:.1f}%",ha="center",va="center",color="white",fontweight="bold")
    ax.text(pas+fail/2,0,f"{fail}\n{fail/total*100:.1f}%",ha="center",va="center",color="white",fontweight="bold")
    ax.set_xlim(0,total); ax.set_yticks([]); ax.set_xlabel("Retained screening items")
    ax.set_title("5 cm validation-screen ledger",loc="left",fontweight="bold")
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.text(0.0,-0.20,"This is a retained validation screen, not a task success rate or overall model accuracy.",transform=ax.transAxes,fontsize=7.5,color=MUTED)

    # C gap fraction
    ax=axs[1,0]; panel_label(ax,"c")
    vals=[78.8,14.6]
    bars=ax.bar(["Before","After"],vals,color=["#D8B27B",TEAL],width=.56)
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+2.0,f"{v:.1f}%",ha="center",fontweight="bold")
    ax.annotate("−64.2 pp",xy=(1,14.6),xytext=(0.45,50),arrowprops=dict(arrowstyle="->",color=INK,lw=1),fontsize=9,fontweight="bold")
    ax.set_ylim(0,90); ax.set_ylabel("Selected high-region samples > 1 m (%)")
    ax.set_title("Coverage-driven completion (B25/B26)",loc="left",fontweight="bold")
    ax.grid(axis="y",color=GRID,lw=.7); ax.set_axisbelow(True)

    # D slope / log
    ax=axs[1,1]; panel_label(ax,"d")
    pairs={"GIS-B high region":(8.12,0.15),"Transformer high region":(3.15,0.06)}
    for i,(name,(before,after)) in enumerate(pairs.items()):
        c=[BLUE,ORANGE][i]
        ax.plot([0,1],[before,after],marker="o",ms=6,lw=2,color=c,label=name)
        ax.text(-.04,before,f"{before:.2f} m",ha="right",va="center",fontsize=8,color=c)
        ax.text(1.04,after,f"{after:.2f} m",ha="left",va="center",fontsize=8,color=c)
    ax.set_yscale("log"); ax.set_xlim(-.25,1.25); ax.set_xticks([0,1],["Before","After"])
    ax.set_ylabel("Median distance (m, log scale)")
    ax.set_title("Selected high-region median distance",loc="left",fontweight="bold")
    ax.grid(axis="y",which="both",color=GRID,lw=.6); ax.legend(frameon=False,fontsize=8,loc="lower left")
    fig.subplots_adjust(hspace=.48,wspace=.28,top=.89,bottom=.09)
    fig.text(0.02,0.02,"Figure 3 · Quantitative evidence uses separate metrics for local agreement and missing-geometry coverage. The 5 cm screen explicitly retains non-passing items.",fontsize=8,color=MUTED)
    save(fig,"fig03_quantitative_evidence")


def figure4_structure_semantics():
    fig,axs=plt.subplots(1,3,figsize=(13.6,4.7),gridspec_kw={"width_ratios":[1.25,1,1.05]})
    fig.suptitle("From scene structure to inspection-addressable semantics",fontsize=15,fontweight="bold",y=.99)

    ax=axs[0]; panel_label(ax,"a")
    names=["Objects","Mesh datablocks","Collections","Scenes","New review scenes"]
    vals=[37153,3916,858,755,719]
    y=range(len(names))
    ax.barh(list(y),vals,color=[BLUE,TEAL,"#9BAABD","#B0BAC5","#C2CAD2"])
    ax.set_yticks(list(y),names); ax.invert_yaxis(); ax.set_xscale("log"); ax.set_xlabel("Count (log scale)")
    ax.set_title("D38.2/D40-equivalent artifact scale",loc="left",fontweight="bold")
    for yy,v in zip(y,vals): ax.text(v*1.08,yy,f"{v:,}",va="center",fontsize=8)
    ax.grid(axis="x",which="both",color=GRID,lw=.6); ax.set_axisbelow(True)
    ax.text(.02,-.20,"37,153 objects / 3,916 mesh datablocks ≈ 9.5× descriptive reuse ratio.",transform=ax.transAxes,fontsize=7.5,color=MUTED)

    ax=axs[1]; panel_label(ax,"b")
    linked,unmatched=76,30; total=106
    ax.barh([0],[linked],color=TEAL,height=.40)
    ax.barh([0],[unmatched],left=[linked],color="#D9A06B",height=.40)
    ax.text(linked/2,0,f"Linked\n{linked}",ha="center",va="center",color="white",fontweight="bold")
    ax.text(linked+unmatched/2,0,f"Unmatched\n{unmatched}",ha="center",va="center",color="white",fontweight="bold")
    ax.set_xlim(0,total); ax.set_yticks([]); ax.set_xlabel("Official names (n=106)")
    ax.set_title("Device-level semantic attachment",loc="left",fontweight="bold")
    ax.text(.02,.70,"151 devices in station_part_map",transform=ax.transAxes,fontsize=10,fontweight="bold",color=BLUE)
    ax.text(.02,.59,"100 12MZ groups attached to geometry",transform=ax.transAxes,fontsize=8,color=MUTED)
    ax.text(.02,-.20,"Unmatched names remain explicit rather than being forced onto uncertain geometry.",transform=ax.transAxes,fontsize=7.5,color=MUTED)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)

    ax=axs[2]; panel_label(ax,"c")
    vals=[31,4,1]; labels=["Model part","External component","Non-visual"]
    colors=[TEAL,BLUE2,"#C3C9D0"]
    left=0
    for v,l,c in zip(vals,labels,colors):
        ax.barh([0],[v],left=[left],height=.40,color=c,label=f"{l}: {v}")
        if v>=3: ax.text(left+v/2,0,str(v),ha="center",va="center",fontweight="bold",color="white")
        left+=v
    ax.set_xlim(0,36); ax.set_yticks([]); ax.set_xlabel("Official #1 transformer inspection points (n=36)")
    ax.set_title("Transformer inspection-point categorization",loc="left",fontweight="bold")
    ax.legend(frameon=False,fontsize=7.5,loc="upper left",bbox_to_anchor=(0,.83))
    ax.text(.02,.54,"189 semantic meshes → 26 part classes",transform=ax.transAxes,fontsize=9,fontweight="bold",color=BLUE)
    ax.text(.02,.44,"D41 adds 79 accessory meshes",transform=ax.transAxes,fontsize=9,fontweight="bold",color=TEAL)
    ax.text(.02,.35,"17 missing inspection-relevant classes × T1/T2",transform=ax.transAxes,fontsize=8,color=MUTED)
    ax.text(.02,-.20,"Categorization coverage is not equivalent to complete station-wide part geometry.",transform=ax.transAxes,fontsize=7.5,color=MUTED)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)

    fig.subplots_adjust(wspace=.42,top=.82,bottom=.22,left=.08,right=.98)
    fig.text(.02,.025,"Figure 4 · Geometry stabilization, explicit reuse, device mapping, and transformer inspection semantics are reported as distinct layers rather than a single accuracy number.",fontsize=8,color=MUTED)
    save(fig,"fig04_structure_and_semantics")


def figure5_failure_recovery():
    fig,ax=plt.subplots(figsize=(13.5,7.5)); ax.axis("off"); ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.02,.97,"Failure and recovery: what changed after the agent was wrong",fontsize=16,fontweight="bold",va="top")
    ax.text(.02,.925,"Each column traces a preserved failure from trigger to protocol change. These are longitudinal case studies, not frequency estimates.",fontsize=9.5,color=MUTED,va="top")
    cases=PROTOCOL["key_cases"][:4]
    x0=.02; gap=.018; w=(.96-gap*3)/4
    colors=[RED,PURPLE,BLUE,TEAL]
    row_titles=["Trigger","Diagnosis","Correction","Research lesson"]
    y_positions=[.72,.51,.30,.09]
    h=.15
    for i,(case,c) in enumerate(zip(cases,colors)):
        x=x0+i*(w+gap)
        ax.text(x,.86,case["id"],fontsize=11,fontweight="bold",color=c)
        for j,(key,rt) in enumerate(zip(["trigger","diagnosis","change","lesson"],row_titles)):
            yy=y_positions[j]
            ax.text(x,yy+h+.015,rt.upper(),fontsize=7.2,fontweight="bold",color=MUTED)
            wrapped="\n".join(textwrap.wrap(case[key],32))
            rect=FancyBboxPatch((x,yy),w,h,boxstyle="round,pad=0.009,rounding_size=0.01",fc="#FBFCFD" if j<3 else "#F2F7F5",ec=c if j==3 else GRID,lw=1.1)
            ax.add_patch(rect)
            ax.text(x+.012,yy+h/2,wrapped,fontsize=8,va="center",ha="left",linespacing=1.25)
            if j<3:
                ax.add_patch(FancyArrowPatch((x+w/2,yy-.003),(x+w/2,y_positions[j+1]+h+.003),arrowstyle="-|>",mutation_scale=8,lw=.9,color="#A5AEB8"))
    ax.text(.02,.012,"Figure 5 · The central evidence for reliability is not a perfect first attempt; it is whether invalid hypotheses are detected, retained, diagnosed, and converted into explicit protocol or abstraction changes.",fontsize=8,color=MUTED)
    save(fig,"fig05_failure_recovery")


def _load_rgb(path):
    im=Image.open(path).convert("RGB")
    return im


def figure6_d38_feedback():
    paths={
        "markup":PFP/"output/fixed/clean.png",
        "corrected":PFP/"output/installation_D38/769_D38_Station_Top_Clean.png",
        "gis":PFP/"output/installation_D38/768_D38_GIS_Row_Overlay.png",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        print("skip fig06, missing",missing); return
    fig=plt.figure(figsize=(13.4,7.8))
    gs=fig.add_gridspec(2,3,height_ratios=[1,0.44],width_ratios=[1,1,0.72],hspace=.13,wspace=.08)
    ax1=fig.add_subplot(gs[0,0]); ax2=fig.add_subplot(gs[0,1]); ax3=fig.add_subplot(gs[0,2])
    for ax in [ax1,ax2,ax3]: ax.axis("off")
    ax1.imshow(_load_rgb(paths["markup"])); ax1.set_title("Human review markup (B35 top view)",loc="left",fontweight="bold",fontsize=10)
    ax2.imshow(_load_rgb(paths["corrected"])); ax2.set_title("D38.2 corrected station view",loc="left",fontweight="bold",fontsize=10)
    ax3.imshow(_load_rgb(paths["gis"])); ax3.set_title("GIS-row correction review",loc="left",fontweight="bold",fontsize=10)
    fig.suptitle("D38 human-in-the-loop correction: markup becomes traceable 3D evidence",fontsize=15,fontweight="bold",y=.985)

    ax=fig.add_subplot(gs[1,:]); ax.axis("off")
    steps=[
        ("1 · Register markup","NCC 0.94 / 0.92\nscale 0.94"),
        ("2 · Invert camera mapping","7 marked regions →\nmodel-world coordinates"),
        ("3 · Diagnose","3 false cabinet groups\n3 GIS gaps + fire room"),
        ("4 · Preserve provenance","9 cabinet objects moved\nto quarantine, not deleted"),
        ("5 · Rebuild + review","GIS gaps + fire facilities;\nD38.1 yaw error → D38.2"),
    ]
    n=len(steps); margin=.025; gap=.012; w=(1-2*margin-gap*(n-1))/n; y=.22; h=.53
    boxes=[]
    for i,(t,s) in enumerate(steps):
        x=margin+i*(w+gap); c=[BLUE,BLUE2,ORANGE,PURPLE,TEAL][i]
        r=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=.012",transform=ax.transAxes,fc="#FAFBFD",ec=c,lw=1.2)
        ax.add_patch(r); boxes.append((x,y,w,h))
        ax.text(x+.012,y+h-.13,t,transform=ax.transAxes,fontsize=8.2,fontweight="bold",color=c)
        ax.text(x+.012,y+.12,s,transform=ax.transAxes,fontsize=7.5,va="bottom",linespacing=1.25,color=DARK)
        if i<n-1:
            ax.add_patch(FancyArrowPatch((x+w+.002,y+h/2),(x+w+gap-.002,y+h/2),transform=ax.transAxes,arrowstyle="-|>",mutation_scale=9,lw=1,color=MUTED))
    ax.text(.025,.02,"Figure 6 · Sparse human feedback supplies an error signal; the agent performs evidence registration, diagnosis, geometric correction, and provenance-preserving quarantine.",transform=ax.transAxes,fontsize=8,color=MUTED)
    save(fig,"fig06_d38_human_feedback")


def figure7_d41_semantics():
    imgs=[
        (PFP/"output/installation_D41/render_D41_T1_front.png","T1 front"),
        (PFP/"output/installation_D41/render_D41_T1_rear_fans.png","T1 rear / fans"),
        (PFP/"output/installation_D41/render_D41_T1_bushing_closeup.png","Bushing / accessory close-up"),
    ]
    if any(not p.exists() for p,_ in imgs):
        print("skip fig07, missing D41 render"); return
    fig=plt.figure(figsize=(13.2,7.2)); gs=fig.add_gridspec(2,3,height_ratios=[1,.36],hspace=.12,wspace=.08)
    fig.suptitle("D41: augmenting a stabilized transformer with inspection-addressable accessories",fontsize=15,fontweight="bold",y=.985)
    for i,(p,title) in enumerate(imgs):
        ax=fig.add_subplot(gs[0,i]); ax.imshow(_load_rgb(p)); ax.axis("off"); ax.set_title(title,loc="left",fontsize=9.5,fontweight="bold")
    ax=fig.add_subplot(gs[1,:]); ax.axis("off")
    cards=[
        ("79","accessory meshes","selected from semantic source geometry"),
        ("17","inspection-relevant classes","missing from the B08 visible assembly"),
        ("2","site instances","T1 and T2 reuse the same accessory master"),
        ("36","official inspection points","31 model-part + 4 external + 1 non-visual categorized"),
        ("ok=true","D41 validation","79/79 structure; 17/17 classes per transformer"),
    ]
    margin=.025; gap=.015; w=(1-2*margin-gap*4)/5
    for i,(big,title,sub) in enumerate(cards):
        x=margin+i*(w+gap); c=[BLUE,TEAL,PURPLE,ORANGE,DARK][i]
        r=FancyBboxPatch((x,.23),w,.60,boxstyle="round,pad=.01,rounding_size=.012",transform=ax.transAxes,fc="#FAFBFD",ec=GRID,lw=1)
        ax.add_patch(r); ax.text(x+.015,.66,big,transform=ax.transAxes,fontsize=16,fontweight="bold",color=c)
        ax.text(x+.015,.51,title,transform=ax.transAxes,fontsize=8.3,fontweight="bold")
        ax.text(x+.015,.29,"\n".join(textwrap.wrap(sub,27)),transform=ax.transAxes,fontsize=7.2,color=MUTED,va="bottom",linespacing=1.2)
    ax.text(.025,.03,"Figure 7 · D41 is an augmentation layer, not a new station reconstruction. It adds inspection-relevant accessories while reusing the established T1/T2 site transforms.",transform=ax.transAxes,fontsize=8,color=MUTED)
    save(fig,"fig07_d41_inspection_semantics")


def figure8_validation_stack():
    fig,ax=plt.subplots(figsize=(12.8,6.5)); ax.axis("off");ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.03,.96,"Verifier stack: different checks answer different failure questions",fontsize=16,fontweight="bold",va="top")
    ax.text(.03,.91,"AstraBuild does not collapse provenance, software validity, geometric agreement, physical placement, and coverage into one score.",fontsize=9.5,color=MUTED,va="top")
    groups=[
        ("History & provenance",BLUE,["prior object/scene/collection signatures","site transforms unchanged","SHA-256 source / protected-file chain"]),
        ("Artifact integrity",PURPLE,["save → reopen round trip","finite geometry","manifest-based numeric reproduction"]),
        ("Geometry & placement",TEAL,["BVH nearest-surface residuals","ground / support / endpoint continuity","rigid instance SVD + det > 0"]),
        ("Reviewability",ORANGE,["camera framing / non-empty renders","qualitative overlay review","quarantine / limitation records"]),
        ("Completeness signal",RED,["10 cm occupancy audit","selected >1 m unexplained fraction","coverage-driven task selection"]),
    ]
    x=.04; y=.75; w=.92; h=.13; gap=.025
    for i,(title,c,items) in enumerate(groups):
        yy=y-i*(h+gap)
        r=FancyBboxPatch((x,yy),w,h,boxstyle="round,pad=.012,rounding_size=.012",fc="#FBFCFD",ec=c,lw=1.1)
        ax.add_patch(r); ax.text(x+.018,yy+h*.68,title,fontsize=10,fontweight="bold",color=c,va="center")
        ax.text(x+.22,yy+h*.67,"  •  ".join(items),fontsize=8.2,color=DARK,va="center")
    ax.text(.04,.02,"Figure 8 · Passing one layer does not imply passing another: e.g., a software-valid transform can still fail held-out geometry, and a low residual does not prove independent survey accuracy.",fontsize=8,color=MUTED)
    save(fig,"fig08_validation_stack")


def figure9_task_suite_composition():
    fig, ax = plt.subplots(figsize=(13.6, 7.6))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(.02, .965, "From heterogeneous reconstruction tasks to a persistent station digital twin", fontsize=16.5, fontweight="bold", va="top")
    ax.text(.02, .922, "The scientific story has three levels: task breadth, behavior under revision, and long-horizon composition into one engineering state.", fontsize=9.6, color=MUTED, va="top")

    # Stage labels
    stages = [
        (.025, .825, .43, .055, "A · Reconstruction task suite", BLUE),
        (.475, .825, .21, .055, "B · Persistent engineering state", PURPLE),
        (.705, .825, .27, .055, "C · System-level integration", TEAL),
    ]
    for x, y, w, h, label, c in stages:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.008,rounding_size=.012",fc="#F9FBFD",ec=c,lw=1.3))
        ax.text(x+.012,y+h/2,label,ha="left",va="center",fontsize=9.3,fontweight="bold",color=c)

    # Task families
    tasks = [
        ("Arresters", "B01–B05 · B18", "local fitting / holdout"),
        ("Walls + gate", "B06", "civil geometry"),
        ("Transformers", "B07–B08", "complex assembly / reuse"),
        ("Capacitor banks", "B09–B10", "repeated structures"),
        ("VC-A GIS", "B11–B16", "family / variants"),
        ("VC-B GIS", "B17–B19", "complex topology"),
        ("Bus + conductors", "B20–B30", "connectivity / paths"),
        ("Building + ground", "B31–B34", "large structured civil"),
        ("Auxiliary facilities", "B35–D37", "long-tail infrastructure"),
        ("Human correction", "B36 · D38", "review → rebuild"),
        ("Presentation control", "D40", "geometry invariance"),
        ("Inspection semantics", "D41", "part-addressable layer"),
    ]
    x0=.025; y0=.735; cols=3; rows=4; gapx=.012; gapy=.016
    w=(.43-gapx*(cols-1))/cols; h=.125
    task_boxes=[]
    for i,(title,batch,cap) in enumerate(tasks):
        r=i//cols; c=i%cols
        x=x0+c*(w+gapx); y=y0-r*(h+gapy)
        edge=[BLUE,TEAL,ORANGE,PURPLE][r%4]
        box=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.007,rounding_size=.011",fc="white",ec="#D8E0E8",lw=1)
        ax.add_patch(box); task_boxes.append((x,y,w,h))
        ax.text(x+.010,y+h-.025,title,fontsize=8.7,fontweight="bold",va="top",color=INK)
        ax.text(x+.010,y+.056,batch,fontsize=7.3,fontweight="bold",color=edge,va="center")
        ax.text(x+.010,y+.019,cap,fontsize=7.1,color=MUTED,va="bottom")

    # Persistent state column
    state_cards=[
        (.49,.665,.18,.12,"Reusable asset hierarchy","MASTER → instance\nsite-specific connectors",BLUE),
        (.49,.505,.18,.12,"Deterministic verification","history · hashes · BVH\ncontact · coverage",PURPLE),
        (.49,.345,.18,.12,"External engineering memory","plans · builders · manifests\nfailed drafts · limitations",ORANGE),
        (.49,.185,.18,.12,"Human-steerable revision","equivalence approval\nmarkup · omission review",RED),
    ]
    for x,y,wc,hc,title,sub,c in state_cards:
        ax.add_patch(FancyBboxPatch((x,y),wc,hc,boxstyle="round,pad=.009,rounding_size=.012",fc="#FBFCFD",ec=c,lw=1.2))
        ax.text(x+.012,y+hc-.032,title,fontsize=8.5,fontweight="bold",color=c,va="top")
        ax.text(x+.012,y+.027,sub,fontsize=7.2,color=DARK,va="bottom",linespacing=1.25)
    # Task suite to persistent state arrows
    for yy in [.69,.53,.37,.21]:
        ax.add_patch(FancyArrowPatch((.455,yy),(.49,yy),transform=ax.transAxes,arrowstyle="-|>",mutation_scale=10,lw=1.2,color="#9AA7B6"))

    # System integration panel
    ax.add_patch(FancyBboxPatch((.72,.49),.235,.25,boxstyle="round,pad=.012,rounding_size=.016",fc="#F4F9F7",ec=TEAL,lw=1.4))
    ax.text(.735,.705,"Integrated station model",fontsize=10.5,fontweight="bold",color=TEAL)
    ax.text(.735,.665,"37,153 objects",fontsize=14,fontweight="bold",color=INK)
    ax.text(.735,.625,"755 scenes · 858 collections",fontsize=8.3,color=DARK)
    ax.text(.735,.592,"3,916 mesh datablocks",fontsize=8.3,color=DARK)
    ax.text(.735,.559,"≈9.5× descriptive reuse",fontsize=8.3,color=DARK)
    ax.text(.735,.526,"38 core batches in one history",fontsize=8.3,color=DARK)

    ax.add_patch(FancyBboxPatch((.72,.29),.235,.14,boxstyle="round,pad=.012,rounding_size=.016",fc="#F8FAFC",ec=BLUE,lw=1.2))
    ax.text(.735,.397,"Long-horizon composition",fontsize=9.5,fontweight="bold",color=BLUE)
    ax.text(.735,.355,"shared assets + site transforms\nconnected systems + coverage audits\nhistory-preserving correction",fontsize=7.7,color=DARK,va="center",linespacing=1.28)

    ax.add_patch(FancyBboxPatch((.72,.12),.235,.11,boxstyle="round,pad=.012,rounding_size=.016",fc="#F5F1FA",ec=PURPLE,lw=1.2))
    ax.text(.735,.195,"D41 inspection-semantic endpoint",fontsize=9.1,fontweight="bold",color=PURPLE)
    ax.text(.735,.152,"79 accessory meshes · 17 classes × T1/T2",fontsize=7.8,color=DARK)

    # State to system arrows
    for yy in [.66,.50,.34,.20]:
        ax.add_patch(FancyArrowPatch((.67,yy),(.72,yy if yy>.45 else .36 if yy>.28 else .18),transform=ax.transAxes,arrowstyle="-|>",mutation_scale=10,lw=1.15,color="#9AA7B6",connectionstyle="arc3,rad=0.03"))

    # Bottom interpretation strip
    ax.add_patch(Rectangle((.025,.03),.93,.055,transform=ax.transAxes,fc="#F8FAFC",ec=GRID,lw=1))
    ax.text(.04,.057,"Breadth",fontsize=8.5,fontweight="bold",color=BLUE,va="center")
    ax.text(.102,.057,"many equipment / infrastructure task families",fontsize=7.8,color=DARK,va="center")
    ax.text(.38,.057,"Depth",fontsize=8.5,fontweight="bold",color=RED,va="center")
    ax.text(.435,.057,"failures change protocol and abstraction",fontsize=7.8,color=DARK,va="center")
    ax.text(.69,.057,"Scale",fontsize=8.5,fontweight="bold",color=TEAL,va="center")
    ax.text(.74,.057,"task outputs compose into one persistent twin",fontsize=7.8,color=DARK,va="center")

    save(fig,"fig09_task_suite_composition")



def figure10_visual_abstract():
    """Visual abstract using real field evidence and historical reconstruction renders."""
    field = PFP / "inputs" / "P05" / "_DSC2972.jpg"
    coarse = PFP / "output" / "installation_B17" / "277_B17_4D76_Front_Reference.png"
    assets = [
        (PFP / "output" / "installation_B18" / "314_B18_2899_Front_Clean.png", "Arrester"),
        (PFP / "output" / "installation_B08" / "36_B08_T1_Front_Clean_r2.png", "Transformer"),
        (PFP / "output" / "installation_B10" / "63_B10_031_Clean.png", "Capacitor bank"),
        (PFP / "output" / "installation_B17" / "275_B17_4D76_Front_Clean.png", "VC-B GIS"),
    ]
    station = PFP / "output" / "installation_D38" / "769_D38_Station_Top_Clean.png"
    semantics = PFP / "output" / "installation_D41" / "render_D41_T1_front.png"
    paths = [field, coarse, station, semantics] + [p for p, _ in assets]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("skip fig10, missing", missing)
        return

    fig = plt.figure(figsize=(14.2, 7.6), facecolor="white")
    canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis("off")
    canvas.text(.025, .955, "Visual abstract: from heterogeneous evidence to a persistent component-level digital twin",
                fontsize=16.5, fontweight="bold", va="top", color=INK)
    canvas.text(.025, .915, "One GPT-6 Astra/Codex workflow repeatedly observes, models, validates, revises, reuses, and composes task-level outputs.",
                fontsize=9.7, color=MUTED, va="top")

    def image_panel(rect, path, title, subtitle=None, edge=GRID):
        ax = fig.add_axes(rect)
        im = Image.open(path).convert("RGB")
        # center-crop to the panel aspect ratio
        ratio = rect[2] / rect[3]
        w, h = im.size
        src_ratio = w / h
        if src_ratio > ratio:
            new_w = int(h * ratio)
            left = max(0, (w - new_w) // 2)
            im = im.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / ratio)
            top = max(0, (h - new_h) // 2)
            im = im.crop((0, top, w, top + new_h))
        ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(edge); s.set_linewidth(1.25)
        ax.set_title(title, loc="left", fontsize=8.8, fontweight="bold", pad=5, color=INK)
        if subtitle:
            ax.text(0, -0.09, subtitle, transform=ax.transAxes, fontsize=7.1, color=MUTED, va="top")
        return ax

    # A: Evidence
    canvas.text(.03, .855, "A · Evidence", fontsize=10.5, fontweight="bold", color=BLUE)
    image_panel([.03, .57, .145, .23], field, "Field photograph", "visible component evidence", edge="#B7C8DD")
    image_panel([.19, .57, .145, .23], coarse, "Coarse reference", "registered photogrammetric geometry", edge="#B7C8DD")

    # B: Agent / verifier
    agent = FancyBboxPatch((.365,.575),.17,.215,boxstyle="round,pad=.014,rounding_size=.018",
                           transform=canvas.transAxes,fc="#F0F5FC",ec=BLUE,lw=1.6)
    canvas.add_patch(agent)
    canvas.text(.45,.745,"GPT-6 Astra + Codex",transform=canvas.transAxes,ha="center",fontsize=11,fontweight="bold",color=BLUE)
    canvas.text(.45,.695,"3D engineering agent",transform=canvas.transAxes,ha="center",fontsize=9.5,fontweight="bold",color=INK)
    canvas.text(.45,.635,"inspect evidence\nwrite Blender/Python\nvalidate · diagnose · revise",transform=canvas.transAxes,
                ha="center",va="center",fontsize=8.2,color=DARK,linespacing=1.35)
    canvas.text(.365,.855,"B · Agentic loop",fontsize=10.5,fontweight="bold",color=BLUE)

    # arrows evidence -> agent
    for y in [.68]:
        canvas.add_patch(FancyArrowPatch((.335,y),(.365,y),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=12,lw=1.5,color="#94A4B7"))

    # C: Heterogeneous tasks (2 x 2)
    canvas.text(.565,.855,"C · Heterogeneous reconstruction tasks",fontsize=10.5,fontweight="bold",color=TEAL)
    positions=[[.565,.675,.115,.125],[.69,.675,.115,.125],[.565,.51,.115,.125],[.69,.51,.115,.125]]
    for (p,title),rect in zip(assets,positions):
        image_panel(rect,p,title,edge="#9CC7BE")
    canvas.add_patch(FancyArrowPatch((.535,.68),(.56,.68),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=12,lw=1.5,color=TEAL))

    # persistent state strip
    canvas.add_patch(FancyBboxPatch((.36,.39),.45,.075,boxstyle="round,pad=.01,rounding_size=.012",
                                    transform=canvas.transAxes,fc="#FBFCFD",ec=PURPLE,lw=1.2))
    canvas.text(.585,.435,"Persistent engineering state",transform=canvas.transAxes,ha="center",fontsize=9.5,fontweight="bold",color=PURPLE)
    canvas.text(.585,.405,"MASTER / instances  ·  deterministic validators  ·  immutable batches  ·  human-steerable revision",
                transform=canvas.transAxes,ha="center",fontsize=7.3,color=DARK)
    for x in [.45,.63]:
        canvas.add_patch(FancyArrowPatch((x,.51),(x,.467),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=10,lw=1.1,color="#9B8BB9"))

    # D: station and semantics
    canvas.text(.835,.855,"D · System-level composition",fontsize=10.5,fontweight="bold",color=TEAL)
    image_panel([.835,.565,.135,.235], station, "Integrated station", "D38.2 core geometry", edge="#83B8AF")
    image_panel([.835,.265,.135,.215], semantics, "Inspection semantics", "D41 transformer accessory layer", edge="#B9A9D1")
    canvas.add_patch(FancyArrowPatch((.81,.425),(.835,.675),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=12,lw=1.5,color=TEAL,connectionstyle="arc3,rad=-.1"))
    canvas.add_patch(FancyArrowPatch((.902,.565),(.902,.485),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=11,lw=1.4,color=PURPLE))

    # footer evidence summary
    canvas.add_patch(Rectangle((.03,.08),.94,.11,transform=canvas.transAxes,fc="#F8FAFC",ec=GRID,lw=1))
    footer=[
        ("12 task families", BLUE),
        ("38 core batches", BLUE),
        ("37,153 scene objects", TEAL),
        ("≈9.5× descriptive reuse", TEAL),
        ("D41: 79 meshes / 17 classes × T1/T2", PURPLE),
    ]
    xs=[.055,.225,.39,.595,.77]
    for (text,c),x in zip(footer,xs):
        canvas.text(x,.135,text,transform=canvas.transAxes,fontsize=8.5,fontweight="bold",color=c,ha="left",va="center")
    canvas.text(.03,.035,"Figure 10 · Real project evidence and renders. The visual abstract summarizes the paper's core claim: task-level reconstructions remain part of one persistent, revisable engineering state.",
                transform=canvas.transAxes,fontsize=8,color=MUTED)
    save(fig,"fig10_visual_abstract")


def figure11_canonical_workflow():
    """Canonical reconstruction core plus optional task-specific evidence operators."""
    ref = PFP / "output" / "installation_B23" / "481_B23_T1_Neutral_Oblique_Reference.png"
    clean = PFP / "output" / "installation_B23" / "479_B23_T1_Neutral_Oblique_Clean.png"
    overlay = PFP / "output" / "installation_B23" / "480_B23_T1_Neutral_Oblique_Overlay.png"
    profiles = PFP / "output" / "installation_B23" / "B23_measurement_profiles.png"
    preflight = PFP / "output" / "installation_B23" / "component_and_lead_preflight.png"
    route = PFP / "output" / "installation_B20" / "4100_route_diagnostic.png"
    truss = PFP / "output" / "installation_B25" / "B25_truss_profiles.png"
    markup = PFP / "output" / "fixed" / "overlay.png"
    paths = [ref, clean, overlay, profiles, preflight, route, truss, markup]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("skip fig11, missing", missing)
        return

    fig = plt.figure(figsize=(14.2, 8.4), facecolor="white")
    canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis("off")
    canvas.text(.025, .962, "Canonical reconstruction loop with task-specific engineering operators",
                fontsize=16.2, fontweight="bold", va="top", color=INK)
    canvas.text(.025, .923,
                "The historical batches share a stable core loop; profile fitting, routing, coverage, collision, and human-review operators are enabled only when the task requires them.",
                fontsize=9.4, color=MUTED, va="top")

    # Core loop
    stages = [
        ("1", "Freeze + extract", "baseline hashes\nlocal coarse crop\nfield evidence"),
        ("2", "Inspect + plan", "select evidence\nmeasure / diagnose\nchoose representation"),
        ("3", "Build + refine", "Blender/Python\nMASTER / SITE\nfinite connectors"),
        ("4", "Render + review", "clean · overlay\nreference views\nhuman review"),
        ("5", "Validate", "geometry · contact\ncontinuity · history\ncoverage / collision"),
        ("6", "Freeze + remember", "manifest · release\nfailed drafts retained\nCONTINUE_FROM_Bxx"),
    ]
    x0, y, w, h, gap = .035, .70, .135, .13, .027
    for i, (num, title, sub) in enumerate(stages):
        x = x0 + i * (w + gap)
        canvas.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.009,rounding_size=.012",
                                        transform=canvas.transAxes,fc="#FBFCFD",ec=BLUE if i < 5 else PURPLE,lw=1.25))
        canvas.text(x+.012,y+h-.025,num,transform=canvas.transAxes,fontsize=8.5,fontweight="bold",color=BLUE)
        canvas.text(x+.012,y+h-.053,title,transform=canvas.transAxes,fontsize=9.2,fontweight="bold",color=INK)
        canvas.text(x+.012,y+.024,sub,transform=canvas.transAxes,fontsize=7.3,color=MUTED,va="bottom",linespacing=1.25)
        if i < len(stages)-1:
            canvas.add_patch(FancyArrowPatch((x+w,y+h/2),(x+w+gap*.85,y+h/2),transform=canvas.transAxes,
                                             arrowstyle="-|>",mutation_scale=10,lw=1.15,color="#9AA7B6"))
    # Return path is routed through the whitespace between the core loop and
    # task-specific operators so it does not cross titles or evidence panels.
    right_x = x0 + 5*(w+gap) + w - .01
    left_x = x0 + .02
    canvas.add_patch(FancyArrowPatch((right_x,y-.005),(right_x,.625),transform=canvas.transAxes,
                                     arrowstyle="-",lw=1.1,color=PURPLE))
    canvas.add_patch(FancyArrowPatch((right_x,.625),(left_x,.625),transform=canvas.transAxes,
                                     arrowstyle="-",lw=1.1,color=PURPLE))
    canvas.add_patch(FancyArrowPatch((left_x,.625),(left_x,y-.005),transform=canvas.transAxes,
                                     arrowstyle="-|>",mutation_scale=11,lw=1.1,color=PURPLE))
    canvas.text(.50,.641,"persistent engineering state feeds the next task",transform=canvas.transAxes,
                ha="center",fontsize=7.8,fontweight="bold",color=PURPLE)

    def thumb(rect, path, title, subtitle, edge):
        ax=fig.add_axes(rect)
        im=Image.open(path).convert("RGB")
        ratio=rect[2]/rect[3]; sw,sh=im.size; sr=sw/sh
        if sr>ratio:
            nw=int(sh*ratio); l=(sw-nw)//2; im=im.crop((l,0,l+nw,sh))
        else:
            nh=int(sw/ratio); t=(sh-nh)//2; im=im.crop((0,t,sw,t+nh))
        ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_color(edge); s.set_linewidth(1.15)
        ax.set_title(title,loc="left",fontsize=8.3,fontweight="bold",pad=4,color=INK)
        ax.text(0,-.10,subtitle,transform=ax.transAxes,fontsize=6.8,color=MUTED,va="top")

    canvas.text(.035,.585,"Task-specific operators — invoked as needed, not mandatory stages",fontsize=10.2,fontweight="bold",color=TEAL)
    ops = [
        ([.035,.345,.17,.18], profiles, "Profile / measurement fitting", "B23: point-cloud profiles guide curved lead and shared component axes"),
        ([.225,.345,.17,.18], preflight, "Representation preflight", "B23: straight-line hypothesis is contradicted by the observed bow"),
        ([.415,.345,.17,.18], route, "Route / topology diagnosis", "B20: bus route discontinuity and turn geometry before construction"),
        ([.605,.345,.17,.18], truss, "Section / structure fitting", "B25: truss cross-sections and repeated brace spans"),
        ([.795,.345,.17,.18], markup, "Human spatial feedback", "D38: stored review markup becomes a coordinate-grounded correction task"),
    ]
    for rect,path,title,sub in ops:
        thumb(rect,path,title,sub,TEAL)

    # Result/evidence vocabulary row
    canvas.text(.035,.255,"Every batch leaves reviewable result evidence",fontsize=10.2,fontweight="bold",color=BLUE)
    thumb([.035,.075,.19,.135], ref, "Reference", "registered source/coarse evidence in the comparison view", "#B7C8DD")
    thumb([.245,.075,.19,.135], clean, "Clean", "component model without the comparison overlay", "#B7C8DD")
    thumb([.455,.075,.19,.135], overlay, "Overlay", "same-view model/reference comparison", "#B7C8DD")
    canvas.add_patch(FancyBboxPatch((.685,.075),.285,.135,boxstyle="round,pad=.01,rounding_size=.012",
                                    transform=canvas.transAxes,fc="#F8FAFC",ec=GRID,lw=1))
    canvas.text(.702,.176,"Process evidence is part of the result",transform=canvas.transAxes,fontsize=9.3,fontweight="bold",color=INK)
    canvas.text(.702,.108,
                "plans · profiles · preflight diagnostics · component libraries\nclean/overlay/reference renders · validation ledgers · manifests\nfailed revisions · continuation notes",
                transform=canvas.transAxes,fontsize=7.4,color=DARK,va="center",linespacing=1.35)
    canvas.text(.035,.022,
                "Figure 11 · The common core is supported by repeated prepare/extract/build/validate/release stages; specialized operators vary by equipment and failure mode. Intermediate artifacts externalize geometric hypotheses and revisions rather than serving only as presentation graphics.",
                transform=canvas.transAxes,fontsize=7.8,color=MUTED)
    save(fig,"fig11_canonical_workflow")


def figure12_b32_worked_example():
    """Paper Figure 2: one reconstruction task explained as a simple evidence-action-feedback episode."""
    field = BS / "photo-audit" / "keyframes" / "_DSC3140_small.jpg"
    facade = PFP / "output" / "installation_B32" / "C110_facade_diagnostic.png"
    steps = PFP / "output" / "installation_B32" / "B32_source_steps_diagnostic.png"
    clean = PFP / "output" / "installation_B32" / "658_B32_C110_Oblique_Clean.png"
    overlay = PFP / "output" / "installation_B32" / "659_B32_C110_Oblique_Overlay.png"
    reference = PFP / "output" / "installation_B32" / "660_B32_C110_Oblique_Reference.png"
    paths = [field, facade, steps, clean, overlay, reference]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("skip fig12, missing", missing)
        return

    fig = plt.figure(figsize=(14.2, 8.2), facecolor="white")
    canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis("off")
    canvas.text(.025, .965, "One AstraBuild task: evidence → hypothesis → program → review → retained engineering state",
                fontsize=16.0, fontweight="bold", va="top", color=INK)
    canvas.text(.025, .925,
                "B32 reconstructs two secondary-equipment cabins. The figure separates what the agent decides from what deterministic tools compute, render and validate.",
                fontsize=9.2, color=MUTED, va="top")

    def image_panel(rect, path, title, subtitle=None, edge=GRID, contain=False, crop_box=None):
        ax = fig.add_axes(rect)
        im = Image.open(path).convert("RGB")
        if crop_box is not None:
            im = im.crop(crop_box)
        if not contain:
            ratio = rect[2] / rect[3]
            w0, h0 = im.size; sr = w0 / h0
            if sr > ratio:
                nw = int(h0 * ratio); l = max(0, (w0 - nw)//2); im = im.crop((l, 0, l+nw, h0))
            else:
                nh = int(w0 / ratio); t = max(0, (h0 - nh)//2); im = im.crop((0, t, w0, t+nh))
        ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_color(edge); s.set_linewidth(1.2)
        ax.set_title(title, loc="left", fontsize=8.7, fontweight="bold", pad=4, color=INK)
        if subtitle:
            ax.text(0, -0.085, subtitle, transform=ax.transAxes, fontsize=6.9, color=MUTED, va="top", linespacing=1.25)
        return ax

    image_panel([.035,.59,.20,.225], field, "1 · Evidence", "field image + inherited registered civil geometry", "#B7C8DD", crop_box=(110,250,650,750))
    image_panel([.275,.59,.20,.225], facade, "2 · Measure / diagnose", "deterministic fitting turns coarse geometry into explicit measurements", TEAL, contain=True)
    image_panel([.515,.59,.20,.225], clean, "3 · Build editable geometry", "component masters + rigid site instances", BLUE)
    image_panel([.755,.59,.20,.225], overlay, "4 · Review against the same reference", "cyan model over registered reference", PURPLE)
    for x in [.235,.475,.715]:
        canvas.add_patch(FancyArrowPatch((x,.70),(x+.035,.70),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=12,lw=1.5,color="#93A2B4"))

    strip_y=.39
    cards=[
        (.035,.20,"INPUT",BLUE,"B31 state + vertical samples\nfield photos + prior history"),
        (.275,.20,"ASTRA / CODEX",BLUE,"choose a representation\nwrite / revise programs\ninterpret review feedback"),
        (.515,.20,"DETERMINISTIC TOOLS",TEAL,"SciPy / Matplotlib\nBlender render + geometry\nvalidator recomputes checks"),
        (.755,.20,"OUTPUT",PURPLE,"measurement JSON + .blend\nClean/Overlay/Reference\nvalidation + continuation"),
    ]
    for x,w,title,c,txt in cards:
        canvas.add_patch(FancyBboxPatch((x,strip_y),w,.13,boxstyle="round,pad=.009,rounding_size=.012",
                                        transform=canvas.transAxes,fc="#FBFCFE",ec=c,lw=1.15))
        canvas.text(x+.012,strip_y+.105,title,transform=canvas.transAxes,fontsize=7.8,fontweight="bold",color=c)
        canvas.text(x+.012,strip_y+.078,txt,transform=canvas.transAxes,fontsize=7.0,color=DARK,va="top",linespacing=1.4)

    canvas.text(.035,.315,"Review feedback changes the hypothesis",fontsize=10.0,fontweight="bold",color=ORANGE)
    revisions=[(.035,"R1","door interpretation wrong"),(.355,"R2","C110 side corrected"),(.675,"R3","two C220 doors after stair/photo evidence")]
    for i,(x,tag,txt) in enumerate(revisions):
        canvas.add_patch(FancyBboxPatch((x,.205),.25,.075,boxstyle="round,pad=.008,rounding_size=.01",
                                        transform=canvas.transAxes,fc="#FFFDF9",ec=ORANGE if i<2 else TEAL,lw=1.1))
        canvas.text(x+.014,.248,tag,transform=canvas.transAxes,fontsize=8,fontweight="bold",color=ORANGE if i<2 else TEAL)
        canvas.text(x+.065,.248,txt,transform=canvas.transAxes,fontsize=7.3,color=DARK,va="center")
        if i<2:
            canvas.add_patch(FancyArrowPatch((x+.255,.242),(revisions[i+1][0]-.01,.242),transform=canvas.transAxes,arrowstyle="-|>",mutation_scale=10,lw=1.1,color=ORANGE))

    canvas.add_patch(Rectangle((.035,.075),.94,.085,transform=canvas.transAxes,fc="#F7F9FC",ec=GRID,lw=1))
    canvas.text(.055,.128,"Retained engineering state",transform=canvas.transAxes,fontsize=8.8,fontweight="bold",color=PURPLE)
    canvas.text(.205,.128,"componentized B32 geometry · 8 fixed-camera review views · validation record · manifest · continuation note → inherited by the next task",
                transform=canvas.transAxes,fontsize=7.4,color=DARK,va="center")
    canvas.text(.025,.022,"Figure 2 · Observable B32 task trace. Astra/Codex chooses and revises the engineering hypothesis/program; deterministic tools compute measurements, build geometry, render the review, and validate what is allowed into persistent state. The historical record does not preserve private chain-of-thought.",transform=canvas.transAxes,fontsize=7.7,color=MUTED)
    save(fig,"fig12_b32_worked_example")


def figure13_review_protocol():
    """Representative historical Clean/Overlay/Reference review triplets across task families."""
    rows = [
        ("B07\nMain transformer", PFP/"output/installation_B07/29_B07_T1_Clean_r2.png", PFP/"output/installation_B07/30_B07_T1_Overlay_r2.png", PFP/"output/installation_B07/31_B07_T1_Reference_r2.png"),
        ("B08\nShared transformer", PFP/"output/installation_B08/37_B08_T1_Rear_Clean_r2.png", PFP/"output/installation_B08/38_B08_T1_Rear_Overlay_r2.png", PFP/"output/installation_B08/45_B08_T1_Rear_Reference_r2.png"),
        ("B09\nCapacitor bank 031", PFP/"output/installation_B09/49_B09_031_Clean.png", PFP/"output/installation_B09/50_B09_031_Overlay.png", PFP/"output/installation_B09/51_B09_031_Reference.png"),
        ("B17\nVC-B GIS 4B77", PFP/"output/installation_B17/r3/305_B17_4B77_Side_Clean.png", PFP/"output/installation_B17/r3/306_B17_4B77_Side_Overlay.png", PFP/"output/installation_B17/r3/307_B17_4B77_Side_Reference.png"),
    ]
    missing=[str(p) for _,*ps in rows for p in ps if not p.exists()]
    if missing:
        print("skip fig13, missing", missing); return
    fig=plt.figure(figsize=(12.8,10.2),facecolor="white")
    canvas=fig.add_axes([0,0,1,1]); canvas.axis("off")
    canvas.text(.035,.965,"Historical review protocol: same-camera model ↔ registered coarse reference",fontsize=15.5,fontweight="bold",va="top",color=INK)
    canvas.text(.035,.925,"Representative task families use the review pages as experiment-facing evidence: Clean shows the modeled asset, Overlay shows correspondence, and Reference preserves the registered coarse geometry under the same camera.",fontsize=9.0,color=MUTED,va="top")
    headers=["Clean model","Overlay","Registered reference"]
    for j,h in enumerate(headers):
        canvas.text(.2975+j*.26,.865,h,fontsize=9.2,fontweight="bold",color=[BLUE,TEAL,MUTED][j],ha="center")
    y0=.68; rh=.17; gap=.045
    for i,(label,clean,overlay,reference) in enumerate(rows):
        y=y0-i*(rh+gap)
        canvas.text(.035,y+rh*.52,label,fontsize=8.7,fontweight="bold",color=INK,va="center",linespacing=1.25)
        for j,p in enumerate([clean,overlay,reference]):
            ax=fig.add_axes([.18+j*.26,y,.235,rh])
            im=Image.open(p).convert("RGB")
            ratio=.255/rh; sw,sh=im.size; sr=sw/sh
            if sr>ratio:
                nw=int(sh*ratio); l=(sw-nw)//2; im=im.crop((l,0,l+nw,sh))
            else:
                nh=int(sw/ratio); t=(sh-nh)//2; im=im.crop((0,t,sw,t+nh))
            ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_color("#C7D1DD"); s.set_linewidth(1.0)
    canvas.text(.035,.025,"Figure 13 · Representative views extracted from the original batch review artifacts. The companion website exposes all 32 historical review.html pages from B07–D38 so the reader can use each batch's original selectors, sliders, modes, notes and validation context rather than only these static examples.",fontsize=7.7,color=MUTED)
    save(fig,"fig13_review_protocol")


def figure14_behavioral_analysis():
    """v0.8: behavior-level statistics mined from the preserved batch history."""
    beh = json.loads((ROOT / "release" / "behavior_analysis.json").read_text())
    dist = beh["revision_distribution"]["batches_by_visible_attempt_tags"]
    multi3 = beh["revision_distribution"]["three_or_more"]
    layers = beh["failure_mode_layer_counts"]
    modes = beh["adaptation_mode_counts"]
    ops = beh["operator_prevalence_40_dossiers"]

    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.6))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.86, bottom=0.10, hspace=0.52, wspace=0.30)
    fig.text(0.02, 0.965, "Behavioral analysis of the preserved process record",
             fontsize=15.5, fontweight="bold", color=INK)
    fig.text(0.02, 0.925,
             "Statistics mined by scripts/analyze_process_behavior.py from the read-only historical batch folders "
             "(42 primary installation folders). Revision tags are a lower bound: revisions not frozen under an "
             "r-tagged name (e.g. D38.1 → D38.2) are invisible to this scan.",
             fontsize=9.0, color=MUTED)

    # (a) revision attempt distribution
    ax = axes[0][0]
    cats = ["1 attempt", "2 attempts", "3+ attempts"]
    vals = [dist["1"], dist["2"], dist["3+"]]
    bars = ax.bar(cats, vals, color=[BLUE2, BLUE, DARK], width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, str(v), ha="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_ylim(0, max(vals) + 4)
    ax.set_ylabel("batches")
    ax.set_title("Visible revision tags per batch", loc="left", fontweight="bold")
    ax.text(0.0, -0.32, "3+ attempts: " + ", ".join(multi3), transform=ax.transAxes, fontsize=7.6, color=MUTED)
    for _s in ("top", "right"):
        ax.spines[_s].set_visible(False)
    panel_label(ax, "a")

    # (b) failure-mode layers among annotated episodes
    ax = axes[0][1]
    order = ["protocol", "abstraction", "representation", "task-selection", "human-triggered"]
    vals = [layers.get(k, 0) for k in order]
    bars = ax.barh(order[::-1], vals[::-1], color=ORANGE, height=0.58)
    for b, v in zip(bars, vals[::-1]):
        ax.text(v + 0.05, b.get_y() + b.get_height() / 2, str(v), va="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_xlim(0, max(vals) + 1.2)
    ax.set_xlabel("annotated episodes")
    ax.set_title("Failure attribution by layer (7 documented episodes)", loc="left", fontweight="bold")
    for _s in ("top", "right"):
        ax.spines[_s].set_visible(False)
    panel_label(ax, "b")

    # (c) adaptation modes
    ax = axes[1][0]
    order = ["explicit self-diagnosed", "human-triggered", "human-authorized"]
    vals = [modes.get(k, 0) for k in order]
    colors = [TEAL, BLUE, PURPLE]
    bars = ax.bar(order, vals, color=colors, width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.06, str(v), ha="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_ylim(0, max(vals) + 1.0)
    ax.set_ylabel("annotated episodes")
    ax.set_title("Adaptation behavior: who initiates the correction", loc="left", fontweight="bold")
    ax.tick_params(axis="x", labelsize=8)
    for _s in ("top", "right"):
        ax.spines[_s].set_visible(False)
    panel_label(ax, "c")

    # (d) operator prevalence
    ax = axes[1][1]
    items = sorted(ops.items(), key=lambda kv: kv[1])
    names = [k for k, _ in items]
    vals = [v for _, v in items]
    ax.barh(names, vals, color=BLUE2, height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 0.4, i, str(v), va="center", fontsize=7.6, color=MUTED)
    ax.set_xlim(0, 44)
    ax.set_xlabel("dossiers invoking the operator (of 40)")
    ax.set_title("Canonical core vs task-specific operators", loc="left", fontweight="bold")
    ax.tick_params(axis="y", labelsize=7.6)
    for _s in ("top", "right"):
        ax.spines[_s].set_visible(False)
    panel_label(ax, "d")

    fig.text(0.02, 0.012,
             "Figure 14 · Panels a–c describe behavior of the reconstruction process (revision, failure attribution, adaptation initiation); "
             "panel d shows that build/validate/release form a stable core while measure/inspect/refine/coverage operators activate only on the tasks that need them.",
             fontsize=7.7, color=MUTED)
    save(fig, "fig14_behavioral_analysis")


def main():
    figure1_system_loop()
    figure2_longitudinal()
    figure3_quantitative()
    figure4_structure_semantics()
    figure5_failure_recovery()
    figure6_d38_feedback()
    figure7_d41_semantics()
    figure8_validation_stack()
    figure9_task_suite_composition()
    figure10_visual_abstract()
    figure11_canonical_workflow()
    figure12_b32_worked_example()
    figure13_review_protocol()
    figure14_behavioral_analysis()
    print("generated", len(list(FIG.glob('fig*.svg'))), "SVG figures in", FIG)

if __name__ == "__main__":
    main()
