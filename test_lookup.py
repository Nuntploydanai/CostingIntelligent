import csv

# Check a specific lookup
print("Looking for Rubber_Print + 3X3 cm...")
with open('basicshirts_web/master_clean/print_embroidery_price_lookup.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        if row['printing_embroidery'] == 'Rubber_Print' and '3X3' in row['dimension']:
            print(f"Found: '{row['printing_embroidery']}' + '{row['dimension']}' = {row['default_price_each']}")
            print(f"  Repr: {repr(row['printing_embroidery'])}, {repr(row['dimension'])}")

print("\nAll Rubber_Print entries:")
with open('basicshirts_web/master_clean/print_embroidery_price_lookup.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        if row['printing_embroidery'] == 'Rubber_Print':
            print(f"  '{row['dimension']}' -> {row['default_price_each']}")
