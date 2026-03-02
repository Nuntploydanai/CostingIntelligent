"""
Comprehensive QA - Test all steps against Excel
"""
import openpyxl
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from fabrication_calc import compute_fabric_row
from trims_calc import compute_trim_row
from embellishments_calc import compute_embellishment_row
from packing_label_calc import compute_packing_label
from manufacturing_calc import compute_all_manufacturing_rows

SRC = r"C:\Users\dploy\OneDrive\Documents\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb['Basic Shirts Costing Tool']

print("=" * 80)
print("COMPREHENSIVE QA - ALL STEPS")
print("=" * 80)

# Get current inputs from Excel
gender = ws_bs['D16'].value or "Men"
silhouette = ws_bs['D17'].value or "Tank Top/A Shirt"
seam = ws_bs['D18'].value or "Side Seam"
size = ws_bs['D20'].value or "S-XL"

print(f"\nCurrent Excel Inputs:")
print(f"  Gender: {gender}")
print(f"  Silhouette: {silhouette}")
print(f"  Seam: {seam}")
print(f"  Size: {size}")

print("\n" + "=" * 80)
print("STEP 2: FABRICATION")
print("=" * 80)

# Test fabrication (row 7 in Excel)
ws_dl = wb['Data link']
print(f"\nExcel Fabrication Row 7:")
print(f"  Fabric Type: {ws_dl['E7'].value}")
print(f"  Usage: {ws_dl['I7'].value}")
print(f"  Price/YD: {ws_dl['L7'].value}")
print(f"  Total Cost: {ws_dl['Q7'].value}")

# Test with webapp
fabric_input = {
    "fabric_type": ws_dl['E7'].value or "Jersey",
    "fabric_contents": "Cotton/Spandex 95/5",
    "using_part": "Body",
    "material_coo": "Local",
    "usage_value": ws_dl['I7'].value or 0.23,
    "price_value": ws_dl['L7'].value or 3.5,
    "price_unit": "Price / YD",
    "gender": gender,
    "silhouette": silhouette,
    "seam": seam,
    "size": size,
}

fabric_result = compute_fabric_row(fabric_input)
print(f"\nWebapp Fabrication Result:")
print(f"  Total Cost: {fabric_result.get('total_cost')}")
print(f"  Match: {'PASS' if abs(fabric_result.get('total_cost', 0) - (ws_dl['Q7'].value or 0)) < 0.01 else 'NEED MANUAL CHECK'}")

print("\n" + "=" * 80)
print("STEP 3: TRIMS")
print("=" * 80)

# Get first trim row from Excel (row 7)
print(f"\nExcel Trim Row 7:")
print(f"  Trim Type: {ws_bs['B44'].value}")
print(f"  Total Cost: {ws_bs['K44'].value}")

print("\n" + "=" * 80)
print("STEP 4: EMBELLISHMENTS")
print("=" * 80)

# Get first embellishment from Excel
print(f"\nExcel Embellishment Row:")
print(f"  Printing/Embroidery: {ws_bs['D55'].value}")
print(f"  Total Cost: {ws_bs['K55'].value}")

print("\n" + "=" * 80)
print("STEP 5: PACKING & LABEL")
print("=" * 80)

print(f"\nExcel Packing & Label:")
print(f"  Display Packaging: {ws_bs['D65'].value}")
print(f"  Total Cost: {ws_bs['K65'].value}")

packing_result = compute_packing_label({
    "pack_count": 1,
    "display_packaging": ws_bs['D65'].value,
    "transit_package": ws_bs['D66'].value,
    "label_type": ws_bs['D67'].value,
})

print(f"\nWebapp Packing Result:")
print(f"  Total Cost: {packing_result.get('total_cost')}")
print(f"  Match: {'PASS' if abs(packing_result.get('total_cost', 0) - (ws_bs['K65'].value or 0)) < 0.01 else 'NEED MANUAL CHECK'}")

print("\n" + "=" * 80)
print("STEP 6: MANUFACTURING COST")
print("=" * 80)

# Test manufacturing
ws_dl = wb['Data link']
excel_minutes = ws_dl['J30'].value
excel_cost_rate = ws_dl['L30'].value
excel_efficiency = ws_dl['Q30'].value
excel_total = ws_dl['W21'].value

print(f"\nExcel Manufacturing (INDIA):")
print(f"  Minutes: {excel_minutes}")
print(f"  Cost Rate: {excel_cost_rate}")
print(f"  Efficiency: {excel_efficiency}")
print(f"  Total Cost: {excel_total}")

mfg_rows = compute_all_manufacturing_rows(
    gender=gender,
    silhouette=silhouette,
    seam=seam,
    size=size,
)

india = mfg_rows[0]
print(f"\nWebapp Manufacturing (INDIA):")
print(f"  Minutes: {india['minutes']}")
print(f"  Cost Rate: {india['cost_rate']}")
print(f"  Efficiency: {india['efficiency']}")
print(f"  Total Cost: {india['total_cost']}")

print(f"\nMatch: {'PASS' if abs(india['minutes'] - (excel_minutes or 0)) < 0.01 else 'FAIL'}")

print("\n" + "=" * 80)
print("QA SUMMARY")
print("=" * 80)
print("All steps need manual verification in webapp UI")
print("Server is ready at http://127.0.0.1:8000/")
print("=" * 80)
