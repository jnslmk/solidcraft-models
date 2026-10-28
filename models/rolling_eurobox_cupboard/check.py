"""Read-only native geometry check; run under the finite CAD lock in README."""

import json
import math
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent


def close(actual, expected, tolerance=0.00001):
    assert math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0), (actual, expected)


def check(design):
    assert all(not f.get("error") and not f.get("warning") for f in design["timeline"])
    assert all(not p.get("error") for p in design["params"])
    assert not design["sketches"]
    p = {item["name"]: item["value"] for item in design["params"]}
    b = {item["name"]: item for item in design["bodies"]}
    assert len(b) == 74
    bay, depth, gap = p["bay_w"], p["frame_d"], p["head_gap"]
    width = bay + 48
    top = 143 + 4 * (128 + gap) + 5 * (83 + gap) + 75 + gap
    close(p["overall_h"], top + 44)
    timber = 0
    for name, body in b.items():
        if name.endswith("_rail") or name.endswith("_post") or name.startswith("Runner_"):
            timber += 1
            dims = [body["bbox"]["max"][j] - body["bbox"]["min"][j] for j in range(3)]
            close(body["volume_mm3"], math.prod(dims), 0.01)
            if name.endswith("_post"):
                for a, e in zip(dims, (24, 44, top - 135)):
                    close(a, e)
            elif name.endswith("_rail"):
                expected = (width, 24, 44) if "Front" in name or "Rear" in name else (24, depth - 48, 44)
                for a, e in zip(dims, expected):
                    close(a, e)
    assert timber == 32
    z = 143
    for i, height in enumerate([120] * 4 + [75] * 6, 1):
        crate = b[f"Crate_{i:02}_{height:03}"]
        for side, target in (("min", (-150, -200, z)), ("max", (150, 200, z + height))):
            for a, e in zip(crate["bbox"][side], target):
                close(a, e)
        volume = 280 * 380 * (height - 20) - 270 * 370 * (height - 25)
        volume += (300 * 400 - 270 * 370) * 8 + (260 * 360 - 250 * 350) * 12 - 250 * 350
        close(crate["volume_mm3"], volume, 0.01)
        assert crate["kernel"]["shells"] == 1
        left, right = [b[f"Runner_{i:02}_{side}"] for side in ("Left", "Right")]
        for runner in (left, right):
            close(runner["bbox"]["max"][2], z + 12)
            close(runner["bbox"]["min"][2], z - 8)
            close(runner["volume_mm3"], 400 * depth, 0.01)
        opening = right["bbox"]["min"][0] - left["bbox"]["max"][0]
        close(opening, bay - 40)
        assert (opening - 260) / 2 >= 2 - 0.00001
        assert (280 - opening) / 2 >= 6 - 0.00001
        next_bottom = b[f"Runner_{i + 1:02}_Left"]["bbox"]["min"][2] if i < 10 else b["Top_Front_rail"]["bbox"]["min"][2]
        close(next_bottom - (z + height), gap)
        z += height + gap + 8
    for side, sx in (("Left", -1), ("Right", 1)):
        for face, sy in (("Front", -1), ("Rear", 1)):
            prefix = f"{side}_{face}"
            for suffix, size, low, high in (("caster_pad", 80, 73, 91), ("caster_plate", 60, 70, 73)):
                body = b[f"{prefix}_{suffix}"]
                cx, cy = sx * (width / 2 - 40), sy * (depth / 2 - 40)
                for key, expected in (("min", (cx - size / 2, cy - size / 2, low)), ("max", (cx + size / 2, cy + size / 2, high))):
                    for actual, target in zip(body["bbox"][key], expected):
                        close(actual, target)


def main():
    commands = [{"command": "document.inspect", "params": {"measure": True}}]
    for name, values in (("bay_w", (304, 308)), ("frame_d", (440, 460, 448)), ("head_gap", (34, 29))):
        for value in values:
            commands.extend([
                {"command": "parameters.change", "params": {"name": name, "expression": f"{value} mm"}},
                {"command": "document.inspect", "params": {"measure": True}},
            ])
    with TemporaryDirectory(prefix="rolling-cupboard-check-") as directory:
        script = Path(directory) / "check.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(
            ["solidcraft-cli", "run", str(script), "--in", str(HERE / "rolling_cupboard.solidcraft"), "--results"],
            capture_output=True, text=True, check=True,
        )
    for state in json.loads(result.stdout)[::2]:
        check(state)
    print("PASS saved cupboard: 8 states, 10 crates, 20 runners, 32 timber parts, caster pads/plates and clean timelines")


if __name__ == "__main__":
    main()
