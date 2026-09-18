# Website preview

Run from the parent `astra-build` directory:

```bash
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/website/`.

The site has no framework/build dependency. `app.js` loads
`../release/metrics.json` when served over HTTP (the `#metrics-status` line reports
the result) and `../release/process_catalog.json`, which drives both the evaluation
console viewer and the batch-dossier appendix.

## Page narrative (aligned with the B01–B36 manuscript, `rewrite_b01_b36/22_FULL_MANUSCRIPT_FIGURE_V24.md`)

The site follows the manuscript "AstraBuild: From Local Fits to Persistent
Industrial 3D Reconstruction with a General-Purpose Reasoning Model". Scope is
B01–B36 only (36 batches); D37/D38 appear only as an explicitly labeled extended
record in the console. Section structure:

- Hero — title, bilingual abstract, headline facts (36 batches / 4 descriptive
  bands / 8 anchor batches / 3 contributions), links to
  `../rewrite_b01_b36/paper_layout_v24.pdf`.
- `#overview` — §1: Figure 1 + three contributions.
- `#method` — §2: division of labor, persistent loop `(E_t, S_{t-1}) → O_t → G_t → V_t → S_t`,
  B23 worked trace (`#method-trace`).
- `#study-design` — §3: Figure 2 longitudinal map, four descriptive band cards
  (B01–B06 / B07–B19 / B20–B30 / B31–B36), evidence description.
- `#results` — §4: 4.1 broadening operator portfolio (Figure 3), 4.2 three
  transitions (`#results-transitions`, Figure 4), 4.3 persistent state
  (`#results-persistence`, Figure 5).
- `#console` — §5: unified three-mode review viewer (below) + `#evidence-appendix`
  batch dossier browser.
- `#videos` — §6: two annotation-free videos.
- `#discussion` — §7: discussion + limitations.
- `#references` / `#sources` / `#citation`.

Figures: fig01/04/05 from `../rewrite_b01_b36/figure_v24/hybrid_svg/*.svg`,
fig02/03 from `../rewrite_b01_b36/figures/*.png`.

## Evaluation console (unified viewer)

Data source: `process_catalog.json` dossiers with a `review_page` (32 batches:
B07–B36 plus extended D37/D38). For each batch one representative view is picked
from `view_triplets`: the first non-station triplet with clean+overlay+reference,
else the first with clean+overlay, else the first with any image, else the first
loose view. Batches are grouped in the selector by band (repeated / connected /
site closure / extended). Three mode buttons (Model / Overlay / Coarse reference)
switch the single large image; modes missing an image are disabled. The original
Chinese `review.html` is linked per batch ("Original batch record") instead of
being embedded. `?review=B32` deep links are supported.
