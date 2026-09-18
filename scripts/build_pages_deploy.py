#!/usr/bin/env python3
"""Build a self-contained GitHub Pages deploy tree for the AstraBuild site.

The working tree uses symlinks (media/ -> historical experiment outputs, 150 GB)
that GitHub Pages cannot serve. This script copies only the files reachable from
the website into DEPLOY_DIR, dereferencing symlinks, converting referenced
historical PNGs to WebP, and recompressing base64 images embedded in the
historical review HTML pages.

Output layout mirrors the repo root so relative paths (../media, ../release,
../rewrite_b01_b36) keep working when website/ is served under Pages.
"""

import base64
import io
import json
import os
import re
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOY_DIR = sys.argv[1] if len(sys.argv) > 1 else "/tmp/astrabuild-pages"

REWRITE_SUBSET = [
    "paper_layout_v24.pdf",
    "22_FULL_MANUSCRIPT_FIGURE_V24.md",
    "figure_v24/hybrid_svg/fig01_overview_v24.svg",
    "figure_v24/hybrid_svg/fig04_transitions_v24.svg",
    "figure_v24/hybrid_svg/fig05_persistence_v24.svg",
    "figure_v24/hybrid_svg/fig06_findings_v24.svg",
    "figure_v24/hybrid_svg/fig07_session_anatomy_v24.svg",
    "figure_v24/hybrid_svg/fig07_session_anatomy_v24_zh.svg",
    "figures/fig02_longitudinal_map_b01_b36.png",
    "figures/fig03_operator_portfolio_b01_b36.png",
]

HISTORICAL_RE = re.compile(r"[^\"'\s]*media/historical/[^\"'\s)]+")
PNG_DATA_RE = re.compile(r"data:image/png;base64,([A-Za-z0-9+/=\s]+?)(?=[\"'\)\]])")
DATA_URI_RE = re.compile(r"data:image/[A-Za-z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+")

PUBLIC_TOKEN_MAP = {
    "C110": "Cabin-A",
    "C220": "Cabin-B",
    "SA110": "SA-A",
    "SA220": "SA-B",
    "GIS110": "GIS-A",
    "GIS220": "GIS-B",
}
PUBLIC_TEXT_EXTS = {".json", ".md", ".txt", ".csv", ".html"}


def _sanitize_plain_text(text):
    text = re.sub(
        r"(?i)220\s*kV\s+Xialin\s+Substation(?:,\s*Xuancheng)?",
        "an anonymized operating substation",
        text,
    )
    text = re.sub(r"(?i)Xialin\s+Substation", "an anonymized substation", text)
    text = re.sub(r"(?i)Xialin", "site", text)
    text = re.sub(r"(?i)Xuancheng", "anonymized-location", text)
    text = re.sub(r"(?i)(?<!\d)35\s*kV(?!\d)|35\s*千伏", "VC-C", text)
    text = re.sub(r"(?i)(?<!\d)110\s*kV(?!\d)|110\s*千伏", "VC-A", text)
    text = re.sub(r"(?i)(?<!\d)220\s*kV(?!\d)|220\s*千伏", "VC-B", text)
    for old_token, public_token in PUBLIC_TOKEN_MAP.items():
        text = re.sub(rf"(?i){re.escape(old_token)}(?!\d)", public_token, text)
    return text


def sanitize_public_text(text):
    """Remove site-identifying labels while leaving embedded base64 untouched."""
    out = []
    pos = 0
    for match in DATA_URI_RE.finditer(text):
        out.append(_sanitize_plain_text(text[pos:match.start()]))
        out.append(match.group(0))
        pos = match.end()
    out.append(_sanitize_plain_text(text[pos:]))
    return "".join(out)


def sanitize_public_path(rel):
    """Anonymize voltage-coded identifiers in public asset paths."""
    out = rel
    for old_token, public_token in PUBLIC_TOKEN_MAP.items():
        out = re.sub(rf"(?i){re.escape(old_token)}(?!\d)", public_token, out)
    return out


def collect_historical_refs():
    refs = set()
    for name in os.listdir(os.path.join(ROOT, "release")):
        if not name.endswith(".json"):
            continue
        text = open(os.path.join(ROOT, "release", name), encoding="utf-8", errors="replace").read()
        refs.update(HISTORICAL_RE.findall(text))
    for name in ("app.js", "index.html"):
        text = open(os.path.join(ROOT, "website", name), encoding="utf-8").read()
        refs.update(HISTORICAL_RE.findall(text))
    norm = set()
    for ref in refs:
        rel = ref[3:] if ref.startswith("../") else ref
        norm.add(os.path.normpath(rel))
    return sorted(norm)


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def png_to_webp(src, dst, quality=80):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with Image.open(src) as im:
        if im.mode == "P":
            im = im.convert("RGBA")
        im.save(dst, "WEBP", quality=quality, method=4)


def recompress_review_html(src, dst, quality=70):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    text = open(src, encoding="utf-8", errors="replace").read()
    stats = {"n": 0, "before": 0, "after": 0}

    def repl(match):
        try:
            raw = base64.b64decode(match.group(1), validate=False)
            with Image.open(io.BytesIO(raw)) as im:
                im = im.convert("RGB")
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=quality)
            encoded = base64.b64encode(buf.getvalue()).decode("ascii")
            stats["n"] += 1
            stats["before"] += len(match.group(0))
            stats["after"] += len(encoded) + 24
            return "data:image/jpeg;base64," + encoded
        except Exception:
            return match.group(0)

    out = sanitize_public_text(PNG_DATA_RE.sub(repl, text))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return stats


def rewrite_release_json(deploy):
    for name in os.listdir(os.path.join(ROOT, "release")):
        src = os.path.join(ROOT, "release", name)
        dst = os.path.join(deploy, "release", name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        ext = os.path.splitext(name)[1].lower()
        if ext in PUBLIC_TEXT_EXTS:
            text = open(src, encoding="utf-8", errors="replace").read()
            text = sanitize_public_text(text)
            if ext == ".json":
                text = re.sub(
                    r"((?:\.\./)?media/historical/[^\"'\s)]+?)\.png\b",
                    r"\1.webp",
                    text,
                )
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(text)
        else:
            shutil.copyfile(src, dst)


def main():
    deploy = os.path.abspath(DEPLOY_DIR)
    if os.path.exists(deploy):
        shutil.rmtree(deploy)
    os.makedirs(deploy)

    refs = collect_historical_refs()
    print(f"historical refs: {len(refs)}")

    copy(os.path.join(ROOT, "index.html"), os.path.join(deploy, "index.html"))
    open(os.path.join(deploy, ".nojekyll"), "w").close()
    shutil.copytree(os.path.join(ROOT, "website"), os.path.join(deploy, "website"))
    rewrite_release_json(deploy)

    # media/: real files and dereferenced symlinks, excluding historical/
    media_src = os.path.join(ROOT, "media")
    for dirpath, dirnames, filenames in os.walk(media_src, followlinks=False):
        rel_dir = os.path.relpath(dirpath, media_src)
        if rel_dir.split(os.sep)[0] == "historical":
            dirnames[:] = []
            continue
        if "historical" in dirnames:
            dirnames.remove("historical")
        for name in filenames:
            src = os.path.join(dirpath, name)
            dst = os.path.join(deploy, "media", rel_dir, name)
            copy(os.path.realpath(src), dst)

    # referenced historical files only
    counts = {"webp": 0, "copy": 0, "html": 0}
    for rel in refs:
        src = os.path.join(ROOT, rel)
        public_rel = sanitize_public_path(rel)
        if not os.path.exists(src):
            print(f"  MISSING {rel}")
            continue
        ext = os.path.splitext(rel)[1].lower()
        if ext == ".png":
            dst = os.path.join(deploy, public_rel[:-4] + ".webp")
            png_to_webp(os.path.realpath(src), dst)
            counts["webp"] += 1
        elif ext == ".html":
            dst = os.path.join(deploy, public_rel)
            stats = recompress_review_html(os.path.realpath(src), dst)
            counts["html"] += 1
            if stats["n"]:
                print(f"  html {os.path.basename(public_rel)}: {stats['n']} images, "
                      f"{stats['before']/1e6:.1f} -> {stats['after']/1e6:.1f} MB (b64 chars)")
        elif ext in PUBLIC_TEXT_EXTS:
            dst = os.path.join(deploy, public_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            text = open(os.path.realpath(src), encoding="utf-8", errors="replace").read()
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(sanitize_public_text(text))
            counts["copy"] += 1
        else:
            copy(os.path.realpath(src), os.path.join(deploy, public_rel))
            counts["copy"] += 1
    print("historical:", counts)

    for rel in REWRITE_SUBSET:
        copy(os.path.join(ROOT, "rewrite_b01_b36", rel),
             os.path.join(deploy, "rewrite_b01_b36", rel))

    total = 0
    for dirpath, _dirnames, filenames in os.walk(deploy):
        for name in filenames:
            total += os.path.getsize(os.path.join(dirpath, name))
    print(f"deploy tree: {deploy}  total {total/1e6:.1f} MB")


if __name__ == "__main__":
    main()
