#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["build123d==0.10.0", "ocp-gordon==0.1.18"]
# ///
"""Tessellate an exported native STEP, without redefining the SolidCraft model.

Usage: uv run --script export_stl.py native-export.step printable.stl
SolidCraft's direct STL has microscopic threaded-face seam defects. OCCT meshes
its exported STEP consistently; this script rejects rather than heals a bad mesh.

The ocp-gordon pin keeps build123d 0.10 on its compatible OCP 7.8 ABI.
"""

import argparse
import json
import math
import struct
from pathlib import Path
from tempfile import TemporaryDirectory


def validate_stl(path: Path) -> dict:
    """Require a closed, oriented, edge- and vertex-manifold connected shell."""
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError("Expected a nonempty binary STL")
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50 * count or not count:
        raise ValueError("Invalid or empty binary STL")
    vertices, faces, edges, vertex_faces = {}, [], {}, {}
    volume = 0.0
    for index in range(count):
        values = struct.unpack_from("<12f", data, 84 + 50 * index)[3:]
        points = [values[start : start + 3] for start in (0, 3, 6)]
        if not all(math.isfinite(value) for point in points for value in point):
            raise ValueError("Mesh has a non-finite coordinate")
        face = tuple(vertices.setdefault(point, len(vertices)) for point in points)
        if len(set(face)) != 3:
            raise ValueError("Mesh has a degenerate facet")
        a, b, c = points
        cross = (
            b[1] * c[2] - b[2] * c[1],
            b[2] * c[0] - b[0] * c[2],
            b[0] * c[1] - b[1] * c[0],
        )
        volume += sum(x * y for x, y in zip(a, cross)) / 6
        faces.append(face)
        for vertex in face:
            vertex_faces.setdefault(vertex, set()).add(index)
        for a, b in zip(face, face[1:] + face[:1]):
            edges.setdefault(tuple(sorted((a, b))), []).append((index, a < b))
    if any(len(incident) != 2 for incident in edges.values()):
        raise ValueError("Mesh is not closed and edge-manifold")
    if any(incident[0][1] == incident[1][1] for incident in edges.values()):
        raise ValueError("Mesh has inconsistent winding")
    adjacency = [[] for _ in faces]
    for (first, _), (second, _) in edges.values():
        adjacency[first].append(second)
        adjacency[second].append(first)
    reached, stack = {0}, [0]
    while stack:
        for other in adjacency[stack.pop()]:
            if other not in reached:
                reached.add(other)
                stack.append(other)
    if len(reached) != len(faces):
        raise ValueError("Expected one connected printable shell")
    for vertex, incident in vertex_faces.items():
        reached = {next(iter(incident))}
        stack = list(reached)
        while stack:
            for neighbour in faces[stack.pop()]:
                if neighbour != vertex:
                    for other, _ in edges[tuple(sorted((vertex, neighbour)))]:
                        if other not in reached:
                            reached.add(other)
                            stack.append(other)
        if reached != incident:
            raise ValueError("Mesh has a nonmanifold vertex")
    if not math.isfinite(volume) or volume <= 0:
        raise ValueError("Mesh has no positive outward-oriented volume")
    return {
        "triangles": count,
        "vertices": len(vertices),
        "edges": len(edges),
        "connected_components": 1,
        "closed_edge_and_vertex_manifold": True,
        "consistent_outward_winding": True,
        "mesh_volume_mm3": volume,
    }


def main():
    from build123d import export_stl, import_step

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_step", type=Path)
    parser.add_argument("printable_stl", type=Path)
    args = parser.parse_args()
    if args.native_step.resolve() == args.printable_stl.resolve():
        parser.error("STEP input and STL output must be different files")
    # No model geometry lives here: the persisted native design supplies STEP.
    with TemporaryDirectory(prefix="endcap-mesh-", dir=args.native_step.resolve().parent) as directory:
        temporary = Path(directory) / "mesh.stl"
        shape = import_step(str(args.native_step))
        export_stl(shape, str(temporary), tolerance=0.005, angular_tolerance=0.1)
        metrics = validate_stl(temporary)
        args.printable_stl.write_bytes(temporary.read_bytes())
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
