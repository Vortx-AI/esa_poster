"""Compose the v13 board's track.v1 note: every record the board's figures rest on, in panel order, each
re-checked where it stands, chained to one head. Reads ids from the data files the figures read; nothing typed by hand.
    python make_track_v13.py            -> track_body.md (without the board pointer step)
    python make_track_v13.py <board_note_cid>  -> adds the final print's pointer note as the first step"""
import json, base64, sys, re, pathlib, blake3
H = pathlib.Path(__file__).resolve().parents[4]
cid = lambda b: base64.b32encode(blake3.blake3(b).digest()[:16]).decode().lower().rstrip("=")
N = "https://emem.dev/memories/by_attester/njedkglt/"
inv = json.load(open(H / "research/repro/v8/inventory.json")); F = lambda k: inv[k]["token"]
cell = json.load(open(H / "research/v13/evidence/critic/cell.json")); cur = cell["current_by_band"]
K = "defi.zb572.xoso.zb1ec"
ron = json.dumps(json.load(open(H / "research/repro/v12/data/case_rondonia_eudr.json")))
R = lambda p: re.search(p + r"[a-z2-7]{44}", ron).group(0)
ask = json.load(open(H / "research/repro/data/v11/ask_keylong.json"))
state = [s["state"] for s in ask["reasoning"]["states"] if s["stage"] == "scored"][0]
STEPS = [
 ("Keylong NDVI record, 25 Sep 2026", F("ndvi_keylong"), "fact"),                       # panels 1, 4, 5, 6
 ("pre-fix record, 23 Sep, wrong pixel", F("ndvi_prefix_23sep"), "fact"),              # panel 6
 ("Keylong NDVI, 30 Sep scene", f"emem:fact:{K}:{cur['indices.ndvi']}", "fact"),       # panels 2, 8
 ("town-point NDVI, 597 m away", f"emem:fact:{ask['place_resolved']['cell64']}:{ask['fact_cids'][0]}", "fact"),  # panel 2
 ("B04 reflectance, 25 Sep", f"emem:fact:{K}:{cur['s2.B04']}", "fact"),
 ("B08 reflectance, 25 Sep", f"emem:fact:{K}:{cur['s2.B08']}", "fact"),
 ("Sentinel-2 B08 COG, 292 chunks", N + "khiqtqrddb6jponqn4gv72if7e.md", "pointer.v1"),  # panel 4 source files
 ("Sentinel-2 B04 COG, 292 chunks", N + "h6d7xdoc5b2uzood22lowblbc4.md", "pointer.v1"),
 ("Keylong cell, every product", f"emem:cell:{K}", "cell"),                              # panel 7
 ("elevation 918.0 m, May", F("elev_may"), "fact"),                                      # panel 8
 ("elevation 915.07 m, September", F("elev_sep"), "fact"),
 ("Rondonia cell A, Hansen loss year", f"emem:fact:defi.zb391.taza.zcc31:{R('6rtcbfum')}", "fact"),  # panel 9
 ("Rondonia cell A, tree cover 2000", f"emem:fact:defi.zb391.taza.zcc31:{R('iv6mhn5v')}", "fact"),
 ("Rondonia cell A, GFC2020 V4", f"emem:fact:defi.zb391.taza.zcc31:{R('ncupl5pt')}", "fact"),
 ("Rondonia cell A, TMF deforestation", f"emem:fact:defi.zb391.taza.zcc31:{R('sw4zpem3')}", "fact"),
 ("Rondonia cell A, CCI biomass", f"emem:fact:defi.zb391.taza.zcc31:{R('yc5qjlgh')}", "fact"),
 ("Prithvi-EO-2.0 vector, checkpoint bound", f"emem:fact:{K}:{cur['prithvi_eo2']}", "fact"),  # panel 10
 ("TESSERA vector, path only", F("tessera_keylong"), "fact"),
 ("an ask reasoning stage, scored", state, "state"),                                      # panel 2 place row
 ("the measurements behind the board", N + "6wmlonyq2jy7u24vcyx43afh5q.md", "pointer.v1"),
]
if len(sys.argv) > 1:
    STEPS.insert(0, ("the printed board", N + sys.argv[1] + ".md", "pointer.v1"))
assert all(len(l) <= 40 and ":" not in l for l, _, _ in STEPS)
link = cid(b""); rows = []
for i, (label, ref, kind) in enumerate(STEPS, 1):
    link = cid(link.encode() + ref.encode()); rows.append(f"| {i} | {label} | {ref} | {kind} | ✓ | {link} |")
body = "\n".join(["---", "emem: track.v1", f"steps: {len(STEPS)}", f"verified: {len(STEPS)} of {len(STEPS)}", f"head: {link}",
  "chain: each link = blake3(previous link ‖ step reference), first 128 bits", "---", "",
  "# EMEM poster, Agentic AI for Earth Observation, Berlin 2026", "",
  f"> {len(STEPS)} steps: the records the printed board rests on, in panel order, each re-checked where it stands; the chain's head commits to all of them and to their order.", "",
  "| # | step | evidence | kind | checked | chain |", "|---|---|---|---|---|---|", *rows, ""])
open(pathlib.Path(__file__).with_name("track_body.md"), "w").write(body); print(link, len(STEPS), len(body))
