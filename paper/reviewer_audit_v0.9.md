# AstraBuild v0.9 — Reviewer/Reader Audit

**Branch:** `review/robodojo-narrative-v0.9`
**Purpose:** restructure the paper and website around a scientific question rather than an inventory of artifacts.

## 1. Central reviewer concern

The current draft contains strong evidence but distributes it across three competing stories: task breadth, station-scale composition, and hypothesis revision. The scientifically distinctive story is the third. Task breadth should define the probes; station composition should serve as a long-horizon stress test; neither should compete with the central behavioral question.

### Proposed central question

**When a general-purpose reasoning model is constrained by registered geometric evidence, programmatic tools, and deterministic validation in a persistent 3D engineering environment, how does it form, test, and revise engineering hypotheses, and where do those decisions fail?**

Operational subquestions:
1. Which heterogeneous reconstruction tasks can the same model/harness execute under one interface?
2. When evidence contradicts the current model, does revision occur at the parameter, protocol, abstraction, representation, or task-selection level?
3. Which decisions remain error-prone and require deterministic review or human feedback?
4. Can accepted outputs persist and compose over a long task horizon without losing provenance or state consistency?

## 2. Abstract audit

### Current weaknesses
- opens with a broad agent statement but then becomes a chronological inventory;
- reports many counts before stating the scientific finding;
- seven cases are enumerated rather than synthesized;
- strengths and limitations of Astra are not stated as a paired result;
- station scale and D41 are overrepresented relative to the behavioral question.

### Target abstract contract
1. problem/gap: editable engineering reconstruction requires decisions beyond surface recovery;
2. scientific question: hypothesis formation/revision under evidence and validation;
3. design: one focal model, one site, 38 longitudinal batches, 12 task families, preserved process record; not IID;
4. principal finding: hard cases often require revising the hypothesis class rather than tuning geometry;
5. strengths: operator selection, structured measurement, abstraction/reuse, evidence-driven revision, persistent state;
6. weaknesses: first-pass fine detail/representation errors, coordinate/semantic misinterpretation, dependence on deterministic validation and material human steering;
7. boundary: single site, no independent survey reference, no matched model comparison.

## 3. Section-by-section audit

### Introduction
**Issue:** breadth/depth/scale are useful but currently read as three equal contributions.
**Change:** lead with the hypothesis-revision question. Introduce breadth as the experimental probe set and composition as the final stress test.

### Related Work
**Issue:** generally sound; keep concise.
**Change:** distinguish scene generation/reconstruction from engineering decision making, then use GPT-Policy/Astra embodied-policy primarily as evaluation-structure precedents, not as claims of statistical comparability.

### Method / Evaluation Setting
**Issue:** too many abstractions appear before readers know what is being evaluated; the E1/E2/E3 taxonomy is post-hoc and risks looking self-defined to fit the result.
**Change:** describe the focal model, evidence interface, action interface, validators, and persistent state directly. Move interpretive taxonomy out of the main setup or remove it.

### Task Suite
**Issue:** task cards, evidence matrix, capability ladder, and quantitative ledger partially duplicate one another.
**Change:** task cards/table define probes; task-native metrics define readouts. Move capability conclusions to Findings.

### Task-Level Evidence
**Issue:** object counts and global residuals can be mistaken for the paper's main result.
**Change:** report them as calibration/context. Make explicit that 3.6 cm is correlated-reference agreement and 37,153 objects is composition scale, not reconstruction accuracy.

### Case Studies
**Strength:** strongest section of the paper.
**Change:** cases precede findings. Prioritize episodes that expose different decision layers: B01 (protocol), B15 (abstraction), B23 (representation), B25/B26 (task selection), B32 (fine-detail interpretation), B36/D38 (human-triggered correction). B08 is useful for explicit human authorization of reuse but need not carry equal space.

### Cross-Case Findings
**Issue:** current F1–F6 appear before the detailed case evidence on the website. Some labels generalize from seven selected documented episodes.
**Change:** move after cases; qualify prevalence statements as applying to the documented/selected adaptation episodes. Organize findings as strengths and recurring failure modes rather than six slogan-like cards.

Proposed findings:
- F1: deterministic measurement operators make metric envelope fitting reliable once the comparison domain is well specified;
- F2: the difficult failures occur at hypothesis level (protocol, abstraction, representation, task selection), not only parameter level;
- F3: first-pass fine detail and semantic/coordinate interpretation remain unreliable; externalized review evidence is necessary;
- F4: human input is sparse but material, so the demonstrated workflow is human-steerable rather than autonomous;
- F5: persistent state enables long-horizon composition but also makes reuse boundaries and error propagation first-class engineering risks.

### System Composition / D41
**Issue:** currently too prominent and repeats assembly visualization.
**Change:** one compact long-horizon stress-test section. Keep one station-level comparison video; remove repeated assembly video. D41 becomes an endpoint example, not a second paper topic.

### Discussion / Limitations
**Issue:** 'Not supported' and a separate Limitations section repeat one another.
**Change:** one interpretation section followed by compact threats-to-validity paragraphs.

### Review Console / Dossiers
**Strength:** excellent evidence resource.
**Issue:** too central in the main reading path.
**Change:** retain all 32 original reviews and 40 dossiers, but move them to an Interactive Evidence appendix after the main scientific narrative.

## 4. Target narrative

**Abstract → 1 Question & setting → 2 Task suite / evaluation protocol → 3 Task-level results → 4 Behavioral case studies → 5 Cross-case findings (strengths + failure modes) → 6 Long-horizon composition stress test → 7 Discussion & limitations → Interactive evidence appendix → References/resources.**

The paper manuscript retains a conventional Related Work section after the Introduction.

## 5. Evidence boundaries that must remain locked
- single-site longitudinal case study;
- batches are dependent, not IID;
- reference residuals are against the same photogrammetric mesh used during reconstruction;
- human steering materially affects B08/B36/D38 and semantic audit;
- historical model/reasoning metadata are owner-confirmed rather than independently frozen;
- no matched baseline reruns and no cross-site generalization claim;
- D38.2 = main geometry baseline; D40 = presentation-only geometry-preserving layer; D41 = additive semantic endpoint.
