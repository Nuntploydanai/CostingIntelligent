"""
Test total cost calculation
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

print("=" * 80)
print("TEST TOTAL COST SUMMARY")
print("=" * 80)

# Test with sample values
result = compute_total_cost_summary(
    fabric_cost=0.14,
    trim_cost=16.8,
    print_embroidery_cost=1.05,
    display_packaging_cost=0.01,
    transit_packaging_cost=0.1,
    label_cost=0.02884,
    labour_cost=0.144907,
    gender="Men",
    silhouette="Tank top/A Shirt",
    size="S-XL",
    supplier_margin_percent=10.0,
)

print("\nResults:")
for key, value in result.items():
    print(f"  {key}: {value}")

print("\n" + "=" * 80)
print("EXPECTED FROM EXCEL:")
print("=" * 80)
print("  Sewing Thread: 0.035")
print("  Product Testing: 0.01")
print("  Subtotal: 18.32")
print("  Margin (10%): 1.83")
print("  FOB: 20.15")
print("=" * 80)

print(f"\nSewing Thread Match: {abs(result['total_sewing_thread_cost'] - 0.035) < 0.001}")
print(f"Product Testing Match: {abs(result['total_product_testing_cost'] - 0.01) < 0.001}")
