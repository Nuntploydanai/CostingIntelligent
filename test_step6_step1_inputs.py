"""
Test Step 6: Manufacturing Cost with Step 1 inputs
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_manufacturing_row

print("=" * 70)
print("STEP 6: MANUFACTURING COST - USING STEP 1 INPUTS")
print("=" * 70)

# Test with Step 1 inputs (like Excel)
result = compute_manufacturing_row({
    'coo': 'INDIA',
    'ideal_quantity': 'More than 100,000',
    'silhouette': 'Long Sleeve Shirt (Crew Neck)',
    'seam': 'Side Seam',
})

print("\nStep 1 Inputs:")
print("  COO: INDIA")
print("  Ideal Quantity: More than 100,000")
print("  Silhouette: Long Sleeve Shirt (Crew Neck)")
print("  Seam: Side Seam")

print("\nStep 6 Manufacturing Cost Results:")
print(f"  Country: {result['country']}")
print(f"  Quantity: {result['quantity']}")
print(f"  Minutes: {result['minutes']}")
print(f"  Cost Rate: {result['cost_rate']}")
print(f"  Efficiency: {result['efficiency']}")
print(f"  Total Cost: {result['total_cost']}")

print("\n" + "=" * 70)
print("Expected from Excel (for INDIA):")
print("  Minutes: 4.3")
print("  Cost Rate: 0.046537")
print("  Efficiency: 0.738")
print("  Total Cost: 0.271148")
print("=" * 70)

# Validation
checks = [
    ('Minutes', result['minutes'], 4.3),
    ('Cost Rate', result['cost_rate'], 0.046537),
    ('Efficiency', result['efficiency'], 0.738),
    ('Total Cost', result['total_cost'], 0.271148),
]

all_pass = True
for name, actual, expected in checks:
    if isinstance(expected, float):
        match = abs(float(actual) - expected) < 0.0001 if isinstance(actual, (int, float)) else False
    else:
        match = str(actual) == str(expected)

    status = "[PASS]" if match else "[FAIL]"
    print(f"{status} - {name}: {actual} (expected {expected})")
    if not match:
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("ALL CHECKS PASSED - Manufacturing uses Step 1 inputs correctly!")
else:
    print("SOME CHECKS FAILED")
print("=" * 70)
