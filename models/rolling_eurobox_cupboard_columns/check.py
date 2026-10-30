"""Read-only saved-native checks; run under the finite CAD lock in README."""

import json
import math
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
TOL = 0.00001
TOOL_HEIGHTS = (175, 120, 175, 120, 175, 120, 120)
CRATE_HEIGHTS = (120,) * 4 + (75,) * 6


def close(actual, expected, tolerance=TOL):
    assert math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0), (actual, expected)


def clean(design):
    assert all(not f.get("error") and not f.get("warning") for f in design["timeline"])
    assert all(not p.get("error") for p in design["params"])
    assert not design["sketches"]
    names = [body["name"] for body in design["bodies"]]
    assert len(names) == len(set(names)), "duplicate body names"
    assert all(body["closed"] and body["volume_mm3"] > 0 for body in design["bodies"])


def bounds(body, low, high):
    for key, expected in (("min", low), ("max", high)):
        for actual, target in zip(body["bbox"][key], expected):
            close(actual, target)


def box(body, low, high):
    bounds(body, low, high)
    close(body["volume_mm3"], math.prod(b - a for a, b in zip(low, high)), 0.01)
    assert body["kernel"]["shells"] == 1


def overlap(a, b, axis):
    return min(a["bbox"]["max"][axis], b["bbox"]["max"][axis]) - max(
        a["bbox"]["min"][axis], b["bbox"]["min"][axis]
    )


def separate(a, b):
    # ponytail: bbox separation proves no clash; intersecting hollow parts need CAD checks.
    assert any(overlap(a, b, axis) <= TOL for axis in range(3)), (a["name"], b["name"])


def check_toolbox(design, prefix, height, origin=(0, 0, 0), rotated=False):
    clean(design)
    assert height in (120, 175)
    p = {item["name"]: item["value"] for item in design["params"]}
    b = {item["name"]: item for item in design["bodies"]}
    suffixes = {"Case", "Lid", "Handle", "Latch_1", "Latch_2", "Hinge_1", "Hinge_2"}
    assert {name for name in b if name.startswith(prefix)} == {prefix + s for s in suffixes}
    if prefix == "tb_":
        assert len(b) == 7
    for name, value in (
        ("height", height), ("length", 400), ("depth", 300),
        ("inlet_l", 394), ("inlet_d", 248), ("lid_h", 20), ("floor_z", 23),
        ("foot_h", 10), ("recess", 10),
    ):
        close(p[prefix + name], value)
    close(p[prefix + "height"] - p[prefix + "lid_h"] - p[prefix + "floor_z"], height - 43)
    case_volume = 400 * 300 * (height - 30) - 394 * 248 * (height - 43)
    case_volume += 23040 - 145600 - 2 * 40 * 6 * 26 - 2 * 42 * 7 * 10
    volumes = {"Case": case_volume, "Lid": 1333648, "Handle": 77568,
               "Latch_1": 4560, "Latch_2": 4560, "Hinge_1": 2880, "Hinge_2": 2880}
    local_bounds = {
        "Case": ((-200, -150, 0), (200, 150, height - 20)),
        "Lid": ((-200, -150, height - 20), (200, 150, height)),
        "Handle": ((-180, -120, height - 8), (180, 120, height - 2)),
        "Latch_1": ((-188, -150, height - 45), (-150, -145, height - 21)),
        "Latch_2": ((150, -150, height - 45), (188, -145, height - 21)),
        "Hinge_1": ((-155, 144, height - 29), (-115, 150, height - 17)),
        "Hinge_2": ((115, 144, height - 29), (155, 150, height - 17)),
    }
    for suffix, volume in volumes.items():
        body = b[prefix + suffix]
        close(body["volume_mm3"], volume, 0.01)
        assert body["kernel"]["shells"] == 1
        low, high = local_bounds[suffix]
        if rotated:
            low, high = (-high[1], low[0], low[2]), (-low[1], high[0], high[2])
        bounds(body, tuple(a + o for a, o in zip(low, origin)),
               tuple(a + o for a, o in zip(high, origin)))


def check_cupboard(design):
    clean(design)
    b = {item["name"]: item for item in design["bodies"]}
    p = {item["name"]: item["value"] for item in design["params"]}
    assert len(b) == 141
    assert "shelf_t" not in p
    assert not any(name.startswith("Tool_shelf_") for name in b), "plywood shelves remain"
    bay, tool_bay, depth = p["bay_w"], p["tool_bay_w"], p["frame_d"]
    gap, tool_gap = p["head_gap"], p["tool_gap"]
    assert 304 <= bay <= 308 and 304 <= tool_bay <= 308 and 440 <= depth <= 460
    assert 29 <= gap <= 34 and 21 <= tool_gap <= 26
    width = bay + tool_bay + 72
    crate_cx, tool_cx, divider = -(tool_bay + 24) / 2, (bay + 24) / 2, (bay - tool_bay) / 2
    top = 143 + 4 * (128 + gap) + 5 * (83 + gap) + 75 + gap
    for name, value in (
        ("frame_w", width), ("crate_cx", crate_cx), ("tool_cx", tool_cx),
        ("divider_x", divider), ("top_z", top), ("overall_h", top + 44),
        ("post_h", top - 135), ("base_z", 91), ("first_z", 143),
        ("post_w", 24), ("post_d", 44), ("rail_h", 44), ("runner", 20),
        ("slide_drop", 12), ("low_h", 120), ("high_h", 75),
        ("caster_h", 73), ("pad_t", 18),
    ):
        close(p[name], value)

    timber_names = set()
    frame = []
    for level, z in (("Bottom", 91), ("Top", top)):
        for face, sy in (("Front", -1), ("Rear", 1)):
            name = f"{level}_{face}_rail"
            y = -depth / 2 if sy < 0 else depth / 2 - 24
            box(b[name], (-width / 2, y, z), (width / 2, y + 24, z + 44))
            timber_names.add(name)
            frame.append(b[name])
        for side, x in (("Left", -width / 2), ("Middle", divider - 12), ("Right", width / 2 - 24)):
            name = f"{level}_{side}_rail"
            box(b[name], (x, -depth / 2 + 24, z), (x + 24, depth / 2 - 24, z + 44))
            timber_names.add(name)
            frame.append(b[name])
    for side, x in (("Left", -width / 2), ("Middle", divider - 12), ("Right", width / 2 - 24)):
        for face, y in (("Front", -depth / 2), ("Rear", depth / 2 - 44)):
            name = f"{side}_{face}_post"
            box(b[name], (x, y, 135), (x + 24, y + 44, top))
            timber_names.add(name)
            frame.append(b[name])

    crates, runners = [], []
    z = 143
    for i, height in enumerate(CRATE_HEIGHTS, 1):
        crate = b[f"Crate_{i:02}_{height:03}"]
        bounds(crate, (crate_cx - 150, -200, z), (crate_cx + 150, 200, z + height))
        volume = 280 * 380 * (height - 20) - 270 * 370 * (height - 25)
        volume += (300 * 400 - 270 * 370) * 8 + (260 * 360 - 250 * 350) * 12 - 250 * 350
        close(crate["volume_mm3"], volume, 0.01)
        assert crate["kernel"]["shells"] == 1
        left, right = [b[f"Runner_{i:02}_{side}"] for side in ("Left", "Right")]
        for runner, x in ((left, crate_cx - bay / 2), (right, crate_cx + bay / 2 - 20)):
            box(runner, (x, -depth / 2, z - 8), (x + 20, depth / 2, z + 12))
            timber_names.add(runner["name"])
            assert overlap(crate, runner, 0) > 0 and overlap(crate, runner, 1) >= 400 - TOL
        opening = right["bbox"]["min"][0] - left["bbox"]["max"][0]
        close(opening, bay - 40)
        assert (opening - 260) / 2 >= 2 - TOL, "crate foot clearance"
        assert (280 - opening) / 2 >= 6 - TOL, "crate bearing overlap"
        next_bottom = b[f"Runner_{i + 1:02}_Left"]["bbox"]["min"][2] if i < 10 else top
        close(next_bottom - (z + height), gap)
        for member in frame:
            separate(crate, member)
        if crates:
            separate(crates[-1], crate)
        crates.append(crate)
        runners.extend((left, right))
        z += height + gap + 8

    tool_parts, ledgers = [], []
    tool_z = 135
    for i, height in enumerate(TOOL_HEIGHTS, 1):
        prefix = f"Tool_{i:02}_"
        check_toolbox(design, prefix, height, (tool_cx, 0, tool_z), rotated=True)
        case = b[prefix + "Case"]
        for side, x, foot_x in (
            ("Left", tool_cx - tool_bay / 2, tool_cx - 125),
            ("Right", tool_cx + tool_bay / 2 - 20, tool_cx + 125),
        ):
            ledger = b[f"Tool_ledger_{i:02}_{side}"]
            rail_half_depth = depth / 2 - (24 if i == 1 else 0)
            box(ledger, (x, -rail_half_depth, tool_z - 20),
                (x + 20, rail_half_depth, tool_z))
            timber_names.add(ledger["name"])
            close(ledger["bbox"]["max"][2], case["bbox"]["min"][2])
            # Modeled feet only: real foot geometry and printed bearing need verification.
            bearing = min(x + 20, foot_x + 12) - max(x, foot_x - 12)
            close(bearing, 137 - tool_bay / 2 + 20)
            assert 3 - TOL <= bearing <= 5 + TOL, "toolbox foot lateral bearing"
            for foot_y in (-175, 175):
                supported_depth = min(rail_half_depth, foot_y + 12) - max(-rail_half_depth, foot_y - 12)
                close(supported_depth, 24)
            if i > 1:
                close(ledger["bbox"]["min"][2] - b[f"Tool_{i - 1:02}_Lid"]["bbox"]["max"][2], tool_gap)
            ledgers.append(ledger)
        tool_parts.extend(body for name, body in b.items() if name.startswith(prefix))
        tool_z += height + tool_gap + 20
    assert b["Tool_07_Lid"]["bbox"]["max"][2] < top - TOL
    assert len(timber_names) == 50
    assert timber_names == {name for name in b if name.endswith(("_rail", "_post"))
                            or name.startswith(("Runner_", "Tool_ledger_"))}
    for part in tool_parts:
        for other in frame + crates + runners + ledgers:
            separate(part, other)

    for side, sx in (("Left", -1), ("Right", 1)):
        for face, sy in (("Front", -1), ("Rear", 1)):
            prefix = f"{side}_{face}"
            cx, cy = sx * (width / 2 - 40), sy * (depth / 2 - 40)
            for suffix, size, low, high in (("caster_pad", 80, 73, 91), ("caster_plate", 60, 70, 73)):
                box(b[f"{prefix}_{suffix}"], (cx - size / 2, cy - size / 2, low),
                    (cx + size / 2, cy + size / 2, high))


def inspect_saved(path, walk):
    commands = [{"command": "document.inspect", "params": {"measure": True}}]
    for name, values in walk:
        for value in values:
            commands.extend([
                {"command": "parameters.change", "params": {"name": name, "expression": f"{value} mm"}},
                {"command": "document.inspect", "params": {"measure": True}},
            ])
    with TemporaryDirectory(prefix="rolling-columns-check-") as directory:
        script = Path(directory) / "check.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(
            ["solidcraft-cli", "run", str(script), "--in", str(path), "--results"],
            capture_output=True, text=True, check=True,
        )
    results = json.loads(result.stdout)
    assert len(results) == len(commands)
    return results[::2]


def main():
    total = 0
    for filename, default in (("tb_4311.solidcraft", 120), ("tb_4316.solidcraft", 175)):
        heights = (120, 175, 120) + ((175,) if default == 175 else ())
        states = inspect_saved(HERE.parent / "auer_toolbox_pro" / filename, (("tb_height", heights),))
        for state, height in zip(states, (default,) + heights, strict=True):
            check_toolbox(state, "tb_", height)
        total += len(states)
    states = inspect_saved(HERE / "rolling_cupboard_columns.solidcraft", (
        ("bay_w", (304, 308)), ("tool_bay_w", (304, 308)),
        ("frame_d", (440, 460, 448)), ("head_gap", (34, 29)), ("tool_gap", (26, 21)),
    ))
    defaults = {"bay_w": 308, "tool_bay_w": 308, "frame_d": 448, "head_gap": 29, "tool_gap": 21}
    for state in (states[0], states[-1]):
        p = {item["name"]: item["value"] for item in state["params"]}
        for name, value in defaults.items():
            close(p[name], value)
    for state in states:
        check_cupboard(state)
    print(f"PASS saved native models: {total} toolbox states, {len(states)} cupboard states; "
          "7 toolboxes, 10 crates, 50 timber parts, support clearances and clean timelines")


if __name__ == "__main__":
    main()
