import csv

# Check if we have the finishing lookup
path = 'basicshirts_web/master_clean/fabric_price_ar_as_lookup.csv'
print('Checking fabric_price_ar_as_lookup.csv...')
with open(path, 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    found = []
    for row in r:
        if 'Wicking' in row['key'] or 'wicking' in row['key'].lower():
            found.append(f"{row['key']} = {row['value']}")

print(f"Found {len(found)} matches for Wicking:")
for m in found:
    print(f"  {m}")

print("\nAll keys in lookup:")
with open(path, 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        print(f"  {row['key']} = {row['value']}")
