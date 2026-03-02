"""
Test manufacturing with COO parameter
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_manufacturing_for_coo

print("=" * 80)
print("TEST: Manufacturing for BANGLADESH (from your Excel)")
print("=" * 80)

result = compute_manufacturing_for_coo(
    gender="Men",
    silhouette="Tank top/A Shirt",
    seam="Side Seam",
    size="S-XL",
    quantity="More than 100,000",
    coo="BANGLADESH",
)

print(f"\nW18 (Minutes): {result['minutes']} (expected 2.3)")
print(f"W19 (Cost Rate): {result['cost_rate']} (expected ~0.051662)")
print(f"W20 (Efficiency): {result['efficiency']} (expected 0.82)")
print(f"W21 (Total Cost): {result['total_cost']} (expected ~0.1449)")

print("\n" + "=" * 80)
print("Expected from your Excel screenshot:")
print("  W18: 2.3")
print("  W19: 0.05166238869928356")
print("  W20: 0.82")
print("  W21: 0.14490696470484932")
print("=" * 80)

# Calculate manually
minutes = 2.3
cost_rate = 0.05166238869928356
efficiency = 0.82
total = (minutes / efficiency) * cost_rate

print(f"\nManual calculation:")
print(f"  Total = ({minutes} / {efficiency}) * {cost_rate}")
print(f"  Total = {total}")

print(f"\nWebapp result: {result['total_cost']}")
print(f"Match: {'PASS' if abs(result['total_cost'] - 0.1449) < 0.001 else 'FAIL'}")
