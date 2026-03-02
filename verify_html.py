"""
Verify HTML has all sections
"""

html_file = r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\web\index.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'Manufacturing Cost Section': 'id="mfgGrid"' in content,
    'Manufacturing Output Section': 'id="mfgOutGrid"' in content,
    'Total Cost Summary Section': 'id="summaryGrid"' in content,
    'Manufacturing Country Dropdown': "dropdowns.manufacturing_countries" in content,
    'Manufacturing Minutes Field': 'mfg_minutes_ro' in content,
    'Manufacturing Cost Rate Field': 'mfg_cost_rate_ro' in content,
    'Manufacturing Efficiency Field': 'mfg_efficiency_ro' in content,
    'Manufacturing Total Field': 'mfg_total_ro' in content,
    'Summary Fabric Field': 'summary_fabric_ro' in content,
    'Summary Trims Field': 'summary_trims_ro' in content,
    'Summary Manufacturing Field': 'summary_mfg_ro' in content,
    'Summary Grand Total Field': 'summary_grand_total_ro' in content,
    'Manufacturing in Payload': 'manufacturing: {' in content and 'made_in' in content,
    'Manufacturing Render Code': 'mfg.minutes' in content,
    'Summary Render Code': 'summary.total_fabric_cost' in content,
}

print("=" * 70)
print("HTML VERIFICATION - Manufacturing + Total Cost Summary")
print("=" * 70)

all_pass = True
for check, result in checks.items():
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} - {check}")
    if not result:
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("ALL CHECKS PASSED - Frontend is ready!")
    print("\nTo test:")
    print("  1. Start server: cd basicshirts_web && python server.py")
    print("  2. Open browser: http://127.0.0.1:8000/")
    print("  3. Press Ctrl+F5 to hard refresh")
    print("  4. Fill in data and click Calculate")
    print("  5. See Manufacturing Cost + Total Cost Summary!")
else:
    print("SOME CHECKS FAILED - Review above")
print("=" * 70)
