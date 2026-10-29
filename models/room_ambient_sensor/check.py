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
    "case_length": (108, 116, 108), "case_width": (74, 82, 74),
    "case_height": (42, 46, 42), "lid_clearance": (0.25, 0.6, 0.35),
    "co2_width": (22, 26, 23),
    "perfboard_width": (26, 28, 26), "perfboard_length": (28.5, 30.5, 28.5),
    "perfboard_z": (12.5, 14, 13.4),
    "lid_snap_t": (1, 1.4, 1.2), "lid_snap_length": (20, 24, 22),
    "snap_engagement": (0.5, 0.7, 0.7), "pcb_clearance": (0.25, 0.4, 0.35),
    "pcb_snap_t": (1, 1.2, 1.2), "mh_snap_length": (12, 14, 12),
    "pcb_top_gap": (0.15, 0.4, 0.25),
    "outer_corner_radius": (1, 2, 1.5), "print_edge_chamfer": (0.2, 0.6, 0.4),
}


def expected_volumes(p):
    """Independent box/triangle/cylinder integration of the native features.

    No CAD-reported volumes or feature success flags enter these expectations.
    The shortened supports are 8 x 4 x 8 mm; there are 34 four-mm vents.
    The low wire passage clips the baffle's end at narrower case widths.
    The 0.2 mm join overlaps and locator/support intersections are unions.
    The corrected side vents do not intersect the 16 mm USB window or its roof.
    """
    L, W, H = (p[n] for n in ("case_length", "case_width", "case_height"))
    w, t, length = p["wall"], p["pcb_snap_t"], p["mh_snap_length"]
    clear, engagement, gap = (p[n] for n in ("pcb_clearance", "snap_engagement", "pcb_top_gap"))
    pw, pl = p["perfboard_width"], p["perfboard_length"]
    wire_passage = 2 * 5 * max(0, min(12, W/2 - 28))
    base = (L * W * H - (L - 2*w) * (W - 2*w) * (H - w)
            + 2*(W-20)*(H-w-5) - 44*(H-w-12) - wire_passage
            + 2*8*4*8 + 18*p["co2_width"]
            - 34*4*w*(H-16) - w*(16*24 + 16*8/2))
    front_depth = clear + engagement
    rear_depth = max(-4.5 + pl/2, 10.16) + clear - (-4.5 + pl/2 - engagement)
    locator_y = -4.5 - pl/2 + 0.6
    support_overlap = max(0, min(locator_y + 2, -14) - max(locator_y, -18))
    base += (-28*w*1.5 + 2*2.4*t*(8+pw+gap+2.2)
             + 1.2*(front_depth**2 + rear_depth**2)
             + 2*1.2*(2*11.6 - 8*support_overlap)
             - 4*(3.6*(length+0.6) + t*0.6)*w
             + 4*t*1.6*(7+gap+clear+engagement-w)
             + 4*front_depth**2*1.6/2 + 4*math.pi*0.6**2*3)
    lid = (L*W*w + 460.8
           + 21*p["lid_snap_t"]*p["lid_snap_length"]
           - 15*p["lid_snap_t"]*2
           + 21*(p["lid_clearance"]+engagement)**2/2)
    r, chamfer = p["outer_corner_radius"], p["print_edge_chamfer"]
    # Four outside quarter-rounds, then a 45-degree inset of their perimeter.
    # These remove material only; the lid seat and every internal fit stay put.
    perimeter = 2*(L+W) - 8*r + 2*math.pi*r
    edge_loss = perimeter*chamfer**2/2 - math.pi*chamfer**3/3
    base -= 4*(1-math.pi/4)*r*r*H + edge_loss
    lid -= 4*(1-math.pi/4)*r*r*w + edge_loss
    return base, lid


DEFAULT_PARAMS = {name: values[2] for name, values in RANGES.items()} | {"wall": 2.4}
DEFAULT = expected_volumes(DEFAULT_PARAMS)


def check_state(design):
    assert all(not p["error"] for p in design["params"])
    issues = [(f["name"], f["error"], f["warning"]) for f in design["timeline"]
              if f["error"] or f["warning"]]
    assert not issues, ({p["name"]: p["value"] for p in design["params"]}, issues)
    assert all(s["dof"] == 0 and s["status"] == "solved" for s in design["sketches"])
    bodies = {b["name"]: b for b in design["bodies"]}
    assert set(bodies) == {"Base", "Lid"}
    p = {p["name"]: p["value"] for p in design["params"]}
    assert abs(p["rear_latch_x"] - (p["case_length"]/2 - 22.5)) < 0.002
    # Worst independent endpoints, including the shorter MH floor-plane beam.
    assert 1.5*RANGES["lid_snap_t"][1]*(RANGES["lid_clearance"][1]+RANGES["snap_engagement"][1])/(RANGES["lid_snap_length"][0]-5)**2 < 0.015
    assert 1.5*RANGES["pcb_snap_t"][1]*(RANGES["pcb_clearance"][1]+RANGES["snap_engagement"][1])/RANGES["mh_snap_length"][0]**2 < 0.015
    # Rear release window stays between the last antenna and first side vent.
    assert p["rear_latch_x"] - 2 > 26
    assert p["case_length"]/2 - 19 - (p["rear_latch_x"] + 2) >= 1.5 - 0.002
    # The pitched USB roof remains 45 degrees and below the lid mating face.
    assert p["wall"] + 35 < p["case_height"]
    # Neither the PCB nor its taller insertion ramps can strike the lid plate.
    assert p["wall"] + 8 + p["perfboard_width"] + p["pcb_top_gap"] + 2.2 < p["case_height"]
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
            expected_x = p["lid_x"] + (p["rear_latch_x"]-1.5 if (sx, sy) == (1, 1)
                                      else -26 if sx == -1 else -16)
            assert abs(tip[0] - expected_x) < 0.002
    for sy in (-1, 1):
        s = by_name[f"Stack PCB insertion ramp {sy} profile"]
        tip = next(q["world"] for q in s["points"] if q["id"] == "p2")
        assert abs(tip[1] - (-4.5+sy*(p["perfboard_length"]/2-p["snap_engagement"]))) < 0.002
        assert abs(tip[2] - (p["wall"]+8+p["perfboard_width"]+p["pcb_top_gap"])) < 0.002
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = by_name[f"MH PCB flexure catch {sx} {sy} profile"]
            tip = min((q["world"] for q in s["points"] if q["id"] != "origin"),
                      key=lambda point: sx*point[0])
            assert abs(tip[0] - (p["co2_x"]+sx*(10-p["snap_engagement"]))) < 0.002
            assert abs(tip[2] - (7+p["pcb_top_gap"])) < 0.002
    roof = by_name["USB pitched roof profile"]
    roof_points = sorted(q["world"] for q in roof["points"] if q["id"] != "origin")
    for actual, expected in zip(roof_points, (
            [5, -p["case_width"]/2-1, p["wall"]+27],
            [13, -p["case_width"]/2-1, p["wall"]+35],
            [21, -p["case_width"]/2-1, p["wall"]+27])):
        assert all(abs(a-e) < 0.002 for a, e in zip(actual, expected))
    assert len(roof_points) == 3


CATCH_SKETCHES = ([f"Lid ramp and undercut {x} {y} profile" for x in (-1, 1) for y in (-1, 1)]
                  + [f"Stack PCB insertion ramp {y} profile" for y in (-1, 1)]
                  + [f"MH PCB flexure catch {x} {y} profile" for x in (-1, 1) for y in (-1, 1)])
CASE_SKETCHES = CATCH_SKETCHES + ["USB pitched roof profile"]


def main():
    commands, inspections = [], []
    def inspect():
        inspections.append(len(commands))
        commands.append({"command": "document.inspect", "params": {"measure": True}})
        commands.extend({"command": "sketch.inspect", "params": {"sketch": n}} for n in CASE_SKETCHES)
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
    initial = {p["name"]: p["value"] for p in results[0]["params"]}
    assert all(abs(initial[name]-value) < 0.002 for name, value in DEFAULT_PARAMS.items())
    for index in inspections:
        design = results[index]
        check_state(design)
        check_catches({p["name"]: p["value"] for p in design["params"]},
                      results[index+1:index+1+len(CASE_SKETCHES)])
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
            expected = (DEFAULT_PARAMS["case_length"], DEFAULT_PARAMS["case_width"],
                        DEFAULT_PARAMS["case_height"] if name == "Base"
                        else DEFAULT_PARAMS["wall"]+DEFAULT_PARAMS["lid_snap_length"])[axis]
            assert abs(max(coords)-min(coords)-expected) < 0.002
            assert abs((max(coords)+min(coords))/2 if axis < 2 else min(coords)) < 0.002
    print(f"PASS: native reload; {len(RANGES)} endpoint walks restored; healthy timeline, constrained sketches, 2 solids")
    print("PASS: independent union volumes, actual catch/USB roof geometry and centered manifold STL print poses")


if __name__ == "__main__":
    main()
