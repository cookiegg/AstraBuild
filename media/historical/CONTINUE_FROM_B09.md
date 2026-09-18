# Continue from B09 — capacitor bank exterior candidates

Latest station: output/installation_B09/site_B09_capacitor_banks.blend
SHA256: d9d95b447b58165719096bb2f53d1f630fca0170e9ebfb5abea58a1b48e60b5f
Default scene: 59_B09_Three_Banks. Station: 47_B09_Station_Clean.
Review: output/installation_B09/B09_review.html (12 embedded real Blender renders).
Standalone editable local #1 bank: output/installation_B09/B09_capacitor_editable.blend.
Append library: output/installation_B09/B09_capacitor_append_library.blend.
Queue: asset_variant_installation_queue_v9.json. CURRENT.md is mutable; all prior snapshots frozen.

## User scope and preserved work

User requested “继续后续其他设备处理”. B09 processes VC-C capacitor groups #1/#2/#3,
respectively 031 / 12MZ0000000242519, 032 / 12MZ0000000242517, 033 / 12MZ0000000242515.
This is a bounded core-exterior batch, not a claim to finish all station equipment.
T1 and T2 still share B08_TRANSFORMER_MASTER exactly as the user explicitly confirmed;
do not reopen the same-parts question. Edit scene 44 in the main file for both transformer bodies.

B09 readback preserves 22,106 previous objects, 242 collections, 31 scenes, 263 materials,
all 15,096 v50 formal components, 69 B06 civil meshes and 445 protected files.
All 3,852 legacy meshes for these three capacitor banks are omitted only in new B09 scenes;
they remain in every historical scene. New station context retains 10,495 original tagged
component meshes plus previous candidates and B09. All old mounting failures 748-B and
746-A/B, 749 cabinet depth, B08 residual/remote lead issues remain pending.
Working candidates = 21 (15 arresters + 1 partial GIS cabinet + 2 transformer exteriors
+ 3 capacitor bank core exteriors), not completion/acceptance counts. Formal promotions = 0.

## Evidence and site geometry

Original photos individually viewed with readable signs:
- DJI_20260804130920_0027_V: #1 / 031.
- DJI_20260804130949_0031_V: #2 / 032.
- DJI_20260804131021_0035_V: #3 / 033.
- DJI_20260825145433_0032_V: elevated arrangement reference. Foreground is another group
  (#6); it is not direct #3 pose evidence. Used only for family form/arrangement.

All paths and hashes in B09_plan_r2.json; source photographs unchanged.
031/032/033_reference.npz contain original registered coarse triangle crops in legacy seed
frames. Corresponding reference_origins.json preserve each source tile / triangle index.
To convert crop coordinates to final bank coordinates use inverse(manifest.frames[unit])
times reference.frame_to_world. Do not treat legacy placement as ground truth.

Old banks placed reactor / front discharge equipment in the reverse longitudinal order.
B09 puts the reactor at local Y about -2, two-layer racks near +0.5 and low discharge tanks
near +2.4, with individually fitted coordinates. Final yaw relative to each seed is about
2.8–3.0 degrees. Fences remain rectangular, fitted independently from equipment dimensions.
R1 plan picked a forward face for 033 lane 3; r2 restricts every rack to the negative-X
plain-back face, keeping r1 and its hash. Do not use B09_plan.json for the final bank poses.

## Shared editable parts

Each bank has 3 racks, 3 cylindrical reactor bodies, 3 low discharge tanks, 3 small arresters,
concrete pads, visible bus strips, front supports, fence and four incoming supports.
Each bank expands to 1,560 mesh instances; saved dependency-graph counts agree.
There are 299 newly authored direct mesh objects and 108 authored collection instances,
including site roots and nested class assembly pieces (not unique field equipment counts).

- P05_RACK_ASSEMBLY reused unchanged at uniform 0.80 scale, rotated 180 degrees about Z;
  its same-end paired terminals face +X. Eight modeled cans per rack (two layers × four)
  remain a candidate fine count. This is not acceptance of the frozen P05 BANK_DEMO site layout.
- P05_POST_INSULATOR, P05_DISCHARGE_BUSHING and P05_SMALL_ARRESTER retained unchanged;
  all 119 appended source objects pass local mesh/material/reference preservation checks.
- B09_REACTOR_BODY_MASTER is a newly authored dimensional class, radius 0.598336 m,
  height .70 m, inner bore .28 m. Frozen P05 body was not stretched. Eight top spokes are
  visual approximations; no winding-turn count is asserted. Each body stands on three
  uniform .80 porcelain post instances and individually height-set steel stands.
- B09_DISCHARGE_MASTER has a rounded tank profile with three short triangular-arranged
  terminal instances. Angles/dimensions are photo-guided approximations.
- New strips use observed visual colors without assigning A/B/C phase IDs or claiming
  full electrical topology. Source P05 rack links remain visible approximation modules.
- Four incoming post positions follow coarse peaks about 1.2 m apart. The bridge/legs are
  exterior placeholders; the switching mechanism and second-row internals are not completed.

Scene 60_B09_EDIT_031_LOCAL contains #1 local arrangement. B09_031_LOCAL_ASSEMBLY,
B09_032_LOCAL_ASSEMBLY and B09_033_LOCAL_ASSEMBLY hold independent poses, instantiated
at rigid site roots. Class edits in the main file affect all corresponding instances.
The standalone local asset opens into scene 60 with 1,560 meshes and matches saved main
geometry. It is an independent Append/edit file, not externally linked back into the station.

## Validation and limits

Saved geometry, uniform source class scaling, paired terminal orientation, 27 reactor
post contacts, candidate camera framing and historical preservation pass. Twelve PNGs
were rendered on the workstation GPU and verified for size/readability/nonblank pixels.

Reactor sampling gates and alternating 45-degree train/heldout sectors were selected
before fitting. A shared radius is the median of nine training fits. All heldout residuals
are retained. The checks concern only radial cylinder-face distance, not survey accuracy,
full equipment matching or electrical clearance. Rack-back distances use fit points and
are explicitly diagnostics, not independent holdouts.

| Bank / lane | Held-out triangles | Median absolute / m | P95 / m |
| --- | ---: | ---: | ---: |
| 031 / 1 | 69 | 0.0046 | 0.0247 |
| 031 / 2 | 67 | 0.0036 | 0.0313 |
| 031 / 3 | 85 | 0.0051 | 0.0192 |
| 032 / 1 | 85 | 0.0072 | 0.1157 |
| 032 / 2 | 82 | 0.0047 | 0.0218 |
| 032 / 3 | 76 | 0.0049 | 0.0218 |
| 033 / 1 | 66 | 0.0042 | 0.0248 |
| 033 / 2 | 68 | 0.0272 | 0.0704 |
| 033 / 3 | 73 | 0.0083 | 0.0939 |

## Pending and next work

1. Model the visible side stepped bus supports and complete incoming switch exterior;
   trace their routes from coarse/photos. This batch intentionally stops at the four
   incoming supports, without inventing switch state or connectivity.
2. Resolve small arrester foot offsets and discharge terminal details. Pad locations and
   dimensions are coarse-relative, not measured. Hidden tank connections remain unassigned.
3. Refine adjacent #1/#2 shared fence boundary, gate hardware and exact mesh pitch.
   Wire mesh pitch .12 m is illustrative. Each bank footprint stays rectangular.
4. Inspect 032 lane 1 P95 .11575 m and 033 lane 2 median .02719 m; do not erase tails or
   independently deform shared manufactured classes to hide mismatch.
5. Proceed to #4/#5/#6 only with each bank identity and pose checked. A shared inventory
   model alone does not authorize blanket site placement or fine count acceptance.
6. Preserve all B08 notes, shared transformer geometry and B06 wall calibration. Continue
   GIS longitudinal review / arrester mounting failures in subsequent bounded batches.

Scenes 47/48 station clean/overlay; 49–51 #1 clean/overlay/reference; 52–54 #2;
55–57 #3; 58 vertical orthographic top overlay; 59 group view; 60 editable local #1.
All overlays and reference pairs use the same cameras. Source context outside the crop
may be clipped; no reference image is generatively edited.
