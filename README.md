# Cookiepocalypse Planner

A single-page web app for planning a big holiday cookie bake, ported from the
"Cookiepocalypse 2024" Google Sheet with its formulas kept intact.

## What it does
- **Plan:** batches = ⌈cookies per unit × total cookie units ÷ cookies per batch⌉; oven time = minutes per batch × batches.
- **Recipes:** add, edit, duplicate and delete recipes, with per-batch amounts, grams and mixing phases.
- **Baking Cheat Sheet:** per-batch and scaled totals for each planned recipe, grouped by phase and ordered by "When to bake?".
- **Shopping List:** totals by ingredient and unit, converted to bulk units through the Bulk Conversions table, with checkboxes.
- **Recipients:** cookie units per person; the total drives the batch counts.
- **Conversions:** a checker for gram and bulk conversions, a quick converter, and editable conversion tables.
- **Import / Export:** recipes as CSV or JSON, a full backup as JSON, the shopping list and cheat sheet as CSV.

## Files
- `index.html`: the built app, a single self-contained file.
- `src/index.src.html` + `src/calc.js`: source code. Build with `python3 scripts/build.py src/index.src.html src/calc.js index.html`.
- `data/seed.json`: starter data imported from the 2024 sheet. The app loads it on first run.
- `scripts/test.js`: checks the calculations against the sheet's computed shopping list (`node scripts/test.js data/seed_full_2024.json data/sheet_shopping_2024.json`).

## Saving progress
In the hosted version, progress saves to your Claude account automatically. Use **Import / Export → Full backup**
to save a `.json` snapshot, which you can commit to `backups/` to keep history here.
