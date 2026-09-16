# AstraBuild: GPT-6 Astra as a Long-Horizon 3D Engineering Agent for Component-Level Substation Reconstruction

**Status:** polished advisor-discussion draft v0.7  
**Study site:** 220 kV Xialin Substation, Xuancheng  
**Research endpoint:** D41  
**Core geometry baseline:** D38.2  
**Presentation-only geometry-preserving layer:** D40  

> **Experiment-provenance note.** The project owner reports that the historical reconstruction process used **Codex + GPT-6 Astra with Extra High reasoning effort**. The inspected historical Blender batch files do not freeze model/reasoning-effort metadata. We therefore treat this configuration as **owner-confirmed experimental metadata**, not as provenance independently recoverable from the old batch logs.

---

## Abstract

General-purpose reasoning models are increasingly evaluated as agents that operate tools across heterogeneous tasks. We ask whether the same idea extends to industrial 3D engineering: **can one reasoning agent repeatedly solve different component-level reconstruction tasks, preserve the engineering consequences of earlier decisions, and compose the resulting assets into a persistent digital twin?**

We study this question through the longitudinal reconstruction of an operating 220 kV substation. A single GPT-6 Astra-based workflow is used across a **12-family reconstruction task suite** spanning surge arresters, walls and gates, transformers, capacitor banks, 110 kV and 220 kV GIS equipment, bus/conductor systems, buildings and ground, auxiliary facilities, human-guided correction, presentation invariance, and inspection-semantic augmentation. For each task, the agent receives a bounded evidence package assembled from a registered but noisy photogrammetric mesh, field photographs, engineering/semantic records, prior batch artifacts, and sparse human feedback. It acts through Blender/Python programs; task-specific deterministic validators determine whether the resulting artifact is retained, revised, or quarantined.

The historical folders reveal a second layer of evidence that is easy to lose when only final renders are shown. Across batches, the workflow repeatedly leaves **process artifacts**—registered reference crops, measurement/profile plots, preflight diagnostics, routing and cross-section fits, clean/overlay/reference render sets, validation ledgers, manifests, failed revisions, and continuation notes. These records show that the process is not a single rigid pipeline. It has a stable reconstruction core, while task-specific engineering operators are invoked only when required by the current geometry or failure mode.

The historical record contains **38 core reconstruction batches**, **54 build scripts**, **58 validation scripts**, **150 manifests**, **71 validation JSON files**, and **109 local coarse-reference crops**. At the D38.2/D40-equivalent geometry layer, the station contains **37,153 objects, 755 scenes, 858 collections, and 3,916 mesh datablocks**, corresponding to an approximate descriptive object-to-mesh reuse ratio of **9.5×**. The geometry ledger contains **1,550 current reference-surface comparisons** with median/p90/p95 residuals of **0.036/0.084/0.116 m** against the same photogrammetric mesh used by the reconstruction process; these values are **not independent survey accuracy**.

The strongest evidence comes not from a single aggregate score but from how the workflow behaves across tasks and failures. B01 preserves a failed arrester reconstruction and changes the holdout protocol; B08 converts two transformers into a shared reusable assembly after an explicit equivalence authorization; B15 revises both the measurement method and the boundary between reusable and site-specific GIS geometry; **B23 rejects an inadequate straight-lead hypothesis after measurement profiles expose substantial curvature and replaces it with fitted curved paths through multiple revisions**; B25/B26 changes task selection from inventory-driven completion to unexplained-geometry coverage; B36 turns a sparse omission report into a multi-revision reconstruction; and D38 maps 2D review markup into model coordinates, quarantines false objects, rebuilds missing GIS/fire infrastructure, and corrects a subsequent orientation-semantics error. These task-level results are then composed into one persistent station model, after which D41 adds **79 accessory meshes spanning 17 inspection-relevant part classes** to both transformer instances and records part/world locations.

We therefore present AstraBuild as a **long-horizon 3D engineering agent case study**, rather than as a model leaderboard or a claim of survey-grade autonomous reconstruction. The central finding is that a general-purpose model can repeatedly operate a structured reconstruction process—reasoning over heterogeneous evidence, revising geometric abstractions after failure, preserving external engineering memory, and integrating many task-level outputs into a component-level industrial digital twin.

---

# 1. Introduction

Modern photogrammetry and neural scene reconstruction can recover rich appearance and geometry from image collections [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians]. Industrial digital twins, however, often require a different representation. Downstream inspection, simulation, asset maintenance, and change management benefit from models that remain **editable, componentized, reusable, semantically addressable, and traceable over time**. A fused surface can show where an object is, but it does not by itself state which pieces belong to the same GIS bay, which repeated devices should share a master asset, which connection is site-specific, or how an inspection concept maps to an explicit component.

These requirements become difficult in an operating substation because the evidence is incomplete and heterogeneous. The registered photogrammetric mesh provides global layout and local occupied surfaces but contains holes, fused neighbors, stretched geometry, and insufficient component detail. UAV and ground photographs reveal visible structure but are not uniformly calibrated and do not authenticate every device identity. Engineering inventories and 12MZ records provide expected names and inspection concepts but do not guarantee that corresponding geometry has been reconstructed. Human reviewers can recognize omissions or implausible structures, but requiring them to manually edit Blender vertices would negate much of the value of an agentic workflow.

The Xialin reconstruction project provides a long trace of one reasoning system operating inside this setting. Rather than asking a model to reconstruct one isolated object, the project repeatedly asks the **same agent/harness** to solve different 3D engineering tasks in a shared Blender environment. Early tasks fit arresters and civil boundaries. Later tasks build shared transformer assemblies, capacitor banks, GIS families, bus/conductor systems, buildings, and auxiliary facilities. Still later tasks revisit earlier assumptions after geometric validation or human review exposes omissions and errors. The final artifact is not a folder of independent meshes but one persistent station-scale engineering state.

This structure is closer to recent embodied-agent studies than to a conventional single-object reconstruction benchmark. In embodied-policy reports, one general-purpose policy is exercised across multiple tasks under a shared robot/controller environment [@cheng2026gptpolicy; @su2026astraembodied]. Here, the shared environment is a persistent 3D engineering system: Blender/Python is the actuator; images, coarse geometry, inventories, and prior artifacts form the observation/context; validators provide execution feedback; and the filesystem provides durable external memory.

We therefore ask a single central question:

> **Can one general-purpose reasoning agent operate across heterogeneous component-level 3D reconstruction tasks and compose the resulting assets into a persistent industrial digital twin?**

We organize the evidence at three levels:

1. **Breadth — reconstruction task suite.** What equipment and infrastructure task families can the same agent/harness reconstruct, reuse, connect, or revise?
2. **Depth — behavior under revision.** When validation or review contradicts the current hypothesis, does the workflow merely tune parameters, or can it revise its metric, abstraction boundary, task-selection strategy, or interpretation of feedback?
3. **Scale — long-horizon composition.** Can outputs from many heterogeneous tasks coexist inside one editable station model with shared assets, persistent history, connectivity, coverage auditing, and later semantic augmentation?

This paper is intentionally a **longitudinal single-site case study**. The 38 core batches are not IID trials: later tasks inherit geometry, component libraries, validators, and lessons from earlier tasks. We therefore do not collapse the study into one success rate or infer a causal ranking against models that were never rerun under matched conditions. Instead, we report a reconstruction task suite, task-native quantitative evidence, representative behavioral episodes, and a system-level integration result.

## 1.1 Contributions

This work makes five contributions.

1. **A 3D-engineering-agent formulation with a canonical reconstruction loop.** We cast component-level industrial reconstruction as an evidence-grounded agent loop in which a general-purpose reasoning model proposes programmatic Blender/Python actions, while deterministic execution and validation determine what enters persistent engineering state. The historical workflow separates a stable core from task-specific measurement, routing, coverage, collision, and human-feedback operators.
2. **A heterogeneous reconstruction task suite from one real industrial site.** The historical record spans isolated device fitting, repeated assemblies, reusable GIS families, connected conductor systems, civil structures, auxiliary infrastructure, correction tasks, and inspection-semantic augmentation.
3. **Intermediate engineering evidence as a first-class record.** Measurement profiles, preflight graphics, route/topology diagnostics, clean/overlay/reference sets, validation JSON, manifests, and continuation notes externalize the geometric hypotheses that lead from evidence to a retained or revised model.
4. **Behavioral evidence from preserved failures.** Representative cases show the workflow revising not only geometry but also evaluation domains, reusable-asset boundaries, representation choices, task-selection strategy, and the interpretation of human spatial feedback.
5. **A station-scale compositional demonstration.** The task-level outputs accumulate into a 37k-object editable digital twin with explicit reuse, long-horizon history preservation, coverage accounting, and a later inspection-semantic layer.

---

# 2. Related Work and Research Positioning

## 2.1 Surface reconstruction versus editable engineering representation

Classical structure-from-motion/photogrammetry and modern neural scene representations solve important perception problems [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians]. Their outputs, however, do not automatically supply engineering structure. An industrial model must often encode repeated equipment families, instance relationships, finite site-specific connectors, explicit component identities, and a history of later corrections.

AstraBuild therefore treats the photogrammetric reconstruction as **evidence and spatial context**, not as the final representation. The target artifact is an editable Blender scene with component collections, reusable masters, site instances, explicit connections, review views, provenance records, and later semantic mappings.

## 2.2 Programmatic 3D agents and general-purpose models as tool users

Language and vision-language models can synthesize executable programs and operate structured tool interfaces [@liang2023code; @huang2023voxposer]. In 3D generation, 3D-GPT decomposes procedural modeling into task-dispatch, conceptualization, and modeling agents that ultimately emit Python/Blender operations [@sun2023threegpt]. SceneCraft is closer to AstraBuild at the execution level: it plans a scene graph, translates spatial relations into numerical constraints and Blender-executable Python, evaluates rendered outputs with a visual reviewer, iteratively refines the scene, and distills reusable functions into a library [@hu2024scenecraft].

AstraBuild differs in problem direction and evidence regime. 3D-GPT and SceneCraft primarily synthesize scenes from language descriptions; AstraBuild performs **reverse engineering from registered physical evidence**. Its intermediate artifacts are therefore not only rendering feedback. They include metric profiles, local reference domains, conductor-route fits, collision/coverage diagnostics, history-preservation checks, and frozen revisions whose purpose is to constrain an evolving industrial model.

GPT-Policy is especially relevant because it separates context construction, model decisions, constrained execution, feedback-driven replanning, and append-only run recording [@cheng2026gptpolicy]. The GPT-6 Astra embodied-policy report similarly studies one general-purpose model across multiple tasks in a common embodied environment and analyzes representative behavioral episodes rather than only final aggregate scores [@su2026astraembodied].

AstraBuild adopts the same **agent-centric experimental viewpoint**, but the environment and time horizon differ. The model does not output robot actions; it writes and revises reconstruction programs, inspects renders and validation results, and operates over an engineering history spanning many task families and saved artifacts.

## 2.3 Task suite, not IID benchmark

The historical sequence contains many equipment and infrastructure reconstruction cases, but they are not statistically independent episodes. The same Blender scene, component libraries, validators, and history persist across tasks. We therefore use each equipment/infrastructure family as a **task instance in a shared persistent environment**, analogous to one embodied policy being exercised on heterogeneous tasks, while explicitly avoiding an IID success-rate interpretation.

---

# 3. AstraBuild: A Persistent 3D Engineering Agent

## 3.1 Reconstruction state and evidence context

Let the persistent engineering state after task/batch \(t\) be

\[
S_t=(M_t,A_t,H_t,X_t),
\]

where \(M_t\) is the editable Blender scene, \(A_t\) the reusable asset/instance hierarchy, \(H_t\) the accumulated external engineering history, and \(X_t\) semantic/inspection mappings.

For each task, an evidence compiler constructs a bounded context

\[
C_t=\mathcal{C}(G,I,R,U,H_t),
\]

from photogrammetric geometry \(G\), field images \(I\), engineering/semantic records \(R\), spatial priors \(U\), and prior history \(H_t\). The reasoning agent proposes an operation

\[
a_t\sim\pi_{\mathrm{Astra}}(\cdot\mid S_t,C_t,f_{t-1}),
\]

which a deterministic Blender/Python layer materializes. Task-specific validation then decides whether the result becomes persistent state, is revised, or is retained as a failed/limited artifact.

![Figure 1 — AstraBuild closed-loop 3D engineering agent.](../figures/fig01_agentic_loop.png)

**Figure 1.** Study overview. Field imagery, registered coarse geometry, engineering records, and prior history form the evidence context. The same Astra/Codex engineering agent repeatedly proposes and revises programs; validated component models accumulate into one editable station state.

## 3.2 Recurring evidence types

The workflow repeatedly combines five evidence classes:

- **registered photogrammetric geometry:** global layout, local reference surfaces, rough metric scale, and unexplained occupancy;
- **UAV/ground photography:** visible part form, count, ordering, orientation, and appearance;
- **inventory/12MZ records:** expected device identities, semantic groups, and inspection concepts;
- **UE/manual spatial priors:** position hypotheses and cross-checks;
- **human review + prior artifacts:** equivalence authorization, omission reports, image markup, previous failures, manifests, and unresolved limitations.

These sources have different epistemic roles. In particular, a coarse mesh used to guide reconstruction cannot simultaneously be treated as independent survey truth for the same residual measurement.

## 3.3 Programmatic action space

The agent primarily acts by generating or revising Python code that manipulates Blender. Recurrent actions include extracting local reference geometry, creating parametric subcomponents, constructing shared `MASTER` collections, instantiating site equipment, generating finite connectors/conductor paths, fitting transforms, rendering review views, computing validation quantities, quarantining suspect objects without deleting provenance, and freezing immutable outputs.

This makes the model a **reconstruction operator over an engineering API**, rather than a one-shot vertex generator.

## 3.4 Worked example: B32 as an observable agent–tool trace

A generic loop is difficult to interpret without first seeing what one reconstruction task actually contains. B32 is a useful worked example because its historical folder preserves the inherited state, measurement scripts, diagnostic figures, three geometry revisions, componentized Blender output, fixed-camera comparison renders, an interactive review page, an independent validator, and the continuation record used by the next task.

A crucial provenance boundary is that the historical batches **do not preserve GPT-6 Astra's private chain-of-thought**. We therefore do not claim to reconstruct an internal reasoning transcript. What the artifacts do preserve is an **observable engineering decision trail**: which evidence was selected, which measurement or Blender program was written/revised, what deterministic program output was produced, what review/validation evidence contradicted the current representation, and what changed in the next revision.

![Figure 2 — B32 worked example with explicit inputs, agent decisions, deterministic tools, revisions, review and validation.](../figures/fig12_b32_worked_example.png)

**Figure 2.** One concrete reconstruction task. B32 turns field imagery and inherited registered civil geometry into an editable cabin model through an explicit evidence → hypothesis → program → review → validation trace. The figure separates the agent's decisions from deterministic computation, rendering, and validation.

| Phase | Why this phase exists | Input | Observable Astra/Codex role | Deterministic execution and output |
|---|---|---|---|---|
| Freeze inherited state | B31 left the two secondary-equipment cabins unresolved, but earlier station work must not be overwritten | frozen B31 `.blend`, manifest, protected hashes | select B32 scope and preserve prior state | `prepare_B32.py` checks hashes/stats and writes `inputs_B32.json` |
| Measure cabin envelope | screenshot appearance alone is insufficient for metric pose/size | `B31_vertical_samples.npz` and the B31 station frame | choose separate rectangular fits for C110/C220 and a fit/comparison split | SciPy soft-L1 least squares fits wall datums; Matplotlib writes façade diagnostics; `B32_container_measurements.json` stores width, length, yaw and root transform |
| Diagnose visible details | fitted walls do not determine door count, side or position | low-height registered coarse slices plus field photographs, including the reviewed DSC3140 view | interpret stair/door evidence and revise the representation | `inspect_B32_steps.py` writes `B32_source_steps_diagnostic.png`; review evidence drives R1→R2→R3 door corrections |
| Build componentized geometry | accepted measurements must become editable reusable structure | measurement JSON, revised door parameters, inherited B31 scene | write/revise the Blender construction program and decide reuse boundaries | `build_B32_r3.py` creates shared `B32_CABIN_END_WALL_HVAC_MASTER` and `B32_CABIN_DOOR_MASTER`, separate C110/C220 cabin masters and rigid SITE instances; writes station/component `.blend` files and 27 renders |
| Same-camera review | one attractive render cannot reveal correspondence errors | eight fixed cameras over the saved model and local registered reference | interpret clean/overlay/reference mismatch as revision evidence | Blender renders 8 views × Clean/Overlay/Reference; `review_B32.py` packages 25 embedded images into `B32_review.html` with mode switching and a split slider |
| Validate and freeze | only checked artifacts should enter the next persistent state | saved B32 model, inherited B31 state, fixed comparison triangles and asset library | react to failed checks through another revision rather than silent acceptance | `validate_B32_r3.py` recomputes inherited-state preservation, facade residuals, door opening/stair constraints, camera framing and asset round-trip; writes `B32_validation_r3.json`, after which manifest/release/continuation artifacts become external memory |

The input/output chain is therefore concrete rather than metaphorical. For the envelope fit,

`B31_vertical_samples.npz → measure_B32_containers.py → B32_container_measurements.json + C110/C220_facade_diagnostic.png`.

For the door correction,

`registered low-height geometry + photographs → inspect_B32_steps.py → B32_source_steps_diagnostic.png → revised build program`.

For review,

`saved Blender geometry + local registered reference + fixed camera → Clean / Overlay / Reference → B32_review.html`.

The review chain materially changed the representation. R1 placed one door on each cabin and put the C110 door on the wrong side; R2 moved C110 to the east side but retained one C220 west-side door; R3 uses one C110 east-side door at local Y≈−3.90 and two C220 west-side doors at approximately −5.50 and +5.32, with wall panels/joints clipped around the openings. The continuation record explicitly notes that a C220 middle depression previously interpreted as a door was rejected after photographs and two stair-platform signatures contradicted it.

The final validator records preservation of 34,191 inherited objects, 7,114 prior station-object transforms and 2,953 protected previous files, while also checking four shared end/HVAC module instances, three door instances, eight review-camera envelopes and fixed odd-triangle facade comparison domains. These checks remain comparisons to a correlated registered reconstruction, not independent survey truth.

The original `B32_review.html` is therefore part of the experimental method, not merely a presentation page. It exposes eight directions and three comparison modes under matched cameras, allowing the reviewer to switch between the generated component model, cyan model/reference overlay and reference-only geometry. The companion website embeds this historical page directly rather than recreating only selected screenshots.

## 3.5 Historical review protocol across device cases

B32 is not an isolated review mechanism. The publication catalog identifies **32 formal batches with original `review.html` pages from B07 through D38**. These pages were generated during the corresponding experiments and embed their own Blender renders. They therefore provide a task-level review protocol that is unusually consistent across otherwise heterogeneous equipment.

The details vary by task, but the recurring interface is the same: a named equipment/view selector; the modeled geometry under a fixed camera; the registered photogrammetric reference under the same camera; an overlay or split-slider comparison; and batch-specific notes about what is modeled, what is still uncertain, and which validation quantities are meaningful. B07 compares the earlier transformer candidate with the revised B07 model and the same coarse reference. B08 switches between T1/T2 and their same-camera coarse comparisons. B09/B10 let the reviewer select individual capacitor-bank groups and switch among `Clean`, `Compare`, `Overlay`, and `Reference`. Later GIS, conductor, civil and correction batches retain the same principle while adding task-specific views and diagnostics.

![Figure 3 — Representative original review triplets across transformer, capacitor-bank and GIS tasks.](../figures/fig13_review_protocol.png)

**Figure 3.** Representative `Clean / Overlay / Reference` views extracted from the original B07, B08, B09 and B17 review artifacts. The companion website does not stop at this static sample: it directly exposes all 32 historical review pages, preserving each batch's original selectors, sliders, modes, explanatory text and limitations.

This review protocol is important for the paper's case-study framing. Each device task is not evidenced only by a final render; the reader can inspect the model against the coarse reconstruction using the same review interface that was produced at the time of the batch. The review page is therefore part of the experiment record, while the process dossier adds the upstream measurement/preflight/diagnostic files and downstream validation/manifests around it.

## 3.6 Canonical reconstruction loop with task-specific operators

The historical B01–B36 scripts and output folders support a more specific process model than a generic “reason → code → validate” loop. The recurring core is:

1. **freeze/prepare the inherited state** and protect prior artifacts;
2. **extract a registered local reference** and select relevant photographs/records;
3. **inspect and plan** the representation to build;
4. **build/refine** geometry, reusable masters, site instances, or finite connectors;
5. **render review evidence**, typically clean/overlay/reference views under controlled cameras;
6. **validate/audit** task-native geometry, contact, continuity, history, coverage, or interference conditions;
7. **freeze the batch and externalize memory** through manifests, release records, failed revisions, and `CONTINUE_FROM_Bxx` notes.

This is a **canonical core, not a rigid identical pipeline**. A filename-level operational audit of B01–B36 installation scripts finds `build` and `validate` in 36/36 batches, `prepare` in 29/36, `extract` in 27/36, `audit` in 20/36, `plan` in 19/36, `measure` in 17/36, and `inspect`/`refine` in 16/36 each. These are workflow-record counts rather than success rates. Measurement/profile fitting, representation preflight, route fitting, coverage audit, collision checks, and human-markup registration appear only on the subsets that need them. The workflow therefore behaves more like a common engineering harness with task-specific operators than a fixed sequence of image-processing blocks.

![Figure 4 — Canonical reconstruction loop and task-specific operators.](../figures/fig11_canonical_workflow.png)

**Figure 4.** The stable core carries state from one task to the next. Specialized operators are activated by the equipment geometry or by a failure: B23 uses profile/preflight evidence, B20 route diagnostics, B25 structural profiles and coverage reasoning, and D38 human spatial markup.

## 3.7 Intermediate engineering evidence is part of the method

Several batch folders make the hidden reasoning state unusually concrete. B23 contains `B23_measurement_profiles.png`, `component_and_lead_preflight.png`, a 3,800-line plan describing fitted geometry, clean/overlay/reference render triplets, multiple manifests and validations, and retained r1/r2/r3 revisions. B20 records route/topology diagnostics before connecting the 220 kV bus row. B25 stores truss profiles and fixed comparison domains before adding the large gantry system. B29 records strain profiles and jumper/crossline fits before conductor construction.

These files are method evidence rather than presentation ephemera: they record **which geometric hypothesis was under consideration and what evidence changed it**. For this reason, the companion website exposes per-batch process dossiers instead of showing only the final station render.

## 3.8 Reusable assets are explicit hypotheses

A mature task separates shared device geometry from site-specific geometry:

`MASTER geometry → reusable submodules → rigid SITE instances → finite site-specific connectors`

This is not only an efficiency mechanism. A shared master encodes the hypothesis that two installations are equivalent for the purposes of the model. If later evidence contradicts that assumption, the abstraction itself must change. B15 provides a direct example in which finite bus geometry is removed from a shared GIS master.

## 3.9 Validators and external memory

The technical record documents at least eleven recurring validation mechanisms: history preservation, site-transform preservation, SHA-256 protection, save/reopen checks, finite geometry, manifest replay, BVH reference-surface comparisons, contact/support/endpoint continuity, camera framing, rigid-instance checks, and occupancy/coverage audits.

The filesystem is also the practical long-term memory of the agentic process. Plans, builders, validators, manifests, review renders, failed drafts, continuation notes, and explicit limitations allow later tasks to reason over what happened earlier without relying on transient conversational memory.

---

# 4. Reconstruction Task Suite

## 4.1 Task definition

We reinterpret the B/D history as a suite of heterogeneous reconstruction tasks solved by one persistent agent/harness. Each task consists of a target equipment/infrastructure family, a bounded evidence package, an allowed Blender/Python action space, and task-native validation criteria. Tasks share the same evolving engineering state and are therefore not IID.

## 4.2 Task families

| Task family | Historical batches | Representative target/output | Capability exercised | Representative recorded evidence |
|---|---|---|---|---|
| Surge-arrester fitting | B01–B05, B18 | SA110/SA220 bodies and installation | local fitting, pose/scale, held-out checking | B01 preserved failure; B02 naked-shaft RMS 1.8–3.4 cm under revised domain |
| Wall and gate | B06 | station wall + gate | large civil geometry from coarse reference | east-wall median reference distance 7.87 m→0.015 m |
| Transformer reconstruction | B07–B08 | two main transformers | complex assembly and reusable abstraction | shared T1/T2 assembly; bank median ~0.01 m; T2 front P95 0.62 m tail retained |
| Capacitor-bank reconstruction | B09–B10 | six 35 kV capacitor groups | repeated structures and local assemblies | 18 lane medians 0.6–2.4 cm; first broad outdoor coverage audit |
| 110 kV GIS/device families | B11–B16 | GIS bays, arresters, bus-tie/VT structures | reusable families and variants | B13 creates seven GIS sets with ~2,400 expanded meshes |
| 220 kV GIS/outgoing families | B17–B19 | outgoing bays and variants | cross-family reuse and complex topology | B17 75 local checks: 50 pass / 25 retained non-pass |
| Bus and conductor systems | B20–B30 | busbars, drops, insulator strings | explicit connectivity and flexible paths | ~88.8 m busbar; 804 discs; endpoint continuity ~1e-6 m scale |
| Building and ground | B31–B34 | main building + ground | large structured civil reconstruction | building 946 components; ground ~10,182 m²; wall-domain RMS 1.8–3.2 cm |
| Auxiliary facilities | B35–D37 | CCTV, fence, bus racks, floodlights, manholes | long-tail infrastructure and revision | B35 multi-revision path; later omission audit triggers B36 |
| Human-guided correction | B36, D38 | missing bus rack; false cabinets; missing GIS/fire room | history search, markup-to-3D correction | B36 multi-revision recovery; D38 NCC 0.94/0.92 and coordinate-grounded correction |
| Presentation invariance | D40 | PBR material layer | modify appearance while preserving geometry | 37,153 objects / 29,986,649 vertices unchanged |
| Inspection-semantic augmentation | D41 | transformer inspection accessories | part-addressable semantic augmentation | 79 accessory meshes, 17 selected missing classes × T1/T2; validation `ok=true` |

The table is the main **breadth result**: one persistent agent/harness is exercised across qualitatively different 3D engineering regimes rather than being demonstrated on a single object type.

![Figure 5 — Task breadth, persistent state, and system-level composition.](../figures/fig09_task_suite_composition.png)

**Figure 5.** The paper’s central organization: heterogeneous reconstruction tasks feed a persistent engineering state, and the resulting assets compose into a station-scale digital twin. Breadth, behavioral depth, and system-level scale are distinct forms of evidence.

## 4.3 Longitudinal progression

The task suite also changes over time. Early work focuses on local fitting and device families; later work emphasizes connected systems, coverage-driven omission discovery, human correction, and semantics. Because later tasks inherit earlier artifacts and protocol changes, chronology matters and is retained as part of the evidence.

---

# 5. Task-Level Evidence

## 5.1 Breadth and engineering scale

At the D38.2/D40-equivalent layer, the project contains **37,153 objects, 755 scenes, 858 collections, 3,916 mesh datablocks, and 29,986,649 vertices**. The technical report summarizes reconstructed coverage including **48 arrester bodies, 8+3 GIS bays, two main transformers, six capacitor groups, approximately 88.8 m of busbar, 804 insulator discs, approximately 10,182 m² of ground surface, and a 946-component main building**, in addition to auxiliary facilities and later D38 corrections.

These counts do not imply that every physical object is independently verified. They demonstrate the breadth of engineering operations carried out by one persistent reconstruction process.

## 5.2 Internal geometry ledger

The technical summary contains **1,550 current surface-comparison records** with median/p90/p95 residuals of **0.036/0.084/0.116 m**. A separate 5 cm screen retains **149 passing and 101 non-passing** items. Non-passing evidence remains in the historical accounting rather than being deleted to produce a uniformly favorable final statistic.

Because the comparison surface is the same registered photogrammetric mesh that also supplies reconstruction evidence, these values describe **internal reference agreement**, not independent survey accuracy.

![Figure 6 — Quantitative evidence.](../figures/fig03_quantitative_evidence.png)

**Figure 6.** Geometry residuals, retained validation-screen items, and coverage-gap measurements answer different engineering questions and are therefore reported separately.

## 5.3 Reuse as a persistent-system property

The final layer contains 37,153 scene objects backed by 3,916 mesh datablocks, giving a descriptive object-to-mesh ratio of approximately **9.5×**. This is not a labor-speed or compression metric. It indicates that repeated equipment is increasingly represented through shared geometry and instances.

B08 is the clearest example: after an explicit user authorization that the two transformer component assemblies can be treated as equivalent, the workflow creates a common master and T1/T2 site instances. Later GIS, arrester, and insulator tasks extend this reuse principle, while B15 shows that invalid reuse boundaries must be revised.

## 5.4 Coverage becomes a task-selection signal

B25/B26 marks an important transition. Instead of asking only which inventory entry is unresolved, the workflow asks where selected high-region coarse geometry remains unexplained by the component model. In that audit:

- the fraction of selected samples more than 1 m from modeled geometry changes from **78.8% to 14.6%**;
- the selected GIS220 high-region median changes from **8.12 m to 0.15 m**;
- the selected transformer high-region median changes from **3.15 m to 0.06 m**.

The significance is not absolute metric accuracy. The reference scene becomes an **active sensor for omission discovery and task selection**.

---

# 6. Case Studies of Agent Behavior

The task table demonstrates breadth. The following episodes demonstrate **behavioral depth**: they show how the workflow changes after validation or human feedback contradicts the current hypothesis.

![Figure 7 — Failure and recovery cases.](../figures/fig05_failure_recovery.png)

**Figure 7.** Representative failures alter later evaluation protocol, reusable abstractions, reconstruction logic, or feedback interpretation rather than being silently discarded.

## 6.1 B01→B02: the evaluation domain is itself a hypothesis

B01 installs three arrester candidates. Source hashes and transform checks pass, but held-out cylindrical-domain RMS values of approximately **0.048, 0.073, and 0.051 m** violate the selected 5 cm screen. The batch is retained as failed.

The diagnosis is not merely that model parameters are wrong. The comparison domain mixes the target shaft with protruding accessory geometry. B02 therefore separates fitting and holdout regions, and the historical notes explicitly state that the revised metric should not be presented as a directly comparable accuracy improvement over B01.

**Interpretation.** The workflow can revise the *measurement protocol* after diagnosing a failure while preserving the original failed result.

## 6.2 B08: from one device to a reusable engineering abstraction

B07 reconstructs only part of the #1 transformer exterior. After the user explicitly authorizes the two transformer assemblies to be treated as equivalent, B08 introduces a shared transformer `MASTER` and site-specific T1/T2 instances.

The result is more than duplicated geometry: later structural edits can propagate consistently. At the same time, the validation history keeps a T2-front P95 residual tail of approximately **0.62 m** rather than allowing the otherwise small bank-distance summary to hide it.

**Interpretation.** The workflow can promote a successful local reconstruction into a reusable asset abstraction while retaining evidence that challenges parts of the fit.

## 6.3 B15: the reusable abstraction is wrong

B15 reconstructs reserve GIS equipment and undergoes multiple revisions. One local measurement procedure is contaminated by neighboring equipment. Separately, the first shared bus-spool design extends the same finite geometry across installations whose physical extents differ, creating overlaps with adjacent equipment.

Recovery therefore changes two levels simultaneously: the measurement method and the **MASTER/site boundary**. Site-specific finite bus segments are removed from the shared master; obsolete supports are archived rather than silently overwritten.

**Interpretation.** A reusable component library is a geometric hypothesis, not merely a software convenience, and that hypothesis can be falsified by field evidence.

## 6.4 B23: process evidence changes the representation

B23 reconstructs the transformer neutral-side mechanisms and leads. An earlier preflight inherited from B22 effectively treated a connection as a simple straight segment. Direct inspection of the registered coarse geometry instead reveals a mid-span bow of roughly half a meter. The batch therefore bins the observed geometry, extracts control points, fits a smooth curved path with fixed endpoints, and refines the shared mechanism and soft connections.

The revision history is informative. The first reconstruction worsens one validation domain because older geometry had accidentally covered part of the soft connection; r2 explicitly adds the soft lead, and r3 adds lower bridge contact. The final record evaluates 32 fixed triangle domains, with 30 meeting the selected 5 cm screen and two retained misses. The process folder preserves `B23_measurement_profiles.png`, `component_and_lead_preflight.png`, the fitted plan, render triplets, manifests, and validation files.

**Interpretation.** Intermediate measurement and preflight artifacts can change the *class of geometry being built*, not merely its parameters. In this case, observed curvature invalidates the simpler representation and causes a new path model plus subsequent contact revisions.

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

![Figure 8 — D38 human-feedback chain.](../figures/fig06_d38_human_feedback.png)

**Figure 8.** Sparse 2D markup is transformed into a traceable sequence of registration, coordinate inference, diagnosis, quarantine/rebuild, and review.

**Interpretation.** The system can convert high-level human spatial feedback into programmatic correction while retaining the history of both the original generation error and an intermediate correction error.

---

# 7. System-Level Demonstration: From Tasks to a Station Digital Twin

The strongest system-level result is not any one device reconstruction. It is that outputs from many heterogeneous tasks persist inside one Blender project and eventually form a connected, reviewable, and semantically extensible station model.

## 7.1 Long-horizon engineering trace

The core history contains **38 reconstruction batches, 54 build scripts, 58 validation scripts, 150 manifests, 71 validation JSON files, 28 installation-queue revisions, and 109 local coarse-reference NPZ crops**. By the later B35-era chain, the technical report records **2,859+ protected-file hashes**. These artifacts provide a durable trace across which later tasks reuse previous components and inspect previous failures.

At D38.2/D40 scale, the integrated project contains **37,153 objects, 755 scenes, 858 collections, and 3,916 mesh datablocks**.

## 7.2 Composition is more than concatenating meshes

The station-scale result requires cross-task consistency:

- device families must remain shared where equivalence is justified;
- finite site-specific connections must remain outside globally shared masters;
- previous transforms and objects must survive later batches;
- bus/conductor endpoints must remain connected to equipment introduced in earlier tasks;
- new tasks must not silently overwrite historical outputs;
- coverage audits must expose structures never introduced as explicit semantic tasks;
- human corrections must modify the active model while preserving the rejected geometry in history.

These constraints make the integrated station a stronger demonstration than a gallery of independent object meshes. It tests maintenance of **persistent engineering state over a long task horizon**.

## 7.3 Layered endpoint

The version boundary remains explicit:

- **D38.2:** principal reconstructed station geometry after the D38 correction loop;
- **D40:** material/presentation layer validated to preserve geometry, transforms, object counts, and vertex counts;
- **D41:** additive transformer inspection-semantic accessory layer.

Separating these layers prevents a better-looking render from being misreported as new geometry and prevents later semantic additions from being back-projected into earlier results.

---

# 8. From Integrated Geometry to Inspection Semantics

Once geometry stabilizes, the project builds semantic mappings as a separate layer. At station level, the current part map contains **151 devices**. Among **106 official names**, **76 are attached** and **30 remain unmatched** rather than being forced onto uncertain geometry.

For the #1 transformer pilot, **189 semantic meshes** are grouped into **26 part classes**. The official **36 inspection concepts** are categorized as **31 model-part points, 4 external-component points, and one non-visual operating-sound concept**. A later semantic audit also identifies incorrect attachments caused by naïve string/box logic, including cross-bay bus tubes and misidentified arresters/switches, and revises them instead of forcing semantic completeness.

## 8.1 D41: inspection-addressable transformer accessories

The B08 transformer assembly captures major station-visible structure but lacks several inspection-relevant accessories present in the semantic transformer group. D41 selects **79 accessory meshes covering 17 missing inspection-relevant part classes**, aligns them to the B08 tank frame, stores them as one shared accessory collection, and instantiates that collection into both T1 and T2 using the existing site transforms.

The recorded D41 validation reports `ok=true`, including 79/79 structure/count checks and 17/17 selected class coverage for both transformer instances. The batch also writes part/world-location records.

![Figure 9 — D41 inspection-semantic augmentation.](../figures/fig07_d41_inspection_semantics.png)

**Figure 9.** The final study layer demonstrates a path from heterogeneous reconstruction tasks and station-level composition to component-addressable inspection semantics.

---

# 9. Discussion

## 9.1 Breadth, depth, and scale are complementary evidence

The existing project is strongest when interpreted through three complementary lenses.

**Breadth:** one agent/harness is exercised across 12 qualitatively different reconstruction task families.  
**Depth:** preserved failures show the workflow revising its metric, abstraction, task selection, and feedback interpretation.  
**Scale:** outputs from those tasks persist and interact inside one station-level engineering artifact.

No single metric captures all three.

## 9.2 What is actually demonstrated?

The current evidence does not establish that GPT-6 Astra is the best 3D reconstruction model, nor that the station is reconstructed fully autonomously. A narrower and better-supported claim is:

> **A general-purpose reasoning model can serve as a persistent 3D engineering agent across heterogeneous reconstruction tasks when its actions are mediated by programmatic tools, explicit evidence, deterministic validation, and external engineering memory.**

The task suite supports the breadth of this claim; the case studies explain behavior under failure; the integrated station supports long-horizon composition.

## 9.3 Why the analogy to embodied-agent reports is useful

The reporting logic parallels embodied-agent studies without copying their statistics:

| Embodied-agent study | AstraBuild |
|---|---|
| shared robot/controller environment | shared Blender/Python engineering environment |
| observation/context | images, coarse geometry, inventories, history |
| general-purpose policy/reasoner | GPT-6 Astra reasoning |
| action interface | Blender/Python reconstruction operations |
| execution feedback | validators, overlays, geometric checks |
| task suite | equipment/infrastructure reconstruction families |
| representative behavior episodes | B01, B08, B15, B23, B25/B26, B36, D38 |
| long-horizon demonstration | full-station compositional digital twin |

The analogy stops where the data differ: these are not repeated randomized robot episodes, task validators are heterogeneous, and later tasks inherit earlier state.

## 9.4 Failure preservation is part of the result

B01 fails its selected screen; B15 requires multiple abstraction revisions; B17 keeps 25 non-passing checks out of 75 local checks; B29 separates excellent endpoint continuity from large residuals caused by still-missing neighboring structures; D38.1 introduces an orientation-semantics error before D38.2 fixes it.

These episodes should remain visible in the main paper. They show how fluent model reasoning can be wrong, and why deterministic verification and traceable revision are necessary for engineering use.

---

# 10. Limitations and Next Research Decisions

## 10.1 Single-site external validity

All task families come from one substation. Diversity within one site does not establish transfer to a different station, vendor, climate, or data-acquisition protocol.

## 10.2 No independent survey reference

The headline centimeter-scale residuals compare reconstructed geometry with the same photogrammetric mesh that also guides reconstruction. They are **not independent survey accuracy**.

## 10.3 Heterogeneous task-native validators

Different equipment families require different checks. This is appropriate for an engineering case study but prevents the current suite from being reduced to one stationary benchmark success rate.

## 10.4 Human steering is material

B08 equivalence authorization, B36 omission review, D38 image markup, and semantic audit all influence the reconstruction trajectory. The supported claim is therefore **agent-driven, human-steerable reconstruction**, not full autonomy.

## 10.5 Historical model provenance is owner-confirmed

The original batch logs do not freeze the model identifier/reasoning effort. Future controlled studies should log model/version, reasoning setting, tool versions, evidence manifest, token usage, wall-clock time, human intervention, and output hashes per run.

## 10.6 Controlled comparisons remain a future design choice

The historical data do not contain matched reruns with another foundation model, a specialized 3D model, a no-image/no-coarse ablation, or a professional human CAD baseline. Which comparison would most strengthen the paper depends on the intended research venue and should be decided after the core positioning is agreed.

---

# 11. Conclusion

AstraBuild documents one general-purpose reasoning model operating across a broad sequence of real 3D engineering tasks. The process begins with local device fitting and grows into reusable equipment hierarchies, repeated assemblies, complex GIS families, connected conductor systems, civil structures, auxiliary facilities, omission recovery, human-markup-driven correction, and inspection-semantic augmentation. Crucially, the history preserves not only final geometry but also intermediate profiles, diagnostics, review renders, validators, and failed revisions that make the engineering trajectory inspectable.

Individually, these are heterogeneous reconstruction case studies. Together, they provide evidence of a different capability: a reasoning model operating a **persistent engineering process** in which prior geometry, failures, abstractions, validators, and human feedback influence later tasks. The final 37k-object station model is therefore not merely a larger reconstruction output; it is a system-level demonstration that many task-level results can be maintained, revised, connected, and composed over a long horizon.

The remaining research decision is not yet which competing model to run. It is how to position this existing evidence most effectively—as a case study of general-purpose agentic 3D engineering, as an industrial digital-twin systems paper, or as a reconstruction paper that would require additional controlled geometric evaluation. That choice should determine the next experiment rather than the other way around.

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

Use the existing `references.bib`. The framing references most relevant to the advisor discussion are GPT-Policy [@cheng2026gptpolicy], the GPT-6 Astra embodied-policy technical report [@su2026astraembodied], RoboDojo [@chen2026robodojo], SceneCraft [@hu2024scenecraft], 3D-GPT [@sun2023threegpt], foundational photogrammetry/neural-reconstruction work [@schonberger2016sfm; @mildenhall2020nerf; @kerbl2023gaussians], and programmatic/tool-using model work [@liang2023code; @huang2023voxposer].
