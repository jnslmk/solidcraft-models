"""Read-only checks of the saved native crate and cupboard; stdlib only.

Run under the workstation CAD lock and a finite process-group timeout; see README.
No model is generated or rewritten. Expectations use disjoint rectangular volumes,
not measurements frozen from SolidCraft. These checks do not validate real-box fit.
"""

import json
import math
import subprocess
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "led_profiles"))
from export_stl import validate_stl

HEIGHTS = (75, 120, 170, 220, 270, 320)
ROWS = (220, 170, 170, 170, 170, 120, 120, 75, 75, 75)


def expected(h, foot=12, wall=5):
    outer = (270 + 2 * wall) * (370 + 2 * wall)
    # Signed volumes and their independent Z centroids, including cavity/recesses.
    pieces = (
        (outer * (h - foot), (h + foot) / 2),
        (-270 * 370 * (h - foot - 5), (h + foot + 5) / 2),
        ((300 * 400 - outer) * 6, h - 5),
        ((294 * 394 - outer) * 2, h - 1),
        ((260 * 360 - 250 * 350) * foot, foot / 2),
        (12 * 3 * 4 * (h - foot - 8), (h + foot - 8) / 2),
        (-2 * 90 * 2 * 20, h - 28),
    )
    volume = sum(v for v, _ in pieces)
    return volume, sum(v * z for v, z in pieces) / volume


def close(actual, target, tolerance=0.00001):
    assert math.isclose(actual, target, rel_tol=0, abs_tol=tolerance), (actual, target)


def health(design):
    for f in design["timeline"]:
        assert not f["error"] and not f["warning"], f
    for p in design["params"]:
        assert not p["error"], p
    for sketch in design["sketches"]:
        assert sketch["dof"] == 0 and sketch["status"] == "solved", sketch
    for joint in design.get("joints", []):
        assert not joint["errors"] and not joint["conflicts"], joint


def crate(body, height, foot=12, wall=5, center=(0, 0, 0)):
    volume, z = expected(height, foot, wall)
    close(body["volume_mm3"], volume, 0.01)
    assert body["kernel"]["shells"] == 1, body["name"]
    for actual, target in zip(body["center_of_mass"], (center[0], center[1], center[2] + z)):
        close(actual, target)
    for side, offset in (("min", (-150, -200, 0)), ("max", (150, 200, height))):
        for actual, c, d in zip(body["bbox"][side], center, offset):
            close(actual, c + d)


def walk(path, changes):
    with zipfile.ZipFile(path) as archive:
        native = json.loads(archive.read("document.json"))
    # A redistribution regression: imported BREP/mesh must not sneak back in.
    assert {f["type"] for f in native["features"]} <= {"box", "move", "body_transfer"}
    commands = [{"command": "document.inspect", "params": {"measure": True}}]
    for name, value in changes:
        commands.extend([
            {"command": "parameters.change", "params": {"name": name, "expression": f"{value} mm"}},
            {"command": "document.inspect", "params": {"measure": True}},
        ])
    scratch = ROOT / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="crate-check-", dir=scratch) as directory:
        script = Path(directory) / "walk.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(
            ["solidcraft-cli", "run", str(script), "--in", str(path), "--results"],
            capture_output=True, text=True, check=True,
        )
    results = json.loads(result.stdout)
    for design in results[::2]:
        health(design)
        yield design


def main():
    changes = [("crate_h", h) for h in HEIGHTS] + [
        ("crate_h", 220), ("foot_h", 8), ("foot_h", 14), ("foot_h", 12),
        ("wall", 3), ("wall", 5),
    ]
    for design in walk(HERE / "eurobox.solidcraft", changes):
        params = {p["name"]: p["value"] for p in design["params"]}
        assert len(design["bodies"]) == 1
        crate(design["bodies"][0], params["crate_h"], params["foot_h"], params["wall"])
    print("PASS native crate: all six heights, foot/wall range endpoints, restored defaults")
    for h in HEIGHTS:
        mesh = validate_stl(ROOT / "exports/auer_euroboxes" / f"eurobox_{h}.stl")
        close(mesh["mesh_volume_mm3"], expected(h)[0], 0.1)
    print("PASS six STL exports: closed connected manifold shells and analytic volumes")
    changes = [(name, value) for name, values in (
        ("bay_w", (316, 320, 316)), ("frame_d", (410, 430, 420)),
        ("frame_h", (1990, 2050, 2000)), ("crate_wall", (3, 5)),
    ) for value in values]
    path = HERE.parent / "eurobox_cupboard/cupboard_slide.solidcraft"
    for design in walk(path, changes):
        params = {p["name"]: p["value"] for p in design["params"]}
        bodies = {b["name"]: b for b in design["bodies"]}
        assert len(bodies) == 102
        z = 88
        for row, h in enumerate(ROWS, 1):
            for column in (1, 2, 3):
                x = 44 + params["bay_w"] / 2 + (column - 1) * (params["bay_w"] + 44)
                crate(bodies[f"Eurobox_H{h}_C{column}_R{row}"], h,
                      wall=params["crate_wall"], center=(x, params["frame_d"] / 2, z))
                for side in ("left", "right"):
                    rib = bodies[f"Rail_{column}_{row}_{side}"]
                    close(rib["bbox"]["max"][2], z + 12)
                    close(rib["bbox"]["min"][2], z - 32)
                    close(rib["volume_mm3"], 24 * 44 * params["frame_d"], 0.01)
            # At minimum bay width: 4 mm foot clearance, 6 mm bearing overlap per side.
            close(params[f"crate_z{row}"], z)
            assert (params["bay_w"] - 48 - 260) / 2 >= 4
            assert (270 + 2 * params["crate_wall"] - (params["bay_w"] - 48)) / 2 >= 2
            z += h + 20 + 44 - 12
        assert params["frame_h"] - 44 - (z - 52) >= 25
    print("PASS cupboard: 30 native crates, 60 ribs, frame/wall endpoints, nominal clearances")


if __name__ == "__main__":
    main()
