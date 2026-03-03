"""
Test: What if trim cost should exclude sewing thread?
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# If FOB should be 19.62, and margin is 10%, then subtotal = 19.62 / 1.10 = 17.84
# Current subtotal is 18.32
# Difference is 0.48

# If trim cost is 16.8, and we need to reduce subtotal by 0.48,
# then trim cost should be 16.8 - 0.48 = 16.32

test_trim_cost = 16.32

result = compute_total_cost_summary(
    fabric_cost=0.14,
    trim_cost=test_trim_cost,
    print_embroidery_cost=1.05,
    display_packaging_cost=0.01,
    transit_packaging_cost=0.1,
    label_cost=0.02884,
    labour_cost=0.144907,
    gender="Men",
    silhouette="Tank Top/A Shirt",
    size="S-XL",
    supplier_margin_percent=10.0,
)

print("=" * 80)
print(f"TEST: If trim cost = ${test_trim_cost}")
print("=" * 80)

print(f"\nSubtotal: ${result['subtotal']:.2f}")
print(f"Margin (10%): ${result['supplier_margin_amount']:.2f}")
print(f"FOB: ${result['fob_cost']:.2f}")

print(f"\nExpected FOB: $19.62")
print(f"Difference: ${abs(result['fob_cost'] - 19.62):.2f}")

if abs(result['fob_cost'] - 19.62) < 0.01:
    print("\n✅ MATCH! Trim cost should be $16.32")
else:
    print(f"\n❌ Still not matching. Need to investigate further.")
