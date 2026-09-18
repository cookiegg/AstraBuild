# D40 金属/瓷件材质批次

**目的**：铁架（构架/桁架/支架）、缆线（导线/跳线/引线）、绝缘子瓷件等按现场照片证据赋 PBR 材质（金属度/粗糙度/基色），解决展示渲染中"灰蒙蒙、无金属感"的问题。**只改材质，不动任何几何/变换/场景结构**。

**基线**：`output/installation_D38/site_D38_fire_gis_fixes.blend`（SHA-256 `ca84352903281ba8ff431ab22f32efe76efa5098061fc45fcb447d73717e7db4`），只读打开，另存为 `output/installation_D40/site_D40_metal_materials.blend`。

**照片证据**（`图像数据/`）：
- DJI_20260804131058_0039_V（VC-A GIS 区）：GIS 母线筒为白漆铝管、构架桁架/立柱为镀锌钢（中灰金属）、悬式绝缘子串深灰褐、支撑/金具镀锌亮灰；
- DJI_20260804131402_0059_V：围墙/土建；
- _DSC3181（主变后部）：散热片白灰、支架腿镀锌灰、消防管红色（已有材质）。

**材质表**（`plan_D40.json` 有完整参数）：

| 材质 | 用途 | 基色 | 金属度 | 粗糙度 |
| --- | --- | --- | --- | --- |
| MTL_STEEL_GALV | 构架/桁架/柱腿/爬梯/支架 (B25/B26/B36 及 .post/.leg/.support 等) | 0.52,0.55,0.58 | 0.90 | 0.42 |
| MTL_CONDUCTOR | 导线/跳线/软连接 (.wire/.braid/bundle/lead 类) | 0.30,0.31,0.33 | 0.90 | 0.55 |
| MTL_ALU_PIPE | 铝管母线筒/端盖 (B20/B21 .shell/ENDCAP/expansion) | 0.82,0.83,0.84 | 0.35 | 0.38 |
| MTL_FITTING | 金具/法兰/线夹 (.cap/.end_flange/.seat/clamp/yoke) | 0.62,0.65,0.68 | 0.95 | 0.30 |
| MTL_PORCELAIN_DARK | 悬式绝缘子盘 (.disc) | 0.28,0.24,0.21 | 0.0 | 0.28 |
| MTL_PORCELAIN_LIGHT | 支柱绝缘件 (insulating_mount/insulator) | 0.72,0.71,0.69 | 0.0 | 0.25 |

**排除**：混凝土基础/防火墙/围墙/地坪（名称含 WALL/FOUNDATION/.FOOT/.GROUND/PLINTH）不改；既有带色设备（消防红、柜体青、母排红/黄/绿等）不改。

**实现要点**：对象级材质槽（`slot.link='OBJECT'`）赋值，不改共享网格数据块的槽内容；无槽对象才在网格上 append（同件共享同材质，安全）。

**验证**：`validate_D40.py`——D38 哈希不变；D40 重读后对象/场景/集合/网格数与 D38 逐项一致；全部对象 matrix_world 逐一比对一致；网格顶点总数一致（几何零改动）；各材质赋值对象数与 plan 一致；整站渲染非空。

**修订记录**：D40.1（已删除）遗漏了实例集合内部的网格——悬式绝缘子盘等部件在站内只有实例 Empty，盘体网格在 MASTER 集合里（`MTL_PORCELAIN_DARK` 赋值 0）。D40.2 起赋值范围改为"审查集合可达对象 + 实例集合递归内容"。
