"""STEP 2a: agent B, cross-family = Qwen2.5-Instruct GGUF (llama-cpp-python, CPU), minimal JSON tool loop.
Tool call: the model emits {"tool":"resolve","token":"..."}; the harness executes it via the official MCP Python SDK against
https://emem.dev/mcp (tools/call emem_memory_token_resolve) and returns the trimmed JSON. The harness separately re-hashes the CBOR and
verifies the receipt with independent code (common.harness_verify -> crossruntime/indep.py)."""
import json, os, re, sys, time
from llama_cpp import Llama
import common, mcp_resolve

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM = ("You are an agent with exactly one tool. To call it, reply with ONLY this JSON on one line and nothing else:\n"
          "{\"tool\":\"resolve\",\"token\":\"<an emem:fact:... token copied exactly>\"}\n"
          "The harness will reply with a message starting TOOL_RESULT: followed by JSON. "
          "Call the tool at most once per token. When you are done, give your answer.")
TOOL_RE = re.compile(r"\{[^{}]*\"tool\"\s*:\s*\"resolve\"[^{}]*\}")


def load(path, seed=0):
    return Llama(model_path=path, n_ctx=4096, n_threads=4, seed=seed, verbose=False)


def trial(llm, handoff, seed, max_tool_turns=3):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": common.B_TEMPLATE.format(handoff=handoff)}]
    tool_calls, gen_tokens, gen_s, prompt_tokens = [], 0, 0.0, 0
    final = None
    for turn in range(max_tool_turns + 1):
        t0 = time.time()
        r = llm.create_chat_completion(messages=msgs, temperature=0.7, top_p=0.95, seed=seed + turn, max_tokens=300)
        dt = time.time() - t0
        txt = r["choices"][0]["message"]["content"] or ""
        gen_tokens += r["usage"]["completion_tokens"]; prompt_tokens += r["usage"]["prompt_tokens"]; gen_s += dt
        msgs.append({"role": "assistant", "content": txt})
        m = TOOL_RE.search(txt)
        if m and turn < max_tool_turns:
            try:
                call = json.loads(m.group(0))
            except Exception:
                call = {"tool": "resolve", "token": (common.TOK_RE.findall(m.group(0)) or [""])[0]}
            tok = call.get("token", "")
            t1 = time.time()
            try:
                trimmed, sc, meta = mcp_resolve.resolve(tok)
            except Exception as e:
                trimmed, sc, meta = {"isError": True, "error": f"transport error: {e!r}"[:300]}, None, {}
            rec = {"token": tok, "trimmed": trimmed, "meta": meta, "tool_s": round(time.time() - t1, 2)}
            # harness-side independent check of whatever the server actually served (full token or bare cid)
            vtok = tok if common.TOK_RE.fullmatch(tok) else ((sc or {}).get("canonical_token") if isinstance(sc, dict) and not trimmed.get("isError") else None)
            rec["token_form"] = "full" if common.TOK_RE.fullmatch(tok) else ("bare_cid" if common.CID_RE.fullmatch(tok) else "malformed")
            rec["harness"] = common.harness_verify(vtok, (sc or {}).get("receipt") if isinstance(sc, dict) else None) if vtok else {}
            rec["receipt"] = (sc or {}).get("receipt") if isinstance(sc, dict) else None
            rec["server_degraded"] = (sc or {}).get("degraded") if isinstance(sc, dict) else None
            rec["server_cell"] = (sc or {}).get("cell") if isinstance(sc, dict) else None
            tool_calls.append(rec)
            msgs.append({"role": "user", "content": "TOOL_RESULT: " + json.dumps(trimmed)})
            continue
        final = txt
        break
    return {"messages": msgs, "tool_calls": tool_calls, "final": final, "gen_tokens": gen_tokens, "prompt_tokens": prompt_tokens, "llm_s": round(gen_s, 2)}


if __name__ == "__main__":
    model_path = sys.argv[1]
    llm = load(model_path)
    # warm-up / speed (not a trial)
    t0 = time.time(); r = llm.create_chat_completion(messages=[{"role": "user", "content": "Count from 1 to 30 separated by spaces."}], temperature=0.0, max_tokens=80)
    dt = time.time() - t0
    print(json.dumps({"warmup_completion_tokens": r["usage"]["completion_tokens"], "prompt_tokens": r["usage"]["prompt_tokens"], "s": round(dt, 2),
                      "tok_per_s_incl_prompt": round(r["usage"]["completion_tokens"] / dt, 2)}))
