import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
os.environ["EMEM_MCP_CONFIG"]="emem_mcp_full.json"
os.environ["EMEM_DISALLOW"]=",".join("mcp__emem__"+t for t in ["emem_memory_create","emem_memory_insert","emem_memory_str_replace","emem_memory_rename","emem_memory_delete","emem_memory_supersede","emem_derive","emem_entity","emem_entity_link","emem_eudr_dds"])
import claude_run
PROMPT="Using emem, determine whether the surface at Keylong, Lahaul (32.57126 N, 77.03448 E) changed between the Sentinel-2 scenes of 23 Sep 2026 and 25 Sep 2026. Work from the raw band values, not a precomputed index: choose the bands and the method yourself. Cite every number you use by its emem token. End with exactly three lines: CHANGE=<greener|browner|no material change>, METHOD=<one line: bands and formula>, TOKENS=<comma-separated emem tokens you used>."
start=int(sys.argv[1]); end=int(sys.argv[2])
for i in range(start,end+1):
    attempt=0
    while True:
        tag=f"trial{i:02d}" + (f"_retry{attempt}" if attempt else "")
        r=claude_run.run(PROMPT,"claude-sonnet-5-5",tag,os.path.join(HERE,"raw"),budget="3")
        full=r.pop("_full_results")
        r["i"]=i; r["attempt"]=attempt
        json.dump(full,open(os.path.join(HERE,"raw",tag+".results_full.json"),"w"))
        infra = (not r["result_text"] and r["exit"]!=0) or not r["mcp_servers"] or any(s.get("status")!="connected" for s in (r["mcp_servers"] or []))
        r["infra_fail"]=bool(infra)
        with open(os.path.join(HERE,"trials.jsonl"),"a") as f: f.write(json.dumps(r)+"\n")
        print(tag, r["exit"], r["cost_usd"], r["wall_s"], len(r["calls"]), "INFRA" if infra else "", flush=True)
        if infra and attempt<2: attempt+=1; continue
        break
