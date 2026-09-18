# B01 749 arrester small-batch installation trial

All paths below are relative to experiments/blender-substation/photo-first-pilot.
User goal: outdoor equipment assets from photos and inventory first, installation second.
Do NOT turn a coarse-reference residual into permission to distort asset-local geometry.
This turn moved from five isolated prototypes to three real-world-coordinate candidate instances.

## Saved deliverables

- output/installation_B01/P02_B01_749_installation_review.blend
  SHA256 2d06f288a3da6ca2170025814438fadcaa7009200b500ddd2a1a355fde0edb0e
- output/installation_B01/B01_validation.json: software/immutability QA passed.
  IMPORTANT: alignment_screen_passed=false, formal_promotion=false.
- output/installation_B01/placement_B01.json: only common scale and per-instance rigid poses.
- output/installation_B01/release_B01.json: hashes of model, code, evidence and queue.
- output/installation_B01/B01_result.md: Chinese result summary.
- output/installation_B01/B01_reference_model_comparison.jpg: same-camera source/clean/overlay.
- asset_variant_installation_queue_v2.json: additive queue, previous v1 retained.

Formal station remains semantic v50, all five photo-first assets are unchanged.
No newly promoted official equipment, no inspection-point mapping update.
152 protected original/release files were checked before and after the work.

## What was instantiated

Frozen source output/P02_r1/P02_SA-A_photo_first.blend, SHA256
1df8ba4ec1fcaca62d985bddfe3f4dcaac493af7879effda4981feef53dc385b.
Source has 67 authored objects across BODY38 / PEDESTAL17 / ACCESSORY7 / LOCAL_LEAD5,
using four primitive Mesh datablocks. All 67 original geometry hashes, local matrices,
material slots and modifiers were checked. The trial includes BODY+PEDESTAL ONLY:
55 objects per physical candidate, 165 evaluated objects in each metric scene.
Original 67-object demo remains in scene 01 with the original accessory display.
Do not count its accessories as field-installed modules.

The three trial candidates inherit inventory identities, not new nameplate certification:
- B01_749_A / 12MZ0000000150127 / 兴盛I749避雷器A相
- B01_749_B / 12MZ0000000150128 / 兴盛I749避雷器B相
- B01_749_C / 12MZ0000000150129 / 兴盛I749避雷器C相

Scene instance objects carry candidate_device_id, not official device_id.
They do not change the official roots or source registry. Cylindrical body/pedestal
geometry is shared, not independently rebuilt. One common scale is used for all
three and for both included modules: 1.1461626865312622 m/H, an estimated registered-
reference scale, NOT survey calibration. H itself remains unscaled in the source asset.
Three independently inferred scale ratios vary by about 0.2835%; no per-device scaling.

Estimated axes:
A (26.08476413368603, 15.277855060304063)
B (25.213802174491413, 17.087595350635702)
C (24.340262192771753, 18.88326979694424)
Relative XY corrections to old manual boxes are approximately 1.9,9.7,4.5 cm.
Per-candidate vertical translation uses its own foot surface; top mounting levels
and top-disk envelope are independently compared after the shared-scale placement.
Azimuth remains the old station-axis candidate (3.5360370645405115 rad), not an
independently measured top-lug or label orientation. Do not imply full 6D pose certainty.

## Source and photo evidence

installation/prepare_B01.py freezes sources and reads inventory and four photo regions.
installation/extract_B01.py extracts 29,897 vertices /57,281 triangles from original
registered photo_workbench. No source blend is saved. Original tile/triangle indices
are in B01_reference_origins.json; numerical data in B01_reference.npz.
Target-only overlays select 12,684 triangles within radius0.55m of three axes,
height[-0.15,4.38]; full context is also available separately. Do not claim this crop
is an independent segmented ground-truth mesh or a complete field dataset.

Outer0014 and0011 show the three vertical apparatus bodies beside the749 GIS;
inner0053 provides the749 cabinet context and two matching vertical apparatus;
inner0051 has only one relevant label and is NOT a relative-order test.
Three images have matching horizontal order using approximate old cameras.
This verifies order only, not precise camera reprojection, identity by new nameplates,
or all30 Y10W2-102/266 records sharing the same variant.
See B01_visual_and_identity_review.json: the fourth image is not_testable_single_label,
not a contradictory order. Older placement report represents it as false due to a
minimum-two-label condition; do not misread that as a failed correspondence.

## Screen result — PRESERVE THE FAILURE

Selected mounting heights are close without asset deformation, but the original
broad support-source held-out sample contains accessory protrusions/irregular coarse
surfaces. Reference cylinder heldout RMS:
A 0.0484411931m (local screen pass), B0.0731742786m (fail), C0.0509813358m (fail).
The explicit pilot RMS screen is0.05m, not an industry standard. Batch screen FAILS.
Top disk height residuals are +0.0274,+0.0910,+0.0390m. Pedestal plate residuals are
-0.0267,-0.0330,-0.0390m. These are reconstruction comparisons, NOT field accuracy.
The failure has NOT been relabelled as a success. Do not raise the threshold merely
to promote. The physically reasonable placement can be used for further review
without pretending it is a final accepted installation.

The source round accessories and local lead routes exist; absent from B01 trial
because independent attachment positions are unresolved, NOT scope_excluded.
The P01 original R01 spacing failure also remains unchanged.

## Blender scenes / visual output

01_FROZEN_P02_ASSET_H: normalized original demo; not metres.
02_B01_WORLD_CLEAN: default, three candidates in registered estimated metres.
03_B01_TARGET_COARSE_OVERLAY: same candidates plus explicit target reference crops.
04_B01_749_COARSE_CONTEXT: larger original context, wall and nearby GIS included.
Clean/overlap/context share the same six BODY/PEDESTAL collection-instance objects.
No independent display re-copy is used to claim placement success.

Actual output includes oblique/front/top clean and overlay renders. The montage's
colored overlay was rendered read-only with transient INSTANCE display colors because
collection source object colors alone were ineffective. Model file was not resaved;
its saved overlay may appear gray. This is only display color, not material or geometry.

## QA and processing state

installation/validate_B01.py reopens the saved file, checks source release hashes,
all67 geometry/local matrices, source material slots/modifiers, six equal uniform
module transforms, three scenes x165 evaluated components, source crop vertices/
faces, actual plane/contact diagnostics, nonuniform instance deformation rejection,
camera framing and152 protected inputs. Max evaluated matrix error about9.6e-7.
QA status=passed certifies software workflow, NOT all-surface alignment or field count.
No source model is saved during validation or presentation rendering.

No active Blender batch job remains at closure. Interactive GUI file not switched.
All paths are remote Cyborg project paths; do not fabricate local sandbox links.
Git worktree historically unavailable; use source hashes and no claim of git clean.

## Next actions

1. Review the B/C reference sample at accessory heights and compare the photo regions;
   separate physical pole faces from attachments with explicit source indices. Keep
   original broad sample and residuals for comparison. Do not shape-deform the P02.
2. Confirm accessory/bracket presence and orientations per candidate; create separate
   attachment transforms only after evidence review. Do not recreate unseen wires.
3. Keep current trial as immutable diagnostic. A later revised installation report or
   station integration candidate must point to this frozen source and revised evidence.
4. Avoid blocking the entire project on sub-centimetre coarse agreement; maintain
   distinct visual-acceptance, scale/pose-uncertainty and official-promotion states.
   Additional photo-reviewed subsets can use the same downstream pipeline.
