# Outline v1 — B01–B36 longitudinal reconstruction paper

## Status

Outline only. No manuscript prose should be drafted from this file until the central question, section order, and figure plan are accepted.

Empirical boundary: **B01–B36 only**.

Excluded from the main scientific argument: D37, D38, D40, D41 and claims that depend primarily on those later stages.

---

# 0. Paper contract

## 0.1 Recommended paper archetype

**Longitudinal systems / field-study paper on agentic industrial 3D reconstruction.**

This is not positioned as:

- an IID benchmark;
- a model leaderboard;
- a state-of-the-art geometric reconstruction paper;
- an autonomous digital-twin system;
- a paper whose contribution is the final object count.

The paper studies **how one general-purpose reasoning model coordinates a changing set of engineering operations as one persistent reconstruction grows from local geometry to site-scale structured state**.

## 0.2 Recommended working title

### Preferred

**AstraBuild: From Local Fits to Persistent Industrial 3D Reconstruction with a General-Purpose Reasoning Agent**

Why this title is preferred:

- it states the longitudinal progression rather than advertising a final asset;
- it does not imply controlled scaling laws;
- it leaves room for both the agent contribution and deterministic geometry tools;
- it matches the natural B01–B36 boundary.

### Alternatives

1. **From Local Geometry to Connected Engineering Systems: A Longitudinal Study of GPT-6 Astra for Industrial 3D Reconstruction**
2. **AstraBuild: Long-Horizon Agentic Reconstruction of a Component-Level Industrial Site**
3. **AstraBuild: Coordinating Geometry Tools for Persistent Industrial 3D Reconstruction**

Do not use a title centered on “hypothesis revision”, “human correction”, D38, inspection semantics, or “37k objects”.

## 0.3 Central scientific question

> **Can a general-purpose reasoning model coordinate a persistent reconstruction process that grows from local metric fitting to reusable equipment families, connected systems, and site-level closure?**

Secondary question:

> **How does the required division of labor between model reasoning and explicit engineering operators change as the reconstruction problem becomes structurally richer?**

These are the only two paper-level research questions.

## 0.4 One-sentence thesis

> **Across B01–B36, the reconstruction problem changes from local fitting to abstraction, connectivity, and accumulated-state integration; the same reasoning model remains useful by choosing evidence, representations, decompositions, and executable operations, while numerical geometry and acceptance are delegated to task-specific deterministic tools and validators.**

## 0.5 Three contributions only

1. **Persistent agentic reverse-engineering formulation.** Industrial component-level reconstruction is formulated as a persistent process over heterogeneous physical evidence, editable scene state, executable geometry operators, and task-specific validation.
2. **B01–B36 longitudinal field study.** A 36-batch reconstruction record from one operating substation is organized into four qualitatively different reconstruction regimes rather than treated as 36 IID trials.
3. **Cross-regime analysis of changing computational structure.** The record shows that local fitting, reusable equipment, connected systems, and late site closure require different combinations of measurement, abstraction, routing, coverage, review, and state-preservation operations.

The final station scale is evidence for contribution 2/3, not a fourth contribution.

---

# 1. Abstract — rebuild only after Results stabilize

## Reader function

Tell a reviewer in ~180–220 words:

1. what scientific problem is studied;
2. why existing 3D reconstruction/generation formulations do not fully cover it;
3. what B01–B36 constitutes as an experiment;
4. what the principal cross-regime findings are;
5. what the evidence does not establish.

## Required five-move structure

### Move 1 — Problem

Photogrammetric reconstruction supplies geometry/appearance, but an engineering model additionally requires editable components, reuse, explicit connectivity, and persistent revision across heterogeneous tasks.

### Move 2 — Question

Ask whether one general-purpose reasoning model can coordinate such a persistent reconstruction process as the problem changes structurally.

### Move 3 — Study design

State only:

- one GPT-6 Astra/Codex workflow;
- one operating operating substation;
- B01–B36;
- four reconstruction regimes;
- later batches inherit earlier state;
- therefore not an IID benchmark.

### Move 4 — Findings

Use **three findings**, not a batch list:

1. early local tasks can be reduced to explicit fitting problems once the relevant evidence/domain is selected;
2. repeated equipment and connected systems require higher-level abstractions, topology/path reasoning, and task-specific operators beyond local fitting;
3. late site closure is primarily an accumulated-state integration problem, requiring preservation, review, and interference checks while thousands of prior objects remain active.

Then state the division of labor:

- model: evidence selection, representation/decomposition, program synthesis, operator choice, interpretation of feedback;
- tools: numerical fitting, transforms, geometry execution, residual/contact/collision computation, acceptance checks.

### Move 5 — Boundary

Single site; no independent survey truth; no matched second-model/expert baseline; human review remains material in parts of the process.

## Explicit exclusions from Abstract

Do not include:

- D37/D38/D40/D41;
- 54 builders / 58 validators / 150 manifests;
- long lists of equipment counts;
- 37k-object headline from D38/D40;
- a catalog of failure episodes;
- semantic inspection results;
- “Astra is accurate to X cm”.

---

# 2. Introduction

Target: **~1.25–1.5 pages**.

## 2.1 From reconstructed surfaces to engineering representations

### Reader function

Establish the scientific gap before introducing GPT-6 Astra.

### Core claim

Recovering occupied 3D geometry is not equivalent to recovering an editable engineering system.

### Evidence / concepts allowed

Explain that an industrial engineering representation needs:

- component identity and hierarchy;
- repeated equipment expressed through reusable structure;
- finite site-specific connections;
- conductor/bus topology and continuity;
- persistent state that can be edited without destroying prior work;
- task-appropriate validation.

### Do not do

- no project chronology yet;
- no batch numbers in the first paragraph;
- no object counts;
- no GPT-6 marketing language.

## 2.2 Why the problem is difficult for a general-purpose model

### Reader function

Explain why this is not one fixed input-output mapping.

### Core claim

The representation and required operations change with the target: rigid local fitting, reusable device families, flexible routes, connected topology, large civil geometry, and late-stage site closure are different computational problems.

This paragraph should motivate the longitudinal experiment naturally.

## 2.3 Research questions

Only two:

**RQ1. Persistent reconstruction.** Can one general-purpose reasoning model operate a single persistent reconstruction process across local components, reusable equipment families, connected systems, and site-level closure?

**RQ2. Changing computational structure.** As the reconstruction regime changes, which decisions remain with the reasoning model and which require explicit measurement, routing, validation, review, or state-preservation operators?

No separate RQ for failures, semantics, human correction, coverage, or final scale.

## 2.4 Contributions

Exactly the three contributions from §0.5.

### Bridge into Related Work

The novelty should be framed as the interaction of three previously more separate themes:

- structured reverse engineering;
- programmatic 3D generation/tool use;
- long-horizon persistent agent operation.

---

# 3. Related Work

Target: **~0.75–1 page**.

The section must end in a precise gap. It should not become a literature survey.

## 3.1 Structured 3D / CAD reverse engineering

Examples: Point2CAD, CAD-Recode and related structured reconstruction work.

### Use them to establish

The field already recognizes that editable/parametric structure is a different target from raw surface recovery.

### Gap relative to this paper

Most object/CAD reconstruction methods implement a comparatively fixed mapping from a defined input representation to a structured output. AstraBuild instead studies a heterogeneous site sequence in which the target representation and engineering operators change across tasks.

## 3.2 LLMs as 3D program generators

Examples: 3D-GPT, SceneCraft.

### Use them to establish

LLMs can decompose 3D tasks, generate Blender/programmatic geometry, inspect results, and reuse functions/assets.

### Gap relative to this paper

Those works mainly synthesize from language/specifications. B01–B36 is a reverse-engineering process constrained by registered physical evidence, inherited scene state, connectivity, and validation.

## 3.3 Long-horizon tool-using agents

Examples: Voyager, GPT-Policy; RoboDojo only as an evaluation/reporting contrast where useful.

### Use them to establish

Persistent state, executable action spaces, feedback, and reusable skills can support long-horizon model behavior.

### Gap sentence to end the section

> Existing work separately demonstrates structured reverse engineering, 3D program synthesis, and long-horizon tool use; B01–B36 provides a field record in which these requirements interact inside one persistent industrial reconstruction whose computational structure changes over time.

Do not overextend the robotics analogy.

---

# 4. Problem Setting and Agent Interface

Target: **~1–1.25 pages**.

This section should be compact. Its purpose is only to make the later experiment interpretable.

## 4.1 Evidence and target state

### Inputs

- registered photogrammetric geometry;
- UAV / ground imagery;
- engineering / inventory records where available;
- accepted geometry and metadata from earlier batches.

### Persistent output state

- editable Blender component geometry;
- reusable equipment masters and instances where justified;
- site-specific connectors and routes;
- review/validation artifacts and frozen history.

A formal state notation is optional. If retained, use one equation only.

## 4.2 Division of labor: model decisions versus deterministic execution

### Model-visible decisions

- choose the local evidence/domain;
- choose geometric representation;
- decompose a task;
- write or revise Python/Blender programs;
- choose which measurement/routing/inspection operator to invoke;
- interpret review/validation feedback and decide what to revise.

### Deterministic execution

- least-squares / profile fitting;
- coordinate transforms;
- Blender geometry construction and rendering;
- residual, endpoint, contact, continuity, coverage, collision calculations;
- file/hash/state-preservation checks.

### Main methodological rule

A numerical residual produced by a deterministic solver is **not** evidence of internal LLM numerical precision. The model contribution is the formulation and orchestration of the engineering operation.

## 4.3 Persistent state and acceptance

One simple loop only:

`evidence + previous state -> agent decision -> executable operator -> review/validation -> accepted or revised state`

State that different task families require different validators. Do not present one global score.

## Main figure

### Figure 1 — Problem and agent interface

The figure should be visually intuitive, not a software architecture diagram.

Left:

- field image;
- registered coarse geometry;
- prior accepted station state.

Center:

- Astra reasoning / code generation;
- compact set of operator icons: fit, build, route, review, validate.

Right:

- editable component model;
- reusable family;
- connected subsystem;
- updated persistent station state.

Bottom strip:

`model chooses the engineering operation | deterministic tools compute and verify it`

No filesystem boxes, 10-arrow loop, or D38/D41 material.

---

# 5. Longitudinal Evaluation Design

Target: **~1.25 pages**.

## 5.1 Experimental unit and why it is not a benchmark

### Reader function

Prevent the reader from interpreting B01–B36 as 36 independent trials.

State:

- one model/harness;
- one site;
- sequential inherited state;
- heterogeneous targets and validators;
- no global success-rate denominator.

The basic unit of analysis is therefore a **reconstruction regime and its representative tasks**, not an IID trial.

## 5.2 Four reconstruction regimes

### Table 1 — Study organization

| Regime | Batches | Main target | New structural requirement | Representative cases |
|---|---:|---|---|---|
| I. Local fitting | B01–B06 | arresters, wall, gate | registered local metric fitting | B01/B02, B06 |
| II. Reusable equipment | B07–B19 | transformers, capacitor banks, GIS | reuse, variants, master/site boundary | B08, B15, B17 |
| III. Connected systems | B20–B30 | buses, conductors, insulators | topology, endpoints, flexible paths, unexplained occupancy | B20, B23, B25/B26, B29 |
| IV. Site closure | B31–B36 | civil/auxiliary gaps and remaining interfaces | accumulated-state preservation, review, interference | B31/B32, B35/B36 |

### Figure 2 — B01–B36 longitudinal map

This should show:

- four color-coded regimes;
- B01 … B36 on one axis;
- representative targets above the axis;
- cumulative station state below the axis;
- only major methodological transitions, not every batch note.

Suggested transition labels:

1. local fit domains;
2. reusable masters / instances;
3. connectivity / flexible routes;
4. coverage-driven omission search;
5. late state-preservation / interference checks.

## 5.3 Evaluation evidence

Define only quantities actually used later.

1. **Local reference agreement** on selected domains.
2. **Fit / holdout separation** where applicable.
3. **Endpoint/contact/continuity** for connected systems.
4. **Selected-region coverage gap** for omission discovery.
5. **State preservation** for late-stage integration.
6. **Same-camera Clean / Overlay / Reference review** as qualitative correspondence evidence.

### Table 2 — Selected readouts, not global score

Suggested rows only:

- B01/B02 — evaluation-domain lesson;
- B06 — local civil fit;
- B08 — reusable transformer family;
- B17 — complex GIS family with retained non-passing checks;
- B23 — curved lead / representation change;
- B25/B26 — coverage-gap signal;
- B32 — metric envelope versus fine-detail interpretation;
- B36 — accumulated-state preservation / interference handling.

Columns:

`Case | What is measured | Readout | What it supports | What it does not support`

This table replaces giant metric inventories.

---

# 6. Results — From Local Fits to System Reconstruction

Target: **~4–4.5 pages**. This is the center of the paper.

Every subsection follows the same contract:

1. reconstruction challenge;
2. representative case(s);
3. quantitative / visual evidence;
4. new engineering operation or abstraction that became necessary;
5. narrow conclusion for that regime.

Do not end each subsection with a generic “lesson”. State the result directly.

## 6.1 Regime I — Local geometry can be reduced to explicit fitting problems

### Cases

B01/B02 + B06.

### Reader question

What does the simplest successful reconstruction regime look like?

### Argument

1. Registered local geometry makes metric reconstruction tractable.
2. B01/B02 shows that defining the fitting/holdout domain is itself part of the reconstruction problem.
3. Once the domain and representation are specified, numerical fitting can be delegated to deterministic solvers.
4. B06 shows the same principle on larger civil geometry rather than a small device.

### Main claim

> **At the local-fitting regime, the model's main role is to select the relevant evidence, parameterization, and comparison domain; the geometric estimate itself is produced and checked by explicit numerical tools.**

### Figure 3A

One compact paired example:

`reference -> fitted model -> overlay / residual domain`

Use arrester and/or wall only. Do not show six B01–B06 outputs.

### Evidence boundary

No claim of survey accuracy.

## 6.2 Regime II — Repeated equipment requires reusable engineering abstractions

### Cases

B08 + B15 + one complex GIS example (prefer B17; use B19 only if B17 evidence is insufficient).

### Reader question

What changes when the goal is no longer one fitted object, but a family of related installations?

### Argument

1. B08 promotes transformer structure into a reusable master/site representation.
2. Repeated GIS families extend reuse to larger and more varied assemblies.
3. B15 shows why reuse is not only an implementation optimization: finite site-specific geometry placed inside a shared master propagates the wrong structure.
4. Therefore the central problem becomes deciding the **abstraction boundary** between shared and local geometry.

### Main claim

> **Scaling from isolated objects to equipment families requires the model to reason about equivalence, reuse boundaries, and variants in addition to local fit.**

### Figure 3B / Figure 3

Preferred Figure 3 as a full-width “fit → reusable family” transition:

- left: Regime I local fitted object;
- center: B08 shared MASTER → T1/T2;
- right: B15 shared-vs-site-specific boundary correction.

This makes Figure 3 support the transition between regimes rather than one batch.

### Evidence boundary

Do not describe reuse ratio as speedup or productivity.

## 6.3 Regime III — Connected systems require topology, paths, and coverage reasoning

### Cases

B20 + B23 + B25/B26 + B29 (B29 only where it adds a distinct conductor/route point).

### Reader question

What breaks when individually plausible components must become one connected electrical/mechanical system?

### Argument

1. B20 introduces explicit endpoint / connection reasoning; local component fit is no longer sufficient.
2. B23 shows that a connection may require a different representation class (curved/flexible path rather than rigid/straight segment).
3. B25/B26 changes completion logic: the coarse reference becomes a sensor for **unexplained occupancy**, not only a fitting surface.
4. B29 can show that endpoint continuity and surface agreement answer different questions for conductor systems.

### Main claim

> **Once reconstruction targets relationships between components, the problem changes from object fitting to constrained system construction: topology, endpoint continuity, flexible paths, and unexplained occupancy become first-class state variables.**

### Importance

This should be the **largest and strongest Results subsection**.

### Figure 4 — Connected-system reconstruction

A four-panel scientific figure, not a gallery:

A. B20 route / endpoint diagnostic.
B. B23 measured profile → curved lead representation.
C. B25/B26 unexplained-coverage before/after.
D. final connected-system overlay or B29 route example.

Every panel should answer a distinct system-level constraint.

### Evidence boundary

Coverage reduction is for selected audited regions, not whole-station completeness.

## 6.4 Regime IV — Site closure becomes an accumulated-state integration problem

### Cases

B31/B32 + B35/B36.

### Reader question

What is difficult after most major equipment already exists?

### Argument

1. B31–B34 add building, ground, cabins and civil structure into an already large station state.
2. B32 demonstrates a useful distinction: deterministic envelope fitting can be satisfactory while fine structural interpretation still requires review.
3. B35/B36 concern residual/auxiliary structures and interfaces, where the main risk is corrupting or interfering with accepted previous state.
4. B36 adds collision/interference handling while preserving inherited objects/transforms/files.

### B36 endpoint evidence

Use the B36 validator because it is inside the natural B01–B36 boundary:

- 36,812 objects;
- 743 scenes;
- 7,116 station objects;
- 36,615 previous objects unchanged;
- 7,114 previous station transforms unchanged;
- 2,798 protected files unchanged;
- finite new geometry and asset round-trip checks retained.

These are **state-preservation / scale descriptors**, not independent accuracy statistics.

### Main claim

> **Late-stage reconstruction is dominated by integration under accumulated state: new geometry must close residual gaps without invalidating previously accepted structure.**

### Figure 5 — Site closure under accumulated state

Left:

- B31/B32 building/cabin review or station view.

Center:

- B36 bus-rack / interference example.

Right:

- compact preservation ledger: prior objects, transforms, protected files, current station objects.

No post-B36 station view.

---

# 7. Cross-Regime Analysis

Target: **~1.25–1.5 pages**.

Only three findings. They must synthesize the four Results sections rather than introduce new cases.

## 7.1 Finding 1 — The model's decision level moves upward with structural complexity

### Evidence pattern

Regime I:

- evidence/domain selection;
- local representation;
- fitting invocation.

Regime II:

- equivalence;
- shared/local abstraction boundary;
- variant handling.

Regime III:

- route/topology representation;
- endpoint constraints;
- coverage-driven task choice.

Regime IV:

- integration ordering;
- review of fine details;
- preservation / interference decisions under accumulated state.

### Interpretation

> **The useful role of general reasoning shifts from specifying local measurement problems to organizing representations and dependencies that are difficult to encode as one fixed reconstruction operator.**

This is the paper's main interpretive result.

## 7.2 Finding 2 — The stable backbone is build/validate; the specialized operators change by regime

### Evidence

Use the existing B01–B36 stage audit as descriptive evidence.

Regime I B01–B06:

- fit: 6/6;
- plan: 0/6;
- measure: 0/6;
- refine: 0/6.

Regime II B07–B19:

- extract: 13/13;
- measure: 8/13;
- plan: 7/13;
- refine: 9/13;
- audit: 10/13.

Regime III B20–B30:

- inspect: 8/11;
- plan: 8/11;
- fit: 6/11;
- refine: 7/11;
- audit: 10/11.

Regime IV B31–B36:

- measure: 6/6;
- inspect: 5/6;
- review: 5/6;
- plan: 4/6;
- collision appears in B36.

These counts describe **recorded workflow stages**, not agent success, cognitive effort, or causal necessity.

### Figure 6 — Operator evolution heatmap

Rows: B01–B36.

Columns, grouped semantically rather than raw filename prefix order:

- prepare / extract;
- fit / measure;
- plan / inspect;
- build / refine;
- route / connectivity / coverage / collision where available;
- review;
- validate / audit / release.

Add horizontal boundaries between four regimes.

Do not put 18 tiny raw-prefix columns if they become unreadable. Combine only where the underlying records genuinely support the grouping.

### Main claim

> **B01–B36 does not instantiate one universal reconstruction algorithm; it uses a stable execution/validation backbone with specialized operators activated as the structure of the engineering problem changes.**

## 7.3 Finding 3 — Persistent state is both enabling infrastructure and a propagation risk

### Evidence

Positive:

- accepted geometry is inherited;
- reusable masters support later tasks;
- transformations and protected artifacts remain available;
- connected systems reference equipment created earlier;
- B36 validates preservation at large state scale.

Negative:

- B15 demonstrates that an incorrect shared abstraction can propagate through persistence/reuse.

### Main claim

> **Persistent state enables station-scale composition, but it also makes early representation errors consequential; provenance, validation, and explicit shared/local boundaries are therefore part of the reconstruction method rather than bookkeeping.**

Do not introduce D38 quarantine or D40/D41 version layering here.

---

# 8. Discussion

Target: **~1–1.25 pages**.

## 8.1 What the B01–B36 record demonstrates

Supported statement:

> A general-purpose reasoning model can coordinate a heterogeneous, long-horizon 3D engineering process when geometric computation and acceptance are externalized to explicit tools and validators, and when accepted state is preserved for later tasks.

The distinctive contribution is **orchestration of changing reconstruction problems**, not raw numerical geometry.

## 8.2 What the study does not isolate

State clearly:

- no matched second-model comparison;
- no no-agent / fixed-pipeline ablation;
- no professional CAD baseline;
- no independent survey reference;
- one site only;
- human review affects parts of the trajectory;
- model/version/reasoning configuration is owner-confirmed rather than frozen in all old batch manifests.

Therefore the paper characterizes one successful longitudinal system record; it does not causally attribute every outcome to GPT-6 Astra alone.

## 8.3 Design implication

One concise principle:

> **Use the general model to formulate, decompose, and revise engineering operations; use deterministic tools to compute and verify geometry; preserve accepted state so later tasks can build on it.**

This should end Discussion. No new result after this point.

---

# 9. Conclusion

Target: **one short paragraph, 3–5 sentences**.

Required sequence:

1. B01–B36 progresses from local fitting to reusable equipment, connected systems, and site closure.
2. The required computational structure changes with the reconstruction regime.
3. The observed value of the general-purpose model lies primarily in evidence/representation/operator orchestration rather than numerical geometry computation or acceptance.
4. Controlled second-model, second-site, and independent-reference studies are the next empirical step.

Do not restate every batch, metric, or limitation.

---

# 10. Main-paper visual and table budget

## Figures — maximum six

### Figure 1 — Problem and agent interface

Purpose: make the paper understandable in 10 seconds.

Physical evidence + previous state → model decisions → specialized geometry operators → review/validation → editable persistent state.

### Figure 2 — B01–B36 longitudinal study map

Purpose: establish the four regimes and progression before Results.

### Figure 3 — From local fits to reusable equipment

Purpose: support Results 6.1 + 6.2 as one transition.

Suggested panels:

- local fitted object / civil surface;
- B08 MASTER → T1/T2;
- B15 correction of shared/site boundary.

### Figure 4 — Connected systems

Purpose: flagship scientific result.

Panels:

- route / endpoint constraints;
- B23 flexible path representation;
- B25/B26 coverage-driven completion;
- connected-system output / B29 example.

### Figure 5 — Site closure under accumulated state

Purpose: show that the natural endpoint is B36, not later D-series work.

Panels:

- civil/cabin closure;
- B36 integration/interference;
- compact B36 state-preservation ledger.

### Figure 6 — Operator evolution across regimes

Purpose: cross-regime analysis.

Batch × operator heatmap with regime boundaries.

## Tables — maximum two

### Table 1 — Four reconstruction regimes

Study organization, not results dump.

### Table 2 — Selected evidence with claim scope

Only representative cases used in the argument.

Suggested columns:

`Case | Measurement / check | Readout | Supports | Does not support`

---

# 11. Batch-to-paper assignment

A batch should appear in the main text only if it serves a specific argumentative function.

| Batch / range | Main-text role |
|---|---|
| B01/B02 | local fitting; comparison-domain definition |
| B06 | local/civil fitting generalization |
| B08 | reusable transformer abstraction |
| B15 | failure of shared/local abstraction boundary |
| B17 | complex reusable GIS family / retained non-pass evidence |
| B20 | transition to explicit connectivity / routes |
| B23 | flexible path representation based on measured profile |
| B25/B26 | coverage as omission/task-selection signal |
| B29 | optional distinct conductor/path evidence only if it adds beyond B20/B23 |
| B31/B32 | civil/site closure; metric envelope versus fine-detail interpretation |
| B35/B36 | residual auxiliary closure; accumulated-state preservation and interference |

All other B batches remain part of Table 1 / Figure 2 / appendix evidence, but they do not each receive prose subsections.

This is deliberate. The paper must not become a batch log.

---

# 12. Page budget for a ~10-page main paper

Approximate body allocation before references:

| Section | Pages |
|---|---:|
| Abstract | 0.25 |
| Introduction | 1.25 |
| Related Work | 0.75 |
| Problem Setting / Agent Interface | 1.0 |
| Longitudinal Evaluation Design | 1.0 |
| Results | 3.75–4.0 |
| Cross-Regime Analysis | 1.25 |
| Discussion | 0.75–1.0 |
| Conclusion | 0.25 |

The Results section should occupy roughly **40% of the paper body**.

If space is tight, cut Related Work detail and appendix material before cutting Results 6.3.

---

# 13. Claim hierarchy

## Tier 1 — central claim

A general-purpose reasoning model can coordinate one persistent industrial 3D reconstruction across qualitatively different reconstruction regimes when explicit engineering operators and validators externalize numerical computation and acceptance.

## Tier 2 — supported mechanistic interpretations

1. The model's useful decision level moves from local evidence/domain selection toward abstraction, topology, and orchestration as structural complexity increases.
2. No single fixed reconstruction operator accounts for B01–B36; a stable build/validate backbone is combined with regime-specific operators.
3. Persistent state is necessary for long-horizon composition but can propagate incorrect abstractions.

## Tier 3 — case-specific claims

Examples:

- B01/B02: comparison-domain definition matters to local fitting.
- B15: shared/local abstraction boundaries can be wrong.
- B23: measured evidence can require a different path representation.
- B25/B26: selected-region coverage can drive omission discovery.
- B32: metric envelope fit does not resolve visible structural detail.
- B36: late additions can be validated while preserving a large inherited state.

Tier 3 evidence should support Tier 2. Do not promote individual case observations into population frequencies.

---

# 14. Material explicitly removed from the new main paper

The following should not re-enter unless the research scope changes:

- D37 / D38 / D40 / D41;
- the D38 human-markup storyline;
- inspection semantics as a paper contribution;
- 37,153-object D38/D40 endpoint statistics;
- 150-manifest / 58-validator / 54-builder counts as headline results;
- six or more behavioral “findings”;
- failure-layer taxonomy as a core experiment;
- “human correction” as a main section;
- repeated assembly videos;
- full 32-review-page browser in the main narrative;
- all 36 batch dossiers in main-paper order.

These may remain in historical/publication archives, but the B01–B36 rewrite should be scientifically self-contained without them.

---

# 15. Reviewer red-team questions the outline must survive

Before drafting, the answer to each question should be one or two sentences.

1. **What is scientifically new beyond using GPT to write Blender Python?**
   - The longitudinal evidence shows one model coordinating different reverse-engineering regimes whose required abstractions/operators change as persistent state grows.

2. **Are the centimeter residuals just SciPy results?**
   - Yes, the numerical estimates are deterministic-tool outputs; the paper explicitly attributes to Astra the formulation, representation, evidence/domain, code, and operator-selection decisions rather than numerical precision.

3. **Why is this not simply a project report?**
   - Because B01–B36 is analyzed through four reconstruction regimes and three cross-regime findings, not narrated batch by batch.

4. **Why not report a success rate?**
   - Batches are sequential, inherit state, target heterogeneous geometry, and use different validators; no stationary denominator exists.

5. **Why does one site matter scientifically?**
   - It provides a long, stateful field trace that exposes transitions from object fitting to reuse, connected topology, and late integration; external generalization remains explicitly untested.

6. **What does the final station prove?**
   - It demonstrates persistent composition/state preservation over the studied trajectory, not survey accuracy or model superiority.

7. **Could a fixed pipeline have done the same thing?**
   - The historical record does not contain a controlled fixed-pipeline ablation, so the paper cannot make a causal superiority claim. It can show descriptively that different regimes invoked different operators and representation decisions.

8. **How much human work was required?**
   - Human review is material in parts of B01–B36; the historical record does not contain a complete human-time ledger, so autonomy/productivity claims are excluded.

---

# 16. Decisions to lock before drafting Outline v2 / manuscript prose

The following choices should be agreed before writing the new Abstract or Introduction:

1. **Title:** use the preferred “From Local Fits to Persistent Industrial 3D Reconstruction” framing or a more conservative title?
2. **Four regimes:** accept B01–B06 / B07–B19 / B20–B30 / B31–B36 as the principal study organization?
3. **Results emphasis:** accept Regime III connected systems as the largest / most important results subsection?
4. **B36 endpoint:** use B36 as the natural system endpoint and exclude all post-B36 numbers?
5. **Cross-regime findings:** keep exactly the three findings proposed here?
6. **B29:** include only if its conductor evidence adds a distinct point beyond B20/B23; otherwise leave it in appendix.
7. **Main-paper figures:** accept the six-figure budget and move historical review browsers/dossiers entirely outside the paper narrative?

Until these are locked, do not draft full manuscript prose.
