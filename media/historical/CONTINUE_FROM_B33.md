# B33 保存与续作

当前工程 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B33/site_B33_entrance_service_buildings_r2.blend`，SHA256 `009050a5a745f05a889e6e4be115a1f56a851329ff7403d5ceb356f3177fc1df`。独立组件 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B33/B33_service_building_components_r2.blend`。R2为最终基线；R1保留。

广义目标仍 active：尽可能完善剩余室外建筑、土建和辅助设施。不要因建筑完成就标记整站目标完成。

B33_plan_r2.json保存两栋建筑及低构筑物参数。泵房7.1986×8.8558m，yaw−.373347°，roof4.34/parapet5.15；入口建筑12.6657×3.7481m，yaw−.361195°，roof3.32/parapet4.04。三墙拟合、正面缺失由侧墙端点与照片推断。泵房4窗1后门，入口7窗1门（背面5窗、西侧1窗/门、正面仅1处已辨认窗），遮挡面其余开口未确认。源屋面大面积缺失，细节尺寸近似。

泵房后平台顶.65、基底−.25，中央平台旋转宏观X−28.7..−24.8，外伸1.32，两侧各5级台阶顶.50/.35/.20/.05/−.10，前沿坡道栏杆高1.10；后门底升至.65。B33_pump_entry_diagnostic.png为原始台阶与栏杆证据。雨棚等细部仍为比例近似。爬梯西墙Y−65.53，底1.18顶6.30，与低屋面衔接。

低构筑物宏观X−49.4..−31，Y−67.35..−58.3，roof1.12/parapet1.62，3通气管+3检修盖+近泵房排气器。源有边墙、管帽，平顶按DJI0005補齐。没有地下空间建模。

9个旧 pump_house.* 通过新B33_RETAINED集合从新整站显示中剔除，旧对象/集合/场景完整保存。35034对象697场景7110整站直接对象；新3个主实例。B33_validation_r2核验历史、变换、真门窗洞无遮挡、台阶/屋面标高、刚性矩形根、独立组件重读、9个相机包络。B33_review.html九组/28内嵌图/控件检查通过。R2 GUI重读dirtyFalse，截图已看。

## B34 已准备

尚无B34 Blender几何、inputs/release。已有extract_B34_site.py、inspect_B34_site.py、measure_B34_site.py、mesh_B34_ground.py及对应npz/json/png。
SITE_LOW_reference.npz为全站低地面原三角形；SITE_PERIMETER_reference.npz为外边缘原三角形。源引用只读无另存。
B34_site_plan.json墙线宏观式：west x=.0055099*y−76.99351；east x=.00571555*y+12.43139；front y=−.00567651*x−69.03208。north两端Y45.30/44.82，长北墙在粗模缺失，需按两端补齐并注明推断。
B06已建西墙宏观a[−77.527,−68.769]到b[−77.029,21.501]、南墙分两段与门：西段[−17.761,−69.093]到[−77.527,−68.769]；东段[1.633,−69.198]到[−8.070,−69.146]；门中[−12.912,−68.396]，宽9.69。需要补西墙21.501..45、北墙、东墙、南东剩余1.633..12，保留既有墙/门不移位。
B34_ground_grid.npz：2m格网低近平面样本28分位，经插值和平滑，Z−.468..+.119；缺失区域是推断非测绘。B34_ground_mesh.npz为39897顶点65150三角形，面积10181.7448m²，材质索引0碎石/1沥青/2白边/3路缘/4步道；道路与碎石通过三角形裁切分区无重叠顶面。主环路中心线boundsX−54.65..−13.8、Y−54.2..32.3，圆角R9宽4.5；入口宽5.35通过x−13附近接入。步道含主建筑与附属建筑外圈、GIS两侧长条与端部横条。
需看B34_ground_layout.png（绘图进程结束后）核对道路合理性，然后从B33R2创建地坪、剩余墙。关注地面低于原基础导致悬空：可按真实基础底形新增向下混凝土接地裙，不能移动旧设备。部件必须通过父级+instance_offset完整展开，人工/程序核验需要。
后续B35：内部绿栅栏/门、路灯、CCTV、消防筒、标牌、低设备白围栏、小地面井盖等已见照片。三角形坡道绿色围栏宏观大概X−32..−11,Y−61..−41，由源继续定位置。不要盲目铺假设备。

原生MCP后台ps与shell PID不同；超时不等于退出。旧构建器只AST抽纯函数。新阶段继承release/inputs文件保护，不改冻结成果。user_prompt逐字“继续后续其他设备处理”。无技能或子代理。
