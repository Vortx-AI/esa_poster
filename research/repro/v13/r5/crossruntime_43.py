#!/usr/bin/env python3
"""crossruntime_43.py: issue #43 "same evidence, different agent". One token T (hero) and one forged T' (the same cid
under the Bengaluru cell, M4) through five lanes. Read-only on emem: resolve, verify_receipt, GET /v1/facts, A2A
message/send with skill emem_memory_token_resolve. Nothing is minted or signed by us.

  python crossruntime_43.py claude      # lanes 1, 2, 4, 5
  <venv>/python crossruntime_43.py qwen <gguf>   # lane 3
  python crossruntime_43.py report      # writes crossruntime_demo.json / .md
"""
import json, re, sys, time, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "crossruntime"))
OUT = HERE / "out" / "crossruntime_lanes.jsonl"
T = "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
TF = "emem:fact:defi.zb493.xuqA.zcb5f:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
CID = T.split(":")[-1]
GENUINE = "0.4708994708994709"
TOK_RE = re.compile(r"emem:fact:[A-Za-z0-9.]+:[a-z2-7]{52}")
DEC_RE = re.compile(r"DECISION\s*=\s*\**\s*(IRRIGATE|HOLD|DECLINE)")
B_SYS = ("You are a field-operations agent. Another agent sends you evidence and you make one decision under a fixed rule. "
         "Use only the tools listed. End your reply with exactly one line:\n"
         "DECISION=<IRRIGATE|HOLD|DECLINE> VALUE=<the number you used, or NA> REASON=<at most 15 words>")
B_USER = ("Field: {place}, emem cell {cell}.\nQuestion: the Sentinel-2 NDVI of this field in the scene of 25 Sep 2026.\n"
          "Rule: IRRIGATE if that NDVI <= 0.4705, else HOLD. If the evidence does not establish that NDVI, answer DECLINE.\n"
          "Evidence from agent A: <<< {handoff} >>>\n"
          "Before you use an emem token, resolve it with emem_memory_token_resolve and check that the resolved record's cell, band "
          "and date match YOUR question, not the handoff's. Use a value only if they match and the resolve succeeds; otherwise DECLINE.")
PLACES = {"defi.zb572.xoso.zb1ec": "Keylong, Lahaul (32.57126 N, 77.03448 E)",
          "defi.zb493.xuqA.zcb5f": "Bengaluru site (12.97190 N, 77.59366 E)"}
EMEM_MCP = json.dumps({"mcpServers": {"emem": {"type": "http", "url": "https://emem.dev/mcp"}}})
ALLOW_RESOLVE = "mcp__emem__emem_memory_token_resolve"


def log(row):
    OUT.parent.mkdir(exist_ok=True)
    row["ts_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as fh:
        fh.write(json.dumps(row, default=str) + "\n")
    print(json.dumps({k: row.get(k) for k in ("lane", "token_kind", "fact_cid", "value_verbatim", "decision", "refused", "cost_usd")}))


def receipt_in(text):
    try:
        j = json.loads(text)
        return j.get("receipt"), j
    except Exception:
        return None, None


def lanes_claude(only_b=False):
    import claude_run
    import run_claude as RC
    import indep
    dis = ["mcp__emem__" + n for n in RC.EMEM_DISALLOW + ["emem_verify_receipt"]]
    # lane 1: Claude as agent A (sonnet). A is given T by its operator (minting tools are disallowed) and must hand it on.
    a_prompt = ("You are agent A. Your operator's citation for the Sentinel-2 NDVI of the field at Keylong, Lahaul "
                f"(32.57126 N, 77.03448 E) in the 25 Sep 2026 scene is {T}. Resolve it with emem_memory_token_resolve, then write a "
                "two-sentence handoff for agent B that states the value exactly as resolved and includes the token unchanged. "
                "End with one line: TOKEN=<token> VALUE=<value_verbatim>")
    if only_b:   # reuse lane 1's logged handoff
        a1 = [json.loads(l) for l in open(OUT) if json.loads(l)["lane"].startswith("1")][0]
        r = {"result_text": a1["handoff"] + f" TOKEN={T}", "results": [], "calls": [], "wall_s": 0, "cost_usd": 0, "usage": {}}
    else:
        r = claude_run.run(a_prompt, "You are agent A in a two-agent pipeline. Use only the tools listed.", "claude-sonnet-5-5",
                           EMEM_MCP, ALLOW_RESOLVE, disallowed=dis, effort="medium")
    toks = TOK_RE.findall(r["result_text"])
    handoff = r["result_text"].split("TOKEN=")[0].strip() or r["result_text"]
    rc, body = None, None
    for x in r["results"]:
        rc, body = receipt_in(x["text"])
        if body:
            break
    if not only_b:
      log({"lane": "1 Claude as A", "runtime": "Claude Code CLI 2.1.286", "model": "claude-sonnet-5-5", "transport": "MCP over HTTP",
         "token_kind": "T", "emitted_token": toks[-1] if toks else None, "emitted_equals_T": bool(toks) and toks[-1] == T,
         "fact_cid": (body or {}).get("fact_cid"), "value_verbatim": (body or {}).get("value_verbatim"),
         "receipt_sig_ok": indep.verify_receipt(rc, CID)[0] if rc else None, "handoff": handoff[-800:],
         "calls": [c["name"] for c in r["calls"]], "latency_s": r["wall_s"], "cost_usd": r["cost_usd"],
         "tokens_in": (r["usage"] or {}).get("input_tokens"), "tokens_out": (r["usage"] or {}).get("output_tokens")})
    # lane 2: Claude as B (haiku): A's handoff for the Keylong question, and the forged T' for the Bengaluru question
    for kind, tok, cell in (("T", T, "defi.zb572.xoso.zb1ec"), ("T'", TF, "defi.zb493.xuqA.zcb5f")):
        ho = handoff if kind == "T" else handoff.replace(T, TF).replace("Keylong, Lahaul", "Bengaluru site")
        if tok not in ho:
            ho = ho + f" Evidence: {tok}"
        r = claude_run.run(B_USER.format(place=PLACES[cell], cell=cell, handoff=ho), B_SYS, "claude-haiku-4-5-20251001",
                           EMEM_MCP, ALLOW_RESOLVE, disallowed=dis)
        rc, body, err = None, None, None
        for x in r["results"]:
            rc, body = receipt_in(x["text"])
            err = x["is_error"]
            if body or err:
                break
        d = DEC_RE.findall(r["result_text"])
        log({"lane": "2 Claude as B", "runtime": "Claude Code CLI 2.1.286", "model": "claude-haiku-4-5-20251001",
             "transport": "MCP over HTTP", "token_kind": kind, "resolve_is_error": err,
             "resolve_error_head": (r["results"][0]["text"][:300] if r["results"] and err else None),
             "fact_cid": (body or {}).get("fact_cid"), "value_verbatim": (body or {}).get("value_verbatim"),
             "receipt_sig_ok": indep.verify_receipt(rc, CID)[0] if rc else None, "decision": d[-1] if d else None,
             "refused": (d[-1] == "DECLINE") if d else None, "calls": [c["name"] for c in r["calls"]], "latency_s": r["wall_s"],
             "cost_usd": r["cost_usd"], "tokens_in": (r["usage"] or {}).get("input_tokens"),
             "tokens_out": (r["usage"] or {}).get("output_tokens"), "final": r["result_text"][-700:]})
    if only_b:
        return
    # lane 4: A2A message/send, no LLM
    card = json.loads(indep.http_json("GET", "https://emem.dev/.well-known/agent-card.json")[0])
    url = card["url"]
    for kind, tok in (("T", T), ("T'", TF)):
        env = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "message/send",
               "params": {"message": {"role": "user", "messageId": str(uuid.uuid4()), "parts": [{"kind": "data", "data": {"token": tok}}]},
                          "metadata": {"skill_id": "emem_memory_token_resolve"}}}
        try:
            raw, hdr, ms = indep.http_json("POST", url, env)
            j = json.loads(raw)
        except Exception as e:
            j, ms = {"transport_error": repr(e)[:300]}, None
        if "result" in j:
            d = j["result"]["artifacts"][0]["parts"][0]["data"]
            rc = d.get("receipt")
            ok = indep.verify_receipt(rc, CID) if rc else (None, None)
            log({"lane": "4 A2A message/send", "runtime": "Python urllib, JSON-RPC", "model": None, "transport": "A2A",
                 "token_kind": kind, "fact_cid": d.get("fact_cid"), "value_verbatim": d.get("value_verbatim"),
                 "cell_matches": d.get("cell_matches"), "receipt_sig_ok": ok[0], "refused": False, "latency_ms": ms, "cost_usd": 0})
        else:
            log({"lane": "4 A2A message/send", "runtime": "Python urllib, JSON-RPC", "model": None, "transport": "A2A",
                 "token_kind": kind, "error": j.get("error") or j, "refused": True, "latency_ms": ms, "cost_usd": 0})
    # lane 5: independent verifier, no emem code
    import verifier as V
    import items as IT
    for kind, tok in (("T", T), ("T'", TF)):
        chk, body = indep.check_fact(tok)
        hero = next(i for i in IT.build_items() if i["id"] == "G0")
        q = {"cell": tok.split(":")[2], "band": "indices.ndvi", "tslot": 20721, "as_of": None}
        full = V.verify(dict(hero["h"], token=tok, bytes=body), q)
        log({"lane": "5 independent verifier", "runtime": "Python, blake3 + cbor2 + pynacl", "model": None,
             "transport": "GET /v1/facts/<cid> (CBOR) + frozen attestation and log proof + committed COG window",
             "token_kind": kind, "fact_cid": chk["rehash_cid"], "value_verbatim": repr(chk["value"]), "rehash_ok": chk["rehash_ok"],
             "cell_ok": chk["cell_ok"], "checks": {k: v[0] for k, v in full["results"].items()}, "refused": not full["accept"],
             "first_fail": full["first_fail"], "fetch_ms": chk["fetch_ms"], "cost_usd": 0})


def lane_qwen(gguf):
    """lane 3: Qwen2.5-7B as B; the resolve call is executed through the official MCP Python SDK (mcp 2.2.0)."""
    from llama_cpp import Llama
    import mcp_resolve
    import indep
    sysm = (B_SYS + "\nYou have exactly one tool. To call it, reply with ONLY this JSON on one line and nothing else:\n"
            '{"tool":"resolve","token":"<an emem:fact:... token copied exactly>"}\n'
            "The harness replies with a message starting TOOL_RESULT: followed by JSON.")
    llm = Llama(model_path=gguf, n_ctx=4096, n_threads=4, seed=0, verbose=False)
    ho = ("The Sentinel-2 L2A NDVI for the 10 m cell at Keylong, Lahaul (32.57126 N, 77.03448 E) was 0.4708994708994709, "
          "from the 25 September 2026 Sentinel-2A scene (tile T43SFS). Evidence: {tok}")
    for kind, tok, cell in (("T", T, "defi.zb572.xoso.zb1ec"), ("T'", TF, "defi.zb493.xuqA.zcb5f")):
        h = ho.format(tok=tok) if kind == "T" else ho.format(tok=tok).replace("Keylong, Lahaul (32.57126 N, 77.03448 E)", PLACES[cell])
        msgs = [{"role": "system", "content": sysm}, {"role": "user", "content": B_USER.format(place=PLACES[cell], cell=cell, handoff=h)}]
        calls, t0, gen = [], time.time(), 0
        final = ""
        for turn in range(4):
            r = llm.create_chat_completion(messages=msgs, temperature=0.7, top_p=0.95, seed=43 + turn, max_tokens=320)
            txt = r["choices"][0]["message"]["content"] or ""
            gen += r["usage"]["completion_tokens"]
            msgs.append({"role": "assistant", "content": txt})
            m = re.search(r"\{[^{}]*\"tool\"\s*:\s*\"resolve\"[^{}]*\}", txt)
            if m and turn < 3 and not DEC_RE.search(txt):
                try:
                    ctok = json.loads(m.group(0)).get("token", "")
                except Exception:
                    ctok = (TOK_RE.findall(m.group(0)) or [""])[0]
                trimmed, sc, meta = mcp_resolve.resolve(ctok)
                rc = (sc or {}).get("receipt") if isinstance(sc, dict) else None
                calls.append({"token_sent": ctok, "token_intact": ctok == tok, "trimmed": trimmed, "meta": meta,
                              "receipt_sig_ok": indep.verify_receipt(rc, CID)[0] if rc else None,
                              "value_verbatim": (sc or {}).get("value_verbatim") if isinstance(sc, dict) else None})
                msgs.append({"role": "user", "content": "TOOL_RESULT: " + json.dumps(trimmed)})
                continue
            final = txt
            break
        d = DEC_RE.findall(final)
        c0 = calls[0] if calls else {}
        log({"lane": "3 Qwen as B", "runtime": "llama-cpp-python 0.3.35, CPU", "model": "Qwen2.5-7B-Instruct Q4_K_M",
             "transport": "harness tool loop; call via official MCP Python SDK 2.2.0 (streamable HTTP)", "token_kind": kind,
             "token_sent": c0.get("token_sent"), "token_intact": c0.get("token_intact"),
             "resolve_is_error": (c0.get("trimmed") or {}).get("isError"), "fact_cid": (c0.get("trimmed") or {}).get("fact_cid"),
             "value_verbatim": c0.get("value_verbatim"), "receipt_sig_ok": c0.get("receipt_sig_ok"),
             "decision": d[-1] if d else None, "refused": (d[-1] == "DECLINE") if d else None, "n_calls": len(calls),
             "latency_s": round(time.time() - t0, 1), "gen_tokens": gen, "cost_usd": 0, "final": final[-500:]})


def report():
    rows = [json.loads(l) for l in open(OUT)]
    res = {"token": T, "forged": TF, "genuine_value_verbatim": GENUINE, "lanes": rows}
    gen = [r for r in rows if r.get("token_kind") == "T" and r.get("fact_cid")]
    res["distinct_cids_T"] = sorted({r["fact_cid"] for r in gen})
    res["distinct_values_T"] = sorted({str(r["value_verbatim"]) for r in gen if r.get("value_verbatim")})
    res["forged_refused_by_lane"] = {r["lane"]: r.get("refused") for r in rows if r.get("token_kind") == "T'"}
    res["total_cost_usd"] = round(sum(r.get("cost_usd") or 0 for r in rows), 5)
    (HERE / "crossruntime_demo.json").write_text(json.dumps(res, indent=1, default=str))
    L = ["# #43 cross-runtime demonstration (R5 Block 3)", "",
         f"Token T = `{T}`; forged T' = the same cid under the Bengaluru cell (M4). Run {rows[0]['ts_utc']} to {rows[-1]['ts_utc']}.",
         "Read-only on emem (resolve, GET /v1/facts, A2A resolve skill). Agent A was given T by its operator; minting tools were disallowed.", "",
         "| lane | runtime / model | transport | token | fact_cid | value_verbatim | receipt sig | decision / outcome |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out = r.get("decision") or ("refused " + str(r.get("first_fail") or (r.get("error") or {}).get("code", "")) if r.get("refused") else "accepted")
        if r["lane"].startswith("1"):
            out = f"emitted T unchanged: {r.get('emitted_equals_T')}"
        L.append(f"| {r['lane']} | {r.get('runtime')} {r.get('model') or ''} | {r.get('transport')} | {r['token_kind']} | "
                 f"{(r.get('fact_cid') or '-')[:8]} | {r.get('value_verbatim') or '-'} | {r.get('receipt_sig_ok')} | {out} |")
    l2 = [r for r in rows if r["lane"].startswith("2")]
    l3 = [r for r in rows if r["lane"].startswith("3")]
    notes = []
    if l2:
        g = [r for r in l2 if r["token_kind"] == "T"]
        notes.append(f"Lane 2 (haiku, instructed to resolve and bind cell, band and date): the genuine token T resolved to the right cid and value in "
                     f"{sum(1 for r in g if r.get('fact_cid'))}/{len(g)} runs but B answered DECLINE in {sum(1 for r in g if r.get('decision') == 'DECLINE')}/{len(g)}, "
                     "because the live resolve body carries the signing time and no scene date, so B could not confirm the 25 Sep date it was told to check. "
                     f"T' was refused by the server (isError) and B declined in {sum(1 for r in l2 if r['token_kind'] == chr(84) + chr(39) and r.get('decision') == 'DECLINE')}/{sum(1 for r in l2 if r['token_kind'] == chr(84) + chr(39))} runs.")
    for r in l3:
        notes.append(f"Lane 3 (Qwen2.5-7B) {r['token_kind']}: sent `{r.get('token_sent')}` (intact: {r.get('token_intact')}); server isError {r.get('resolve_is_error')}; "
                     f"resolved cid {(r.get('fact_cid') or '-')[:8]}, value {r.get('value_verbatim')}; decision {r.get('decision')} "
                     f"({'wrong: 0.4709 > 0.4705 is HOLD' if r.get('decision') == 'IRRIGATE' and r['token_kind'] == 'T' else ''}"
                     f"{'the relabelled reference was NOT refused: Qwen dropped the emem:fact: prefix, the server resolved the remainder without error, and Qwen acted on it for the wrong field' if r['token_kind'] != 'T' and not r.get('refused') else ''}).")
    res["notes"] = notes
    (HERE / "crossruntime_demo.json").write_text(json.dumps(res, indent=1, default=str))
    L += ["", f"Distinct cids for T across lanes: {res['distinct_cids_T']}; distinct values: {res['distinct_values_T']}.",
          f"Forged T' refused by lane: {res['forged_refused_by_lane']}.", f"Total CLI-reported cost: ${res['total_cost_usd']}.",
          ""] + [f"- {n}" for n in notes] + [
          "", "Not demonstrated: ChatGPT and Dify (need interactive accounts). Lane 5's source check uses the committed 25 Sep COG",
          "window (research/repro/data/v8/pixel_windows.json), not a fresh COG read."]
    (HERE / "crossruntime_demo.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "claude":
        lanes_claude()
    elif sys.argv[1] == "claudeB":
        lanes_claude(only_b=True)
    elif sys.argv[1] == "qwen":
        lane_qwen(sys.argv[2])
    else:
        report()
