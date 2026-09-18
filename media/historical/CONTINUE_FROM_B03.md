# B03 r2 — six neighboring photo-first candidates added to cumulative station preview

All paths below are relative to experiments/blender-substation/photo-first-pilot.
User wants outdoor equipment from identity/photos first, installation second. Frozen
P01-P05 shape files must not be distorted to fit coarse data. Show concrete progress
and real renders during work. Original formal station remains semantic v50.

## Current deliverables

- Full station: output/installation_B03/r2/site_photo_first_B03_station_preview.blend
  SHA256 04a5974dca2a04e3134915e7f76f2aea47c58b46e8b46faead7508dd29c5c2fc
  734,770,677 bytes. B03_station_validation.json passed (software/integration scope).
- Local six-target review: output/installation_B03/r2/P02_B03_748_747_installation_review.blend
  SHA256 f87fbd4827f256ade8598451255247174fd3a9fdc4a10aa613cf76b89b1b9657
  4,524,255 bytes. B03_validation.json passed (source/pose/reuse scope).
- Frozen release: output/installation_B03/r2/release_B03.json, hashes for26files.
- Final poses: output/installation_B03/r2/placement_B03.json.
- Candidate queue: asset_variant_installation_queue_v4.json (old v3 unchanged).
- Real same-camera contact: output/installation_B03/r2/B03_reference_model_comparison.jpg.
- Whole-station render: output/installation_B03/r2/B03_station_overlay.jpg.

## What changed

Two more groups: 平兴II748 A/B/C and 东坡I747 A/B/C. IDs:
748 A/B/C: 12MZ0000000150102 / 12MZ0000000150103 / 12MZ0000000150104.
747 A/B/C: 12MZ0000000150077 / 12MZ0000000150078 / 12MZ0000000150079.
They remain inventory/photo-order candidates, not independently read phase nameplates.
Raw outer0014/0015/0011 contacts support slender vertical insulation body, cylindrical
pedestal and upper side accessory. All six group/image horizontal-order checks match
under approximate existing cameras, NOT calibrated absolute reprojection.

Six BODY+PEDESTAL assemblies use frozen P02 r1, same1.1461626865312622m/H scale as
B02 (estimated, NOT surveyed). No asset-local matrices, dimensions or vertex positions
changed. Per-target rigid positions are independent; top-lug azimuth remains inherited.
Five independent ACCESSORY poses; 748-B accessory omitted as pending, never scope_excluded.
No local cable route or full overhead leads copied.

Cumulative preview has previous B02 749three + new B03six = NINE candidate equipment.
All9 reference the exact same BODY/PEDESTAL/ACCESSORY source collections in the new
station file; no additional append with duplicate geometry was used. Previous B02
instance matrices are checked unchanged. New17moduleinstances evaluate to365components;
previous9modules evaluate to186; cumulative551candidatecomponents.

## Important unpassed screen and draft history

Mounting protocol was frozen in installation/prepare_B03.py BEFORE new coarse extraction.
Bare-shaft train z1.0-1.65m, validation1.75-2.10m, radius.45m, normal/area gates same
as B02. NO residual trimming of validation. Same0.05m pilot shaft criterion; NOT standard.
Fixed scale inherited B02, individual foot translations only. Foot RMS limit.03m,
body-base height limit.12m, top-fitting limit.15m. All24azimuth bins represented.

Frozen model validation RMS for748A/B/C: .0325413/.0512417/.0283585m.
747A/B/C: .0256496/.0292992/.0251154m. Five pass bounded mounting checks; 748-B FAILS
(5.124cm>5cm). It remains visible but amber in the local coarse overlay and explicitly
marked unpassed in data. Do not relabel as full geometric acceptance or weaken criteria.
B01 original broad-domain failure and P01 R01 spacing failure remain untouched.

First B03 proposal/draft in output/installation_B03 (without /r2) had six accessories.
Its independent readback caught748-B bracket tip penetrating modeled pole by.089829m,
exceeding.08m structural screen. Correcting it would exceed.035m bounded placement
translation. r2 therefore OMITS that accessory, not modifies its mesh or relaxes screen.
All five remaining mounts pass. See r2/revision_decision.json. Original failed draft,
original six-accessory proposal and original builder/validator retained; not releases.

## Four Scenes in latest cumulative station file

07_Full_Station_Semantic_v50 — original15096 tagged objects preserved unchanged.
12_Photo_First_B03_Station_Clean — cumulative working clean.
13_Photo_First_B03_Coarse_Overlay — DEFAULT, same candidates plus23originalcoarse tiles.
14_Photo_First_B03_Local_Detail — new six-target context, same B03 objects as full views.

Working full scenes retain14916original objects shared with baseline, exclude exactly
180oldcomponents corresponding to9targets (120newly omitted this turn), and add551
candidatecomponents, totaling15467equipmentMesh instances. Official roots/registry and
inspection mappings NOT rewritten. Old untagged 'DT neutral ground' presentation plane
is omitted only from working views as in B02r2, preventing source ground occlusion.
Old B02preview Scenes removed from this NEW file to keep4Scenes; original B02file intact.
No interactive Blender GUI was switched. User must open the new file to see changes.

## Code / preservation

installation/prepare_B03.py: 196protected input hashes, six selected photo crops and protocol.
installation/extract_B03.py: read-only original coarse, 44185vertices/84297triangles,
explicit tile/triangle mapping in B03_reference_origins.json. Original coarse not saved.
installation/fit_B03.py: downstream poses, footprint/top datums, attachment hypotheses.
installation/build_B03.py / validate_B03.py: retained draft; fails748-B accessory check.
installation/revise_B03.py: SHA-pinned source generation, omits uncertain attachment.
installation/build_B03_r2.py / validate_B03_r2.py: accepted saved-file local QA.
installation/build_B03_station.py / validate_B03_station.py: cumulative preview + readback.
installation/release_B03.py: release and additive queuev4, no overwrites permitted.

Both final validations independently reopen output. They check source geometry/hash,
local transforms/materials, global uniform scale, same-instance reuse, original baseline
fingerprint from B02, old B02poses,23coarse tiles, unpassed/pending flags, and196protected
files. Local validation includes nonuniform distortion detection/restoration and saved
camera framing. No manufacturer CAD, full surface/phase identity or survey claim.

## Next

Continue another independently photo-reviewed subset, e.g.夏津746 or备用陆750.
Do not regenerate current batches or fit manufacture components to coarse noise.
Keep prior nine candidates when advancing the cumulative preview. Record failed screens
and omitted accessories without blocking all other equipment. After extending the row,
return to an already authored major family for first controlled installation, rather than
spending every turn on small fasteners. Official semantic mapping is a separate explicit
step; candidate previews must not be silently used as inspection-label ground truth.

All B03 build/readback processes exited normally before handoff; no active save task.
Remote Cyborg paths are not local /mnt/data links. Git worktree historically unavailable;
use recorded file hashes, never claim git clean.
