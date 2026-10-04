"""verifier_hard.py: the hardened conventional receiver (B++) of prereg addendum 2, a sensitivity analysis.

B+ (verifier_conv.py) plus four consistency checks that a careful conventional receiver can run on plain JSON and that
verifier.py does not have (emem leaves them to the signature):
  scene_date  the acquisition date in the source scene id (MSIL2A_YYYYMMDD) equals the observation's date
  tile_band   the MGRS latitude band of the scene's tile (T43SFS: band S, 32 to 40 N) contains the latitude of the
              question's field
  offset      the observation's BOA offset is -1000 (Sentinel-2 L2A from processing baseline 04.00, acquired from
              25 Jan 2022 on)
  unit        an elevation observation is in metres
Each is n/a where it does not apply. Accept iff no check fails and binding passes, as in B+.
"""
import datetime as dt
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import items as IT  # noqa: E402
import verifier_conv as VC  # noqa: E402

ORDER = VC.ORDER + ["scene_date", "tile_band", "offset", "unit"]
REQUIRED = VC.REQUIRED
BANDS = "CDEFGHJKLMNPQRSTUVWX"          # MGRS latitude bands, 8 degrees each from 80 S; X spans 72 to 84 N
PB04 = dt.date(2022, 1, 25)


def _scene(ob):
    return ob.get("source_scene") or ""


def _field_lat(q):
    coords = IT.PLACES[q["cell"]][1]                    # "32.57126 N, 77.03448 E", as the question prints it
    lat, hemi = coords.split(",")[0].split()
    return float(lat) * (1 if hemi == "N" else -1)


def _band_of(lat):
    if lat >= 72:
        return "X"
    return BANDS[int((lat + 80) // 8)]


def c_scene_date(ob, q):
    m = re.search(r"MSIL2A_(\d{8})T", _scene(ob))
    if not m:
        return "n/a", "no scene id with an acquisition date"
    sd = dt.datetime.strptime(m.group(1), "%Y%m%d").date().isoformat()
    od = ob.get("date") or (IT.V.date_of(int(ob["tslot"])) if ob.get("tslot") else None)
    return ("pass", f"scene acquired {sd}, the observation's date") if sd == od else \
        ("fail", f"scene acquired {sd}, observation dated {od}")


def c_tile_band(ob, q):
    m = re.search(r"_T(\d{2})([C-X])([A-Z]{2})_", _scene(ob))
    if not m:
        return "n/a", "no MGRS tile in the scene id"
    lat = _field_lat(q)
    b = _band_of(lat)
    return ("pass", f"field latitude {lat} lies in tile band {m.group(2)}") if b == m.group(2) else \
        ("fail", f"field latitude {lat} is in band {b}, the scene's tile is in band {m.group(2)}")


def c_offset(ob, q):
    d = ob.get("derivation") or {}
    if "boa_offset" not in d:
        return "n/a", "no BOA offset in the observation"
    m = re.search(r"MSIL2A_(\d{8})T", _scene(ob))
    if not m or dt.datetime.strptime(m.group(1), "%Y%m%d").date() < PB04:
        return "n/a", "acquired before processing baseline 04.00"
    return ("pass", "BOA offset -1000, as baseline 04.00 requires") if d["boa_offset"] == -1000 else \
        ("fail", f"BOA offset {d['boa_offset']}, baseline 04.00 requires -1000")


def c_unit(ob, q):
    if not str(ob.get("band", "")).startswith("copdem"):
        return "n/a", "not an elevation"
    return ("pass", "elevation in m") if ob.get("unit") == "m" else ("fail", f"elevation in {ob.get('unit')!r}, not m")


CHECKS = dict(VC.CHECKS, scene_date=c_scene_date, tile_band=c_tile_band, offset=c_offset, unit=c_unit)


def verify(ob, q):
    res = {}
    for c in ORDER:
        try:
            res[c] = CHECKS[c](ob, q)
        except Exception as e:  # malformed input is a refusal, never a pass
            res[c] = ("fail", f"error: {type(e).__name__}")
    first = next((c for c in ORDER if res[c][0] == "fail"), None)
    if first is None:
        first = next((c for c in REQUIRED if res[c][0] != "pass"), None)
    accept = first is None
    return {"results": res, "accept": accept, "first_fail": first, "value": ob.get("value") if accept else None}
