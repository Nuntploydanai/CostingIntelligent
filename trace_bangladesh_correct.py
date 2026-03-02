"""
Trace BANGLADESH manufacturing cost - CORRECT columns
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb_f = openpyxl.load_workbook(SRC, data_only=False, keep_vba=True)
wb_v = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)

ws_bs_f = wb_f['Basic Shirts Costing Tool']
ws_bs_v = wb_v['Basic Shirts Costing Tool']

print("=" * 80)
print("BANGLADESH MANUFACTURING COST (Row 31)")
print("=" * 80)

print("\n=== Correct Column Mapping ===")
print("I31 = Minutes")
print("K31 = Cost Rate")
print("M31 = Efficiency")
print("O31 = Total Cost")

print("\n=== BANGLADESH Values from Excel ===")
print(f"I31 (Minutes): {ws_bs_v['I31'].value}")
print(f"K31 (Cost Rate): {ws_bs_v['K31'].value}")
print(f"M31 (Efficiency): {ws_bs_v['M31'].value}")
print(f"O31 (Total): {ws_bs_v['O31'].value}")

print("\n=== BANGLADESH Formulas ===")
print(f"I31: {ws_bs_f['I31'].value}")
print(f"K31: {ws_bs_f['K31'].value}")
print(f"M31: {ws_bs_f['M31'].value}")
print(f"O31: {ws_bs_f['O31'].value}")

# Check Data Link row 40 (BANGLADESH)
ws_dl_v = wb_v['Data link']
ws_dl_f = wb_f['Data link']

print("\n=== DATA LINK Row 40 (BANGLADESH) ===")
print(f"Q40 (Minutes): {ws_dl_v['Q40'].value}")
print(f"S40 (Cost Rate): {ws_dl_v['S40'].value}")
print(f"U40 (Efficiency): {ws_dl_v['U40'].value}")
print(f"Z40 (Total): {ws_dl_v['Z40'].value}")

print("\n=== DATA LINK Formulas ===")
print(f"Q40: {ws_dl_f['Q40'].value}")
print(f"S40: {ws_dl_f['S40'].value}")
print(f"U40: {ws_dl_f['U40'].value}")
print(f"Z40: {ws_dl_f['Z40'].value}")

print("\n" + "=" * 80)
print("EXPECTED FOR BANGLADESH:")
print(f"  Minutes: {ws_bs_v['I31'].value}")
print(f"  Cost Rate: {ws_bs_v['K31'].value}")
print(f"  Efficiency: {ws_bs_v['M31'].value}")
print(f"  Total: {ws_bs_v['O31'].value}")
print("=" * 80)
