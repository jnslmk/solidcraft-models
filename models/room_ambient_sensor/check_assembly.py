"""Read-only native assembly walk; run under README's finite CAD-lock supervisor.

Standard library only. Edits exist only in the CLI's temporary session: no save,
export, generator, or full interference sweep. Photo-based hardware remains an
estimate; the separate conservative clearance proof is not a physical-fit claim.
"""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from check import CASE_SKETCHES, RANGES as CASE_RANGES, check_catches, expected_volumes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "room_ambient_sensor_assembly.solidcraft"
TOL = 0.002
COMPONENTS = {
    "Enclosure base", "Enclosure lid", "Wemos D1 mini", "Connected perfboard",
    "DHT22 upright module", "SGP41 attached breakout", "MH-Z19B wired module",
    "Interconnection leads", "USB power cable",
}
RANGES = CASE_RANGES | {"dht_carrier_height": (37, 40, 40)}
IDENTITY = [[int(i == j) for j in range(4)] for i in range(4)]
LEADS = (
    ("Red", -13.97, -18.15, "low", -1.27, 6.5, 0),
    ("Brown", -13.97, -18.15, "high", 1.27, 6.5, 0),
    ("Orange", 6.35, 11.35, "low", 0, 5, 1),
    ("Yellow", 6.35, 11.35, "high", 2.54, 5, 1),
)
WIRE_SKETCHES = [f"{color} {route}" for color, *_ in LEADS
                 for route in ("lateral lead route", "connector bend route")]


def near(actual, expected, label):
    assert abs(actual - expected) < TOL, (label, actual, expected)


def box(body, minimum, maximum):
    for side, expected in (("min", minimum), ("max", maximum)):
        for axis, value in enumerate(expected):
            near(body["bbox"][side][axis], value, (body["name"], side, axis))


def check_state(design, joints, tree, properties, expected):
    assert Path(design["path"]).resolve() == SOURCE.resolve()
    assert all(not p["error"] for p in design["params"])
    issues = [(f["name"], f["error"], f["warning"]) for f in design["timeline"]
              if f["error"] or f["warning"]]
    assert not issues, (expected, issues)
    assert design["sketches"]
    assert all(s["dof"] == 0 and s["status"] == "solved" for s in design["sketches"])
    params = {p["name"]: p["value"] for p in design["params"]}
    for name, value in expected.items():
        near(params[name], value, name)
    bodies = {b["name"]: b for b in design["bodies"]}
    assert len(bodies) == len(design["bodies"]) == 76
    assert all(not b.get("error") and b["kernel"]["shells"] == 1 for b in bodies.values())

    components = {c["name"]: c for c in tree["components"] if c["id"] != 0}
    assert len(tree["components"]) == 10 and set(components) == COMPONENTS
    assert tree["pending_moves"] == []
    root = next(c for c in tree["components"] if c["id"] == 0)
    assert root["bodies"] == []
    assert components["Enclosure base"]["bodies"] == ["Base"]
    assert components["Enclosure lid"]["bodies"] == ["Lid"]
    reference_names = [name for c in components.values()
                       if c["name"] not in {"Enclosure base", "Enclosure lid"}
                       for name in c["bodies"]]
    assert len(reference_names) == len(set(reference_names)) == 74
    assert set(reference_names) == set(bodies) - {"Base", "Lid"}
    occurrences = []
    for component in components.values():
        assert component["parent"] == 0
        assert len(component["occurrences"]) == 1
        occurrence = component["occurrences"][0]
        assert occurrence["parent"] == 0
        assert occurrence["grounded"] == (component["name"] == "Enclosure base")
        for actual_row, expected_row in zip(occurrence["transform"], IDENTITY):
            assert len(actual_row) == 4
            for actual, value in zip(actual_row, expected_row):
                near(actual, value, (component["name"], "placement"))
        assert len(occurrence["transform"]) == 4
        occurrences.append(occurrence["id"])
    assert len(set(occurrences)) == 9
    assert joints["errors"] == joints["conflicts"] == joints["floating"] == []
    assert len(joints["joints"]) == 8
    assert all(j["type"] == "rigid" and not j["suppressed"] for j in joints["joints"])
    assert {d["occurrence"] for d in joints["dof"]} == {0, *occurrences}
    assert all(d["dof"] == 0 for d in joints["dof"])
    assert components["Enclosure base"]["occurrences"][0]["id"] in joints["fixed"]
    assert all(j["a"] in occurrences and j["b"] in occurrences for j in joints["joints"])

    # Every occurrence transform above is identity, so authored bounds are world
    # bounds at every endpoint. Independently compare the full world-property
    # report at the initial/restored defaults, without integrating all curved
    # wire mass properties twice at every intermediate state.
    world = bodies
    if properties is not None:
        assert properties["coordinate_frame"] == "world"
        assert properties["body_count"] == 76 and properties["placement_count"] == 10
        assert properties["total"]["open_bodies_skipped"] == 0
        world = {b["name"]: b for b in properties["bodies"]}
        assert set(world) == set(bodies)
        for name, body in bodies.items():
            assert world[name]["closed"]
            box(world[name], body["bbox"]["min"], body["bbox"]["max"])
    for name, volume in zip(("Base", "Lid"), expected_volumes(params)):
        assert abs(world[name]["volume_mm3"] - volume) < volume * 0.0002
    L, W, H = (params[n] for n in ("case_length", "case_width", "case_height"))
    box(world["Base"], [-L/2, -W/2, 0], [L/2, W/2, H])
    box(world["Lid"], [-L/2, -W/2, H-params["lid_snap_length"]], [L/2, W/2, H+2.4])
    near(params["rear_latch_x"], L/2 - 22.5, "rear latch follows vent land")
    assert params["wall"] + 8 + params["perfboard_width"] + params["pcb_top_gap"] + 2.2 < H

    x, z = params["stack_x"], params["stack_z"]
    width, length, elevation = (params[n] for n in
                                ("perfboard_width", "perfboard_length", "perfboard_z"))
    near(z, params["wall"] + 8 + width / 2, "support-derived stack height")
    box(world["Wemos blue PCB"],
        [x - 1.6, -params["wemos_length"] / 2, z - params["wemos_width"] / 2],
        [x, params["wemos_length"] / 2, z + params["wemos_width"] / 2])
    box(world["Perfboard PCB"],
        [x - elevation - 1.6, -4.5 - length / 2, z - width / 2],
        [x - elevation, -4.5 + length / 2, z + width / 2])
    near(world["Perfboard PCB"]["bbox"]["min"][2], 10.4, "PCB support resting height")
    near(world["MH-Z19B green PCB"]["bbox"]["min"][2], 5.4, "MH PCB resting height")
    box(world["DHT upright carrier PCB"],
        [x - params["dht_start"] - params["dht_carrier_height"], 1.27, z - 9.27],
        [x - params["dht_start"], 2.87, z + 6.73])
    cable_names = set(components["USB power cable"]["bodies"])
    for name in reference_names:
        bounds = world[name]["bbox"]
        assert H - bounds["max"][2] >= 3.6 - TOL, name
        if name not in cable_names:
            assert bounds["min"][2] > params["wall"], name
            for axis, span in enumerate((L, W)):
                assert bounds["min"][axis] > -span/2 + params["wall"], name
                assert bounds["max"][axis] < span/2 - params["wall"], name
    # Plug and lead both pass through the rectangular part of the USB opening.
    for name in ("USB plug overmould", "USB power lead"):
        bounds = world[name]["bbox"]
        assert 5 < bounds["min"][0] < bounds["max"][0] < 21
        assert params["wall"]+3 < bounds["min"][2] < bounds["max"][2] < params["wall"]+27
    assert world["USB power lead"]["bbox"]["min"][1] < -W/2
    assert world["USB plug overmould"]["bbox"]["max"][1] > -W/2 + params["wall"]
    return world, [(j["id"], j["name"], j["a"], j["b"], j["type"])
                   for j in joints["joints"]]


def check_wires(p, sketches, world):
    """Keep actual spline endpoints attached to both their housings and bends."""
    by_name = {s["name"]: s for s in sketches}
    for color, source_y, target_y, level, pin_x, lane, pair in LEADS:
        route = by_name[f"{color} lateral lead route"]
        curve = next(c for c in route["curves"] if c["type"] == "spline")
        points = {q["id"]: q["world"] for q in route["points"]}
        path = [points[point] for point in curve["points"]]
        assert curve["control"] and curve["degree"] == 3
        bend = {q["id"]: q["world"]
                for q in by_name[f"{color} connector bend route"]["points"]}
        for actual, expected, label in (
                (path[0], [p["jumper_exit_x"], source_y, p[f"jumper_exit_z_{level}"]], "source"),
                (path[-1], bend["p2"], "spline/bend continuity"),
                (bend["p3"], [p["co2_x"]+pin_x, target_y, p["mh_jumper_top"]], "MH terminal")):
            for axis in range(3):
                near(actual[axis], expected[axis], (color, label, axis))
        for point in path[-5:-2]:
            near(point[1], p["case_width"]/2-lane, (color, "rear cable lane"))
        # A control spline lies inside its control hull; include insulation radius.
        for point in path:
            assert -p["case_length"]/2+p["wall"]+0.6 < point[0] < p["case_length"]/2-p["wall"]-0.6
            assert -p["case_width"]/2+p["wall"]+0.6 < point[1] <= p["case_width"]/2-lane+TOL
        assert lane-0.6 >= p["wall"]+p["lid_clearance"]+p["lid_snap_t"]-TOL
        if pair == 0:
            # Keep the front pair's detour around the intact DHT carrier/sensor.
            dht = [world[name]["bbox"] for name in
                   ("DHT upright carrier PCB", "DHT vented sensor body")]
            left = min(bounds["min"][0] for bounds in dht)
            front = min(bounds["min"][1] for bounds in dht)
            assert world[f"{color} jumper insulation"]["bbox"]["min"][0] < left-0.6
            assert any(point[0] < -26 and -11+0.6 < point[1] < front-0.6
                       for point in path)
        source = world[f"Perfboard female jumper pair {pair}"]["bbox"]
        near(path[0][0], source["min"][0], (color, "housing exit face"))
        target = world[f"MH female jumper pair {pair}"]["bbox"]
        near(bend["p3"][2], target["max"][2], (color, "MH housing top"))
        for point, housing in ((path[0], source), (bend["p3"], target)):
            for axis in range(3):
                assert housing["min"][axis]-TOL <= point[axis] <= housing["max"][axis]+TOL


def main():
    commands = []
    inspections = []
    expected = {name: values[2] for name, values in RANGES.items()}
    expectations = []

    def inspect(full=False):
        inspections.append((len(commands), full))
        commands.extend([
            {"command": "document.inspect", "params": {"measure": True}},
            {"command": "joint.list", "params": {}},
            {"command": "component.list", "params": {}},
        ])
        expectations.append(expected.copy())
        commands.extend({"command": "sketch.inspect", "params": {"sketch": name}}
                        for name in CASE_SKETCHES + WIRE_SKETCHES)
        if full:
            commands.append({"command": "component.properties", "params": {"component": "root"}})

    inspect(full=True)
    for name, values in RANGES.items():
        for value in values:
            commands.append({"command": "parameters.change", "params": {
                "name": name, "expression": f"{value} mm"}})
            expected[name] = value
            inspect(full=name == next(reversed(RANGES)) and value == values[-1])
    scratch = ROOT / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="room-sensor-assembly-check-", dir=scratch) as directory:
        script = Path(directory) / "walk.json"
        output = Path(directory) / "results.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run([
            "solidcraft-cli", "run", str(script), "--in", str(SOURCE),
            "--results", "--json-out", str(output),
        ], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        results = json.loads(output.read_text())
    assert len(results) == len(commands)
    original = None
    for (index, full), expectation in zip(inspections, expectations):
        sketch_end = index + 3 + len(CASE_SKETCHES) + len(WIRE_SKETCHES)
        properties = results[sketch_end] if full else None
        world, topology = check_state(*results[index:index+3], properties, expectation)
        params = {p["name"]: p["value"] for p in results[index]["params"]}
        check_catches(params, results[index+3:index+3+len(CASE_SKETCHES)])
        check_wires(params, results[index+3+len(CASE_SKETCHES):sketch_end], world)
        if original is None:
            original, original_topology = world, topology
        assert topology == original_topology
    for name, body in original.items():
        box(world[name], body["bbox"]["min"], body["bbox"]["max"])
        assert abs(world[name]["volume_mm3"] - body["volume_mm3"]) < 0.01, name
    print("PASS: native assembly reload; 2 printable + 74 reference bodies; 9 components; grounded base and 8 stable rigid joints")
    print(f"PASS: {len(RANGES)} parameter endpoint walks restored; actual snap/roof geometry, independent volumes, PCB headroom and connected rear-routed wires")


if __name__ == "__main__":
    main()
