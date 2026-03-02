"""
Debug packing & label calculation
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from packing_label_calc import compute_packing_label

result = compute_packing_label({
    'pack_count': 2,
    'display_packaging': 'Basic STD  HNA',
    'transit_package': 36,
    'label_type': 'Woven Label',
})

print("Full result:")
import json
print(json.dumps(result, indent=2))

print("\n\nChecking specific fields:")
print(f"display_packaging_total: {result.get('display_packaging_total')}")
print(f"transit_total: {result.get('transit_total')}")
print(f"label_total: {result.get('label_total')}")
