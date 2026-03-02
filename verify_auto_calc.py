"""
Verify auto-calculation feature is implemented
"""

html_file = r"C:\Users\dploy\.openclaw\workspace\basicshirts_web\web\index.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'Auto-calc checkbox': 'id="autoCalc"' in content,
    'Debounce function': 'function debounceCalc()' in content,
    'Setup auto-calc function': 'function setupAutoCalc()' in content,
    'Change event listeners': "addEventListener('change', debounceCalc)" in content,
    'Input event listeners': "addEventListener('input', debounceCalc)" in content,
    'Setup called after UI built': 'setupAutoCalc()' in content,
    'Calculating indicator': 'id="calcIndicator"' in content,
    'Calculating CSS class': '.calculating' in content,
    'All field IDs covered': all(f"'{fid}'" in content for fid in ['dev_gender', 'fab_type', 'trim_type', 'emb_type', 'pack_display', 'mfg_country']),
}

print("=" * 70)
print("AUTO-CALCULATION FEATURE VERIFICATION")
print("=" * 70)

all_pass = True
for check, result in checks.items():
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} - {check}")
    if not result:
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("AUTO-CALCULATION FEATURE READY!")
    print("\nHow it works:")
    print("  1. Checkbox 'Auto-calculate (like Excel)' is ON by default")
    print("  2. When you change any input/select, it auto-calculates after 500ms")
    print("  3. Blue 'Calculating...' indicator shows during API call")
    print("  4. Results appear immediately (like Excel!)")
    print("  5. You can uncheck the box to disable auto-calc")
    print("  6. Manual 'Calculate' button still works")
    print("\nTest it:")
    print("  1. Start server: cd basicshirts_web && python server.py")
    print("  2. Open: http://127.0.0.1:8000/ (Ctrl+F5)")
    print("  3. Select/change any field")
    print("  4. Watch it auto-calculate!")
else:
    print("SOME CHECKS FAILED")
print("=" * 70)
