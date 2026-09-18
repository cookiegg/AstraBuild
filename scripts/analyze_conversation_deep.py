#!/usr/bin/env python3
"""Deep process analysis of the AstraBuild B01-B36 conversation log.

Goes beyond session statistics to four analytical questions:
1. Cross-batch consumption: which earlier-batch artifacts does later work
   actually read/reference in tool calls (process-side evidence for the
   persistent-state ledger)?
2. Trial-and-error density: per-batch exec failure rates (exit_code != 0).
3. Compaction boundaries: does the model re-establish context after each
   context compaction by re-reading summary artifacts (manifests, plans,
   review pages) from earlier batches?
4. Autonomy structure: unattended spans between substantive human messages
   and what was accomplished inside them.

Output: release/conversation_deep_analysis.json
Caveat: batch attribution follows the most recently mentioned installation
folder; exec failures include exploratory commands and are a density signal,
not a quality score.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "conversation_logs" / "astra_b01_b36_session.jsonl"
OUT = ROOT / "release" / "conversation_deep_analysis.json"

BATCH_RE = re.compile(r"installation_([BCDR]\d{2})")
EXIT_RE = re.compile(r'exit_code\\\\?":\s*(\d+)')
READ_HINT_RE = re.compile(r"\b(cat|head|tail|sed|rg|grep|less|more|awk|jq|python3? -c|Read)\b")
SUMMARY_ARTIFACT_RE = re.compile(r"(manifest|review\.html|_plan\.json|validation|_summary|continuation)")


def bkey(b):
    return (b[0], int(b[1:3]))


def main():
    current_batch = None
    per_batch = defaultdict(lambda: {"exec": 0, "exec_failed": 0, "consume": Counter(), "produce": 0})
    call_by_id = {}
    compactions = []
    post_compaction_reads = []
    pending_call = None
    events = []  # (ts, kind, detail) for autonomy analysis
    assistant_msgs = []

    with open(SRC, errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("type")
            p = d.get("payload", {})
            ts = d.get("timestamp")
            mentioned = BATCH_RE.findall(line)
            if mentioned:
                current_batch = mentioned[-1]

            if t == "response_item" and p.get("type") == "custom_tool_call":
                inp = p.get("input", "")
                call_by_id[p.get("call_id")] = {
                    "ts": ts, "batch": current_batch, "input": inp[:4000],
                    "refs": sorted(set(BATCH_RE.findall(inp))),
                }
            elif t == "response_item" and p.get("type") == "custom_tool_call_output":
                codes = [int(x) for x in EXIT_RE.findall(line)]
                code = max(codes) if codes else None
                call = call_by_id.get(p.get("call_id"))
                if call:
                    call["exit_code"] = code
                    b = call["batch"]
                    if b:
                        per_batch[b]["exec"] += 1
                        if code not in (0, None):
                            per_batch[b]["exec_failed"] += 1
            elif t == "response_item" and p.get("type") == "message":
                txt = " ".join(c.get("text", "") for c in p.get("content", []) if isinstance(c, dict))
                if p.get("role") == "user" and txt.strip():
                    kind = ("goal" if "codex_internal_context" in txt[:60] else
                            "env" if "environment_context" in txt[:40] else "human")
                    events.append((ts, "user_" + kind, txt.strip()[:300]))
                elif p.get("role") == "assistant" and txt.strip():
                    assistant_msgs.append((ts, txt.strip()))
                    events.append((ts, "assistant", txt.strip()[:200]))
            elif t == "compacted":
                compactions.append(ts)

    # 1. cross-batch consumption edges (tool inputs referencing earlier batches)
    edges = Counter()
    for call in call_by_id.values():
        b = call["batch"]
        if not b:
            continue
        for ref in call["refs"]:
            if ref != b and (b[0], int(b[1:3])) > (ref[0], int(ref[1:3])):
                edges[(b, ref)] += 1
                per_batch[b]["consume"][ref] += 1

    # 3. compaction-boundary context reconstruction
    calls_sorted = sorted(call_by_id.values(), key=lambda c: c["ts"])
    comp_points = sorted(compactions)
    for cts in comp_points:
        after = [c for c in calls_sorted if c["ts"] > cts][:15]
        reads = [c for c in after
                 if READ_HINT_RE.search(c["input"])
                 and (SUMMARY_ARTIFACT_RE.search(c["input"]) or BATCH_RE.search(c["input"]))]
        post_compaction_reads.append({
            "compaction": cts,
            "first_15_calls": len(after),
            "context_reconstructing_reads": len(reads),
            "examples": [r["input"][:120] for r in reads[:3]],
        })

    # 4. autonomy spans between substantive human messages
    human_msgs = [(ts, txt) for ts, kind, txt in events if kind == "user_human"]
    spans = []
    for i in range(len(human_msgs) + 1):
        start = human_msgs[i - 1][0] if i else "2026-09-12T08:16:45"
        end = human_msgs[i][0] if i < len(human_msgs) else "2026-09-13T06:44:55"
        inside = sorted({b for c in call_by_id.values()
                         if c["batch"] and start <= c["ts"] < end
                         for b in [c["batch"]]})
        spans.append({
            "span_start": start, "span_end": end,
            "opened_by": (human_msgs[i - 1][1][:120] if i else "(session start)"),
            "batches_touched": inside,
        })

    # 5. self-reported check trajectory from assistant messages
    num_re = re.compile(r"(\d+)\s*/\s*(\d+)\s*项|(\d+)\s*项[^。]{0,15}?(通过|超过|未通过|仍需|待调)")
    quality = []
    for ts, txt in assistant_msgs:
        hits = num_re.findall(txt)
        if hits:
            quality.append({"ts": ts, "hits": [h for h in hits], "excerpt": txt[:200]})

    out = {
        "release": "AstraBuild conversation deep analysis v0.1",
        "generated_by": "scripts/analyze_conversation_deep.py",
        "scope_notes": [
            "batch attribution follows the most recently mentioned installation folder.",
            "exec failure counts include exploratory commands; a density signal, not a quality score.",
            "cross-batch consumption counts tool inputs that reference earlier-batch paths; reads may serve validation, reuse, or review.",
        ],
        "per_batch_process": {
            b: {"exec": e["exec"], "exec_failed": e["exec_failed"],
                "exec_fail_rate": round(e["exec_failed"] / e["exec"], 3) if e["exec"] else None,
                "consumes": dict(e["consume"].most_common())}
            for b, e in sorted(per_batch.items())
        },
        "cross_batch_edges": [
            {"consumer": c, "consumed": r, "tool_inputs": n}
            for (c, r), n in edges.most_common(40)
        ],
        "compaction_boundaries": post_compaction_reads,
        "autonomy_spans": spans,
        "selfreported_quality": quality,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(OUT)
    fr = [(b, e["exec_failed"], e["exec"]) for b, e in sorted(per_batch.items()) if e["exec"] >= 10]
    fr.sort(key=lambda x: -x[1] / x[2])
    print("top trial-and-error batches:", [(b, f"{x}/{n}") for b, x, n in fr[:8]])
    print("top consumption edges:", [(c, r, n) for (c, r), n in edges.most_common(10)])
    rec = sum(1 for x in post_compaction_reads if x["context_reconstructing_reads"] > 0)
    print(f"compactions with context reconstruction: {rec}/{len(post_compaction_reads)}")


if __name__ == "__main__":
    main()
