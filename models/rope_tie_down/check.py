"""Read-only native parameter walk and printable-mesh checks; stdlib only.

Run under the finite CAD lock wrapper documented in README.md.
This checks the saved design, never generates or edits it.
"""

import json
import math
import struct
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "led_profiles"))
from export_stl import validate_stl

RANGES = {
    "hole_spacing": (35, 50, 40),
    "bar_length": (110, 130, 120),
    "bar_width": (26, 30, 26),
    "bar_t": (8, 10, 8),
    "mount_height": (28, 34, 30),
    "hole_d": (5.2, 5.8, 5.5),
}


def expected_volume(v):
    """Independent ellipse and frustum estimate; blend corrections are <0.1%."""
    h = v["mount_height"] - v["bar_t"]
    slope = (v["foot_d"] - v["post_d"]) / (2 * (h + 1))
    r, R = v["post_d"] / 2 + slope, v["foot_d"] / 2
    bar = math.pi * v["bar_length"] * v["bar_width"] * v["bar_t"] / 4
    posts = 2 * math.pi * h * (r*r + r*R + R*R) / 3
    r, R = v["hole_d"] / 2, v["head_d"] / 2
    depth = R - r
    bores = 2 * math.pi * (r*r * v["mount_height"]
        + depth * (R*R + R*r - 2*r*r) / 3)
    return bar + posts - bores


def check_design(design, allow_rebinding):
    assert all(s["dof"] == 0 and s["status"] == "solved" for s in design["sketches"])
    assert all(not p["error"] for p in design["params"])
    for f in design["timeline"]:
        assert not f["error"], f
        warning = f["warning"]
        if warning:
            assert allow_rebinding and all(
                "was found by geometry, not exact history; check it" in part
                for part in warning.split("; edge ")
            ), f
    assert len(design["bodies"]) == 1
    body = design["bodies"][0]
    assert body["kernel"]["shells"] == 1
    v = {p["name"]: p["value"] for p in design["params"]}
    assert v["hole_spacing"] - v["foot_d"] >= 11
    assert 0 < v["post_taper"] < math.pi / 4
    estimate = expected_volume(v)
    assert abs(body["volume_mm3"] - estimate) < estimate * 0.001
    for side, sign in (("min", -1), ("max", 1)):
        expected = (sign * v["bar_length"] / 2, sign * v["bar_width"] / 2,
                    0 if side == "min" else v["mount_height"])
        assert all(abs(a - b) < 0.002 for a, b in zip(body["bbox"][side], expected))
    assert all(abs(c) < 0.002 for c in body["center_of_mass"][:2])
    return body


def main():
    commands = [{"command": "document.inspect", "params": {"measure": True}}]
    for name, values in RANGES.items():
        for value in values:
            commands += [
                {"command": "parameters.change", "params": {"name": name, "expression": f"{value} mm"}},
                {"command": "document.inspect", "params": {"measure": True}},
            ]
    scratch = ROOT / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="rope-check-", dir=scratch) as directory:
        script = Path(directory) / "walk.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(
            ["solidcraft-cli", "run", str(script), "--in", str(HERE / "rope_tie_down_40.solidcraft"), "--results"],
            capture_output=True, text=True, check=True,
        )
    states = json.loads(result.stdout)[::2]
    original = check_design(states[0], False)
    for design in states[1:]:
        check_design(design, True)
    restored = check_design(states[-1], False)
    assert abs(restored["volume_mm3"] - original["volume_mm3"]) < 0.01

    path = ROOT / "exports/rope_tie_down/rope_tie_down_40.stl"
    mesh = validate_stl(path)
    assert abs(mesh["mesh_volume_mm3"] - original["volume_mm3"]) < original["volume_mm3"] * 0.001
    data = path.read_bytes()
    vertices = set()
    for i in range(struct.unpack_from("<I", data, 80)[0]):
        values = struct.unpack_from("<12f", data, 84 + 50 * i)[3:]
        vertices.update(tuple(values[j:j + 3]) for j in (0, 3, 6))
    # Actual exported circular interfaces, not just stored parameter expressions.
    for x in (-20, 20):
        for z, radii in ((0, (5.25,)), (2.5, (2.75,)), (30, (2.75, 12))):
            ring = [math.hypot(a - x, b) for a, b, c in vertices
                    if abs(c - z) < 0.0001 and math.hypot(a - x, b) < max(radii) + 0.1]
            assert all(any(abs(r - target) < 0.0001 for target in radii) for r in ring), (x, z, ring)
            assert all(sum(abs(r - target) < 0.0001 for r in ring) >= 12 for target in radii)
    print("PASS: native reload, six parameter endpoint walks and restored defaults; one healthy solid")
    print("PASS: manifold STL; 40 mm centres, 5.5 mm bores, 10.5 mm mouth 90-degree countersinks")


if __name__ == "__main__":
    main()
