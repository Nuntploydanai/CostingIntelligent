"""
Carefully trace manufacturing formulas from Excel screenshots
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

print("=" * 80)
print("TRACING MANUFACTURING COST FROM EXCEL - STEP BY STEP")
print("=" * 80)

# Load Excel
wb_formulas = openpyxl.load_workbook(SRC, data_only=False, keep_vba=True)
wb_values = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)

ws_bs_formulas = wb_formulas['Basic Shirts Costing Tool']
ws_bs_values = wb_values['Basic Shirts Costing Tool']
ws_dl_formulas = wb_formulas['Data link']
ws_dl_values = wb_values['Data link']

print("\n=== STEP 1: INPUTS FROM BASIC SHIRTS ===")
print(f"D14 (Silhouette): {ws_bs_values['D14'].value}")
print(f"D15 (Seam): {ws_bs_values['D15'].value}")
print(f"D21 (Pack Count): {ws_bs_values['D21'].value}")
print(f"D22 (Ideal Quantity): {ws_bs_values['D22'].value}")
print(f"D23 (COO): {ws_bs_values['D23'].value}")

print("\n=== STEP 2: MANUFACTURING COST FORMULAS (W18-W21) ===")
print("\nW18 (Minutes):")
print(f"  Formula: {ws_bs_formulas['W18'].value}")
print(f"  Value: {ws_bs_values['W18'].value}")

print("\nW19 (Cost Rate):")
print(f"  Formula: {ws_bs_formulas['W19'].value}")
print(f"  Value: {ws_bs_values['W19'].value}")

print("\nW20 (Efficiency):")
print(f"  Formula: {ws_bs_formulas['W20'].value}")
print(f"  Value: {ws_bs_values['W20'].value}")

print("\nW21 (Total Cost):")
print(f"  Formula: {ws_bs_formulas['W21'].value}")
print(f"  Value: {ws_bs_values['W21'].value}")

print("\n=== STEP 3: DATA LINK ROW 30 (Source of W18-W20) ===")
print("\nK30 (Minutes base):")
print(f"  Formula: {ws_dl_formulas['K30'].value}")
print(f"  Value: {ws_dl_values['K30'].value}")

print("\nL30 (Cost Rate):")
print(f"  Formula: {ws_dl_formulas['L30'].value}")
print(f"  Value: {ws_dl_values['L30'].value}")

print("\nQ30 (Efficiency):")
print(f"  Formula: {ws_dl_formulas['Q30'].value}")
print(f"  Value: {ws_dl_values['Q30'].value}")

print("\n=== STEP 4: DATA LINK DEPENDENCIES ===")
print("\nE31 (for efficiency lookup):")
print(f"  Formula: {ws_dl_formulas['E31'].value}")
print(f"  Value: {ws_dl_values['E31'].value}")

print("\nE32 (for cost rate lookup):")
print(f"  Formula: {ws_dl_formulas['E32'].value}")
print(f"  Value: {ws_dl_values['E32'].value}")

print("\nN30 (efficiency multiplier):")
print(f"  Formula: {ws_dl_formulas['N30'].value}")
print(f"  Value: {ws_dl_values['N30'].value}")

print("\n=== STEP 5: J30 (Base minutes before pocket bag check) ===")
print(f"  Formula: {ws_dl_formulas['J30'].value}")
print(f"  Value: {ws_dl_values['J30'].value}")

print("\n" + "=" * 80)
print("PLEASE SHARE:")
print("1. Screenshot of Excel showing the WRONG webapp values")
print("2. What are the CORRECT Excel values?")
print("3. Which specific cells are different?")
print("=" * 80)
