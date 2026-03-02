"""
Extract manufacturing cost data from Excel Data link sheet
"""
import openpyxl
import csv
from pathlib import Path

SRC = r"C:\Users\dploy\OneDrive\Documents\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"
OUT_DIR = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean")

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_dl = wb['Data link']

print("=" * 80)
print("MANUFACTURING COST DATA FROM DATA LINK")
print("=" * 80)

# Countries are in rows 30-35
countries_order = ['INDIA', 'BANGLADESH', 'INDONESIA', 'THAILAND', 'CAMBODIA', 'VIETNAM']

manufacturing_data = []

for i, country in enumerate(countries_order):
    row = 30 + i

    # Get values from Data link
    minutes = ws_dl[f'J{row}'].value
    cost_rate = ws_dl[f'L{row}'].value
    efficiency = ws_dl[f'Q{row}'].value

    print(f"\n{country} (Row {row}):")
    print(f"  J{row} (Minutes): {minutes}")
    print(f"  L{row} (Cost Rate): {cost_rate}")
    print(f"  Q{row} (Efficiency): {efficiency}")

    manufacturing_data.append({
        'country': country,
        'minutes': minutes or 0.0,
        'cost_rate': cost_rate or 0.0,
        'efficiency': efficiency or 0.0,
    })

# Write to CSV
csv_path = OUT_DIR / "manufacturing_cost_by_country.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=['country', 'minutes', 'cost_rate', 'efficiency'])
    w.writeheader()
    for row in manufacturing_data:
        w.writerow(row)

print(f"\n\nWrote manufacturing data to {csv_path}")
