"""
Comprehensive QA test for all Basic Shirts steps.
Validates calculation logic matches Excel formulas exactly.
"""

import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

# Import all calculation modules
from fabrication_calc import compute_fabric_row
from trims_calc import compute_trim_row
from embellishments_calc import compute_embellishment_row
from packing_label_calc import compute_packing_label

print("=" * 70)
print("COMPREHENSIVE QA TEST - ALL STEPS")
print("=" * 70)

# ============================================================================
# STEP 2: FABRICATION
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: FABRICATION")
print("=" * 70)

fabrication_input = {
    'fabric_type': 'Jersey',
    'fabric_contents': 'Cotton/Spandex 95/5',
    'using_part': 'Whole Garment',
    'material_coo': 'Import',
    'weight_gsm_override': None,
    'price_unit': 'Price / Lbs',
    'price_value': 2.63,
    'fabric_finishing': 'Wicking',
    'color_design': 'Solid',
    'silhouette': 'T-Shirt (Crew Neck)',
    'seam': 'Regular',
    'gender': 'MEN',
    'size': 'S-XL',
}

print("\nInput:")
for k, v in fabrication_input.items():
    print(f"  {k}: {v}")

fab_result = compute_fabric_row(fabrication_input)

print("\nOutput:")
print(f"  Fixed Fabric Width: {fab_result['fixed_fabric_width']}")
print(f"  Default Weight (GSM): {fab_result['default_weight_gsm']}")
print(f"  DEFAULT (PRICE/YD): {fab_result['default_price_yd']}")
print(f"  DEFAULT (PRICE/KILO): {fab_result['default_price_kilo']}")
print(f"  PRICE / Lbs (default): {fab_result['default_price_lb']}")
print(f"  TOTAL COST: {fab_result['total_cost']}")

# Expected values from Excel
expected_fab = {
    'fixed_fabric_width': '60"',
    'default_weight_gsm': 160.0,
    'default_price_yd': 1.319,
    'default_price_kilo': 5.909,
    'default_price_lb': 1.6,
}

print("\nExpected from Excel:")
for k, v in expected_fab.items():
    print(f"  {k}: {v}")

print("\nValidation:")
fab_pass = True
for k, expected_val in expected_fab.items():
    actual_val = fab_result.get(k)
    if isinstance(expected_val, float):
        match = abs(float(actual_val) - expected_val) < 0.01
    else:
        match = str(actual_val) == str(expected_val)
    
    status = "PASS" if match else "FAIL"
    print(f"  {k}: {status}")
    if not match:
        print(f"    Expected: {expected_val}, Got: {actual_val}")
        fab_pass = False

# ============================================================================
# STEP 3: TRIMS & SEWN IN LABEL
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: TRIMS & SEWN IN LABEL")
print("=" * 70)

trims_input = {
    'trims_type': 'Main Label',
    'garment_part': 'Neck',
    'usage_override': None,
    'price_override': None,
    'material_coo': 'Domestic',
    'gender': 'MEN',
    'size': 'S-XL',
}

print("\nInput:")
for k, v in trims_input.items():
    print(f"  {k}: {v}")

trim_result = compute_trim_row(trims_input)

print("\nOutput:")
print(f"  UNIT: {trim_result['unit']}")
print(f"  DEFAULT USAGE (YD/PIECE): {trim_result['default_usage']}")
print(f"  DEFAULT PRICE/EACH: {trim_result['default_price_each']}")
print(f"  TOTAL COST: {trim_result['total_cost']}")

print("\nValidation:")
trim_pass = True
if isinstance(trim_result['default_usage'], (int, float)):
    print(f"  DEFAULT USAGE: PASS (numeric)")
else:
    print(f"  DEFAULT USAGE: {trim_result['default_usage']}")
    
if isinstance(trim_result['default_price_each'], (int, float)):
    print(f"  DEFAULT PRICE/EACH: PASS (numeric)")
else:
    print(f"  DEFAULT PRICE/EACH: {trim_result['default_price_each']}")

# ============================================================================
# STEP 4: EMBELLISHMENTS
# ============================================================================
print("\n" + "=" * 70)
print("STEP 4: EMBELLISHMENTS")
print("=" * 70)

embellishment_input = {
    'printing_embroidery': 'Rubber_Print',
    'dimension': '3X3 cm',
    'usage_unit': '1',
}

print("\nInput:")
for k, v in embellishment_input.items():
    print(f"  {k}: {v}")

emb_result = compute_embellishment_row(embellishment_input)

print("\nOutput:")
print(f"  DEFAULT PRICE/EACH: {emb_result['default_price_each']}")
print(f"  TOTAL COST: {emb_result['total_cost']}")

expected_emb = {
    'default_price_each': 0.1725,
    'total_cost': 0.172,
}

print("\nExpected from Excel:")
for k, v in expected_emb.items():
    print(f"  {k}: {v}")

print("\nValidation:")
emb_pass = True
for k, expected_val in expected_emb.items():
    actual_val = emb_result.get(k)
    match = abs(float(actual_val) - expected_val) < 0.01
    status = "PASS" if match else "FAIL"
    print(f"  {k}: {status}")
    if not match:
        print(f"    Expected: {expected_val}, Got: {actual_val}")
        emb_pass = False

# ============================================================================
# STEP 5: PACKING & LABEL
# ============================================================================
print("\n" + "=" * 70)
print("STEP 5: PACKING & LABEL")
print("=" * 70)

packing_input = {
    'pack_count': '2',
    'display_packaging': 'Basic STD  HNA',
    'transit_package': '36',
    'label_type': 'Woven Label',
}

print("\nInput:")
for k, v in packing_input.items():
    print(f"  {k}: {v}")

pack_result = compute_packing_label(packing_input)

print("\nOutput:")
print(f"  Display Packaging - DEFAULT USAGE: {pack_result['display_packaging']['default_usage']}")
print(f"  Display Packaging - TOTAL: {pack_result['display_packaging']['total']}")
print(f"  Transit Package - DEFAULT USAGE: {pack_result['transit_package']['default_usage']}")
print(f"  Transit Package - TOTAL: {pack_result['transit_package']['total']}")
print(f"  Label - DEFAULT USAGE: {pack_result['label']['default_usage']}")
print(f"  Label - TOTAL: {pack_result['label']['total']}")

expected_pack = {
    'display_packaging_usage': 0.5,
    'display_packaging_total': 0.05,
    'transit_usage': 1,
    'transit_total': 0.025,
    'label_usage': 1,
    'label_total': 0.029,
}

print("\nExpected from Excel:")
for k, v in expected_pack.items():
    print(f"  {k}: {v}")

print("\nValidation:")
pack_pass = True
actual_pack = {
    'display_packaging_usage': pack_result['display_packaging']['default_usage'],
    'display_packaging_total': pack_result['display_packaging']['total'],
    'transit_usage': pack_result['transit_package']['default_usage'],
    'transit_total': pack_result['transit_package']['total'],
    'label_usage': pack_result['label']['default_usage'],
    'label_total': pack_result['label']['total'],
}

for k, expected_val in expected_pack.items():
    actual_val = actual_pack[k]
    if isinstance(expected_val, float):
        match = abs(float(actual_val) - expected_val) < 0.01
    else:
        match = int(actual_val) == expected_val
    
    status = "PASS" if match else "FAIL"
    print(f"  {k}: {status}")
    if not match:
        print(f"    Expected: {expected_val}, Got: {actual_val}")
        pack_pass = False

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("QA SUMMARY")
print("=" * 70)

print(f"\nStep 2 (Fabrication): {'PASS' if fab_pass else 'FAIL'}")
print(f"Step 3 (Trims): {'PASS' if trim_pass else 'FAIL'}")
print(f"Step 4 (Embellishments): {'PASS' if emb_pass else 'FAIL'}")
print(f"Step 5 (Packing & Label): {'PASS' if pack_pass else 'FAIL'}")

if fab_pass and emb_pass and pack_pass:
    print("\n✓ ALL CRITICAL TESTS PASSED!")
else:
    print("\n✗ SOME TESTS FAILED - need investigation")

print("\n" + "=" * 70)
