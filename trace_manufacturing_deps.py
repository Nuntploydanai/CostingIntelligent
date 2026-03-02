"""
Trace manufacturing cost formula dependencies
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

print("=" * 70)
print("MANUFACTURING COST FORMULA DEPENDENCIES")
print("=" * 70)

print("\n=== BASIC SHIRTS - Manufacturing Section ===")
print("W18 (Minutes) = Data link!K30")
print("W19 (Cost Rate) = Data link!L30")
print("W20 (Efficiency) = Data link!Q30 (or 0.65 if Kenya)")
print("W21 (Total Cost) = W18/W20*W19")

print("\n=== DATA LINK - K30 (Minutes) ===")
print("K30 = IF(any row has Pocket bag, J30+0.4, J30)")
print("J30 = Array formula (need to check)")

print("\n=== DATA LINK - L30 (Cost Rate) ===")
print("L30 = XLOOKUP(E32, 'Cost Rate'!A:A, 'Cost Rate'!O:O)")
print("E32 = Basic Shirts D23 = COO (Country)")

print("\n=== DATA LINK - Q30 (Efficiency) ===")
print("Q30 = XLOOKUP(E31, 'SAM&Product EFF%'!AA:AA, 'SAM&Product EFF%'!AB:AB) * N30")
print("E31 = Basic Shirts D22 = Ideal Quantity")
print("N30 = ? (array formula)")

print("\n=== KEY FINDING ===")
print("Manufacturing cost depends on:")
print("  1. Step 1 - Silhouette + Seam (affects base minutes J30)")
print("  2. Step 1 - Ideal Quantity (affects efficiency via E31)")
print("  3. Step 1 - COO (affects cost rate via E32)")
print("  4. Fabrication rows - if any has 'Pocket bag' (adds 0.4 to minutes)")

print("\n=== ISSUE IN WEBAPP ===")
print("Webapp has:")
print("  - Step 6: MADE IN dropdown (separate from Step 1 COO)")
print("  - Not connected to silhouette/seam from Step 1")
print("  - Not connected to Ideal Quantity from Step 1")

print("\n=== SOLUTION ===")
print("Remove Step 6 'MADE IN' dropdown")
print("Use Step 1 fields instead:")
print("  - COO (for cost rate)")
print("  - Ideal Quantity (for efficiency)")
print("  - Silhouette + Seam (for base minutes)")

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb['Basic Shirts Costing Tool']

print("\n=== CURRENT EXCEL VALUES ===")
print(f"D14 (Silhouette): {ws_bs['D14'].value}")
print(f"D15 (Seam): {ws_bs['D15'].value}")
print(f"D21 (Pack Count): {ws_bs['D21'].value}")
print(f"D22 (Ideal Quantity): {ws_bs['D22'].value}")
print(f"D23 (COO): {ws_bs['D23'].value}")

ws_dl = wb['Data link']
print(f"\nK30 (Minutes): {ws_dl['K30'].value}")
print(f"L30 (Cost Rate): {ws_dl['L30'].value}")
print(f"Q30 (Efficiency): {ws_dl['Q30'].value}")
print(f"R30 (Total): {ws_dl['R30'].value}")
