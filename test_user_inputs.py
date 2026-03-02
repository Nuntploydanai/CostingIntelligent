"""
Test manufacturing with user's exact inputs: Men + T-Shirt (Crew Neck) + No Seam + S-XL
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_all_manufacturing_rows

print("=" * 80)
print("TEST WITH USER'S INPUTS")
print("=" * 80)

# User's inputs from screenshot
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
print("Expected from user's Excel:")
print("  W18 (Minutes) = 2.3")
print("=" * 80)

# Check INDIA
india = rows[0]
print(f"\nINDIA Validation:")
print(f"  Minutes: {india['minutes']} (expected 2.3)")
print(f"  Match: {'✓ YES!' if abs(india['minutes'] - 2.3) < 0.01 else '✗ NO!'}")
