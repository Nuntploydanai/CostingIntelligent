"""
Calculate with 7% margin (user's actual value)
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# Test with 7% margin
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
    supplier_margin_percent=7.0,  # 7% margin!
)

print("=" * 80)
print("CALCULATION WITH 7% MARGIN")
print("=" * 80)

print(f"\nSubtotal (items 1-10): ${result['subtotal']:.6f}")
print(f"Supplier Margin (7%):  ${result['supplier_margin_amount']:.6f}")
print(f"FOB Cost:              ${result['fob_cost']:.6f}")

print(f"\nExpected FOB: $19.62")
print(f"Actual FOB:   ${result['fob_cost']:.2f}")
print(f"Difference:   ${abs(result['fob_cost'] - 19.62):.2f}")

if abs(result['fob_cost'] - 19.62) < 0.01:
    print("\nMATCH! With 7% margin")
else:
    print(f"\nStill off by ${abs(result['fob_cost'] - 19.62):.2f}")
