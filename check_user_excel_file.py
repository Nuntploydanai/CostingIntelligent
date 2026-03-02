"""
Check user's Excel file from OneDrive
"""
import openpyxl

SRC = r"C:\Users\dploy\OneDrive\Documents\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)

ws_sam = wb['SAM&Product EFF%']

print("=" * 80)
print("CHECKING USER'S EXCEL FILE")
print("=" * 80)

print("\n=== Row 20 (Men + T-Shirt (Crew Neck) + No seam + S-XL) ===")
print(f"A20 (Gender): {ws_sam['A20'].value}")
print(f"B20 (Product): {ws_sam['B20'].value}")
print(f"C20 (Seam): {ws_sam['C20'].value}")
print(f"D20 (Size): {ws_sam['D20'].value}")
print(f"E20 (SAM): {ws_sam['E20'].value}")

print("\n=== Basic Shirts inputs ===")
ws_bs = wb['Basic Shirts Costing Tool']
print(f"D13 (Gender): {ws_bs['D13'].value}")
print(f"D14 (Silhouette): {ws_bs['D14'].value}")
print(f"D15 (Seam): {ws_bs['D15'].value}")
print(f"D16 (Size): {ws_bs['D16'].value}")

print("\n=== Data link W18 (Minutes) ===")
ws_dl = wb['Data link']
print(f"W18: {ws_dl['W18'].value}")

print("\n" + "=" * 80)
print(f"Expected: 2.3")
print(f"Actual: {ws_sam['E20'].value}")
print("=" * 80)
