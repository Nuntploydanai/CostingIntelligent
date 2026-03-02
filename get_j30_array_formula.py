"""
Trace the complete chain: J30 array formula -> K30 -> W18
"""
import openpyxl
import win32com.client

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"

excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = True

try:
    wb = excel.Workbooks.Open(SRC)
    ws_dl = wb.Sheets('Data link')

    print("=" * 80)
    print("J30 ARRAY FORMULA (using Excel COM)")
    print("=" * 80)

    j30_formula = ws_dl.Range('J30').FormulaArray
    print(f"\nJ30 FormulaArray: {j30_formula}")

    print("\n" + "=" * 80)
    print("Now checking which cells J30 references")
    print("=" * 80)

    # Get the range that J30 covers
    j30_range = ws_dl.Range('J30')
    print(f"J30 Range: {j30_range.Address}")

    wb.Close(False)
except Exception as e:
    print(f"Error: {e}")
finally:
    excel.Quit()
