#!/usr/bin/env python3
"""Mine the preserved Codex conversation log of the AstraBuild B01-B36 run.

Reads conversation_logs/astra_b01_b36_session.jsonl (NOT tracked by git) and
produces release/conversation_analysis.json: session anatomy, per-batch
timeline, user interventions, assistant decision messages, tool-call and
token-usage series.

Scope notes / caveats:
- reasoning items carry only encrypted_content: the private chain-of-thought
  is NOT readable. Analysis covers visible messages and tool calls only.
- assistant messages are self-reported accounts by the model; counts quoted
  from them (e.g. "37/60 checks passed") are the model's own reports, not
  independent validator output.
- batch attribution of tool calls is approximate: an event is attributed to
  the most recently mentioned installation_* folder at that point in the log.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "conversation_logs" / "astra_b01_b36_session.jsonl"
OUT = ROOT / "release" / "conversation_analysis.json"

BATCH_RE = re.compile(r"installation_([BCDR]\d{2})")
CHECK_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s*项")
PASS_RE = re.compile(r"(\d+)\s*项[^。]{0,12}通过|通过[^。]{0,12}?(\d+)\s*项")


def classify_user(text: str) -> str:
    if "codex_internal_context" in text[:60]:
        return "goal_auto_continuation"
    t = text.strip()
    if any(k in t for k in ["复用就行", "完全一样", "授权"]):
        return "authorization"
    if any(k in t for k in ["我觉得", "不对", "有角度差", "问题"]):
        return "correction_or_review"
    if t.startswith("\\") or t in ("ls",):
        return "command"
    return "instruction"


def main():
    batches = defaultdict(lambda: {
        "first_mention": None, "last_mention": None,
        "tool_calls": 0, "assistant_messages": 0,
        "check_reports": [], "summary_excerpt": None, "review_link": None,
    })
    users = []
    assistants = []
    tool_calls = Counter()
    tool_by_name = Counter()
    tokens = {"input": 0, "cached_input": 0, "output": 0, "reasoning_output": 0, "records": 0}
    token_series = Counter()
    compactions = []
    current_batch = None
    t0 = t1 = None
    n_records = 0
    n_reasoning = 0

    with open(SRC, errors="replace") as fh:
        for line in fh:
            n_records += 1
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("type")
            p = d.get("payload", {})
            ts = d.get("timestamp")
            if ts:
                t0 = t0 or ts
                t1 = ts
                hour = ts[:13]
            else:
                hour = None

            line_batches = set(BATCH_RE.findall(line))
            if line_batches:
                # most specific: last mention on the line drives attribution
                current_batch = BATCH_RE.findall(line)[-1]
            for b in line_batches:
                e = batches[b]
                e["first_mention"] = e["first_mention"] or ts
                e["last_mention"] = ts

            if t == "response_item":
                pt = p.get("type")
                if pt == "reasoning":
                    n_reasoning += 1
                elif pt == "custom_tool_call":
                    tool_by_name[p.get("name", "?")] += 1
                    if hour:
                        tool_calls[hour] += 1
                    if current_batch:
                        batches[current_batch]["tool_calls"] += 1
                elif pt == "message":
                    txt = " ".join(c.get("text", "") for c in p.get("content", []) if isinstance(c, dict))
                    role = p.get("role")
                    if role == "user":
                        if txt.strip():
                            users.append({"ts": ts, "kind": classify_user(txt), "excerpt": txt.strip()[:400]})
                    elif role == "assistant" and txt.strip():
                        msg_batches = sorted(set(BATCH_RE.findall(txt)))
                        checks = [(int(a), int(b)) for a, b in CHECK_RE.findall(txt)]
                        entry = {"ts": ts, "batches": msg_batches, "excerpt": txt.strip()[:600]}
                        assistants.append(entry)
                        for b in msg_batches:
                            batches[b]["assistant_messages"] += 1
                            batches[b]["summary_excerpt"] = txt.strip()[:400]
                            m = re.search(r"installation_" + b + r"/[^\s)]*review\.html", txt)
                            if m:
                                batches[b]["review_link"] = m.group(0)
                            if checks:
                                batches[b]["check_reports"].append({"ts": ts, "checks": checks, "excerpt": txt.strip()[:200]})
            elif t == "token_usage_record":
                u = p.get("usage", {})
                tokens["input"] += u.get("input_tokens", 0)
                tokens["cached_input"] += u.get("cached_input_tokens", 0)
                tokens["output"] += u.get("output_tokens", 0)
                tokens["reasoning_output"] += u.get("reasoning_output_tokens", 0)
                tokens["records"] += 1
                if hour:
                    token_series[hour] += u.get("total_tokens", 0)
            elif t == "compacted":
                compactions.append(ts)

    user_kinds = Counter(u["kind"] for u in users)

    out = {
        "release": "AstraBuild conversation analysis v0.1",
        "generated_by": "scripts/analyze_conversation.py",
        "source": {
            "file": "conversation_logs/astra_b01_b36_session.jsonl (git-ignored copy)",
            "origin": "~/.codex/sessions/2026/09/12/rollout-2026-09-12T15-34-19-01a09489-e32f-7e40-ba52-6d3183ad6ba8.jsonl",
        },
        "scope_notes": [
            "reasoning items are encrypted; analysis covers visible messages and tool calls only.",
            "assistant messages are model self-reports, not independent validator output.",
            "batch attribution of tool calls follows the most recently mentioned installation folder.",
        ],
        "session": {
            "start_utc": t0, "end_utc": t1,
            "records": n_records,
            "reasoning_items_encrypted": n_reasoning,
            "assistant_messages": len(assistants),
            "user_messages": len(users),
            "tool_calls": sum(tool_by_name.values()),
            "tool_calls_by_name": dict(tool_by_name.most_common()),
            "compactions": len(compactions),
            "compaction_times": compactions,
        },
        "token_usage": tokens,
        "token_series_by_hour": dict(sorted(token_series.items())),
        "tool_calls_by_hour": dict(sorted(tool_calls.items())),
        "user_intervention_kinds": dict(user_kinds),
        "user_messages": users,
        "batches": {b: batches[b] for b in sorted(batches)},
        "assistant_messages": assistants,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(OUT)
    print(f"batches found: {len(batches)}, users: {len(users)}, assistants: {len(assistants)}, "
          f"tool calls: {sum(tool_by_name.values())}, tokens in/out: {tokens['input']}/{tokens['output']}")


if __name__ == "__main__":
    main()
