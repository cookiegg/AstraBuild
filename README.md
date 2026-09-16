# AstraBuild worked-example research release · v0.7

This directory is an **isolated paper + academic-figure + evidence-first research website release** for the Xialin substation Blender reconstruction experiments. It does not modify or replace any historical `photo-first-pilot` batch, `.blend` output, validation record, or existing presentation asset.

## Working title

> **AstraBuild: GPT-6 Astra as a Long-Horizon 3D Engineering Agent for Component-Level Substation Reconstruction**

The release frames the longitudinal engineering record as one persistent 3D engineering agent operating across heterogeneous tasks:

`field/coarse/record evidence → Codex + GPT-6 Astra → Blender/Python actions → deterministic validation → persistent engineering memory → revision / reuse / next task`.

The declared configuration **Codex + GPT-6 Astra + Extra High reasoning** is project-owner-confirmed. Historical Blender batches inspected for this release do not freeze model/reasoning-effort metadata, so the publication explicitly labels this provenance rather than retroactively claiming log-level proof.

## Version boundary

- **D38.2** — core geometry reconstruction baseline used by headline scene-scale / residual accounting.
- **D40** — material-only presentation layer with geometry/transform/vertex-count invariance validation.
- **D41** — research endpoint; adds inspection-relevant transformer accessories and part/world-location records.

These layers must not be collapsed into one undifferentiated version in the paper or website.

## What changed in v0.7

v0.7 addresses a remaining explanation problem in the method section: the canonical loop was still too abstract to answer what Astra actually consumes, why a step is needed, who generates a diagnostic figure, what each stage outputs, and how review evidence changes the next revision.

Major changes:

- new **Figure 12** uses B32 as a complete worked example with explicit trigger, input package, observable Astra/Codex role, deterministic NumPy/SciPy/Matplotlib/Blender execution, R1→R2→R3 revisions, validation and persistent outputs;
- the website now explains B32 before showing the generalized Figure 11 workflow;
- the original historical `B32_review.html` is lazily embedded in the method section, preserving its eight camera directions, Clean/Overlay/Reference modes and split slider;
- the website now has a primary **Original Reconstruction Reviews** browser that indexes all 32 historical `review.html` pages from B07–D38 and loads the original interactive page for each transformer, capacitor-bank, GIS, conductor, civil or correction batch;
- new **Figure 13** extracts representative same-camera `Clean / Overlay / Reference` triplets from B07/B08/B09/B17 for the static paper while the website preserves the full original interactive reviews;
- the process catalog now indexes each batch's original `*_review.html`, review checks, input record and measurement JSON when present, so dossier users can inspect the historical review UI rather than only selected thumbnails;
- the paper explicitly states that old batches preserve an observable engineering decision trail, **not GPT-6 Astra's private chain-of-thought**;
- v0.6's canonical-core/task-specific-operator model, 40 formal dossiers, evidence-first task gallery, D38 flagship, station integration and D41 semantics remain in place.

## Contents

- `paper/paper_teacher_discussion.md` — current polished English manuscript for advisor discussion.
- `paper/teacher_discussion_notes_zh.md` — concise Chinese framing/questions for the meeting.
- `paper/paper.md` — previous detailed v0.2 manuscript retained for reference.
- `paper/paper.tex` — LaTeX manuscript source.
- `paper/technical_report_zh.md` — detailed Chinese technical report.
- `paper/references.bib` — reconstruction / agent / benchmark references.
- `figures/` — **13 academic figures**, each generated in SVG/PDF/PNG.
- `scripts/generate_figures.py` — deterministic publication-figure generator.
- `scripts/build_process_catalog.py` — read-only scanner that indexes historical batch evidence for the website dossier browser.
- `release/experiment_manifest.json` — release boundary and provenance contract.
- `release/metrics.json` — measurements with explicit scope/source and semantic/D38/D40/D41 data.
- `release/study_protocol.json` — research questions, evidence roles, metric definitions, and key cases.
- `release/media.json` — publication-media registry.
- `release/process_catalog.json` — generated index of 40 formal publication dossiers (B01–B36 + D37/D38/D40/D41) and their review/process evidence; superseded C37/variant directories remain historical but are not counted as formal dossiers.
- `release/claim_matrix.md` — claim → evidence → allowed-interpretation guardrail.
- `website/` — bilingual static research-report website.
- `media/` — selected historical videos/renders exposed without modifying the originals, plus the derived short hero loop.
- `media/cases/` — historical case-study thumbnails/episode evidence for the website.
- `media/historical/` — local symlink to the read-only `photo-first-pilot` tree so the dossier browser can show original process evidence without copying or modifying it.
- `scripts/validate_release.py` — offline structural / claim-scope / asset-path validation.

## Preview

From this directory:

```bash
python3 -m http.server 8765
```

Open either URL:

```text
http://127.0.0.1:8765/
http://127.0.0.1:8765/website/
```

The root page redirects to the research website. Historical images/videos are exposed through publication-layer paths so local HTTP preview does not require changing the experiment outputs.

## Regenerate academic figures

```bash
python3 scripts/generate_figures.py
```

Generated files include:

```text
figures/fig01_agentic_loop.{svg,pdf,png}
figures/fig02_longitudinal_study.{svg,pdf,png}
figures/fig03_quantitative_evidence.{svg,pdf,png}
figures/fig04_structure_and_semantics.{svg,pdf,png}
figures/fig05_failure_recovery.{svg,pdf,png}
figures/fig06_d38_human_feedback.{svg,pdf,png}
figures/fig07_d41_inspection_semantics.{svg,pdf,png}
figures/fig08_validation_stack.{svg,pdf,png}
figures/fig09_task_suite_composition.{svg,pdf,png}
figures/fig10_visual_abstract.{svg,pdf,png}
figures/fig11_canonical_workflow.{svg,pdf,png}
figures/fig12_b32_worked_example.{svg,pdf,png}
figures/fig13_review_protocol.{svg,pdf,png}
```

## Regenerate process catalog

```bash
python3 scripts/build_process_catalog.py
```

The catalog is a publication index only. It does not modify any historical experiment output.

## Validate release

```bash
python3 scripts/validate_release.py
```

## Claim discipline

The central centimeter-scale geometric values are **residuals against the same photogrammetric coarse mesh used by the reconstruction workflow**. They are **not independent survey accuracy**.

The `149 / 101` 5 cm ledger is a validation screen, not model “accuracy.” The `78.8% → 14.6%` value is a selected high-region coverage-gap audit, not whole-station completeness. The `≈9.5×` figure is a descriptive object/mesh-datablock reuse ratio, not a measured modeling-speedup. Human review is explicitly part of the method, so the report uses *agent-driven / human-steerable* rather than *fully autonomous*.
