# B27 续作说明

当前 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B27/xialin_B27_central_strain_insulators.blend`，SHA `3d931d4e25eb93d7e526ea014c4dceba6a684af4669396aad348a9a68b1535df`；资产 `/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B27/B27_central_strain_components.blend`，SHA `06851aa03cbbb001e14eac5f8cd200d9d11e91d1d62f7b94a79060166b1db8ab`。GUI已打开556_B27_Central_Clean，dirtyFalse，31032对象、550场景。新增554–565共12场景：554全站clean、555全站叠图，556–558主变区，559–561仅绝缘子，562–564单相两侧，565盘片母版编辑。B27_review.html三个滑动对照与全站/母版预览，链接与JS检查通过，未做浏览器布局验收。

本轮属于实质推进：实拍0059完整5280×3956显示中央6相位位置各有两侧耐张串，共12串。沿用B26 CENTRAL_reference.npz及原三角身份，宏观F与B20/B25/B26一致。负X侧短串约1.76米，正X侧长串约2.95米；中心线Y线性、Z二次拟合偶数三角，盘片等弧长布置并逐个沿切线旋转。B27_plan.json保存轴线、13/20盘片近似数、.135m半径、6相位Ys、端点和固定奇数比较域。不是制造图纸/铭牌规格，源粗模平滑单片细节。

新母版B27_PORCELAIN_DISC_UNIT含伞裙/底面环槽、金属帽和连接销3个对象；所有198盘片使用该集合的刚性实例。B27_CENTRAL_STRAIN_STRINGS集合包含12串、梁端挂接件、末端轭板/夹具及24段过渡导线。B27_CENTRAL_WITH_TRANSFORMERS仅链接新绝缘子+B26构架墙体+B26旧主变设备展示。站场直接复用B26全部原集合，再加入新集合，没排除任何旧设备。两主变和305/306保持共享母版。

纠正B26续作种子误读：B08 rear_medium引线的X包围盒最大值−26.3不是开放末端。必须读真实最后12顶点圆环中心。当前existing_B08_lead_geometry.json导出24旧引线全顶点，负X侧实际末端约−27.6至−28.0，正X侧约−20.4至−20.7。plan_B27按T1/T2、front_large/rear_medium及相号匹配双引线，从末端轭板各自引出短过渡，不移动旧线。连接段以曲线网格生成，最后16点圆环与旧末端12点圆环读回差最大0.00000243米。双线末端间距约.16米沿用旧引线；真实局部线夹细节仍近似。

validate_B27原生读回：30690旧对象、538旧场景、676旧集合、334旧材质结构保持；全部旧站场对象世界变换保持，198实例无缩放，24连接端点连续，盘片与整组资产连材质/结构回读相同。12固定奇数域RMS约3.0–4.4厘米，之前约.94–1.20米；不删残差。偶奇来自相关重建，不是独立测绘/用户容差。2617旧文件按继承SHA/size/mtime证据保持。B27源照片另有hash记录。GUIaudit验证550场景、未脏和共享关系。

## 下一步

目标仍为“请持续进行变电站建模任务，直到室外设备大都实现建模与对齐。”当前有明显物理缺项，不完成目标。G110_OUT、G110_IN、G220_OUT三排的垂直悬挂串、斜耐张串仍未建；跨场主导线、GIS下引线网络仍缺，B27只是中央短过渡。B25各排reference.npz和_origins.json可继续用，corridor可能截断向外耐张串，必要时从01_SOURCE_MESH__registered_clay扩大X范围提取。源图片0059非常清楚220长垂直串/近水平耐张串以及双引线和下垂跳线；0014、0026、0039可看110。

B25支持/横梁位置与当前几何见CONTINUE_FROM_B26和B25_gantry_plan.json；不再从头建结构。复用B27盘片形状，但各电压类别串数/片数/安装轴需按照片及粗模分别核对。先安装各排悬挂设备，再跟踪实际导线至端点。缺少粗模导线不代表实物没有导线。

最后用照片、粗模和真实保存场景复核大多数室外设备的覆盖，不以153混合台账、内部formal promotion或任意5厘米清零作为目标。未测绘五金、局部小残差、高杆截断顶端可列精修余项，不无限扩展。

## 工具

native Blender5.1.2由MCP后台启动，LD_LIBRARY_PATH=/data/program/blender-5.1.2-linux-x64/lib。每次MCP user_prompt逐字“继续后续其他设备处理”。shell PID namespace不同；超时不算失败，原生ps和日志Blender quit核实终止。GUIexec脚本要显式globals={'__file__':str(p),'__name__':'__main__'}，否则__file__未定义。parent-aware object_transform/expand及instance_offset，禁用未激活场景matrix_world缓存。旧builder只AST提取纯函数，不能import顶层。

看原图完整细节要view_image(detail='original')并image(v.image_url,'original')；仅前者仍会显示缩小图。没有使用图片编辑或裁图，只看原图和绘制数值诊断图。本轮无subagent/skill。所有B27发布文件冻结，CURRENT可变。后续从B27开B28。
