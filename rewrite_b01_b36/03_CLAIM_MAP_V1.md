# Claim Map v1 — B01–B36 evidence-grounded refinement

## Purpose

This document refines the paper's claims before prose drafting. It uses **B01–B36 only** and treats later D-series work as outside the main empirical boundary.

The goal is not to maximize the number of claims. The goal is to identify the smallest set of claims that (a) a reader can remember, (b) are directly supported by the preserved engineering record, and (c) jointly answer one scientific question.

---

# 1. Recommended top-level thesis

## Recommended thesis

> **AstraBuild is best understood as a persistent orchestration system rather than a monolithic 3D generator. Across B01–B36, a stable evidence–program–validation backbone is augmented with task-specific geometry operators as reconstruction dependencies grow, while persistent external state allows locally reconstructed components to be reused and connected across later tasks.**

A second sentence can state the model/tool division:

> **Metric estimation and acceptance are externalized to deterministic geometry code and validators; the model's observable contribution is to select evidence, choose representations and decomposition, and author or revise the programs that invoke those operators.**

This formulation is stronger than “Astra built a large substation” because it states a system-level scientific interpretation. It is safer than “GPT-6 Astra learned to reconstruct increasingly complex systems” because B01–B36 is one sequential field record, not a controlled learning study.

## What the thesis does NOT claim

- no claim that GPT-6 Astra is better than another model;
- no claim that the task sequence demonstrates in-context learning or skill acquisition;
- no claim that operator changes were caused by task complexity in a controlled statistical sense;
- no claim that centimeter-scale residuals are independent survey accuracy;
- no claim that persistence improves accuracy relative to a stateless baseline;
- no claim of autonomous reconstruction.

---

# 2. The claim pyramid

The main paper should have **three supporting claims**.

## Claim 1 — Geometry computation is externalized; the model orchestrates the engineering problem

### Reader question

What is GPT-6 Astra actually contributing? Is it doing geometric optimization itself, or is it coordinating conventional geometry code?

### Canonical claim

> **In the documented B01–B36 workflow, metric estimation and acceptance are performed by explicit deterministic operators. The model's observable role is to select evidence and comparison domains, choose or revise geometric representations, decompose tasks, and author or revise programs that invoke those operators.**

### Why this is defensible

The historical record does not preserve private chain-of-thought, so the paper should make claims only about observable actions and artifacts. Those artifacts repeatedly separate two layers:

1. **problem formulation / program authoring** — selection of source regions, representation, decomposition, and code;
2. **deterministic computation / validation** — least squares, profile fitting, coordinate transforms, rendering, surface distances, endpoint/contact checks, collision checks, history checks.

### Strong evidence

#### B01 → B02: the numerical result depends on how the problem is defined

- B01 broad cylindrical holdout domains contain accessory protrusions and produce RMS values 4.84 / 7.32 / 5.10 cm, with two of three candidates failing the 5 cm internal screen (`CONTINUE_FROM_B01.md`, lines 77–88).
- B02 does **not** simply optimize the same objective harder. It defines bare-shaft fitting and validation domains and explicitly states that the revised values are not an apples-to-apples accuracy improvement (`CONTINUE_FROM_B02.md`, lines 27–31).
- Scientific relevance: the engineering decision is partly **what to measure**, not only the resulting fitted parameters.

#### B06: line fitting is numerical; domain/model formulation is the higher-level task

- wall headings are fit to inward-facing vertical triangles, with alternate 2 m strips held out (`CONTINUE_FROM_B06.md`, lines 8–21);
- the model uses the wall inward face rather than the centerline and preserves observed endpoints rather than inventing unobserved perimeter sections;
- numerical heldout changes are produced by explicit fitting code, not by an LLM estimating the final angles numerically.

#### B23: representation selection precedes deterministic path fitting

- B22's inherited preflight considered only a straight two-end region;
- B23 inspection finds a roughly 0.5 m lateral bow in the registered source;
- the final path uses binned control points, a cubic B-spline, fixed endpoints, and a smoothness penalty (`CONTINUE_FROM_B23.md`, lines 15–19);
- the validator then evaluates the saved finite geometry (`B23_validation.json`).

The important model-side decision is not the numerical coefficients of the spline; it is that the connection should be represented and solved as a curved path rather than as a straight segment.

#### B25/B26: deterministic coverage computation informs a higher-level modeling decision

- B25 evaluates millions of registered coarse triangles against the current scene and reveals large unexplained high structures (`CONTINUE_FROM_B25.md`, lines 5–9);
- B25/B26 then reconstruct major gantries/firewalls, reducing selected high-region distances (`CONTINUE_FROM_B25.md`, lines 15–23; `CONTINUE_FROM_B26.md`, lines 17–23).

Again, the distance field is computed deterministically. Its value to the agentic process is that it changes **what should be modeled next**.

### Scope limit

This evidence supports a **division-of-labor description**, not an ablation claim. There is no controlled run in which the same model operates without SciPy/Blender/validators, and no run in which another planner controls the same tools.

### Safe paper wording

> “The reconstruction record separates high-level problem formulation from numerical geometry. Astra/Codex authors and revises executable procedures that select evidence, representations, and task-specific operators; numerical fitting and acceptance checks are performed by deterministic code.”

### Wording to avoid

- “Astra achieves centimeter-level geometric reasoning.”
- “GPT-6 Astra computes accurate geometry directly.”
- “The LLM is responsible for the 3.6 cm residual.”
- “Astra outperforms classical fitting methods.”

### Role in the paper

This is primarily a **method + interpretation claim**. It should explain how to read all later quantitative results.

---

# 3. Claim 2 — The operator portfolio broadens as reconstruction dependencies accumulate

## Reader question

Why does this need an agentic workflow instead of repeatedly running one fitting algorithm on different objects?

## Important refinement relative to Outline v0

Do **not** say that the model's role monotonically “moves upward” and replaces local fitting. Local fitting remains important even in B25–B36. The defensible observation is that **additional decision layers appear while the local geometric machinery remains**.

## Canonical claim

> **Across the B01–B36 sequence, local fitting remains part of the workflow, but the required operator portfolio broadens as reconstructed elements become more interdependent: repeated equipment introduces reusable-asset boundaries; connected systems introduce ports, routes, flexible paths, and topology constraints; coverage analysis introduces omission-driven task selection; late-stage integration adds large-state preservation and interference checks.**

A more model-centered version, for Discussion rather than Results:

> **The observable model-side decisions therefore broaden from local domain and pose specification to abstraction, representation, connectivity, task selection, and integration.**

## Systematic evidence from the process catalog

Filename-level stage audit over **B01–B36**:

- `build`: 36/36
- `validate`: 36/36
- `prepare`: 29/36
- `extract`: 27/36
- `fit`: 13/36
- `measure`: 17/36
- `plan`: 19/36
- `inspect`: 16/36
- `refine`: 16/36
- `audit`: 20/36
- explicit `review` script stage: 10/36
- `collision`: 1/36
- original interactive review pages: 30/36 (B07–B36)

The regime-level pattern is descriptive:

### B01–B06

- `fit`: 6/6
- `measure`: 0/6
- `plan`: 0/6
- `refine`: 0/6
- `audit`: 0/6
- no formal review HTML pages

This is the clearest local-fit regime.

### B07–B19

- `measure`: 8/13
- `plan`: 7/13
- `refine`: 9/13
- `audit`: 10/13
- review pages: 13/13

Reusable equipment families introduce more explicit decomposition, measurement, refinement, and review.

### B20–B30

- `plan`: 8/11
- `inspect`: 8/11
- `refine`: 7/11
- `audit`: 10/11
- review pages: 11/11

This region contains route plans, feature detection, path fitting, endpoint inventory, crossline/jumper fits, and coverage-based completion.

### B31–B36

- `measure`: 6/6
- `inspect`: 5/6
- `plan`: 4/6
- explicit review script stage: 5/6
- one explicit collision stage in B36
- review pages: 6/6

Civil/site closure therefore does not stop using measurement; it adds fixed-view review, large-state preservation, and interference-aware integration.

**Important qualification:** these counts come from script/file naming conventions, not a standardized event log. They support a descriptive operator-evolution figure, not statistical significance or causal attribution.

## Representative evidence chain

### Local domain specification — B01/B02/B06

The main decisions concern reference crops, fit/holdout domains, rigid pose, wall line/face selection, and whether observed or unobserved regions should be modeled.

### Reusable abstraction — B08/B15

B08:

- explicit user authorization allows T1/T2 to share one component configuration;
- both site roots instance the same `B08_TRANSFORMER_MASTER`;
- site-specific leads are kept outside the master (`CONTINUE_FROM_B08.md`, lines 10–28);
- validation confirms one shared master, two rigid roots, and shared edit propagation (`B08_validation_r2.json`, lines 16–35).

B15 provides the counterexample:

- an early common bus-spool assumption uses identical ±3.3 m extents and overlaps neighboring installations (`CONTINUE_B15_IN_PROGRESS.md`, line 21);
- the revision plan removes site-dependent spool geometry from the common master and creates finite site wrappers/segments instead (`CONTINUE_B15_IN_PROGRESS.md`, lines 23–27);
- the final B15 record explicitly states that neighboring site pipe segments and supports are modeled separately rather than folded into common equipment dimensions (`CONTINUE_FROM_B15.md`, lines 10–13).

This is stronger evidence than a generic “reuse saves work” statement. It shows that **the reuse boundary itself is an engineering hypothesis**.

### Connectivity and route structure — B20/B23/B29

B20:

- constructs a `port_inventory` from actual existing equipment ends;
- plans 21 neighboring intervals, distinguishes already connected sections, new straight sections, and one 4100 turn that cannot be solved by straight continuation (`CONTINUE_FROM_B20.md`, lines 9–14);
- explicitly distinguishes geometric connection from electrical identity.

B23:

- changes a connection representation from straight to curved based on measured source trajectory;
- later revisions add missing soft leads and bridge contact rather than treating one global scalar fit as sufficient.

B29:

- reconstructs 60 strain strings, 60 jumper conductors, and 24 main cross conductors;
- endpoints are tied to existing clamps, B28 suspension ends, and existing B08-derived lead endpoints (`CONTINUE_FROM_B29.md`, lines 5–17);
- validators check endpoint continuity independently from surface similarity.

These records demonstrate that once components interact, geometry must satisfy **relationship constraints**, not only individual surface correspondence.

### Omission-driven task selection — B25/B26

B25 explicitly asks where registered high geometry is unexplained by the current model and identifies large gantry omissions. This is qualitatively different from simply taking the next inventory item. B26 continues the same strategy around transformer/firewall regions.

This supports a narrow claim:

> “Coverage analysis became an additional task-selection signal in the later sequence.”

It does **not** support a general claim that coverage-driven planning is superior to inventory-driven planning.

### Late integration — B31–B36

B31/B32 move into large civil structures and use explicit wall/cabin measurements plus fixed review views.

B35 records a near-complete **visible outdoor** model while explicitly excluding hidden/underground and uncertain details (`CONTINUE_FROM_B35.md`, lines 5–17).

B36 then adds missed transformer-side bus racks and introduces a concrete interference correction: a route is shifted by up to 0.16 m to avoid an existing fire riser while endpoint locations are retained (`CONTINUE_FROM_B36.md`, lines 13–25; `B36_validation_r3.json`, lines 676–754).

## Scope limit

The four regime boundaries are an analytical organization imposed after the fact. The batches were not randomized by complexity and the model was not periodically reset. Therefore:

- do not claim a statistically measured “complexity → reasoning level” causal relationship;
- do not claim the model learned these operators over time;
- do not call stage-prevalence counts performance metrics.

## Safe paper wording

> “The historical sequence shows a stable build–validate backbone with a widening set of task-specific operators. Early batches are dominated by local extraction and fitting; later batches additionally require reusable-asset boundaries, route and endpoint reasoning, flexible path representations, coverage analysis, review, and interference checks.”

## Wording to avoid

- “Astra learns increasingly sophisticated reasoning skills.”
- “Task complexity causes the LLM to reason at a higher level.”
- “The operator heatmap proves emergent planning.”
- “Later batches are harder according to a common difficulty scale.”

## Role in the paper

This should be the **main empirical claim** and the center of the Results section.

---

# 4. Claim 3 — Persistent external state is the mechanism for cross-batch composition, and a propagation surface for mistakes

## Reader question

What makes this a long-horizon reconstruction system rather than 36 unrelated Blender jobs?

## Canonical claim

> **Later B01–B36 batches explicitly consume and preserve earlier assets, transforms, ports, and scene state. This persistent external state is the mechanism used to compose local reconstructions into larger connected assemblies; because shared abstractions are inherited, it also makes upstream representation errors consequential until they are revised.**

This claim should be written as a description of the documented mechanism, not as a controlled statement that persistence improves accuracy.

## Strong positive evidence: explicit cross-batch dependency

### B08 creates reusable transformer state

- one `B08_TRANSFORMER_MASTER`;
- T1/T2 are rigid site roots referencing the same collection;
- site-specific leads remain outside the shared master;
- validation checks shared-edit propagation and preserves 21,459 prior objects (`B08_validation_r2.json`, lines 8–35).

### B20 consumes prior equipment ports

B20 constructs bus connections from actual existing ends from B17/B19/earlier equipment rather than rebuilding those devices (`CONTINUE_FROM_B20.md`, lines 9–16).

### B23 consumes B08 transformer terminals

B23's curved neutral lead terminates at the real `B08 front_small` terminal port (`CONTINUE_FROM_B23.md`, lines 15–19). The B08 transformer geometry is not duplicated or independently reconstructed.

### B29 consumes earlier conductor and transformer endpoints

B29 routes new main cross conductors to existing B08-derived lead ends and B28 suspension geometry (`CONTINUE_FROM_B29.md`, lines 7–17).

### B36 closes a later connection onto B08 and building-side geometry

B36 endpoint checks explicitly compare each new main busbar against existing B08 terminal stubs and new wall bushings; saved endpoint gaps are on the order of 1e-7 m (`B36_validation_r3.json`, lines 676–713). The record also says existing B08 short terminal bars remain intact (lines 746–754).

This B08 → B23/B29/B36 dependency chain is a stronger long-horizon argument than simply reporting the final object count.

## Strong positive evidence: preservation is actively validated

Representative checkpoints:

- B08: 21,459 original objects preserved;
- B15: 24,531 R1 objects and 954 protected prior files preserved;
- B23: 28,246 previous objects, 3,301 current-station world transforms, and 2,192 protected files preserved;
- B25: 28,693 old objects and 2,783 active world transforms preserved;
- B31: 33,223 old objects and 7,113 old station-object transforms preserved;
- B35: 35,550 old objects and 7,112 station transforms preserved;
- B36: 36,615 previous objects, 7,114 previous station transforms, and 2,798 protected files preserved; final file contains 36,812 objects and 7,116 station objects.

These numbers are **state-preservation descriptors**, not counts of independently verified physical assets.

## Negative evidence: persistence can propagate a wrong abstraction

B15 is the clearest case:

- common spool geometry was embedded at a shared level;
- using identical finite extents across installations created overlaps;
- recovery required separating common manufactured geometry from finite site-specific connections;
- obsolete geometry was retained/archived rather than silently overwritten.

Therefore the claim should not be “persistent state is always beneficial.” A better interpretation is:

> persistent state creates both **compositional leverage** and a **propagation surface** for earlier abstraction errors.

## Scope limit

No stateless control run exists. Therefore avoid:

- “persistent memory improves reconstruction accuracy by X”;
- “persistent state is necessary in all industrial reconstruction systems”;
- “without memory the task would fail.”

## Safe paper wording

> “AstraBuild's long horizon is implemented through external engineering state rather than transient conversational memory. Later batches reuse earlier masters, transforms, terminals, and accepted geometry, while validators explicitly check that prior state is preserved. B15 shows the corresponding risk: a wrong shared abstraction can propagate across installations until the reuse boundary is revised.”

## Role in the paper

This is the **system-level claim**. B36 should appear here as the endpoint stress test, not as an achievement section centered on object count.

---

# 5. What happens to the old Claim A: “one interface spans heterogeneous tasks”

The idea is true but too weak to carry one third of the paper by itself.

Recommended treatment:

> **Use it as feasibility evidence and as setup for Claims 1–2, not as a standalone scientific conclusion.**

Safe sentence:

> “The same programmatic evidence–build–validate interface was used throughout 36 sequential batches spanning equipment, conductors, civil structures, and auxiliary infrastructure, while task-specific operators varied substantially.”

What it supports:

- breadth of the field study;
- legitimacy of cross-regime analysis;
- motivation for the operator-evolution figure.

What it does not support:

- cross-site generalization;
- universal task competence;
- a global success rate;
- superiority to specialized systems.

---

# 6. Recommended paper-level claim hierarchy after refinement

## One thesis

> **Long-horizon industrial 3D reconstruction is better represented as persistent orchestration of specialized geometry operations than as repeated direct 3D generation.**

## Three supporting claims

### C1. Externalized geometry computation

The model formulates and revises engineering operations; deterministic code computes geometry and validates acceptance.

### C2. Broadening operator portfolio

As reconstruction dependencies accumulate, local fitting remains but additional operators become necessary for reuse boundaries, representation changes, connectivity, coverage-driven task selection, review, and interference.

### C3. Persistent state as composition mechanism and risk surface

Later tasks reuse and preserve earlier assets/endpoints/state; this enables cumulative system construction within the documented sequence and makes upstream abstraction mistakes consequential.

This is a cleaner pyramid than:

- breadth;
- failure recovery;
- human correction;
- composition;
- semantics;
- final object count.

---

# 7. Which batches should carry the main paper

Do not give all 36 batches equal narrative weight.

## Tier 1 — indispensable explanatory cases

- **B01/B02** — measurement/evaluation domain formulation;
- **B08** — shared equipment abstraction and explicit site-specific separation;
- **B15** — reuse boundary failure and correction;
- **B20** — transition to port/route-based connected systems;
- **B23** — representation change from straight to curved path;
- **B25/B26** — unexplained geometry becomes a task-selection signal;
- **B29** — large-scale endpoint/topology composition across existing subsystems;
- **B36** — late-stage state preservation, endpoint closure, and interference-aware revision.

These eight anchors are sufficient to explain the thesis.

## Tier 2 — visual breadth / corroborating examples

- B06 — clean local-fit civil example;
- B10 — repeated capacitor assemblies;
- B17/B19 — complex reusable GIS families;
- B31/B32 — building/cabin civil reconstruction and review;
- B35 — visible outdoor closure baseline.

Use these in figures/tables or short supporting paragraphs.

## Tier 3 — appendix/evidence browser

All remaining batches. They establish continuity and breadth but do not need standalone prose.

---

# 8. Claims that should disappear from the main narrative

These may remain as appendix facts but should not be headline claims:

- “37k objects” as a scientific result;
- global residual median as an overall reconstruction-accuracy claim;
- visible revision-tag counts as model performance;
- selected failure-layer frequencies;
- number of manifests/scripts/review scenes as contributions;
- D37/D38/D40/D41 material;
- semantic inspection endpoint;
- human correction as a separate major contribution;
- a global task success rate.

For the B01–B36 rewrite, the strongest endpoint scale is the B36 record (36,812 objects, 743 scenes, 7,116 station objects), but it should be used only to establish **state scale and preservation burden**.

---

# 9. Proposed Results logic after claim refinement

The Results section should follow the claim pyramid, not the batch chronology.

## 5.1 A stable engineering loop supports heterogeneous reconstruction through specialized operators

Purpose: establish feasibility and Claim 1.

Evidence:

- B01/B06 local fitting;
- B08/B17 reusable equipment;
- B20/B29 connected systems;
- B31/B35 civil/auxiliary closure;
- build/validate 36/36 with changing operator portfolio.

End with the division of labor: model formulates/coordinates; deterministic tools compute/check.

## 5.2 Reconstruction dependencies broaden the required decision and operator set

Purpose: main empirical Claim 2.

Organize by **three transitions**, not four regime subsections:

1. **fit → reusable abstraction**: B01/B06 → B08/B15;
2. **object → connected representation**: B20/B23/B29;
3. **inventory-driven addition → gap/state-driven closure**: B25/B26 → B31/B36.

The operator heatmap belongs here.

## 5.3 Persistent state turns local reconstructions into a connected engineering system

Purpose: Claim 3.

Use the explicit dependency chain:

`B08 transformer master/ports → B23 local connections → B29 overhead/cross conductors → B36 bus rack/wall closure`

Then use B15 as the counterexample showing propagation risk.

This structure gives each Results subsection a single memorable answer.

---

# 10. Reviewer red-team of the refined claims

## Likely challenge 1

“Is the operator evolution just an artifact of filenames and your retrospective regime labels?”

Response strategy:

- yes, operator prevalence is descriptive and retrospective;
- do not treat counts as inferential statistics;
- ground the substantive claim in direct artifacts (plans, diagnostics, connection inventories, spline profiles, coverage maps, endpoint checks), not only filename counts;
- use the heatmap as orientation, not proof by itself.

## Likely challenge 2

“How do you know GPT-6 Astra, rather than the deterministic scripts, is responsible for the useful behavior?”

Response strategy:

- do not attribute numerical outputs to the model;
- claim only the observable model-in-harness workflow: program authoring/revision, representation/decomposition choices, and interpretation of external evidence;
- acknowledge the absence of a matched alternative planner/model baseline.

## Likely challenge 3

“Does the sequence show learning?”

Answer: no. The record shows **stateful task progression**, not controlled model learning. Avoid “learned” and “improved reasoning over time.”

## Likely challenge 4

“Does B36 prove station-scale accuracy?”

Answer: no. B36 demonstrates a large preserved engineering state with task-local checks and explicit endpoint/contact constraints. It does not provide independent survey validation of the complete station.

## Likely challenge 5

“Why is persistence a research result rather than an implementation detail?”

Response strategy:

- later geometry literally uses earlier terminals, transforms, reusable masters, and connection endpoints;
- validators explicitly protect prior state;
- B15 shows that errors in a shared abstraction propagate through the same mechanism;
- therefore persistence changes the problem being solved: later tasks operate on and must preserve an existing engineered world rather than generating isolated assets.

---

# 11. Claim priority for drafting

## Strongest claim

**C2 — operator/decision broadening with structural dependency.**

This is the most distinctive scientific observation in B01–B36 and should receive the most Results space.

## Second strongest

**C3 — persistent state as composition mechanism and risk surface.**

This gives the long-horizon/system contribution substance beyond “many batches.”

## Foundational but less novel

**C1 — externalized geometry computation and model/tool division of labor.**

This is essential for scientific attribution and clarity, but by itself is not enough for a paper. It becomes important because C2 and C3 occur through this interface.

---

# 12. Current recommended one-sentence paper answer

If a reader asks, “What did this paper actually find?”, the answer should be possible in one sentence:

> **Across a 36-batch industrial reconstruction, GPT-6 Astra was most useful as an orchestrator of explicit geometry programs rather than as a direct geometry estimator: as the scene accumulated dependencies, the workflow added abstraction, path/topology, coverage, review, and interference operators, while persistent external state allowed these locally solved tasks to compose and also exposed the system to propagation of earlier abstraction errors.**

This sentence should be the test for the future Abstract, Introduction, Results headings, and Conclusion. If a paragraph does not help establish or qualify this answer, it probably belongs in the appendix or website evidence browser.
