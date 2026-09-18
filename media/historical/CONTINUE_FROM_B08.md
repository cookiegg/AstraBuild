# Continue from B08 r2 — shared transformer exterior

Latest station: output/installation_B08/site_B08_shared_transformers_r2.blend.
Default scene: 42_B08_Transformer_Pair. Editable master scene: 44_B08_EDIT_SHARED_MASTER.
Offline review: output/installation_B08/B08_review.html.
Directly openable local asset: output/installation_B08/B08_transformer_editable.blend.
Append library: output/installation_B08/B08_transformer_shared_asset_r2.blend.
Queue snapshot: asset_variant_installation_queue_v8.json. CURRENT.md is the mutable pointer.

## User-confirmed configuration

User: “好的，继续主变1，主变2跟主变一的部件是完全一样的，做好其中一个，另一个复用就行”

This explicitly authorizes one common component configuration for T1 (12MZ0000000150023)
and T2 (12MZ0000000149769). It supersedes B07's pending T2 configuration review.
Do not ask again whether the two transformers share parts. Position and external conductors
are still site-specific. B08 is a downstream photo/coarse exterior assembly, not a claim
that the unchanged frozen P04 full core fits the station. The queue's old exact P04 variant
flag stays separate from the new explicit T1/T2 configuration confirmation.

## Editable reuse

B08_TRANSFORMER_MASTER is authored in local meter coordinates. The T1 and T2 site roots
reference exactly this same collection. Both root transforms are rigid, positive, scale 1.
Edit the master in scene 44 inside the station file; the two in-file instances update together.
Do not make one unit real and edit its parts independently. Site leads live in B08_T1_SITE_LEADS
and B08_T2_SITE_LEADS. The standalone file is for independent editing/Append into other projects;
it is not externally linked back to this station file.

The master has 473 direct meshes and 47 nested module instances.
Each unit expands to 1606 meshes, verified against Blender's dependency graph.
Shared nested modules: 34 radiator packs, 11 roof bushings, 2 cabinet instances.
The standalone file opens directly into the local edit scene and matches exported geometry.

## Built scope and evidence

- Kept B07 oil tank, upper rounded enclosure, louvers, ladder, supports and four original
  roof bushings in the calibrated T1 frame, copied into an independently editable B08 master.
- Rebuilt a new radiator class at 0.53 × 1.40 × 3.25 m candidate envelope, 17 packs per bank.
  Front #1 is visible in DJI_20260804130719_0012_V; rear #18 in DSC3181 and #34 plus preceding
  numbers in DSC3184 support a 17+17 layout. Front count is supported by numbering continuity,
  not a direct reading of all 17 plates. Ten internal leaves per pack remain illustrative.
  Coarse inner/outer bank separation supports about 1.4 m depth; this is not a survey.
  Frozen P04 radiator geometry was not stretched or overwritten.
- Added seven rear roof bushings: three medium, one outer short and three low terminal
  bushings, based on DSC3172, side photographs and coarse slices. Medium unequal spacing is
  retained. P04 small bushing classes are reused at uniform 3.2 / 2.7 / 1.2 scales; voltage,
  phase and exact shed counts remain unassigned. Nearby neutral devices and the foreground
  bus support rack remain separate equipment, not extra main-tank bushings.
- Added smart terminal and oil/gas monitor cabinets, identified in DSC3188/3189. DSC3190
  supports their distinct heights and visible lifting eyes. Depth and location are coarse
  candidates. Door seams, handles, vents, unread labels, plinths and pavement pad included.
- Added rear visible fire rails/supports, pipe-post clamps, radiator beams/legs and visible
  end service box/tube/gauge. Hidden routes and structural/hydraulic design are not asserted.
- Each unit has six independently traced paired leads (12 conductor meshes), following
  the corresponding original coarse crop. Paths stop around local Z 12.2–12.5 m at the
  last traced observations. Remote connections remain unaccepted; no extrapolation to an
  assumed station circuit. The two leads of each pair meet the modeled terminal center.
  Wire diameter/spacing and terminal-to-first-observation interpolation are approximate.
  Three low terminal bars remain bounded visible segments; their rack connections are pending.

Additional original photo paths, hashes and roles are in B08_plan.json. All ten originals
are unchanged. Earlier P04 photo sources remain available in inputs/P04/photo_sources.json.
T1_reference.npz / T2_reference.npz preserve registered coarse triangle crops; each triangle
has source tile and original index in the corresponding reference_origins.json. T2 crop
uses the initial seed frame; apply inverse T2_rigid_correction to compare in final local frame.
B08_lead_tracking.png shows traced paths over source coordinates; rendered views are actual
Blender images, with no generative substitution for photos or geometry evidence.

## Site pose and readback

T1 keeps the B07 calibrated frame. T2 first uses the legacy seed relation, then a rigid
correction: local translation [0.682643, -0.399223, -0.011985] m, yaw -0.008764 degrees.
Bank direction/offset, upper-enclosure X extent center and front bank top constrain this pose.
No shape, scale or individual component adjustment was applied only to T2.

Bank plane checks use alternating 1 m X strips held out before fitting. The original gates
and all held-out residuals are retained, without post-fit rejection.

| Unit / bank | Held-out triangles | Median absolute distance / m | P95 / m |
| --- | ---: | ---: | ---: |
| T1 front | 1226 | 0.0112 | 0.1934 |
| T1 rear | 1000 | 0.0090 | 0.2833 |
| T2 front | 1267 | 0.0212 | 0.6201 |
| T2 rear | 1105 | 0.0190 | 0.2504 |

These are exterior-plane diagnostics only. Tail residuals are substantial, especially T2
front P95 0.6201 m. Investigate source-surface correspondence and local mismatches; do not
report whole-device centimeter accuracy from the medians. No full-device, measured scale,
electrical-clearance or mechanical acceptance is implied by the validator's passed status.

Readback preserved 21459 objects, 228 collections,
18 scenes, 256 materials, 15,096 v50 components,
69 B06 civil meshes and 380 protected files. Old T1/T2's 378 meshes are only
omitted in new B08 working scenes; all remain in historical scenes. The new station retains
14,347 original tagged component meshes. Other 15 arrester candidates and one partial GIS
cabinet are unchanged; 746-A/B, 748-B mounting issues and 749 depth pending remain open.
Working queue now contains 18 equipment candidates, not 18 completed/accepted devices.

Shared edit propagation was checked in memory and restored without saving the probe.
Conductor lower rings match manufactured terminal ports to floating point tolerance;
max saved-coordinate error 0.00000199 m is a connectivity check, not measured accuracy.
Radiator support/beam and cabinet/pad contact checks pass. All five tested candidate cameras
frame the entire modeled candidate; source context outside the crop may be clipped.
Eleven final r2 PNGs passed read/size/nonblank checks and were rendered on the workstation GPU.

## Views and continuation

- 34 / 35: station clean / original coarse overlay.
- 36 / 37: T1 front / rear clean exterior.
- 38 / 39: T1 rear / vertical orthographic top overlay.
- 40 / 41: T2 rear clean / coarse overlay.
- 42: pair with independent visible leads (default).
- 43: T1 lead overlay.
- 44: edit the shared local master.
- 45 / 46: original T1 / T2 rear references, same cameras as their comparisons.

Next: investigate T2 front residual tail; resolve remote lead junctions and short terminal
connections to separate equipment; refine occluded details only with further evidence.
Continue GIS longitudinal review, arrester mounting failures and gate dimensions afterwards.
Keep the shared body configuration and existing B06 wall calibration. Formal promotions: zero.

R1 is retained. R2 adds 39 support meshes and snaps lead end rings by at most 1.45 mm to
the manufactured source port. No frozen file or historical README was overwritten.
CURRENT.md alone is a mutable latest-version pointer.
