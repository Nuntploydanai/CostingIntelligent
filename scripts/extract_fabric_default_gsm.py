import csv
import re
from pathlib import Path
import openpyxl

SRC = r"C:\Users\dploy\Downloads\Design to Basic Shirt Tool First Trail Version 1 - 20250801-update latest.xlsm"
OUT = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\master_clean\fabric_type_default_gsm.csv")

wb=openpyxl.load_workbook(SRC,data_only=False,keep_vba=True)
ws=wb['Conversion']
formula=ws['B3'].value
if not isinstance(formula,str):
    raise SystemExit('B3 formula missing')

# pattern: H7="TYPE",<number>
pair_re=re.compile(r"H7=\"([^\"]+)\"\s*,\s*([0-9]+(?:\.[0-9]+)?)")
pairs=pair_re.findall(formula)
rows=[["fabric_type","default_gsm"]]
for t,num in pairs:
    rows.append([t,float(num)])

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
    csv.writer(f).writerows(rows)
print('wrote', OUT, 'rows', len(rows)-1)
