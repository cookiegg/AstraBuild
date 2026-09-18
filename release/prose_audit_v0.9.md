# AstraBuild v0.9 Prose Audit

Date: 2026-09-17

The `academic-writing-skills` exact-candidate audit was applied separately to scholarly prose and to full delivery text.

## Scholarly prose candidates

- Website scholarly prose: **PASS, 0 findings**. Candidate SHA-256: `ae20bcb2c4d661ccff46d6e2579f874d0b102f89e19ed231587bbc11a1b8cb00`.
- Paper scholarly prose: **PASS, 0 findings**. Candidate SHA-256 after the final prose cleanup is recorded by the final validation run.

The scholarly-prose candidates include paragraph text, section claims, case descriptions, figure captions, and Discussion/Limitations prose while excluding data-table cells, filenames, code identifiers, and document-control metadata from stylistic judgment.

## Full-delivery diagnostics retained contextually

The full Markdown/website scans may still report lexical-hyphen density in tables, headings, filenames, or established technical terms such as `task-selection`, `site-specific`, `human-steerable`, `GPT-Policy`, and component-level labels. These findings are retained where the hyphen prevents ambiguity or is part of an established name/technical compound. They are not treated as evidence of AI authorship and were not mechanically synonym-rotated.

Syntactic em-dash punctuation in English scholarly prose was removed during the final cleanup. Chinese punctuation is not governed by the English prose profile.

## Claim-scope checks

The final text preserves the following boundaries:

- the study is a single-site longitudinal case study, not an IID benchmark;
- surface residuals measure internal agreement with the same photogrammetric reference used during reconstruction, not independent survey accuracy;
- the seven adaptation/failure episodes are selected documented cases and their layer counts are descriptive, not failure-frequency estimates;
- human steering materially affects B08, B36, D38, and semantic audit decisions;
- the legacy model configuration is owner-confirmed rather than independently frozen in batch logs;
- the historical record contains no matched second-model, specialist-3D, or professional-CAD rerun;
- D38.2 is the geometry baseline, D40 is presentation-only with geometry preserved, and D41 is an additive semantic endpoint.

## Narrative check

The final main narrative is:

**scientific question → evaluation setting → task probes → representative B32 task → behavioral cases → cross-case findings → long-horizon composition stress test → discussion/limitations**.

The 32 original review pages and 40 process dossiers are retained as interactive evidence appendices rather than interleaved with the main argument.
