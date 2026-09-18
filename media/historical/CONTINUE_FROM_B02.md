# B02: photo-first models now available in a full-station working preview

Paths below are relative to this photo-first-pilot directory. Continue photo/identity-driven asset authoring; coarse geometry is downstream installation evidence only. Do not distort frozen manufactured shapes. Give intermediate progress and real renders.

## Latest files

- Full-station working preview: `output/installation_B02/site_photo_first_B02_station_preview_r2.blend`.
- Full preview SHA: bf3d0dc5c62434f19dda3d828bd69ce1eacae191a0e7fde007d75e20ae11ea36.
- `output/installation_B02/B02_station_preview_r2_validation.json`: passed, integration/immutability QA, NOT formal semantic promotion.
- Small local review: `output/installation_B02/P02_B02_749_installation_review.blend`.
- Local SHA: d358d69acd5fbc82618841bc580267ce1c8068bd33c7b906233dcddd600bd567.
- `output/installation_B02/B02_validation.json`: passed, scoped shaft/mount and frozen-shape QA.
- `output/installation_B02/release_B02.json` pins current files; do not rerun builders on frozen outputs.
- `asset_variant_installation_queue_v3.json`: three working-preview candidates, formal installed/promoted count remains zero.
- Actual same-camera before/after: `output/installation_B02/B02_before_after_comparison.jpg`.
- Whole-station final render: `output/installation_B02/B02_station_r2_overlay.jpg`.
- Formal original remains semantic v50; all five P01-P05 photo-first samples remain untouched.

## Actual changes

The 749 arrester A/B/C candidate identities remain inherited from inventory and photo-order association, not newly surveyed labels. Three BODY+PEDESTAL placements reused frozen P02 r1. All67 source object-local transforms, geometry and material slots remain unchanged, shared sourceMesh count4. Scale remains exactly B01's1.1461626865312622m/H estimate. New XY refinements relative B01 are7.71,4.81,8.63mm, not field accuracy.

Three ACCESSORY modules were independently posed. Presence supported by raw outer0014 and0011 cropped upper-support photographs; new images in output/installation_B02/B02_upper_attachment_photos.jpg. Small round accessories and upper cable loops are NOT bare cylindrical shaft surfaces. We did NOT add/copy LOCAL_LEAD: real routing is unresolved.

Accessory source surface patches were selected in row-relative t/f coordinates and z[2.25,2.50]m, recorded explicit triangle indices. Weighted patch plane/centroid guides orientation and position, but centroids are NOT certified dial centers. Type/reading remains unknown. C candidate required1.568cm rigid translation to bring frozen bracket arm into its pole; original proposal retained in placement_B02.json and final mounting-consistent poses in placement_B02_r2.json. No accessory scaling or source mesh change. A/B original patch poses unchanged. All3 bracket tips now overlap pole model by5-25mm. These are exterior assembly consistency checks, not certified clearances.

## Distinguish the two checks

B01 broad cylindrical selection included protruding attachments/cables. Keep old B01 failure exactly as is (broad heldoutRMS~4.84/7.32/5.10cm). B02 only checks bare-shaft spatial domains: train z1.0-1.65m, validation z1.75-2.10m; same radius/normal/area gates; NO residual trimming of validation faces. Validation sets144/168/160 triangles, frozen modelRMS~1.81/3.42/3.30cm below unchanged5cm pilot screen. These are different domains and cannot be presented as apples-to-apples accuracy improvement. Domain chosen after residual diagnosis, not a blind benchmark. All previous broad indices and new-axis-on-old-broad results remain in final proposal.

SoftwareQA and new scoped shaft check pass. Full exterior/identity/metric accuracy is NOT certified. Accessory poses approximate, terminal azimuth inherited, wires pending. Do not let a pass field imply whole equipment or full station completed.

## Full station integration

Full r2 preview has four Scenes:
- 07_Full_Station_Semantic_v50: original15096 tagged component objects unchanged.
- 09_Photo_First_B02_Station_Clean: working clean scene.
- 10_Photo_First_B02_Coarse_Overlay: default, working scene plus original23coarse tiles.
- 11_Photo_First_B02_Local_Detail: local context from B02.

The working scenes omit exactly60 old components (20 per749arrester). All other15036 tagged objects are shared with the original baseline Scene, unchanged in geometry/materials/world transform/parent. Add9 frozen module instances yielding186 candidate meshes (=3x62). Working equipment total15222, NOT new official devices. Candidate instance collection B02_PHOTO_FIRST_749_CANDIDATES is shared by all3preview scenes. Objects use candidate_device_id, not new official device_id. Original registry and patrol mappings were NOT rewritten; do not feed preview replacements to official semantic exporters without mapping work.

r1fullpreview is retained as validated integration draft. r2 only excludes the old untagged `DT neutral ground` presentation mesh from the working-preview collection because it hid portions of actual registered ground. The original baseline Scene retains that plane; coarse vertices unchanged. Default r2file is the usable deliverable.

## Code and verification

installation/inspect_B02.py, render_B02_evidence.py: source bands and photo/source crop diagnosis.
fit_B02.py: independent shaft pose and approximate accessory planes; close_B02_mounts.py: bounded mount-only translation.
build_B02.py / validate_B02.py: small review and standalone independent readback.
build_B02_station_preview.py / validate_B02_station_preview.py: non-destructive whole-station preview and baseline fingerprint.
revise_B02_preview_display.py / validate_B02_station_preview_r2.py: final display-only fix and independent readback.
render_B02_before_after.py: transient B01/B02 instance poses under identical camera; never saves model.
release_B02.py: release and additive queuev3. 170protectedpriorfiles verified; release pins24currentfiles.

Recoverable implementation issues fixed before release: Pillow default font could not draw Chinese crop suffix (ASCII labels used); Blender shading enum is OBJECT, not INSTANCE (color the instance objects); Blender Python lacksPillow (compose contact with systemPython). Failed first runs did not overwrite any frozen asset. No remaining render/build/save job at closeout, no interactive GUI file switched. Git worktree unavailable; do not claim git clean. Remote Cyborg paths are not sandbox paths.

## Next batch

Use this full-station working-preview mechanism to expand a photo-reviewed subset of neighboring same-family arresters, e.g.748A/B/C after checking inventory and raw photos. Preserve B02 and all frozen assets. Confirm body/pedestal/accessory variant per target; no blanket copy to all30records. Keep localwire/terminalazimuth work as explicit pending fields rather than blocking all other equipment on fine reference noise. New whole-station working preview should preserve the unchanged v50 Scene and already reviewed B02instances. Resolve official mapping separately before calling anything a new formal semantic version.
