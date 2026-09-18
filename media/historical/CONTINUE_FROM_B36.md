# B36 R3 主变母线架补建

已补齐两台主变与房屋之间遗漏的低位母线支架及可见外部连接。主变 1 为侧向转弯，主变 2 为直行；两台主变本体仍共享原 B08 组件，没有改动。

新增 5 根母线架钢柱、33 个短支柱绝缘子、6 组房屋侧立式器件及支柱、6 个穿墙套管、6 条连续主连接排，以及基础、柱脚加劲板、纵横梁和接续附件。四类主要部件均使用同一组件库中的共享集合。

工程：`/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B36/site_B36_transformer_bus_racks_r3.blend`。SHA-256：`b6bbc3caeffdf72ca52df2dd5e01234269fe652827131e64f1f8a1da7ef502e8`。

组件库：`/data/proj/xunjian-copilot/experiments/blender-substation/photo-first-pilot/output/installation_B36/B36_bus_rack_components_r3.blend`。SHA-256：`f7a4065277b49b0ede055eeefbd28ce853c896ebe951b761d75816bd5a791c8d`。

默认场景 753 为主变 1 安装位置；747/750 为两个独立母线架，748/751 叠加粗模，755/756 为俯视，758 为穿墙接口，757 为整站。

## 验证

重读工程和独立组件库通过。原 36615 个对象、731 个场景及 7114 个整站对象变换保持。新几何均为有限坐标；11 处基础落地和柱脚接触、5 处柱顶承梁、33 处绝缘子承托、6 条主连接排两端接续已检查。

同一粗模中固定部件区域的奇数原始三角形用于回查：柱轴表面 RMS 范围 0.0021–0.0327 m，短绝缘子表面 RMS 范围 0.0054–0.0411 m。这是粗模一致性检查，不是独立测量精度。

## 依据与边界

原照片 DSC3172、3174、3176、3179、3180；两组局部参考位于本目录 `T1_BUS_RACK_reference.npz`、`T2_BUS_RACK_reference.npz`，保留原始三角形索引与坐标框架。`B36_bus_rack_plan_r3.json` 记录柱脚、绝缘子、转弯和端点。

房屋側外形按照片处理，未创建不可见墙内走线。没有填写不清楚的电气型号或相别铭牌。瓷裙、螺栓和小夹具细节近似。

首个失败草稿保留于 `draft_failed_vertical_frame`，含非有限路径截面，不可使用。首次有效草稿保留原文件名；R2 改进了竖直连接排的截面方向，减少扭转。R3 将红色进线局部外移最多 0.16 m，避让旧消防支管；两端接点与支架落点不变。最终版主连接排相互及与既有主变外部构件的表面穿插检查通过。最终以 R3 工程及 `B36_validation_r3.json` 为准。

后续仍需补 GIS 矮杆投光灯、局部井盖/沟盖板和白色标识桩；本轮未宣称全站小设施全部完成。

维护：冻结 B35 及更早版本。后续从 B36 R3 另存；CURRENT.md 可更新。原生后台脚本完成以日志结束与输出校验为准；MCP user_prompt 使用最新用户原话。
