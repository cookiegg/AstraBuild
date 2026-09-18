# B28 续作说明

当前 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B28/site_B28_outdoor_suspension_insulators.blend`，SHA `d9911b13470022524f7f215f71bcea49acd7abad7787a86fe99bb175cee8a774`；资产 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B28/B28_suspension_components.blend`，SHA `fa8fe99da78ed73a79f9b34ec2651f3d68bc0da1c44b8a8a43c1ef24bad73eb7`。GUI默认577_B28_G110_OUT_Detail_Clean，dirtyFalse，共31379对象、569场景。新增566–584共19场景：566/567全站clean/overlay；568–570 G110_OUT、571–573 G110_IN、574–576 G220_OUT；577–579 110首跨、580–582 220首跨；583/584分别短/长悬挂母版编辑。五组模型/粗模滑动对照及全站和两母版预览，链接/JS检查通过，未浏览器布局验收。

## 已完成

本轮B27中央12斜耐张串+24主变引线过渡已发布冻结，接着B28在三排装入42垂直悬挂绝缘子。源照片0014/0059原分辨率可见大小交替伞裙与连续芯杆，故新建两个长杆外观母版，未把中央离散盘片直接拉伸。110：1.55米伞裙段、12大+11小；220：3.00米、23大+22小；大伞裙r.133、小r.100、芯杆r.037。数量、材料与小金具照片近似，不是铭牌/制造图纸。

B28_SHORT_110_MASTER、B28_LONG_220_MASTER可编辑；42安装为刚性集合实例，共用几何、无缩放。每件按原偶数重建三角的Z分层中位数拟合独立X/Y轴线，上下眼接和末端销分开。顶端跨接条横过两根B25下弦，避免挂接点落在空梁中心。B28_ALL_SUSPENSION包含三个B28_<row>_SUSPENSION_SITE；全站保留B27全部集合再加入三个新安装集合，没有排除旧几何或移动两主变。

利用B25各row_reference.npz和_origins.json，未重提原始几何。inspect_B28_rows输出三排Y/Z诊断；fit_B28_suspension用梁下0.65–1.30米带、排除支架Y±.85米，识别24/6/12竖串；plan_B28_suspension用偶数三角拟合轴，固定奇数域保留。短串相同构型在外排梁底约10.1米及内排约12.0米安装；长串在220梁底约13.8米安装。悬挂本体顶面设梁下.33米，末端在本体底面沿轴下.24米。

各排Y种子见B28_suspension_initial/plan，24外排在−62.4至−20.9及+27.6至+39.0；6内排−15.77/−13.77/−11.76与−.76/+1.25/+3.25；12长串−54.1至−12.2。无对应设备的空跨没有补虚构悬挂件。

首次首跨展示集合按高度裁切时单独留下旧支架法兰/横撑，refine_B28_detail_views只移除两个新展示集合中的非SPAN旧B25件链接并重建两个青色代理。全站/资产不改，重渲染577–582六图，随后重新运行完整validate_B28。初版验证保存B28_validation_initial，.blend1是展示清理前备份。现场安装集合和历史场景均保持。

## 核验

最终文件原生读回：31032旧对象、550旧场景、685旧集合、337旧材质和旧站场世界变换保持；两主变、305/306共享关系保持。42刚性实例及上下连接轴间隙最大0.00000774米，7组视角实际包容，全部安装与两母版资产结构/材质回读相同。固定42粗模域表面RMS：G110_OUT 2.2–3.2厘米；G110_IN 2.1–2.7厘米；G220_OUT 2.0–2.7厘米。不删残差、没有测绘容差主张，未以每个5厘米清零作为目标。2663以前文件保护。B28发布后冻结，CURRENT可变。

## 下一步：斜耐张串、跳线与主要导线

目标继续为“请持续进行变电站建模任务，直到室外设备大都实现建模与对齐。”42垂直悬挂下方主要引线仍未补，斜耐张串也仍明显缺失。不要把这些实际缺项误当小误差而标完成，也不要把内部语义153行或形式晋升当目标。

next_strain_candidates.json是源粗模初步候选，未确认设备数：G110_OUT负X侧24，与竖串对应；G110_IN正X侧6，与竖串对应；G220_OUT正X侧14（其中+29/+31两个可能是交叉导线或无关面，不能直接安装），负X侧6也需核实与主变跨场线关系。搜索帯为距梁X0.95–1.55米、Z相对梁−1.15至+1.1米，排除支架Y±.8米，因此只是种子。源照片0014正面可见110斜串和U形跳线，0059可见220近水平斜串和向GIS下引双线。垂直长杆有交替大小伞裙，斜串需分别看其真实轮廓，不盲目复用。

目前B25 corridor X范围：G110_OUT[-77,-69.5]、G110_IN[-64,-56]、G220_OUT[4,13]；若斜串/导线超边界应从01_SOURCE_MESH__registered_clay扩大提取。宏观frame_to_world继续沿B20，见B28 plan；X横站、Y沿GIS排，别当worldXYZ。B27中央连接末端和纠正的B08末端读法见CONTINUE_FROM_B27。B26墙梁与B25三排位置见各自plan，不重新建。

进一步补主要线路后结合原图、注册粗模和真实全站保存场景审查室外大多数覆盖。剩余小金具、局部爬梯或高杆顶部重建缺损可列精修，不无限追逐内部阈值。当前从B28继续B29。

## 执行注意

Blender5.1.2原生后台经MCP启动，LD_LIBRARY_PATH=/data/program/blender-5.1.2-linux-x64/lib。所有MCP user_prompt逐字“继续后续其他设备处理”。GUIexec脚本需__file__全局，纯函数AST抽取而不import旧builder顶层。object_transform/expand需parent-aware及instance_offset；未激活场景matrix_world缓存不可靠。shell PID namespace不同，MCP ps核对原生进程；工具超时不是任务终止，日志Blender quit/原生pid终止证明结束。图片原分辨率要view_image(detail='original')并image(v.image_url,'original')，未裁图/修改原图。无skill/subagent。
