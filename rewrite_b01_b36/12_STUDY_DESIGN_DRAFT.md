# 6 Study design

## 6.1 Sequential reconstruction record

We analyze B01–B36 as one sequential reconstruction record from an operating 220 kV substation. Later batches inherit accepted geometry, reusable assets, transforms, and validation state from earlier batches. The targets also change over the sequence: the early work focuses on local equipment and civil fitting, later work introduces repeated equipment families and explicit connections, and the final batches operate on residual civil and auxiliary structures within a large accumulated scene. Because geometry type, dependency structure, and task-specific validation differ across the sequence, we do not collapse all 36 batches into a single success-rate denominator. The analysis instead asks how the reconstruction operation changes as additional dependencies appear.

For orientation, we group the chronology into four descriptive bands. These bands summarize target structure and are not treated as discovered task regimes or as a common difficulty scale.

| Descriptive band | Batches | Representative targets | Structural issue introduced |
|---|---|---|---|
| Local fitted structures | B01–B06 | arresters, wall, gate | comparison domain, rigid pose, simple fitted geometry |
| Repeated equipment | B07–B19 | transformers, capacitor banks, 110/220 kV GIS | reusable components, variants, master/site boundaries |
| Connected systems | B20–B30 | busbars, insulators, jumpers, conductors | ports, routes, flexible paths, continuity, unexplained occupancy |
| Site closure | B31–B36 | buildings, cabins, ground, auxiliary facilities, bus racks | residual reconstruction under a large inherited state |

The grouping is used only to help the reader locate representative cases. The main Results section is organized by the claims supported by those cases rather than by the four bands themselves.

## 6.2 Evidence used in the analysis

The preserved record contains several forms of engineering evidence. Fixed-camera clean, overlay, and reference renders support visual comparison without changing the viewpoint between model and registered source. Local surface checks quantify scoped geometric agreement where a finite comparison domain can be defined. Connected-system validators add endpoint, contact, and continuity checks that are not reducible to surface distance. B25/B26 introduce selected-region coverage diagnostics for finding large unexplained structures, and late batches record preservation of inherited objects, transforms, collections, and protected files. These evidence types answer different questions and are reported with their local scope rather than combined into one station-wide accuracy metric.

The operator analysis in §7.1 is reconstructed from preserved stage/script artifacts and review records. In the B01–B36 catalog, `build` and `validate` appear in all 36 batches, while other named stages vary by target. We use this record descriptively to orient the longitudinal analysis. Absence of a named stage does not imply absence of reasoning, and stage prevalence is not treated as a performance measure. Mechanistic interpretations in §7.2 are instead grounded in direct artifacts such as measurement domains, reusable-master boundaries, port inventories, route plans, profile fits, coverage diagnostics, and collision/interference revisions.

## 6.3 Selection of main-text cases

The main paper does not give all 36 batches equal narrative weight. B01/B02 establish the local measurement problem; B08 and B15 expose the boundary between reusable and site-specific geometry; B20, B23, and B29 provide evidence from connected systems; B25/B26 use coverage of unexplained geometry as an additional signal for task selection; and B36 provides the clearest composition and interference example near the end of the sequence. B06, B17/B19, B31/B32, and B35 are used as corroborating visual or structural examples. The complete batch history, review pages, revision files, and task-local metric records belong in the supplement or website evidence browser.
