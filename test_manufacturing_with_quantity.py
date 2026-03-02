"""
Test manufacturing with quantity parameter
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_all_manufacturing_rows

print("=" * 80)
print("TEST WITH QUANTITY = 'More than 100,000'")
print("=" * 80)

rows = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="Tank top/A Shirt",
    seam="Side Seam",
    size="S-XL",
    quantity="More than 100,000",
)

print("\nCountry          | Minutes | Cost Rate | Efficiency | Total Cost")
print("-" * 80)
for row in rows:
    print(f"{row['country']:16} | {row['minutes']:7} | {row['cost_rate']:9.6f} | {row['efficiency']:10} | {row['total_cost']:10.6f}")

print("\n" + "=" * 80)
print("Expected: Minutes=2.3, Efficiency=0.82")
print(f"Actual: Minutes={rows[0]['minutes']}, Efficiency={rows[0]['efficiency']}")
print(f"Match: {'PASS' if rows[0]['efficiency'] == 0.82 else 'FAIL'}")
print("=" * 80)
