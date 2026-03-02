import csv

print("Checking fabric_price_lookup.csv for Cotton/Spandex 95/5...")
with open('basicshirts_web/master_clean/fabric_price_lookup.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    found = []
    for row in r:
        if 'Cotton/Spandex 95/5' in row['key']:
            found.append(f"{row['key']} = {row['value']}")

print(f"Found {len(found)} matches:")
for m in found[:10]:
    print(f"  {m}")

print("\nAll keys starting with 'Jersey':")
with open('basicshirts_web/master_clean/fabric_price_lookup.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    jersey_keys = [row['key'] for row in r if row['key'].startswith('Jersey')]
    for k in jersey_keys[:10]:
        print(f"  {k}")
