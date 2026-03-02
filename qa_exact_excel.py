"""
QA Test with EXACT Excel inputs from screenshot
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_manufacturing_row
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

print("=" * 80)
print("QA TEST - EXACT EXCEL INPUTS FROM SCREENSHOT")
print("=" * 80)

# Load Excel to get the actual values
wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb['Basic Shirts Costing Tool']

# Get Step 1 inputs from Excel
silhouette = ws_bs['D14'].value
seam = ws_bs['D15'].value
coo = ws_bs['D23'].value
ideal_quantity = ws_bs['D22'].value

print("\n=== STEP 1 INPUTS FROM EXCEL ===")
print(f"Silhouette: {silhouette}")
print(f"Seam: {seam}")
print(f"COO: {coo}")
print(f"Ideal Quantity: {ideal_quantity}")

# Get expected manufacturing values from Excel
ws_bs2 = wb['Basic Shirts Costing Tool']
print("\n=== EXPECTED MANUFACTURING VALUES FROM EXCEL ===")
print(f"W18 (Minutes): {ws_bs2['W18'].value}")
print(f"W19 (Cost Rate): {ws_bs2['W19'].value}")
print(f"W20 (Efficiency): {ws_bs2['W20'].value}")
print(f"W21 (Total Cost): {ws_bs2['W21'].value}")

# Test with webapp
print("\n=== WEBAPP CALCULATION ===")
result = compute_manufacturing_row({
    'coo': coo,
    'ideal_quantity': ideal_quantity,
    'silhouette': silhouette,
    'seam': seam,
})

print(f"Country: {result['country']}")
print(f"Minutes: {result['minutes']}")
print(f"Cost Rate: {result['cost_rate']}")
print(f"Efficiency: {result['efficiency']}")
print(f"Total Cost: {result['total_cost']}")

# Compare
print("\n" + "=" * 80)
print("COMPARISON")
print("=" * 80)

excel_minutes = ws_bs2['W18'].value
excel_cost_rate = ws_bs2['W19'].value
excel_efficiency = ws_bs2['W20'].value
excel_total = ws_bs2['W21'].value

checks = [
    ('Minutes', result['minutes'], excel_minutes),
    ('Cost Rate', result['cost_rate'], excel_cost_rate),
    ('Efficiency', result['efficiency'], excel_efficiency),
    ('Total Cost', result['total_cost'], excel_total),
]

all_pass = True
for name, webapp_val, excel_val in checks:
    if isinstance(excel_val, float) and isinstance(webapp_val, (int, float)):
        match = abs(webapp_val - excel_val) < 0.001
    else:
        match = str(webapp_val) == str(excel_val)

    status = "[PASS]" if match else "[FAIL]"
    print(f"{status} {name}:")
    print(f"    Excel:  {excel_val}")
    print(f"    Webapp: {webapp_val}")
    if not match:
        all_pass = False

print("\n" + "=" * 80)
if all_pass:
    print("ALL CHECKS PASSED!")
else:
    print("MISMATCH FOUND - Need to fix!")
print("=" * 80)
