"""
Find which combination gives 2.3 minutes
"""
import csv
from pathlib import Path

SAM_FILE = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean\sam_minutes_lookup.csv")

print("=" * 80)
print("FINDING WHICH COMBINATION GIVES 2.3 MINUTES")
print("=" * 80)

with SAM_FILE.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        sam = float(row['sam_minutes'])
        if 2.2 <= sam <= 2.4:
            print(f"{row['gender']} + {row['product']} + {row['seam']} + {row['size']} = {sam}")

print("\n" + "=" * 80)
print("Looking for T-Shirt (Crew Neck) + No seam combinations")
print("=" * 80)

with SAM_FILE.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        if 'T-Shirt (Crew Neck)' in row['product'] and row['seam'] == 'No seam':
            print(f"{row['gender']} + {row['product']} + {row['seam']} + {row['size']} = {row['sam_minutes']}")
