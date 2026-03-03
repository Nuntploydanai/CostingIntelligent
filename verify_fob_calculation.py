"""
Verify the FOB calculation
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from total_cost_calc import compute_total_cost_summary

# Test with actual values from screenshot
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

print("=" * 80)
print("CALCULATION BREAKDOWN")
print("=" * 80)

print("\nItem Costs:")
print(f"1. Fabric Cost:              ${result['total_fabric_cost']:.6f}")
print(f"2. Trim Cost:                ${result['total_trim_cost']:.6f}")
print(f"3. Display Packaging:        ${result['total_display_packaging_cost']:.6f}")
print(f"4. Transit Packaging:        ${result['total_transit_packaging_cost']:.6f}")
print(f"5. Label Cost:               ${result['total_label_cost']:.6f}")
print(f"6. Sewing Thread:            ${result['total_sewing_thread_cost']:.6f}")
print(f"7. Labour Cost:              ${result['total_labour_cost']:.6f}")
print(f"8. Product Testing:          ${result['total_product_testing_cost']:.6f}")
print(f"9. Print/Embroidery:         ${result['total_print_embroidery_cost']:.6f}")
print(f"10. Other Cost:              ${result['total_other_cost']:.6f}")

print(f"\nSubtotal (1-10):             ${result['subtotal']:.6f}")
print(f"Supplier Margin (10%):       ${result['supplier_margin_amount']:.6f}")
print(f"\nFOB Cost (Subtotal + Margin): ${result['fob_cost']:.6f}")

print(f"\nExpected FOB: $19.62")
print(f"Actual FOB:   ${result['fob_cost']:.2f}")
print(f"Difference:   ${abs(result['fob_cost'] - 19.62):.2f}")

# Calculate what the subtotal should be for FOB to be 19.62
# FOB = subtotal + (subtotal * 0.10) = subtotal * 1.10
# 19.62 = subtotal * 1.10
# subtotal = 19.62 / 1.10 = 17.84
print(f"\nFor FOB to be $19.62, subtotal should be: ${19.62 / 1.10:.2f}")
print(f"Current subtotal is: ${result['subtotal']:.2f}")
print(f"Difference in subtotal: ${result['subtotal'] - 19.62/1.10:.2f}")
