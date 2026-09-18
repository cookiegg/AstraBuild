# D41 主变巡检附件并入（T1/T2 试点）

## 目标

把 12MZ 巡检级语义组（`12MZ0000000150023`,#1主变ABC相）中 **B08 站内重建组件缺失的附件**
按 B08 主站框架对齐后并入站内 T1/T2 两台主变，使官方 36 个巡视点位在场景中"看得见、有坐标"。
不改动 D40 及之前任何工程文件；本批次基于 D40 副本另存。

## 背景（调研结论）

- 站内可见主变 = B08 重建组件（`B08_TRANSFORMER_MASTER`，集合实例）:
  - T1 `B08::T1.SHARED_ASSEMBLY` @ (-3.158, -39.493, 0.500), rotZ -1.13 rad
  - T2 `B08::T2.SHARED_ASSEMBLY` @ (-9.625, -25.981, 0.488), rotZ -1.13 rad
- 12MZ 语义组 189 网格带全部附件（油位计/吸湿器/瓦斯/分接开关/风扇/在线监测…）,
  但**不在场景 769 中**；其对象 matrix_world 即组局部框架（原点在主变中心）。
- 两框架同手性（套管均在 y- 侧、风扇 y+ 侧、油枕居中偏 y+)，但比例不同：
  - 12MZ 主油箱 x±3.40 / y±1.20 / z 0.45–3.45
  - B08 油箱壳 x±4.50 / y±1.58 / z 0.16–3.63
- 对齐方式：**逐轴仿射**（以主油箱为基准）,x ×1.3235,y ×1.3167,
  z' = 0.16 + (z-0.45) × 1.1567;XY 缩放几乎各向同性，附件相对箱壁的相对位置得以保持。

## 并入范围（19 个部件）

含：conservator_level, breather, buchholz, pressure_relief, sudden_pressure,
oil_flow_relay, gauges, bushing_oil_gauge, bushing_test_tap, fans, cooling_control,
tapchanger_mech, tapchanger_conservator, tapchanger_breather, tapchanger_filter,
nameplate, cabinet_louvers（共 17 个巡检部件）+ 见 plan_D41.json。

排除（B08 已有，避免重复）: tank, conservator, radiators, hv_bushings, lv_bushings,
fire_spray, foundation; monitor_online 与 smart_terminal 亦排除——B08 已有
`B08::accessory.monitor`（监测柜）与 `B08::accessory.smart`（智能柜），摆位不同但为同类设备。

## 结构

- 新母集合 `D41_T_ACCESSORIES_MASTER`：附件对象的关联复制（共享网格，不改源对象）,
  命名 `D41::acc.<part_id>.<short>`,matrix 已烘焙仿射（对齐 B08 母框架）。
- 实例 Empty `D41::T1.ACCESSORIES` / `D41::T2.ACCESSORIES`(collection instance),
  matrix_world 与 B08 T1/T2 实例完全一致。
- 新层集合 `D41_T1T2_INSPECTION_LAYER` 挂入 `D38_FULL_STATION_REVIEW`。

## 产物

- `output/installation_D41/xialin_D41_T_inspection_accessories.blend`
- `output/installation_D41/D41_part_world_locations.json`（部件×巡视点位×T1/T2 世界坐标清单）
- `output/installation_D41/D41_validation.json` + 渲染核查图
