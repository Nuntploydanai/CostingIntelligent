"""
Test manufacturing with Step 1 inputs: Men + T-Shirt (Crew Neck) + No Seam + S-XL
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_all_manufacturing_rows

print("=" * 80)
print("TEST: Men + T-Shirt (Crew Neck) + No Seam + S-XL")
print("=" * 80)

rows = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="T-Shirt (Crew Neck)",
    seam="No Seam",
    size="S-XL",
)

print("\nCountry          | Minutes | Cost Rate | Efficiency | Total Cost")
print("-" * 80)
for row in rows:
    print(f"{row['country']:16} | {row['minutes']:7} | {row['cost_rate']:9.6f} | {row['efficiency']:10} | {row['total_cost']:10.6f}")

print("\n" + "=" * 80)
print("Expected Minutes: 2.9 (from SAM&Product EFF% sheet)")
print("Expected Total for INDIA: (2.9 / 0.738) * 0.046537 = 0.183")
print("=" * 80)

# Check first row (INDIA)
india = rows[0]
print(f"\nINDIA Validation:")
print(f"  Minutes: {india['minutes']} (expected 2.9)")
print(f"  Total Cost: {india['total_cost']} (expected ~0.183)")
