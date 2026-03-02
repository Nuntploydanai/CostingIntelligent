import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

import importlib
import fabrication_calc
importlib.reload(fabrication_calc)
from fabrication_calc import compute_fabric_row

# Test with CORRECT silhouette and seam (Long Sleeve Shirt + Side Seam = usage 1.167)
result = compute_fabric_row({
    'fabric_type': 'Jersey',
    'fabric_contents': 'Cotton/Spandex 95/5',
    'using_part': 'Whole Garment',
    'material_coo': 'Import',
    'weight_gsm_override': None,  # Use default 160
    'price_unit': 'Price / Lbs',
    'price_value': 2.63,
    'fabric_finishing': 'Wicking',
    'color_design': 'Solid',
    'silhouette': 'Long Sleeve Shirt (Crew Neck)',  # Correct silhouette
    'seam': 'Side Seam',  # Correct seam
    'gender': 'MEN',
    'size': 'S-XL',
})

print("=" * 70)
print("FABRICATION CALCULATION - COMPLETE TEST (CORRECTED)")
print("=" * 70)

print("\nInput:")
print("  Fabric Type: Jersey")
print("  Fabric Contents: Cotton/Spandex 95/5")
print("  Using Part: Whole Garment")
print("  Material COO: Import")
print("  Price Unit: Price / Lbs")
print("  Price Value: 2.63")
print("  Fabric Finishing: Wicking")
print("  Color/Design: Solid")
print("  Silhouette: Long Sleeve Shirt")
print("  Seam: Side Seam")
print("  Gender: MEN")
print("  Size: S-XL")

print("\nOutput:")
print(f"  Fixed Fabric Width: {result['fixed_fabric_width']}")
print(f"  Default Weight (GSM): {result['default_weight_gsm']}")
print(f"  DEFAULT (PRICE/YD): {result['default_price_yd']}")
print(f"  DEFAULT (PRICE/KILO): {result['default_price_kilo']}")
print(f"  K7 Key: {result['k7_key']}")
print(f"  Usage: {result['usage']}")
print(f"  TOTAL COST: {result['total_cost']}")

print("\nExpected from Excel:")
print("  Fixed Fabric Width: 60\"")
print("  Default Weight (GSM): 160")
print("  DEFAULT (PRICE/YD): 1.319")
print("  DEFAULT (PRICE/KILO): 5.909")
print("  K7 Key: Long_Sleeve_Shirt_Side_Seam")
print("  Usage: 1.167")
print("  TOTAL COST: 1.616")

print("\nValidation:")
checks = [
    ('Fixed Fabric Width', result['fixed_fabric_width'], '60"'),
    ('Default Weight (GSM)', result['default_weight_gsm'], 160.0),
    ('DEFAULT (PRICE/YD)', result['default_price_yd'], 1.319),
    ('DEFAULT (PRICE/KILO)', result['default_price_kilo'], 5.909),
    ('K7 Key', result['k7_key'], 'Long_Sleeve_Shirt_Side_Seam'),
    ('Usage', result['usage'], 1.167),
    ('TOTAL COST', result['total_cost'], 1.616),
]

all_pass = True
for name, actual, expected in checks:
    if isinstance(expected, float):
        match = abs(float(actual) - expected) < 0.01
    else:
        match = str(actual) == str(expected)
    
    status = "PASS" if match else "FAIL"
    print(f"  {name}: {status}")
    if not match:
        print(f"    Expected: {expected}, Got: {actual}")
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("ALL CHECKS PASSED!")
else:
    print("SOME CHECKS FAILED")
print("=" * 70)
