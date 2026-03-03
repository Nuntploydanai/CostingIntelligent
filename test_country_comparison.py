"""
Test that country comparison returns all countries
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from country_comparison_calc import compute_fob_by_country

# Test with sample inputs
results = compute_fob_by_country(
    fabric_cost=0.14,
    trim_cost=16.8,
    print_embroidery_cost=1.05,
    display_packaging_cost=0.01,
    transit_packaging_cost=0.1,
    label_cost=0.02884,
    gender="Men",
    silhouette="Tank Top/A Shirt",
    seam="Side Seam",
    size="S-XL",
    quantity="More than 100,000",
    supplier_margin_percent=7.0,
)

print("=" * 80)
print("COUNTRY COMPARISON RESULTS")
print("=" * 80)

print(f"\nTotal countries returned: {len(results)}")
print(f"\n{'Country':<15} {'Labour Cost':>15} {'FOB Cost':>15}")
print("-" * 80)

for row in results:
    print(f"{row['country']:<15} ${row['labour_cost']:>14.3f} ${row['fob_cost']:>14.3f}")

print("\n" + "=" * 80)
print("EXPECTED COUNTRIES:")
print("=" * 80)
print("1. INDIA")
print("2. BANGLADESH")
print("3. INDONESIA")
print("4. THAILAND")
print("5. CAMBODIA")
print("6. VIETNAM")

# Check if all expected countries are present
expected = ['INDIA', 'BANGLADESH', 'INDONESIA', 'THAILAND', 'CAMBODIA', 'VIETNAM']
actual = [r['country'] for r in results]

print(f"\nAll countries present: {set(expected) == set(actual)}")
if set(expected) != set(actual):
    print(f"Missing: {set(expected) - set(actual)}")
    print(f"Extra: {set(actual) - set(expected)}")
