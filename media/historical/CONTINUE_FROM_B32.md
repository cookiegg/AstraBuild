# B32 保存与续作

当前工程 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B32/site_B32_secondary_equipment_cabins_r3.blend`，SHA256 `b0265b2626a009cea20056b08d01e671d0761952710185b375b0cfd3780a587f`。独立组件 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B32/B32_cabin_components_r3.blend`。从 R3 继续；R1/R2 保留，不作为后续基线。之前 B31/B30 及所有冻结版本保持。

广义目标仍 active：在已有基础上尽可能完善剩余室外建筑、土建和辅助设施；不能因设备舱完成标记整站目标完成。

两座舱独立矩形旋转拟合，Cabin-A 2.80077 × 9.19289米 yaw−0.286864°；Cabin-B 2.79861 × 12.19722米 yaw−0.344053°。框架及原三角形奇偶对照域在 B32_container_measurements.json。共享两种主组件 B32_CABIN_END_WALL_HVAC_MASTER / B32_CABIN_DOOR_MASTER，四端部与三门；各舱 SITE 根实例在 B32_CABINS_SITE。

门位修正：Cabin-A 东侧局部Y−3.90；Cabin-B 西侧Y−5.50与+5.32。源台阶诊断 B32_source_steps_diagnostic.png。B31续作记录中曾把220舱西侧中部凹陷当门，已被照片和两端台阶证据纠正，不能再沿用。角条和板缝已经裁开门洞，楼梯基底采用源地面−.13/−.30，顶面.28/.13；小构件尺寸近似。

最终 B32_validation_r3.json 验证全部旧数据/场景结构、7114旧整站位置、新对象/实例变换、真实门洞无遮挡、台阶标高、组件独立重读和八个相机包络。三面/四面墙域为同源相关重建，残差不可作独立测绘精度。B32_review.html八组同相机滑动对照，25内嵌图，JS与控件检查通过。GUI重读R3，dirtyFalse，截图已看。

下一阶段 B33 已有 inspect_B33_buildings.py / measure_B33_buildings.py / plan_B33.py 和 B33_plan.json，还未建模。泵房7.1986×8.8558米，源三面墙拟合，前面从侧墙端点推断；入口小建筑12.6657×3.7481米，前面同样缺失需照片补齐。屋面大面积源缺失。泵房邻近低构筑物X−49.4..−31、Y−67.35..−58.3，屋面约1.12/女儿墙1.62，3通气管+3检修盖可见于DJI0005。不要建成高楼。

旧泵房共9个 pump_house.* 粗件需从新整站显示集合剔除，但保留历史对象/集合/场景；新建保留集合，不直接修改旧集合。之后继续道路碎石步道、缺失围墙、内部绿栅栏、路灯监控消防标牌等。

框架变换使用 build_B19 纯函数 object_transform/expand，计入父级与instance_offset。旧构建器仅AST提纯函数，不可导入顶层。原生MCP后台ps与shell PID不同，超时不等于失败。user_prompt逐字“继续后续其他设备处理”。没有子代理或技能。
