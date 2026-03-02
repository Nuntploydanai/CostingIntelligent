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

print("\nResult keys:")
for k in sorted(result.keys()):
    print(f"  {k}: {result[k]}")

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

checks = [
    ('Fixed Fabric Width', result.get('fixed_fabric_width'), '60"'),
    ('Default Weight (GSM)', result.get('default_weight_gsm'), 160.0),
    ('DEFAULT (PRICE/YD)', result.get('default_price_yd'), 1.319),
    ('DEFAULT (PRICE/KILO)', result.get('default_price_kilo'), 5.909),
    ('TOTAL COST', result.get('total_cost'), 1.616),
]

all_pass = True
for name, actual, expected in checks:
    if isinstance(expected, float):
        match = abs(float(actual) - expected) < 0.01 if actual is not None else False
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
    print("SOME CHECKS FAILED - check usage lookup")
print("=" * 70)
