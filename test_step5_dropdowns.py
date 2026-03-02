import urllib.request
import json

# Test if Step 5 dropdowns are loading
print("Testing Step 5 dropdowns...")

for name in ['display_packaging', 'transit_package', 'label']:
    req = urllib.request.Request(f'http://127.0.0.1:8000/api/dropdown/{name}')
    resp = urllib.request.urlopen(req, timeout=5)
    data = json.loads(resp.read().decode('utf-8'))
    print(f"\n{name}:")
    print(f"  values: {data['values'][:5]}")
