"""
Compare each item to find the $0.48 difference
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# Current calculation
result = compute_total_cost_summary(
    fabric_cost=0.14,
    trim_cost=16.8,
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

# Expected FOB = 19.62
# FOB = subtotal * 1.10
# So subtotal = 19.62 / 1.10 = 17.84

expected_subtotal = 19.62 / 1.10
actual_subtotal = result['subtotal']

print("=" * 80)
print("ITEM-BY-ITEM COMPARISON")
print("=" * 80)

items = [
    ("Fabric Cost", result['total_fabric_cost'], 0.14),
    ("Trim Cost", result['total_trim_cost'], 16.8),
    ("Display Packaging", result['total_display_packaging_cost'], 0.01),
    ("Transit Packaging", result['total_transit_packaging_cost'], 0.1),
    ("Label Cost", result['total_label_cost'], 0.02884),
    ("Sewing Thread", result['total_sewing_thread_cost'], 0.035),
    ("Labour Cost", result['total_labour_cost'], 0.144907),
    ("Product Testing", result['total_product_testing_cost'], 0.01),
    ("Print/Embroidery", result['total_print_embroidery_cost'], 1.05),
    ("Other Cost", result['total_other_cost'], 0.0),
]

print(f"\n{'Item':<25} {'Actual':>15} {'Expected':>15} {'Diff':>10}")
print("-" * 80)

for name, actual, expected in items:
    diff = actual - expected
    print(f"{name:<25} ${actual:>14.6f} ${expected:>14.6f} ${diff:>9.6f}")

print("-" * 80)
print(f"{'SUBTOTAL':<25} ${actual_subtotal:>14.6f} ${expected_subtotal:>14.6f} ${actual_subtotal - expected_subtotal:>9.6f}")
print(f"{'Margin (10%)':<25} ${result['supplier_margin_amount']:>14.6f}")
print(f"{'FOB':<25} ${result['fob_cost']:>14.6f} ${19.62:>14.2f} ${result['fob_cost'] - 19.62:>9.6f}")

print("\n" + "=" * 80)
print("ANALYSIS:")
print("=" * 80)
print(f"Current subtotal: ${actual_subtotal:.2f}")
print(f"Expected subtotal: ${expected_subtotal:.2f}")
print(f"Difference: ${actual_subtotal - expected_subtotal:.2f}")
print("\nThis means one of the items is ${:.2f} too high.".format(actual_subtotal - expected_subtotal))
