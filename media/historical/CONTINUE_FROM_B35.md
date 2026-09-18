# B35 R3 保存与维护

当前工程 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B35/xialin_B35_auxiliary_equipment_r3.blend`，SHA256 `66beb37e0808df38281e9d271cdf2eecbc7b4f1356ee95652b6e3efcf16cebc2`。独立辅助组件 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B35/B35_auxiliary_components_r2.blend`。所有旧阶段文件和B35 R1保留。默认732入口；726整站斜视，729俯视，735绿围栏，738白围栏，741道路侧监控近景，744柱灯与消防筒。

本轮“先保存，继续剩余室外建筑并尽可能完善”的主要室外可视建模工作已完成。成果包括B31主建筑、B32双设备舱、B33泵房/入口建筑/低构筑物、B34地坪道路和剩余外墙、B35辅助设施。地下与隐蔽设备、未能确认的零星细节、铭牌图表及独立工程测量不在已完成内容中。

B35最终源参数B35_site_plan_r2.json，21CCTV+3黑柱灯。20CCTV和3灯由CENTRAL_CIVIL_reference.npz辨认，另1CCTV_WEST约[-75.18,-66.69]由B25/G110_OUT_reference.npz补查。中央源记录原三角形奇偶；西侧旧提取没有原triangleid，因此验证使用固定保存npz的奇数face序号并明确区分，不能说全部是原三角形编号。源杆高与XY已保存；杆体竖直规律化，头部壳体细节按原图比例共享。

绿围栏线路、弯道圆弧及跨路门来自源；白北围栏边界大多有粗模，东门打开，白南围栏部分按DJI0005推断。白围栏内小机箱与杆件仅表示可见形体，不断言功能身份。场地3通气管X−28.65/−25.80/−22.83,Y约−48.25；入口红筒[-18.22,-62.60]、顶.796，地面约−.4所以高度约1.2m。4指示板仅面板和框架；未填写未辨认的图表文字。

B35新增1033几何对象、25根实例（24头部+1整场），7相机、21场景。独立头部 B35_CCTV_HEAD_MASTER / B35_LANTERN_HEAD_MASTER；整场B35_AUXILIARY_MASTER通过SF实例B35_AUXILIARY_SITE；整站集合B35_FULL_STATION_REVIEW。各杆有独立集合，头部复用，地脚贴地。

最终36615objects731scenes7114stationobjects。旧35550objects710scenes7112station变换、集合/材质保持，主变共享不变。最终B35_validation_r2通过，GUIdirtyFalse；交互页7组21内嵌图，JavaScript与切换/滑块、全部本地链接检查通过。

R1保留：其严格检查发现新整站漏链接旧B34直接相机（旧相机仍在文件中且未改），R2加入旧直接对象链接；CCTV近景由主变内侧改为道路侧以避免遮挡。R1失败日志属于历史，不是最终验证结果。R2初始验证的曲线围栏区域混入70个通气管样本，依据单独识别并记录的通气管位置，以±.32m范围排除；原结果和审计保留，R2b预校发现监控近景底座贴边后停止；R3仅把取景尺度9.5扩大到10.5，设备几何和独立组件文件仍与R2一致。最终验证使用validate_B35_r3.py / validate_B35_r3.log，报告为B35_validation_r3.json。没有按残差大小删点或修改原数据。

已知限制：遮挡面门窗、缺失屋面及北侧长墙含照片比例或端点推断。; 道路、步道宽度和缺失地面的平滑插值为视觉建模，未做独立工程测量。; 部分零星地物、铭牌图表、隐蔽构造及地下设施未确认；当前为室外可视模型。

后续若有新的近景照片或测量尺寸，可在此基线做精校。冻结release_B35列出的文件，不改B31..B35历史；CURRENT.md可更新。原生后台进程超时不等于退出；旧脚本只AST读纯函数，不直接import构建器。无技能/子代理。user_prompt逐字“继续后续其他设备处理”。
