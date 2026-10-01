#!/usr/bin/env python3
"""What does an agent receive when it asks each public EO service about ONE scene / place,
and can a SECOND agent independently check it?  Re-runnable; uses curl (proxy-aware) only.
No emem code is imported.  Writes industry_probe.json next to this file.

Scene: Sentinel-2A L2A, tile 43SFS, 2026-09-25 (the scene behind emem fact oj5cecci...).
Place: Bengaluru (77.59E, 12.97N) for NASA CMR.
"""
import json, subprocess, struct, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {"run_at_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
SCENE = "S2A_MSIL2A_20260925T054251_N0513_R005_T43SFS_20260925T090015"


def curl(args, timeout=60):
    r = subprocess.run(["curl", "-sS", "-m", str(timeout)] + args, capture_output=True)
    return r.stdout


def curl_code(url):
    return curl(["-o", "/dev/null", "-w", "%{http_code}", url]).decode()


def sse_json(b):
    s = b.decode()
    for line in s.splitlines():
        if line.startswith("data:"):
            return json.loads(line[5:])
    return json.loads(s)


# 1. NASA official Earthdata MCP (cmr.earthdata.nasa.gov/mcp/v1)
EP = "https://cmr.earthdata.nasa.gov/mcp/v1"
H = ["-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream"]
hdr = curl(["-D", "-", "-o", "/dev/null", "-X", "POST", EP] + H + ["-d", json.dumps(
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18",
     "capabilities": {}, "clientInfo": {"name": "probe", "version": "0"}}})]).decode()
sid = re.search(r"(?im)^mcp-session-id:\s*(\S+)", hdr).group(1)
S = H + ["-H", f"mcp-session-id: {sid}"]
curl(["-X", "POST", EP] + S + ["-d", '{"jsonrpc":"2.0","method":"notifications/initialized"}'])
tools = sse_json(curl(["-X", "POST", EP] + S + ["-d", '{"jsonrpc":"2.0","id":2,"method":"tools/list"}']))
call = sse_json(curl(["-X", "POST", EP] + S + ["-d", json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {"name": "get_granules", "arguments": {"collection_concept_id": "C2021957295-LPCLOUD",
    "temporal_start_date": "2026-09-01T00:00:00Z", "temporal_end_date": "2026-09-29T00:00:00Z",
    "spatial_wkt_geometry": "POINT(77.59 12.97)", "limit": 1}}})]))
g = call["result"]["structuredContent"]["granules"][0]
cid, rev = g["concept_id"], g["revision_id"]
gtxt = json.dumps(g).lower()
revs = {r: curl_code(f"https://cmr.earthdata.nasa.gov/search/concepts/{cid}/{r}.umm_json") for r in range(1, rev + 2)}
umm = json.loads(curl([f"https://cmr.earthdata.nasa.gov/search/concepts/{cid}/{rev}.umm_json"]))
OUT["nasa_cmr_mcp"] = {
    "tools": [t["name"] for t in tools["result"]["tools"]],
    "granule_keys": sorted(g.keys()), "concept_id": cid, "revision_id": rev,
    "granule_ur": g["granule_ur"], "n_access_urls": len(g["access_urls"]),
    "access_urls_protected": all("protected" in u for u in g["access_urls"]),
    "has_checksum_in_mcp_result": any(w in gtxt for w in ["checksum", "md5", "sha256"]),
    "umm_archive_info": umm.get("DataGranule", {}).get("ArchiveAndDistributionInformation"),
    "revision_http_codes": revs,
}

# 2. Microsoft Planetary Computer STAC (same scene emem read)
item = json.loads(curl(["-X", "POST", "https://planetarycomputer.microsoft.com/api/stac/v1/search",
    "-H", "Content-Type: application/json", "-d", json.dumps({"collections": ["sentinel-2-l2a"],
    "datetime": "2026-09-25T00:00:00Z/2026-09-25T23:59:59Z", "query": {"s2:mgrs_tile": {"eq": "43SFS"}}, "limit": 5})]))
f = [x for x in item["features"] if x["id"].startswith("S2A_MSIL2A_20260925T054251")][0]
b08 = f["assets"]["B08"]
sas = json.loads(curl(["https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a"]))
head = curl(["-I", b08["href"] + "?" + sas["token"]]).decode()
OUT["mpc_stac"] = {
    "item_id": f["id"], "b08_asset_keys": sorted(b08.keys()),
    "item_has_file_checksum": "file:checksum" in json.dumps(f),
    "item_has_created_or_updated": any(k in f["properties"] for k in ("created", "updated")),
    "sas_expiry": sas.get("msft:expiry"),
    "b08_head": {k: (re.search(rf"(?im)^{k}:\s*(.+)$", head).group(1).strip() if re.search(rf"(?im)^{k}:", head) else None)
                 for k in ["Content-Length", "ETag", "Content-MD5", "Last-Modified"]},
}

# 3. Copernicus Data Space Ecosystem OData (same scene)
od = json.loads(curl(["-G", "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
    "--data-urlencode", f"$filter=Name eq '{SCENE}.SAFE'"]))
p = od["value"][0]
OUT["cdse_odata"] = {"id": p["Id"], "name": p["Name"], "checksums": p.get("Checksum"),
                     "content_length": p.get("ContentLength"), "publication": p.get("PublicationDate")}

# 4. AlphaEarth Foundations annual embeddings index on Source Cooperative (parquet footer only)
U = "https://data.source.coop/tge-labs/aef/v1/annual/aef_index.parquet"
h = curl(["-I", U]).decode()
size = int(re.search(r"(?im)^content-length:\s*(\d+)", h).group(1))
tail = curl(["-r", f"{size-8}-{size-1}", U]); n = struct.unpack("<I", tail[:4])[0]
foot = curl(["-r", f"{size-8-n}-{size-1}", U])
try:
    import pyarrow as pa, pyarrow.parquet as pq
    pf = pq.ParquetFile(pa.BufferReader(pa.py_buffer(b"PAR1" + foot)))
    cols, rows = pf.schema_arrow.names, pf.metadata.num_rows
except Exception as e:  # pyarrow missing
    cols, rows = f"pyarrow unavailable: {e}", None
OUT["alphaearth_source_coop_index"] = {"url": U, "bytes": size, "rows": rows, "columns": cols,
    "etag": re.search(r'(?im)^etag:\s*(.+)$', h).group(1).strip(),
    "has_hash_column": isinstance(cols, list) and any(re.search("hash|checksum|md5|sha|blake", c, re.I) for c in cols)}

# 5. emem: resolve a token over MCP, and check what comes back
r = sse_json(curl(["-X", "POST", "https://emem.dev/mcp"] + H + ["-d", json.dumps({"jsonrpc": "2.0", "id": 2,
    "method": "tools/call", "params": {"name": "emem_memory_token_resolve", "arguments": {"token":
    "emem:fact:defi.zb493.zezo.zcb35:nflpddk7zsncywguwjzk5koksseqfyx4jnngkuryrnd4aykqlpfq"}}})]))
sc = r["result"]["structuredContent"]
OUT["emem_mcp_resolve"] = {"value": sc["value"], "unit": sc["unit"], "band": sc["band"], "fact_cid": sc["fact_cid"],
    "receipt_keys": sorted(sc["receipt"].keys()), "receipt_preimage_version": sc["receipt"]["preimage_version"],
    "responder_pubkey_b32": sc["receipt"]["responder_pubkey_b32"], "provenance_class": sc["provenance"].get("class"),
    "fact_url_status_no_auth": curl_code(sc["fact_url"])}

json.dump(OUT, open(os.path.join(HERE, "industry_probe.json"), "w"), indent=1, default=str)
print(json.dumps(OUT, indent=1, default=str))
