"""Check the saved endcaps against independent build123d reference measurements.

Run from the repository root: uv run --no-project models/led_profiles/check.py
Run CAD checks under the workstation heavy-verification lock and a finite timeout.
The native files are source; this script inspects them and never rewrites them.
"""

import json
import math
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from export_stl import validate_stl

HERE = Path(__file__).resolve().parent
# Fresh create_endcap(DEFAULT) / create_endcap_wired() from the sibling source.
REFERENCE = {
    "endcap": {
        "volume_mm3": 7209.672471272087,
        "area_mm2": 5156.599925814905,
        "center_of_mass": (0.002991164545541252, -1.2102720888720258, 8.954641242708714),
        "top": 31.85,
    },
    "endcap_wired": {
        "volume_mm3": 10575.110654484079,
        "area_mm2": 6846.136864603628,
        "center_of_mass": (0.0020390183401315888, -0.45308407511154436, 12.715659730764253),
        "top": 41.85,
    },
}


ENDPOINTS = {
    "endcap": {
        8: (6752.28369153914, 4563.97553351916,
            (0.0031937655684065114, -0.6290879419995205, 7.68161799915011)),
        30: (8010.10283580474, 6193.692612332463,
             (0.002692287699809646, -2.067634416798936, 11.93180761721042)),
    },
    "endcap_wired": {
        8: (10117.72188022515, 6253.512472307882,
            (0.0021311936220721034, -0.030988115650012298, 11.584035986044771)),
        30: (11375.54100943722, 7883.229551121185,
             (0.0018955476457912066, -1.1100758315341603, 15.251036219986377)),
    },
}


def assert_matches(name, design, expected):
    for feature in design["timeline"]:
        assert not feature["error"], (name, feature["name"], feature["error"])
        assert not feature["warning"], (name, feature["name"], feature["warning"])
    for parameter in design["params"]:
        assert not parameter["error"], (name, parameter["name"], parameter["error"])
    for sketch in design["sketches"]:
        assert sketch["dof"] == 0 and sketch["status"] == "solved", (name, sketch)
    assert len(design["bodies"]) == 1, (name, len(design["bodies"]))
    body = design["bodies"][0]
    assert body["kernel"]["shells"] == 1, (name, body["kernel"])
    # SolidCraft measures the displayed tessellation, not OCCT's exact BREP.
    for field in ("volume_mm3", "area_mm2"):
        assert math.isclose(body[field], expected[field], rel_tol=0.001), (
            name, field, body[field], expected[field]
        )
    for field, target in (
        ("center_of_mass", expected["center_of_mass"]),
        ("bbox_min", (-13.05, -15.25, 0)),
        ("bbox_max", (13.05, 15.25, expected["top"])),
    ):
        actual = body["bbox"][field.removeprefix("bbox_")] if field.startswith("bbox_") else body[field]
        assert all(abs(a - b) <= 0.005 for a, b in zip(actual, target, strict=True)), (
            name, field, actual, target
        )
    print(f"PASS {name}: one body, healthy timeline, constrained sketches, reference dimensions and mass properties")


def check(name, expected):
    commands = [{"command": "document.inspect", "params": {"measure": True}}]
    for depth in (8, 30, 16):
        commands.extend([
            {"command": "parameters.change", "params": {
                "name": "plug_depth", "expression": f"{depth} mm"}},
            {"command": "document.inspect", "params": {"measure": True}},
        ])
    scratch = HERE.parents[1] / ".codex-tmp"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="endcap-check-", dir=scratch) as directory:
        script = Path(directory) / "walk.json"
        script.write_text(json.dumps({"commands": commands}))
        result = subprocess.run(
            ["solidcraft-cli", "run", str(script), "--in",
             str(HERE / f"{name}.solidcraft"), "--results"],
            capture_output=True, text=True, check=True,
        )
    results = json.loads(result.stdout)
    assert_matches(f"{name} default", results[0], expected)
    for index, depth in ((2, 8), (4, 30)):
        volume, area, center = ENDPOINTS[name][depth]
        assert_matches(f"{name} plug_depth={depth}", results[index], {
            "volume_mm3": volume, "area_mm2": area,
            "center_of_mass": center, "top": expected["top"] + depth - 16,
        })
    assert_matches(f"{name} restored", results[6], expected)
    mesh = validate_stl(HERE.parents[1] / "exports" / "led_profiles" / f"{name}.stl")
    assert math.isclose(mesh["mesh_volume_mm3"], expected["volume_mm3"], rel_tol=0.001), (
        name, mesh["mesh_volume_mm3"], expected["volume_mm3"]
    )
    print(f"PASS {name}.stl: one closed, outward-oriented edge- and vertex-manifold shell")


if __name__ == "__main__":
    for name, expected in REFERENCE.items():
        check(name, expected)
