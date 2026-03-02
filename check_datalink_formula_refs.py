"""
Check Data link formulas to see which Basic Shirts cells they reference
"""
import openpyxl

SRC = r"C:\Users\dploy\OneDrive\Documents\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=False, keep_vba=True)

ws_dl = wb['Data link']

print("=" * 80)
print("DATA LINK FORMULAS - WHICH BASIC SHIRTS CELLS?")
print("=" * 80)

# E25, E26, E27, E29 formulas
print(f"E25 formula: {ws_dl['E25'].value}")
print(f"E26 formula: {ws_dl['E26'].value}")
print(f"E27 formula: {ws_dl['E27'].value}")
print(f"E29 formula: {ws_dl['E29'].value}")

print("\n" + "=" * 80)
print("Now checking what's in those Basic Shirts cells")
print("=" * 80)

wb_data = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb_data['Basic Shirts Costing Tool']

# Check both D13-D16 AND D16-D20
print("\n=== D13-D16 ===")
print(f"D13: {ws_bs['D13'].value}")
print(f"D14: {ws_bs['D14'].value}")
print(f"D15: {ws_bs['D15'].value}")
print(f"D16: {ws_bs['D16'].value}")

print("\n=== D16-D20 ===")
print(f"D16: {ws_bs['D16'].value}")
print(f"D17: {ws_bs['D17'].value}")
print(f"D18: {ws_bs['D18'].value}")
print(f"D19: {ws_bs['D19'].value}")
print(f"D20: {ws_bs['D20'].value}")
