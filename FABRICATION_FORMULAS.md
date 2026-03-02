"""
Fabrication formula chain from Excel:

BASIC SHIRTS Q7 (PRICE/YD):
=IFERROR(IF(ISBLANK(U7), IF(ISBLANK(G7), "-", Conversion!O18), Conversion!O18), "-")

BASIC SHIRTS S7 (PRICE/KILO):
=IFERROR(Conversion!K20, 0)

CONVERSION K20 (PRICE/KILO):
=O18/(J3*1.3946/1000)

CONVERSION O18 (PRICE/YD):
=IFERROR(M18, "Please select yarn contents")

CONVERSION M18:
=(M16+V6)*V18

CONVERSION M16:
=(K16*K13)*0.9144

CONVERSION K16:
=E23+V6

CONVERSION E23:
=(C23/0.9144)/C13

CONVERSION C23:
=IF(ISBLANK('Basic Shirts Costing Tool'!U7), A24, C24)

CONVERSION C24 (price unit conversion):
=IF(U6="Price / Yds", A24*1,
IF(U6="Price / Kgs", A24*C13*0.9144,
IF(U6="Price / Meters", A24*0.9144,
IF(U6="Price / Lbs", A24*C11*0.9144,
IF(U6="Price / Ounces", A24*C4*0.9144,
"Invalid Input")))))

CONVERSION A24:
='Data link'!P7

DATA LINK P7:
=IF(ISBLANK('Basic Shirts Costing Tool'!U7), 'Data link'!O7, 'Basic Shirts Costing Tool'!U7)

DATA LINK O7 (default price lookup):
=XLOOKUP($E$7, 'Fabric Price'!U:U, 'Fabric Price'!W:W)

DATA LINK E7 (lookup key):
=CONCATENATE(H7, J7)  # Fabric Type + Fabric Contents

CONVERSION C13:
=1*D3*C3

CONVERSION D3:
=B3/1000  # B3 = default GSM from fabric type (e.g., 160 for Jersey)

CONVERSION C3:
=B2*0.0254  # B2 = 60 (fixed width in inches)

CONVERSION V6:
=V5*T4/1000

CONVERSION V5:
=(V4*1.19599)*1.6667

CONVERSION V4:
='Basic Shirts Costing Tool'!$O$7+'Basic Shirts Costing Tool'!$M$7  # Fabric width (e.g., 160)

CONVERSION T4 (finishing surcharge):
=XLOOKUP(Q4, 'Fabric Price'!AR:AR, 'Fabric Price'!AS:AS)

CONVERSION Q4:
='Data link'!E12  # Fabric finishing type

DATA LINK E12:
='Basic Shirts Costing Tool'!D24  # Fabric Finishing

CONVERSION V18 (color multiplier):
=IF(V17="Solid", 1, IF(V17="white", 0.95, IF(V17="Heather", 1.1, IF(V17="Others", 1.07, "0"))))

CONVERSION V17:
='Data link'!$E$28  # Color/Design

DATA LINK E28:
='Basic Shirts Costing Tool'!D19  # Color/Design

CONVERSION J3 (fabric width for K20):
='Data link'!N7

DATA LINK N7:
='Basic Shirts Costing Tool'!M7+'Basic Shirts Costing Tool'!O7  # Fabric width parts
"""
