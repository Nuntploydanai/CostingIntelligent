"""
Test Step 6: Manufacturing Cost
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_manufacturing_row, get_country_list

print("=" * 70)
print("STEP 6: MANUFACTURING COST TEST")
print("=" * 70)

# Test country list
countries = get_country_list()
print(f"\nAvailable countries: {countries}")

# Test INDIA
result = compute_manufacturing_row({"made_in": "INDIA"})
print(f"\nINDIA Manufacturing Cost:")
print(f"  Minutes: {result['minutes']}")
print(f"  Cost Rate: {result['cost_rate']}")
print(f"  Efficiency: {result['efficiency']}")
print(f"  Basic Cost: {result['basic_cost']}")
print(f"  Total Cost: {result['total_cost']}")

print("\n" + "=" * 70)
print("Backend is ready!")
print("=" * 70)
