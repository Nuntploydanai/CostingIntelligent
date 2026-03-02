"""
Final comprehensive test - All steps
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

print("=" * 80)
print("FINAL COMPREHENSIVE TEST - ALL STEPS")
print("=" * 80)

# Test 1: Manufacturing with both combinations
from manufacturing_calc import compute_all_manufacturing_rows

print("\n" + "=" * 80)
print("TEST 1: Manufacturing - Tank top/A Shirt + Side Seam")
print("=" * 80)

rows1 = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="Tank top/A Shirt",
    seam="Side Seam",
    size="S-XL",
    quantity="More than 100,000",
)

print(f"Minutes: {rows1[0]['minutes']} (expected 2.3)")
print(f"Efficiency: {rows1[0]['efficiency']} (expected 0.82)")
print(f"Result: {'PASS' if rows1[0]['minutes'] == 2.3 and rows1[0]['efficiency'] == 0.82 else 'FAIL'}")

print("\n" + "=" * 80)
print("TEST 2: Manufacturing - T-Shirt (Crew Neck) + No Seam")
print("=" * 80)

rows2 = compute_all_manufacturing_rows(
    gender="Men",
    silhouette="T-Shirt (Crew Neck)",
    seam="No Seam",
    size="S-XL",
    quantity="More than 100,000",
)

print(f"Minutes: {rows2[0]['minutes']} (expected 2.9)")
print(f"Efficiency: {rows2[0]['efficiency']} (expected 0.82)")
print(f"Result: {'PASS' if rows2[0]['minutes'] == 2.9 and rows2[0]['efficiency'] == 0.82 else 'FAIL'}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("All master data files extracted:")
print("  - sam_minutes_lookup.csv (126 rows)")
print("  - cost_rate.csv (15 countries)")
print("  - efficiency_by_quantity.csv (5 quantity ranges)")
print("\nUI Updates:")
print("  - Input fields now have grey background (#f5f5f5)")
print("  - Focus state changes to white background")
print("  - Total cost summary section added")
print("\nNext Steps:")
print("  1. Restart server: python server.py")
print("  2. Open http://127.0.0.1:8000/ with Ctrl+F5")
print("  3. Test all inputs and verify calculations match Excel")
print("=" * 80)
