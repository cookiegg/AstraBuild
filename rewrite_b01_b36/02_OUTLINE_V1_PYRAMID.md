# Outline v1 — reader-first / pyramid structure

## Purpose of this version

This outline replaces the material-first structure in `01_OUTLINE_V0.md` with a reader-first argument hierarchy. The paper should be readable as an argument even if the reader never opens the batch folders, review pages, manifests, or website.

Evidence boundary remains **B01–B36 only**.

The four longitudinal regimes remain useful for analysis, but they are no longer the top-level paper structure. They are evidence used to support the main argument.

---

# 0. Writing architecture

## 0.1 Pyramid principle

The paper should have one answer at the top, three supporting claims beneath it, and concrete batch evidence beneath those claims.

### Top-level answer

> **A general-purpose reasoning model can operate a persistent industrial 3D reconstruction process across heterogeneous tasks when it is coupled to executable geometry tools and task-specific validation. Its useful role changes as task structure becomes richer: from defining local measurement problems, to managing reusable abstractions and connected representations, to maintaining a large accumulated engineering state.**

This is the paper's answer. The rest of the manuscript should justify it.

### Three supporting claims

**Claim A — Breadth under one interface.**  
A common evidence → program → validate interface supports heterogeneous reconstruction tasks, from local fitting to equipment assemblies, conductors, civil structures, and auxiliary infrastructure.

**Claim B — Increasing structural complexity changes what the agent must decide.**  
As tasks move from isolated geometry to repeated equipment and connected systems, success depends less on fitting parameters and more on choosing abstractions, representations, topology, routing, and task-specific operators.

**Claim C — Persistent state enables composition, but also makes mistakes consequential.**  
Later tasks can build on earlier accepted geometry, shared assets, transforms, and validators; the same persistence can propagate a wrong abstraction, so provenance and validation are part of the engineering method.

These three claims are the main paper. Everything else is method, evidence, qualification, or appendix.

---

## 0.2 SCQA for the Introduction

### Situation

Photogrammetry and related reconstruction methods provide registered scene geometry and appearance.

### Complication

An engineering digital model needs more than a surface: explicit components, reusable families, site-specific connections, topology, editable structure, and a state that can survive later revisions. A single fixed reconstruction operator is unlikely to cover arresters, transformer assemblies, GIS, flexible conductors, buildings, and site closure equally well.

### Question

> Can one general-purpose reasoning model coordinate a persistent reconstruction process across these heterogeneous tasks, and how does its role change as the engineering structure becomes more complex?

### Answer

> Yes, in this B01–B36 record, the same model/tool interface spans the full reconstruction sequence, but the computational burden changes. Early tasks are mainly local measurement problems; repeated equipment requires reusable abstractions; connected systems require topology and path reasoning; late tasks require maintenance of accumulated state. Numerical geometry is delegated to deterministic operators, while the model primarily structures the engineering problem and chooses or revises the programmatic operation.

The Introduction should reach this answer quickly. It should not make the reader wait until Discussion to learn what the paper found.

---

# 1. Title

## Preferred working title

**AstraBuild: From Local Geometry Fits to Persistent Industrial 3D Reconstruction with a General-Purpose Reasoning Model**

Why this title works:

- names the actual progression studied;
- does not overclaim autonomy;
- does not make GPT-6 branding the scientific contribution;
- does not reduce the work to the final station artifact;
- remains compatible with the three-claim pyramid above.

Possible shorter alternative:

**AstraBuild: A General-Purpose Reasoning Agent for Persistent Industrial 3D Reconstruction**

---

# 2. Abstract

## Reader function

A reader should understand the problem, the answer, the evidence, and the boundary in approximately 180–220 words.

## Structure

### Sentence group 1 — problem and gap

Surface reconstruction does not directly provide editable component structure, reuse, connectivity, or revision history required for engineering models.

### Sentence group 2 — question and study design

Study one GPT-6 Astra/Codex workflow over B01–B36 of an operating 220 kV substation, using registered photogrammetric geometry, field imagery, engineering records, executable Blender/Python tools, and batch-specific validators.

### Sentence group 3 — main answer, in the same three-part structure as the paper

1. One common agent/tool interface spans heterogeneous reconstruction families.
2. The agent's decisions change with task structure: local fitting → reusable abstraction → connected paths/topology → accumulated-state maintenance.
3. Persistent state enables later tasks to compose previous results, but also propagates wrong abstractions unless checked.

### Sentence group 4 — concrete evidence

Use only 2–3 concrete facts, for example:

- B01–B36 cover 36 sequential batches across nine broad catalog families;
- B23 changes from a straight lead to a curved path after profile evidence reveals approximately 0.5 m mid-span bow;
- B36 validation preserves 36,615 previous objects and 2,798 protected files while extending a 36,812-object state.

Do not put every metric into the abstract.

### Sentence group 5 — boundary

Single site; no matched model baseline; no independent survey reference; human review remains part of the workflow.

## Forbidden abstract content

- D37/D38/D40/D41;
- counts of builders/manifests/JSON files;
- a long sequence of batch examples;
- 37,153-object D38/D40 scale;
- overall success-rate language;
- claims of autonomous or survey-grade reconstruction.

---

# 3. Introduction

Target length: ~1.2–1.5 pages.

## 3.1 From reconstructed surfaces to engineering models

### Reader question

Why is this a research problem rather than a Blender automation project?

### Main point

Physical reconstruction and engineering reconstruction have different outputs.

### Develop only the minimum necessary distinctions

A usable engineering representation requires:

- component identity and hierarchy;
- repeated equipment represented by reusable structure;
- finite site-specific connections;
- topology / continuity for conductor systems;
- editable persistent state;
- validation appropriate to the represented geometry.

Do not enumerate the full dataset here.

## 3.2 Why a general-purpose reasoning model is relevant

### Reader question

Why use a reasoning model at all?

### Main point

The challenge is not one numerical algorithm. Different tasks require different evidence selections, representations, decompositions, and executable operators.

The model is potentially useful as the layer that specifies and revises these engineering operations; deterministic geometry code remains responsible for numerical computation.

## 3.3 Research question and answer preview

State one primary question:

> **Can one general-purpose reasoning model coordinate a persistent industrial 3D reconstruction process across heterogeneous tasks, and how does its role change as the structure of the reconstruction problem becomes richer?**

Then preview the answer with the same three claims A/B/C.

## 3.4 Contributions

Exactly three contributions:

1. **Persistent agentic reconstruction formulation.** A general-purpose model operates over registered physical evidence through executable geometry programs, task-specific validation, and inherited engineering state.
2. **B01–B36 longitudinal field record.** Thirty-six sequential batches cover the progression from local fits to reusable equipment, connected systems, civil/auxiliary closure, and a large accumulated station state.
3. **Cross-task structural analysis.** The record shows how the model's useful decisions shift from defining measurement problems toward managing abstractions, connected representations, operator choice, and accumulated state as task structure becomes richer.

Do not list failure recovery, website review pages, object count, semantic augmentation, or human correction as separate contributions.

---

# 4. Related Work

Target length: ~0.8–1.0 page.

The section should be argumentative and end with the gap. It should not become a literature catalog.

## 4.1 Structured 3D / CAD reverse engineering

Use Point2CAD / CAD-Recode and adjacent work.

Function:

> establish that moving from sampled geometry to structured editable representations is itself a reconstruction problem.

Gap:

> these works usually solve a fixed object-scale mapping rather than a heterogeneous, persistent site sequence.

## 4.2 LLM-based 3D program generation

Use 3D-GPT / SceneCraft.

Function:

> establish that language models can reason through procedural 3D representations and executable Blender programs.

Gap:

> those works primarily synthesize from language or scene specifications; AstraBuild reconstructs a registered physical site and must maintain metric consistency and inherited state.

## 4.3 Long-horizon tool-using agents

Use Voyager / GPT-Policy as conceptual precedents.

Function:

> motivate executable actions, feedback, reusable state, and long-horizon accumulation.

Do not turn the paper into a robotics analogy.

## Closing gap paragraph

One paragraph only:

> Existing work separately addresses structured reverse engineering, programmatic 3D generation, and long-horizon tool use. B01–B36 provides a field record where all three requirements interact: a general-purpose model repeatedly converts registered physical evidence into executable reconstruction programs while inheriting and modifying a growing engineering state.

---

# 5. AstraBuild Method

Target length: ~1.5 pages maximum.

The Method should explain enough to understand the Results. It must not become a second Results section.

## 5.1 Evidence and target state

Inputs:

- registered photogrammetric geometry;
- UAV / ground imagery;
- engineering / inventory records when relevant;
- accepted geometry and assets from earlier batches.

Persistent state contains:

- editable Blender scene;
- reusable equipment collections / instances;
- site-specific geometry and connections;
- validation and provenance artifacts.

## 5.2 Division of labor: model vs deterministic tools

This should be the conceptual center of the Method.

### Model decisions

- which evidence and local domain are relevant;
- which geometric representation to use;
- how to decompose the task;
- which measurement / routing / inspection operator to call;
- how to write or revise Blender/Python code;
- how to react to review / validation evidence.

### Deterministic operations

- fitting and optimization;
- coordinate transforms;
- geometry construction / rendering;
- distance / contact / continuity / collision calculations;
- history/hash checks.

Key sentence:

> A small geometric residual is therefore evidence that the workflow formulated and executed a valid measurement procedure, not evidence that the language model itself performed high-precision numerical optimization.

## 5.3 Persistent reconstruction loop

One simple diagram:

`physical evidence + previous state → model decision → executable operator → validation → accepted / revised state`

No detailed filesystem hierarchy in the main paper.

## 5.4 One short worked example

Use **B23**, not B32, because B23 directly illustrates the distinction between model representation choice and deterministic geometry fitting:

straight connection assumption → profile evidence shows ≈0.5 m bow → curved path representation → revised geometry + validation.

Keep to approximately half a page. The purpose is to make the interface concrete before Results.

---

# 6. Evaluation Design

Target length: ~1 page.

This section should positively state what is evaluated. Avoid headings framed as defenses such as “Why this is not an IID benchmark.”

## 6.1 Reconstruction sequence

State simply:

- B01–B36 are sequential;
- later tasks inherit accepted earlier state;
- the targets evolve from isolated local structures to interconnected and residual site structures;
- task-native validation is used because geometry classes differ.

A single sentence can note that results are therefore analyzed by task structure rather than collapsed into one global success rate.

## 6.2 Task spectrum

Use one compact table, not 36 entries.

Recommended rows:

| Task group | Representative batches | What is reconstructed | Structural challenge |
|---|---|---|---|
| Local fitted geometry | B01–B06 | arresters, wall, gate | define local comparison / fit domain |
| Repeated equipment | B07–B19 | transformers, capacitors, GIS | reusable structure and variants |
| Connected systems | B20–B30 | busbars, conductors, insulators | endpoints, paths, topology, unexplained occupancy |
| Site closure | B31–B36 | buildings, ground, cabins, auxiliaries | integrate residual structures while preserving prior state |

Important: call these **descriptive groups**, not four formally discovered regimes unless later analysis supports that stronger terminology.

## 6.3 Evidence used in Results

Define only the recurring evidence forms needed later:

- fixed-camera model / reference review;
- local residual / fit checks;
- endpoint / contact / route checks;
- selected-region coverage gap;
- state-preservation counts.

Detailed review pages and batch dossiers belong in supplement / website.

---

# 7. Results

This section mirrors the three supporting claims. This is the main pyramid.

Target length: ~4–5 pages.

# 7.1 Result A — One agent/tool interface spans heterogeneous reconstruction tasks

## Reader question

Does the method work only for one type of geometry, or can the same model/tool interface support qualitatively different reconstruction problems?

## Claim

> The same evidence–program–validation interface is reused across heterogeneous task groups, while the deterministic operators and validation criteria vary with geometry type.

## Evidence

Show task breadth without giving each batch equal narrative weight.

Representative visual cases:

- B06 wall/gate;
- B08 transformer;
- B10 capacitor bank;
- B17 GIS;
- B23 conductor/lead;
- B32 cabin/building.

Use **one 2×3 visual figure** with `Reference / Model / Overlay` style snapshots rather than six mini case studies.

Use a compact quantitative table with selected task-native readouts. The purpose is breadth, not ranking.

## Interpretation

One general-purpose model can operate through a shared reconstruction interface across distinct geometry classes, but there is no single shared geometric solver underneath those tasks.

## What not to claim

- global success rate;
- common accuracy metric;
- model superiority.

---

# 7.2 Result B — Increasing structural complexity changes what the agent must decide

This should be the **longest and most important subsection**.

## Reader question

What changes when reconstruction progresses from isolated objects to reusable equipment and connected systems?

## Claim

> As the engineering structure becomes richer, the critical model decisions move from selecting fit domains and parameters toward choosing abstraction boundaries, representation classes, topology, routes, and task-specific operators.

## Evidence sequence

This is where the four descriptive groups are useful as a progression, but they appear inside one argument.

### Stage 1 — local fitting: B01/B02

- local geometry can be expressed as a fit problem;
- B01/B02 shows the comparison domain itself must be defined correctly;
- deterministic solver handles the numerical fit once the problem is specified.

### Stage 2 — reusable equipment: B08 + B15

- B08: repeated transformer structure motivates a shared master / site-instance abstraction;
- B15: reuse can be overgeneralized; finite geometry must sometimes move back to site-specific scope.

Meaning:

> the decision is now “what is shared?” rather than only “what are the dimensions?”

### Stage 3 — connected systems: B20 + B23 + B25/B26

- B20: connections depend on existing equipment and route structure;
- B23: straight versus curved representation becomes the key decision;
- B25/B26: unexplained occupancy can determine what should be reconstructed next.

Meaning:

> the task is now about topology, representation, and missing structure, not independent object fitting.

### Stage 4 — accumulated-site work: B31/B32/B36

- B31/B32: civil/cabin geometry must be interpreted relative to a large existing model;
- B36: interference and preservation constraints appear while adding remaining bus-rack structures.

Meaning:

> late tasks are constrained by what already exists.

## Main figure

**Operator-evolution figure** should be the central evidence of this subsection.

Preferred design:

- x-axis: B01 → B36;
- grouped visually into the four descriptive stages;
- y-axis: operator families such as fit, measure, plan, inspect, refine, audit, review, collision;
- cells show whether a batch records that operation;
- above the heatmap, a thin band labels the reconstruction target family.

This figure lets the reader see the argument instead of reading a list of stage counts.

## Interpretation

The process does not scale by repeatedly applying one reconstruction primitive. The engineering problem changes, and the model's useful role shifts toward selecting or revising the representation and operator structure.

---

# 7.3 Result C — Persistent state enables station-scale composition and creates propagation risk

## Reader question

Can accepted outputs from earlier tasks remain usable as later tasks are added?

## Claim

> Persistent geometry, reusable assets, transforms, and validation history allow later work to compose over a long horizon, but the same persistence makes incorrect abstractions propagate until explicitly revised.

## Positive evidence

Use B36 as the natural endpoint:

- 36,812 objects;
- 743 scenes;
- 7,116 station objects;
- 36,615 previous objects preserved;
- 7,114 previous station transforms preserved;
- 2,798 protected files unchanged.

These are **state-preservation and scale descriptors**, not reconstruction accuracy.

## Counter-evidence

Use B15:

- a wrong shared abstraction propagates finite geometry to multiple installations;
- persistence makes the mistake consequential;
- revision of the MASTER/site boundary is therefore necessary.

## Interpretation

Persistent state is not just implementation detail. It is both the mechanism that makes site-scale reconstruction possible and a source of system-level risk.

## Figure

One station-scale B36 visual plus a compact inheritance diagram:

`earlier accepted assets → reused / connected / preserved → B36 state`

Do not show another assembly video in the paper.

---

# 8. Discussion

Target length: ~1 page.

Discussion should interpret the three results, not repeat the batch stories.

## 8.1 What the general-purpose model contributes

Main interpretation:

> its strongest role in this record is **problem formulation and orchestration**: selecting evidence, representation, decomposition, reusable boundaries, and executable operators.

Numerical precision remains external.

## 8.2 Why explicit tools and validators matter

The system works because reasoning is externalized into executable programs and inspectable evidence. Plausible model output is not its own acceptance criterion.

Use B01/B15/B23 briefly as examples; no retelling.

## 8.3 Limits of the evidence

Put all defensive statements here, once:

- single site;
- no independent survey ground truth;
- no matched alternative-model / CAD-expert baseline;
- human review influences the trajectory;
- B01–B36 are sequential historical tasks, not controlled repeated trials;
- old logs do not independently freeze model/reasoning provenance.

Do not repeat these caveats throughout Results unless a specific metric requires it.

## 8.4 What a controlled follow-up should test

Prioritize:

1. matched second-model runs on a small representative task subset;
2. independent survey measurements for selected devices;
3. second site;
4. per-task cost / wall-clock / human intervention logging.

---

# 9. Conclusion

Target: one short paragraph.

Structure:

1. Restate the question.
2. State the three answers in compressed form.
3. State the boundary / next experiment.

Possible logical form:

> B01–B36 shows that one reasoning model can operate a persistent 3D reconstruction interface across heterogeneous industrial tasks. The sequence further shows that scaling is not achieved by repeating one geometric primitive: the model's role shifts from framing local measurements to managing reusable abstractions, connected representations, and accumulated engineering state. This supports general-purpose reasoning as an orchestration layer around deterministic geometry tools, while leaving model comparison, survey accuracy, and cross-site generality to controlled follow-up studies.

---

# 10. Figure and table budget

The main paper should be visually sparse enough that every figure advances the argument.

## Figure 1 — The problem and the answer

Reader should understand in <10 seconds:

`registered physical evidence → reasoning model + executable geometry tools → editable component model → persistent station state`

Add three labels under the output side:

`local fit → reusable structure → connected / accumulated system`

No detailed software architecture.

## Figure 2 — B01–B36 study map

A simple chronological strip:

B01 … B36, with task-family color bands and 5–7 representative batch callouts.

Purpose: orient the reader once.

## Figure 3 — Heterogeneous task breadth

2×3 representative review examples from B06, B08, B10, B17, B23, B32.

Purpose: support Result A.

## Figure 4 — Operator evolution across B01–B36

Batch × operator heatmap.

Purpose: support Result B. This should probably become the most important analytical figure in the paper.

## Figure 5 — Representation / abstraction transitions

Three compact examples:

- B01/B02: comparison-domain revision;
- B15: shared-master boundary revision;
- B23: straight → curved path.

Purpose: make Result B concrete without creating a separate “failure case” section.

## Figure 6 — B36 persistent-state endpoint

Station view + inheritance/preservation summary.

Purpose: support Result C.

## Table 1 — Task spectrum

Only four descriptive groups, representative batches, targets, and structural challenge.

## Table 2 — Selected task-native evidence

Maximum 6–8 rows. Each row must have explicit metric scope.

Everything else moves to supplement / website.

---

# 11. Material-to-claim map

This prevents interesting batches from becoming standalone stories.

| Batch / group | Main paper role | Supporting claim |
|---|---|---|
| B01/B02 | local fitting + evaluation-domain definition | B |
| B06 | breadth example for civil geometry | A |
| B08 | reusable equipment abstraction | B |
| B10 | repeated assembly breadth | A |
| B15 | counterexample: abstraction boundary and propagation | B, C |
| B17 | complex GIS breadth | A |
| B20 | transition to connected-system reasoning | B |
| B23 | representation-class change; worked example | B |
| B25/B26 | unexplained geometry / task selection | B |
| B29 | optional additional connected-path evidence | B |
| B31/B32 | accumulated-state civil interpretation | B |
| B36 | long-horizon composition / preservation endpoint | C |
| Other B batches | supporting breadth / supplement | A or appendix |

No batch receives a subsection solely because it has an interesting story.

---

# 12. Reader-first section test

Before accepting any section, ask:

1. **What question is the reader asking at this point?**
2. **Does the first paragraph answer that question before giving details?**
3. **Is every subsequent paragraph evidence or explanation for that answer?**
4. **Could one paragraph be removed without weakening the argument? If yes, remove it or move it to the supplement.**
5. **Does the section end by establishing why the next section is needed?**

If a section begins with project bookkeeping, batch taxonomy, caveats, or terminology before the reader knows why it matters, the order is wrong.

---

# 13. Narrative flow in one minute

A reader should be able to summarize the paper as follows:

> Photogrammetry gives us a rough physical scene, but an engineering model needs explicit reusable components and connections. AstraBuild asks whether a general-purpose reasoning model can operate that reconstruction process using executable geometry tools. Across B01–B36, the same agent/tool interface is used for very different reconstruction tasks. The important change is not simply scale: as the problem becomes structurally richer, the model must move from defining fit problems to managing reusable abstractions, connected representations, and accumulated state. Deterministic tools provide metric computation and validation, while persistent state lets later tasks build on earlier ones. B36 shows that this state can grow to a large integrated station model, and B15 shows why such persistence also requires careful provenance and validation.

If the final manuscript cannot be retold this simply, the outline has become too complicated again.
