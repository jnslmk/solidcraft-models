"""Read-only checks of the saved design and printable half; never a generator.

Run under the finite, workstation-wide CAD lock shown in README.md.
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
    "pot_d": (170, 180, 174),
    "pot_clearance": (0.3, 0.8, 0.5),
    "stem_d": (8, 12, 10),
    "support_h": (100, 140, 120),
    "fit": (0.25, 0.4, 0.3),
}


def check_state(design, pot, stem, channel, roof):
    assert all(s["dof"] == 0 and s["status"] == "solved" for s in design["sketches"])
    assert all(not p["error"] for p in design["params"])
    for feature in design["timeline"]:
        assert not feature["error"], feature
        warning = feature["warning"]
        assert (not warning or warning.startswith("Boolean retry: tool displacement")
                or (feature["name"] == "SoftReceiverEnds"
                    and "was split; using the piece nearest the picked point" in warning)), feature
    values = {p["name"]: p["value"] for p in design["params"]}
    bodies = design["bodies"]
    assert len(bodies) == 2
    for body in bodies:
        assert body["kernel"]["shells"] == 1
        assert abs(body["bbox"]["min"][2]) < 0.002
        assert abs(body["bbox"]["max"][2] - values["support_h"] - 6) < 0.002
        assert abs(max(abs(body["bbox"][side][0]) for side in ("min", "max"))
                   - values["R"] - 8.5) < 0.002
    assert abs(bodies[0]["volume_mm3"] - bodies[1]["volume_mm3"]) < bodies[0]["volume_mm3"] * 0.0001
    assert abs(pot["diameter"] - values["pot_d"] - 2 * values["pot_clearance"]) < 0.002
    assert abs(stem["diameter"] - values["stem_d"]) < 0.002
    assert abs(channel["distance_mm"] - 1.6 - 2 * values["fit"]) < 0.002
    assert abs(roof["distance_mm"] - values["fit"]) < 0.002
    # Positive running clearance and barb capture, across the documented fit range.
    assert 0 < values["fit"] < 0.8
    assert 1.6 - (0.8 + values["fit"]) >= 0.4 - 1e-9
    return bodies[0]["volume_mm3"]


def inspection(values):
    r = values["pot_d"] / 2 + values["pot_clearance"]
    cx = r + 4.5 + 5
    fit = values["fit"]
    def face(point, body="SupportHalf"):
        return {"type": "face", "body": body, "point": point}
    def measure(*items):
        return {"command": "inspect.measure", "params": {"items": list(items)}}
    return [
        {"command": "document.inspect", "params": {"measure": True}},
        measure(face([0, r, 4])),
        measure(face([0, values["stem_d"] / 2, values["support_h"] + 3])),
        measure(face([-cx + 0.8 + fit, 10, 3]), face([-cx - 0.8 - fit, 10, 3])),
        measure(face([cx, -10, 6]), face([cx, -10, 6 + fit], "SupportHalf (2)")),
    ]


def main():
    current = {name: values[-1] for name, values in RANGES.items()}
    commands = inspection(current)
    for name, values in RANGES.items():
        for value in values:
            current[name] = value
            commands.append({"command": "parameters.change", "params": {
                "name": name, "expression": f"{value} mm"}})
            commands.extend(inspection(current))
    scratch = ROOT / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="plant-check-", dir=scratch) as directory:
        script = Path(directory) / "walk.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run([
            "solidcraft-cli", "run", str(script), "--in",
            str(HERE / "plant_support_174.solidcraft"), "--results",
        ], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr or result.stdout
    results = json.loads(result.stdout)
    initial = check_state(*results[:5])
    assert abs(initial - 19112.693) < 2
    for index in range(6, len(results), 6):
        check_state(*results[index:index + 5])
    assert abs(results[-5]["bodies"][0]["volume_mm3"] - initial) < 0.01

    path = ROOT / "exports/plant_support/plant_support_half.stl"
    mesh = validate_stl(path)
    assert abs(mesh["mesh_volume_mm3"] - initial) < initial * 0.001
    data = path.read_bytes()
    vertices = set()
    for index in range(struct.unpack_from("<I", data, 80)[0]):
        coordinates = struct.unpack_from("<12f", data, 84 + 50 * index)[3:]
        vertices.update(tuple(coordinates[j:j + 3]) for j in (0, 3, 6))
    # The exported bores, rather than just parameter values in the saved document.
    for z, radius in ((0, 87.5), (126, 5)):
        points = [(x, y) for x, y, h in vertices
                  if abs(h - z) < 0.002 and abs(math.hypot(x, y) - radius) < 0.002]
        assert len(points) >= 12, (z, radius)
    for expected in ((96.2, -20, 0), (97.8, -20, 0), (98.6, -14, 0)):
        assert any(math.dist(expected, point) < 0.002 for point in vertices), expected
    print("PASS: saved native reload, measured bores, 15 parameter states and restored defaults")
    print("PASS: two single-shell bodies; manifold print mesh with pot/stem bores and snap tongue")


if __name__ == "__main__":
    main()
