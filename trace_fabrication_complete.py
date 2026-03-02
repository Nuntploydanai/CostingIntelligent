"""
Complete trace of Conversion sheet formulas for Q7/S7 calculation.
This matches Excel exactly.
"""

# Test case from Excel
fabric_type = "Jersey"
fabric_contents = "Cotton/Spandex 95/5"
using_part = "Whole Garment"
material_coo = "Import"
weight_gsm_override = None  # Use default
price_unit = "Price / Lbs"
price_value = 2.63  # Override from Excel
fabric_finishing = "Wicking"  # From earlier trace
color_design = "Solid"  # Default

# Expected results
expected_Q7 = 1.319
expected_S7 = 5.909

print("=" * 60)
print("TRACING CONVERSION SHEET FORMULAS")
print("=" * 60)

# Step 1: Basic inputs
print("\n--- STEP 1: Basic Inputs ---")
print(f"Fabric Type: {fabric_type}")
print(f"Fabric Contents: {fabric_contents}")
print(f"Using Part: {using_part}")
print(f"Price Unit: {price_unit}")
print(f"Price Value (override): {price_value}")
print(f"Fabric Finishing: {fabric_finishing}")
print(f"Color/Design: {color_design}")

# Step 2: Constants
print("\n--- STEP 2: Constants ---")
B2 = 60.0  # Fixed width in inches
print(f"B2 (fixed width inches): {B2}")

# Default GSM based on fabric type
default_gsm_map = {
    "Jersey": 160.0,
    "Rib1x1": 180.0,
    "Rib2x1": 180.0,
    "Mesh": 150.0,
    "Fleece": 220.0,
}
B3 = default_gsm_map.get(fabric_type, 160.0)
print(f"B3 (default GSM from fabric type): {B3}")

# Effective GSM (user override or default)
weight_gsm = weight_gsm_override if weight_gsm_override is not None else B3
print(f"Effective GSM (weight_gsm): {weight_gsm}")

# Step 3: Width calculations (J2, J3, K3, L3)
print("\n--- STEP 3: Width Calculations ---")
J2 = B2  # J2 = IFERROR(Data link!I38, "-") = 60
print(f"J2 (width inches): {J2}")

J3 = weight_gsm  # J3 = Data link!N7 = O7+M7 = weight_gsm
print(f"J3 (width mm = weight_gsm): {J3}")

K3 = J2 * 0.0254  # K3 = J2*0.0254
print(f"K3 (width meters): {K3}")

L3 = J3 / 1000.0  # L3 = J3/1000
print(f"L3 (width mm to meters): {L3}")

K13 = L3 * K3  # K13 = 1*L3*K3
print(f"K13 (area factor): {K13}")

# Step 4: Price lookup
print("\n--- STEP 4: Price Lookup ---")
# Data link!E7 = CONCATENATE(H7, J7) = fabric_type + fabric_contents
E7 = fabric_type + fabric_contents
print(f"Data link E7 (lookup key): {E7}")

# Data link!O7 = XLOOKUP(E7, Fabric Price!U:U, W:W) = default price/lb
# For Jersey + Cotton/Spandex 95/5, this is 1.6
O7_default = 1.6
print(f"Data link O7 (default price/lb): {O7_default}")

# Data link!P7 = IF(ISBLANK(U7), O7, U7) = use override if provided
# Basic Shirts U7 = price_value (2.63)
P7 = price_value if price_value is not None else O7_default
print(f"Data link P7 (effective price/lb): {P7}")

# Step 5: Price unit conversion (C11, C13, C4)
print("\n--- STEP 5: Price Unit Conversion ---")
C3 = B2 * 0.0254  # C3 = B2*0.0254
D3 = B3 / 1000.0  # D3 = B3/1000
C13 = D3 * C3  # C13 = 1*D3*C3
print(f"C13 (kgs conversion): {C13}")

C11 = C13 * 2.20462262  # C11 = C13*2.20462262
print(f"C11 (lbs conversion): {C11}")

C4 = C3 * D3 * 35.274  # C4 = C3*D3*35.274
print(f"C4 (ounces conversion): {C4}")

# Step 6: A24 and C23 calculation
print("\n--- STEP 6: A24 and C23 ---")
A24 = P7  # A24 = Data link!P7
print(f"A24 (effective price): {A24}")

# C24 = unit conversion based on Basic Shirts U6 (price_unit)
if price_value is not None:
    if price_unit == "Price / Yds":
        C24 = price_value
    elif price_unit == "Price / Kgs":
        C24 = price_value * C13 * 0.9144
    elif price_unit == "Price / Meters":
        C24 = price_value * 0.9144
    elif price_unit == "Price / Lbs":
        C24 = price_value * C11 * 0.9144
    elif price_unit == "Price / Ounces":
        C24 = price_value * C4 * 0.9144
    else:
        C24 = A24
    C23 = C24
    print(f"C24 (converted price for {price_unit}): {C24}")
else:
    C23 = A24
    print("C23 = A24 (no override)")

print(f"C23 (final price for conversion): {C23}")

# Step 7: E23 calculation
print("\n--- STEP 7: E23 ---")
E23 = (C23 / 0.9144) / C13
print(f"E23 = (C23/0.9144)/C13 = {E23}")

# Step 8: V6 (finishing cost) calculation
print("\n--- STEP 8: V6 (Finishing Cost) ---")
V4 = weight_gsm  # V4 = Basic Shirts O7+M7
print(f"V4 (weight_gsm): {V4}")

V5 = (V4 * 1.19599) * 1.6667
print(f"V5 = (V4*1.19599)*1.6667 = {V5}")

# T4 = XLOOKUP(Q4, Fabric Price!AR:AR, AS:AS)
# Q4 = Data link!E12 = Basic Shirts D24 = fabric_finishing
Q4 = fabric_finishing
print(f"Q4 (finishing type): {Q4}")

# T4 lookup (from fabric_price_ar_as_lookup.csv)
finishing_lookup = {
    "Wicking": 0.06615,
    "Odor Control": 0.11025000000000001,
    "Xtemp": 0.33075,
    "Odor Control + Wicking": 0.1764,
    "Xtemp + Odor Control": 0.44100000000000006,
    "None": 0.0,
    "OTHER": 0.0,
}
T4 = finishing_lookup.get(Q4, 0.0)
print(f"T4 (finishing price): {T4}")

V6 = V5 * T4 / 1000.0
print(f"V6 = V5*T4/1000 = {V6}")

# Step 9: K16 and M16 calculation
print("\n--- STEP 9: K16 and M16 ---")
K16 = E23 + V6
print(f"K16 = E23+V6 = {K16}")

M16 = (K16 * K13) * 0.9144
print(f"M16 = (K16*K13)*0.9144 = {M16}")

# Step 10: V18 (color factor)
print("\n--- STEP 10: V18 (Color Factor) ---")
if color_design == "Solid":
    V18 = 1.0
elif color_design == "white":
    V18 = 0.95
elif color_design == "Heather":
    V18 = 1.1
elif color_design == "Others":
    V18 = 1.07
else:
    V18 = 0.0
print(f"V18 (color factor for '{color_design}'): {V18}")

# Step 11: M18 and O18 (PRICE/YD)
print("\n--- STEP 11: M18 and O18 (PRICE/YD) ---")
M18 = (M16 + V6) * V18
print(f"M18 = (M16+V6)*V18 = {M18}")

O18 = M18  # O18 = IFERROR(M18, "Please select yarn contents")
print(f"O18 (PRICE/YD) = {O18}")

Q7 = round(O18, 3)
print(f"Q7 (rounded) = {Q7}")

# Step 12: K20 (PRICE/KILO)
print("\n--- STEP 12: K20 (PRICE/KILO) ---")
K20 = O18 / (J3 * 1.3946 / 1000.0)
print(f"K20 = O18/(J3*1.3946/1000) = {K20}")

S7 = round(K20, 3)
print(f"S7 (rounded) = {S7}")

# Step 13: Compare with expected
print("\n" + "=" * 60)
print("COMPARISON WITH EXPECTED VALUES")
print("=" * 60)
print(f"Expected Q7: {expected_Q7}")
print(f"Calculated Q7: {Q7}")
print(f"Difference: {abs(Q7 - expected_Q7):.6f}")
print()
print(f"Expected S7: {expected_S7}")
print(f"Calculated S7: {S7}")
print(f"Difference: {abs(S7 - expected_S7):.6f}")

if abs(Q7 - expected_Q7) < 0.01 and abs(S7 - expected_S7) < 0.01:
    print("\n✓ CALCULATION MATCHES EXCEL!")
else:
    print("\n✗ CALCULATION DOES NOT MATCH - need to investigate")
