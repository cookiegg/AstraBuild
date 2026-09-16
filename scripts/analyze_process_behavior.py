#!/usr/bin/env python3
"""Mine behavioral process statistics from the preserved AstraBuild batch history.

The historical experiment outputs are read-only. This script never modifies them.
It scans the preserved batch folders (reached through media/historical, a read-only
symlink into the historical experiment directory) and derives descriptive,
behavior-level statistics used by the v0.8 analysis draft:

- per-batch revision traces (filename- and directory-level `_rN` / `rN/` tags)
- preserved failure variants (folders/files marked failed/initial)
- validation / manifest artifact counts per batch
- operator (stage) prevalence, passed through from release/process_catalog.json
- manual episode annotations (failure modes, adaptation modes) whose labels are
  fixed in this file and traceable to the v0.7/v0.8 manuscript case studies

Every statistic is reported with its scope. Filename-level revision counts are a
LOWER BOUND on revision behavior: revisions that were never frozen to disk, and
revisions named at release level rather than file level (e.g. D38.1 -> D38.2),
are not visible to this scan.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RELEASE = ROOT / "release"
HISTORICAL_OUTPUT = (ROOT / "media" / "historical" / "output").resolve()

REVISION_TAG = re.compile(r"_r(\d+)(?=\.|_|$)")
REVISION_DIR = re.compile(r"^r(\d+)$")

# Episode annotations are manual labels assigned from the documented case studies
# (paper/paper_teacher_discussion.md section 6; carried into the v0.8 findings).
# They are annotations of the historical record, not measurements produced here.
FAILURE_MODE_ANNOTATIONS = [
    {
        "episode": "B01",
        "failure_mode": "evaluation-domain hypothesis error",
        "layer": "protocol",
        "observable_evidence": "held-out cylindrical-domain RMS ~0.048/0.073/0.051 m violates the 5 cm screen; batch retained as failed; comparison domain mixed target shaft with accessory geometry",
        "response": "B02 separates fitting and holdout regions; revised metric explicitly declared not directly comparable to B01",
        "source": "paper section 6.1; installation_B01 dossier",
    },
    {
        "episode": "B15",
        "failure_mode": "measurement contamination + reusable-abstraction boundary error",
        "layer": "abstraction",
        "observable_evidence": "local measurement procedure contaminated by neighboring equipment; shared bus-spool master overlapped installations with different physical extents",
        "response": "measurement method revised; finite site-specific bus geometry removed from the shared master; obsolete supports archived, not overwritten",
        "source": "paper section 6.3; installation_B15 dossier",
    },
    {
        "episode": "B23",
        "failure_mode": "representation-class error",
        "layer": "representation",
        "observable_evidence": "inherited preflight treated a connection as a straight segment; registered coarse geometry shows a mid-span bow of roughly half a meter",
        "response": "geometry binned, control points extracted, smooth curved path fitted with fixed endpoints; r1 worsened one validation domain, r2 added the soft lead, r3 added lower bridge contact",
        "source": "paper section 6.4; installation_B23 validation_initial/validation/validation_r2 chain",
    },
    {
        "episode": "B25/B26",
        "failure_mode": "unknown-omission risk under inventory-driven task selection",
        "layer": "task-selection",
        "observable_evidence": "structures can be absent from the model while their inventory entry appears resolved",
        "response": "coverage audit over selected high regions becomes a task-selection signal; >1 m unexplained-sample fraction 78.8% -> 14.6%",
        "source": "paper sections 5.4 and 6.5; installation_B25/B26 dossiers",
    },
    {
        "episode": "B36",
        "failure_mode": "omission surfaced by sparse human review",
        "layer": "human-triggered",
        "observable_evidence": "top-view reviewer reports missing low bus racks; omission traced to an earlier decision treating the structure as outside the transformer assembly",
        "response": "audit-only history search, then multi-revision rebuild (non-finite path section fixed, section orientation fixed, one segment moved 0.16 m to avoid a fire pipe)",
        "source": "paper section 6.6; installation_B36 dossier",
    },
    {
        "episode": "D38",
        "failure_mode": "false-object generation + missing structure, surfaced by 2D markup",
        "layer": "human-triggered",
        "observable_evidence": "marked review images registered to original views at NCC ~0.94/0.92; three false cabinet groups identified",
        "response": "false objects quarantined (not deleted); three GIS gaps and fire-room/sand-box structures rebuilt",
        "source": "paper section 6.7; installation_D38 dossier",
    },
    {
        "episode": "D38.1",
        "failure_mode": "coordinate-semantics error introduced during correction",
        "layer": "representation",
        "observable_evidence": "a registration yaw was mistaken for equipment orientation; overlay review exposed the error",
        "response": "D38.2 corrects the orientation semantics; the intermediate error is preserved in history",
        "source": "paper section 6.7; version boundary appendix",
    },
]

ADAPTATION_ANNOTATIONS = [
    {
        "episode": "B01->B02",
        "mode": "explicit self-diagnosed",
        "note": "failure diagnosed to the protocol level; the evaluation domain itself was revised while the failed batch was preserved",
    },
    {
        "episode": "B08",
        "mode": "human-authorized",
        "note": "reusable T1/T2 master created only after explicit user equivalence authorization",
    },
    {
        "episode": "B15",
        "mode": "explicit self-diagnosed",
        "note": "measurement method and MASTER/site boundary revised together after overlap evidence",
    },
    {
        "episode": "B23",
        "mode": "explicit self-diagnosed",
        "note": "measurement profiles invalidated the straight-lead hypothesis; representation class changed across preserved r1/r2/r3",
    },
    {
        "episode": "B25/B26",
        "mode": "explicit self-diagnosed",
        "note": "task selection shifted from inventory completion to unexplained-geometry coverage",
    },
    {
        "episode": "B36",
        "mode": "human-triggered",
        "note": "sparse omission report triggered history search plus a multi-revision rebuild",
    },
    {
        "episode": "D38",
        "mode": "human-triggered",
        "note": "2D markup registered (NCC 0.94/0.92) and converted to traceable 3D corrections; a correction error (D38.1) was itself caught and fixed (D38.2)",
    },
]


def scan_batches():
    batches = {}
    failed_variants = []
    for path in sorted(HISTORICAL_OUTPUT.iterdir()):
        if not path.is_dir() or not path.name.startswith("installation_"):
            continue
        name = path.name[len("installation_"):]
        is_variant = ("failed" in name) or ("modified" in name)
        max_rev = 1
        revision_files = []
        validation_jsons = []
        manifests = []
        review_pages = []
        for f in path.rglob("*"):
            if f.is_dir():
                m = REVISION_DIR.match(f.name)
                if m:
                    max_rev = max(max_rev, int(m.group(1)))
                continue
            m = REVISION_TAG.search(f.name)
            if m:
                rev = int(m.group(1))
                max_rev = max(max_rev, rev)
                if len(revision_files) < 5:
                    revision_files.append(f.name)
            if "validation" in f.name and f.suffix == ".json":
                validation_jsons.append(f.name)
            if "manifest" in f.name and f.suffix == ".json":
                manifests.append(f.name)
            if f.name.endswith("review.html") or f.name.endswith("_review.html"):
                review_pages.append(f.name)
        entry = {
            "attempt_tags_visible": max_rev,
            "revision_evidence_files": sorted(set(revision_files)),
            "validation_json_count": len(validation_jsons),
            "manifest_count": len(manifests),
            "review_page_count": len(review_pages),
        }
        if is_variant:
            failed_variants.append(name)
        else:
            batches[name] = entry
    return batches, failed_variants


def main() -> int:
    batches, failed_variants = scan_batches()

    dist = {"1": 0, "2": 0, "3+": 0}
    for b, e in batches.items():
        n = e["attempt_tags_visible"]
        dist["1" if n == 1 else "2" if n == 2 else "3+"] += 1

    catalog = json.loads((RELEASE / "process_catalog.json").read_text())

    out = {
        "release": "AstraBuild behavior analysis v0.8",
        "generated_by": "scripts/analyze_process_behavior.py",
        "source": {
            "historical_output_dir": str(HISTORICAL_OUTPUT),
            "access": "read-only scan through media/historical symlink",
            "operator_prevalence": "release/process_catalog.json stage_prevalence (40-dossier scope)",
        },
        "scope_notes": [
            "attempt_tags_visible counts distinct _rN file tags / rN directory levels per batch folder; it is a lower bound on revision behavior because not every revision was frozen under an r-tagged name (e.g. D38.1 -> D38.2 is a release-level revision invisible to this scan).",
            "B01 shows no revision tag because the failed batch was preserved and the protocol change landed in B02; single-attempt tags do not imply single-attempt reasoning.",
            "operator prevalence uses the 40-dossier process catalog and differs in scope from the 36-batch filename audit reported in the v0.7 manuscript (build/validate 36/36 etc.).",
            "failure-mode and adaptation labels are manual annotations of the documented case studies, embedded in this script with sources; the script aggregates them but does not derive them.",
            "the folder scan finds 33 review html pages vs 32 formal review pages in process_catalog.json; the extra page belongs to C37, whose failed-camera variant was superseded by D37 and which is therefore not in the formal catalog.",
            "artifact counts cover installation_* folders only; project-wide totals reported in the technical report (e.g. 150 manifests) additionally count release-level records outside these folders.",
        ],
        "batch_population": {
            "primary_installation_folders": len(batches),
            "preserved_failed_or_modified_variants": failed_variants,
        },
        "revision_distribution": {
            "batches_by_visible_attempt_tags": dist,
            "multi_revision_batches": sorted(
                b for b, e in batches.items() if e["attempt_tags_visible"] >= 2
            ),
            "three_or_more": sorted(
                b for b, e in batches.items() if e["attempt_tags_visible"] >= 3
            ),
            "per_batch": batches,
        },
        "artifact_counts": {
            "validation_json_files": sum(e["validation_json_count"] for e in batches.values()),
            "manifest_files": sum(e["manifest_count"] for e in batches.values()),
            "review_html_pages": sum(e["review_page_count"] for e in batches.values()),
        },
        "operator_prevalence_40_dossiers": catalog["stage_prevalence"],
        "failure_mode_annotations": FAILURE_MODE_ANNOTATIONS,
        "failure_mode_layer_counts": _count_by(FAILURE_MODE_ANNOTATIONS, "layer"),
        "adaptation_annotations": ADAPTATION_ANNOTATIONS,
        "adaptation_mode_counts": _count_by(ADAPTATION_ANNOTATIONS, "mode"),
    }

    out_path = RELEASE / "behavior_analysis.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out_path.relative_to(ROOT)}")
    print(f"  primary installation folders: {len(batches)}")
    print(f"  revision distribution (visible attempt tags): {dist}")
    print(f"  three-or-more: {sorted(b for b, e in batches.items() if e['attempt_tags_visible'] >= 3)}")
    print(f"  preserved failed/modified variants: {failed_variants}")
    print(f"  validation jsons: {out['artifact_counts']['validation_json_files']}, "
          f"manifests: {out['artifact_counts']['manifest_files']}, "
          f"review pages: {out['artifact_counts']['review_html_pages']}")
    return 0


def _count_by(rows, key):
    counts = {}
    for row in rows:
        counts[row[key]] = counts.get(row[key], 0) + 1
    return counts


if __name__ == "__main__":
    raise SystemExit(main())
