from pathlib import Path
from PIL import Image, ImageChops
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import textwrap

HERE = Path(__file__).resolve().parent
HIST = (HERE / '../../../photo-first-pilot/output').resolve()
FIG = HERE / 'figures'
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'WenQuanYi Zen Hei','axes.unicode_minus':False})


def open_img(rel):
    p = HIST / rel
    if not p.exists(): raise FileNotFoundError(p)
    im = Image.open(p).convert('RGB')
    bg = Image.new('RGB', im.size, 'white')
    diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 8 else 0)
    bbox = diff.getbbox()
    if bbox:
        x0,y0,x1,y1=bbox; pad=max(8,int(min(im.size)*.015))
        bbox=(max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad))
        if (bbox[2]-bbox[0]) < im.width*.98 or (bbox[3]-bbox[1]) < im.height*.98:
            im=im.crop(bbox)
    return im


def image_card(ax, rel, title, caption):
    ax.imshow(open_img(rel)); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_linewidth(.8)
    ax.set_title(title,fontsize=10.5,fontweight='bold',loc='left',pad=5)
    ax.text(0,-.055,textwrap.fill(caption,28),transform=ax.transAxes,ha='left',va='top',fontsize=8.45,linespacing=1.20)


def add_arrow_between(fig, a, b, label=None):
    p1=a.get_position(); p2=b.get_position(); x1=p1.x1+.008; x2=p2.x0-.008; y=(p1.y0+p1.y1)/2
    fig.add_artist(FancyArrowPatch((x1,y),(x2,y),transform=fig.transFigure,arrowstyle='-|>',mutation_scale=13,linewidth=1.15))
    if label: fig.text((x1+x2)/2,y+.014,textwrap.fill(label,16),ha='center',va='bottom',fontsize=8.35)


def build_fig4():
    fig,axes=plt.subplots(3,3,figsize=(14.8,12.0))
    fig.subplots_adjust(left=.085,right=.985,top=.91,bottom=.09,hspace=.88,wspace=.28)
    fig.suptitle('为什么重建循环会扩展：三个结构性转变',fontsize=18,y=.965)
    fig.text(.5,.935,'每一行均使用 B01–B36 的保存工件说明：新增依赖改变的是工程决策，而不仅是拟合参数。',ha='center',fontsize=10.3)
    rows=[
        ('A  局部拟合 → 可复用范围',[
            ('installation_B01/B01_front_overlay.jpg','B01 · 局部拟合','单个对象：定义局部比较域，拟合位姿/尺度，然后验证。'),
            ('installation_B08/42_B08_Transformer_Pair_r2.png','B08 · 共享设备','两个安装位置共享一个主变 MASTER；现场线路仍位于共享资产之外。'),
            ('installation_B15/B15_profiles.png','B15 · 修订复用边界','不同安装位置的有限几何不同；公共短管范围被替换为场站特定段。')],
         ['重复引入不变性','复用边界成为可证伪假设']),
        ('B  对象几何 → 连接关系表示',[
            ('installation_B20/4100_route_diagnostic.png','B20 · 端口与路径','已有设备末端变成显式端口；剩余 4100 连接需要转向。'),
            ('installation_B23/B23_measurement_profiles.png','B23 · 改变表示类别','剖面证据暴露中部弯曲；连接由直线重新表述为受约束曲线。'),
            ('installation_B29/B29_crossline_fits.png','B29 · 大尺度关系约束','跨场导线在保持继承端点的同时拟合；连续性与表面拟合分开检查。')],
         ['出现关系约束','端点 / 拓扑约束扩展']),
        ('C  预定添加 → 缺口 / 状态驱动闭合',[
            ('installation_B25/B25_source_height_map.png','B25 · 未解释几何','配准高位结构仍远离当前场景，暴露资产清单未捕获的遗漏。'),
            ('installation_B26/543_B26_Structure_Overlay.png','B26 · 重建选定缺口','由覆盖度驱动的后续工作补建构架/防火墙，同时保持既有场站状态。'),
            ('installation_B36/B36_busbar_plan_overlay.png','B36 · 受状态约束的插入','后期母线构架路径必须保持继承端点，并与已有空间占用和基础设施协调。')],
         ['覆盖度成为任务信号','新几何必须适配既有工程世界'])]
    for r,(label,cards,arrows) in enumerate(rows):
        pos=axes[r,0].get_position(); fig.text(.012,(pos.y0+pos.y1)/2,label,rotation=90,va='center',ha='left',fontsize=10.2,fontweight='bold')
        for c,card in enumerate(cards): image_card(axes[r,c],*card)
        add_arrow_between(fig,axes[r,0],axes[r,1],arrows[0]); add_arrow_between(fig,axes[r,1],axes[r,2],arrows[1])
    fig.text(.085,.026,'图中使用历史工件作为工作流证据。该序列为描述性记录，并不建立普适复杂度规律，也不能证明模型随时间发生学习。',fontsize=9.0,ha='left')
    png=FIG/'fig04_structural_transitions_b01_b36_zh.png'
    fig.savefig(png,dpi=220,bbox_inches='tight')
    fig.savefig(FIG/'fig04_structural_transitions_b01_b36_zh.svg',bbox_inches='tight')
    plt.close(fig)
    Image.open(png).convert('RGB').save(FIG/'fig04_structural_transitions_b01_b36_zh.pdf','PDF',resolution=220.0)


def build_fig5():
    fig=plt.figure(figsize=(15.2,9.5)); fig.subplots_adjust(left=.04,right=.985,top=.88,bottom=.11)
    fig.suptitle('持久化外部状态把局部重建组合成连接的工程系统',fontsize=18,y=.965)
    fig.text(.5,.925,'后续批次显式使用此前的 MASTER、端子和端点；同一机制也会传播错误共享抽象，直到其被修订。',ha='center',fontsize=10.2)
    x0s=[.045,.285,.525,.765]; w,h,y=.19,.315,.49
    nodes=[
        ('B08','installation_B08/42_B08_Transformer_Pair_r2.png','共享主变 MASTER\n+ 持久化端子状态','一套可复用部件结构；T1/T2 为刚性场站实例。'),
        ('B23','installation_B23/r3/480_B23_T1_Neutral_Oblique_Overlay.png','连接使用已有\n主变端子','新的中性点引线几何相对于 B08 接口定义。'),
        ('B29','installation_B29/600_B29_G220_OUT_Detail_Overlay.png','导线复用此前\n线夹与端点','跳线 / 跨场导线连接此前已建子系统。'),
        ('B36','installation_B36/r2_previews/748_B36_T1_Rack_Overlay.png','后期母线构架闭合使用\n保存 stub 与空间占用','新路径闭合到继承主变接口，而无需重建已有设备。')]
    axes=[]
    for x0,(batch,rel,title,desc) in zip(x0s,nodes):
        ax=fig.add_axes([x0,y,w,h]); ax.imshow(open_img(rel)); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_linewidth(.8)
        fig.text(x0,y+h+.022,batch,fontsize=12.5,fontweight='bold',ha='left')
        fig.text(x0,y-.032,textwrap.fill(title,16),fontsize=9.9,fontweight='bold',ha='left',va='top')
        fig.text(x0,y-.100,textwrap.fill(desc,24),fontsize=8.4,ha='left',va='top',linespacing=1.18)
        axes.append(ax)
    labels=['使用 B08 端子','扩展既有端点图','闭合到保存 stub']
    for i in range(3):
        p1=axes[i].get_position(); p2=axes[i+1].get_position(); yy=y+h*.52; x1=p1.x1+.008; x2=p2.x0-.008
        fig.add_artist(FancyArrowPatch((x1,yy),(x2,yy),transform=fig.transFigure,arrowstyle='-|>',mutation_scale=14,linewidth=1.25))
        fig.text((x1+x2)/2,yy+.018,textwrap.fill(labels[i],12),ha='center',va='bottom',fontsize=8.35)

    bx,by,bw,bh=.245,.060,.39,.225
    fig.add_artist(FancyBboxPatch((bx,by),bw,bh,transform=fig.transFigure,boxstyle='round,pad=.012,rounding_size=.01',fill=False,linewidth=1.2))
    axb=fig.add_axes([bx+.012,by+.027,.125,bh-.054]); axb.imshow(open_img('installation_B15/r3/227_B15R2_756_Side_Overlay.png')); axb.set_xticks([]); axb.set_yticks([])
    for s in axb.spines.values(): s.set_linewidth(.7)
    fig.text(bx+.15,by+bh-.03,'B15 · 继承抽象会传播表示错误',fontsize=10.0,fontweight='bold',va='top')
    risk='多个安装实例继承了相同的有限母线短管范围，但相邻设备实际间距不同，因此发生重叠。修复重新划分 MASTER / 场站特定边界：可复用设备继续共享，有限连接移回场站特定范围。'
    fig.text(bx+.15,by+bh-.075,textwrap.fill(risk,34),fontsize=8.35,va='top',linespacing=1.20)
    p=axes[0].get_position(); fig.add_artist(FancyArrowPatch(((p.x0+p.x1)/2,p.y0-.01),(bx+.07,by+bh),transform=fig.transFigure,arrowstyle='-|>',mutation_scale=12,linewidth=1.0,linestyle='--'))
    fig.text(.13,.34,'共享抽象跨安装实例继承',fontsize=8.5,ha='center')

    sx,sy,sw,sh=.66,.070,.305,.19
    fig.add_artist(FancyBboxPatch((sx,sy),sw,sh,transform=fig.transFigure,boxstyle='round,pad=.012,rounding_size=.01',fill=False,linewidth=1.2))
    fig.text(sx+.012,sy+sh-.03,'B36 状态保持负担',fontsize=10.5,fontweight='bold',va='top')
    fig.text(sx+.012,sy+sh-.072,'36,615 个既有对象保持不变\n7,114 个既有场站变换保持不变\n2,798 个受保护文件保持不变\n最终 B36 文件包含 36,812 个对象',fontsize=9.0,va='top',linespacing=1.28)
    fig.text(sx+.012,sy+.012,textwrap.fill('这些是状态规模描述，不是经独立核验的真实物理资产数量。',34),fontsize=7.7,va='bottom')
    fig.text(.045,.018,'该依赖链记录了通过显式外部工程状态实现的组合；由于没有无状态对照，本图不声称持久化本身提高了精度。',fontsize=9.0,ha='left')
    png=FIG/'fig05_persistent_state_dependency_b01_b36_zh.png'
    fig.savefig(png,dpi=220,bbox_inches='tight')
    fig.savefig(FIG/'fig05_persistent_state_dependency_b01_b36_zh.svg',bbox_inches='tight')
    plt.close(fig)
    Image.open(png).convert('RGB').save(FIG/'fig05_persistent_state_dependency_b01_b36_zh.pdf','PDF',resolution=220.0)

if __name__=='__main__':
    build_fig4(); build_fig5()
    print(FIG/'fig04_structural_transitions_b01_b36_zh.png')
    print(FIG/'fig05_persistent_state_dependency_b01_b36_zh.png')
