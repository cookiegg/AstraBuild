# AstraBuild 与老师讨论用提纲 · v0.7

## 一句话定位

> **我们不是在研究“GPT-6 Astra 能不能生成一个 3D 模型”，而是在研究：同一个通用推理智能体能否在持续的 Blender/Python 工程环境中完成多类部件级重建任务，在失败后修改自己的工程假设，并最终把这些任务结果组合成一个可编辑、可验证、可继续挂接巡检语义的工业数字孪生。**

暂定英文标题：

> **AstraBuild: GPT-6 Astra as a Long-Horizon 3D Engineering Agent for Component-Level Substation Reconstruction**

当前先不把 Kimi、专用 3D baseline 或人工 CAD baseline 放进主线。先讨论现有工作本身是否构成一篇成立的论文，再决定最值得补哪一种实验。

---

# 1. 现有数据为什么已经构成“实验”

B01–D41 不是一个最终模型的开发日志，而可以重新理解为：

> **同一个 Astra / Blender-Python harness 在一个共享工程环境中面对的一组异构 Reconstruction Tasks。**

目前可以整理为 12 类任务：

1. 避雷器拟合与留出验证（B01–B05、B18）
2. 围墙与大门（B06）
3. 双主变复杂组件 / 共享总成（B07–B08）
4. 六组 VC-C 电容器重复结构（B09–B10）
5. VC-A GIS / 避雷器 / 母联压变族（B11–B16）
6. VC-B GIS / 出线 / 变体（B17–B19）
7. 母线、下引线、耐张串与连接系统（B20–B30）
8. 主建筑与地坪（B31–B34）
9. CCTV、围栏、母线架、灯、井盖等长尾设施（B35–D37）
10. 人工引导纠错（B36、D38）
11. 几何不变的材质展示对照（D40）
12. 主变巡检附件与部件世界坐标（D41）

这些任务共享上一阶段产生的几何、MASTER、验证器和历史，所以**不能解释成 38 个 IID trial**；但很适合类似机器人 policy technical report 的写法：

> 同一个模型 / 同一套工具环境 / 多种不同任务 / 典型 behavior episode / 最终长期组合演示。

## 1.1 现在能从历史目录直接抽出的“统一方法”

这次重新审计 `photo-first-pilot/installation/` 和 `output/installation_Bxx/` 后，一个重要结论是：**不是每个设备都走完全相同的固定流水线，而是共享一个核心闭环，并按任务启用专用工程算子。**

核心闭环可以写成：

`冻结/准备上一版 → 提取局部注册证据 → inspect/plan → build/refine → clean/overlay/reference 审查 → validate/audit → release + CONTINUE_FROM_Bxx → 下一任务`

按任务出现的专用算子包括：

- measurement / profile / cross-section fitting；
- component / lead preflight；
- route / jumper / downlead fitting；
- coverage audit 驱动遗漏发现；
- collision / interference；
- human-markup registration 与纠错。

所以论文的方法贡献不应只画一个笼统 `agent → Blender → verifier` 框图，而应展示“**canonical core + task-specific operators**”。过程图也应该作为第一类证据：`measurement_profiles.png`、`component_and_lead_preflight.png`、route diagnostics、clean/overlay/reference 三联图、validation JSON、manifest 和 continuation notes 都在记录“为什么这个几何表示被选择/否定/修改”。

核心新图：`fig11_canonical_workflow`。

脚本文件名前缀审计（仅表示工作阶段是否有记录，不是成功率）进一步支持这个判断：`build 36/36`、`validate 36/36`、`prepare 29/36`、`extract 27/36`、`audit 20/36`、`plan 19/36`、`measure 17/36`、`inspect/refine 16/36`。因此 measurement/preflight 不能被画成所有任务的必经步骤。

## 1.2 方法不要先讲抽象图：先用 B32 完整跑一遍

B32 是现在最适合给老师解释“**Astra 到底在做什么**”的 worked example。必须把智能体角色和确定性程序分开：

- **输入**：冻结的 B31 整站工程/manifest/hash、`B31_vertical_samples.npz`、注册土建参考、现场照片（例如 DSC3140）；
- **Astra/Codex 的可观察作用**：选择任务证据和表示、编写/修改 measurement 与 Blender 程序、根据 diagnostic/review/validator 结果修改下一版；
- **确定性程序**：SciPy 做矩形拟合，Matplotlib 画 façade/step diagnostics，Blender 真正创建 MASTER/SITE、渲染固定机位，validator 重新计算几何/历史保持；
- **输出**：`B32_container_measurements.json`、`C110/C220_facade_diagnostic.png`、`B32_source_steps_diagnostic.png`、station/component `.blend`、8×Clean/Overlay/Reference、`B32_review.html`、validation、manifest、continuation。

最值得展示的是 R1→R2→R3：R1 两舱各一扇门且 C110 侧别错误；R2 把 C110 改到东侧；R3 根据低高度粗模台阶和照片，把 C110 定为东侧 Y≈−3.90，并把 C220 改成西侧两扇门 Y≈−5.50/+5.32。这里可以直接说明：**中间证据改变了建模表示，而不是只产生了一张“过程图”。**

`B32_review.html` 本身就是实验方法的一部分：8 个方向、模型/叠图/仅粗模三种状态和滑块比较，25 张内嵌图片。网站应该直接嵌入这个历史 review，而不是只截取其中一张图。

进一步审计后可以把这个逻辑推广到整个任务集：正式 publication dossier 中有 **32 个批次（B07–D38）保存了原始 `review.html`**。B07 可拖动旧/新主变对照，B08 可切 T1/T2，B09/B10 可逐 031–036 设备组切换 `Clean / Compare / Overlay / Reference`，后续 GIS、导线、土建也沿用相同的同机位模型/粗模审查思想。网站现在应把这 32 个原始 review 作为核心 gallery，而不是只做二次整理后的 case card。

静态论文中用 Figure 13 选 B07/B08/B09/B17 的 `Clean / Overlay / Reference` 代表例；网页则直接让老师打开全部原始 review。这比只展示最终 render 更能说明“每一个设备就是一个 case study”。

证据边界也要主动说明：旧 batch 没有保存 Astra 的内部 chain-of-thought，所以论文描述的是**可观察的 engineering decision trace**，不是事后编写模型内心独白。

---

# 2. 论文建议用三层证据结构

## A. Breadth — 任务广度

回答：**同一个智能体到底做过哪些不同类型的工程任务？**

现有任务覆盖的代表规模：

- 48 只避雷器主体；
- 8+3 套 GIS 间隔；
- 双主变；
- 6 组电容器；
- 约 88.8 m 母线；
- 804 个耐张绝缘子盘；
- 约 10,182 m² 地坪；
- 主建筑 946 部件；
- 最终 D38.2/D40 等价层：37,153 objects / 755 scenes / 858 collections / 3,916 mesh datablocks。

核心图：`fig09_task_suite_composition` 左侧 task suite。

## B. Depth — 失败后智能体会不会改变做法

正文建议重点讲 7 个 episode：

**B01→B02 — 修改度量协议**  
软件 QA 通过但留出几何失败；失败被保留，随后重新定义 fitting / holdout domain。

**B08 — 从单设备提升为共享抽象**  
用户明确确认两台主变可视为同构后，建立 `MASTER → T1/T2 instance`。

**B15 — 拆掉错误抽象**  
邻台污染 + 共享 bus spool 过度泛化，最终同时修改测量方式和 MASTER/site 边界。

**B23 — 过程证据改变几何表示**  
旧 preflight 隐含直线连接假设，但 measurement/profile 显示约半米中段弯曲；随后改为曲线路径并经历 r1/r2/r3 接触与连接修正。这个 case 最适合说明 profile/preflight 不是“报告附图”，而是在改变模型表示。

**B25/B26 — 改变“下一步建什么”**  
从“台账还缺什么”转成“粗模哪些高区仍未被模型解释”；选定 >1m gap 从 78.8% 降至 14.6%。

**B36 — 人只指出遗漏，智能体完成后续工程**  
历史审计 → 构建 → 非有限路径失败 → 修正 → 消防管避让 0.16 m。

**D38 — 最完整的人机纠错闭环**  
红框 → 图像配准 → 世界坐标 → 错误对象 quarantine → GIS/消防设施补建 → D38.1 朝向语义错误 → D38.2 修正。

## C. Scale — 最终整站长期组合能力

回答：**这些 task 的结果是不是只是一堆互不相关的 demo？**

核心证据：

- 38 core reconstruction batches；
- 54 build scripts / 58 validate scripts；
- 150 manifests / 71 validation JSON；
- 109 reference NPZ；
- 2,859+ protected hashes；
- 37,153 objects / 3,916 mesh datablocks，描述性复用比约 9.5×；
- 不同 task 的设备资产、站点实例、导线连接、历史和审查场景能长期共存；
- 后期还能继续做 D41 inspection-semantic augmentation。

**这一层是论文区别于“LLM 生成若干 Blender demo”的关键。**

---

# 3. 老师讨论时建议先展示什么

建议控制在 10–15 分钟内，按下面顺序：

1. **一句话 research question**
2. **Visual Abstract：现场证据 → Astra → 多设备 → 整站**
3. **B32 worked example（Figure 12）**：按输入 → 测量 → door/stair 诊断 → R1/R2/R3 → Blender build → B32_review → validation 讲清一次真实任务
4. **直接打开原始 B32_review.html**，让老师拖滑块看粗模 / clean / overlay
5. **再抽象 Canonical Workflow（Figure 11）**，此时 task-specific operators 才有直觉含义
6. Task Suite 表快速说明 12 类任务，并用 dossier 展示 B15/B23/B29 等其他过程证据
7. 选 3–4 个行为 episode 深讲：建议 B01、B15/B23、B25/B26、D38
6. 整站逐步装配视频 + 37k-object integration
7. D41 inspection semantics
8. 最后一页只放“现有限制 + 请老师判断下一步最值得补什么实验”

---

# 4. 希望老师重点判断的问题

### 问题 1：核心 claim 是否成立？

建议：

> **General-purpose reasoning model as a persistent 3D engineering agent across heterogeneous reconstruction tasks.**

而不是：

- 全自动重建；
- 3.6 cm 测绘精度；
- Astra 优于所有 3D 模型。

### 问题 2：Task Suite + Case Study + System Integration 是否可以作为主要实验结构？

即不强求所有设备统一成一个 success rate，而是：

`task breadth → task-native evidence → representative behavior episodes → system-level integration`

### 问题 3：更适合投哪个研究方向？

- **Agent / general-purpose model**：强调 task breadth、tool use、failure recovery、long-horizon state；
- **3D reconstruction**：可能需要独立几何 GT 和传统/专用 baseline；
- **Digital twin / industrial systems**：强调 componentization、复用、可维护性、语义和巡检价值。

### 问题 4：下一轮最值得补哪一种 controlled experiment？

等定位确定后再选：

- 第二个通用模型；
- no-image / no-coarse ablation；
- 独立 LiDAR / 全站仪真值；
- 第二座变电站；
- 专业人工 CAD 时间/质量基线。

### 问题 5：标题是否应该直接写 GPT-6 Astra？

优点：研究对象非常明确。  
风险：旧 batch 没有冻结模型 provenance，目前只能标为项目负责人确认。

更保守的标题候选：

> **AstraBuild: Evidence-Grounded Long-Horizon Agentic Reconstruction of Component-Level Industrial Digital Twins**

---

# 5. 必须坚持的证据边界

- `3.6 cm` = 对同一 photogrammetric coarse mesh 的 median residual，**不是独立测绘精度**；
- `149 / 101` = 5 cm validation screen，通过/未通过项，**不是模型准确率**；
- `78.8% → 14.6%` = selected high-region coverage gap，**不是全站完成率**；
- `9.5×` = object / mesh-datablock 描述性复用比，**不是建模效率提升 9.5×**；
- human review 是方法组成部分，论文应使用 **agent-driven / human-steerable**；
- D38.2 / D40 / D41 必须分别描述；
- 当前没有 matched baseline，因此不能做“Astra 相对其他模型更强”的因果结论。

---

# 6. 当前版本文件

- 正文：`paper/paper_teacher_discussion.md`
- 老师讨论提纲：`paper/teacher_discussion_notes_zh.md`
- 网站：`website/index.html`
- 新核心图：`figures/fig09_task_suite_composition.{svg,pdf,png}`
- 方法总图：`figures/fig01_agentic_loop.*`
- D38 episode：`figures/fig06_d38_human_feedback.*`
- D41 语义图：`figures/fig07_d41_inspection_semantics.*`

当前建议先用这套材料和老师讨论论文定位，再决定下一轮实验。