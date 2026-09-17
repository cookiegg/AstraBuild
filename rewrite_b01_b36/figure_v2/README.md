# AstraBuild Figure v2

This directory contains the second-generation paper figures for the B01--B36 clean-sheet manuscript.

## Design provenance

The visual hierarchy and layout language were first explored with GPT Image prototypes during paper review. The publication assets in this directory do **not** use generated engineering geometry as empirical evidence. Instead, the final hybrid figures reconstruct the same layout using preserved B01--B36 historical artifacts already present in the AstraBuild publication repository.

## Hybrid SVG strategy

The figures deliberately use a mixed representation:

- titles, labels, boxes, arrows, dividers, statistics, and explanatory text are native SVG vectors/text;
- complex engineering renders, diagnostics, measurement profiles, overlays, and station views remain embedded raster evidence from the historical experiment archive;
- CairoSVG converts the SVG master files to PDF for LaTeX inclusion;
- PNG exports are retained only for preview and browser inspection.

This avoids low-quality automatic vector tracing of complex 3D imagery while keeping all explanatory graphics and text scalable and editable.

## Main assets

- `hybrid_svg/fig01_overview_v2.svg` — evidence / Astra-Codex / deterministic tools / persistent-state overview.
- `hybrid_svg/fig04_transitions_v2.svg` — three structural transitions explaining why the reconstruction loop broadens.
- `hybrid_svg/fig05_persistence_v2.svg` — cross-batch persistent-state dependency and B15 error-propagation risk.
- `hybrid_pdf/*.pdf` — vector/text-preserving versions used by `paper_layout_v2.tex`.
- `preview_png/*.png` — visual inspection copies.
- `build_figure_v2.py` — deterministic regeneration script.

Figure 2 (longitudinal map) and Figure 3 (operator matrix) remain deterministic analysis figures from the original clean-sheet draft because they are timeline/data visualizations rather than conceptual schematics.

## Paper v2

The corresponding paper artifacts are:

- `../20_FULL_MANUSCRIPT_FIGURE_V2.md`
- `../build_typeset_paper_v2.py`
- `../paper_layout_v2.tex`
- `../paper_layout_v2.pdf`

The paper uses the v2 hybrid PDFs for Figures 1, 4, and 5, while retaining the existing deterministic Figures 2 and 3.
