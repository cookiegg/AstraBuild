# Findings section draft v1 (for integration into the B01–B36 manuscript as new §6; Discussion/Conclusion shift to §7/§8)

<!--
Writing contracts (internal notes, removed before integration):

§6 opening — function: tell the reader the section's claim in two sentences; claim: the record supports exactly two findings; evidence: synthesis of §5; inference limit: findings are about this workflow in this record; bridge: scope note.
§6 scope — function: pre-empt overgeneralization; claim: single site, single configuration, no control; evidence: §4 study design; bridge: into Finding 1.
§6.1 — function: re-read the record as bottleneck migration; claim: fitting is solved early and stays solved; documented failures sit at the problem-definition layer; evidence: per-band revision-tag rates, Table 1; inference limit: revision tags are a filename-based lower bound, not telemetry; bridge: why the migration is structural.
§6.2 — function: reframe persistent state; claim: one mechanism both composes local solutions and propagates abstraction errors; evidence: Table 2, B15 case, adaptation-mode counts; inference limit: no stateless control run; bridge: to Discussion.
Table 1 — failure attribution, 5 episodes inside B01–B36 (D38/D41 excluded by author decision), sources = batch dossiers.
Table 2 — persistent-state ledger, 4 consumption events, numbers from §5.3 and B31/B36 validators.
Figure 6 — decision-layer ladder (left) + per-band multi-revision rate bars (right); rates: 67/100/45/83% for the four descriptive bands.
-->

# 6 Findings

Two findings structure this record. The first reads the 36-batch sequence as a migration of the bottleneck: geometric fitting is solved early and stays solved, while every documented failure sits one level up, in how the reconstruction problem itself was defined. The second reframes persistent state: it is neither memory nor storage but a shared engineering surface, and the same mechanism that composes local solutions across batches also propagates erroneous abstractions.

**Scope.** Both findings are drawn from one substation, one owner-confirmed GPT-6 Astra/Codex configuration, and the preserved B01–B36 artifacts. They characterize this workflow in this record; they do not claim that the same behavior would appear with another model, another site, or a stateless variant of the same harness.

## 6.1 Finding 1: Fitting stays solved; the bottleneck migrates to problem definition

Across all 36 batches, no documented failure is a failure of numerical fitting. The five preserved failure episodes (Table 1) all sit at the definition level: four in a named definition layer — evaluation protocol, reusable-abstraction boundary, representation class, task selection — and the fifth, an omission surfaced by human review, traces to an earlier scoping decision that had placed the missing structure outside the reconstruction target. What changes along the sequence is not whether the workflow can fit geometry, but what kind of decision turns out to be wrong.

[Figure 6 here: decision-layer ladder (geometric fitting: strong throughout; problem definition: revised in place; cross-batch abstraction: propagation risk) with per-band multi-revision rates]

The revision record quantifies the migration. Counting visible revision tags in the preserved batch folders, the fraction of batches with two or more attempts is 4 of 6 in the local-fitting band (B01–B06), 13 of 13 in the repeated-equipment band (B07–B19), 5 of 11 in the connected-systems band (B20–B30), and 5 of 6 in the site-closure band (B31–B36). These tags are a filename-based lower bound rather than action telemetry — B01, for example, carries no tag because its failure was preserved and the protocol change landed in B02 — so we read them as a distribution, not as per-batch counts. The distribution is not monotone: revision is densest exactly where new abstractions are introduced — the band in which reusable masters and site-specific boundaries are first defined.

**Table 1.** Documented failure episodes in B01–B36, attributed by layer. Sources: preserved batch dossiers and validation chains.

| Episode | Failure layer | Observable evidence | Response |
|---|---|---|---|
| B01 | Evaluation protocol | Held-out cylindrical-domain RMS 4.84/7.32/5.10 cm violates the 5 cm screen; comparison domain mixed the target shaft with accessory geometry | B02 separates fitting and holdout regions; the revised metric is declared not directly comparable to B01 |
| B15 | Reusable-abstraction boundary | Local measurement contaminated by neighboring equipment; shared bus-spool master overlapped installations with different physical extents | Measurement method revised; finite site-specific geometry moved out of the shared master; obsolete supports archived, not overwritten |
| B23 | Representation class | Straight-lead hypothesis contradicted by a ≈0.5 m mid-span bow in the registered source | Reformulated as a constrained curved path; fixed-endpoint B-spline fitted by deterministic code; r1–r3 revision chain preserved |
| B25/B26 | Task selection | Structures absent from the model while their inventory entry appeared resolved | Coverage audit over selected high regions becomes a task-selection signal; >1 m unexplained-sample fraction 78.8% → 14.6% (B26) |
| B36 | Omission surfaced by review | Low bus racks missing; omission traced to an earlier decision that treated the structure as outside the transformer assembly | Audit-only history search, then a multi-revision rebuild including a 0.16 m displacement to avoid a fire riser |

This pattern is structural rather than incidental. Because numerical estimation and acceptance live in deterministic geometry code (§3.2), the model's observable decisions are confined to selecting evidence, choosing representations, defining comparison domains and reuse boundaries, and sequencing work — and those are exactly the layers at which the preserved failures occur. The bottleneck migrates to problem definition because problem definition is the only layer the model actually decides.

## 6.2 Finding 2: Persistent state is a shared engineering surface

### 6.2.1 Composition: later batches consume an engineered world

Later batches do not start from a blank scene; they consume geometry, transforms, terminals, and reusable components produced and accepted earlier, while validators check that the inherited state is unchanged. Table 2 lists the documented consumption events.

**Table 2.** Persistent-state ledger: what later batches consume, how it is checked, and what a wrong upstream state would propagate.

| Consumer | Inherited asset consumed | Validation check | Propagation surface if the asset were wrong |
|---|---|---|---|
| B23 | B08 transformer terminal interface | Endpoint/termination checks on the saved path | Every later neutral-lead connection would land on a wrong terminal |
| B29 | Previously modeled clamps and suspension/lead endpoints | Endpoint relations checked independently of coarse-surface agreement | Displaced clamps would detach strings and jumpers across intervals |
| B31 | More than 7,000 existing station transforms | State-preservation tests over inherited transforms | Transform drift would silently move already-accepted equipment |
| B36 | 36,615 previous objects, 7,114 prior station transforms, 2,798 protected files | Preservation checks plus explicit collision/interference checks | Inherited stubs or bushings that no longer match the site would misroute every new busbar closing onto them |

### 6.2.2 Propagation: the same channel in reverse

The composition channel is also the propagation channel. B15's shared finite bus spool carried an inappropriate extent into every installation built from the master, and the error remained nonlocal until the reusable/site-specific boundary itself was revised. No stateless control run exists, so the record supports a narrower claim than "memory improves reconstruction": persistent external state is what makes a 36-batch engineering sequence possible in this workflow at all, and upstream abstraction choices become part of every downstream problem.

### 6.2.3 Who notices: self-diagnosed versus human-triggered adaptation

The six documented adaptation episodes in B01–B36 split by who first notices the mismatch. In four — B01→B02, B15, B23, B25/B26 — the mismatch surfaces in validator or measurement evidence and the revision is self-diagnosed: B23's measurement profiles invalidated the straight-lead hypothesis, and the r1→r2→r3 chain shows the correction proceeding without external direction. In two, a person is in the loop: B08's shared transformer master was created only after explicit user authorization of cross-installation equivalence, and B36's omission was spotted by a human reviewer scanning a top view, after which the workflow traced the cause to a documented earlier decision before rebuilding. The record is therefore agent-driven and human-steerable: validators and sparse human review catch different failure classes, and neither alone covers the record.
