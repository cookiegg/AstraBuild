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
    must("Reconstruction Task Suite" in paper and "System-Level Demonstration" in paper, "paper must contain task-suite and system-level framing")
    must("fig09_task_suite_composition" in paper and "fig06_d38_human_feedback" in paper, "paper must reference task-suite and behavioral figures")
    must("fig01_agentic_loop" in html, "site must include the primary study-overview Figure 1")
    must("fig11_canonical_workflow" in html, "site must include the canonical workflow/process figure")
    must("fig12_b32_worked_example" in html, "site must include the B32 worked-example figure")
    must('id="reviews"' in html and "evaluation console" in html.lower(), "site must expose the original reconstruction-review gallery as the evaluation console")
    must("review-gallery-frame" in html and "review-batch-select" in html, "site must include interactive original-review browser controls")
    must("fig13_review_protocol" in paper and "Historical review protocol across device cases" in paper, "paper must include the cross-task historical review protocol")
    must("fig13_review_protocol" in tex, "LaTeX must include the review-protocol figure")
    must("Worked example: B32 secondary equipment cabins" in html, "site must explain one concrete task inside the protocol section")
    must("B32_review.html" in html, "site must expose the original B32 interactive review")
    must("Worked example: B32" in paper and "fig12_b32_worked_example" in paper, "paper must include the B32 observable agent-tool trace")
    must("fig12_b32_worked_example" in tex, "LaTeX must include the B32 worked-example figure")
    must('id="dossiers"' in html and "batch dossiers" in html, "site must expose the historical process dossier browser")
    must("B23: process evidence changes the representation" in paper, "paper must include B23 process-evidence case study")
    must(html.count('class="task-card"') == 12, "site must expose twelve visual task cards")
    must("Task evidence matrix" in html, "site must include the task-native evidence matrix")
    must("D38 correction chain" in html, "site must include the D38 human-steerable correction case")
    must("What this evaluation does and does not show" in html, "site must include the supported/not-supported discussion section")
    must(html.count('class="paper-prose') >= 8 and 'abstract-text' in html and 'discussion-sections' in html, "site must embed substantial manuscript prose across major paper sections")
    must("formalism-block" in html, "site must include formal method definitions")
    must('id="references"' in html and "Selected references" in html, "site must include an explicit References section")
    must("fig03_quantitative_evidence" in tex and "fig07_d41_inspection_semantics" in tex, "LaTeX must include publication figures")
    for marker in ["1 · Model under test / harness", "2 · One task, observed", "3 · Task suite (not IID)", "4 · Behavioral findings", "5 · Evaluation console", "6 · Failure attribution", "7 · System composition", "8 · What is / is not shown", "9 · Limitations"]:
        must(marker in html, f"site missing paper-structure marker: {marker}")
    paper_order = ["summary", "model-harness", "worked-example", "tasks", "behavioral-findings", "reviews", "gallery", "dossiers", "cases", "d38", "integration", "semantics", "discussion", "scope", "references", "sources", "citation"]
    positions = [html.index(f'id=\"{anchor}\"') for anchor in paper_order]
    must(positions == sorted(positions), "site sections must follow the paper narrative order")

    # v0.8 analysis-report layer: behavioral findings must be backed by the mined record.
    must('id="behavioral-findings"' in html, "site must include the behavioral findings section")
    must("fig14_behavioral_analysis" in html, "site must include the behavioral-analysis figure")
    for finding_id in ["f1", "f2", "f3", "f4", "f5", "f6"]:
        must(f'id="{finding_id}"' in html, f"site missing finding anchor: {finding_id}")

    v8 = (PAPER / "paper_v08_analysis.md").read_text(encoding="utf-8")
    must("not independent survey accuracy" in v8, "v0.8 draft must retain the accuracy disclaimer")
    must("owner-confirmed" in v8, "v0.8 draft must retain the model-provenance qualifier")
    must("fig14_behavioral_analysis" in v8, "v0.8 draft must reference the behavioral-analysis figure")
    must("Finding 1" in v8 and "Finding 6" in v8, "v0.8 draft must contain the six findings")
    must("the harness is the method" in v8, "v0.8 draft must state the model/harness decoupling")

    behavior = load_json(RELEASE / "behavior_analysis.json")
    must(behavior["generated_by"] == "scripts/analyze_process_behavior.py", "behavior analysis must come from the mining script")
    dist = behavior["revision_distribution"]["batches_by_visible_attempt_tags"]
    must(dist["1"] + dist["2"] + dist["3+"] == behavior["batch_population"]["primary_installation_folders"], "revision distribution must sum to the scanned folder population")
    must(sum(behavior["failure_mode_layer_counts"].values()) == len(behavior["failure_mode_annotations"]), "failure-mode counts must match the annotation table")
    must(sum(behavior["adaptation_mode_counts"].values()) == len(behavior["adaptation_annotations"]), "adaptation-mode counts must match the annotation table")
    for value, label in [("15", "single-attempt"), ("18", "two-attempt"), ("9", "three-or-more-attempt")]:
        must(value in html, f"site must carry the mined {label} count")

    parser = SiteParser()
    parser.feed(html)
    anchors = ["summary", "model-harness", "worked-example", "reviews", "tasks", "dossiers", "behavioral-findings", "cases", "d38", "integration", "semantics", "discussion", "gallery", "scope", "references", "sources", "citation"]
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
