# Continue from B10 — six capacitor banks and whole-outdoor audit

Active user objective: 请持续进行变电站建模任务，直到室外设备大都实现建模与对齐。
Keep this goal active. B10 is concrete progress, not completion of the objective.
Do not call update_goal complete based on candidate counts or these narrow checks.

Latest station: output/installation_B10/site_B10_capacitor_banks.blend
SHA256: bfc18cd99b6db6f54d47b9a1434488ba34e69ba9965043fe03462658e4b43a87
Default scene 81_B10_Six_Banks; full station 61_B10_Station_Clean.
Review: output/installation_B10/B10_review.html (21 embedded actual renders).
Editable local #4 bank: output/installation_B10/B10_capacitor_editable.blend.
Queue: asset_variant_installation_queue_v10.json. CURRENT.md mutable, historical snapshots frozen.
Full outdoor inventory: output/installation_B10/B10_outdoor_coverage.json and .md.

## Goal audit and next action

The saved station has more geometry than has been reviewed for pose/fidelity. The audit
reads every official record and actual direct/candidate objects in scene 61. Its statuses
are evidence tiers, not completion percentages: {"transformer_major_exterior_alignment_reviewed": 2, "previously_classified_indoor": 23, "bank_major_exterior_alignment_reviewed": 6, "legacy_geometry_pose_review_pending": 77, "unresolved_outdoor_or_mixed": 26, "legacy_major_fit_record_needs_current_visual_review": 3, "partial_candidate_present": 1, "arrester_body_mount_reviewed": 12, "arrester_candidate_mount_unpassed": 3}.
Records mix individual phases, complete bays, bus names and station-wide infrastructure.
Do not exclude unresolved outdoor records or divide a candidate count by 153 to claim
completion. Inferred dimensions and unseen small internal details do not themselves block
the user's exterior modeling objective; major visible forms and independent poses do.

Next priority: remaining VC-A arresters (751/758/759 and T1/T2 medium-voltage side; exact 15 IDs in B10_next_arrester_targets.json),
then VC-A GIS outgoing/spare bay longitudinal arrangement and different exterior variants.
Repair existing 748-B/746-A/B mounting errors. Review VC-B legacy major fitted bays versus
unverified repeated family templates; resolve neutral and aggregate infrastructure mapping.
The coverage file records 77 legacy geometry records needing review, 3 older major-fit
records needing current visual review, and 26 unresolved outdoor/mixed mappings.

## This batch

Added #4 / 034 / 12MZ0000000242513, #5 / 035 / 12MZ0000000242511, and
#6 / 036 / 12MZ0000000242509 with independently fitted rigid site frames and component poses.
Also generated updated downstream #1/#2/#3 assemblies, preserving every B09 object and scene.
Each of six banks contains 3 racks, 3 reactors, 3 discharge tanks, 3 small arresters,
4 side stepped supports, incoming support structure, visible operator linkage, and modeled
external strips. There are 18 rack-to-primary terminal connections checked against saved
source geometry. Complete circuit/phase labels and switch operating state remain unassigned.

New original full-resolution views: DJI_20260825145433_0032_V (#6 foreground),
DJI_20260825145438_0033_V (#5 and #6), DJI_20260825145454_0036_V (#4 and #5).
All originals viewed directly, no generated/cropped photo substituted. Sources/hashes in plan.
These views show tall primary bushings above discharge tanks; B09's three short plugs had
not represented them. B10 adds three larger primary bushings and keeps small front plugs
separate. Angles ±18/0 degrees and uniform .95 post-source scale are exterior approximations.
The photograph's three colored visible positions are reflected without assigning A/B/C.

P05 manufactured can, steel rack, post and arrester geometry is unchanged. B10_RACK_ASSEMBLY_PHOTO
reuses those structures and four terminal rails, omitting the old removable top/down routes
so independent B10 strips can be attached. B09_REACTOR_BODY_MASTER is reused unchanged by
all six banks. Each bank has independent local poses, each site root remains rigid scale 1.
T1/T2 still share B08_TRANSFORMER_MASTER exactly as explicitly authorized by the user.

Incoming rows follow their source crops: 8 visible supports in 031/032/033/036 and 7 in
034/035 (first back-row position has insufficient source evidence, so not filled by copying).
These are modeled counts, not a claim of confirmed physical absence. Four progressively
lower side supports per bank follow separate small-source patches, with approximate feet.
Input and side/front strip paths express visible exterior routes only; hidden junctions and
mechanical operating details remain unresolved. Source support dimensions are uniform per class.

## Plan and provenance

Use B10_plan_r2.json. It combines frozen B09 poses for 031–033 and B10_new_bank_plan.json
for 034–036. Later r2 excludes third-row lead fragments from incoming support clustering
and keeps four distinct X stations, avoiding a collapsed 036 column cluster in r1.
036 negative-X fence initially picked the adjacent building wall. The plan records the
superseded plane and selects the observed inner fence plane consistent with about 8m
spans in the five other banks. All footprints stay rectangular.

Original 031–033 coarse files remain in installation_B09; new 034–036 crops in installation_B10.
Each NPZ has source-frame vertices, triangle centers/normals and frame_to_world; matching
reference_origins.json identifies every source tile and original triangle. Use
inverse(final_frame) @ reference.frame_to_world to compare with new local geometry.
Per-family proportions are not individually stretched to conceal pose residuals.

## Saved checks

Preserved 22641 previous objects, 263 collections,
45 scenes, 279 materials, 15,096 v50 components,
69 B06 civil meshes and 498 previous files. The additional 3,852 legacy meshes
of 034–036 are omitted only in B10 scenes; original 031–033 B09 site collections are
superseded only there. New station retains 6,643 original tagged direct component meshes.

Expanded mesh counts: {"031": 1771, "032": 1771, "033": 1771, "034": 1756, "035": 1756, "036": 1771}. New authored objects: 939 meshes and
244 instance empties including roots/nested classes. Shared source P05 objects: 119 unchanged.
54 reactor post contacts, 24 side supports and 54 discharge primary bushing instances
are present. All saved source scales are uniform. Rack downstraps meet actual primary
mesh top centers within 0.000000546 m (numerical attachment
check, not measured accuracy). The editable standalone #4 opens directly into scene 83
and has 1,756 expanded meshes matching the station's local assembly; it is not externally
linked back to the station file. All 21 rendered PNGs pass size/read/nonblank checks.

Reactor holdouts retain alternating 45-degree sectors selected before circle fitting;
shared radius remains the frozen B09 class radius. Only cylindrical radial distances are
checked, not entire-device accuracy. Rack back-plane measurements use fit points and
are explicitly diagnostics, not independent holdouts. Do not hide residual tails.

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
| 034 / 1 | 48 | 0.0062 | 0.0569 |
| 034 / 2 | 49 | 0.0074 | 0.0195 |
| 034 / 3 | 74 | 0.0064 | 0.0255 |
| 035 / 1 | 61 | 0.0075 | 0.0482 |
| 035 / 2 | 30 | 0.0243 | 0.0517 |
| 035 / 3 | 30 | 0.0149 | 0.0242 |
| 036 / 1 | 68 | 0.0083 | 0.0307 |
| 036 / 2 | 72 | 0.0067 | 0.0330 |
| 036 / 3 | 79 | 0.0139 | 0.0337 |

Unresolved close-detail concerns include small tank/arrester feet, terminal angles, side
support roots, front-pad clearance especially 036, shared fences/gates, and fine switch
mechanics. 032 lane 1 retains P95 .11575 m; 033/035 partial-reactor surfaces also have
larger tails. These do not justify changing frozen classes independently for each unit.
Whole-equipment mechanical/electrical acceptance is not asserted. Formal promotions zero;
queue has 24 working equipment candidates, including a partial GIS cabinet and 3 failed
arrester mounts. This is not a complete-outdoor count.

## Views

61/62 station clean/overlay; 63–65 #1, 66–68 #2, 69–71 #3, 72–74 #4,
75–77 #5, 78–80 #6, each clean/overlay/reference. 81 six-bank group; 82 true
vertical orthographic #1 top overlay; 83 local editable #4. Reference pairs share cameras.
Historical 45 scenes are untouched. New station has 68 scenes total.
