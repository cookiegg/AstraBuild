# Continue from B06 r2 — civil perimeter plan calibrated

Current file: output/installation_B06/xialin_photo_first_B06_wall_aligned_r2.blend.
Saved-file check: output/installation_B06/B06_validation_r2.json.
Queue: asset_variant_installation_queue_v6.json. Current entry: CURRENT.md.
All B05 and formal v50 source scenes remain present and unchanged.

## Completed change

Existing NW and E wall headings were 29.3063° and -60.2395°. New plan headings are
25.5889° and -64.4160°, fitted to inward-facing vertical triangles of the original
registered coarse mesh. The model inward face, not its centerline, follows the
observed wall surface; inherited thickness remains 0.28 m. Centerline corner is
(14.680765, 46.285317) m. Endpoints retain prior observed coverage, projected onto
the corrected lines. Unobserved perimeter sections were not fabricated.

Alternate 2 m strips were held out. Median absolute face distance on heldout
triangles changed from 1.4083 to 0.03223 m (NW), and 7.8696 to 0.01466 m (E).
P95 after correction is 0.11570 / 0.10446 m. Independent heldout direction fits
differ by 0.01894° / 0.00150°. These are coarse-relative comparisons, not survey
accuracy. Sampling gates, source indices and fitting limits remain in B06_plan.json.

Gate: all 13 authored gate components are rigid copies, without shape or width
changes. Center moved to (-43.281369, 17.725686) m; heading follows the corrected
NW wall. Pose uses the closed-leaf plane and one clear pillar. Width remains
9.69127 m from the earlier photo/RTK approximation. Opposite pillar, exact clear
opening and height remain unresolved because the coarse gate region has overlap
and missing surfaces. Four short wall-return components connect the recessed gate
to the wall. These connections are inferred junction geometry, not new measured detail.

Working scenes replace the 61 legacy wall/gate meshes with 69 civil candidate
meshes. 14,725 other original components plus 901 existing equipment candidate
mesh instances remain, for 15,695 components in the working equipment/civil set.
The 15 arrester candidates, one partial GIS cabinet, 746-A/B and 748-B failures,
cabinet depth pending flag and full GIS non-installation are unchanged.
Formal promotions remain zero; civil revision is not an additional accepted device.

## Views and validation

- 21_Photo_First_B06_Station_Clean: material view, existing overview camera.
- 22_Photo_First_B06_Coarse_Overlay: default, cyan civil candidate over original coarse.
- 23_B06_Wall_Top_Overlay: full top view.
- 24_B06_Station_Perspective: actual perspective camera with coarse context.
- 25_B06_Wall_Top_Clean: clean top view.
- 26_B06_Gate_Overlay: local gate alignment and outstanding shape differences.

R2 only improves new camera framing, persists review colors and adds coarse context
to the perspective scene. It preserves all 69 r1 civil geometries. All 20,857 original
objects, 214 original collections, five original scenes, 15,096 formal tagged meshes,
original cameras, mesh data, material slots, custom properties and 288 protected
files passed unchanged checks. Complete coarse and civil bounding boxes fit the two
new overview cameras. Seven final frames were rendered on the workstation GPU.

Initial preservation check read uninitialized world matrices for objects excluded
from the default B06 scene. The validator now evaluates the same original scenes
before comparing; no tolerance was relaxed, and source transforms are unchanged.
Top framing in r1 clipped part of the coarse context, so r2 frames all coarse tile
and civil object bounding boxes. Keep r1 and diagnostics for traceability.

The historical README.md is included in the protected B05 release; it is unchanged.
Use CURRENT.md as the latest entry. Never rerun builders over existing outputs.
