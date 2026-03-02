"""
Check Basic Shirts D16, D17, D18, D20 (the ACTUAL inputs for manufacturing)
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)
ws_bs = wb['Basic Shirts Costing Tool']

print("=" * 80)
print("BASIC SHIRTS - ACTUAL INPUTS FOR MANUFACTURING")
print("=" * 80)

print(f"D16: {ws_bs['D16'].value}")
print(f"D17: {ws_bs['D17'].value}")
print(f"D18: {ws_bs['D18'].value}")
print(f"D19: {ws_bs['D19'].value}")
print(f"D20: {ws_bs['D20'].value}")

print("\n" + "=" * 80)
print("DATA LINK pulls from these cells:")
print("E25 = D16")
print("E26 = D17")
print("E27 = D18")
print("E29 = D20")
print("=" * 80)

# Check Data link
ws_dl = wb['Data link']
print(f"\nData link E25: {ws_dl['E25'].value}")
print(f"Data link E26: {ws_dl['E26'].value}")
print(f"Data link E27: {ws_dl['E27'].value}")
print(f"Data link E29: {ws_dl['E29'].value}")

print(f"\nData link J30 (minutes): {ws_dl['J30'].value}")
