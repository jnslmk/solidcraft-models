#!/usr/bin/env python3
"""Read-only binary STL topology check; Python standard library only.

Validator copied from models/led_profiles/export_stl.py. Exact coordinate
identity is used: no rounding, welding, repair, or geometry regeneration.
"""
import argparse
import json
import math
import struct
from pathlib import Path


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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path)
    args = parser.parse_args()
    data = args.stl.read_bytes()
    result = {"file": args.stl.as_posix()}
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + 50 * count:
            result["triangles"] = count
            result["repeated_vertex_facets"] = sum(
                len({values[3:6], values[6:9], values[9:12]}) < 3
                for values in (
                    struct.unpack_from("<12f", data, 84 + 50 * index)
                    for index in range(count)
                )
            )
    try:
        result.update(validate_stl(args.stl))
    except ValueError as error:
        result.update(valid=False, error=str(error))
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    result["valid"] = True
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
