"""
Debug: Check what silhouette/gender is being passed and lookup
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import _load_sewing_thread_cost

# Load the lookup table
lookup = _load_sewing_thread_cost()

print("=" * 80)
print("SEWING THREAD COST LOOKUP TABLE")
print("=" * 80)

for (gender, silhouette), cost in sorted(lookup.items()):
    print(f"{gender:10} | {silhouette:35} | ${cost:.3f}")

print("\n" + "=" * 80)
print("CHECKING SPECIFIC LOOKUPS")
print("=" * 80)

# Test different silhouette variations
test_cases = [
    ("Men", "Tank top/A Shirt"),
    ("Men", "Tank Top/A Shirt"),
    ("Men", "T-Shirt (Crew Neck)"),
    ("Men", "T-Shirt (V Neck)"),
]

for gender, silhouette in test_cases:
    cost = lookup.get((gender, silhouette), "NOT FOUND")
    print(f"{gender:10} | {silhouette:35} | {cost}")

print("\n" + "=" * 80)
print("CHECKING FRONTEND DROPDOWN VALUE")
print("=" * 80)

# Check what's in the dropdown
import csv
from pathlib import Path

dropdown_path = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean\dropdown_silhouette_pattern.csv")
with open(dropdown_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    silhouettes = [row['value'] for row in reader]
    print("Silhouette dropdown values:")
    for s in silhouettes:
        print(f"  - '{s}'")
        # Check if this exists in lookup
        cost = lookup.get(("Men", s), "NOT FOUND")
        print(f"    Lookup result: {cost}")
