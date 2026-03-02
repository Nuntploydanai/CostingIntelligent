# Basic Shirts Costing Tool → Webapp (Approach B)

## Goal
Rebuild the costing logic as a webapp **without using Excel at runtime**.
Excel is only used as a *specification* during migration/validation.

## Confirmed UI scope
### Inputs
- All **grey cells** in `Basic Shirts Costing Tool`.
- Implementation proxy: all **unlocked** cells on that sheet (70 cells found).

### Outputs
1. **TOTAL COST SUMMARY**
   - Show **both** cost values and % columns.
2. **COST COMPARING FOR EACH COUNTRY**
   - Default view: key columns (COUNTRY, TOTAL, SUPPLIER FOB COST, REMARK)
   - Expand view: show full Excel-like detail columns.

## Sheets classification
### Non-master (inputs/presentation)
- `Manual`
- `Basic Shirts Costing Tool`

### Migration glue (not master, but logic reference)
- `Data link`
  - Acts as a wiring harness between inputs, master tables, and final outputs.
  - Will be replaced by explicit Python modules.

### Master data (global)
All other sheets are treated as candidate master data tables.
We extracted **72** table blocks into CSVs.

See: `master/master_data_registry.json` (draft, auto-generated).

## Master data storage
- Multiple CSVs (one table = one CSV)
- Globally applied immediately (no approvals/versioning for now)

## Next mapping steps (in progress)
1. Refine `master_data_registry.json`:
   - Remove helper/formula-only blocks
   - Assign stable dataset IDs and schemas (keys/columns)
2. Build `input_ui_map.json`:
   - Friendly labels
   - Types and dropdown sources
3. Replace `Data link` with Python modules:
   - fabric cost
   - trims/packing
   - labor (SAM + cost rate + efficiency)
   - testing / print+embroidery / other
   - totals + %
   - country comparison table

## Validation artifacts (Excel-derived, dev-only)
- Formula dumps:
  - `schema/formulas_total_cost_summary.csv`
  - `schema/formulas_country_comparison.csv`
- Dependency graphs:
  - `schema/deps_total_cost_summary.json`
  - `schema/deps_country_comparison.json`
- Calc order:
  - `schema/deps_total_cost_summary_calc_order.csv`
  - `schema/deps_country_comparison_calc_order.csv`

These are used to validate that the Python engine matches the workbook.
