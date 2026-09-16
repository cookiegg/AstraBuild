#!/usr/bin/env python3
"""Build a read-only catalog of the historical photo-first-pilot reconstruction dossiers.

The catalog does not reinterpret numerical results. It indexes existing batch artifacts so
that the publication website can expose result triplets and intermediate process evidence
without copying or modifying historical experiment outputs.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BS = ROOT.parent.parent
PILOT = BS / "photo-first-pilot"
OUT = PILOT / "output"
INSTALL = PILOT / "installation"
DEST = ROOT / "release" / "process_catalog.json"

STAGES = [
    "prepare", "extract", "inspect", "measure", "plan", "fit", "build", "refine",
    "connect", "features", "render", "review", "audit", "validate", "release",
    "deliver", "discover", "collision",
]

FAMILY_RANGES = [
    (range(1, 6), "Surge-arrester fitting"),
    (range(6, 7), "Wall and gate"),
    (range(7, 9), "Main transformers"),
    (range(9, 11), "Capacitor banks"),
    (range(11, 17), "110 kV GIS and device families"),
    (range(17, 20), "220 kV GIS and outgoing families"),
    (range(20, 31), "Bus, conductors, insulators, and connections"),
    (range(31, 35), "Buildings and ground"),
    (range(35, 37), "Auxiliary facilities and omission recovery"),
]

FEATURED = ["B01", "B08", "B15", "B20", "B23", "B25", "B29", "B31", "B32", "B36", "D37", "D38", "D41"]


def family(batch: str) -> str:
    if batch.startswith("B") and batch[1:].isdigit():
        n = int(batch[1:])
        for r, name in FAMILY_RANGES:
            if n in r:
                return name
    return {
        "D37": "Auxiliary facilities — formal continuation",
        "D38": "Human-guided correction",
        "D40": "Presentation invariance",
        "D41": "Inspection-semantic augmentation",
    }.get(batch, "Later station refinement")


def rev_score(path: Path) -> tuple[int, int, str]:
    s = path.as_posix().lower()
    score = 0
    if "/r3/" in s:
        score += 30
    elif "/r2/" in s:
        score += 20
    if "final" in s:
        score += 5
    if "failed" in s or "draft" in s:
        score -= 100
    return (score, path.stat().st_mtime_ns if path.exists() else 0, path.name)


def webpath(path: Path) -> str:
    rel = path.relative_to(PILOT).as_posix()
    return f"../media/historical/{rel}"


def describe_role(name: str) -> str | None:
    n = name.lower()
    if "preflight" in n:
        return "preflight"
    if any(x in n for x in ["profile", "measurement", "datum", "axis", "cross_section", "section", "slice"]):
        return "measurement / profile"
    if any(x in n for x in ["route_diagnostic", "jumper_fit", "downlead_fit", "lead_tracking", "strain_profile"]):
        return "route / conductor fitting"
    if "diagnostic" in n:
        return "diagnostic"
    if "coverage" in n:
        return "coverage audit"
    if any(x in n for x in ["layout", "plan_overlay", "fits"]):
        return "planning / fit diagnostic"
    return None


def image_candidates(d: Path) -> list[Path]:
    return [p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}]


def triplets(images: list[Path]) -> list[dict]:
    groups: dict[tuple[str, str], dict[str, Path]] = {}
    # Render indices differ between clean/overlay/reference (e.g. 479/480/481),
    # so the leading scene number is not part of the semantic view key.
    rx = re.compile(r"^(?:\d+_)?(.+?)_(Clean|Overlay|Reference)(?:_r\d+)?$", re.I)
    for p in images:
        m = rx.match(p.stem)
        if not m:
            continue
        key = (p.parent.as_posix(), m.group(1))
        groups.setdefault(key, {})[m.group(2).lower()] = p
    rows = []
    for (_, stem), g in groups.items():
        if "clean" in g and "overlay" in g:
            paths = list(g.values())
            quality = max(rev_score(p)[0] for p in paths)
            row = {
                "label": stem,
                "clean": webpath(g["clean"]),
                "overlay": webpath(g["overlay"]),
                "reference": webpath(g["reference"]) if "reference" in g else None,
                "is_station": "station" in stem.lower(),
                "quality": quality,
            }
            rows.append(row)
    rows.sort(key=lambda x: (x["quality"], x["is_station"], x["label"]), reverse=True)
    # Deduplicate near-identical labels across root/r2/r3 by keeping the best-scored one.
    out, seen = [], set()
    for row in rows:
        normalized = re.sub(r"^\d+_", "", row["label"], flags=re.I)
        normalized = re.sub(r"_r\d+$", "", normalized, flags=re.I)
        if normalized in seen:
            continue
        seen.add(normalized)
        row.pop("quality", None)
        out.append(row)
    return out[:8]


def process_media(images: list[Path]) -> list[dict]:
    found = []
    for p in images:
        role = describe_role(p.name)
        if not role:
            continue
        score = rev_score(p)[0]
        found.append((score, role, p))
    found.sort(key=lambda x: (x[0], x[1], x[2].name), reverse=True)
    result, seen = [], set()
    for _, role, p in found:
        key = p.name.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append({"role": role, "name": p.name, "path": webpath(p)})
    return result[:12]


def loose_views(images: list[Path]) -> list[dict]:
    """Best clean/overlay/reference renders even when scene-number naming prevents a triplet."""
    rows = []
    for p in images:
        n = p.stem.lower()
        role = None
        for candidate in ("clean", "overlay", "reference"):
            if candidate in n:
                role = candidate
                break
        if not role:
            continue
        bonus = 5 if "station" in n else 0
        rows.append((rev_score(p)[0] + bonus, p.stat().st_mtime_ns, role, p))
    rows.sort(reverse=True)
    out, seen = [], set()
    for _, _, role, p in rows:
        if p.name.lower() in seen:
            continue
        seen.add(p.name.lower())
        out.append({"role": role, "name": p.name, "path": webpath(p)})
    # Later D40/D41 layers use semantic names such as render_D41_T1_front.png
    # instead of the historical Clean/Overlay/Reference suffix convention.
    if not out:
        fallback = sorted(images, key=lambda p: (rev_score(p)[0], p.stat().st_mtime_ns), reverse=True)
        for p in fallback[:8]:
            out.append({"role": "review", "name": p.name, "path": webpath(p)})
    return out[:12]


def script_stages(batch: str) -> tuple[list[str], dict[str, list[str]]]:
    by_stage: dict[str, list[str]] = {s: [] for s in STAGES}
    if batch.startswith("B"):
        for p in INSTALL.glob(f"*_{batch}*.py"):
            stage = p.stem.split("_", 1)[0]
            if stage in by_stage:
                by_stage[stage].append(p.name)
    elif batch.startswith("D"):
        d = PILOT / batch
        if d.is_dir():
            for p in d.glob("*.py"):
                stage = p.stem.split("_", 1)[0]
                if stage in by_stage:
                    by_stage[stage].append(p.name)
    by_stage = {k: sorted(v) for k, v in by_stage.items() if v}
    ordered = [s for s in STAGES if s in by_stage]
    return ordered, by_stage


def choose_json(d: Path, batch: str, token: str) -> str | None:
    candidates = [p for p in d.rglob("*.json") if token.lower() in p.name.lower()]
    if not candidates:
        return None
    candidates.sort(key=rev_score, reverse=True)
    return webpath(candidates[0])


def review_metadata(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    title = re.sub(r"\s+", " ", m.group(1)).strip() if m else path.stem
    return {
        "review_title": title,
        "review_embedded_images": text.count("data:image/"),
        "review_has_slider": bool(re.search(r'type=["\']range["\']', text, re.I)),
        "review_select_count": len(re.findall(r"<select\b", text, re.I)),
        "review_button_count": len(re.findall(r"<button\b", text, re.I)),
    }


def choose_review_html(d: Path, batch: str) -> str | None:
    candidates = [p for p in d.rglob("*.html") if "review" in p.name.lower()]
    if not candidates:
        return None
    # Prefer the canonical <batch>_review.html, then latest revision score.
    candidates.sort(key=lambda p: ((p.name.lower() == f"{batch.lower()}_review.html"), *rev_score(p)), reverse=True)
    return webpath(candidates[0])


def choose_measurement_json(d: Path) -> str | None:
    candidates = [p for p in d.rglob("*.json") if any(t in p.name.lower() for t in ("measurement", "measurements", "datum", "datums"))]
    if not candidates:
        return None
    candidates.sort(key=rev_score, reverse=True)
    return webpath(candidates[0])


def build_batch(batch: str) -> dict | None:
    d = OUT / f"installation_{batch}"
    if not d.is_dir():
        return None
    images = image_candidates(d)
    stages, stage_files = script_stages(batch)
    t = triplets(images)
    process = process_media(images)
    cont = PILOT / f"CONTINUE_FROM_{batch}.md"
    if batch.startswith("D"):
        candidate = PILOT / batch / f"README_{batch}.md"
        if candidate.exists():
            cont = candidate
    review = choose_review_html(d, batch)
    result = {
        "batch": batch,
        "family": family(batch),
        "featured": batch in FEATURED,
        "output_file_count": sum(1 for p in d.rglob("*") if p.is_file()),
        "image_count": len(images),
        "stages": stages,
        "stage_files": stage_files,
        "view_triplets": t,
        "loose_views": loose_views(images),
        "process_media": process,
        "continuation": webpath(cont) if cont.exists() else None,
        "plan": choose_json(d, batch, "plan"),
        "validation": choose_json(d, batch, "validation"),
        "manifest": choose_json(d, batch, "manifest"),
        "coverage": choose_json(d, batch, "coverage"),
        "review_page": review,
        "review_checks": choose_json(d, batch, "review_checks"),
        "inputs": choose_json(d, batch, "inputs"),
        "measurements": choose_measurement_json(d),
        **review_metadata(Path(PILOT / review.replace('../media/historical/', '')) if review else None),
    }
    return result


def main() -> None:
    # Publication dossiers follow canonical batch directories only. This discovers
    # Bxx/Dxx additions automatically while excluding archived variants such as
    # C37_failed_camera, D37_modified_1930, and the pre-core R01 prototype.
    batches = sorted(
        [p.name.replace("installation_", "") for p in OUT.glob("installation_*")
         if p.is_dir() and re.fullmatch(r"(?:B\d{2}|D\d{2})", p.name.replace("installation_", ""))],
        key=lambda b: (b[0], int(b[1:])),
    )
    dossiers = [x for b in batches if (x := build_batch(b))]
    prevalence = Counter()
    for d in dossiers:
        for s in d["stages"]:
            prevalence[s] += 1
    payload = {
        "release": "AstraBuild worked-example process catalog v0.7",
        "source": "photo-first-pilot historical outputs (read-only)",
        "interpretation": "A canonical core reconstruction loop with task-specific operators; absence of a stage or graphic is not a failed task.",
        "featured_batches": FEATURED,
        "stage_prevalence": dict(prevalence),
        "dossier_count": len(dossiers),
        "dossiers": dossiers,
    }
    DEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEST} with {len(dossiers)} dossiers")
    print("featured", ",".join(b for b in FEATURED if any(d['batch']==b for d in dossiers)))


if __name__ == "__main__":
    main()
