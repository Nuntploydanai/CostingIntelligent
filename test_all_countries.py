"""
Test ALL countries manufacturing costs
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

from manufacturing_calc import compute_all_manufacturing_rows

print("=" * 80)
print("MANUFACTURING COST - ALL COUNTRIES")
print("=" * 80)

rows = compute_all_manufacturing_rows()

print("\nCountry          | Minutes | Cost Rate | Efficiency | Total Cost")
print("-" * 80)
for row in rows:
    print(f"{row['country']:16} | {row['minutes']:7} | {row['cost_rate']:9.6f} | {row['efficiency']:10} | {row['total_cost']:10.6f}")

print("\n" + "=" * 80)
print("EXPECTED FROM EXCEL:")
print("BANGLADESH should show:")
print("  Minutes: 4.3")
print("  Cost Rate: 0.051662")
print("  Efficiency: 0.738")
print("  Total Cost: 0.301")
print("=" * 80)

# Verify BANGLADESH
bangladesh = [r for r in rows if r['country'] == 'BANGLADESH'][0]
print("\nBANGLADESH Validation:")
checks = [
    ('Minutes', bangladesh['minutes'], 4.3),
    ('Cost Rate', bangladesh['cost_rate'], 0.051662),
    ('Efficiency', bangladesh['efficiency'], 0.738),
    ('Total Cost', bangladesh['total_cost'], 0.301),
]

all_pass = True
for name, actual, expected in checks:
    if isinstance(expected, float):
        match = abs(float(actual) - expected) < 0.001 if isinstance(actual, (int, float)) else False
    else:
        match = str(actual) == str(expected)

    status = "[PASS]" if match else "[FAIL]"
    print(f"  {status} {name}: {actual} (expected {expected})")
    if not match:
        all_pass = False

print("\n" + ("ALL CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
