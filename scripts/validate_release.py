#!/usr/bin/env python3
"""Offline checks for the AstraBuild paper/site release.

This validator performs no Blender execution and no model/API calls. It verifies the
isolated publication layer, claim guardrails, academic figures, root landing page,
and relative/symlinked media used for local preview.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
RELEASE = ROOT / "release"
PAPER = ROOT / "paper"
FIGURES = ROOT / "figures"
SCRIPTS = ROOT / "scripts"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.styles: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])
        if tag in {"img", "source", "video"} and data.get("src"):
            self.links.append(data["src"])
        if tag == "script" and data.get("src"):
            self.scripts.append(data["src"])
        if tag == "link" and data.get("href") and data.get("rel") == "stylesheet":
            self.styles.append(data["href"])


def must(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_site_path(relative: str) -> Path:
    return (SITE / relative).resolve()


def main() -> int:
    required = [
        ROOT / "index.html",
        ROOT / "README.md",
        PAPER / "paper.md",
        PAPER / "paper_teacher_discussion.md",
        PAPER / "paper_v08_analysis.md",
        PAPER / "teacher_discussion_notes_zh.md",
        PAPER / "paper.tex",
        PAPER / "technical_report_zh.md",
        PAPER / "references.bib",
        RELEASE / "experiment_manifest.json",
        RELEASE / "metrics.json",
        RELEASE / "study_protocol.json",
        RELEASE / "media.json",
        RELEASE / "process_catalog.json",
        RELEASE / "behavior_analysis.json",
        RELEASE / "claim_matrix.md",
        SITE / "index.html",
        SITE / "styles.css",
        SITE / "app.js",
        SITE / "favicon.svg",
        SCRIPTS / "generate_figures.py",
        SCRIPTS / "build_process_catalog.py",
    ]
    for path in required:
        must(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

    manifest = load_json(RELEASE / "experiment_manifest.json")
    metrics = load_json(RELEASE / "metrics.json")
    protocol = load_json(RELEASE / "study_protocol.json")
    media = load_json(RELEASE / "media.json")
    process_catalog = load_json(RELEASE / "process_catalog.json")

    must(manifest["research_endpoint"]["version"] == "D41", "research endpoint must be D41")
    must(manifest["research_endpoint"]["geometry_baseline"] == "D38.2", "geometry baseline must remain D38.2")
    must(manifest["agent_configuration"]["provenance"] == "user_confirmed", "agent config provenance must stay explicit")
    must(metrics["release"].endswith("v0.7"), "metrics release should be v0.7")
    must(metrics["geometry"]["surface_residual_m"]["independent_survey_accuracy"] is False, "surface residual must not be marked survey accuracy")
    must(metrics["geometry"]["five_cm_screen"]["pass"] + metrics["geometry"]["five_cm_screen"]["not_pass"] == 250, "5 cm screen denominator mismatch")
    must(metrics["semantic"]["official_names_linked"] + metrics["semantic"]["official_names_unmatched"] == metrics["semantic"]["official_names_total"], "semantic name accounting mismatch")
    must(metrics["semantic"]["transformer_pilot"]["model_part_points"] + metrics["semantic"]["transformer_pilot"]["external_component_points"] + metrics["semantic"]["transformer_pilot"]["nonvisual_points"] == metrics["semantic"]["transformer_pilot"]["official_inspection_points"], "inspection-point accounting mismatch")
    must(metrics["d41"]["validation_ok"] is True, "D41 validation flag expected true from recorded file")
    must(len(protocol["research_questions"]) == 5, "expected five research questions")

    expected_figures = [
        "fig01_agentic_loop",
        "fig02_longitudinal_study",
        "fig03_quantitative_evidence",
        "fig04_structure_and_semantics",
        "fig05_failure_recovery",
        "fig06_d38_human_feedback",
        "fig07_d41_inspection_semantics",
        "fig08_validation_stack",
        "fig09_task_suite_composition",
        "fig10_visual_abstract",
        "fig11_canonical_workflow",
        "fig12_b32_worked_example",
        "fig13_review_protocol",
        "fig14_behavioral_analysis",
    ]
    for stem in expected_figures:
        for ext in ("svg", "pdf", "png"):
            p = FIGURES / f"{stem}.{ext}"
            must(p.is_file() and p.stat().st_size > 1024, f"missing/empty publication figure: {p.name}")

    html = (SITE / "index.html").read_text(encoding="utf-8")
    root_html = (ROOT / "index.html").read_text(encoding="utf-8")
    paper = (PAPER / "paper_teacher_discussion.md").read_text(encoding="utf-8")
    tex = (PAPER / "paper.tex").read_text(encoding="utf-8")
    zh = (PAPER / "technical_report_zh.md").read_text(encoding="utf-8")

    must("website/" in root_html, "root landing page must route to website/")
    must("independent survey accuracy" in html, "site must retain the correlated-reference accuracy boundary")
    must("not independent survey accuracy" in paper, "paper must retain accuracy disclaimer")
    must("不是独立测绘精度" in zh, "Chinese report must retain accuracy disclaimer")
    must("owner-confirmed" in paper, "paper must retain model-provenance qualifier")

    # v1.0 site contract: the website now tracks the B01-B36 manuscript
    # (rewrite_b01_b36/, paper_layout_v24.pdf), not the v0.9 main draft.
    must("From Local Fits to Persistent Industrial 3D Reconstruction" in html, "site hero must carry the B01-B36 manuscript title")
    must("paper_layout_v24.pdf" in html, "site must link the typeset B01-B36 paper")
    must("B01–B36" in html, "site must use the B01-B36 record framing")
    for fig_ref in ["fig01_overview_v24", "fig02_longitudinal_map_b01_b36", "fig03_operator_portfolio_b01_b36", "fig04_transitions_v24", "fig05_persistence_v24"]:
        must(fig_ref in html, f"site must include manuscript figure: {fig_ref}")
    must(html.count('class="task-card"') == 4, "site must expose four descriptive band cards")
    must('id="method-trace"' in html and "B23" in html, "site must include the B23 worked trace")
    must('id="console"' in html, "site must include the unified evaluation console")
    for elm in ["view-batch-select", "view-mode-clean", "view-mode-overlay", "view-mode-reference", "view-image", "view-prev", "view-next", "view-original"]:
        must(f'id="{elm}"' in html, f"unified review viewer missing control: {elm}")
    must("Coarse reference" in html, "review viewer must label the coarse-reference mode in English")
    must("Original batch record" in html, "review viewer must link the original Chinese batch records as provenance")
    must("coarse_vs_d40.mp4" in html and "assembly_metal.mp4" in html, "site must include both no-caption videos")
    must('id="evidence-appendix"' in html and "dossier-select" in html, "site must keep the process-dossier evidence appendix")
    must("formalism-block" in html, "site must include formal method definitions")
    must('id="references"' in html and "Selected references" in html, "site must include an explicit References section")
    for marker in ["1 · Overview", "2 · Method", "3 · Study design", "4 · Results", "5 · Evaluation console", "6 · Videos", "7 · Discussion"]:
        must(marker in html, f"site missing paper-structure marker: {marker}")
    paper_order = ["overview", "method", "method-trace", "study-design", "results", "results-transitions", "results-persistence", "console", "evidence-appendix", "videos", "discussion", "references", "sources", "citation"]
    positions = [html.index(f'id=\"{anchor}\"') for anchor in paper_order]
    must(positions == sorted(positions), "site sections must follow the B01-B36 manuscript narrative order")

    audit = (PAPER / "reviewer_audit_v0.9.md").read_text(encoding="utf-8")
    must("Proposed central question" in audit and "Task breadth should define the probes" in audit, "v0.9 reviewer audit must document the narrative rationale")

    behavior = load_json(RELEASE / "behavior_analysis.json")
    must(behavior["generated_by"] == "scripts/analyze_process_behavior.py", "behavior analysis must come from the mining script")
    dist = behavior["revision_distribution"]["batches_by_visible_attempt_tags"]
    must(dist["1"] + dist["2"] + dist["3+"] == behavior["batch_population"]["primary_installation_folders"], "revision distribution must sum to the scanned folder population")
    must(sum(behavior["failure_mode_layer_counts"].values()) == len(behavior["failure_mode_annotations"]), "failure-mode counts must match the annotation table")
    must(sum(behavior["adaptation_mode_counts"].values()) == len(behavior["adaptation_annotations"]), "adaptation-mode counts must match the annotation table")

    parser = SiteParser()
    parser.feed(html)
    anchors = paper_order + ["top", "videos"]
    for anchor in anchors:
        must(anchor in parser.ids, f"missing site anchor: {anchor}")

    checked_assets = 0
    for relative in parser.scripts + parser.styles + parser.links:
        if relative.startswith(("http://", "https://", "data:")):
            continue
        path = resolve_site_path(relative)
        must(path.exists(), f"broken site asset/media path: {relative} -> {path}")
        checked_assets += 1

    for item in media["media"]:
        path = resolve_site_path(item["path_from_website"])
        must(path.exists(), f"media registry path does not exist: {item['id']} -> {path}")

    must(process_catalog["dossier_count"] >= 40, "process catalog should cover B01-B36 plus D37/D38/D40/D41")
    review_dossiers = [d for d in process_catalog["dossiers"] if d.get("review_page")]
    must(len(review_dossiers) == 32, "expected 32 formal historical review pages from B07-D38")
    must(all(resolve_site_path(d["review_page"]).exists() for d in review_dossiers), "every indexed historical review page must resolve")
    b23 = next((d for d in process_catalog["dossiers"] if d["batch"] == "B23"), None)
    b32 = next((d for d in process_catalog["dossiers"] if d["batch"] == "B32"), None)
    must(any(d["batch"] == "D37" for d in process_catalog["dossiers"]), "formal D37 dossier missing from process catalog")
    must(b23 is not None, "B23 dossier missing")
    must(b32 is not None, "B32 dossier missing")
    must((b32.get("review_page") or "").endswith("B32_review.html"), "B32 dossier must expose original B32_review.html")
    must(b32.get("review_checks") and b32.get("measurements") and b32.get("inputs"), "B32 dossier must expose review checks, inputs and measurements")
    b23_roles = {m["role"] for m in b23["process_media"]}
    must("preflight" in b23_roles and "measurement / profile" in b23_roles, "B23 process dossier must expose profile + preflight evidence")
    for dossier in process_catalog["dossiers"]:
        for triplet in dossier.get("view_triplets", []):
            for key in ("clean", "overlay", "reference"):
                relative = triplet.get(key)
                if relative:
                    must(resolve_site_path(relative).exists(), f"broken dossier triplet path: {dossier['batch']} {relative}")
        for key in ("review_page", "review_checks", "inputs", "measurements", "continuation", "plan", "validation", "manifest", "coverage"):
            relative = dossier.get(key)
            if relative:
                must(resolve_site_path(relative).exists(), f"broken dossier record path: {dossier['batch']} {key} {relative}")
        for item in dossier.get("process_media", []) + dossier.get("loose_views", []):
            must(resolve_site_path(item["path"]).exists(), f"broken dossier media path: {dossier['batch']} {item['path']}")

    # Publication-level local preview media should live under the release root as
    # real files or symlinks so a server started at astra-build/ can serve them.
    for name in ["coarse_vs_d40.mp4", "assembly_metal.mp4", "hero_loop.mp4", "d40_overview.png", "d41_t1_front.png", "field_gis.jpg"]:
        must((ROOT / "media" / name).exists(), f"local preview media unresolved: media/{name}")
    must((ROOT / "media" / "historical").exists(), "historical process-evidence symlink must resolve")

    # Paths are stored from repository root.
    repo_root = ROOT.parents[3]
    for source in manifest["primary_sources"]:
        must((repo_root / source).exists(), f"primary source missing: {source}")

    print("AstraBuild release validation: PASS")
    print(f"  required files: {len(required)}")
    print(f"  publication figures: {len(expected_figures)} × 3 formats")
    print(f"  research questions: {len(protocol['research_questions'])}")
    print(f"  site anchors: {len(anchors)}")
    print(f"  HTML local assets/media checked: {checked_assets}")
    print(f"  media registry entries checked: {len(media['media'])}")
    print(f"  process dossiers checked: {process_catalog['dossier_count']}")
    print("  claim guards: D41 endpoint, D38.2 geometry baseline, non-survey residual disclaimer, human-steerable scope, owner-confirmed model provenance")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"AstraBuild release validation: FAIL: {exc}", file=sys.stderr)
        raise
