# B31 保存与续作

当前工程 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B31/site_B31_main_building_r2.blend`，SHA256 `22643b892ae05b9dd2c2eb0e18d31c9526c38dacf5c1a41641956118742c559b`。独立组件 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B31/B31_main_building_components_r2.blend`，SHA256 `e9d7fb04869bb34fcfa843e05e7f0edb0ec5414c6e67509cf0edcef4cbf09aa5`。R1 文件及全部历史版本保留；后续从 R2 继续，不能误用 R1。

## 持续目标

在已有基础上，继续对剩下的室外建筑，等剩下的进行建模。目标是尽可能的完善变电站建模。先保存已有成果，然后处理。

目标仍 active，本版只是主建筑阶段。B30 多数室外主设备目标之前已完成，新目标包含建筑、土建和辅助设施；不能因单栋建筑完成就标记整个新目标完成。

## 本版

保存前确认 B30 GUI dirtyFalse，逐字节复制到 `site_B31_before_buildings_checkpoint.blend`，SHA 与 B30 相同。保护前版 2859 个文件。

从粗模抽取中央土建走廊 4288747 个原三角形，`CENTRAL_CIVIL_reference.npz` 保留宏观顶点、面、原对象索引和原 loop_triangle 索引。`PERIMETER_reference.npz` 包含外边缘。`B31_vertical_samples.npz` 是 8 厘米体素化的竖直表面样本；`B31_existing_central_inventory.json` 是已有整站中央范围对象，不要整份输出。

主建筑四墙共享旋转拟合 yaw −0.292534°，尺寸 49.25876 × 12.74769 米，仍为矩形。世界框架在 `B31_building_plan_r2.json`；不要因为视图角度剪切几何。高低屋面分界局部 Y=−24.70，女儿墙顶 4.96 / 6.24，屋面 3.91 / 5.12。低屋面在粗模里大面积缺失，高屋面也不完整，按照片与高低关系补齐，非实测屋面高程。

12 窗=西10、正2；4 门=正1、西3；上9下10共19通风口；11 台空调=西4、东5、后2，共享 `B31_AC_OUTDOOR_UNIT_MASTER`。整体 `B31_MAIN_BUILDING_MASTER`，站内通过 `B31::MAIN_BUILDING` 的刚体框架实例放置。所有B31部件946个；展开实例会增加引用数量。两处爬梯分别位于后墙和屋面高低交界。

## 核验

原 33223 对象、618 场景、全部旧集合和材质结构保持；7113 个旧整站对象世界变换保持。T1/T2 共享部件仍同一个集合。946 个新几何对象和12个实例变换、洞口边界、屋面标高、刚性矩形框架、6相机包络、独立组件重读均已核验。R1与R2都独立保存并验证，最终R2报告 `B31_validation_r2.json`。

四个固定原奇数面墙域未按残差删点，有限模型表面 RMS 约0.018–0.032米；这些来自同一相关重建，不能解释为独立实测精度。门窗和空调等小部件尺寸近似。

R2 共22张预览；`B31_review.html` 6组同相机滑动对照、20张内嵌PNG。JS语法及6方向×3模式×3滑块位置控件检查通过。已看R1东西正后参考/模型、R2西东后/全站斜视俯视，GUI重读默认636，dirtyFalse。

## 接下来 B32

B32 目录已建立，只做了测量，尚无新几何、输入保护记录或发布。
`installation/measure_B32_containers.py`、`output/installation_B32/B32_container_measurements.json`、Cabin-A/Cabin-B立面诊断。
Cabin-A 宽2.80077、长9.19289米，yaw−0.286864°；Cabin-B 宽2.79861、长12.19722米，yaw−0.344053°。两者单独定位，公共白色横向墙板、青绿色屋顶/角柱、端部竖式空调、雨水管、舱门可复用；不要把短舱拉伸为长舱导致门/空调变形。
已看原图 DJI0010 和 DSC3117/3140 的110舱，DJI0002的220舱。两个舱短端中心都有竖式空调，长面白色板材与青绿角带。Cabin-B西侧局部Y约−48.1有单门，110舱另一侧门需看原图再定位。源顶面高度约110舱3.1、220舱2.9–3.0，需结合屋顶数据，不能把端面高点直接当统一顶高。

然后继续入口小建筑、已有泵房细化和低附属区域、道路/碎石地坪/步道、剩余围墙和监控照明等。已有泵房粗体 `T23052218322040428::pump_house.*` 在宏观X−32..−24、Y−67..−57，不能叠加一个实体造成双壳。前部大低矩形X−49..−31,Y−68..−58可能是水池/低附属区域，先看图不要盲目建成高楼。

## 操作

冻结本版所有文件，CURRENT可更新；新阶段进入B32。从 release_B31 与 inputs_B31 继承文件保护，保留所有历史物体和场景。需替换旧粗体时，从新整站显示集合移除，保留旧数据及场景。
原生 Blender `/data/program/blender-5.1.2-linux-x64/blender`，MCP可通过subprocess启动后台，env LD_LIBRARY_PATH 指向同路径lib。原生与shell PID命名空间不同，检查后台用MCP subprocess ps。超时不能当失败，不要重复启动。
父级和 instance_offset 必须计入，使用 build_B19 的 object_transform/expand 纯函数；旧构建器仅AST抽纯函数，不能import带顶层构建。
未用技能或子代理；MCP user_prompt逐字“继续后续其他设备处理”。
