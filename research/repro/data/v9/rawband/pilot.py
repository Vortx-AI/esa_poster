import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claude_run
which = sys.argv[1]
os.environ["EMEM_MCP_CONFIG"] = f"emem_mcp_{which}.json"
import importlib; importlib.reload(claude_run)
r = claude_run.run("List every emem tool available to you, with its exact name and a one-line description of what it does. Say specifically whether any tool can read raw Sentinel-2 band values (digital numbers / reflectances) at a point. Do not call any tools other than what you need to answer.", "claude-sonnet-5-5", f"pilot_{which}", os.path.join(os.path.dirname(os.path.abspath(__file__)),"raw"), budget="0.5")
r.pop("_full_results")
json.dump(r, open(f"raw/pilot_{which}.summary.json","w"), indent=1)
print(json.dumps({k:r[k] for k in ["tools_offered","mcp_servers","result_text","cost_usd","wall_s","exit"]}, indent=1))
