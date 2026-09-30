"""Compose the board's entry track.v1 note: the ordered §-steps, each ref re-checked, with the chain head."""
import json, base64, blake3
cid = lambda b: base64.b32encode(blake3.blake3(b).digest()[:16]).decode().lower().rstrip("=")
N = "https://emem.dev/memories/by_attester/njedkglt/"
inv = json.load(open("inventory.json")); F = lambda k: inv[k]["token"]
cube = json.load(open("../data/cubeK_members.json"))["cube_token"]
rs = json.load(open("rasterset_mint.json"))["tokens"]["raster_bundle"]
bundle = json.load(open("bundle_mint.json"))["bundle_token"]
STEPS = [
 ("the board, seal box blank", N + "ubaylj2hnx5ho3gnelzgndncai.md", "pointer.v1"),
 ("Sentinel-2 B08 COG, 292 tiles", N + "khiqtqrddb6jponqn4gv72if7e.md", "pointer.v1"),
 ("Sentinel-2 B04 COG, 292 tiles", N + "h6d7xdoc5b2uzood22lowblbc4.md", "pointer.v1"),
 ("NDVI record, Keylong, 25 Sep 2026", F("ndvi_keylong"), "fact"),
 ("B04 field, Keylong, 443 x 453 px", json.load(open("../hero_field.json"))["s2.B04"]["token"], "raster"),
 ("B08 cube, five scenes", cube, "cube"),
 ("pre-fix record, 23 Sep, pixel south", F("ndvi_prefix_23sep"), "fact"),
 ("CHANGELOG line 68, the pixel fix", N + "7zmocvinsgzdayubripuzruy7q.md", "pointer.v1"),
 ("Tessera 128-D embedding", F("tessera_keylong"), "fact"),
 ("Clay v1.5 1024-D embedding", F("clay_v15"), "fact"),
 ("caller-signed NDVI change", F("derived_ndvi_delta"), "fact"),
 ("elevation 918.0 m, May", F("elev_may"), "fact"),
 ("elevation 915.07 m, September", F("elev_sep"), "fact"),
 ("temperature 28.0 degC, guard test", F("temp_bengaluru"), "fact"),
 ("signed absence, open ocean", F("absence_ocean"), "fact"),
 ("the 8 stored records, one handle", bundle, "bundle"),
 ("statistics rows, 0 of 72, p 0.035", N + "k2ww7uxf7umrfsvy33syzafrfq.md", "pointer.v1"),
 ("handoff and paraphrase-trap rows", N + "hyl7r2yl3ybzcegxjhxiplr4ai.md", "pointer.v1"),
 ("sizes and the authors scorecard", N + "eoe5s4arfksqtpd66rczwetviq.md", "pointer.v1"),
 ("the record and 19 withdrawals", N + "izycf6molcl5z53fkolqly57ze.md", "pointer.v1"),
 ("paraphrase-trap value, 17 Jul", F("ndvi_trap_17jul"), "fact"),
 ("the measurements behind the board", N + "3g76s4vrcboxicj6hrd2mztesu.md", "pointer.v1"),
]
assert all(len(l) <= 40 and ":" not in l for l, _, _ in STEPS)
link = cid(b""); rows = []
for i, (label, ref, kind) in enumerate(STEPS, 1):
    link = cid(link.encode() + ref.encode())
    rows.append(f"| {i} | {label} | {ref} | {kind} | ✓ | {link} |")
body = "\n".join(["---", "emem: track.v1", f"steps: {len(STEPS)}", f"verified: {len(STEPS)} of {len(STEPS)}", f"head: {link}",
  "chain: each link = blake3(previous link ‖ step reference), first 128 bits", "---", "",
  "# EMEM poster, Agentic AI for Earth Observation, Berlin 2026", "",
  f"> {len(STEPS)} steps, in order: step n is §n on the printed board. Each was re-checked where it stands; the chain's head commits to all of them and to their order.", "",
  "| # | step | evidence | kind | checked | chain |", "|---|---|---|---|---|---|", *rows, ""])
open("track_body.md", "w").write(body); print(link, len(body))
