# Outline v0 — discussion draft

## Working title candidates

1. **AstraBuild: Scaling a General-Purpose Reasoning Model from Local Fits to Persistent Industrial 3D Reconstruction**
2. **From Local Geometry to Connected Engineering Systems: A Longitudinal Study of GPT-6 Astra for Industrial 3D Reconstruction**
3. **AstraBuild: Long-Horizon Agentic Reconstruction of a Component-Level Industrial Site**

Preferred at this stage: **1**. It states the progression being studied rather than advertising the final artifact.

---

# Abstract logic — do not write as a batch summary

The abstract should contain only five moves:

1. **Problem gap.** Existing 3D generation / CAD reconstruction work typically focuses on isolated objects, short-horizon scene synthesis, or fixed input-output models. Industrial site reconstruction is heterogeneous, stateful, and requires editable component structure, reuse, connectivity, and revision.
2. **Question.** Can a general-purpose reasoning model coordinate executable geometry tools over a long horizon, and how does the workflow change as reconstruction complexity grows?
3. **Study design.** One GPT-6 Astra/Codex workflow, one operating substation, B01–B36, grouped into four reconstruction regimes; no IID-success-rate claim.
4. **Main findings.** Local fitting relies mainly on extraction/fitting; reusable equipment introduces measurement/planning/refinement; connected systems require routing/topology/coverage operators; late site closure depends on persistent state preservation and review/interference checks. Deterministic tools provide metric computation; the model primarily controls representation, decomposition, evidence selection, and program synthesis.
5. **Boundary.** Single site, no matched model baseline, no independent survey truth.

No D37+, no D38 markup story, no D40/D41, no long list of scripts/manifests in the abstract.

---

# 1. Introduction

## 1.1 The engineering gap

Start with the distinction between **recovering a surface** and **constructing an editable engineering model**.

A photogrammetric reconstruction can provide occupied geometry and appearance, but an engineering representation needs:

- explicit component identities;
- repeated equipment represented through reusable structure;
- site-specific connections;
- topology / continuity for conductor systems;
- revision without destroying prior state;
- validation that is appropriate to each type of geometry.

Then state why this is hard for a general model: the input evidence is heterogeneous, tasks are not homogeneous, and the desired representation changes over time.

## 1.2 Scientific question

> Can one general-purpose reasoning model coordinate a persistent tool-using reconstruction process that scales from local metric fitting to reusable equipment families, connected systems, and site-level closure?

Secondary question:

> Which parts of the process are handled by model reasoning, and which require explicit deterministic geometry operators and validators?

## 1.3 Contributions

Keep to **three contributions**, not five or six.

1. **Problem / system formulation.** Industrial component-level reconstruction as a persistent agentic reverse-engineering process over heterogeneous physical evidence and executable geometry tools.
2. **Longitudinal B01–B36 study.** A 36-batch real-site reconstruction trace organized into four increasingly structured reconstruction regimes, from local fitting to connected-system and site-level integration.
3. **Cross-regime analysis.** Evidence that the computational demands change with problem structure: fitting dominates early tasks; reusable abstractions, planning and refinement emerge for equipment families; route/topology/coverage operators emerge for connected systems; persistent state and review become central at site closure.

Do not make “37k objects” a contribution.

---

# 2. Related Work

This section should be short and argumentative, not encyclopedic.

## 2.1 Structured 3D / CAD reverse engineering

Discuss work that reconstructs editable or parametric models from point clouds, e.g. Point2CAD / CAD-Recode. The relevance is the shared goal of moving from sampled geometry to structured, editable representations.

Gap relative to AstraBuild: those methods generally learn a fixed mapping for object-scale CAD reconstruction; our setting is a heterogeneous site-scale sequence whose representation and tools vary across tasks.

## 2.2 LLMs as 3D program generators

Discuss 3D-GPT and SceneCraft.

Key contrast: these methods primarily synthesize scenes from language. AstraBuild reconstructs a real physical site from registered evidence and must preserve metric relationships, prior state, and engineering reuse.

## 2.3 Long-horizon tool-using agents

Discuss Voyager and GPT-Policy as examples of executable action spaces, feedback loops, persistent context / skill reuse.

Use these works to motivate the agent architecture, not to turn the paper into a robotics analogy.

End Related Work with one precise gap sentence:

> Existing work separately demonstrates structured reverse engineering, 3D code generation, and long-horizon tool use; B01–B36 provides a field record in which all three requirements interact inside one persistent industrial reconstruction.

---

# 3. Problem Setting and Agent Interface

This should be compact: approximately 1–1.5 pages.

## 3.1 Inputs and target representation

Inputs:

- registered photogrammetric geometry;
- UAV / ground imagery;
- engineering / inventory records when available;
- previously accepted reconstruction state.

Output:

- editable Blender component geometry;
- reusable equipment masters / instances;
- explicit site-specific connections;
- persistent scene state and validation records.

## 3.2 What the model does versus what tools do

**Model / agent decisions:**

- choose evidence / local domain;
- choose geometric representation;
- decompose task;
- write or revise Python / Blender code;
- decide which specialized measurement / routing / inspection tool to invoke;
- interpret validation and review feedback.

**Deterministic execution:**

- fitting / optimization;
- coordinate transforms;
- rendering;
- distance / residual computation;
- contact / continuity / collision checks;
- file / history preservation.

This division is important because a centimeter-scale fit should not be attributed to “LLM numerical precision.”

## 3.3 Persistent reconstruction state

Only one schematic is needed:

`evidence + previous state -> agent decision -> executable operator -> validation -> updated persistent state`

Do not put the full historical file hierarchy in the main paper.

---

# 4. Longitudinal Evaluation Design

This section replaces the current mixture of task cards, behavior labels, review console, and case taxonomy.

## 4.1 Why B01–B36 are a longitudinal study, not a benchmark

- one model / harness;
- one site;
- later tasks inherit earlier outputs;
- validators differ by geometry type;
- therefore there is no meaningful global success-rate denominator.

## 4.2 Four reconstruction regimes

Main table:

| Regime | Batches | Reconstruction target | New structural challenge | Representative evidence |
|---|---:|---|---|---|
| I. Local fitting | B01–B06 | arresters, wall, gate | local metric geometry | B01/B02, B06 |
| II. Reusable equipment | B07–B19 | transformers, capacitor banks, GIS | repeated structure, variants, reuse boundary | B08, B15, B17/B19 |
| III. Connected systems | B20–B30 | busbars, conductors, insulators | topology, flexible paths, coverage gaps | B20, B23, B25/B26, B29 |
| IV. Site closure | B31–B36 | buildings, ground, cabins, auxiliaries | closing residual gaps while preserving prior state | B31/B32, B35/B36 |

## 4.3 Evaluation evidence

Only define metrics that recur in the results:

- local reference-surface agreement for selected domains;
- fit / holdout checks where meaningful;
- endpoint / contact continuity for connected systems;
- selected-region coverage gap for omission discovery;
- history preservation and state counts at late stages.

Avoid one giant global metric table.

---

# 5. Results: From Local Fits to System Reconstruction

This is the core of the paper. Each subsection should have the same internal pattern:

**challenge -> representative task -> quantitative / visual evidence -> what capability was newly required**.

## 5.1 Regime I: Local geometry can be reduced to explicit fitting problems

Use B01/B02 and B06.

Story:

- local reference extraction makes metric fitting possible;
- B01 also shows that defining the comparison domain is part of the engineering task;
- once the domain is defined, fitting can be delegated to deterministic solvers.

Main point:

> early reconstruction is mostly an evidence-selection + fitting problem.

One figure: arrester / wall example with reference, model, residual domain.

## 5.2 Regime II: Repeated equipment requires reusable abstractions, not independent fits

Use B08, B15 and one GIS family example.

Story:

- B08 introduces reusable transformer structure;
- GIS families scale this idea;
- B15 shows that the boundary between reusable master and site-specific finite geometry matters.

Main point:

> scaling from one object to equipment families requires abstraction and representation management.

One figure: MASTER -> site instances + example of site-specific connector boundary.

## 5.3 Regime III: Connected systems change the problem from object geometry to topology and paths

Use B20, B23, B25/B26, optionally B29.

Story:

- conductor / bus reconstruction depends on endpoints and route continuity;
- B23 shows why flexible path representation is different from rigid object fitting;
- B25/B26 shows that coverage can become a signal for choosing the next reconstruction task.

Main point:

> once components must interact, local fit quality is insufficient; routing, topology, and unexplained occupancy become first-class constraints.

This should probably be the **most important results subsection**.

## 5.4 Regime IV: Site closure tests persistent state rather than a new device family

Use B31/B32 and B35/B36.

Story:

- civil and auxiliary tasks fill large and small residual structures;
- later batches must preserve tens of thousands of existing objects and prior transforms;
- B36 adds interference/collision reasoning while preserving inherited state.

B36 endpoint evidence available in the existing record:

- 36,812 objects;
- 743 scenes;
- 7,116 station objects;
- 36,615 previous objects preserved;
- 2,798 protected files unchanged.

Main point:

> late-stage difficulty is integration under accumulated state, not simply generating more geometry.

One figure: B36 station view + compact state-preservation summary.

---

# 6. Cross-Regime Analysis

Keep this to **three findings**.

## Finding 1 — The agent's role moves upward as tasks become structurally richer

Early: select local evidence and fit parameters.

Later: choose abstraction boundaries, topology, flexible representations, task order, and specialized operators.

Interpretation: general reasoning is most useful in specifying the engineering problem, not replacing numerical geometry algorithms.

## Finding 2 — No single reconstruction operator covers the full site

The process catalog shows a stable build/validate backbone but changing operator use across regimes:

- B01–B06: fit dominates;
- B07–B19: measure / plan / refine / audit become common;
- B20–B30: inspect / plan / routing-like and coverage operations become important;
- B31–B36: measurement / review / state preservation / interference checks dominate.

Present this as a descriptive longitudinal observation, not a causal statistic.

A batch × operator heatmap would be much more informative than the current list of stage counts.

## Finding 3 — Persistent state is the enabling condition for station-scale reconstruction

Reuse, inherited transforms, protected history, and earlier accepted geometry allow later tasks to compose.

But persistence also creates risk: a wrong reusable abstraction can propagate. B15 is the clean example.

This is where reuse / state preservation belongs; not as a separate “37k-object achievement” section.

---

# 7. Discussion

## 7.1 What B01–B36 demonstrates

A general-purpose reasoning model can operate a long-horizon structured 3D reconstruction process when metric computation and acceptance are delegated to explicit tools and validators.

## 7.2 What it does not demonstrate

- superiority over alternative models;
- survey accuracy;
- autonomy;
- transfer to another site;
- a stationary benchmark success rate.

## 7.3 Implication for agentic engineering systems

The main design principle:

> use the general model to formulate and revise structured engineering operations; use deterministic tools to compute and verify geometry; preserve accepted state so later tasks can build on it.

---

# 8. Conclusion

Three sentences are enough:

1. B01–B36 shows a progression from local fitting to reusable, connected, persistent engineering reconstruction.
2. The required computational structure changes with task complexity, so the useful role of a general-purpose model is orchestration and representation-level reasoning rather than raw geometric calculation.
3. Controlled multi-model and multi-site experiments are the next step.

---

# Appendix / website evidence

Move here rather than main paper:

- all 36 batch entries;
- original review pages;
- detailed manifests / file counts;
- all revision histories;
- full task-native metric ledger;
- process dossiers;
- extra videos.

The website can remain a rich evidence browser, but the paper should not read like the website.

---

# Proposed main-paper visual budget

1. **Figure 1 — Problem and agent loop:** noisy physical evidence -> model/tool loop -> structured editable state.
2. **Figure 2 — B01–B36 longitudinal map:** four regimes, representative batches, cumulative state.
3. **Figure 3 — Regime I/II transition:** local fit -> reusable equipment family.
4. **Figure 4 — Regime III:** connected-system routing / flexible lead / coverage example.
5. **Figure 5 — Regime IV/B36 endpoint:** site closure + preserved state.
6. **Figure 6 — Operator evolution heatmap:** batch x operator, grouped by the four regimes.

Main tables: at most two.

- Table 1: four regimes and representative evidence.
- Table 2: selected quantitative readouts with explicit scope.

Everything else moves to appendix / website.
