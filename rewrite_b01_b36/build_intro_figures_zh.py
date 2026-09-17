from pathlib import Path
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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
SOFT_BLUE = '#EAF1FA'
SOFT_TEAL = '#EAF6F3'
SOFT_ORANGE = '#FAF1E5'
SOFT_PURPLE = '#F0EDF7'
SOFT_GRAY = '#F6F8FB'

plt.rcParams.update({
    'font.family': 'WenQuanYi Zen Hei',
    'font.size': 9.5,
    'text.color': INK,
    'axes.unicode_minus': False,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
})


def crop_img(path, ratio=None):
    im = Image.open(path).convert('RGB')
    if ratio:
        w, h = im.size
        sr = w / h
        if sr > ratio:
            nw = int(h * ratio); left = max(0, (w - nw) // 2)
            im = im.crop((left, 0, left + nw, h))
        else:
            nh = int(w / ratio); top = max(0, (h - nh) // 2)
            im = im.crop((0, top, w, top + nh))
    return im


def hist(rel):
    p = HIST / rel
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def save(fig, stem):
    png = FIG / f'{stem}.png'
    fig.savefig(png, dpi=220, bbox_inches='tight')
    fig.savefig(FIG / f'{stem}.svg', bbox_inches='tight')
    plt.close(fig)
    Image.open(png).convert('RGB').save(FIG / f'{stem}.pdf', 'PDF', resolution=220.0)


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


def arrow(canvas, a, b, label=None, color=INK):
    x1, y1, w1, h1 = a; x2, y2, w2, h2 = b
    p1 = (x1 + w1, y1 + h1/2); p2 = (x2, y2 + h2/2)
    arr = FancyArrowPatch(p1, p2, transform=canvas.transAxes,
                          arrowstyle='-|>', mutation_scale=14, lw=1.35, color=color)
    canvas.add_patch(arr)
    if label:
        canvas.text((p1[0]+p2[0])/2, p1[1]+.035, label,
                    transform=canvas.transAxes, fontsize=7.7, color=MUTED,
                    ha='center', va='bottom')


def build_fig1():
    fig = plt.figure(figsize=(14.8, 7.7))
    canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis('off')
    canvas.text(.035, .963, '从配准物理证据到持久化工程模型', fontsize=18, fontweight='bold', va='top')
    canvas.text(.035, .918,
                'AstraBuild 将工程问题形成与数值几何计算分开：模型选择或修订操作，显式工具负责执行与验证，通过验收的状态再成为后续重建的上下文。',
                fontsize=9.4, color=MUTED, va='top')

    canvas.text(.035, .845, '1 · 物理证据 + 既有工程状态', fontsize=9.4, fontweight='bold', color=BLUE)
    field = ROOT / 'media' / 'field_gis.jpg'
    ref = hist('installation_B17/r3/307_B17_4B77_Side_Reference.png')
    add_image(fig, [.035, .545, .165, .225], field, '现场图像', '#AFC4DE', '可见部件结构与外观')
    add_image(fig, [.215, .545, .165, .225], ref, '配准粗模', '#AFC4DE', '度量布局、占用表面与遗漏区域')
    box(canvas, .035, .345, .345, .11, '继承的工程上下文',
        '已验收 Blender 状态 · 可复用资产 · 工程记录 · 既有验证 / 修订', fc=SOFT_GRAY, ec='#CAD4DF')

    reason = box(canvas, .43, .515, .185, .255, '2 · GPT-6 ASTRA / CODEX',
                 '选择证据 / 比较域\n选择表示方式\n分解任务\n编写或修订程序\n解释复核 / 验证反馈',
                 fc=SOFT_BLUE, ec='#9DB9DF', title_color=BLUE)
    tools = box(canvas, .65, .515, .155, .255, '3 · 确定性工具',
                '拟合 / 变换 / 样条\n构建几何\n固定视角渲染\n表面 / 端点 / 接触检查\n覆盖度 / 碰撞 / 状态保持检查',
                fc=SOFT_TEAL, ec='#9FCBC1', title_color=TEAL)
    arrow(canvas, (.38, .515, .0, .255), reason, '形成操作', BLUE)
    arrow(canvas, reason, tools, '执行', TEAL)

    station = hist('installation_B36/r3_previews/757_B36_Station_Clean.png')
    add_image(fig, [.835, .53, .145, .24], station, '4 · 已验证工程状态', '#9FCBC1', None)
    box(canvas, .69, .345, .29, .105, '持久化状态包含',
        '可编辑部件 · 具名接口 · 场站连接 · 既有变换 · 来源 / 验证状态',
        fc=SOFT_TEAL, ec='#9FCBC1', title_color=TEAL)
    canvas.add_patch(FancyArrowPatch((.807, .64), (.832, .64), transform=canvas.transAxes,
                                    arrowstyle='-|>', mutation_scale=14, lw=1.35, color=TEAL))
    canvas.add_patch(FancyArrowPatch((.91, .49), (.53, .49), transform=canvas.transAxes,
                                    arrowstyle='-|>', mutation_scale=14, lw=1.15,
                                    color=PURPLE, connectionstyle='arc3,rad=-0.09'))
    canvas.text(.72, .468, '通过验收的状态成为下一任务上下文', transform=canvas.transAxes,
                fontsize=8.0, color=PURPLE, ha='center', va='top')

    canvas.text(.035, .265, '主要纵向结果', fontsize=9.4, fontweight='bold', color=PURPLE)
    canvas.text(.035, .225, '基本循环保持稳定，但随着依赖累积，决策与算子集合不断扩展：', fontsize=9.2, color=INK)
    stages = [
        ('局部拟合', '比较域\n位姿 / 几何基元', SOFT_BLUE, BLUE),
        ('可复用范围', '共享 MASTER 与\n场站特定几何', SOFT_PURPLE, PURPLE),
        ('连接关系表示', '端口 · 路径 ·\n连续性 · 路径类别', SOFT_ORANGE, ORANGE),
        ('受既有状态约束的集成', '覆盖度 · 复核 ·\n保持 · 干涉', SOFT_TEAL, TEAL),
    ]
    xs = [.035, .275, .515, .755]; boxes=[]
    for x,(t,s,fc,ec) in zip(xs,stages):
        boxes.append(box(canvas,x,.07,.205,.115,t,s,fc=fc,ec=ec,title_color=ec))
    for i in range(3):
        arrow(canvas, boxes[i], boxes[i+1], None, color=MUTED)

    canvas.text(.035, .018,
                '图 1. AstraBuild 的持久化“证据–程序–验证”工作流。数值几何计算和结果验收显式位于语言模型之外；本文研究的是随着场景获得可复用、关系性和累积状态依赖，围绕该主干被选择的操作如何变化。',
                fontsize=7.8, color=MUTED, va='bottom')
    save(fig, 'fig01_problem_method_answer_b01_b36_zh')


def build_fig2():
    fig = plt.figure(figsize=(15.3, 7.8))
    ax = fig.add_axes([.055, .08, .91, .84]); ax.axis('off')
    ax.set_xlim(0.3, 36.7); ax.set_ylim(0, 10)
    ax.text(.35, 9.78, 'B01–B36：一条连续的重建记录', fontsize=18, fontweight='bold', va='top')
    ax.text(.35, 9.26,
            '四个描述性区段用于定位时间轴；八个锚点批次对应主文分析的关键决策。区段本身不构成统一难度尺度。',
            fontsize=9.5, color=MUTED, va='top')

    bands = [
        (1, 6, '局部拟合结构', SOFT_BLUE, BLUE),
        (7, 19, '重复设备', SOFT_PURPLE, PURPLE),
        (20, 30, '连接系统', SOFT_ORANGE, ORANGE),
        (31, 36, '场站闭合', SOFT_TEAL, TEAL),
    ]
    y0, bh = 4.05, .82
    for a,b,label,fc,ec in bands:
        ax.add_patch(FancyBboxPatch((a-.45,y0), (b-a+1)-.1, bh,
                                    boxstyle='round,pad=.015,rounding_size=.08', fc=fc, ec=ec, lw=1.0))
        ax.text((a+b)/2, y0+.57, f'B{a:02d}–B{b:02d}', ha='center', va='center', fontsize=9.0, fontweight='bold', color=ec)
        ax.text((a+b)/2, y0+.24, label, ha='center', va='center', fontsize=8.2, color=INK)
    for b in range(1,37):
        ax.plot([b,b],[3.76,4.01], color='#8E98A5', lw=.65)
        if b in [1,6,7,19,20,30,31,36]:
            ax.text(b,3.57,f'B{b:02d}',ha='center',va='top',fontsize=7.1,color=MUTED)

    thumbs = [
        (3.5, hist('installation_B01/B01_front_overlay.jpg'), '局部拟合'),
        (13, hist('installation_B08/42_B08_Transformer_Pair_r2.png'), '可复用设备'),
        (25, hist('installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png'), '连接关系表示'),
        (33.5, hist('installation_B36/r3_previews/757_B36_Station_Clean.png'), '累积场站状态'),
    ]
    for x,p,label in thumbs:
        xfrac = (x-0.3)/(36.4); rect = [.055 + .91*xfrac - .068, .605, .136, .185]
        ia = fig.add_axes(rect); ia.imshow(crop_img(p, rect[2]/rect[3])); ia.set_xticks([]); ia.set_yticks([])
        for s in ia.spines.values(): s.set_color(GRID); s.set_linewidth(.9)
        ia.set_title(label, fontsize=8.7, fontweight='bold', loc='left', pad=3)

    anchors = [
        (1.5, 5.35, 'B01/B02', '定义 / 修订\n比较域', BLUE),
        (8, 2.55, 'B08', '共享主变\nMASTER', PURPLE),
        (15, 5.35, 'B15', '修订共享与\n场站特定边界', PURPLE),
        (20, 2.55, 'B20', '端口 + 路径\n规划', ORANGE),
        (23, 5.35, 'B23', '直线 → 曲线\n表示', ORANGE),
        (25.5, 2.55, 'B25/B26', '覆盖度成为\n任务选择信号', ORANGE),
        (29, 5.35, 'B29', '跨子系统\n端点约束', ORANGE),
        (36, 2.55, 'B36', '状态保持 +\n干涉闭合', TEAL),
    ]
    for x,yy,batch,label,color in anchors:
        target_y = y0+bh if yy>4 else y0
        ax.plot([x,x],[target_y, yy-.15 if yy>4 else yy+.62], color=color, lw=1.0)
        ax.scatter([x],[y0+bh/2], s=34, color=color, edgecolor='white', linewidth=.7, zorder=4)
        ax.text(x, yy, batch, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color=color)
        ax.text(x, yy-.08, label, ha='center', va='top', fontsize=7.7, color=INK, linespacing=1.18)

    ax.text(.4, .55, '定位用途：后续任务继承此前已验收状态，因此时间轴描述的是一个不断增长的工程世界，而不是 36 次独立重复的同一任务。', fontsize=8.3, color=MUTED, va='bottom')
    ax.text(.4, .15, '图 2. 纵向研究地图。八个锚点用于解释比较域、复用边界、连接表示、由覆盖度驱动的闭合，以及继承状态下的集成。', fontsize=7.8, color=MUTED, va='bottom')
    save(fig, 'fig02_longitudinal_map_b01_b36_zh')


if __name__ == '__main__':
    build_fig1(); build_fig2()
    print(FIG / 'fig01_problem_method_answer_b01_b36_zh.png')
    print(FIG / 'fig02_longitudinal_map_b01_b36_zh.png')
