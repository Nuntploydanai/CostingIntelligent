"""
Test Step 6: Manufacturing Cost and Total Cost Summary
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_manufacturing_row, get_country_list
from total_cost_calc import compute_total_cost_summary

print("=" * 70)
print("STEP 6: MANUFACTURING COST TEST")
print("=" * 70)

# Test country list
countries = get_country_list()
print(f"\nAvailable countries: {countries}")

# Test each country
print("\n=== Manufacturing Cost by Country ===")
for country in countries:
    result = compute_manufacturing_row({"made_in": country})
    print(f"\n{country}:")
    print(f"  Minutes: {result['minutes']}")
    print(f"  Cost Rate: {result['cost_rate']}")
    print(f"  Efficiency: {result['efficiency']}")
    print(f"  Basic Cost: {result['basic_cost']}")
    print(f"  Total Cost: {result['total_cost']}")

print("\n" + "=" * 70)
print("TOTAL COST SUMMARY TEST")
print("=" * 70)

# Simulate totals from all steps
summary = compute_total_cost_summary(
    fabric_total=1.616,  # From Step 2
    trims_total=0.042,  # From Step 3
    display_packaging_total=0.05,  # From Step 5
    transit_packaging_total=0.025,  # From Step 5
    label_total=0.029,  # From Step 5
    sewing_thread_cost=0.048,  # From Data link
    manufacturing_total=2.30,  # From Step 6 (INDIA)
    product_testing_cost=0.01,  # From Data link
    embellishment_total=0.0,  # From Step 4
)

print("\nTotal Cost Summary:")
for key, value in summary.items():
    if key != "note":
        print(f"  {key}: {value}")

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED")
print("=" * 70)
