import csv
from pathlib import Path
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"
OUT = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean\conversion_constants.csv")

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws = wb["Conversion"]

# Keep a small curated set we already saw referenced:
# Conversion!O18 (used as Q7 in Data link)
constants = [
    ("O18", "fabric_price_unit_factor"),
]

rows = [["name", "cell", "value"]]
for cell, name in constants:
    v = ws[cell].value
    rows.append([name, cell, v if v is not None else ""])

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

print(f"wrote {OUT}")
