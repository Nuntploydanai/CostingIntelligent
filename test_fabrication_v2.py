import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from fabrication_calc_v2 import compute_fabric_row

# Test with actual Excel values
result = compute_fabric_row({
    'fabric_type': 'Jersey',
    'fabric_contents': 'Cotton/Spandex 95/5',
    'using_part': 'Whole Garment',
    'material_coo': 'Domestic',
    'silhouette': 'T-Shirt (Crew Neck)',
    'seam': 'Regular',
    'gender': 'MEN',
    'size': 'S-XL',
    'weight_gsm_override': None,  # use default 160
    'price_unit': 'Price / Lbs',
    'price_value': None,  # use default
})

print("Fabrication result:")
print(f"  Fixed Fabric Width: {result['fixed_fabric_width']}")
print(f"  Default Weight (GSM): {result['default_weight_gsm']}")
print(f"  DEFAULT (PRICE/YD): {result['default_price_yd']}")
print(f"  DEFAULT (PRICE/KILO): {result['default_price_kilo']}")
print(f"  PRICE / Lbs (default): {result['default_price_lb']}")
print(f"  TOTAL COST: {result['total_cost']}")

print("\nExpected from Excel:")
print("  Fixed Fabric Width: 60\"")
print("  Default Weight (GSM): 160")
print("  DEFAULT (PRICE/YD): 1.319")
print("  DEFAULT (PRICE/KILO): 5.909")
