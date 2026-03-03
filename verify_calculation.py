"""
Simple test to verify server calculation works
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# Test the calculation
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

print("Total Cost Summary Test:")
print("-" * 60)
print(f"1. Total Fabric Cost:        ${result['total_fabric_cost']:.2f}")
print(f"2. Total Trim Cost:          ${result['total_trim_cost']:.2f}")
print(f"3. Display Packaging:        ${result['total_display_packaging_cost']:.2f}")
print(f"4. Transit Packaging:        ${result['total_transit_packaging_cost']:.2f}")
print(f"5. Label Cost:               ${result['total_label_cost']:.2f}")
print(f"6. Sewing Thread Cost:       ${result['total_sewing_thread_cost']:.2f}")
print(f"7. Labour Cost:              ${result['total_labour_cost']:.2f}")
print(f"8. Product Testing Cost:     ${result['total_product_testing_cost']:.2f}")
print(f"9. Print/Embroidery Cost:    ${result['total_print_embroidery_cost']:.2f}")
print(f"10. Other Cost:              ${result['total_other_cost']:.2f}")
print("-" * 60)
print(f"Subtotal:                    ${result['subtotal']:.2f}")
print(f"Supplier Margin (10%):       ${result['supplier_margin_amount']:.2f}")
print(f"FOB Cost:                    ${result['fob_cost']:.2f}")
print(f"Grand Total:                 ${result['grand_total']:.2f}")
print("-" * 60)

# Verify against expected values
print("\nVerification:")
print(f"Sewing Thread (expected $0.035): {'PASS' if abs(result['total_sewing_thread_cost'] - 0.035) < 0.001 else 'FAIL'}")
print(f"Product Testing (expected $0.01): {'PASS' if abs(result['total_product_testing_cost'] - 0.01) < 0.001 else 'FAIL'}")
print(f"FOB Cost (expected ~$20.15): {'PASS' if abs(result['fob_cost'] - 20.15) < 0.01 else 'FAIL'}")
