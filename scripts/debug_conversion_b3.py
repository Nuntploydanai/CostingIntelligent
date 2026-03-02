import re
import openpyxl
SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"
wb=openpyxl.load_workbook(SRC,data_only=False,keep_vba=True)
ws=wb['Conversion']
f=ws['B3'].value
print('B3 formula head:', str(f)[:400])
str_re=re.compile(r'"([^"]+)"')
vals=str_re.findall(f)
print('literal count', len(vals))
print(vals[:80])
