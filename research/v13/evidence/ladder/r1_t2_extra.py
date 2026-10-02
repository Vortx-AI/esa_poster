"""Extra T2 probes against the unmodified R1 verifier (research/repro/v11/mutation_suite.py), run from a scratch copy.
Nothing is signed with emem's key: TEST_SIGNER is the suite's public-string test key."""
import sys, json
sys.argv = ["x"]
src = open("mutation_suite.py").read().replace('if __name__ == "__main__":\n    main()', "")
ns = {"__file__": __file__.replace("r1_t2_extra.py", "mutation_suite.py")}
ns["__file__"] = "mutation_suite.py"
exec(compile(src, "mutation_suite.py", "exec"), ns)
g = ns
def t2(mutate):
    h = g["genuine"]()
    g["forge"](h, mutate, signer=g["TEST_SIGNER"])
    h["pinned_key"] = bytes(g["TEST_SIGNER"].verify_key)
    return h
def offset_zero(d):          # signer applies offset 0 to a baseline-05.13 scene and records it consistently
    d["derivation"]["args"][g["OFF_IDX"]] = 0.0
    b8, b4 = d["derivation"]["args"][g["DN_IDX"]]
    d["value"] = g["ndvi"](b8, b4, 0.0)
def scene_relabel(d):        # signer names another scene id but keeps the DNs it read
    d["derivation"]["args"][g["SCENE_IDX"]] = "S2B_MSIL2A_20260925T053639_R105_T43SFS_20260925T074931"
def unit_mislabel(d):        # signer adds a wrong unit (record has no unit field today)
    d["unit"] = "percent"
out = {}
for name, m in [("T2_offset_zero", offset_zero), ("T2_scene_relabel_same_day", scene_relabel), ("T2_unit_mislabel", unit_mislabel)]:
    h = t2(m)
    res = {}
    for lv in "DEFGHI":
        try:
            res[lv] = bool(g["CHECKS"][lv](h))
        except Exception as e:
            res[lv] = f"error {e}"
    refused, failed, v = g["decide"]("I", h)
    out[name] = {"checks_pass": res, "refused_at_level_I": refused, "failed_check": failed, "value_acted_on": v,
                 "decision_flipped": (not refused) and ((v <= g["RULE"]) != (g["GENUINE"] <= g["RULE"]))}
print(json.dumps(out, indent=1))
