# AstraBuild rewrite: B01–B36 only

## Status

Discussion draft. This directory is a clean-sheet rewrite and does **not** revise the existing v0.9 manuscript in place.

## Evidence boundary

Main empirical record: **B01–B36 only**.

Excluded from the scientific narrative:

- D37 and later correction / continuation work;
- D38 human-markup correction;
- D40 presentation-only material changes;
- D41 semantic augmentation;
- claims whose main support comes only from those later stages.

Reason: the rewrite should characterize the natural GPT-6 Astra reconstruction trajectory represented by B01–B36. Later D-series work is historically useful but is not a clean continuation of the same experimental condition and should not determine the paper's scientific thesis.

Primary evidence sources for the rewrite:

- historical `installation_B01` … `installation_B36` folders;
- `release/process_catalog.json`;
- `release/behavior_analysis.json`, restricted to B01–B36 and treated as descriptive metadata;
- batch validation / manifest files;
- the existing technical report and claim registry only where their claims can be traced back to B01–B36.

## Central diagnosis of the current paper

The current paper tries to make several stories equally important: task breadth, failure analysis, hypothesis revision, human correction, station composition, and semantic augmentation. This causes three problems:

1. **No single scientific object.** The reader cannot tell whether the paper studies GPT-6 Astra, a reconstruction workflow, a benchmark, a digital-twin artifact, or failure recovery.
2. **Evidence is organized by artifacts rather than claims.** Batch outputs, videos, reviews, counts, and cases are repeatedly shown without a strong hierarchy.
3. **Later historical accidents become scientific sections.** D37+ material is over-weighted even though it should not define what B01–B36 demonstrates.

## Recommended scientific question

> **Can a general-purpose reasoning model scale from local geometry fitting to a persistent industrial 3D reconstruction by coordinating heterogeneous evidence, executable geometry tools, reusable abstractions, and task-specific validation over a long horizon? What additional operators become necessary as the reconstruction problem changes from isolated components to reusable equipment families, connected systems, and site-level closure?**

This question is preferred because the B01–B36 record naturally forms a progression of reconstruction regimes rather than a set of independent benchmark trials.

## Recommended paper thesis

The scientific contribution should not be “GPT-6 Astra built a large substation model.” A stronger thesis is:

> **The B01–B36 history shows how a general-purpose reasoning model can operate a persistent 3D reverse-engineering process whose computational structure changes with task complexity: early tasks are dominated by local extraction and fitting; repeated equipment introduces reusable abstractions and revision; connected systems require routing, topology, coverage, and specialized diagnostics; later site closure requires explicit review and interference checks. Precise metric estimation is delegated to deterministic operators, while the model primarily selects evidence, representations, decomposition, and programmatic actions.**

The final B36 station state is evidence that this process composes over a long horizon, not the paper's scientific question by itself.

## Natural longitudinal regimes in B01–B36

### Regime I — Local geometric fitting (B01–B06)

Targets: arresters, wall, gate.

Dominant operations in the preserved process catalog: extraction + fitting + build + validation. There is little explicit planning, measurement abstraction, or refinement machinery.

Scientific role: establish the simplest form of the problem — converting registered local evidence into explicit editable geometry.

Representative evidence: B01/B02 evaluation-domain issue; B06 civil wall/gate fit.

### Regime II — Reusable equipment assemblies (B07–B19)

Targets: transformers, capacitor banks, 110 kV / 220 kV GIS families.

The workflow becomes more structured: measurement, planning, refinement, audit, reusable `MASTER`/site separation, and fixed review views appear repeatedly.

Scientific role: test whether reconstruction can move beyond one-off fits to repeated component families and reusable engineering structure.

Representative evidence: B08 transformer reuse; B15 reusable-boundary revision; B17/B19 complex GIS families.

### Regime III — Connected systems and unexplained geometry (B20–B30)

Targets: busbars, conductors, insulator strings, flexible paths, coverage completion.

The problem changes qualitatively. Correct local objects are insufficient: endpoints, routes, topology, flexible geometry, and missing structures must be reasoned about relative to existing state.

Scientific role: show the transition from object reconstruction to system reconstruction.

Representative evidence: B20 connection logic; B23 curved neutral lead; B25/B26 coverage-driven completion; B29 conductor fitting.

### Regime IV — Site closure and civil / auxiliary integration (B31–B36)

Targets: buildings, ground, secondary cabins, auxiliary infrastructure, transformer-side bus racks.

The dominant challenge is no longer introducing a new device family; it is closing remaining structured gaps while preserving the accumulated station state. Measurement, fixed-view review, history preservation, and in B36 collision/interference checks become important.

Scientific role: stress-test whether the accumulated model remains editable and consistent late in the sequence.

The B36 r3 validator records 36,812 objects, 743 scenes, 7,116 station objects, preservation of 36,615 previous objects and 2,798 protected files. These are scale/state-preservation descriptors, not independent reconstruction-accuracy statistics.

## Three possible framings

### A. Scaling from local fits to persistent engineering reconstruction — **recommended**

Main question: how does the required agent/tool structure change as reconstruction complexity increases?

Why it fits the data: B01–B36 naturally form four regimes with increasing structural requirements.

### B. Division of labor between general reasoning and deterministic geometry — secondary mechanism

Main question: what should the LLM decide, and what should numerical tools decide?

Why it is useful: many strong metric results come from deterministic fitting/validation, while the model selects evidence, representation, decomposition, and code.

Why it should not be the only thesis: the existing record has no controlled ablation removing the deterministic tools or replacing the model.

### C. Behavioral failure / hypothesis revision — not recommended as the main framing

Why: selected failure episodes are informative, but they are sparse, manually chosen, and do not represent the full B01–B36 population. Making them the central story causes the paper to overfit to a few cases and obscures the much stronger longitudinal reconstruction trajectory.

## Claims the new paper should avoid

- model superiority over other LLMs or specialized reconstruction systems;
- autonomous reconstruction;
- survey-grade accuracy;
- IID success rate over 36 batches;
- population-level failure-frequency claims from selected cases;
- cross-site generalization;
- treating final object count as a primary scientific metric.

## Writing rule for the rewrite

Every main-paper figure, table, and subsection must answer one of three questions:

1. What reconstruction regime is being tested?
2. What new engineering capability / operator is required at this regime?
3. What evidence shows that the persistent process can or cannot support it?

Anything that does not answer one of these belongs in the appendix or website evidence browser.
