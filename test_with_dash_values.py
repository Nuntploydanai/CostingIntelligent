"""
Test the calculation with '-' values (like Excel returns)
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# Test with "-" values (like Excel returns when no packing selected)
result = compute_total_cost_summary(
    fabric_cost=0.14,
    trim_cost=16.8,
    print_embroidery_cost=1.05,
    display_packaging_cost='-',  # Excel returns this when not selected
    transit_packaging_cost='-',  # Excel returns this when not selected
    label_cost='-',  # Excel returns this when not selected
    labour_cost=0.144907,
    gender="Men",
    silhouette="Tank top/A Shirt",
    size="S-XL",
    supplier_margin_percent=10.0,
)

print("Test with '-' values (Excel style):")
print("-" * 60)
print(f"1. Fabric Cost:        ${result['total_fabric_cost']:.2f} ({result['total_fabric_cost_pct']}%)")
print(f"2. Trim Cost:          ${result['total_trim_cost']:.2f} ({result['total_trim_cost_pct']}%)")
print(f"3. Display Packaging:  ${result['total_display_packaging_cost']:.2f} ({result['total_display_packaging_cost_pct']}%)")
print(f"4. Transit Packaging:  ${result['total_transit_packaging_cost']:.2f} ({result['total_transit_packaging_cost_pct']}%)")
print(f"5. Label Cost:         ${result['total_label_cost']:.2f} ({result['total_label_cost_pct']}%)")
print(f"6. Sewing Thread:      ${result['total_sewing_thread_cost']:.2f} ({result['total_sewing_thread_cost_pct']}%)")
print(f"7. Labour Cost:        ${result['total_labour_cost']:.2f} ({result['total_labour_cost_pct']}%)")
print(f"8. Product Testing:    ${result['total_product_testing_cost']:.2f} ({result['total_product_testing_cost_pct']}%)")
print(f"9. Print/Embroidery:   ${result['total_print_embroidery_cost']:.2f} ({result['total_print_embroidery_cost_pct']}%)")
print(f"10. Other Cost:        ${result['total_other_cost']:.2f} ({result['total_other_cost_pct']}%)")
print("-" * 60)
print(f"Subtotal:              ${result['subtotal']:.2f}")
print(f"Margin (10%):          ${result['supplier_margin_amount']:.2f}")
print(f"FOB Cost:              ${result['fob_cost']:.2f}")
print(f"Grand Total:           ${result['grand_total']:.2f}")
print("=" * 60)
print("SUCCESS: No errors with '-' values!")
