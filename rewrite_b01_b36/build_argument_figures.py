from pathlib import Path
from PIL import Image, ImageChops
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import textwrap

HERE = Path(__file__).resolve().parent
HIST = (HERE / '../../../photo-first-pilot/output').resolve()
FIG = HERE / 'figures'
FIG.mkdir(parents=True, exist_ok=True)


def open_img(rel):
    p = HIST / rel
    if not p.exists():
        raise FileNotFoundError(p)
    im = Image.open(p).convert('RGB')
    # Trim generous white margins on diagnostics while leaving dark Blender renders intact.
    bg = Image.new('RGB', im.size, 'white')
    diff = ImageChops.difference(im, bg).convert('L')
    # Ignore very faint antialiasing/noise.
    diff = diff.point(lambda v: 255 if v > 8 else 0)
    bbox = diff.getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        pad = max(8, int(min(im.size) * 0.015))
        bbox = (max(0, x0-pad), max(0, y0-pad), min(im.width, x1+pad), min(im.height, y1+pad))
        # Only crop if it actually removes a meaningful white border.
        if (bbox[2]-bbox[0]) < im.width * 0.98 or (bbox[3]-bbox[1]) < im.height * 0.98:
            im = im.crop(bbox)
    return im


def image_card(ax, rel, title, caption):
    ax.imshow(open_img(rel))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.8)
    ax.set_title(title, fontsize=10.5, fontweight='bold', loc='left', pad=5)
    ax.text(0.0, -0.055, textwrap.fill(caption, 48), transform=ax.transAxes,
            ha='left', va='top', fontsize=8.45, linespacing=1.20)


def add_arrow_between(fig, ax_left, ax_right, label=None, y_bias=0.0):
    p1 = ax_left.get_position(); p2 = ax_right.get_position()
    x1 = p1.x1 + 0.008; x2 = p2.x0 - 0.008
    y = (p1.y0 + p1.y1) / 2 + y_bias
    arr = FancyArrowPatch((x1, y), (x2, y), transform=fig.transFigure,
                          arrowstyle='-|>', mutation_scale=13, linewidth=1.15)
    fig.add_artist(arr)
    if label:
        fig.text((x1+x2)/2, y+0.014, textwrap.fill(label, 28), ha='center', va='bottom', fontsize=8.35)


def build_fig4():
    fig, axes = plt.subplots(3, 3, figsize=(14.8, 12.0))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.91, bottom=0.09, hspace=0.88, wspace=0.28)
    fig.suptitle('Why the reconstruction loop broadens: three structural transitions', fontsize=18, y=0.965)
    fig.text(0.5, 0.935,
             'Each row uses preserved B01–B36 artifacts to show how a new dependency changes the engineering decision, not just the fitted parameters.',
             ha='center', fontsize=10.3)

    rows = [
        (
            'A  Local fit → reusable scope',
            [
                ('installation_B01/B01_front_overlay.jpg', 'B01 · local fit',
                 'One object: define a local comparison domain, fit pose/scale, then validate.'),
                ('installation_B08/42_B08_Transformer_Pair_r2.png', 'B08 · shared equipment',
                 'Two installations share one transformer MASTER; site routes remain outside the shared asset.'),
                ('installation_B15/B15_profiles.png', 'B15 · revise the reuse boundary',
                 'Finite site geometry differs across installations; common spool extent is replaced by site-specific segments.'),
            ],
            ['repetition introduces invariance', 'reuse boundary becomes falsifiable']
        ),
        (
            'B  Object geometry → connected representation',
            [
                ('installation_B20/4100_route_diagnostic.png', 'B20 · ports and routes',
                 'Existing equipment ends become explicit ports; one remaining 4100 connection requires a turn.'),
                ('installation_B23/B23_measurement_profiles.png', 'B23 · change representation class',
                 'Profile evidence exposes a mid-span bow; the connection is reformulated from straight to a constrained curve.'),
                ('installation_B29/B29_crossline_fits.png', 'B29 · relational constraints at scale',
                 'Crossyard conductors are fit while preserving inherited endpoints; continuity and surface fit are checked separately.'),
            ],
            ['relationship constraints appear', 'endpoint/topology constraints scale']
        ),
        (
            'C  Scheduled addition → gap/state-driven closure',
            [
                ('installation_B25/B25_source_height_map.png', 'B25 · unexplained geometry',
                 'Registered high structures remain far from the current scene, exposing omissions not captured by inventory status alone.'),
                ('installation_B26/543_B26_Structure_Overlay.png', 'B26 · reconstruct selected gaps',
                 'Coverage-driven follow-up adds missing gantry/firewall structure while retaining the existing station state.'),
                ('installation_B36/B36_busbar_plan_overlay.png', 'B36 · state-constrained insertion',
                 'Late bus-rack routes must preserve inherited endpoints and reconcile with occupied space and existing infrastructure.'),
            ],
            ['coverage becomes a task signal', 'new geometry must fit the existing world']
        ),
    ]

    for r, (label, cards, arrow_labels) in enumerate(rows):
        # Row label to the left of the first card.
        pos = axes[r, 0].get_position()
        fig.text(0.012, (pos.y0+pos.y1)/2, label, rotation=90, va='center', ha='left', fontsize=10.2, fontweight='bold')
        for c, card in enumerate(cards):
            image_card(axes[r, c], *card)
        add_arrow_between(fig, axes[r, 0], axes[r, 1], arrow_labels[0])
        add_arrow_between(fig, axes[r, 1], axes[r, 2], arrow_labels[1])

    fig.text(0.085, 0.026,
             'Historical artifacts are shown as evidence of the documented workflow. The sequence is descriptive; it does not establish a universal complexity law or model learning over time.',
             fontsize=9.0, ha='left')

    for ext in ['png', 'svg', 'pdf']:
        fig.savefig(FIG / f'fig04_structural_transitions_b01_b36.{ext}', dpi=220 if ext=='png' else None, bbox_inches='tight')
    plt.close(fig)


def build_fig5():
    fig = plt.figure(figsize=(15.2, 9.5))
    fig.subplots_adjust(left=0.04, right=0.985, top=0.88, bottom=0.11)
    fig.suptitle('Persistent external state turns local reconstructions into a connected engineering system', fontsize=18, y=0.965)
    fig.text(0.5, 0.925,
             'Later batches explicitly consume earlier masters, terminals, and endpoints; the same mechanism propagates a wrong shared abstraction until it is revised.',
             ha='center', fontsize=10.2)

    # Main chain thumbnails.
    x0s = [0.045, 0.285, 0.525, 0.765]
    w, h, y = 0.19, 0.315, 0.49
    nodes = [
        ('B08', 'installation_B08/42_B08_Transformer_Pair_r2.png',
         'Shared transformer MASTER\n+ persistent terminal state',
         'One reusable component structure; T1/T2 are rigid site instances.'),
        ('B23', 'installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png',
         'Connection uses an existing\ntransformer terminal',
         'New neutral-lead geometry is defined relative to a B08 interface.'),
        ('B29', 'installation_B29/600_B29_G-B_OUT_Detail_Overlay.png',
         'Conductors reuse prior\nclamps and endpoints',
         'Jumpers/crossyard conductors connect previously modeled subsystems.'),
        ('B36', 'installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png',
         'Late bus-rack closure uses\npreserved stubs and occupancy',
         'New routes close onto inherited transformer interfaces without rebuilding them.'),
    ]

    axes=[]
    for x0,(batch,rel,title,desc) in zip(x0s,nodes):
        ax=fig.add_axes([x0,y,w,h])
        ax.imshow(open_img(rel)); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_linewidth(0.8)
        fig.text(x0, y+h+0.022, batch, fontsize=12.5, fontweight='bold', ha='left')
        fig.text(x0, y-0.032, textwrap.fill(title, 30), fontsize=9.9, fontweight='bold', ha='left', va='top')
        fig.text(x0, y-0.100, textwrap.fill(desc, 38), fontsize=8.4, ha='left', va='top', linespacing=1.18)
        axes.append(ax)

    arrow_labels = [
        'uses B08 terminal',
        'extends prior endpoint graph',
        'closes onto preserved stubs',
    ]
    for i in range(3):
        p1=axes[i].get_position(); p2=axes[i+1].get_position(); yy=y+h*0.52
        x1=p1.x1+0.008; x2=p2.x0-0.008
        arr=FancyArrowPatch((x1,yy),(x2,yy), transform=fig.transFigure,
                            arrowstyle='-|>', mutation_scale=14, linewidth=1.25)
        fig.add_artist(arr)
        fig.text((x1+x2)/2, yy+0.018, textwrap.fill(arrow_labels[i], 25), ha='center', va='bottom', fontsize=8.35)

    # B15 risk branch.
    bx, by, bw, bh = 0.245, 0.060, 0.39, 0.225
    box = FancyBboxPatch((bx,by),bw,bh, transform=fig.transFigure,
                         boxstyle='round,pad=0.012,rounding_size=0.01', fill=False, linewidth=1.2)
    fig.add_artist(box)
    axb=fig.add_axes([bx+0.012, by+0.027, 0.125, bh-0.054])
    axb.imshow(open_img('installation_B15/r3/227_B15R2_756_Side_Overlay.png'))
    axb.set_xticks([]); axb.set_yticks([])
    for s in axb.spines.values(): s.set_linewidth(0.7)
    fig.text(bx+0.15, by+bh-0.03, 'B15 · inherited abstraction can propagate an error', fontsize=10.0, fontweight='bold', va='top')
    risk = ('A common finite bus-spool extent was inherited across installations and overlapped neighbors with different site separations. '
            'Recovery revised the MASTER/site boundary: reusable equipment stayed shared, while finite connectors moved to site scope.')
    fig.text(bx+0.15, by+bh-0.075, textwrap.fill(risk, 62), fontsize=8.35, va='top', linespacing=1.20)
    # Dashed conceptual edge from B08 main state to risk box.
    p=axes[0].get_position()
    arr=FancyArrowPatch(((p.x0+p.x1)/2, p.y0-0.01), (bx+0.07, by+bh), transform=fig.transFigure,
                        arrowstyle='-|>', mutation_scale=12, linewidth=1.0, linestyle='--')
    fig.add_artist(arr)
    fig.text(0.13, 0.34, 'shared abstraction inherited across sites', fontsize=8.5, ha='center')

    # B36 preservation summary.
    sx, sy, sw, sh = 0.66, 0.070, 0.305, 0.19
    box2 = FancyBboxPatch((sx,sy),sw,sh, transform=fig.transFigure,
                          boxstyle='round,pad=0.012,rounding_size=0.01', fill=False, linewidth=1.2)
    fig.add_artist(box2)
    fig.text(sx+0.012, sy+sh-0.03, 'B36 preservation burden', fontsize=10.5, fontweight='bold', va='top')
    fig.text(sx+0.012, sy+sh-0.072,
             '36,615 previous objects unchanged\n7,114 previous station transforms unchanged\n2,798 protected files unchanged\n36,812 objects in the final B36 file',
             fontsize=9.0, va='top', linespacing=1.28)
    fig.text(sx+0.012, sy+0.012, textwrap.fill('State-scale descriptors, not counts of independently verified physical assets.', 58), fontsize=7.7, va='bottom')

    fig.text(0.045, 0.018,
             'The dependency chain documents composition through explicit external engineering state; no stateless control run is available, so the figure does not claim that persistence improves accuracy.',
             fontsize=9.0, ha='left')

    for ext in ['png','svg','pdf']:
        fig.savefig(FIG / f'fig05_persistent_state_dependency_b01_b36.{ext}', dpi=220 if ext=='png' else None, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    build_fig4()
    build_fig5()
    print(FIG / 'fig04_structural_transitions_b01_b36.png')
    print(FIG / 'fig05_persistent_state_dependency_b01_b36.png')
