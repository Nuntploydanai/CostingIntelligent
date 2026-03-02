"""
Compare Excel results with Webapp results
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from fabrication_calc import compute_fabric_row
from manufacturing_calc import compute_manufacturing_row

# Test with typical values
print("=" * 70)
print("EXCEL vs WEBAPP COMPARISON")
print("=" * 70)

# Fabrication test
print("\n=== FABRICATION TEST ===")
fab_result = compute_fabric_row({
    'fabric_type': 'Jersey',
    'fabric_contents': 'Cotton/Spandex 95/5',
    'using_part': 'Whole Garment',
    'material_coo': 'Import',
    'weight_gsm_override': None,
    'price_unit': 'Price / Lbs',
    'price_value': 2.63,
    'fabric_finishing': 'Wicking',
    'color_design': 'Solid',
    'silhouette': 'Long Sleeve Shirt (Crew Neck)',
    'seam': 'Side Seam',
    'gender': 'MEN',
    'size': 'S-XL',
})

print("Fabrication Results:")
print(f"  PRICE/YD: {fab_result['default_price_yd']}")
print(f"  PRICE/KILO: {fab_result['default_price_kilo']}")
print(f"  Usage: {fab_result['usage']}")
print(f"  Total Cost: {fab_result['total_cost']}")

# Manufacturing test
print("\n=== MANUFACTURING TEST ===")
mfg_result = compute_manufacturing_row({'made_in': 'INDIA'})

print("Manufacturing Results:")
print(f"  Minutes: {mfg_result['minutes']}")
print(f"  Cost Rate: {mfg_result['cost_rate']}")
print(f"  Efficiency: {mfg_result['efficiency']}")
print(f"  Basic Cost: {mfg_result['basic_cost']}")
print(f"  Total Cost: {mfg_result['total_cost']}")

print("\n" + "=" * 70)
print("Please tell me:")
print("1. What are the EXPECTED values from Excel?")
print("2. What are the ACTUAL values showing in webapp?")
print("3. Which specific fields are different?")
print("=" * 70)
