"""
Check Data link J30 to see how it's calculated
"""
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

wb_f = openpyxl.load_workbook(SRC, data_only=False, keep_vba=True)
wb_v = openpyxl.load_workbook(SRC, data_only=True, keep_vba=True)

ws_dl_f = wb_f['Data link']
ws_dl_v = wb_v['Data link']

print("=" * 80)
print("DATA LINK J30 - HOW IS IT CALCULATED?")
print("=" * 80)

print("\nJ30 with formulas:")
j30_formula = ws_dl_f['J30'].value
print(f"J30 Formula: {j30_formula}")
print(f"J30 Type: {type(j30_formula)}")

# If it's an array formula, we need to extract it
if hasattr(j30_formula, 'text'):
    print(f"J30 Array Formula Text: {j30_formula.text}")
elif hasattr(j30_formula, '__str__'):
    print(f"J30 String: {str(j30_formula)}")

print("\nJ30 Value:")
print(f"J30: {ws_dl_v['J30'].value}")

print("\n" + "=" * 80)
print("Check which row J30 is looking at")
print("=" * 80)

# Check E7 (the key that determines which row to lookup)
print(f"E7 (fabrication key): {ws_dl_v['E7'].value}")
print(f"E7 Formula: {ws_dl_f['E7'].value}")

# Check K7 (silhouette+seam key)
print(f"\nK7 (silhouette+seam key): {ws_dl_v['K7'].value}")
print(f"K7 Formula: {ws_dl_f['K7'].value}")

print("\n" + "=" * 80)
print("Maybe J30 uses a different lookup method?")
print("=" * 80)
