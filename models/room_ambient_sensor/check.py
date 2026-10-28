"""Read-only native parameter walk and STL validation; run under README's CAD lock.

Checks the native design; does not generate it. Standard library only.
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
    "case_length": (136, 152, 140), "case_width": (86, 98, 90),
    "case_height": (54, 64, 56), "lid_clearance": (0.25, 0.6, 0.35),
    "co2_width": (22, 26, 23),
    "perfboard_width": (26, 28, 26), "perfboard_length": (28.5, 30.5, 28.5),
    "perfboard_z": (12.5, 14, 13.4),
    "lid_snap_t": (1, 1.4, 1.2), "lid_snap_length": (20, 24, 22),
    "snap_engagement": (0.5, 0.9, 0.7), "pcb_clearance": (0.25, 0.5, 0.35),
    "pcb_snap_t": (1, 1.4, 1.2), "mh_snap_length": (17, 20, 18.4),
    "pcb_top_gap": (0.15, 0.4, 0.25),
}


def expected_volumes(p):
    """Independent box/triangle/cylinder integration, including USB/vent overlap.

    No CAD-reported volumes or feature success flags enter these expectations.
    The 0.2 mm join overlaps are subtracted as unions, not counted twice.
    """
    L, W, H = (p[n] for n in ("case_length", "case_width", "case_height"))
    w, t, length = p["wall"], p["pcb_snap_t"], p["mh_snap_length"]
    clear, engagement, gap = (p[n] for n in ("pcb_clearance", "snap_engagement", "pcb_top_gap"))
    pw, pl = p["perfboard_width"], p["perfboard_length"]
    a = max(0, 69 - L / 2)
    base = (L * W * H - (L - 2*w) * (W - 2*w) * (H - w)
            + 2*(W-20)*(H-w-5) - 44*(H-w-12) - 120
            + 1520 + 1664 + 18*p["co2_width"]
            - 441.6*(H-16) - 40*26*w - (960-9.576)
            + w*(25.4*a + max(0, a-0.1)**2/2))
    front_depth = clear + engagement
    rear_depth = max(-4.5 + pl/2, 10.16) + clear - (-4.5 + pl/2 - engagement)
    locator_y = -4.5 - pl/2 + 0.6
    support_overlap = max(0, min(locator_y + 2, -14) - max(locator_y, -18))
    base += (-28*w*1.5 + 2*2.4*t*(8+pw+gap+2.2)
             + 1.2*(front_depth**2 + rear_depth**2)
             + 2*1.2*(2*11.6 - 8*support_overlap)
             - 4*(t+3.6)*(length+0.6)*w
             + 4*(t*length*(w+0.2) + t*2*0.2)
             + 4*t*1.6*(7+gap+clear+engagement-(w+0.2))
             + 4*front_depth**2*1.6/2 + 4*math.pi*0.6**2*3)
    vents = math.floor((L-34)/6)+1
    lid = (L*W*w + 460.8 - vents*4*(W-32)*w
           + 21*p["lid_snap_t"]*p["lid_snap_length"]
           - 15*p["lid_snap_t"]*2
           + 21*(p["lid_clearance"]+engagement)**2/2)
    return base, lid


DEFAULT_PARAMS = {name: values[2] for name, values in RANGES.items()} | {"wall": 2.4}
DEFAULT = expected_volumes(DEFAULT_PARAMS)


def check_state(design):
    assert all(not p["error"] for p in design["params"])
    issues = [(f["name"], f["error"], f["warning"]) for f in design["timeline"]
              if f["error"] or f["warning"]]
    assert not issues, ({p["name"]: p["value"] for p in design["params"]}, issues)
    assert len(design["timeline"]) == 115
    assert len(design["sketches"]) == 11
    assert all(s["dof"] == 0 and s["status"] == "solved" for s in design["sketches"])
    assert not any(any(word in f["name"] for word in ("screw", "tie slot", "strap route", "Corner post"))
                   for f in design["timeline"])
    bodies = {b["name"]: b for b in design["bodies"]}
    assert set(bodies) == {"Base", "Lid"}
    p = {p["name"]: p["value"] for p in design["params"]}
    assert abs(p["rear_latch_x"] - (p["case_length"]/4 - 5.5)) < 0.002
    # Worst independent endpoints (not only the current one-at-a-time state).
    assert 1.5*1.4*(0.6+0.9)/(20-5)**2 < 0.015
    assert 1.5*1.4*(0.5+0.9)/17**2 < 0.011
    for name, expected_volume in zip(("Base", "Lid"), expected_volumes(p)):
        b = bodies[name]
        assert b["kernel"]["shells"] == 1
        assert abs(b["volume_mm3"] - expected_volume) < expected_volume*0.0002, (name, p, b["volume_mm3"], expected_volume)
        dimensions = (p["case_length"], p["case_width"],
                      p["case_height"] if name == "Base" else p["wall"]+p["lid_snap_length"])
        for axis, expected in enumerate(dimensions):
            assert abs(b["bbox"]["max"][axis] - b["bbox"]["min"][axis] - expected) < 0.002
        assert abs(b["bbox"]["min"][2]) < 0.002
    return bodies


def check_catches(p, sketches):
    """Measure actual native sketch world points, not just parameter values."""
    by_name = {s["name"]: s for s in sketches}
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = by_name[f"Lid ramp and undercut {sx} {sy} profile"]
            tip = next(q["world"] for q in s["points"] if q["id"] == "p2")
            assembled_y = -tip[1]
            assert abs(assembled_y - sy*(p["case_width"]/2-p["wall"]+p["snap_engagement"])) < 0.002
            assert abs(tip[2] - (p["wall"]+p["lid_snap_length"]-3)) < 0.002
    for sy in (-1, 1):
        s = by_name[f"Stack PCB insertion ramp {sy} profile"]
        tip = next(q["world"] for q in s["points"] if q["id"] == "p2")
        assert abs(tip[1] - (-4.5+sy*(p["perfboard_length"]/2-p["snap_engagement"]))) < 0.002
        assert abs(tip[2] - (p["wall"]+8+p["perfboard_width"]+p["pcb_top_gap"])) < 0.002
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = by_name[f"MH PCB flexure catch {sx} {sy} profile"]
            tip = next(q["world"] for q in s["points"] if q["id"] == "p5")
            assert abs(tip[0] - (p["co2_x"]+sx*(10-p["snap_engagement"]))) < 0.002
            assert abs(tip[2] - (7+p["pcb_top_gap"])) < 0.002


CATCH_SKETCHES = ([f"Lid ramp and undercut {x} {y} profile" for x in (-1, 1) for y in (-1, 1)]
                  + [f"Stack PCB insertion ramp {y} profile" for y in (-1, 1)]
                  + [f"MH PCB flexure catch {x} {y} profile" for x in (-1, 1) for y in (-1, 1)])


def main():
    commands, inspections = [], []
    def inspect():
        inspections.append(len(commands))
        commands.append({"command": "document.inspect", "params": {"measure": True}})
        commands.extend({"command": "sketch.inspect", "params": {"sketch": n}} for n in CATCH_SKETCHES)
    inspect()
    for name, values in RANGES.items():
        for value in values:
            commands.append({"command": "parameters.change", "params": {"name": name, "expression": f"{value} mm"}})
            inspect()
    scratch = ROOT / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="room-sensor-check-", dir=scratch) as directory:
        script, output = Path(directory)/"walk.json", Path(directory)/"results.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(["solidcraft-cli", "run", str(script), "--in", str(HERE/"room_ambient_sensor.solidcraft"),
                                "--results", "--json-out", str(output)], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        results = json.loads(output.read_text())
    for index in inspections:
        design = results[index]
        check_state(design)
        check_catches({p["name"]: p["value"] for p in design["params"]}, results[index+1:index+11])
    original, restored = check_state(results[0]), check_state(results[inspections[-1]])
    for name in original:
        assert abs(original[name]["volume_mm3"] - restored[name]["volume_mm3"]) < 0.01
        path = ROOT/"exports/room_ambient_sensor"/f"{name.lower()}.stl"
        mesh = validate_stl(path)
        assert abs(mesh["mesh_volume_mm3"]-original[name]["volume_mm3"]) < original[name]["volume_mm3"]*0.0002
        data = path.read_bytes()
        points = [struct.unpack_from("<12f", data, 84+50*i)[3:] for i in range(mesh["triangles"])]
        for axis in range(3):
            coords = [row[j] for row in points for j in range(axis, 9, 3)]
            expected = (140, 90, 56 if name == "Base" else 24.4)[axis]
            assert abs(max(coords)-min(coords)-expected) < 0.002
            assert abs((max(coords)+min(coords))/2 if axis < 2 else min(coords)) < 0.002
    print("PASS: native reload; 15 endpoint walks restored; 115 healthy features, 11 constrained sketches, 2 solids")
    print("PASS: independent union volumes, actual catch engagement/gaps and centered manifold STL print poses")


if __name__ == "__main__":
    main()
