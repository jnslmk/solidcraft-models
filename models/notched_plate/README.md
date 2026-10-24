# Notched plate sketch

`notched_plate.solidcraft` is the authoritative editable design. It contains one fully constrained XY sketch, `NotchedPlateProfile`, matching the supplied photograph's outline: a tall plate, flared open-top slot, four rounded outside corners, and one lower circular hole. No extrusion or thickness was requested.

The photograph has no scale. All dimensions below are proportional estimates, not measurements of the photographed object.

## Driving parameters

All dimensions are in mm. Parameters are marked as favourites in the design. Point-coordinate expressions preserve centring, symmetry, and relative placement; the hole diameter has a driving sketch dimension.

| Parameter | Default | Allowed range | Meaning |
|---|---:|---:|---|
| `width` | 40 | 36–60 | Overall width |
| `height` | 100 | 90–150 | Overall height |
| `slot_width` | 8 | 6–12 | Straight slot width |
| `slot_depth` | 32 | 26–40 | Slot floor depth below the top |
| `flare` | 8 | 6–9 | Both horizontal and vertical extent of each 45° lead-in |
| `hole_diameter` | 9 | 6–12 | Lower hole diameter |
| `hole_from_bottom` | 25 | 18–32 | Hole centre height above the bottom |
| `corner_radius` | 1.5 | 0.5–2 | Four exterior corner radii |

The origin is at the centre of the overall bounding rectangle. The slot and hole are centred on X=0. At defaults the slot mouth is 24 mm wide, the slot floor is Y=18 mm, and the hole centre is (0, −25) mm.

## Interfaces and manufacturing

No measured or fixed mating interfaces were supplied. The hole and slot are conceptual interfaces only: no fit allowance or manufacturing tolerance has been established, and physical fit is untested. The photograph depicts wood; PETG is the project default if this profile is later made into a printed part. The sketch lies at Z=0; a future positive-Z extrusion would put its broad face on the build plate. There is currently no solid body, printable STL, or specified thickness.

## Verification

Verified with the installed SolidCraft engine, including reopening the saved native file:

- Sketch solved with zero degrees of freedom; 10 lines, four arcs, and one circle.
- No timeline errors or warnings; zero solid bodies, intentionally.
- Overall bounds: X=−20…20 mm, Y=−50…50 mm, Z=0.
- Slot width, floor location, flare, hole diameter and position, and corner radii checked against independent expressions.
- Plate profile area, excluding the hole: 3614.451332 mm². Analytic expectation: `width*height - slot_width*slot_depth - flare^2 - (4-pi)*corner_radius^2 - pi*hole_diameter^2/4`, checked within 0.005 mm².
- Each driving parameter exercised at both documented endpoints and returned to its default, checking solver state, profile area, and interface positions at each state. Defaults were retained in the saved file.
- Top and isometric renders inspected. Inspection images remain disposable under `.codex-tmp/notched_plate/`, not model deliverables.

For a later extrusion, select the plate region (profile 0), not both regions: the circle also appears as selectable profile 1 and must remain a hole.
