"""
VERIFY: Check if I extracted SAM data correctly from Excel
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)

ws_sam = wb['SAM&Product EFF%']

print("=" * 80)
print("VERIFYING SAM DATA EXTRACTION")
print("=" * 80)

print("\n=== Check Row 20 (Men + T-Shirt (Crew Neck) + No seam + S-XL) ===")
print(f"A20 (Gender): {ws_sam['A20'].value}")
print(f"B20 (Product): {ws_sam['B20'].value}")
print(f"C20 (Seam): {ws_sam['C20'].value}")
print(f"D20 (Size): {ws_sam['D20'].value}")
print(f"E20 (SAM): {ws_sam['E20'].value}")

print("\n=== Check Row 5 (Men + Tank top/A Shirt + Side Seam + S-XL) ===")
print(f"A5 (Gender): {ws_sam['A5'].value}")
print(f"B5 (Product): {ws_sam['B5'].value}")
print(f"C5 (Seam): {ws_sam['C5'].value}")
print(f"D5 (Size): {ws_sam['D5'].value}")
print(f"E5 (SAM): {ws_sam['E5'].value}")

print("\n" + "=" * 80)
print("QUESTION: Does your Excel show W18 = 2.3 or 2.9?")
print("If 2.3, which silhouette+seam combination do you have selected?")
print("=" * 80)

# Also check what's in Basic Shirts D14, D15
ws_bs = wb['Basic Shirts Costing Tool']
print("\n=== Current values in Basic Shirts ===")
print(f"D14 (Silhouette): {ws_bs['D14'].value}")
print(f"D15 (Seam): {ws_bs['D15'].value}")
print(f"D13 (Gender): {ws_bs['D13'].value}")
print(f"D16 (Size): {ws_bs['D16'].value}")
