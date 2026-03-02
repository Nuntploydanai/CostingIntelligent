"""
Check E25, E26, E27, E29 (the keys for J30 lookup)
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_dl = wb['Data link']

print("=" * 80)
print("DATA LINK - E25, E26, E27, E29 (Keys for J30)")
print("=" * 80)

print(f"E25 (Gender): {ws_dl['E25'].value}")
print(f"E26 (Product/Silhouette): {ws_dl['E26'].value}")
print(f"E27 (Seam): {ws_dl['E27'].value}")
print(f"E29 (Size): {ws_dl['E29'].value}")

print(f"\nConcatenated key: {ws_dl['E25'].value}{ws_dl['E26'].value}{ws_dl['E27'].value}{ws_dl['E29'].value}")

print("\n" + "=" * 80)
print("J30 (minutes from lookup):")
print(f"Value: {ws_dl['J30'].value}")
print("=" * 80)

# Now check what these should be based on Basic Shirts
ws_bs = wb['Basic Shirts Costing Tool']

print("\n=== Where do E25, E26, E27, E29 come from? ===")
wb_f = openpyxl.load_workbook(SRC, data_only=False, keep_vba=True)
ws_dl_f = wb_f['Data link']

print(f"E25 formula: {ws_dl_f['E25'].value}")
print(f"E26 formula: {ws_dl_f['E26'].value}")
print(f"E27 formula: {ws_dl_f['E27'].value}")
print(f"E29 formula: {ws_dl_f['E29'].value}")
