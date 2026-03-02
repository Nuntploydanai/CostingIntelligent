# Master Data (CSV)

These CSVs are the **only global master inputs** to the Python calculation engine.

## How it works
- Users download a CSV, edit it, upload it.
- Changes apply globally immediately (for now).
- The frontend uses `dropdown_*.csv` to populate select inputs.
- The Python engine loads these CSVs and uses them in calculations.

## Files
### Dropdown datasets
- `dropdown_*.csv` are single-column (`value`) lists.
- The UI should use these as select options.

Example:
- `dropdown_coo.csv` → list of countries of origin

## Notes
- This folder is being built sheet-by-sheet from the workbook.
- Next datasets to be added: conversion tables, cost rates, fabric price tables, trims/packing, thread, SAM.
