from pathlib import Path
import textwrap
from PIL import Image, ImageChops
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HIST = (HERE / '../../../photo-first-pilot/output').resolve()
FIG = HERE / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

INK = '#172033'
MUTED = '#5F6B7A'
GRID = '#DDE3EA'
BLUE = '#356CB6'
TEAL = '#2E8074'
ORANGE = '#C27A2C'
PURPLE = '#7865A5'
RED = '#B54A4A'
SOFT_BLUE = '#EAF1FA'
SOFT_TEAL = '#EAF6F3'
SOFT_ORANGE = '#FAF1E5'
SOFT_PURPLE = '#F0EDF7'
SOFT_GRAY = '#F6F8FB'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9.5,
    'text.color': INK,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
})


def crop_img(path, ratio=None):
    im = path.convert('RGB') if isinstance(path, Image.Image) else Image.open(path).convert('RGB')
    if ratio:
        w, h = im.size
        sr = w / h
        if sr > ratio:
            nw = int(h * ratio)
            left = max(0, (w - nw) // 2)
            im = im.crop((left, 0, left + nw, h))
        else:
            nh = int(w / ratio)
            top = max(0, (h - nh) // 2)
            im = im.crop((0, top, w, top + nh))
    return im


def relight_dark(im, bg_target=(241, 243, 248), bg_tol=42, gamma=0.62):
    """Re-light dark viewport renders for a light figure page: invert
    low-saturation wireframe, else replace dark bg + gamma-lift (hue kept)."""
    import numpy as np
    a = np.asarray(im.convert('RGB'), dtype=float) / 255.0
    corners = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3),
                              a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    if bg.mean() > 0.55:
        return im.convert('RGB')
    dist = np.abs(a - bg).sum(axis=2)
    content = a[dist >= bg_tol / 255.0 * 3]
    sat = float(np.abs(content.max(axis=1) - content.min(axis=1)).mean()) if content.size else 0.0
    if sat < 0.03:
        return Image.fromarray(((1.0 - a) * 255).astype('uint8'))
    out = np.power(a, gamma)
    out[dist < bg_tol / 255.0 * 3] = np.array(bg_target) / 255.0
    return Image.fromarray((out * 255).astype('uint8'))


def hist(rel):
    p = HIST / rel
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def save(fig, stem):
    for ext in ('png', 'svg', 'pdf'):
        fig.savefig(FIG / f'{stem}.{ext}', dpi=220 if ext == 'png' else None, bbox_inches='tight')
    plt.close(fig)


def add_image(fig, rect, path, title=None, border=GRID, subtitle=None):
    ax = fig.add_axes(rect)
    ratio = rect[2] / rect[3]
    ax.imshow(crop_img(path, ratio))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(1.0); s.set_color(border)
    if title:
        ax.set_title(title, fontsize=9.1, fontweight='bold', loc='left', pad=4)
    if subtitle:
        ax.text(0, -0.075, subtitle, transform=ax.transAxes, fontsize=7.7,
                color=MUTED, va='top', ha='left', linespacing=1.25)
    return ax


def box(canvas, x, y, w, h, title, lines, fc='white', ec=GRID, title_color=INK):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=.012,rounding_size=.014',
                       transform=canvas.transAxes, fc=fc, ec=ec, lw=1.2)
    canvas.add_patch(p)
    canvas.text(x + .018, y + h - .034, title, transform=canvas.transAxes,
                fontsize=9.5, fontweight='bold', color=title_color, va='top')
    canvas.text(x + .018, y + h - .083, lines, transform=canvas.transAxes,
                fontsize=8.1, color=INK, va='top', linespacing=1.42)
    return (x, y, w, h)


def arrow(canvas, a, b, label=None, color=INK, rad=0.0, yoff=0.0):
    x1, y1, w1, h1 = a
    x2, y2, w2, h2 = b
    p1 = (x1 + w1, y1 + h1/2 + yoff)
    p2 = (x2, y2 + h2/2 + yoff)
    arr = FancyArrowPatch(p1, p2, transform=canvas.transAxes,
                          arrowstyle='-|>', mutation_scale=14, lw=1.35,
                          color=color, connectionstyle=f'arc3,rad={rad}')
    canvas.add_patch(arr)
    if label:
        canvas.text((p1[0]+p2[0])/2, p1[1]+.035, label,
                    transform=canvas.transAxes, fontsize=7.7, color=MUTED,
                    ha='center', va='bottom')


def build_fig1():
    fig = plt.figure(figsize=(14.8, 7.7))
    canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis('off')

    canvas.text(.035, .963, 'From registered evidence to a persistent engineering model',
                fontsize=18, fontweight='bold', va='top')
    canvas.text(.035, .918,
                'AstraBuild separates engineering problem formulation from numerical geometry: the model chooses or revises an operation, explicit tools execute and validate it, and accepted state becomes context for later reconstruction.',
                fontsize=9.4, color=MUTED, va='top')

    # Evidence column
    canvas.text(.035, .845, '1 · PHYSICAL EVIDENCE + PRIOR STATE', fontsize=9.4,
                fontweight='bold', color=BLUE)
    field = ROOT / 'media' / 'field_gis.jpg'
    ref = hist('installation_B17/r3/307_B17_4B77_Side_Reference.png')
    add_image(fig, [.035, .545, .165, .225], field,
              'Field imagery', '#AFC4DE', 'visible component structure and appearance')
    add_image(fig, [.215, .545, .165, .225], ref,
              'Registered coarse geometry', '#AFC4DE', 'metric layout, occupied surfaces, and omissions')
    evidence_box = box(canvas, .035, .345, .345, .11, 'Inherited engineering context',
                       'accepted Blender state · reusable assets · engineering records · prior validation / revisions',
                       fc=SOFT_GRAY, ec='#CAD4DF')

    # Reasoning box
    reason = box(canvas, .43, .515, .185, .255, '2 · GPT-6 ASTRA / CODEX',
                 'select evidence/domain\nchoose representation\ndecompose the task\nwrite or revise the program\ninterpret review / validator feedback',
                 fc=SOFT_BLUE, ec='#9DB9DF', title_color=BLUE)

    # Deterministic tools box
    tools = box(canvas, .65, .515, .155, .255, '3 · DETERMINISTIC TOOLS',
                'fit / transform / spline\nconstruct geometry\nrender fixed views\ncheck surface / endpoint / contact\ncheck coverage / collision / preservation',
                fc=SOFT_TEAL, ec='#9FCBC1', title_color=TEAL)

    arrow(canvas, (.38, .515, .0, .255), reason, 'formulate', BLUE)
    arrow(canvas, reason, tools, 'execute', TEAL)

    # Output
    station = hist('installation_B36/r3_previews/757_B36_Station_Clean.png')
    out_ax = add_image(fig, [.835, .53, .145, .24], station,
                       '4 · VALIDATED STATE', '#9FCBC1', None)
    out_box = box(canvas, .69, .345, .29, .105, 'Persistent state contains',
                  'editable components · named interfaces · site connections · prior transforms · provenance / validation state',
                  fc=SOFT_TEAL, ec='#9FCBC1', title_color=TEAL)
    canvas.add_patch(FancyArrowPatch((.807, .64), (.832, .64), transform=canvas.transAxes,
                                    arrowstyle='-|>', mutation_scale=14, lw=1.35, color=TEAL))

    # Feedback / persistence loop
    canvas.add_patch(FancyArrowPatch((.91, .49), (.53, .49), transform=canvas.transAxes,
                                    arrowstyle='-|>', mutation_scale=14, lw=1.15,
                                    color=PURPLE, connectionstyle='arc3,rad=-0.09'))
    canvas.text(.72, .468, 'accepted state becomes the next task context', transform=canvas.transAxes,
                fontsize=8.0, color=PURPLE, ha='center', va='top')

    # Bottom answer band
    canvas.text(.035, .265, 'MAIN LONGITUDINAL RESULT', fontsize=9.4, fontweight='bold', color=PURPLE)
    canvas.text(.035, .225,
                'The common loop persists, but the decision/operator portfolio broadens as dependencies accumulate:',
                fontsize=9.2, color=INK)
    stages = [
        ('LOCAL FIT', 'comparison domain\npose / primitive', SOFT_BLUE, BLUE),
        ('REUSABLE SCOPE', 'shared MASTER vs\nsite-specific geometry', SOFT_PURPLE, PURPLE),
        ('CONNECTED REPRESENTATION', 'ports · routes ·\ncontinuity · path class', SOFT_ORANGE, ORANGE),
        ('STATE-CONSTRAINED INTEGRATION', 'coverage · review ·\npreservation · interference', SOFT_TEAL, TEAL),
    ]
    xs = [.035, .275, .515, .755]
    boxes=[]
    for x,(t,s,fc,ec) in zip(xs,stages):
        b=box(canvas,x,.07,.205,.115,t,s,fc=fc,ec=ec,title_color=ec); boxes.append(b)
    for i in range(3):
        arrow(canvas, boxes[i], boxes[i+1], None, color=MUTED)

    canvas.text(.035, .018,
                'Figure 1. AstraBuild as a persistent evidence–program–validation workflow. Numerical geometry and acceptance remain explicit outside the language model; the paper studies how the operation selected around that backbone changes as the reconstructed scene acquires reusable, relational, and accumulated-state dependencies.',
                fontsize=7.8, color=MUTED, va='bottom')
    save(fig, 'fig01_problem_method_answer_b01_b36')


def build_fig2():
    fig = plt.figure(figsize=(15.3, 7.0))
    ax = fig.add_axes([.045, .06, .92, .86]); ax.axis('off')
    ax.set_xlim(0.3, 36.7); ax.set_ylim(0, 10)
    ax.text(.35, 9.85, 'B01–B36: one sequential reconstruction record',
            fontsize=20, fontweight='bold', va='top')
    ax.text(.35, 9.15,
            'Four descriptive target bands orient the chronology; eight anchor batches locate the decisions analyzed in the main text. The bands are not a common difficulty scale.',
            fontsize=11.5, color=MUTED, va='top')

    bands = [
        (1, 6, 'Local fitted structures', SOFT_BLUE, BLUE),
        (7, 19, 'Repeated equipment', SOFT_PURPLE, PURPLE),
        (20, 30, 'Connected systems', SOFT_ORANGE, ORANGE),
        (31, 36, 'Site closure', SOFT_TEAL, TEAL),
    ]
    # Band thumbnails span their band exactly; each carries the band title.
    thumbs = [
        hist('installation_B01/B01_front_overlay.jpg'),
        hist('installation_B08/42_B08_Transformer_Pair_r2.png'),
        hist('installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png'),
        hist('installation_B36/r3_previews/757_B36_Station_Clean.png'),
    ]
    AX_L, AX_W = .045, .92
    X0, XW = 0.3, 36.4

    def fx(data_x):
        return AX_L + AX_W * (data_x - X0) / XW

    TH_Y, TH_H = .50, .27
    for (a, b, label, fc, ec), p in zip(bands, thumbs):
        left = fx(a - .45)
        width = fx(b + .45) - left
        rect = [left + .006, TH_Y, width - .012, TH_H]
        ia = fig.add_axes(rect)
        ia.imshow(crop_img(relight_dark(Image.open(p)), rect[2] / rect[3] * (15.3 / 7.0))); ia.set_xticks([]); ia.set_yticks([])
        for s in ia.spines.values():
            s.set_color(ec); s.set_linewidth(1.4)
        ia.set_title(f'B{a:02d}–B{b:02d} · {label}', fontsize=13, fontweight='bold',
                     loc='center', pad=5, color=ec)

    # Slim timeline strip with all 36 ticks.
    y0, bh = 3.5, .8
    for a, b, label, fc, ec in bands:
        ax.add_patch(FancyBboxPatch((a - .45, y0), (b - a + 1) - .1, bh,
                                    boxstyle='round,pad=.015,rounding_size=.08',
                                    fc=fc, ec=ec, lw=1.0))
    for bn in range(1, 37):
        ax.plot([bn, bn], [y0 - .26, y0 - .02], color='#8E98A5', lw=.8)
        if bn in (1, 6, 7, 19, 20, 30, 31, 36):
            ax.text(bn, y0 - .42, f'B{bn:02d}', ha='center', va='top', fontsize=9.5, color=MUTED)

    # Anchor callouts in two staggered rows below the timeline.
    anchors = [
        (1.5, 2.15, 'B01/B02', 'define / revise\ncomparison domain', BLUE),
        (15, 2.15, 'B15', 'revise reusable vs\nsite boundary', PURPLE),
        (23, 2.15, 'B23', 'straight → curved\nrepresentation', ORANGE),
        (28.6, 2.15, 'B29', 'endpoint constraints\nacross subsystems', ORANGE),
        (8, 0.95, 'B08', 'shared transformer\nMASTER', PURPLE),
        (19.6, 0.95, 'B20', 'ports + route\nplanning', ORANGE),
        (25.6, 0.95, 'B25/B26', 'coverage becomes a\ntask-selection signal', ORANGE),
        (34.8, 0.95, 'B36', 'preservation +\ninterference closure', TEAL),
    ]
    for x, yy, batch, label, color in anchors:
        ax.plot([x, x], [yy + .66, y0], color=color, lw=1.1)
        ax.scatter([x], [y0 + bh / 2], s=52, color=color, edgecolor='white', linewidth=.9, zorder=4)
        ax.text(x, yy, batch, ha='center', va='bottom', fontsize=11.5, fontweight='bold', color=color)
        ax.text(x, yy - .1, label, ha='center', va='top', fontsize=9.8, color=INK, linespacing=1.18)

    ax.text(.4, .05,
            'Orientation only: later tasks inherit accepted earlier state, so the chronology records a growing engineering world rather than 36 repeated trials of one fixed task.',
            fontsize=10, color=MUTED, va='bottom')
    save(fig, 'fig02_longitudinal_map_b01_b36')


if __name__ == '__main__':
    build_fig1()
    build_fig2()
    print(FIG / 'fig01_problem_method_answer_b01_b36.png')
    print(FIG / 'fig02_longitudinal_map_b01_b36.png')
