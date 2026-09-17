# §7.3 Evidence Map — Persistent state as composition mechanism and risk surface

## Status and purpose

Working evidence map for the B01–B36 rewrite. This supports C3 and should be drafted only after §7.2 is stable.

Canonical C3 claim:

> Later B01–B36 batches explicitly consume and preserve earlier masters, transforms, ports, endpoints, and accepted geometry. Persistent external engineering state is therefore the documented mechanism by which local reconstructions compose across batches. The same inheritance makes errors in shared abstractions consequential until the representation is revised.

This is a mechanism description of the preserved record. It is **not** a controlled claim that persistence improves accuracy, efficiency, or success rate.

---

# 7.3 opening paragraph

## Function

Answer the reader's likely question after §7.2: if later tasks depend on earlier geometry, what actually carries those dependencies across batches?

## Narrow claim

The long horizon is implemented through explicit external engineering state, not by treating each batch as a fresh generation task. Later batches reuse previously saved geometry, collection masters, transforms, terminals, and connection endpoints, while validators check that inherited state remains unchanged.

## Evidence

Use the explicit dependency chain:

`B08 transformer master/ports → B23 transformer-connected leads → B29 overhead conductors using prior endpoints → B36 bus-rack closure tied to B08 stubs`

Use preservation checkpoints only as secondary evidence.

## Boundary

Do not claim persistent state is necessary in general, improves accuracy, or is better than a stateless alternative. No stateless control exists.

---

# Paragraph 1 — B08 establishes reusable external state

## Function

Show the first concrete state object that later batches can address rather than recreate.

## Claim

B08 stores transformer geometry as a reusable master with rigid site instances and separate site-specific leads, creating explicit component and terminal state that later reconstruction can reference.

## Evidence

`photo-first-pilot/CONTINUE_FROM_B08.md`

- lines 21–28: `B08_TRANSFORMER_MASTER`; T1/T2 site roots share it; site leads live in separate collections;
- lines 55–60: independently traced leads meet modeled terminal centers and stop at the last observed locations;
- lines 70–75: T2 receives only rigid correction; no per-site shape deformation;
- lines 92–104: large prior scene state preserved; terminal/contact checks retained.

`output/installation_B08/B08_validation_r2.json`

- lines 8–20: 21,459 original objects, 228 collections, 18 scenes, 256 materials preserved; one shared master, two rigid roots, shared edit propagation checked;
- lines 31–35: site conductors independently traced, terminal max error ~2e-6 m, asset export geometry identical.

## Development

The significant state is not the object count itself. It is the existence of stable, addressable geometry and interfaces that later operations can consume.

## Boundary

The shared transformer configuration was explicitly human-authorized. The state is a modeling construct, not a certified manufacturer CAD assembly.

## Bridge

B23 demonstrates direct reuse of a B08 terminal rather than reconstruction from scratch.

---

# Paragraph 2 — B23 consumes B08 terminal state while preserving history

## Function

Show a downstream geometry operation terminating on an earlier batch's modeled interface.

## Claim

B23 constructs the transformer neutral lead against an existing B08 terminal port and preserves the inherited transformer geometry and broader scene state.

## Evidence

`photo-first-pilot/CONTINUE_FROM_B23.md`

- lines 9–11: 28,246 old objects and 3,301 current-station old object world transforms preserved; B08 transformer master remains in use;
- lines 15–19: curved neutral lead endpoint is the existing `B08 front_small` terminal port; parent/collection transforms are re-evaluated in validation;
- lines 29–33: endpoint/cross-section checks are explicit and separate from local surface domains.

`output/installation_B23/B23_validation.json`

- lines 5–15: 28,246 previous objects, 461 scenes, 598 collections, 323 materials and 2,192 protected prior files preserved;
- lines 20–23: B23 adds shared masters without replacing B08;
- prior station transforms remain unchanged.

## Development

This is direct cross-batch composition: the downstream path is defined relative to an earlier modeled terminal. Rebuilding the transformer is unnecessary because the prior interface has become part of the state.

## Boundary

This is internal model continuity, not independent field verification of the terminal position.

## Bridge

B29 expands the same pattern from one local connection to many conductors terminating on previously modeled subsystems.

---

# Paragraph 3 — B29 composes across multiple prior subsystems

## Function

Demonstrate that inherited-state use scales beyond one local dependency.

## Claim

B29 connects new overhead geometry to existing strain/suspension structures and transformer-derived lead endpoints while preserving the prior scene.

## Evidence

`photo-first-pilot/CONTINUE_FROM_B29.md`

- lines 7–11: new strain strings, U-jumpers and main conductors; main conductors terminate on B29 fittings and existing B08/B27-derived transformer lead ends; existing equipment is not replaced in the full station;
- lines 13–17: 31,379 old objects, 569 old scenes, 706 old collections, 340 old materials and 5,308 station object transforms preserved; 84 conductor endpoint checks and 24 main-span interfaces remain below 2e-5 m;
- lines 23–27: future terminal planning is derived from actual saved equipment terminals and parent-aware geometry.

## Development

The reconstructed system now has a growing graph of addressable attachment points. Later tasks are defined relative to these interfaces instead of only to the photogrammetric reference.

## Boundary

The record does not certify full electrical topology, and local source-surface residuals remain imperfect in regions containing branches or missing geometry.

## Bridge

B36 provides the natural endpoint: a late bus-rack task closes onto B08 terminal stubs while preserving almost the entire accumulated station state.

---

# Paragraph 4 — B36 closes onto earlier endpoints under large-state preservation

## Function

Provide the strongest systems-scale evidence for C3.

## Claim

B36 adds new transformer-to-building bus-rack assemblies by connecting to inherited B08 terminal stubs and new wall interfaces while explicitly preserving earlier station state.

## Evidence

`photo-first-pilot/CONTINUE_FROM_B36.md`

- lines 3–5: new bus-rack structures added; B08 transformer assemblies remain shared and unchanged;
- lines 13–17: 36,615 previous objects, 731 scenes and 7,114 station-object transforms preserved;
- lines 19–25: final revision avoids an existing fire pipe while retaining endpoints/support route.

`output/installation_B36/B36_validation_r3.json`

- lines 4–14: 36,615 previous objects, 731 scenes, 827 collections, 392 materials, 7,114 station transforms, and 2,798 protected files preserved; final file contains 36,812 objects and 7,116 station objects;
- lines 23–26: shared main transformers preserved, new component masters shared, finite new geometry and asset roundtrip checks pass;
- lines 676–713: six new main busbars connect to existing B08 stubs and new wall bushings with saved endpoint gaps around 1e-7 m;
- lines 746–754: limitations explicitly record retained B08 terminal bars and local route reconciliation around fire risers.

## Development

The strongest long-horizon evidence is the cross-batch dependency and preservation contract, not the final object count. B36's update has to remain compatible with specific geometry inherited from B08 and with thousands of previously saved transforms.

## Boundary

Preservation counts do not measure the number of independently verified physical assets. Endpoint gaps are internal model consistency checks, not survey or electrical acceptance.

## Bridge

The same inheritance mechanism can transmit a bad abstraction. B15 provides the required counterexample.

---

# Paragraph 5 — B15 shows the propagation risk

## Function

Prevent C3 from becoming a one-sided "memory is good" claim.

## Claim

Persistent state also propagates representation errors when site-dependent geometry is embedded in a reusable abstraction.

## Evidence

`photo-first-pilot/CONTINUE_B15_IN_PROGRESS.md`

- line 21: common ±3.3 m bus-spool extent creates overlap across neighboring installations;
- lines 23–27: revision explicitly removes finite site-dependent spool geometry from the common master and reconstructs it in site wrappers.

`photo-first-pilot/CONTINUE_FROM_B15.md`

- lines 10–13: final representation shares body geometry while modeling neighboring pipe segments/supports separately;
- line 17: prior R1/B14 history is retained rather than rewritten.

`output/installation_B15/B15_validation_r3.json`

- lines 5–10: R1 state and protected files preserved;
- lines 28–134: corrected close and finite interfaces are checked after the representation boundary is revised.

## Development

The same mechanism that makes reuse powerful makes an upstream modeling assumption consequential. A wrong shared boundary is inherited by multiple site instances until the abstraction is corrected.

## Boundary

This is one documented propagation case. It does not estimate an error rate or prove a general memory hazard probability.

---

# §7.3 closing synthesis

## Function

State C3 once, then hand off to Discussion.

## Claim

AstraBuild's long horizon is implemented through a persistent, inspectable engineering world. Later batches consume earlier geometry and interfaces, and validators protect inherited state. This creates compositional leverage and an error-propagation surface.

## Interpretation

Persistence changes the reconstruction problem itself: later operations are constrained not only by external evidence but also by an already engineered world that must remain coherent.

## Boundary

No stateless control exists. Phrase as a documented mechanism in this sequence, not a comparative performance claim.

---

# Figure 5 evidence contract

## Left: dependency chain

`B08 transformer master/ports`
→ `B23 lead to B08 terminal`
→ `B29 conductors to prior suspension/transformer endpoints`
→ `B36 busbars to B08 stubs + wall bushings`

Each arrow must name the inherited object/interface used by the next batch.

## Right: preservation endpoint

Compact B36 state box:

- 36,615 previous objects unchanged;
- 7,114 previous station transforms unchanged;
- 2,798 protected files unchanged;
- final state: 36,812 objects, 7,116 station objects.

Caption must call these **state-preservation descriptors**, not physical asset counts.

## Inset: risk surface

B15 schematic:

`shared master with finite spool` → `overlap at multiple installations` → `revised master/site boundary`.

The inset should make the negative side of persistence visually explicit.
