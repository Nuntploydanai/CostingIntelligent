"""
Debug manufacturing lookup
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import _load_sam_minutes_lookup

sam_lookup = _load_sam_minutes_lookup()

print("=" * 80)
print("SAM LOOKUP TABLE - Sample Keys")
print("=" * 80)

# Show first 10 keys
for i, key in enumerate(sam_lookup.keys()):
    if i < 10:
        print(f"{key} -> {sam_lookup[key]}")

print("\n" + "=" * 80)
print("Looking for: Men + Tank Top/A Shirt + Side Seam + S-XL")
print("=" * 80)

# Check all variations of "Tank top"
for key in sam_lookup.keys():
    gender, product, seam, size = key
    if 'Tank' in product and seam == 'Side Seam' and size == 'S-XL':
        print(f"Found: {key} -> {sam_lookup[key]}")

# Test exact key
test_key = ("Men", "Tank top/A Shirt", "Side Seam", "S-XL")
print(f"\nTest lookup with key {test_key}:")
print(f"Result: {sam_lookup.get(test_key, 'NOT FOUND')}")

# Check if product name matches
print("\n" + "=" * 80)
print("All products with 'Tank' in name:")
print("=" * 80)
for key in sam_lookup.keys():
    if 'Tank' in key[1]:
        print(f"{key[1]}")
        break  # Just show first
