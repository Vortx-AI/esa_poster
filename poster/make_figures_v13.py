"""Regenerate the figures used by the current v13 poster face.

This keeps build_v13.py --figures useful: figures are generated from source code,
not hand-edited SVG/PNG assets. Each script writes SVG, PNG and labels into
poster/fig/v13 via figs_v13/style.py.
"""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FIGS = HERE / "figs_v13"

ACTIVE = [
    "f1_scene.py",
    "f18_workflow.py",
    "f2_spine.py",
    "f3_eight_answers.py",
    "f5_evidence_object.py",
    "f6_mutation_matrix.py",
    "f7_wrong_pixel.py",
    "f8_ladder.py",
    "f9_timeline.py",
    "f11_ecosystem.py",
    "f14_token_family.py",
    "f15b_sat042_strip.py",
]

for name in ACTIVE:
    path = FIGS / name
    if not path.exists():
        raise SystemExit(f"missing active figure source: {path}")
    print(f"[figure] {name}", flush=True)
    subprocess.run([sys.executable, str(path)], cwd=HERE.parent, check=True)
