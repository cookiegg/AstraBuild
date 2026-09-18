# §7.2 Evidence Map — Three transitions in the reconstruction problem

## Status and scope

Working evidence map for the B01–B36 rewrite. This document supports §7.2 of `04_OUTLINE_V2_MATURE.md`. It is not manuscript prose and should remain more explicit than the final paper.

Empirical boundary: **B01–B36 only**.

Primary claim served by this section (C2):

> Across the B01–B36 sequence, local fitting remains part of the workflow, but the required operator portfolio broadens as reconstructed elements become more interdependent. Repeated equipment introduces reusable-asset boundaries; connected systems introduce ports, routes, flexible paths, and topology constraints; later closure introduces coverage-based omission discovery and integration constraints imposed by the accumulated scene.

Interpretive limit:

- descriptive longitudinal claim, not a causal complexity law;
- no claim that Astra learned over time;
- no claim that later batches are uniformly harder on one common scale;
- no attribution of numerical fitting precision to the language model;
- no global success-rate or station-accuracy claim.

---

# 7.2 opening paragraph

## Reader function

Explain why the operator heatmap in §7.1 needs mechanism-level evidence. The paragraph must make clear that the key result is not chronology itself, but a change in the *structure of the reconstruction decisions* as dependencies accumulate.

## Narrow claim

The build–validate backbone remains recognizable, but three recurring changes in task structure introduce additional decision layers: reusable scope, connected representation, and residual-work selection under inherited state.

## Authorized evidence

- filename-level stage audit: B01–B06 dominated by fit; B07–B19 recurring measure/plan/refine/audit/review; B20–B30 recurring inspect/plan plus route/coverage artifacts; B31–B36 measurement/review plus late interference handling;
- direct artifacts below provide the substantive evidence.

## Inference limit

The stage audit is descriptive and depends on historical file/script naming. It may orient the reader but cannot establish causality, model learning, or task difficulty.

## Bridge

Move immediately to the first transition: a local fit can be solved once its comparison domain is defined; repeated equipment adds the separate question of what geometry may be reused.

---

# 7.2.1 From fitting geometry to defining reusable scope

## Paragraph 1 — local-fit baseline: B01/B02

### Function

Establish the simplest reconstruction decision in the sequence: define a local comparison domain, then let deterministic code solve the pose/fit.

### Claim

In the early installation tasks, a major modeling decision is the definition of the geometry to be compared. B01/B02 shows that changing the comparison domain can change the validation outcome without changing the underlying manufactured asset.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B01.md`

- lines 26–31: frozen P02 source asset reused; body/pedestal only in the installation trial;
- lines 43–45: one shared scale is applied; no per-device scaling;
- lines 59–65: registered target crop and explicit source indices; crop is not independent segmented ground truth;
- lines 77–88: broad support-source holdout includes protruding attachments/irregular coarse surfaces; RMS 0.0484 / 0.0732 / 0.0510 m; 5 cm internal screen fails for the batch; failure preserved.

`photo-first-pilot/CONTINUE_FROM_B02.md`

- lines 21–25: same frozen source geometry retained; accessories independently posed; no source mesh deformation;
- lines 27–31: B02 evaluates bare-shaft train/validation domains and explicitly states that the revised values are not an apples-to-apples accuracy improvement over B01.

### Development

The scientific point is not that B02 is "more accurate" than B01. The measurable change is that the workflow reformulates what counts as the target shaft surface. Once that domain is fixed, the residual is produced by deterministic geometry code.

### Boundary

Do not say B01→B02 demonstrates learning, improved reasoning accuracy, or an unbiased holdout comparison. The two checks use different domains and the source is the same coarse reconstruction family.

### Bridge

This local-fit formulation is sufficient while each installation can be treated independently. Repeated equipment adds a new reconstruction variable: which geometry should be shared across sites and which should remain installation-specific.

---

## Paragraph 2 — reuse becomes an explicit representation decision: B08

### Function

Show the first clear move from independent fitting toward a reusable component/site decomposition.

### Claim

B08 makes the reuse boundary explicit: manufactured/exterior component structure is shared between two transformers, whereas conductor routes and site pose remain installation-specific.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B08.md`

- lines 10–19: user explicitly authorizes T1/T2 component equivalence; position and external conductors remain site-specific;
- lines 21–28: one `B08_TRANSFORMER_MASTER`; T1/T2 site roots reference the same collection; `B08_T1_SITE_LEADS` and `B08_T2_SITE_LEADS` remain outside the master;
- lines 30–33: master contains 473 direct meshes and 47 nested instances; each site expands to 1606 meshes;
- lines 70–75: T2 receives a rigid correction; no T2-only shape/scale/component adjustment.

`output/installation_B08/B08_validation_r2.json`

- lines 16–20: one shared master, two shared roots, rigid site instances, edit propagation checked;
- lines 21–35: master/expanded counts, site conductor meshes, independently traced routes, asset roundtrip identical.

### Development

The relevant decision has changed. The workflow no longer needs only a local pose and dimensions; it must encode a hypothesis about invariance across installations. That hypothesis determines what edits should propagate and what geometry must remain local.

### Boundary

The equivalence was human-authorized. Do not claim the model independently inferred transformer equivalence from data. Do not infer efficiency gain because there is no non-reuse baseline.

### Bridge

Once reuse is treated as a representation choice, it can also be wrong. B15 provides the direct counterexample.

---

## Paragraph 3 — the reuse boundary is falsifiable: B15

### Function

Demonstrate that the shared/site boundary affects physical correctness, not just code organization.

### Claim

B15 shows that finite installation geometry cannot always be placed in a common equipment master. An overgeneralized shared spool extent created overlap at neighboring installations and had to be moved to site-specific scope.

### Evidence

`photo-first-pilot/CONTINUE_B15_IN_PROGRESS.md`

- line 16: initial measurement procedure is contaminated by neighboring equipment/supports for some units; revised placement method replaces it;
- line 21: R1 uses the same ±3.3 m bus-spool range and creates overlaps with neighboring installations;
- lines 23–27: computed connection plan distinguishes overlapping close pairs from real finite gaps; proposed R2 removes `bus_spool` geometry from the common master and creates finite site-specific segments/wrappers instead.

`photo-first-pilot/CONTINUE_FROM_B15.md`

- lines 10–13: six new GIS units share common body geometry, while neighboring site pipe segments and supports are modeled separately; 501/502/758 preserve existing bodies while local site segments are updated;
- line 15: local validation remains partial; several finite bridge/support regions still fail the internal screen.

`output/installation_B15/B15_connection_revision_plan.json`

- close pairs such as 752–502 and 754–501 have negative projected port gaps and action `omit_added_spools_on_both_sides`;
- other pairs have finite 3.9–5.7 m projected gaps and action `two_finite_spools_meet_at_common_midpoint`.

`output/installation_B15/B15_validation_r3.json`

- lines 28–60: close interfaces are trimmed without remaining overlap;
- lines 62–134: finite spool connection endpoint gaps are approximately 1e-7–1e-6 m.

### Development

The reusable master therefore encodes an engineering assumption: that a geometry element is invariant across installations. B15 shows that this assumption is testable against neighboring geometry. The correction changes the representation hierarchy before it changes any numeric fit.

### Boundary

The evidence does not quantify reuse efficiency or prove that this abstraction strategy is optimal. Several local surface checks remain unresolved; endpoint closure is not whole-device acceptance or electrical-topology certification.

### Subsection answer

Repeated equipment introduces **reusable scope as a reconstruction variable**. The workflow must decide which geometry belongs to a common manufactured structure and which belongs to a finite installation context.

### Bridge to 7.2.2

After the reuse boundary is made explicit, the next class of tasks operates on actual finite endpoints. The reconstruction objective therefore changes from describing individual objects to satisfying relations between existing objects.

---

# 7.2.2 From object geometry to connected representations

## Paragraph 4 — B20 makes ports and routes explicit

### Function

Introduce connected-system reconstruction as a distinct structural problem.

### Claim

B20 replaces implicit adjacency with explicit ports and route intervals. A plausible object model is insufficient when geometry must connect to previously modeled equipment.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B20.md`

- line 9: `port_inventory.json` records actual equipment end faces from B17/B19/other existing geometry;
- line 10: `route_plan.json` contains 21 neighboring intervals: 16 new straight segments, 4 already connected intervals, 1 pending 4100 path; 32 end rings are checked against existing equipment mesh ends;
- lines 11–14: lane names describe physical rows rather than asserting new electrical topology; 4100 requires a transverse turn and cannot be completed by straight Y continuation;
- line 19: all 16 selected bus surface comparisons exceed the 5 cm internal screen, and the record explicitly warns that attachment/support contamination means the residual is not equivalent to endpoint correctness.

### Development

B20 introduces a relationship representation: ports, interval adjacency, and route type. The key engineering decision is whether two existing ends should be joined by a straight segment, retained as already connected, or routed through a turn. This decision cannot be reduced to fitting each device independently.

### Boundary

The route plan represents geometric connectivity, not certified electrical topology. Surface residuals and endpoint continuity measure different properties.

### Bridge

B20 still represents many connections with finite straight segments. B23 shows why the representation class itself can become the next bottleneck.

---

## Paragraph 5 — B23 changes representation class

### Function

Provide the clearest case in which parameter tuning inside the current representation is insufficient.

### Claim

B23 changes a neutral connection from a straight-end hypothesis to a curved path after source profiles reveal a substantial mid-span bow.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B23.md`

- lines 15–19: prior preflight searched near a straight two-end region and missed the middle; XY inspection reveals approximately 0.5 m lateral bow; the revised path bins source geometry, extracts eight control points, fits a cubic B-spline with fixed endpoints and smoothness penalty;
- lines 23–27: additional mechanism/soft-connection revisions follow when the first revised geometry still misattributes source occupancy;
- lines 29–33: final record preserves 32 fixed comparison domains, with 30 meeting the internal 5 cm screen and two retained misses; main curved leads have finite-surface RMS around 0.024–0.025 m; endpoint/cross-section geometry checks are separate.

`output/installation_B23/B23_validation.json`

- lines 5–10: previous objects/scenes/collections/materials and 3,301 station world transforms are preserved;
- lines 20–23: shared masters are explicitly recorded;
- surface checks remain scoped to named finite regions rather than a whole-device metric.

### Development

The important revision precedes numerical fitting: the workflow changes the mathematical object being fitted. A straight segment and a constrained spline are different representations. Once the curved representation is selected, deterministic code estimates the path and validators check finite surfaces and endpoint/contact relations.

### Boundary

Do not present the internal 5 cm screen as survey tolerance. The odd/even source-face comparisons come from one spatially correlated coarse reconstruction. Do not infer a general ability to choose the optimal representation.

### Bridge

A single curved lead demonstrates representation choice locally. B29 shows that relationship constraints can be composed across many previously reconstructed subsystems.

---

## Paragraph 6 — B29 scales endpoint constraints across subsystems

### Function

Show that connected representations are not limited to one curated path; they become a station-level relation problem.

### Claim

B29 reconstructs overhead conductors by terminating new geometry on previously modeled clamps, suspension endpoints, and transformer-derived lead endpoints, while validating endpoint continuity separately from source-surface similarity.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B29.md`

- lines 5–11: 60 strain strings, 60 jumper conductors, and 24 main cross conductors are added; main conductors connect to B29 strain fittings and existing B08/B27-derived transformer lead endpoints; geometry is organized in site collections without replacing prior equipment;
- lines 13–17: 31,379 previous objects and 5,308 station object transforms are preserved; 84 conductor endpoint checks and 24 main-span interfaces are below 2e-5 m; source-surface domains can still show large RMS because they include missing branches/attachments not represented by one conductor;
- lines 23–27: next-terminal inventory is derived from actual previously saved geometry, and future downlead planning uses those endpoints rather than inactive-scene dimensions or guessed locations.

### Development

This separates two engineering validity conditions. Endpoint/topological continuity tests whether the new object connects to the modeled system as intended. Surface comparison tests whether the chosen local geometric representation explains the coarse source region. Passing one does not imply the other.

### Boundary

Do not claim complete electrical topology. The record explicitly retains missing GIS vertical branches and other unresolved geometry.

### Subsection answer

Connected-system reconstruction introduces **relationship constraints**—ports, routes, continuity, and representation class—as first-class variables. Local object fit remains useful, but it no longer defines correctness by itself.

### Bridge to 7.2.3

Once many major components and connections already exist, the remaining question is not only how to reconstruct a known target. The workflow must also decide which unexplained parts of the site deserve the next reconstruction operation and how to insert them without damaging the accumulated state.

---

# 7.2.3 From scheduled additions to gap-driven, state-constrained closure

## Paragraph 7 — B25/B26 adds coverage as a task-selection signal

### Function

Show the shift from following known inventory/tasks toward discovering missing high-impact structures from unexplained registered geometry.

### Claim

B25/B26 uses unexplained source geometry as an additional signal for selecting subsequent reconstruction work.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B25.md`

- lines 5–9: inspection samples 4,434,234 coarse triangle centers; large high regions above GIS/transformer areas remain more than 1 m from current modeled surfaces; this motivates gantry reconstruction rather than declaring completion from inventory status or visual impression;
- lines 15–23: after the gantry reconstruction, selected high-region medians change from 1.75 m to 0.10 m for GIS-A and from 8.12 m to 0.15 m for GIS-B; the record explicitly states these are not independent survey measurements.

`photo-first-pilot/CONTINUE_FROM_B26.md`

- lines 5–15: missing transformer-central firewalls and wall-top gantries are reconstructed using registered source plus photos;
- lines 17–23: selected transformer high-region median changes from 3.15 m to 0.06 m; fraction of selected high-region samples beyond 1 m changes from 78.8% to 14.6%; the region mixes object classes and is explicitly not a device completion rate.

### Development

The new operator does not estimate a device pose. It compares the accumulated model with the registered scene and identifies spatial regions that remain unexplained. This supplies a task-selection cue that complements inventory-driven progression.

### Boundary

The coverage metric is selected-region and same-source. It does not establish whole-site completeness, general planning superiority, or a causal advantage over inventory scheduling.

### Bridge

After major gaps are reduced, the residual work increasingly consists of civil/auxiliary structures and local omissions embedded in a large existing scene.

---

## Paragraph 8 — B31/B32/B35 corroborate closure under incomplete evidence

### Function

Show that late work still uses measurement and reuse, but increasingly depends on interpreting incomplete evidence within the accumulated scene.

### Claim

The late civil/auxiliary batches continue to use explicit geometric measurement while relying more heavily on fixed-view review and source interpretation where registered geometry is incomplete.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B31.md`

- lines 13–19: prior B30 is checkpointed; large civil reference crops and vertical samples are extracted; main building geometry is fit as a shared rotated rectangle, while missing roof regions are completed using photos and relative structure rather than treated as measured surfaces;
- lines 21–27: 33,223 old objects and 7,113 old station transforms are preserved; fixed wall-domain comparisons and six-direction review are performed.

`photo-first-pilot/CONTINUE_FROM_B32.md`

- lines 7–11: two cabin rectangles are independently fit; reusable end/HVAC and door masters are introduced; an inherited door interpretation is revised using photos and source-step evidence; eight same-camera review groups are retained.

`photo-first-pilot/CONTINUE_FROM_B35.md`

- lines 5–17: the record explicitly defines the endpoint as a visible outdoor model and excludes hidden/underground and uncertain details; 35,550 previous objects and 7,112 station transforms are preserved.

### Development

These batches are not evidence that geometry fitting disappears. Measurement remains central. What changes is the context in which it operates: the workflow must interpret incomplete source surfaces, preserve a large inherited scene, and use review to avoid turning missing/occluded evidence into fabricated detail.

### Boundary

Do not use B35 as evidence of complete station reconstruction. The source explicitly excludes hidden, underground, and uncertain content.

### Bridge

B36 gives the clearest final example of a reconstruction whose geometry is constrained simultaneously by source evidence, existing endpoints, inherited equipment, and physical interference.

---

## Paragraph 9 — B36 shows state-constrained insertion and interference

### Function

Complete C2 by showing a late task whose correctness depends on the already populated world.

### Claim

B36 adds missing bus-rack assemblies while preserving inherited transformers and endpoints, and it revises one route to avoid an existing fire riser without changing the measured connection endpoints.

### Evidence

`photo-first-pilot/CONTINUE_FROM_B36.md`

- lines 3–5: two transformer-to-building bus-rack assemblies are added; B08 transformer bodies remain shared and unchanged;
- lines 13–17: 36,615 previous objects, 731 previous scenes, and 7,114 station transforms are preserved; source checks and component contacts are validated;
- lines 19–25: T1/T2 routing differs; first failed non-finite draft is preserved; R2 revises section orientation; R3 moves a local incoming segment by up to 0.16 m to avoid an existing fire pipe while keeping endpoint and support locations fixed.

`output/installation_B36/B36_validation_r3.json`

- lines 4–14: prior-state preservation and final state counts;
- lines 23–26: shared main transformers preserved; new component masters shared; finite geometry and asset roundtrip checks pass;
- lines 676–713: six main busbars terminate on existing B08 stubs and new wall bushings with saved endpoint gaps around 1e-7 m;
- lines 746–754: limitations record existing B08 terminal bars, wall-bushing termination, and local lateral reconciliation around retained fire risers.

### Development

The late reconstruction problem is therefore constrained by an engineered world that already has geometry, endpoints, and occupied space. A valid update must explain new source evidence while remaining compatible with inherited state. This is qualitatively different from fitting an isolated object into an empty local frame.

### Boundary

Endpoint continuity is an internal geometric consistency check, not field electrical or mechanical acceptance. B36 does not establish complete station accuracy or completeness.

### Subsection answer

Near site closure, reconstruction expands from **building a target** to **selecting and inserting residual work into an existing engineered state**. Coverage, review, preservation, and interference constraints become part of the operation alongside local measurement.

---

# §7.2 closing synthesis paragraph

## Function

Compress the three transitions into the central C2 result and bridge to persistent state (C3).

## Claim

The documented sequence retains local geometric fitting but progressively adds decision layers tied to relationships among reconstructed elements.

## Evidence to mention

Only the three transitions, no new cases:

1. B01/B02 → B08/B15: local domain specification → reusable scope;
2. B20 → B23 → B29: object geometry → ports, paths, continuity, representation class;
3. B25/B26 → B31–B36: scheduled target addition → coverage/review/state-constrained closure.

## Interpretation

The result is best described as **operator accumulation under growing reconstruction dependency**, not model learning or monotonic replacement of fitting by “higher reasoning.”

## Boundary

The chronological sequence is historical and task-dependent. It does not support a universal complexity law.

## Bridge to §7.3

The third transition already depends on a large inherited scene. §7.3 should therefore ask what mechanism makes this accumulated state usable across batches, and what risks follow from inheriting prior abstractions.

---

# Figure 4 evidence contract

Figure 4 should contain three rows. Each row must show `evidence → changed decision → changed representation/operator`.

## Row A — local fit → reusable scope

Suggested artifacts:

- B01/B02 same-camera or residual-domain diagnostic;
- B08 shared-master schematic / T1-T2 review;
- B15 finite-spool overlap / connection revision plan.

Message:

`comparison domain` → `what may be shared?` → `MASTER + site-specific finite geometry`.

## Row B — object → connected representation

Suggested artifacts:

- B20 `4100_route_diagnostic.png`;
- B23 `component_and_lead_preflight.png` + `B23_measurement_profiles.png`;
- B29 `B29_jumper_fits.png` or `B29_crossline_fits.png`.

Message:

`local object geometry` → `ports / route / representation class` → `connected paths with explicit endpoint checks`.

## Row C — scheduled addition → gap/state-driven closure

Suggested artifacts:

- B25/B26 coverage or truss/central-section diagnostics;
- B31/B32 fixed review/diagnostic example;
- B36 `B36_busbar_plan_overlay.png` + station/rack overlay.

Message:

`remaining unexplained source` → `what should be modeled next, and where can it fit?` → `coverage/review/interference-aware insertion into inherited state`.

Caption boundary:

> Panels are selected preserved process artifacts illustrating three documented changes in problem formulation. They are not a standardized difficulty scale or evidence of model learning across batches.

---

# Material deliberately excluded from §7.2 main prose

Move to Table 2 / supplement / website rather than interrupting the argument:

- full 149/101 5 cm screen ledger;
- global 1,550-record residual distribution;
- all 36 batch-by-batch descriptions;
- full B08 component count details beyond what is needed to establish shared master/site split;
- every B15 failed surface domain;
- every B20 bus span and residual;
- B23 full 32-domain table;
- all B29 conductor class counts except one compact scale sentence if space allows;
- complete B31–B35 civil object counts;
- B36 full contact-check table;
- all D-series evidence.
