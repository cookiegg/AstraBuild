# AstraBuild: A Longitudinal Evaluation of GPT-6 Astra as a 3D Engineering Agent

**Task capability, hypothesis revision, and failure modes in component-level substation reconstruction**

**Status:** restructured advisor discussion draft v0.9
**Study site:** an anonymized operating substation
**Research endpoint:** D41
**Core geometry baseline:** D38.2
**Presentation layer (geometry preserved):** D40

> **Experimental provenance note.** The project owner reports that the historical reconstruction process used **Codex + GPT-6 Astra with Extra High reasoning effort**. The inspected historical Blender batch files do not freeze model/reasoning-effort metadata. We therefore treat this configuration as **owner-confirmed experimental metadata**, not as provenance independently recoverable from the old batch logs.

---

## Abstract

Can a general-purpose reasoning model do more than generate plausible 3D assets and instead act as an engineering reasoner that **tests and revises modeling hypotheses when physical evidence contradicts them**? We study this question in a longitudinal reconstruction of one operating operating substation. GPT-6 Astra, accessed through Codex, operates inside a fixed Blender/Python harness that supplies registered photogrammetric geometry, field images, engineering records, prior reconstruction state, deterministic tools, and task-specific validators. The preserved record contains **38 sequential core batches across 12 reconstruction task families**. Because later batches inherit earlier geometry, reusable assets, validators, and failures, the study is a longitudinal case study rather than an IID benchmark.

The record separates two aspects of performance. First, when a task can be reduced to an explicit measurement or fitting problem, the workflow can compile a local reference and delegate numerical estimation to deterministic operators; wall, capacitor, building, and cabin cases then reach centimeter-scale **internal agreement with the same photogrammetric reference used during reconstruction**. Second, the difficult revisions are often not parameter changes. Among the seven documented adaptation/failure episodes selected for cross-case analysis, five concern the evaluation protocol, reusable-asset boundary, geometric representation, or task-selection rule. B15 moves finite geometry out of an overgeneralized shared asset; B23 replaces a straight-lead representation after measured profiles expose roughly 0.5 m of curvature; B25/B26 changes task selection from inventory completion to unexplained geometric coverage; and D38 converts 2D review markup into 3D correction but requires a subsequent review to repair an orientation-semantics error. These episodes show that externalized measurements and review artifacts can cause Astra to revise the **kind of engineering hypothesis** being used, while also showing that first-pass detail interpretation and coordinate semantics remain error-prone.

Accepted task outputs accumulate into a **37,153-object** station state, providing a long-horizon stress test of reuse, provenance, and composition rather than an accuracy benchmark. The evidence therefore supports a narrower characterization: Astra can participate in a persistent, evidence-grounded 3D engineering process and can revise high-level modeling decisions when contradictions are made explicit, but deterministic validation and human review remain material to acceptance. The present record is limited to one site, has no independent survey reference, and contains no matched reruns with another model.

---

# 1. Introduction

Modern photogrammetry and neural scene reconstruction can recover rich appearance and geometry from image collections [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians]. Industrial digital twins, however, often require a different representation. Downstream inspection, simulation, asset maintenance, and change management benefit from models that remain **editable, componentized, reusable, semantically addressable, and traceable over time**. A fused surface can show where an object is, but it does not by itself state which pieces belong to the same GIS bay, which repeated devices should share a master asset, which connection is site-specific, or how an inspection concept maps to an explicit component.

These requirements become difficult in an operating substation because the evidence is incomplete and heterogeneous. The registered photogrammetric mesh provides global layout and local occupied surfaces but contains holes, fused neighbors, stretched geometry, and insufficient component detail. UAV and ground photographs reveal visible structure but are not uniformly calibrated and do not authenticate every device identity. Engineering inventories and 12MZ records provide expected names and inspection concepts but do not guarantee that corresponding geometry has been reconstructed. Human reviewers can recognize omissions or implausible structures, but requiring them to manually edit Blender vertices would negate much of the value of an agentic workflow.

The site reconstruction project provides a long trace of one reasoning system operating inside this setting. Rather than asking a model to reconstruct one isolated object, the project repeatedly asks the **same agent/harness** to solve different 3D engineering tasks in a shared Blender environment. Early tasks fit arresters and civil boundaries. Later tasks build shared transformer assemblies, capacitor banks, GIS families, bus/conductor systems, buildings, and auxiliary facilities. Still later tasks revisit earlier assumptions after geometric validation or human review exposes omissions and errors. The final artifact is not a folder of independent meshes but one persistent station-scale engineering state.

This structure is closer to recent embodied-agent studies than to a conventional single-object reconstruction benchmark. In embodied-policy reports, one general-purpose policy is exercised across multiple tasks under a shared robot/controller environment [@cheng2026gptpolicy; @su2026astraembodied]. Here, the shared environment is a persistent 3D engineering system: Blender/Python is the actuator; images, coarse geometry, inventories, and prior artifacts form the observation/context; validators provide execution feedback; and the filesystem provides durable external memory.

This setting motivates a more specific question than whether the model can produce individual assets:

> **When a general-purpose reasoning model is constrained by registered geometric evidence, programmatic tools, and deterministic validation in a persistent 3D environment, how does it form, test, and revise engineering hypotheses, and where do those decisions fail?**

We use the historical task sequence as a set of probes for this question. The paper asks four operational subquestions: (1) which heterogeneous reconstruction tasks can the same model/harness execute; (2) whether contradictions lead only to parameter tuning or also to revisions of the evaluation protocol, abstraction boundary, representation class, and task-selection rule; (3) which decisions still require deterministic or human review; and (4) whether accepted outputs can persist and compose over a long task horizon without losing provenance or state consistency.

The study is intentionally a **longitudinal single-site case study**. The 38 core batches are dependent observations: later tasks inherit geometry, component libraries, validators, and mistakes from earlier ones. Task diversity is therefore used to probe behavior, not to construct an IID success rate, and the station-scale artifact is treated as a long-horizon composition stress test rather than as evidence of independent metric accuracy.

## 1.1 Contributions

This work makes three contributions.

1. **A longitudinal evaluation protocol for a 3D engineering agent.** Twelve heterogeneous reconstruction task families probe one focal model inside a common evidence/action/validation interface, while the original review pages, validators, and revision artifacts preserve the observations on which later decisions were based.
2. **A cross-case analysis of engineering hypothesis revision.** Preserved failures expose changes at the protocol, abstraction, representation, task-selection, and human-feedback layers. This analysis separates parameter fitting from the higher-level decisions that determine what geometry is measured, shared, built, or revised.
3. **A long-horizon composition stress test.** Accepted task outputs remain in one evolving station model, allowing the study to examine reuse boundaries, error preservation, state consistency, and later semantic augmentation across many sequential tasks.

---

# 2. Related Work and Research Positioning

## 2.1 Surface reconstruction versus editable engineering representation

Classical structure-from-motion/photogrammetry and modern neural scene representations solve important perception problems [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians]. Their outputs, however, do not automatically supply engineering structure. An industrial model must often encode repeated equipment families, instance relationships, finite site-specific connectors, explicit component identities, and a history of later corrections.

AstraBuild therefore treats the photogrammetric reconstruction as **evidence and spatial context**, not as the final representation. The target artifact is an editable Blender scene with component collections, reusable masters, site instances, explicit connections, review views, provenance records, and later semantic mappings.

## 2.2 Programmatic 3D agents and general-purpose models as tool users

Language and vision-language models can synthesize executable programs and operate structured tool interfaces [@liang2023code; @huang2023voxposer]. In 3D generation, 3D-GPT decomposes procedural modeling into task-dispatch, conceptualization, and modeling agents that ultimately emit Python/Blender operations [@sun2023threegpt]. SceneCraft is closer to AstraBuild at the execution level: it plans a scene graph, translates spatial relations into numerical constraints and Blender-executable Python, evaluates rendered outputs with a visual reviewer, iteratively refines the scene, and distills reusable functions into a library [@hu2024scenecraft].

AstraBuild differs in problem direction and evidence regime. 3D-GPT and SceneCraft primarily synthesize scenes from language descriptions; AstraBuild performs **reverse engineering from registered physical evidence**. Its intermediate artifacts are therefore not only rendering feedback. They include metric profiles, local reference domains, conductor-route fits, collision/coverage diagnostics, history-preservation checks, and frozen revisions whose purpose is to constrain an evolving industrial model.

GPT-Policy is especially relevant because it separates context construction, model decisions, constrained execution, replanning from feedback, and persistent run recording [@cheng2026gptpolicy]. The GPT-6 Astra embodied policy report similarly studies one general-purpose model across multiple tasks in a common embodied environment and analyzes representative behavioral episodes rather than only final aggregate scores [@su2026astraembodied].

AstraBuild adopts the same **agent-centric experimental viewpoint**, but the environment and time horizon differ. The model does not output robot actions; it writes and revises reconstruction programs, inspects renders and validation results, and operates over an engineering history spanning many task families and saved artifacts.

## 2.3 Task suite, not IID benchmark

The historical sequence contains many equipment and infrastructure reconstruction cases, but they are not statistically independent episodes. The same Blender scene, component libraries, validators, and history persist across tasks. We therefore use each equipment/infrastructure family as a **task instance in a shared persistent environment**, analogous to one embodied policy being exercised on heterogeneous tasks, while explicitly avoiding an IID success-rate interpretation.

---

# 3. Evaluation Harness and Persistent Engineering State

The evaluation separates the focal model from the deterministic system around it. GPT-6 Astra selects evidence, proposes or revises an engineering representation, and writes or modifies Blender/Python programs. Numerical fitting, rendering, file/state preservation, and task-native validators execute outside the language model. A model-authored program is therefore a proposal, not an accepted result.

## 3.1 Persistent state and evidence context

Let the engineering state after task/batch \(t\) be

\[
S_t=(M_t,A_t,H_t,X_t),
\]

where \(M_t\) is the editable Blender scene, \(A_t\) the reusable asset/instance hierarchy, \(H_t\) the accumulated external engineering history, and \(X_t\) semantic/inspection mappings. For each task, a bounded context

\[
C_t=\mathcal{C}(G,I,R,U,H_t)
\]

is assembled from registered photogrammetric geometry \(G\), field images \(I\), engineering/semantic records \(R\), spatial priors \(U\), and prior history \(H_t\). These sources have different evidentiary roles: geometry supplies registered layout and local comparison surfaces; photographs supply visible form; records supply expected identity and semantics; human review supplies equivalence authorization or error signals; prior batch artifacts expose what the system previously accepted or rejected.

![Figure 1: AstraBuild evaluation harness and persistent state.](../figures/fig01_agentic_loop.png)

**Figure 1.** Evaluation setting. Heterogeneous evidence and inherited state condition the model; Astra proposes programmatic engineering actions; external tools execute them; review and task-specific validation determine what persists.

## 3.2 Model decisions and deterministic execution

The model acts through an engineering API implemented in Python/Blender. Observable decisions include selecting a local reference, choosing a measurement domain, selecting a geometric representation, constructing reusable `MASTER` collections and rigid `SITE` instances, generating finite connectors or conductor paths, requesting diagnostics, and revising programs after review. Deterministic tools then materialize these decisions: NumPy/SciPy perform numerical fits, Matplotlib generates profiles and diagnostics, Blender builds geometry and fixed-camera renders, and validators recompute geometry, contact, continuity, coverage, state-preservation, and file-integrity checks.

This division is important for attribution. A centimeter-scale fitted residual is evidence that the model formulated and invoked a measurement procedure; it is not evidence that the language model numerically optimized the geometry internally. Conversely, plausible generated geometry is not accepted because the model produced it. It enters persistent state only after the corresponding review and validator checks.

## 3.3 Review, validation, and external memory

Across formal batches, the recurring state transition is compact: preserve inherited state; select a local evidence domain; inspect and plan; build or revise geometry; render controlled review evidence; validate task-native properties; then freeze the release and its continuation record. Specialized operators such as profile fitting, route diagnostics, coverage audits, collision checks, or markup registration appear only where the task requires them.

The review layer is unusually well preserved. **Thirty-two formal batches from B07 through D38 retain their original interactive `review.html` pages**, typically exposing fixed-camera Clean/Overlay/Reference evidence, selectors, sliders, and task-specific caveats. The output folders also retain profiles, preflight graphics, route diagnostics, validation JSON, manifests, failed revisions, and continuation notes. These artifacts constitute the external memory used by later tasks and the evidence base for the case analysis; the companion website exposes them as appendices rather than interleaving them with the main argument.

A crucial provenance boundary is that these files **do not preserve GPT-6 Astra's private chain-of-thought**. The paper therefore analyzes the observable decision trail: selected evidence, generated or revised programs, deterministic outputs, review/validation results, and subsequent revisions. It does not infer an internal reasoning transcript.

## 3.4 Representative task trace: B32 secondary-equipment cabins

B32 illustrates the separation between metric fitting and engineering interpretation. Inherited vertical samples and the station frame are processed by a model-authored measurement program; deterministic rectangular fits produce cabin width, length, yaw, root transforms, and facade diagnostics. Those measurements are sufficient for the cabin envelopes but not for the door structure. R1 places one door per cabin and puts the Cabin-A door on the wrong side. Fixed-camera review, low-height registered slices, field photographs, and stair-platform signatures contradict that interpretation. R2 moves the Cabin-A door; R3 retains one Cabin-A east-side door and two Cabin-B west-side doors and rejects a middle Cabin-B depression previously interpreted as a door.

![Figure 2: B32 observable agent–tool trace.](../figures/fig12_b32_worked_example.png)

**Figure 2.** B32 maps inherited evidence to measurement, program revision, componentized geometry, fixed-camera review, validation, and persistent state. The trace distinguishes Astra's engineering decisions from deterministic computation and rendering.

The retained validator also checks inherited-state preservation, facade comparison domains, door/stair constraints, camera framing, and component-library round trips. The original `B32_review.html` remains part of the experiment record and is exposed in the website's interactive evidence appendix. B32 therefore provides a concrete caution for later interpretation: a defensible metric envelope does not imply a correct component model at the level of visible engineering detail.

---

# 4. Reconstruction Task Suite

## 4.1 Task definition

We reinterpret the B/D history as a suite of heterogeneous reconstruction tasks solved by one persistent agent/harness. Each task consists of a target equipment/infrastructure family, a bounded evidence package, an allowed Blender/Python action space, and task-native validation criteria. Tasks share the same evolving engineering state and are therefore not IID.

## 4.2 Task families

| Task family | Historical batches | Representative target/output | Capability exercised | Representative recorded evidence |
|---|---|---|---|---|
| Surge-arrester fitting | B01–B05, B18 | SA-A/SA-B bodies and installation | local fitting, pose/scale, held-out checking | B01 preserved failure; B02 naked-shaft RMS 1.8–3.4 cm under revised domain |
| Wall and gate | B06 | station wall + gate | large civil geometry from coarse reference | east-wall median reference distance 7.87 m→0.015 m |
| Transformer reconstruction | B07–B08 | two main transformers | complex assembly and reusable abstraction | shared T1/T2 assembly; bank median ~0.01 m; T2 front P95 0.62 m tail retained |
| Capacitor-bank reconstruction | B09–B10 | six VC-C capacitor groups | repeated structures and local assemblies | 18 lane medians 0.6–2.4 cm; first broad outdoor coverage audit |
| VC-A GIS/device families | B11–B16 | GIS bays, arresters, bus-tie/VT structures | reusable families and variants | B13 creates seven GIS sets with ~2,400 expanded meshes |
| VC-B GIS/outgoing families | B17–B19 | outgoing bays and variants | cross-family reuse and complex topology | B17 75 local checks: 50 pass / 25 retained non-pass |
| Bus and conductor systems | B20–B30 | busbars, drops, insulator strings | explicit connectivity and flexible paths | ~88.8 m busbar; 804 discs; endpoint continuity ~1e-6 m scale |
| Building and ground | B31–B34 | main building + ground | large structured civil reconstruction | building 946 components; ground ~10,182 m²; wall-domain RMS 1.8–3.2 cm |
| Auxiliary facilities | B35–D37 | CCTV, fence, bus racks, floodlights, manholes | long-tail infrastructure and revision | B35 multi-revision path; later omission audit triggers B36 |
| Human-guided correction | B36, D38 | missing bus rack; false cabinets; missing GIS/fire room | history search, markup-to-3D correction | B36 multi-revision recovery; D38 NCC 0.94/0.92 and coordinate-grounded correction |
| Presentation invariance | D40 | PBR material layer | modify appearance while preserving geometry | 37,153 objects / 29,986,649 vertices unchanged |
| Inspection-semantic augmentation | D41 | transformer inspection accessories | part-addressable semantic augmentation | 79 accessory meshes, 17 selected missing classes × T1/T2; validation `ok=true` |

The table defines the **probe set** used in the longitudinal evaluation. The task families expose different engineering decisions, including local fitting, reuse, connectivity, omission discovery, correction, and semantic augmentation. Their heterogeneous validators are not reduced to one common score.

## 4.3 Longitudinal progression

The task suite also changes over time. Early work focuses on local fitting and device families; later work emphasizes connected systems, coverage-driven omission discovery, human correction, and semantics. Because later tasks inherit earlier artifacts and protocol changes, chronology matters and is retained as part of the evidence.

---

# 5. Task-Level Results

## 5.1 Breadth and engineering scale

At the D38.2/D40-equivalent layer, the project contains **37,153 objects, 755 scenes, 858 collections, 3,916 mesh datablocks, and 29,986,649 vertices**. The technical report summarizes reconstructed coverage including **48 arrester bodies, 8+3 GIS bays, two main transformers, six capacitor groups, approximately 88.8 m of busbar, 804 insulator discs, approximately 10,182 m² of ground surface, and a 946-component main building**, in addition to auxiliary facilities and later D38 corrections.

These counts do not imply that every physical object is independently verified. They demonstrate the breadth of engineering operations carried out by one persistent reconstruction process.

## 5.2 Internal geometry ledger

The technical summary contains **1,550 current surface-comparison records** with median/p90/p95 residuals of **0.036/0.084/0.116 m**. A separate 5 cm screen retains **149 passing and 101 non-passing** items. Non-passing evidence remains in the historical accounting rather than being deleted to produce a uniformly favorable final statistic.

Because the comparison surface is the same registered photogrammetric mesh that also supplies reconstruction evidence, these values describe **internal reference agreement**, not independent survey accuracy.

![Figure 3: Quantitative task-level evidence.](../figures/fig03_quantitative_evidence.png)

**Figure 3.** Geometry residuals, retained validation-screen items, and coverage-gap measurements answer different engineering questions and are therefore reported separately.

## 5.3 Reuse as a persistent-system property

The final layer contains 37,153 scene objects backed by 3,916 mesh datablocks, giving a descriptive object-to-mesh ratio of approximately **9.5×**. This is not a labor-speed or compression metric. It indicates that repeated equipment is increasingly represented through shared geometry and instances.

B08 is the clearest example: after an explicit user authorization that the two transformer component assemblies can be treated as equivalent, the workflow creates a common master and T1/T2 site instances. Later GIS, arrester, and insulator tasks extend this reuse principle, while B15 shows that invalid reuse boundaries must be revised.

## 5.4 Coverage becomes a task-selection signal

B25/B26 marks an important transition. Instead of asking only which inventory entry is unresolved, the workflow asks where selected high-region coarse geometry remains unexplained by the component model. In that audit:

- the fraction of selected samples more than 1 m from modeled geometry changes from **78.8% to 14.6%**;
- the selected GIS-B high-region median changes from **8.12 m to 0.15 m**;
- the selected transformer high-region median changes from **3.15 m to 0.06 m**.

The significance is not absolute metric accuracy. The reference scene becomes an **active sensor for omission discovery and task selection**.

---

# 6. Behavioral Case Studies: How Astra Revises Modeling Decisions

The task suite establishes what the workflow attempted. The following cases examine what happens when the current engineering hypothesis is incomplete or contradicted by measurement, review, or later state. They are selected for diagnostic diversity rather than statistical representativeness.

![Figure 4: Failure and recovery cases.](../figures/fig05_failure_recovery.png)

**Figure 4.** Representative failures alter later evaluation protocol, reusable abstractions, reconstruction logic, or feedback interpretation rather than being silently discarded.

## 6.1 B01→B02: the evaluation domain is itself a hypothesis

B01 installs three arrester candidates. Source hashes and transform checks pass, but held-out cylindrical-domain RMS values of approximately **0.048, 0.073, and 0.051 m** violate the selected 5 cm screen. The batch is retained as failed.

The diagnosis concerns the comparison protocol rather than a fitted dimension: the comparison domain mixes the target shaft with protruding accessory geometry. B02 therefore separates fitting and holdout regions, and the historical notes explicitly state that the revised metric should not be presented as a directly comparable accuracy improvement over B01.

**Interpretation.** The workflow can revise the *measurement protocol* after diagnosing a failure while preserving the original failed result.

## 6.2 B08: from one device to a reusable engineering abstraction

B07 reconstructs only part of the #1 transformer exterior. After the user explicitly authorizes the two transformer assemblies to be treated as equivalent, B08 introduces a shared transformer `MASTER` and site-specific T1/T2 instances.

The result is more than duplicated geometry: later structural edits can propagate consistently. At the same time, the validation history keeps a T2-front P95 residual tail of approximately **0.62 m** rather than allowing the otherwise small bank-distance summary to hide it.

**Interpretation.** The workflow can promote a successful local reconstruction into a reusable asset abstraction while retaining evidence that challenges parts of the fit.

## 6.3 B15: the reusable abstraction is wrong

B15 reconstructs reserve GIS equipment and undergoes multiple revisions. One local measurement procedure is contaminated by neighboring equipment. Separately, the first shared bus-spool design extends the same finite geometry across installations whose physical extents differ, creating overlaps with adjacent equipment.

Recovery therefore changes two levels simultaneously: the measurement method and the **MASTER/site boundary**. Site-specific finite bus segments are removed from the shared master; obsolete supports are archived rather than silently overwritten.

**Interpretation.** A reusable component library encodes a geometric equivalence hypothesis. Field evidence can falsify that hypothesis and require a different MASTER/site boundary.

## 6.4 B23: process evidence changes the representation

B23 reconstructs the transformer neutral-side mechanisms and leads. An earlier preflight inherited from B22 effectively treated a connection as a simple straight segment. Direct inspection of the registered coarse geometry instead reveals a mid-span bow of roughly half a meter. The batch therefore bins the observed geometry, extracts control points, fits a smooth curved path with fixed endpoints, and refines the shared mechanism and soft connections.

The revision history is informative. The first reconstruction worsens one validation domain because older geometry had accidentally covered part of the soft connection; r2 explicitly adds the soft lead, and r3 adds lower bridge contact. The final record evaluates 32 fixed triangle domains, with 30 meeting the selected 5 cm screen and two retained misses. The process folder preserves `B23_measurement_profiles.png`, `component_and_lead_preflight.png`, the fitted plan, render triplets, manifests, and validation files.

**Interpretation.** Intermediate measurement and preflight artifacts can change the *class of geometry being built*. In this case, observed curvature invalidates the straight-segment representation and leads to a curved path model plus subsequent contact revisions.

## 6.5 B25/B26: task selection changes from inventory to unexplained geometry

Earlier work naturally follows equipment lists. By B25/B26, the dominant risk is an unknown omission: a structure can be absent from the model even if its semantic inventory entry appears resolved. Coverage auditing identifies selected high regions of coarse geometry that remain far from reconstructed components and triggers additional modeling.

**Interpretation.** The workflow shifts from executing a predefined to-do list toward **evidence-driven task selection**.

## 6.6 B36: sparse review triggers a multi-step engineering response

After B35, a top-view reviewer identifies missing low bus racks near the transformers/building. The workflow first opens an audit-only path, searches historical logic, and traces the omission to an earlier decision that had treated the structure as outside the transformer assembly.

The reconstruction then requires multiple revisions: an initial draft contains a non-finite path section, a later version fixes section orientation, and a final version moves one incoming segment by **0.16 m** to avoid an existing fire pipe.

**Interpretation.** The human supplies a compact spatial error signal; the agentic workflow performs the history search, geometric reconstruction, revision, and verification.

## 6.7 D38: 2D markup becomes traceable 3D correction

D38 is the most complete human–agent episode. The user marks false red boxes, missing GIS structures, and missing fire infrastructure on stored review images. The workflow registers the marked images to the original views with normalized correlations of approximately **0.94/0.92**, inverts the review-camera mapping, and derives model-world coordinates for the marked regions.

Three false cabinet groups are identified. Their component objects are moved to a **quarantine collection** rather than deleted, preserving the provenance of the earlier mistake. Three missing GIS gaps and the fire-room/sand-box structures are rebuilt. A first D38.1 revision then mistakes a registration yaw for equipment orientation; overlay review reveals the coordinate-semantics error and D38.2 corrects it.

![Figure 5: D38 human-feedback chain.](../figures/fig06_d38_human_feedback.png)

**Figure 5.** Sparse 2D markup is transformed into a traceable sequence of registration, coordinate inference, diagnosis, quarantine/rebuild, and review.

**Interpretation.** The system can convert high-level human spatial feedback into programmatic correction while retaining the history of both the original generation error and an intermediate correction error.

---

# 7. Cross-Case Findings: What Astra Does Well and Where It Fails

The case studies support five findings about the model-in-harness behavior. These are descriptive findings from the preserved episodes and task records; they are not estimates of population-wide failure frequencies.

## 7.1 F1: Explicit measurement operators separate reasoning from numerical estimation

Astra is most defensible when it decides **what to measure and how to structure the comparison**, while deterministic code performs the numerical fit. Wall, capacitor, building, and B32 cabin tasks all use registered local domains and explicit fitting or measurement programs. The resulting centimeter-scale values describe agreement with those correlated reference domains, not independent survey accuracy. The scientific point is the division of labor: the model selects the engineering measurement problem; numerical tools solve it reproducibly.

## 7.2 F2: The difficult revisions are often hypothesis-level, not parameter-level

Among the seven documented adaptation/failure episodes annotated for cross-case analysis, five are classified at the protocol, abstraction, representation, or task-selection layers rather than as simple parameter errors. B01 changes the comparison domain; B15 changes the reusable-asset boundary; B23 changes the geometry class; B25/B26 changes how the next task is chosen; D38.1 corrects a coordinate-semantics interpretation. This pattern should be read as a property of these selected documented episodes, not as an estimated frequency over all reconstruction errors.

## 7.3 F3: First-pass visual detail and semantic interpretation remain unreliable

B32 shows that a correct cabin envelope does not imply correct door structure. B23 initially inherits an inadequate straight connection. D38.1 converts a successful image registration into the wrong equipment orientation. These failures share a boundary: a plausible interpretation of visible geometry can still encode the wrong engineering representation. Review images, profiles, and task-specific diagnostics are therefore part of the measurement process rather than presentation-only artifacts.

## 7.4 F4: Human input is sparse but materially changes the trajectory

B08 requires explicit authorization before two transformer assemblies are treated as equivalent; B36 begins from an omission report; D38 begins from marked review images. The human does not manually edit vertices, but these interventions affect what the agent is allowed to share, what subsystem it reconstructs, and what error it corrects. The demonstrated workflow is therefore **agent-driven and human-steerable**, not autonomous.

## 7.5 F5: Persistent state enables long-horizon composition and creates propagation risk

Reuse, protected history, and inherited transforms let later tasks build on earlier work, but the same persistence makes a wrong abstraction consequential. B15 is the clearest counterexample: geometry placed inside a shared master propagates the mistake across installations until the MASTER/site boundary is revised. Long-horizon state is therefore both an enabling mechanism and an engineering risk that requires provenance and validation.

![Figure 6: Cross-case behavioral analysis.](../figures/fig14_behavioral_analysis.png)

**Figure 6.** Descriptive context for the cross-case analysis. Visible revision tags are a lower bound; failure-layer and adaptation labels are manual annotations of documented episodes; operator counts describe recorded workflow stages rather than success rates.

---

# 8. Long-Horizon Composition Stress Test

The system-level evidence concerns persistence across tasks: outputs from heterogeneous reconstructions remain in one Blender project and eventually form a connected, reviewable, and semantically extensible station model.

## 8.1 Long-horizon engineering trace

The core history contains **38 reconstruction batches, 54 build scripts, 58 validation scripts, 150 manifests, 71 validation JSON files, 28 installation-queue revisions, and 109 local coarse-reference NPZ crops**. By the later B35-era chain, the technical report records **2,859+ protected-file hashes**. These artifacts provide a durable trace across which later tasks reuse previous components and inspect previous failures.

At D38.2/D40 scale, the integrated project contains **37,153 objects, 755 scenes, 858 collections, and 3,916 mesh datablocks**.

![Figure 7: Long-horizon composition stress test.](../figures/fig09_task_suite_composition.png)

**Figure 7.** Heterogeneous task outputs enter one persistent engineering state, making reuse, provenance, and state consistency constraints on later tasks.

## 8.2 Composition is more than concatenating meshes

The station-scale result requires cross-task consistency:

- device families must remain shared where equivalence is justified;
- finite site-specific connections must remain outside globally shared masters;
- previous transforms and objects must survive later batches;
- bus/conductor endpoints must remain connected to equipment introduced in earlier tasks;
- new tasks must not silently overwrite historical outputs;
- coverage audits must expose structures never introduced as explicit semantic tasks;
- human corrections must modify the active model while preserving the rejected geometry in history.

These constraints make the integrated station a stronger demonstration than a gallery of independent object meshes. It tests maintenance of **persistent engineering state over a long task horizon**.

## 8.3 Layered endpoint

The version boundary remains explicit:

- **D38.2:** principal reconstructed station geometry after the D38 correction loop;
- **D40:** material/presentation layer validated to preserve geometry, transforms, object counts, and vertex counts;
- **D41:** additive transformer inspection-semantic accessory layer.

Separating these layers prevents a better-looking render from being misreported as new geometry and prevents later semantic additions from being back-projected into earlier results.

---

## 8.4 Inspection-semantic endpoint

Once geometry stabilizes, the project builds semantic mappings as a separate layer. At station level, the current part map contains **151 devices**. Among **106 official names**, **76 are attached** and **30 remain unmatched** rather than being forced onto uncertain geometry.

For the #1 transformer pilot, **189 semantic meshes** are grouped into **26 part classes**. The official **36 inspection concepts** are categorized as **31 concepts represented by model parts, 4 external components, and one nonvisual operating-sound concept**. A later semantic audit also identifies incorrect attachments caused by naïve string/box logic, including cross-bay bus tubes and misidentified arresters/switches, and revises them instead of forcing semantic completeness.

### 8.4.1 D41: inspection-addressable transformer accessories

The B08 transformer assembly captures major station-visible structure but lacks several inspection-relevant accessories present in the semantic transformer group. D41 selects **79 accessory meshes covering 17 missing inspection-relevant part classes**, aligns them to the B08 tank frame, stores them as one shared accessory collection, and instantiates that collection into both T1 and T2 using the existing site transforms.

The recorded D41 validation reports `ok=true`, including 79/79 structure/count checks and 17/17 selected class coverage for both transformer instances. The batch also writes part/world-location records.

![Figure 8: D41 inspection-semantic augmentation.](../figures/fig07_d41_inspection_semantics.png)

**Figure 8.** The additive semantic endpoint attaches selected transformer inspection parts after the geometry baseline; it does not create a new reconstruction baseline.

---

# 9. Discussion and Limitations

The task suite, case studies, and composition stress test answer different parts of the central question. The task suite establishes that one focal model can operate through the same engineering interface across heterogeneous asset classes. The cases show that the useful behavior is not limited to producing geometry: when evidence is externalized through measurements, overlays, profiles, or coverage maps, Astra can revise the engineering hypothesis that determines what is measured or built. The same cases also establish a boundary: plausible model reasoning is not an acceptance criterion. Fine-detail interpretation, coordinate semantics, reuse decisions, and even corrections can be wrong until checked by deterministic or human review.

The closest analogy to the reference embodied-agent reports is therefore methodological rather than statistical. Their tasks probe a common policy and their behavioral episodes explain aggregate outcomes; here, reconstruction tasks probe one persistent model/harness and the episodes explain why particular engineering decisions are revised. Unlike repeated robot trials, however, these batches are dependent, task validators are heterogeneous, and later tasks inherit earlier state.

## 9.1 Threats to validity

**Single-site external validity.** All task families come from one substation. Diversity within one site does not establish transfer to another station, vendor, climate, or acquisition protocol.

**No independent survey reference.** Centimeter-scale residuals compare reconstructed geometry with the same photogrammetric mesh that also guides reconstruction. They measure internal agreement, not independent survey accuracy.

**Human steering is material.** B08 equivalence authorization, B36 omission review, D38 markup, and semantic audit influence the trajectory. The supported claim is agent-driven, human-steerable reconstruction rather than full autonomy.

**Heterogeneous validators and selected behavioral cases.** Different task families require different checks, so the record has no defensible global success-rate denominator. The seven adaptation/failure episodes used for cross-case analysis were selected because their evidence trails expose distinct decision layers; their layer counts are descriptive, not population estimates.

**Historical model provenance is owner-confirmed.** Legacy batch logs do not freeze model identifier or reasoning effort. Future controlled studies should record model/version, reasoning setting, tool versions, evidence manifests, token usage, wall-clock time, human intervention, and output hashes per run.

**No matched model comparison.** The historical data contain no reruns with another foundation model, specialized 3D system, no-image/no-coarse ablation, or professional CAD baseline. The present paper therefore characterizes one model-in-harness record rather than ranking alternatives.

---

# 10. Conclusion

AstraBuild evaluates GPT-6 Astra through a longitudinal component-level reconstruction record rather than a collection of final 3D assets. Across 12 task families, the model operates through one evidence/action/validation interface while later tasks inherit earlier geometry and mistakes. The revision sequence provides the behavioral evidence: the workflow changes comparison domains, reuse boundaries, representation classes, and task-selection rules when preserved measurements or review artifacts contradict the current engineering hypothesis.

The record also identifies where the approach remains weak. A good metric envelope does not guarantee correct fine detail; coordinate and orientation semantics can be misinterpreted; human signals materially affect several trajectories; and deterministic validators remain necessary to decide what is retained. The 37,153-object station state shows that accepted outputs can persist and compose over a long horizon, but it is a stress test of state discipline rather than independent evidence of reconstruction accuracy.

The supported conclusion is consequently narrower than “Astra reconstructs a substation autonomously.” The evidence supports GPT-6 Astra as a **human-steerable engineering reasoner inside a deterministic reconstruction system**: useful for selecting, constructing, and revising modeling hypotheses over externalized evidence, but not sufficient as its own acceptance authority.

---

# Appendix A. Version Boundary

| Layer | Role | Interpretation |
|---|---|---|
| D38.2 | principal station geometry | main geometry/count baseline |
| D40 | PBR/material presentation | geometry-preserving presentation control |
| D41 | transformer accessory/inspection augmentation | additive research endpoint |

---

# Appendix B. Core Quantitative Guardrails

- `3.6 cm` = median residual to the same photogrammetric reference mesh; **not absolute/survey accuracy**.
- `149 / 101` = retained 5 cm screening-item counts; **not a model success rate**.
- `78.8% → 14.6%` = selected high-region >1 m gap fraction; **not whole-station completeness**.
- `9.5×` = descriptive object/mesh-datablock reuse ratio; **not a measured modeling-speedup**.
- `37,153 objects` = Blender scene scale; **not 37,153 independently verified physical components**.
- `D41 17 classes` = selected transformer inspection-semantic augmentation; **not complete station-wide part semantics**.

---

# References

Use the existing `references.bib`. The framing references most relevant to the advisor discussion are GPT-Policy [@cheng2026gptpolicy], the GPT-6 Astra embodied-policy technical report [@su2026astraembodied], RoboDojo [@chen2026robodojo], SceneCraft [@hu2024scenecraft], 3D-GPT [@sun2023threegpt], foundational photogrammetry and neural reconstruction work [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians], and work on models that use programmatic tools [@liang2023code; @huang2023voxposer].
