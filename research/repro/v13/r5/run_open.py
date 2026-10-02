#!/usr/bin/env python3
"""run_open.py: R5 Block 1 for open-weight models (llama-cpp-python, CPU), conditions A, B, E, E+.
Same items, prompts and tool functions as the Claude runner; the tools are called in-process through a JSON
tool protocol instead of MCP. Resumable; appends to trials.jsonl (cost 0, CPU).

  python run_open.py <gguf path> <model label>
"""
import json, random, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import items as IT  # noqa: E402
import run_claude as RC  # noqa: E402
import score as S  # noqa: E402
import tools as T  # noqa: E402
from llama_cpp import Llama  # noqa: E402

OPEN_CONDS = ["A", "B", "E", "E+"]
TOOL_RE = re.compile(r"\{.*\"tool\"\s*:.*\}", re.S)


def protocol(cond):
    ts = T.TOOLS[cond]
    if not ts:
        return ""
    lines = ["\nTools. To call one, reply with ONLY one line of JSON and nothing else:",
             '{"tool": "<name>", "args": {<arguments>}}',
             "The harness replies with TOOL_RESULT: followed by the result. Available tools:"]
    for t in ts:
        props = t["inputSchema"]["properties"]
        req = t["inputSchema"].get("required", [])
        args = ", ".join(f"{k}{'' if k in req else ' (optional)'}" for k in props)
        lines.append(f"- {t['name']}({args}): {t['description']}")
    return "\n".join(lines)


def extract_call(txt):
    m = TOOL_RE.search(txt)
    if not m:
        return None
    s = m.group(0)
    for end in range(len(s), 0, -1):
        if s[end - 1] != "}":
            continue
        try:
            j = json.loads(s[:end])
            if isinstance(j, dict) and "tool" in j:
                return j
        except Exception:
            continue
    return None


def trial(llm, it, cond, seed, max_tool_turns=4):
    msgs = [{"role": "system", "content": IT.system_prompt(it) + protocol(cond)},
            {"role": "user", "content": IT.user_prompt(it, cond)}]
    calls, results, gen, ptok, t_llm = [], [], 0, 0, 0.0
    final = ""
    for turn in range(max_tool_turns + 1):
        t0 = time.time()
        r = llm.create_chat_completion(messages=msgs, temperature=0.7, top_p=0.95, seed=seed + turn, max_tokens=320)
        t_llm += time.time() - t0
        txt = r["choices"][0]["message"]["content"] or ""
        gen += r["usage"]["completion_tokens"]
        ptok += r["usage"]["prompt_tokens"]
        msgs.append({"role": "assistant", "content": txt})
        call = extract_call(txt) if T.TOOLS[cond] else None
        if call and turn < max_tool_turns and not S.DEC_RE.search(txt):
            name, args = call.get("tool"), call.get("args") or {k: v for k, v in call.items() if k != "tool"}
            err, out, meta = T.call(it, cond, name, args if isinstance(args, dict) else {})
            calls.append({"id": f"c{turn}", "name": name, "input": args})
            results.append({"tool_use_id": f"c{turn}", "is_error": err, "text": out})
            msgs.append({"role": "user", "content": "TOOL_RESULT: " + ("ERROR: " if err else "") + out})
            continue
        final = txt
        break
    return {"calls": calls, "results": results, "result_text": final, "gen_tokens": gen, "prompt_tokens": ptok,
            "llm_s": round(t_llm, 1), "messages": msgs}


def main():
    path, label = sys.argv[1], sys.argv[2]
    conds = sys.argv[3].split(",") if len(sys.argv) > 3 else OPEN_CONDS
    items = IT.build_items()
    cells = [(it["id"], c) for it in items for c in conds if c in it["conds"]]
    random.Random(f"{RC.SEED}-open-{label}").shuffle(cells)
    done = RC.done_ids()
    t0 = time.time()
    llm = Llama(model_path=path, n_ctx=4096, n_threads=4, seed=0, verbose=False)
    load_s = round(time.time() - t0, 1)
    print(f"loaded {label} in {load_s}s", flush=True)
    by = {i["id"]: i for i in items}
    for n, (iid, c) in enumerate(cells):
        tid = f"B1-{label}-{iid}-{c}-r1-1"
        if tid in done:
            continue
        it = by[iid]
        seed = 1000 * (n + 1)
        ts = time.time()
        tr = trial(llm, it, c, seed)
        tx = RC.analyse_transcript("1", it, c, tr, [])
        sc = S.score(it, c, tr["result_text"], seen_served=tx["seen_served"], verified_pass=tx["verified_pass"])
        row = {"trial_id": tid, "block": "1", "model": label, "item": iid, "cond": c, "rep": 1, "k": 1, "task": it["task"],
               "family": it["family"], "primary": it["primary"], "correct_output": it["correct"], "excluded": None, **sc, **tx,
               "latency_s": round(time.time() - ts, 1), "llm_s": tr["llm_s"], "cost_usd": 0.0, "tokens_in": tr["prompt_tokens"],
               "tokens_out": tr["gen_tokens"], "seed": seed, "runtime": "llama-cpp-python 0.3.35, CPU 4 threads, Q4_K_M",
               "load_s": load_s, "calls": [{"name": x["name"], "input": x["input"]} for x in tr["calls"]],
               "results_head": [{"is_error": x["is_error"], "text": x["text"][:500]} for x in tr["results"]],
               "final_text": tr["result_text"][-1500:], "ts": time.time()}
        RC.append(RC.TRIALS, row)
        print(f"{tid:45} {str(sc['decision']):12} fa={sc['fa']} calls={tx['n_tool_calls']} {row['latency_s']}s", flush=True)


if __name__ == "__main__":
    main()
