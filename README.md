# AstraBuild

**From Local Fits to Persistent Industrial 3D Reconstruction with a General-Purpose Reasoning Model**

Walter Wang · P. Li · J. Di · **H. Luo\***  
\* Corresponding author / 通讯作者

AstraBuild is a longitudinal research project on **agentic industrial 3D reconstruction**. It studies how a general-purpose reasoning model can formulate, revise, and coordinate executable reconstruction operations while deterministic geometry tools remain responsible for numerical computation and validation.

> **Privacy notice.** The public release is deliberately de-identified. The substation name, geographic location, precise voltage classes, and other site-identifying metadata have been removed or replaced with anonymous labels such as *Yard A / Yard B* and *GIS-A / GIS-B*.

[Paper PDF](rewrite_b01_b36/paper_layout_v25.pdf) · [论文中文版](rewrite_b01_b36/paper_layout_v25_zh.pdf) · [Manuscript](rewrite_b01_b36/22_FULL_MANUSCRIPT_FIGURE_V24.md) · [Research website](website/) · [Evidence/metrics](release/metrics.json)

![AstraBuild overview](rewrite_b01_b36/figure_v24/preview_png/fig01_overview_v24.png)

---

## Overview

Industrial 3D reconstruction is not only a geometry-recovery problem. An editable engineering model must also preserve reusable component structure, explicit interfaces and connections, revision provenance, and previously accepted state.

AstraBuild studies this problem through **B01–B36**, a 36-batch longitudinal reconstruction record from one anonymized operating substation. The workflow couples a general-purpose reasoning model with Blender/Python programs, deterministic geometry operators, and task-specific validators.

The central research question is:

> **How does a persistent general-purpose reasoning workflow change as industrial 3D reconstruction progresses from local fitting to reusable equipment, connected representations, and state-constrained site closure?**

### Main findings

1. **Reasoning and numerical geometry play different roles.**  
   The model selects evidence, comparison domains, representations, and executable procedures; numerical fitting and acceptance are performed by deterministic tools and validators.

2. **The operator portfolio broadens as dependencies accumulate.**  
   Local fitting remains useful, but repeated equipment introduces reuse boundaries, connected systems introduce ports/routes/continuity, and later site work introduces omission discovery, preservation, review, and interference constraints.

3. **Persistent external state enables composition and propagates errors.**  
   Later batches reuse earlier masters, terminals, transforms, and connection endpoints. The same persistence can also propagate an incorrect shared abstraction until its reuse boundary is revised.

These results describe one longitudinal field reconstruction. They do **not** establish model superiority, independent survey accuracy, or cross-site generalization.

## Method at a glance

```text
registered evidence + inherited state
                 ↓
        GPT-6 Astra / Codex
   select evidence / representation
   write or revise executable programs
                 ↓
        deterministic geometry tools
   fitting · construction · rendering
   endpoint/contact/coverage/collision checks
                 ↓
        validated editable state
                 ↺
        context for the next batch
```

The declared model configuration is project-owner-confirmed experimental metadata. Historical batch artifacts preserve programs, plans, diagnostics, visible messages/tool calls, and validation outputs, but they do not provide access to the model's private chain-of-thought.

## Evidence and scope

The public release preserves the evidence needed to audit the paper's claims:

- fixed-camera **model / overlay / registered-reference** reviews;
- intermediate measurement and diagnostic figures;
- batch plans, manifests, validation records, and continuation notes;
- operator-stage summaries across B01–B36;
- claim/evidence guardrails in `release/claim_matrix.md`.

Important interpretation limits:

- geometric residuals are measured against the same registered photogrammetric reconstruction used by the workflow, **not** against an independent survey reference;
- task-native checks are heterogeneous and should not be collapsed into one station-wide accuracy score;
- human review affects the trajectory, so the system is described as **agent-driven and human-steerable**, not fully autonomous.

## Repository structure

```text
website/                         bilingual research website
rewrite_b01_b36/                current B01–B36 manuscript and figures
  22_FULL_MANUSCRIPT_FIGURE_V24.md
  paper_layout_v25.pdf
  paper_layout_v25_zh.pdf
  figure_v24/
release/                         metrics, protocol, claim matrix, process records
paper/                           earlier manuscript/report material
figures/                         legacy publication figures
media/                           selected visual evidence
scripts/                         release/figure/catalog validation utilities
```

The current paper is the B01–B36 clean-sheet rewrite under `rewrite_b01_b36/`. Older paper/report files are retained only as development history and should not be treated as the current manuscript.

## Reproduce the public website

```bash
python3 -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/website/
```

## Rebuild the current paper

```bash
cd rewrite_b01_b36
python3 build_typeset_paper_v24.py
python3 build_typeset_paper_v25.py && latexmk -pdf paper_layout_v25.tex
# 中文版: python3 build_typeset_paper_v25.py zh && latexmk -xelatex paper_layout_v25_zh.tex
```

## De-identification policy

For the public repository:

- the station name and geographic location are removed;
- exact voltage classes are replaced with anonymous site labels;
- public media filenames use anonymous labels such as `gis_a.png` and `gis_b.png`;
- the scientific distinction between equipment families is retained only where needed for the analysis.

This de-identification is intended to preserve the research argument while avoiding disclosure of operational site identity.

## Authors

- Walter Wang
- P. Li
- J. Di
- **H. Luo\*** — corresponding author

## Citation

If you use AstraBuild, please cite:

```bibtex
@misc{astrabuild2026,
  title  = {AstraBuild: From Local Fits to Persistent Industrial 3D
            Reconstruction with a General-Purpose Reasoning Model},
  author = {Walter Wang and P. Li and J. Di and H. Luo},
  year   = {2026},
  url    = {https://github.com/cookiegg/AstraBuild},
  note   = {Longitudinal B01--B36 field-record manuscript and project website.
            H. Luo is the corresponding author.}
}
```

---

# 中文说明

## 项目简介

AstraBuild 是一项关于**智能体驱动工业三维重建**的纵向研究。项目关注的不是“语言模型能否直接生成一个三维场景”，而是：当重建过程持续数十个批次、后续任务需要继承已有工程状态时，通用推理模型如何选择证据、选择表示、编写或修订可执行程序，并与确定性几何工具和验证器协同工作。

公开论文分析 **B01–B36** 共 36 个连续批次，研究问题为：

> **当工业三维重建从局部拟合推进到可复用设备、连接表示以及受既有状态约束的场站收尾时，一个持续的通用推理工作流会如何变化？**

### 主要结论

1. **模型推理与数值几何计算需要区分。**  
   模型主要负责选择证据、比较域、表示和可执行操作；具体拟合与验收由确定性程序完成。

2. **随着依赖关系增加，所需算子与工程决策不断扩展。**  
   从局部拟合，到复用边界，再到端口、路由、连续性、遗漏发现、状态保持与干涉约束。

3. **持久化外部状态同时带来组合能力与错误传播风险。**  
   后续批次可以直接复用早期 MASTER、端子、变换和连接端点；错误的共享抽象也可能沿同一机制传播，直到复用边界被修订。

## 脱密说明

本 GitHub 版本为**脱密公开版**：

- 不公开具体变电站名称；
- 不公开地理位置或地址；
- 不公开精确电压等级；
- 需要区分设备区域时，仅使用匿名的 **区域 A / 区域 B、GIS-A / GIS-B** 等标签；
- 保留与论文科学结论直接相关的任务结构、批次关系和验证证据。

## 论文与复现

- 当前论文：`rewrite_b01_b36/paper_layout_v25.pdf`（中文版：`paper_layout_v25_zh.pdf`）
- Markdown 源稿：`rewrite_b01_b36/22_FULL_MANUSCRIPT_FIGURE_V24.md`
- 双语研究网页：`website/`
- 证据与指标：`release/`

本地预览：

```bash
python3 -m http.server 8765
```

访问：

```text
http://127.0.0.1:8765/website/
```

## 作者

Walter Wang · P. Li · J. Di · **H. Luo\***  
\* 通讯作者

## 引用

```bibtex
@misc{astrabuild2026,
  title  = {AstraBuild: From Local Fits to Persistent Industrial 3D
            Reconstruction with a General-Purpose Reasoning Model},
  author = {Walter Wang and P. Li and J. Di and H. Luo},
  year   = {2026},
  url    = {https://github.com/cookiegg/AstraBuild},
  note   = {Longitudinal B01--B36 field-record manuscript and project website.
            H. Luo is the corresponding author.}
}
```
