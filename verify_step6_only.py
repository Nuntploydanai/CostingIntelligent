"""
Verify Step 6 is properly added (without Total Cost Summary)
"""

html_file = r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\web\index.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'Title shows Step 1-6': 'Step 1–6' in content,
    'Manufacturing Cost Section': 'id="mfgGrid"' in content,
    'Manufacturing Output Section': 'id="mfgOutGrid"' in content,
    'Manufacturing Country Dropdown': "dropdowns.manufacturing_countries" in content,
    'Manufacturing Minutes Field': 'mfg_minutes_ro' in content,
    'Manufacturing Cost Rate Field': 'mfg_cost_rate_ro' in content,
    'Manufacturing Efficiency Field': 'mfg_efficiency_ro' in content,
    'Manufacturing Total Field': 'mfg_total_ro' in content,
    'Manufacturing in Payload': 'manufacturing: {' in content and 'made_in' in content,
    'Manufacturing Render Code': 'mfg.minutes' in content,
    'NO Total Cost Summary': 'id="summaryGrid"' not in content,
    'NO Grand Total': 'summary_grand_total_ro' not in content,
}

print("=" * 70)
print("VERIFICATION - Step 6 Added (Without Total Cost Summary)")
print("=" * 70)

all_pass = True
for check, result in checks.items():
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} - {check}")
    if not result:
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("ALL CHECKS PASSED!")
    print("\nStep 6 Manufacturing Cost is ready!")
    print("\nTo test:")
    print("  1. Start server: cd basicshirts_web && python server.py")
    print("  2. Open browser: http://127.0.0.1:8000/")
    print("  3. Press Ctrl+F5 to hard refresh")
    print("  4. Fill in data and click Calculate")
    print("  5. See Manufacturing Cost section!")
else:
    print("SOME CHECKS FAILED - Review above")
print("=" * 70)
