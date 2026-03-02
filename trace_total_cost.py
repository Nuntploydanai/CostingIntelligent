"""
Complete trace of Total Cost calculation for Fabrication.
"""

print("=" * 70)
print("TOTAL COST FORMULA CHAIN - FABRICATION")
print("=" * 70)

# From Excel screenshots and formula extraction
print("\n=== BASIC SHIRTS Y7 (TOTAL COST) ===")
print("Y7 formula: =IF(Data link!H7=0, ..., IF(Data link!R7=X, Please select using part, Data link!Y7))")
print("Y7 gets value from: Data link!Y7")
print()

print("=== DATA LINK ROW 7 CHAIN ===")
print()
print("Y7 = X7 * T7")
print("     where:")
print("     X7 = W7 * Q7")
print("     T7 = import_factor (Domestic=1.0, Import=1.05)")
print()
print("W7 = V7 * B26")
print("     where:")
print("     V7 = U7 * size_multiplier")
print("     B26 = silhouette_multiplier")
print()
print("V7 = IF(E29='S-XL', U7*1, IF(E29='2XL-3XL', U7*1.15, IF(E29='S-3XL', U7*1.1, 0)))")
print()
print("U7 = IF(E25='MEN', R7*1, IF(E25='WOMEN', R7*0.85, IF(E25='KIDS', R7*0.75, '0')))")
print()
print("R7 = usage lookup from Fabric Usage sheet (K7 key + Using Part)")
print()
print("Q7 = Conversion!O18 (PRICE/YD)")
print()

print("=" * 70)
print("CALCULATING WITH ACTUAL VALUES")
print("=" * 70)
print()

# Actual values from Excel
R7_usage = 1.167  # From Fabric Usage lookup
E25_gender = "MEN"
E29_size = "S-XL"
B26_silhouette = 1.0  # T-Shirt (Crew Neck)
Q7_price_yd = 1.319
S7_material_coo = "Import"

print(f"R7 (usage from lookup): {R7_usage}")
print(f"E25 (gender): {E25_gender}")
print(f"E29 (size): {E29_size}")
print(f"B26 (silhouette multiplier): {B26_silhouette}")
print(f"Q7 (PRICE/YD): {Q7_price_yd}")
print(f"Material COO: {S7_material_coo}")
print()

# Step 1: U7 = R7 * gender_multiplier
if E25_gender == "MEN":
    gender_mult = 1.0
elif E25_gender == "WOMEN":
    gender_mult = 0.85
elif E25_gender == "KIDS":
    gender_mult = 0.75
else:
    gender_mult = 0.0

U7 = R7_usage * gender_mult
print(f"U7 = R7 * gender_mult = {R7_usage} * {gender_mult} = {U7}")

# Step 2: V7 = U7 * size_multiplier
if E29_size == "S-XL":
    size_mult = 1.0
elif E29_size == "2XL-3XL":
    size_mult = 1.15
elif E29_size == "S-3XL":
    size_mult = 1.1
else:
    size_mult = 0.0

V7 = U7 * size_mult
print(f"V7 = U7 * size_mult = {U7} * {size_mult} = {V7}")

# Step 3: W7 = V7 * B26
W7 = V7 * B26_silhouette
print(f"W7 = V7 * B26 = {V7} * {B26_silhouette} = {W7}")

# Step 4: X7 = W7 * Q7
X7 = W7 * Q7_price_yd
print(f"X7 = W7 * Q7 = {W7} * {Q7_price_yd} = {X7}")

# Step 5: T7 = import_factor
if S7_material_coo == "Domestic":
    import_factor = 1.0
elif S7_material_coo == "Import":
    import_factor = 1.05
else:
    import_factor = 0.0

print(f"T7 = import_factor = {import_factor} (for {S7_material_coo})")

# Step 6: Y7 = X7 * T7
Y7 = X7 * import_factor
print(f"Y7 = X7 * T7 = {X7} * {import_factor} = {Y7}")

print()
print("=" * 70)
print("RESULT")
print("=" * 70)
print(f"Calculated Y7 (Total Cost): {round(Y7, 3)}")
print(f"Expected from Excel:        1.616")
print(f"Difference:                 {abs(Y7 - 1.616):.6f}")

if abs(Y7 - 1.616) < 0.01:
    print("\n✓ CALCULATION MATCHES EXCEL!")
else:
    print("\n✗ CALCULATION DOES NOT MATCH")
