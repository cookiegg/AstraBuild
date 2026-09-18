# B29 续作说明

当前工程 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B29/xialin_B29_strains_jumpers_crosslines.blend`，SHA `33313cca55fbb1d300a10a64d8599e13a3ac2eb1ce8782d26eec0e6ba7f94c5c`。组件 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B29/B29_overhead_components.blend`，SHA `df38df4fb813ff354ba6e0f29cde263dc4d5086df1fd3e5c10df8811014ecdab`。默认599_B29_G220_OUT_Detail_Clean；585全站，587/590/593三排，596/599首跨，602主变与跨场导线；每组有叠图/参考场景。589场景、32818对象。GUI读回dirtyFalse。

## 本轮实际完成

48处两侧耐张安装=24外110单串+6内110单串+12外220双串+6朝主变220单串，共60条串，804盘片刚性实例复用B27_PORCELAIN_DISC_UNIT。110外9片、内13片；220外每双串各16片，内向21片，照片近似。两处220空跨候选剔除，未虚构设备。

42组U跳线=110外24单根+110内6双根+220外12双根，共60根；端点从外侧夹具到B28悬垂下端，源端和旧B28末端微小偏差用短连接件接合。12跨主导线=110六跨、220六跨，共24根，侧端接B29耐张夹具，中央端严格接既有B08引线末端（同B27过渡末端），避免重复原有短过渡。跨线有源弧垂及分裂间距；220主跨间距约7–8厘米，110约16–19厘米，源重建近似。

全部新件在B29_ALL_OVERHEAD，下有三排B29_<row>_OVERHEAD_SITE及B29_MAIN_CROSSYARD_CONDUCTORS。全站将新集合加入B28原集合，原设备无排除。18处裁切支架残件链接只从两个首跨展示集合移除并更新青色代理，220首跨相机转到耐张一侧；模型资产和全站未改。初版.blend1/验证初版保留。

## 核验及限制

最终原生重读保持31379旧对象、569旧场景、706旧集合、340旧材质及5308原站场对象世界变换；两主变共享。84条导线保存后两端误差及24条主跨与已有引线接口均小于2e-5米；804实例刚性，资产回读一致；6组相机覆盖检查。2723以前文件保持。

固定原奇数三角域对照，偶数拟合，空间相关而非独立测量。耐张本体RMS约2.3–3.9厘米；跳线域含原夹具/横支线，单独导线模型表面RMS最大约46厘米，主跨域含尚缺的GIS竖向分支，最大约77厘米；不能把这些域统计谎称导线几何都厘米级。对应主跨/跳线中位表面距离较小，实际X/Z/XY散点诊断图与局部模型已查看。未删残差，未以每项5厘米作为完成条件。

## 继续B30（已开始准备，未建模）

目标仍为室外设备大都建模对齐；下引线/避雷器分支是实际显著缺项，goal保持active。

B29/GIS110_reference.npz、GIS220_reference.npz和CROSS_reference.npz包含从原始01_SOURCE_MESH__registered_clay提取的vertices/faces/frame_to_world，以及每面source_object_index/source_triangle_index，源对象名见B29_source_object_names.json。宏观X横站、Y沿排；F见各plan，勿当worldXYZ。

next_GIS_terminals.json是旧保存设备的66个实际端子：30个110GIS、18个220GIS、18个SA220。110501/502实际根是B15R2::501/502.CORE、母版B15R2_501/502_EQUIPMENT_VARIANT，不要误用被替代B14整机；套管仍共享B12。端子坐标从parent-aware几何求得，不用inactive scene dimensions/matrix_world。B30/SA110_terminal_datums.json另有30个SA110端子。

B30/plan_B30_downleads.py和B30_downlead_plan.json已初拟48组、72根GIS下引线（30个110、18个220）。42组从B29 U跳线下端到对应GIS套管；另外6组从220主跨X约−6.1分接到4801/4802套管。源诊断显示下引线弯曲，且Z约5.4/5.8/7.7/8.0存在避雷器分支；不要将分支混拟入主体。B30拟合代码/图尚须继续检查，尤其G110_OUT_NEG_01源点较少，不能声称已保存建模。SA110/220分支尚未规划。

MCP所有user_prompt逐字“继续后续其他设备处理”。原生Blender5.1.2后台经GUI MCP subprocess启动，LD_LIBRARY_PATH=/data/program/blender-5.1.2-linux-x64/lib，原生PID与shell不同。工具超时不是终止，依日志Blender quit+原生ps确认。GUI执行脚本要__file__。AST抽纯函数，勿import旧builder顶层；expand/object_transform来自B19，含父层和instance_offset。原分辨率看图要view_image(detail='original')再image(...,'original')。未裁图，未用技能/子代理。

发布B29全部产物冻结，CURRENT可更新。后续别修改B29脚本/计划/日志，下一批在B30。
