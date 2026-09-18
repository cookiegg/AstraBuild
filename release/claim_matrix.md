# AstraBuild claim-to-evidence matrix

This file is the editorial guardrail for the paper and website. A public revision
should update this matrix before changing any headline number.

| Claim | Current wording | Primary local evidence | Allowed interpretation | Do **not** claim |
|---|---|---|---|---|
| Agent configuration | Codex + GPT-6 Astra + Extra High reasoning | Project-owner statement in this research-writing task; `experiment_manifest.json` | User-confirmed experiment metadata | That old Blender batch logs independently prove the model/reasoning setting |
| Core reconstruction history | 38 core reconstruction batches through D38 | `presentation/report/技术报告.md` | Longitudinal engineering trajectory | 38 IID trials |
| D38.2/D40 scene scale | 37,153 objects / 755 scenes / 858 collections / 3,916 mesh datablocks | `presentation/report/技术报告.md`; `photo-first-pilot/D40/README_D40.md` | Artifact/scene scale | 37,153 verified physical components |
| Approximate instance reuse | ~9.5× object-to-mesh-datablock ratio | same as above | Descriptive Blender structure/reuse indicator | Storage compression ratio or measured modeling-speedup |
| Surface residual ledger | n=1,550; median 0.036 m; p90 0.084 m; p95 0.116 m | `presentation/report/技术报告.md` §6.2 | Agreement with the same photogrammetric coarse reference mesh | Independent survey accuracy; “3.6 cm reconstruction accuracy” |
| 5 cm screen | 149 pass / 101 not-pass | `presentation/report/技术报告.md` §6.2 | Screening ledger with failures retained | 149/250 overall model accuracy or task success rate |
| Coverage transition | selected >1 m samples 78.8%→14.6%; GIS220 8.12→0.15 m; transformer 3.15→0.06 m | `presentation/report/技术报告.md` B25/B26 case | Omission/coverage accounting | Independent absolute geometric error |
| B01 failure | held-out values ~0.048/0.073/0.051 m and preserved failure | `presentation/report/技术报告.md` B01 case plus historical batch records | Verifier-driven protocol revision | Direct B01→B02 accuracy improvement under identical metric |
| B15 revision | contaminated measurement + overextended shared geometry forced r1→r3 changes | `presentation/report/技术报告.md` B15 case | Abstraction/measurement recovery example | That the first shared-master design was valid |
| D38 correction | markup alignment, quarantine of three cabinet groups, rebuild of three GIS gaps, orientation fix | `photo-first-pilot/D38/D38_evidence.md`; `D38/README_D38.md` | Traceable human-agent correction | Fully autonomous discovery of all D38 issues |
| D40 | material-only layer; geometry/transforms unchanged from D38 | `photo-first-pilot/D40/README_D40.md` | Presentation/material layer | A new geometry reconstruction result |
| Device semantic attachment | 151 devices in station part map; 100 12MZ groups attached; 76/106 official names linked, 30 unmatched | `part-annotation/README.md`; `presentation/report/技术报告.md` | Explicit semantic-accounting state with unresolved names preserved | 100% station semantic completeness or identity correctness |
| Transformer semantic pilot | 189 semantic meshes → 26 part classes; 0 unclassified; 36 official inspection points categorized as 31 model-part + 4 external + 1 non-visual | `part-annotation/README.md` | Pilot-level inspection/part categorization | Complete part geometry for all station devices |
| Semantic v3 correction | isolated renders/photos expose and repair naming/box-based mapping errors | `part-annotation/README.md` v3 audit sections | Semantic verifier/revision case study | That early semantic attachment was correct without review |
| D41 | 79 accessory meshes; 17 missing inspection-relevant part classes; T1/T2; `ok=true` | `photo-first-pilot/output/installation_D41/D41_completion.md`; `D41_validation.json` | Inspection-semantic augmentation at research endpoint | Complete station-wide part semantics |
| Autonomy | agent-driven, human-steerable | B08 authorization, B36 review, D38 markup | Human review is a method component | Fully autonomous reconstruction |
| Revision distribution (v0.8) | 15 single-attempt / 18 two-attempt / 9 three-or-more visible revision tags across 42 primary installation folders | `release/behavior_analysis.json` from `scripts/analyze_process_behavior.py` | Lower-bound behavioral statistic over preserved r-tagged artifacts | Exact revision counts; reasoning-effort measurements; that untagged batches were never revised |
| Failure attribution (v0.8) | 5 of 7 documented failure episodes are hypothesis-layer errors (protocol, abstraction, representation, task-selection) | `release/behavior_analysis.json` annotation table; paper v0.8 §5 episodes | Manual annotation of documented episodes, reported with sources | A derived measurement; a full-population failure taxonomy; that parameter errors never occur |
| Adaptation modes (v0.8) | 4 explicit self-diagnosed / 2 human-triggered / 1 human-authorized adaptation episodes | `release/behavior_analysis.json` annotation table | Annotation of the documented episode set | Fully autonomous adaptation; absence of untraced in-flight adaptation |
| State discipline (v0.8) | 2,859+ protected-file hashes; failed variants (C37_failed_camera, D37_modified_1930) preserved | `presentation/report/技术报告.md`; `release/behavior_analysis.json` | Evidence of history-preservation discipline | A correctness proof of the composed model |

## Editorial rule

If a future paper introduces a stronger claim (for example **survey accuracy**,
**cross-site generalization**, **human-time savings**, or **fully autonomous**), it
must add a new independent experiment/source row here rather than upgrading the
meaning of an existing metric.

