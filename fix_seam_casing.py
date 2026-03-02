"""
Fix SAM lookup CSV - force correct casing
"""
import csv
from pathlib import Path

MASTER_DIR = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean")
SRC = MASTER_DIR / "sam_minutes_lookup.csv"

# Read
with SRC.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} rows")

# Fix casing
seam_map = {
    "No seam": "No Seam",
    "No Seam": "No Seam",
    "Side Seam": "Side Seam",
}

fixed_count = 0
for row in rows:
    old_seam = row['seam']
    new_seam = seam_map.get(old_seam, old_seam)
    if old_seam != new_seam:
        row['seam'] = new_seam
        fixed_count += 1
        print(f"Fixed: {old_seam} -> {new_seam}")

print(f"\nFixed {fixed_count} rows")

# Write back
with SRC.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=['gender', 'product', 'seam', 'size', 'sam_minutes'])
    w.writeheader()
    for row in rows:
        w.writerow(row)

print(f"Updated {SRC}")

# Verify
print("\n=== Verification ===")
with SRC.open("r", encoding="utf-8", newline="") as f:
    for i, row in enumerate(csv.DictReader(f)):
        if i < 10:
            print(f"{row['gender']} + {row['product']} + {row['seam']} + {row['size']} = {row['sam_minutes']}")
