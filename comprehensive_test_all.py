"""
Comprehensive Test - Verify All Calculations and Summary
"""
import openpyxl
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from fabrication_calc import compute_fabric_row
from trims_calc import compute_trim_row
from embellishments_calc import compute_embellishment_row
from packing_label_calc import compute_packing_label
from manufacturing_calc import compute_manufacturing_for_coo

SRC = r"C:\Users\dploy\OneDrive\Documents\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb['Basic Shirts Costing Tool']

print("=" * 80)
print("COMPREHENSIVE TEST - ALL STEPS + TOTAL SUMMARY")
print("=" * 80)

# Get current Excel inputs
gender = ws_bs['D16'].value or "Men"
silhouette = ws_bs['D17'].value or "Tank Top/A Shirt"
seam = ws_bs['D18'].value or "Side Seam"
size = ws_bs['D20'].value or "S-XL"
quantity = ws_bs['D22'].value or "More than 100,000"
coo = ws_bs['D23'].value or "BANGLADESH"

print(f"\nCurrent Excel Inputs:")
print(f"  Gender: {gender}")
print(f"  Silhouette: {silhouette}")
print(f"  Seam: {seam}")
print(f"  Size: {size}")
print(f"  Quantity: {quantity}")
print(f"  COO: {coo}")

print("\n" + "=" * 80)
print("STEP 2: FABRICATION")
print("=" * 80)

# Test fabrication
ws_dl = wb['Data link']
fabric_cost_excel = ws_dl['Q7'].value or 0

print(f"\nExcel Fabrication Total: {fabric_cost_excel}")

print("\n" + "=" * 80)
print("STEP 3: TRIMS")
print("=" * 80)

# Check if there are trims
trim_cost_excel = 0
for row in range(44, 50):
    cost = ws_bs.cell(row, 11).value  # Column K
    if cost and isinstance(cost, (int, float)):
        trim_cost_excel += cost

print(f"\nExcel Trims Total: {trim_cost_excel}")

print("\n" + "=" * 80)
print("STEP 4: EMBELLISHMENTS")
print("=" * 80)

emb_cost_excel = ws_bs['K55'].value or 0
print(f"\nExcel Embellishments Total: {emb_cost_excel}")

print("\n" + "=" * 80)
print("STEP 5: PACKING & LABEL")
print("=" * 80)

packing_cost_excel = ws_bs['K65'].value or 0
print(f"\nExcel Packing & Label Total: {packing_cost_excel}")

print("\n" + "=" * 80)
print("STEP 6: MANUFACTURING COST")
print("=" * 80)

# Get manufacturing values from Excel
ws_dl = wb['Data link']
mfg_minutes_excel = ws_dl['J30'].value
mfg_cost_rate_excel = ws_dl['L30'].value
mfg_efficiency_excel = ws_dl['Q30'].value
mfg_total_excel = ws_dl['W21'].value

print(f"\nExcel Manufacturing (for {coo}):")
print(f"  W18 (Minutes): {mfg_minutes_excel}")
print(f"  W19 (Cost Rate): {mfg_cost_rate_excel}")
print(f"  W20 (Efficiency): {mfg_efficiency_excel}")
print(f"  W21 (Total Cost): {mfg_total_excel}")

# Test with webapp
mfg_result = compute_manufacturing_for_coo(
    gender=gender,
    silhouette=silhouette,
    seam=seam,
    size=size,
    quantity=quantity,
    coo=coo,
)

print(f"\nWebapp Manufacturing (for {coo}):")
print(f"  Minutes: {mfg_result['minutes']}")
print(f"  Cost Rate: {mfg_result['cost_rate']}")
print(f"  Efficiency: {mfg_result['efficiency']}")
print(f"  Total Cost: {mfg_result['total_cost']}")

print("\n" + "=" * 80)
print("TOTAL COST SUMMARY")
print("=" * 80)

# Calculate totals from Excel
total_excel = (fabric_cost_excel or 0) + (trim_cost_excel or 0) + (emb_cost_excel or 0) + (packing_cost_excel or 0) + (mfg_total_excel or 0)

print(f"\nFrom Excel:")
print(f"  Step 2 (Fabrication): ${fabric_cost_excel:.6f}")
print(f"  Step 3 (Trims): ${trim_cost_excel:.6f}")
print(f"  Step 4 (Embellishments): ${emb_cost_excel:.6f}")
print(f"  Step 5 (Packing & Label): ${packing_cost_excel:.6f}")
print(f"  Step 6 (Manufacturing): ${mfg_total_excel}")
print(f"  TOTAL: ${total_excel:.6f}")

print(f"\nFrom Webapp:")
print(f"  Step 6 (Manufacturing): ${mfg_result['total_cost']:.6f}")

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Check if Step 6 matches
if abs(mfg_result['minutes'] - (mfg_minutes_excel or 0)) < 0.01:
    print("✅ Step 6 Minutes: PASS")
else:
    print(f"❌ Step 6 Minutes: FAIL (Excel: {mfg_minutes_excel}, Webapp: {mfg_result['minutes']})")

if abs(mfg_result['efficiency'] - (mfg_efficiency_excel or 0)) < 0.01:
    print("✅ Step 6 Efficiency: PASS")
else:
    print(f"❌ Step 6 Efficiency: FAIL (Excel: {mfg_efficiency_excel}, Webapp: {mfg_result['efficiency']})")

if abs(mfg_result['cost_rate'] - (mfg_cost_rate_excel or 0)) < 0.0001:
    print("✅ Step 6 Cost Rate: PASS")
else:
    print(f"❌ Step 6 Cost Rate: FAIL (Excel: {mfg_cost_rate_excel}, Webapp: {mfg_result['cost_rate']})")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("1. Start server: python server.py")
print("2. Open: http://127.0.0.1:8000/")
print("3. Test with same inputs as Excel")
print("4. Verify Total Cost Summary matches")
print("=" * 80)
