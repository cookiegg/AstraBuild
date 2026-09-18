# Outline v2 — mature claim-driven manuscript plan

## Status and purpose

This is the preferred drafting outline for the **B01–B36-only** rewrite. It replaces the earlier material-first and batch-first structures with a claim-first manuscript architecture designed for a human reader.

The paper should be readable without opening the website, process catalog, review HTML pages, or batch folders. Those artifacts provide evidence and auditability; they do not define the narrative structure.

The claim priority is fixed for this outline:

1. **C2 — main empirical claim:** the operator and decision portfolio broadens as reconstruction dependencies accumulate.
2. **C3 — system-level claim:** persistent external state enables cross-batch composition and also propagates abstraction errors.
3. **C1 — attribution / method foundation:** geometry computation and acceptance are externalized to deterministic tools; the model formulates and revises the engineering operations.

Task breadth is supporting evidence, not a standalone scientific claim.

Evidence boundary: **B01–B36 only**. D37, D38, D40, D41 and claims that depend on them are outside the manuscript.

---

# 0. The paper in one page

## 0.1 The reader's problem

A registered photogrammetric reconstruction provides scene geometry, but an editable industrial engineering model requires decisions that are not reducible to one surface-fitting operator: what constitutes a component, what can be reused, where site-specific geometry begins, how components connect, how flexible paths should be represented, what geometry is still unexplained, and how new work can be added without corrupting prior state.

The paper asks whether a general-purpose reasoning model can coordinate this kind of reconstruction process through executable geometry programs and explicit validation.

## 0.2 One-sentence answer

> **Across B01–B36, station reconstruction proceeds through a stable evidence–program–validation loop whose operator portfolio broadens as dependencies accumulate: GPT-6 Astra/Codex observably formulates and revises the reconstruction operations, deterministic tools compute and validate geometry, and persistent external state allows accepted local solutions to be reused and connected while making mistaken abstractions consequential.**

This sentence is the manuscript's contract. Abstract, Introduction, Results, Discussion, and Conclusion should all be recognizable restatements or qualifications of this answer.

## 0.3 The claim pyramid

### Foundation — C1: division of labor

**Question:** What is the reasoning model actually contributing?

**Answer:** The model selects evidence and domains, chooses representations and decomposition, authors/revises Blender/Python procedures, and interprets review/validation evidence. Numerical fitting, transforms, rendering, residuals, endpoint/contact checks, collision tests, and state-preservation checks are executed by deterministic tools.

**Role in paper:** Method and interpretation. This is necessary for correct attribution, but it is not the paper's central novelty.

### Main claim — C2: broadening decision/operator portfolio

**Question:** Why is this more than repeatedly fitting different objects?

**Answer:** Local fitting remains present, but additional decision layers appear as reconstructed elements become more interdependent: fit-domain selection is joined by reusable-asset boundaries, site-specific connection logic, representation changes, port/route/topology constraints, omission-driven task selection, fixed-view review, and interference checks.

**Role in paper:** Main Results claim. This should receive the most space and the strongest analytical figure.

### System claim — C3: persistent external state

**Question:** What makes B01–B36 one long-horizon reconstruction rather than 36 unrelated Blender jobs?

**Answer:** Later batches explicitly consume earlier masters, transforms, terminals, endpoints, and accepted geometry while validators protect earlier state. This enables cross-batch composition. The same mechanism also propagates upstream abstraction mistakes, as B15 demonstrates.

**Role in paper:** Second Results claim and systems interpretation.

---

# 1. Working title

## Preferred title

**AstraBuild: Orchestrating Persistent Industrial 3D Reconstruction with a General-Purpose Reasoning Model**

Why this is preferred over the earlier "from local fits" title:

- the scientific object is the **orchestration process**, not the final model size;
- it does not imply that the model directly performs numerical geometry;
- it leaves room for the main C2 result: the operation portfolio changes with dependency structure;
- it naturally motivates persistent external state without making persistence the only contribution.

## Alternative, more result-oriented

**AstraBuild: How a General-Purpose Reasoning Model Coordinates Geometry Operations for Persistent Industrial 3D Reconstruction**

Avoid titles centered on:

- "autonomous" reconstruction;
- "centimeter-level" accuracy;
- the final object count;
- hypothesis revision alone;
- D38 human correction;
- semantic inspection.

---

# 2. Abstract — answer first, evidence second

Target: **180–220 words**, one paragraph if the venue permits.

The abstract should follow a strict five-move pyramid. Do not narrate the 36 batches chronologically.

## Move 1 — scientific problem

State the gap in one or two sentences:

- registered 3D reconstruction gives geometry/appearance;
- engineering reconstruction additionally requires explicit editable structure, reuse, connections, and revision of an accumulated state;
- these requirements vary substantially across equipment, conductors, and civil structures.

The abstract should name the scientific problem as **coordinating heterogeneous reconstruction operations over a persistent engineering state**, not merely "building a digital twin."

## Move 2 — study question and setup

One compact sentence:

- one GPT-6 Astra/Codex workflow;
- B01–B36;
- one operating operating substation;
- registered coarse geometry + field images + engineering records + executable Blender/Python tools + task-specific validators.

Do not describe B01–B36 as independent trials or report an overall success rate.

## Move 3 — primary finding (C2)

This is the first result the reader should remember:

> the build–validate backbone remains stable, while the required operator portfolio broadens as reconstruction dependencies accumulate.

Give 2–3 concrete transitions, not a list of all task families:

- local domain/pose fitting;
- reusable master versus site-specific boundaries;
- ports/routes/flexible paths and omission-driven task selection;
- late review/interference constraints.

Use "the historical sequence shows" or "the documented workflow adds" rather than causal language such as "complexity causes."

## Move 4 — mechanism / systems interpretation (C1 + C3)

State both in compressed form:

- metric computation and acceptance are performed by deterministic operators;
- the model's observable contribution is problem formulation, representation/decomposition, and program revision;
- persistent external state lets later tasks reuse prior assets/endpoints while exposing the process to propagated abstraction errors.

One concrete fact is enough: e.g. B36 preserves 36,615 prior objects and 7,114 station transforms while adding new connected geometry. Treat this as state-preservation evidence, not accuracy.

## Move 5 — boundary

One sentence:

- single site;
- no matched alternative-model baseline;
- no independent survey reference for the complete station;
- results characterize one longitudinal field record rather than a general benchmark.

## Abstract content that should not appear

- D37/D38/D40/D41;
- script / manifest / JSON counts;
- global 1,550-record median as a station-accuracy headline;
- selected failure-frequency percentages;
- a sequence of six or seven batch anecdotes;
- "fully autonomous";
- "GPT-6 Astra achieves centimeter-level accuracy."

---

# 3. Introduction — SCQA, then answer preview

Target: **~1.25 pages**. Approximately 6 paragraphs. The reader should know the paper's answer before reaching Related Work.

## Paragraph 1 — Situation: what current reconstruction gives

**Function:** establish shared context.

Start from the common capability of photogrammetry / scene reconstruction: a registered surface or scene representation can recover occupied geometry and appearance.

Do not start with Astra, the substation, object counts, or project history.

## Paragraph 2 — Complication: why engineering reconstruction is different

**Function:** establish the research gap.

An editable engineering model requires more than surface recovery:

- explicit component decomposition;
- repeated structure and variants;
- finite site-specific connections;
- connectivity / path continuity;
- an editable state that survives later work;
- geometry-specific validation.

The key complication is **heterogeneity of the decisions**, not simply scale.

## Paragraph 3 — Why a reasoning model is relevant

**Function:** motivate the method class without claiming success yet.

A single fixed numerical primitive is unlikely to decide all of the following:

- which source region corresponds to a component;
- whether geometry should be rigid, reusable, finite, or flexible;
- whether two structures belong in one reusable master;
- which existing endpoints should be connected;
- which residual geometry should become the next task.

This motivates a general reasoning layer that can author and revise explicit programs while leaving numerical computation to deterministic tools.

## Paragraph 4 — Research question

State one primary question only:

> **Can a general-purpose reasoning model coordinate a persistent industrial 3D reconstruction process through executable geometry tools, and how does the required decision/operator set change as reconstructed elements become more interdependent?**

A secondary systems question may be stated in the same paragraph, not promoted to a separate RQ hierarchy:

> How can accepted local reconstructions remain reusable as the site model grows, and what risks does this persistence introduce?

## Paragraph 5 — Study design and answer preview

Introduce B01–B36 as a sequential field record and give the answer immediately:

- same evidence–program–validation backbone;
- operator portfolio broadens with dependency structure;
- model formulates/revises operations, deterministic tools compute/check;
- persistent external state enables composition and propagates shared-abstraction errors.

This paragraph should make Figure 1 understandable.

## Paragraph 6 — Contributions

Exactly **three** contributions, each corresponding to something the paper later proves:

1. **Persistent programmatic reconstruction formulation.** Industrial reconstruction is represented as a loop over physical evidence, model-authored executable geometry operations, task-specific validation, and inherited engineering state.
2. **Longitudinal B01–B36 field study.** Thirty-six sequential reconstruction batches span local fitted structures, reusable equipment, connected conductor/bus systems, and civil/auxiliary closure while preserving prior state and review evidence.
3. **Cross-sequence analysis.** The record shows a stable build–validate backbone with a broadening operator/decision portfolio, and documents how persistent state enables cross-batch composition while making upstream abstraction errors consequential.

Do not list final object count, review HTML pages, human correction, failure recovery, or semantics as separate contributions.

---

# 4. Related Work — three paragraphs plus the gap

Target: **0.75–1 page**. Prefer three dense subsections or four paragraphs; do not write an encyclopedic survey.

## 4.1 Structured reverse engineering

Use Point2CAD, CAD-Recode, and adjacent structured/CAD reconstruction work.

**Reader function:** establish that converting sampled geometry into editable structure is itself a reconstruction problem.

**Contrast:** those systems usually solve a fixed object-scale mapping. AstraBuild studies a heterogeneous site sequence in which representation, operator, and prior state vary by task.

## 4.2 LLMs for procedural 3D construction

Use 3D-GPT and SceneCraft.

**Reader function:** establish the precedent for language/reasoning models producing executable 3D programs.

**Contrast:** those works predominantly map language or scene specifications into generated content; AstraBuild works backward from registered physical evidence and must maintain compatibility with previously accepted geometry and connections.

## 4.3 Long-horizon tool-use systems

Use Voyager / GPT-Policy as conceptual precedents for executable actions, feedback, reuse, and persistent task context.

**Reader function:** explain why a sequence of programmatic actions and external state is a relevant systems formulation.

Avoid claiming direct equivalence to embodied control.

## Closing gap paragraph

End with one explicit gap statement:

> Existing work separately demonstrates structured 3D reverse engineering, procedural 3D program generation, and long-horizon tool use. The B01–B36 record studies their interaction in one industrial setting: a general-purpose model repeatedly converts physical evidence into executable reconstruction operations while inheriting a growing editable engineering state.

---

# 5. Method — explain attribution, not every historical detail

Target: **1.25–1.5 pages**. Three subsections plus one short worked trace.

The Method should let a skeptical reader answer: what goes into the model, what decisions are attributed to it, what is computed outside it, and what persists between tasks?

## 5.1 Evidence and persistent engineering state

### Inputs available to a batch

- registered photogrammetric geometry / local coarse reference;
- field imagery;
- inventory or engineering records when useful;
- accepted assets, transforms, terminals, and scene state from earlier batches.

### Persistent outputs

- editable Blender geometry;
- reusable collections / masters and site instances;
- site-specific connections;
- measurement/diagnostic artifacts;
- validators and preservation/provenance records.

One equation is optional, but only if it simplifies the concept. Do not build a heavy formalism around `S_t` unless it is actually used later.

## 5.2 Model decisions versus deterministic execution — C1

This is the conceptual center of Method.

### Observable model/harness decisions

- choose relevant evidence and spatial domain;
- choose representation (rigid component, shared master, finite segment, curve/path, etc.);
- decompose the reconstruction task;
- author or revise Blender/Python procedures;
- select or introduce measurement, routing, coverage, review, or collision operators;
- interpret validator/review outputs to decide what to revise.

### Deterministic operations

- least-squares / geometric fitting;
- coordinate transforms;
- spline/profile computation;
- mesh construction and rendering;
- distance, contact, endpoint, continuity, and collision checks;
- history/hash/state-preservation checks.

Mandatory attribution sentence:

> **Quantitative residuals in this study measure the output of explicit geometry procedures selected and executed within the workflow; they should not be interpreted as the language model directly performing numerical optimization.**

## 5.3 Persistent reconstruction loop

Use one simple loop only:

`physical evidence + prior accepted state → formulate operation → execute deterministic geometry program → review/validate → retain or revise state`

Clarify:

- validators are task-specific rather than one universal accuracy metric;
- accepted outputs become available to later batches;
- historical versions are preserved rather than silently overwritten.

Do not show the directory tree or all artifact types here.

## 5.4 Worked trace: B23 as the method in miniature

Target: **~0.4 page + one compact figure panel**.

Sequence:

1. inherited preflight treated the neutral connection as a straight two-end problem;
2. registered source profile shows a roughly 0.5 m mid-span bow;
3. the operation is reformulated as a curved path with fixed endpoints;
4. deterministic binning / control-point extraction / cubic B-spline computation produces the path;
5. saved geometry is checked against finite source domains and endpoint/contact constraints;
6. later revisions add soft leads / bridge contact where the first revised representation still misses physical structure.

The scientific purpose is not "B23 was difficult." It is to make C1 concrete: **representation choice and numerical fitting are different layers of the workflow.**

---

# 6. Study Design — orient once, then move to Results

Target: **0.75–1 page**.

## 6.1 B01–B36 reconstruction sequence

State positively what the study is:

- 36 sequential reconstruction batches at one operating substation;
- later batches inherit accepted earlier state;
- targets span equipment, connections, conductors, civil structures, and auxiliary infrastructure;
- the sequence records changing task structure rather than repeated trials of one fixed task.

One sentence is sufficient to explain why there is no overall success-rate denominator:

> Because geometry types, dependencies, and task-specific validators vary across the sequence, the analysis compares reconstruction structures and operator use rather than collapsing all batches into a single success rate.

Do not introduce IID terminology unless a reviewer later asks for it.

## 6.2 Task spectrum as orientation, not a taxonomy claim

Use **Table 1** with four descriptive bands. Do not call them discovered regimes.

| Descriptive band | Batches | Representative targets | Structural issue introduced |
|---|---|---|---|
| Local fitted structures | B01–B06 | arresters, wall, gate | comparison/fit domain and rigid geometry |
| Repeated equipment | B07–B19 | transformers, capacitors, GIS | reuse, variants, master/site boundaries |
| Connected systems | B20–B30 | busbars, insulators, jumpers, conductors | ports, routes, topology, flexible paths, coverage gaps |
| Site closure | B31–B36 | buildings, cabins, ground, auxiliaries, bus racks | residual structure under a large inherited state |

Important: this table helps the reader navigate chronology. The scientific claims are not "there are four regimes."

## 6.3 Evidence forms used in Results

Define only recurring evidence:

- fixed-camera reference / clean / overlay views;
- local surface comparisons with explicit scope;
- endpoint / contact / route checks;
- selected-region unexplained-geometry coverage;
- prior-state preservation checks.

The website can expose the full review/dossier archive; the paper uses selected evidence only.

---

# 7. Results — the claim pyramid becomes the paper

Target: **4–4.5 pages**. This is the center of the manuscript.

Do **not** create a standalone "task breadth" result. Breadth has already been established in Study Design and representative figures. Results should answer the two substantive questions: what additional decision layers appear, and how does persistent state make the sequence compositional?

---

## 7.1 The reconstruction loop broadens beyond local fitting — C2 overview

### Reader question

What changes across B01–B36 if the build–validate loop itself remains recognizable?

### First paragraph: answer immediately

> **Local fitting never disappears, but the documented workflow accumulates additional operator families as reconstruction becomes more relational: reuse boundaries, explicit ports and routes, flexible path representations, unexplained-geometry coverage, fixed-view review, and late interference checks.**

This should be the main analytical result, not buried after case studies.

### Main evidence: Figure 3, operator-evolution map

Create a **B01–B36 × operator-family heatmap**.

Recommended y-axis families:

- extract / local evidence preparation;
- fit / measure;
- inspect / diagnose;
- plan;
- refine;
- audit / validate;
- review;
- connection / route / feature operations;
- coverage / discovery;
- collision/interference.

Design rules:

- show batch chronology left to right;
- include a thin target-family band above the heatmap;
- annotate only 6–8 transition batches (B01/B02, B08, B15, B20, B23, B25/B26, B29, B36);
- do not convert filename-derived counts into statistical significance;
- use the heatmap as descriptive orientation, then ground each interpretation in direct artifacts.

### Quantitative/descriptive support

Only a few regime-level contrasts are needed in prose:

- B01–B06: `fit` 6/6; no explicit `measure`, `plan`, `refine`, or `audit` scripts; no original review HTML pages.
- B07–B19: measurement, planning, refinement, audit, and review become recurring.
- B20–B30: explicit inspection/planning and route/connectivity/coverage artifacts appear.
- B31–B36: measurement and fixed-view review remain common; B36 adds interference/collision handling.

Label these as **descriptive workflow records**, not performance metrics.

### Interpretation paragraph

The sequence is not explained by repeatedly applying one primitive to more objects. The key observation is **operator accumulation**: local geometric machinery continues to be used, while new relationship-level constraints become necessary.

Bridge to 7.2: the heatmap shows *that* the operator portfolio broadens; three transition cases show *why*.

---

## 7.2 Three transitions explain why new decision layers are needed — C2 mechanism

This should be the longest subsection. Organize by **three transitions**, not by 36 batches and not by four task bands.

### 7.2.1 From fitting geometry to defining reusable scope — B01/B02 → B08/B15

#### Reader question

What new problem appears when one reconstruction must represent repeated physical equipment rather than one local object?

#### Evidence step 1 — B01/B02 establishes the local-fit baseline

Use only enough detail to establish the baseline:

- B01 broad support-source domain mixes shaft and accessory surfaces, causing the chosen 5 cm screen to fail for two candidates;
- B02 changes the fitting/validation domain rather than simply optimizing the same objective harder;
- numerical fitting is deterministic after the domain is specified.

Takeaway: early work is dominated by **what local geometry should be compared and fit**.

#### Evidence step 2 — B08 introduces reuse as an engineering decision

- explicit user equivalence authorization for T1/T2 component configuration;
- one `B08_TRANSFORMER_MASTER`, two rigid site roots;
- site-specific leads remain outside the shared master;
- shared-edit propagation is validated.

Takeaway: the question changes from "what are this object's dimensions?" to **"which geometry is invariant across installations, and which belongs to the site?"**

#### Evidence step 3 — B15 shows the reuse boundary can be wrong

- common ±3.3 m bus-spool extents overlap neighboring installations;
- revision removes finite site-dependent spool geometry from the reusable master;
- finite site wrappers/segments are reconstructed separately;
- historical geometry is preserved rather than overwritten.

Takeaway: the reuse boundary is not a software convenience. It is a **falsifiable engineering representation choice**.

#### Subsection conclusion

> Repetition introduces abstraction as a reconstruction variable: the system must decide not only geometry parameters, but also the boundary between reusable manufactured structure and site-specific installation geometry.

### 7.2.2 From object geometry to connected representations — B20 → B23 → B29

#### Reader question

What changes once a geometrically plausible component must connect correctly to previously modeled equipment?

#### B20 — explicit ports and routes

- build a port inventory from actual existing equipment ends;
- plan neighboring intervals;
- distinguish already connected sections, new straight spans, and the 4100 route that requires a turn;
- geometric connection is explicitly separated from electrical identity.

Takeaway: independent object fit is insufficient; **relationship constraints become first-class.**

#### B23 — representation class becomes part of the decision

- straight-end preflight misses the middle of the physical trajectory;
- profile evidence exposes the bow;
- connection is reformulated as a curved path;
- deterministic spline fitting and endpoint checks follow.

Takeaway: some errors cannot be solved by tuning parameters inside the wrong representation.

#### B29 — connected constraints scale across subsystems

- strain strings, jumpers, and crossyard conductors connect to existing clamps, suspension ends, and transformer-derived lead endpoints;
- endpoint continuity is validated separately from coarse-surface similarity;
- some surface domains remain poor because they contain branches/attachments not represented by a single conductor.

Takeaway: **topological/endpoint validity and local surface fit are different engineering criteria.**

#### Subsection conclusion

> When components interact, reconstruction becomes a problem of satisfying relationships among existing objects—ports, paths, continuity, and representation—not merely matching each object to a local surface.

### 7.2.3 From scheduled additions to gap-driven site closure — B25/B26 → B31–B36

#### Reader question

How does task selection change when many major devices already exist and the remaining problem is an incomplete site model?

#### B25/B26 — unexplained geometry becomes a task signal

- compare registered high-region geometry to the current model;
- large unexplained structures reveal missing gantries/firewalls that inventory-style completion would not necessarily prioritize;
- selected high-region medians / >1 m gap fraction fall after reconstruction;
- explicitly state that this is a selected-region coverage diagnostic, not whole-site completeness.

Takeaway: coverage becomes **an additional task-selection signal**, not a universal planner objective.

#### B31/B32/B35 — civil/auxiliary closure under accumulated context

Use brief corroboration, not separate stories:

- large building/cabin geometry is measured and reviewed against the registered source;
- reusable subcomponents remain possible, but photos and local diagnostics are needed where coarse geometry is incomplete;
- B35 explicitly limits the endpoint to the visible outdoor model, excluding hidden/underground and uncertain details.

#### B36 — late interference constraint

- adds remaining transformer-side bus-rack structures without changing B08 transformer assemblies;
- route endpoints remain tied to existing terminals/wall interfaces;
- one segment is moved by up to 0.16 m to avoid an existing fire riser while preserving measured endpoints/support route;
- prior state is simultaneously protected.

Takeaway: late tasks are constrained by **what already exists**, not simply by source geometry.

#### Subsection conclusion

> Near site closure, the problem expands from reconstructing a target object to choosing residual work and inserting it into an already populated engineering world without breaking existing relationships.

### Figure 4 — three transition panels

Use one figure with three horizontal stories:

1. **domain → abstraction:** B01/B02 + B08/B15;
2. **object → connected representation:** B20/B23/B29;
3. **addition → gap-driven closure:** B25/B26 + B36.

Each panel should show **evidence → decision change → resulting representation**, not decorative final renders.

---

## 7.3 Persistent external state composes local solutions and propagates abstraction errors — C3

### Reader question

What makes the sequence long-horizon in an engineering sense?

### First paragraph: answer immediately

> **Later batches do not merely coexist with earlier outputs; they explicitly reuse earlier masters, transforms, terminals, and connection endpoints while validators protect inherited state. This creates a compositional reconstruction process, but it also means that errors in shared representations can propagate until revised.**

### Positive evidence: dependency chain

Use one explicit chain rather than the final object count alone:

`B08 transformer master/terminal state → B23 transformer-connected leads → B29 crossyard conductors using earlier endpoints → B36 bus-rack/wall closure tied back to B08 stubs`

For each node, use one sentence and one concrete dependency:

- **B08:** one shared transformer master, T1/T2 rigid site instances, site-specific leads outside the master.
- **B23:** curved neutral lead terminates at an existing B08 transformer terminal port; B08 geometry is reused rather than rebuilt.
- **B29:** new conductors connect to existing suspension/clamp geometry and transformer-derived lead ends.
- **B36:** new main busbars are checked against existing B08 terminal stubs and wall bushings; existing short terminal bars remain intact.

### Preservation evidence

Use only endpoint snapshots, not a long table of every batch:

- B08 preserves 21,459 earlier objects;
- B23 preserves 28,246 earlier objects and 2,192 protected files;
- B31 preserves 33,223 earlier objects and 7,113 station transforms;
- B36 preserves 36,615 earlier objects, 7,114 station transforms, and 2,798 protected files while the file reaches 36,812 objects.

State explicitly: these are **engineering-state preservation descriptors**, not physical-asset counts or accuracy metrics.

### Negative evidence: B15 propagation risk

Return to B15, but do not retell the whole case:

- a finite site-dependent spool is placed inside a shared abstraction;
- the abstraction propagates inappropriate extents across installations;
- recovery requires revising the master/site boundary.

Interpretation:

> Persistent external state creates both **compositional leverage** and an **error-propagation surface**.

### Figure 5 — dependency graph + preservation endpoint

Left: dependency graph B08 → B23 → B29 → B36.

Right: B36 station view with compact preservation descriptors.

Inset: B15 as the negative edge, showing why inherited abstractions require validation/provenance.

Do not use another assembly video or a second station-scale hero figure.

---

# 8. Discussion — interpret the claims, do not introduce new stories

Target: **~1 page**.

## 8.1 What general reasoning contributes in this record

Answer C1/C2 together:

> The useful role of the general model is not replacing geometric solvers. It is translating heterogeneous physical evidence into explicit, revisable engineering operations: defining domains, choosing representations, deciding reuse boundaries, identifying relational constraints, selecting specialized operators, and authoring the executable procedures that implement them.

Then note that the operator portfolio broadens rather than local fitting disappearing.

## 8.2 Why explicit tools and validation are part of the scientific result

Explain why the workflow remains inspectable:

- numerical outputs come from explicit code;
- review/validation can contradict the current representation;
- accepted state can be retained while the local operation is revised;
- B01/B02, B15, and B23 are enough as brief evidence references.

Do not create another failure-analysis section.

## 8.3 Persistent state changes both capability and risk

Interpret C3:

- later tasks gain access to a structured engineered world, not a blank scene;
- this enables explicit reuse of terminals, masters, and prior connections;
- errors in reusable abstractions become system-level rather than local.

No claim that persistence improves accuracy relative to a stateless baseline.

## 8.4 Limitations and threats to validity

Keep all broad caveats together:

- one site;
- one model/harness configuration;
- no matched alternative planner/model baseline;
- no independent survey reference for the complete station;
- task sequence is historical and state-dependent rather than controlled by difficulty;
- operator prevalence is reconstructed from preserved scripts/files, not a standardized action log;
- human review/user authorization affects some decisions (e.g. B08 equivalence); therefore the system is agent-driven and human-steerable, not fully autonomous;
- coarse-reference residuals are not survey accuracy;
- visible/outdoor closure does not imply hidden/underground completeness.

## 8.5 What the next controlled study should test

Prioritize four experiments:

1. matched alternative-model runs on a small representative subset (local fit, reusable abstraction, connected path, site closure);
2. selected independent survey measurements;
3. a second site;
4. explicit logging of model calls, human interventions, runtime, and tool invocations.

This paragraph should make clear which present claims are descriptive and which future experiments could support causal/comparative claims.

---

# 9. Conclusion — one paragraph, three statements

Target: **120–160 words**.

Logical order:

1. **Answer the question:** B01–B36 documents a persistent, programmatic industrial reconstruction process operated through one general reasoning model plus deterministic geometry tools.
2. **State the main result:** the sequence does not scale by repeating one fitting primitive; additional decision/operator layers appear around reuse boundaries, connected representations, task selection, review, and interference as dependencies accumulate.
3. **State the systems implication and boundary:** persistent state lets accepted local solutions compose across later tasks while making abstraction errors consequential; controlled multi-model, survey, and cross-site studies are still required.

Do not repeat object count, residual median, or a list of batches.

---

# 10. Main-paper figure and table plan

The figure budget should reflect claim priority. C2 receives the most visual space.

## Figure 1 — Problem, method, and answer at a glance

**Location:** end of Introduction.

**Reader should understand in <10 seconds:**

`registered physical evidence + prior engineering state → reasoning model chooses/revises operation → deterministic geometry tools → validated editable state`

Below the loop, show the three classes of decisions that appear in the paper:

`local geometry → reusable/connected representation → accumulated-state integration`

Do not show filesystem details or every validator.

## Figure 2 — B01–B36 longitudinal study map

**Location:** Study Design.

One chronological strip with:

- B01–B36;
- four descriptive target bands;
- 8 anchor batches only: B01/B02, B08, B15, B20, B23, B25/B26, B29, B36;
- small representative thumbnails if space permits.

Purpose: orientation, not proof.

## Figure 3 — Operator portfolio across the sequence

**Location:** 7.1.

This is the **central analytical figure**.

Batch × operator heatmap + target-family band + transition annotations.

Caption must state:

- based on preserved stage/script artifacts;
- descriptive rather than standardized action telemetry;
- absence of a named stage does not imply task failure or absence of reasoning.

## Figure 4 — Why the operator portfolio broadens

**Location:** 7.2.

Three transition panels:

- B01/B02 → B08/B15: local fit to reuse boundary;
- B20/B23/B29: object geometry to connected representation;
- B25/B26 → B36: unexplained geometry to state-constrained closure.

Each panel: **evidence → changed decision → changed representation/operator**.

This figure should use process artifacts (`measurement_profiles`, route diagnostics, plan overlays) rather than only final clean renders.

## Figure 5 — Persistent state as composition mechanism and risk surface

**Location:** 7.3.

Dependency graph:

`B08 → B23 → B29 → B36`

plus B15 as a negative reuse-boundary example and a compact B36 preservation summary.

## Optional Figure 6 — Representative visual reconstruction breadth

Only include if venue/page budget allows.

2×3 `Reference / Clean / Overlay` examples from B06, B08, B10, B17, B23, B32.

This figure supports feasibility/breadth but is lower priority than Figures 3–5. If the paper is space-constrained, move it to supplement/website.

## Table 1 — Study orientation

Four descriptive target bands, representative batches, reconstruction target, new structural issue.

## Table 2 — Selected task-native evidence

Maximum **6–8 rows**. Every row must name metric scope. Candidate rows:

- B01/B02 local domain comparison;
- B06 heldout wall-face distance;
- B08 shared master + scoped exterior-bank holdout;
- B15 endpoint/finite spool checks;
- B23 curved path surface + endpoint checks;
- B25/B26 selected high-region coverage change;
- B29 endpoint continuity with explicit surface-domain caveat;
- B36 state preservation + endpoint/interference checks.

Do not include a global "accuracy" column.

---

# 11. Material hierarchy — what belongs where

## Main-text anchors

These batches carry the scientific argument:

- **B01/B02** — problem/domain formulation;
- **B08** — reusable equipment abstraction;
- **B15** — abstraction boundary failure/revision;
- **B20** — explicit ports/routes and system connection;
- **B23** — representation change, worked method example;
- **B25/B26** — omission/coverage as task-selection signal;
- **B29** — endpoint/topology composition across prior systems;
- **B36** — inherited-state closure and interference-aware integration.

## Main-text corroboration / figures

- B06 — clean local civil fitting;
- B10 — repeated capacitor assemblies;
- B17/B19 — complex GIS reuse / connection scale;
- B31/B32 — civil/cabin reconstruction under incomplete coarse evidence;
- B35 — visible outdoor closure boundary.

## Supplement / website evidence browser

Everything else:

- complete B01–B36 batch list;
- all review HTML pages;
- all clean/overlay/reference triplets;
- full process dossiers;
- complete metric ledger;
- revision files;
- manifests / script counts;
- extra videos;
- detailed implementation failures.

The website can be richer than the paper. The paper should remain an argument.

---

# 12. Claim-to-section alignment matrix

| Claim | Introduced | Method support | Main Results support | Discussion interpretation | Boundary |
|---|---|---|---|---|---|
| C1: model formulates/revises; deterministic tools compute/check | Intro ¶3–5 | §5.2 + B23 trace | used to interpret all numeric evidence | §8.1–8.2 | no planner/tool ablation |
| C2: operator/decision portfolio broadens with dependency | Intro ¶4–6 | loop permits task-specific operators | §7.1–7.2; Figs. 3–4 | §8.1–8.2 | retrospective/descriptive, not causal learning claim |
| C3: persistent state enables composition and propagates abstraction errors | Intro ¶5–6 | §5.1/5.3 persistent state | §7.3; Fig. 5 | §8.3 | no stateless baseline, no necessity/accuracy-gain claim |

A central statement should not appear in the Abstract unless it has a row in this table and direct evidence in Results.

---

# 13. Paragraph-level writing contracts for the Results

Use the same reader rhythm throughout Results:

1. **Answer sentence** — state the narrow claim before details.
2. **Evidence** — introduce the minimum batch evidence needed.
3. **Mechanism/interpretation** — explain why the evidence supports the claim without inventing an internal model mechanism.
4. **Counterexample or boundary** — show what the claim does not cover when relevant.
5. **Bridge** — explain why the next dependency level matters.

Example for B15:

- Function: show that reuse boundary is a reconstruction decision.
- Claim: finite site geometry cannot always be placed in a reusable equipment master.
- Evidence: common ±3.3 m spools overlap neighbors; revision moves finite geometry to site scope.
- Development: reuse is therefore an engineering hypothesis about invariance, not merely code deduplication.
- Boundary: this does not quantify the efficiency benefit of reuse.
- Bridge: once site-specific geometry is separated, later connected-system tasks can reason about actual finite endpoints.

Do not turn each case into a dramatic anecdote with its own moral.

---

# 14. Reviewer red-team before prose drafting

## Challenge A — “The operator heatmap is just your filenames.”

Required response in the manuscript:

- explicitly call it a descriptive reconstruction of preserved workflow artifacts;
- do not use statistical language;
- ground every important transition in direct plans, diagnostics, validation records, and geometry dependencies;
- treat Figure 3 as orientation, Figure 4 as substantive evidence.

## Challenge B — “Maybe the scripts, not Astra, did everything important.”

Required response:

- never attribute solver output to the model;
- define the observable model/harness contribution as problem formulation, representation/decomposition, program authoring/revision, and interpretation of external evidence;
- acknowledge no matched alternative planner/model baseline.

## Challenge C — “This is just chronological project scope expansion.”

Required response:

- do not claim the chronology itself proves increasing cognitive difficulty;
- show concrete dependency changes: master/site boundary, ports, flexible paths, inherited endpoints, coverage, interference;
- phrase the result as a **broadening operator/decision portfolio in this documented sequence**, not universal complexity law.

## Challenge D — “Does the sequence show model learning?”

Answer: no.

Use "workflow added," "later tasks required," "the documented sequence contains," not "Astra learned" or "reasoning improved over time."

## Challenge E — “Why is persistence more than software engineering?”

Required evidence:

- later geometry explicitly terminates on prior ports/endpoints;
- shared masters are reused by later tasks;
- validators preserve prior state;
- B15 demonstrates a shared abstraction error propagating across installations.

This establishes that persistence changes the *reconstruction problem*, not merely file organization.

## Challenge F — “Where is accuracy?”

Answer by decomposition, not by one headline:

- local surface checks when meaningful;
- endpoint/contact/continuity for connected systems;
- coverage for omission discovery;
- preservation for long-horizon state integrity.

Explicitly state that there is no complete independent survey reference for station-wide accuracy.

---

# 15. Drafting order

Do not write Abstract first. Use the academic-writing lifecycle and stabilize the evidence chain first.

Recommended order:

1. **§7.2 three transitions** — write the main empirical argument first.
2. **§7.3 persistent state** — establish the system claim.
3. **§7.1 operator overview** — summarize only after the transition evidence is written.
4. **§5 Method** — include only what the Results require.
5. **§6 Study Design** — orient the evidence without adding a second taxonomy.
6. **§8 Discussion / Limitations** — interpret stabilized Results.
7. **§4 Related Work** — sharpen the exact gap around the stabilized contribution.
8. **§3 Introduction** — write SCQA around the actual supported answer.
9. **§9 Conclusion**.
10. **§2 Abstract last**.
11. Title last, after Abstract is stable.

This order reduces the risk of inventing a thesis in the Introduction that the evidence cannot support.

---

# 16. Page and emphasis budget

For an 8–9 page main paper excluding references:

- Abstract: 0.25 page
- Introduction: 1.25 pages
- Related Work: 0.75 page
- Method: 1.25–1.5 pages
- Study Design: 0.75 page
- Results: **3.5–4 pages**
  - 7.1 operator overview: ~0.7 page
  - 7.2 three transitions: **~2.0–2.3 pages**
  - 7.3 persistent state: ~0.9–1.0 page
- Discussion + limitations: 0.9–1.0 page
- Conclusion: 0.2 page

The page budget encodes claim priority. If space must be cut, remove visual breadth and batch detail before cutting §7.2 or §7.3.

---

# 17. Language contract

Prefer direct research statements:

- "B23 reformulates the connection as a curved path after profile evidence exposes a mid-span bow."
- "B15 separates finite site spools from the reusable equipment master after shared extents overlap neighboring installations."
- "B29 validates endpoint continuity separately from coarse-surface similarity."

Avoid assistant/presentation phrasing:

- "What makes this interesting is..."
- "The strongest evidence is..."
- "This is not just X, but Y..."
- "The key takeaway is..."
- "Astra truly understands..."
- "We can clearly see..."

Avoid anthropomorphic internal-state claims unless directly observable. Prefer:

- "the workflow selects / revises / authors";
- "the preserved program changes";
- "the validator reports";
- "the representation is revised".

Use "Astra/Codex" for observable model-in-harness actions and "AstraBuild" for the complete system/process.

---

# 18. One-minute reader retelling test

A reader who remembers the paper correctly should be able to say:

> Photogrammetry gives a registered scene, but an editable industrial model also needs decisions about component scope, reuse, connections, paths, and how new work fits an existing engineered world. AstraBuild studies whether a general reasoning model can coordinate those decisions through explicit geometry programs. Across B01–B36, local fitting remains part of the workflow, but additional operators appear as reconstructed elements become more dependent: reusable-asset boundaries, ports and routes, flexible path representations, coverage-based omission discovery, review, and interference checks. The numerical geometry is computed and validated by deterministic tools; the model's observable role is to formulate and revise those operations. Because accepted geometry, assets, and endpoints persist across batches, later work can connect to earlier work, but B15 shows that incorrect shared abstractions can propagate through the same mechanism.

If the final manuscript requires substantially more than this to explain its contribution, the narrative has become too broad again.

---

# 19. Final outline at a glance

**Abstract**

**1. Introduction**  
1.1 Surface reconstruction versus engineering reconstruction  
1.2 Why heterogeneous reconstruction motivates a reasoning/orchestration layer  
1.3 Research question, answer preview, and three contributions

**2. Related Work**  
2.1 Structured 3D/CAD reverse engineering  
2.2 LLM-based procedural 3D construction  
2.3 Long-horizon tool-use systems

**3. AstraBuild Method**  
3.1 Evidence and persistent engineering state  
3.2 Model decisions versus deterministic geometry operations  
3.3 Persistent evidence–program–validation loop  
3.4 B23 worked trace

**4. Study Design**  
4.1 B01–B36 reconstruction sequence  
4.2 Task spectrum as descriptive orientation  
4.3 Evidence forms and task-native validation

**5. Results**  
5.1 The reconstruction loop broadens beyond local fitting  
5.2 Three transitions explain why new decision layers are needed  
 5.2.1 Fit domain → reusable scope: B01/B02, B08, B15  
 5.2.2 Object geometry → connected representation: B20, B23, B29  
 5.2.3 Scheduled addition → gap/state-driven closure: B25/B26, B31–B36  
5.3 Persistent external state composes local solutions and propagates abstraction errors

**6. Discussion**  
6.1 What the general model contributes  
6.2 Why explicit tools and validation matter  
6.3 Persistent state: capability and risk  
6.4 Limitations / threats to validity  
6.5 Controlled follow-up studies

**7. Conclusion**

**Supplement / website evidence browser**  
All B01–B36 reviews, process dossiers, full metric ledger, manifests, revisions, and additional videos.
