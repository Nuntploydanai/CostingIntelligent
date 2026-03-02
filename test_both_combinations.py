"""
Test manufacturing with BOTH combinations
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_all_manufacturing_rows

print("=" * 80)
print("TEST 1: Men + Tank top/A Shirt + Side Seam + S-XL (should give 2.3)")
print("=" * 80)

rows1 = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="Tank top/A Shirt",
    seam="Side Seam",
    size="S-XL",
)

print("\nCountry          | Minutes | Total Cost")
print("-" * 80)
for row in rows1[:3]:  # Just show first 3
    print(f"{row['country']:16} | {row['minutes']:7} | {row['total_cost']:10.6f}")

print(f"\nMinutes: {rows1[0]['minutes']} (expected 2.3) - {'PASS' if abs(rows1[0]['minutes'] - 2.3) < 0.01 else 'FAIL'}")

print("\n" + "=" * 80)
print("TEST 2: Men + T-Shirt (Crew Neck) + No Seam + S-XL (should give 2.9)")
print("=" * 80)

rows2 = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="T-Shirt (Crew Neck)",
    seam="No Seam",
    size="S-XL",
)

print("\nCountry          | Minutes | Total Cost")
print("-" * 80)
for row in rows2[:3]:  # Just show first 3
    print(f"{row['country']:16} | {row['minutes']:7} | {row['total_cost']:10.6f}")

print(f"\nMinutes: {rows2[0]['minutes']} (expected 2.9) - {'PASS' if abs(rows2[0]['minutes'] - 2.9) < 0.01 else 'FAIL'}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Test 1 (Tank top + Side Seam): {rows1[0]['minutes']} minutes - {'PASS' if abs(rows1[0]['minutes'] - 2.3) < 0.01 else 'FAIL'}")
print(f"Test 2 (T-Shirt + No Seam): {rows2[0]['minutes']} minutes - {'PASS' if abs(rows2[0]['minutes'] - 2.9) < 0.01 else 'FAIL'}")
print("=" * 80)
