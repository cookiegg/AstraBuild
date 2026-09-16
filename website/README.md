# Website preview

Run from the parent `astra-build` directory:

```bash
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/website/`.

The site has no framework/build dependency. `app.js` loads
`../release/metrics.json` when served over HTTP and falls back to the static metric
values embedded in the HTML if fetch is unavailable. `../release/process_catalog.json`
drives the review browser (32 historical review pages) and the 40-batch dossier
browser. Behavioral statistics quoted in the Summary and Findings sections come from
`../release/behavior_analysis.json` (mined by `scripts/analyze_process_behavior.py`)
and are embedded as static bilingual prose.

## Page narrative (aligned with paper v0.8)

The page is framed as a behavioral evaluation report with GPT-6 Astra as the model
under test and the harness (evidence compiler, Blender/Python action space,
deterministic validators, filesystem memory) as the method. Section structure:

- `#summary` — research question, protocol transparency, headline behavioral
  numbers (revision distribution 15/18/9, adaptation 4/2/1, 37,153 objects,
  3.6 cm* internal agreement), negative results first.
- `#model-harness` — §1: E1/E2/E3 taxonomy, harness components, protocol
  transparency, Figure 1.
- `#worked-example` — §2: B32 worked example, review protocol as instrument,
  canonical core + operator prevalence (40-dossier scope), Figures 2–4.
- `#tasks` — §3: the 12-family task suite (not an IID benchmark), evidence matrix,
  capability ladder, quantitative ledger with calibrations, Figures 5–6.
- `#behavioral-findings` — §4: findings F1–F6 with mechanism attributions and
  anchor links, Figure 7 (`fig14_behavioral_analysis.svg`).
- `#reviews` / `#gallery` / `#dossiers` — §5: the evaluation console (interactive
  review browser, station videos, dossier browser).
- `#cases` / `#d38` — §6: failure attribution (layer table) + episodes in
  trigger → diagnosis → revision → lesson form, Figures 8–9.
- `#integration` / `#semantics` — §7: system-level composition, version boundary
  (D38.2 / D40 / D41), semantic endpoint, Figure 10.
- `#discussion` — §8: supported / not supported / what would change the picture.
- `#scope` — §9: limitations; then references, resources, citation.

Large videos and D41 review renders are referenced by relative path so this draft
does not duplicate or alter the historical presentation/experiment media.
