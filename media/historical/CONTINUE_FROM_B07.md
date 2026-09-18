# Continue from B07 r2 — #1 partial transformer site exterior

Current model: output/installation_B07/site_B07_T1_site_exterior_r2.blend.
Review: output/installation_B07/B07_review.html. Validation: output/installation_B07/B07_validation_r2.json.
Queue: asset_variant_installation_queue_v7.json. Latest entry: CURRENT.md.

## Completed scope

Target is #1 主变 ABC 相, registry 12MZ0000000150023. This is a downstream site-calibrated
partial exterior candidate, combining original photographs and registered coarse geometry.
It is NOT an unchanged installation of P04 full core and NOT a new independent photo-only asset.
P04 r3 and all its frozen files remain unchanged. Original P04 proportions could not match
bank span/height and bushing positions with one uniform scale; the rejected initial overlay
is retained in the B07 workbench, with no acceptance claim.

The new tank and upper exterior enclosure are parameterized from coarse envelopes and photo
form. Hidden geometry remains inferred; no internal winding, vessel or hydraulic CAD is claimed.
36 frozen P04 radiator modules use one uniform scale of 3.4; the 18-per-side count is illustrative.
Three frozen tall bushings share scale 2.9; one small bushing uses its separate scale 3.2.
Individual bushing axes are fitted to coarse slice centers. No phase assignment is made.
The radiator inner depth remains the uniformly scaled P04 hypothesis, not an accepted measurement.
Foundation and visible open U / overhead fire routes are separate coarse-relative approximations.
Their incomplete rear routing is not a hydraulic design.

Assembly heading changes 2.9045 degrees relative to the old #1 seed frame;
origin shifts locally to [0.3, 2.9448489824189887, 0.0]. This frame was only an initial coordinate
reference. Actual coarse features set placement; the old model was not used as ground truth.

New working scenes omit all 189 legacy #1 meshes and insert 1178 expanded
candidate meshes (362 new authored parts and 40 module instances).
Other retained original equipment meshes: 14536.
All 11 earlier scenes and the old #1 model remain available for comparison. #2 is unchanged.
Existing 15 arrester candidates, one partial GIS cabinet, 69 B06 civil meshes, mounting failures
746-A/B and 748-B, and 749 cabinet-depth pending status are preserved. Formal promotions: zero.
The working queue contains 17 equipment candidates, including the partial cabinet and partial
transformer; this is not a completed or accepted device count.

## Evidence and checks

Photos inspected: P04 crops DJI_20260804130750_0016_V and DJI_20260825145628_0049_V,
the P04 photo contact sheet, photo source manifest and frozen P04 primary model render.
Original source paths/crop rectangles are recorded in inputs/P04/photo_sources.json.
The full coarse crop contains 331600 triangles;
each face has tile name and original triangle index in B07_reference_full_origins.json.

Bank fit gates are stored in B07_plan.json. Alternating 1 m X strips are held out, with no
post-fit residual rejection on the held-out triangles. Both banks share one rigid heading;
their outer leaf planes are checked from saved instance and source vertex coordinates.
- front: old median 1.1779 m; new median 0.0119 m; new P95 0.2375 m; 1506 held-out triangles.
- rear: old median 4.7251 m; new median 0.0105 m; new P95 0.2816 m; 1352 held-out triangles.

These metrics describe bank exterior planes only. The P95 values and remaining visible
mismatches are retained; this does not measure inner bank depth, count, full-device accuracy,
survey accuracy or electrical acceptance. Bushing axes use the fit data itself and are not
reported as independently validated.

Readback passed: 20930 original objects, 219
collections, 11 scenes, all 15,096 formal v50 tagged meshes,
124 source module objects,
and 330 protected files. Mesh data, local transforms, material slots
and source properties of the reusable modules are unchanged; appended module object color
is cyan only for overlay display. All 40 instance transforms have uniform positive scales.
Manual expanded mesh count equals the Blender dependency graph count.

R1 top camera clipped the station surround due to world-up orientation. R2 explicitly aligns
that camera with the assembly XY axes and preserves all 402
candidate objects from r1. Both final detail and top cameras frame the entire candidate.
All seven final r2 PNGs were rendered by actual Blender Workbench on the workstation GPU.
The first validator attempted to keep ephemeral dependency graph wrappers; it now reads
their mesh types while iterating. No geometry or residual threshold was relaxed for this fix.

## Views

- 27_B07_Station_Clean: complete working station context, with partial #1 candidate.
- 28_B07_Station_Overlay: station plus original coarse.
- 29_B07_T1_Clean: default local candidate, material colors.
- 30_B07_T1_Overlay: cyan candidate over gray original crop.
- 31_B07_T1_Reference: same camera, original crop only.
- 32_B07_T1_Top_Overlay: local axes, vertical orthographic camera.
- 33_B07_T1_Before_Overlay: same detail camera and crop, old #1 model.

## Next work

1. Reconcile remaining visible front/side and rear bushings with full source photos before
   adding modules. Four fitted bushings are a bounded subset, not the full transformer inventory.
2. Revisit radiator count and depth, hidden tank shape, interface routes and accessory cabinets.
   The new working scene currently omits all legacy #1 accessories; they remain in B06/v50.
3. Reconstruct visible conductors only after terminal correspondences are established.
4. Review #2 independently before copying any station variant. Continue GIS longitudinal
   review, arrester mounting failures and gate dimensions without changing frozen sources.

Do not overwrite existing builds, captures, source assets or historical README.md.
CURRENT.md is deliberately mutable; the B07 continuation and v7 queue are release snapshots.
