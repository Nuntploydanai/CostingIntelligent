import urllib.request
import json

# Test Step 5 with the exact values from the user's expected result
print("Testing Step 5 with expected values...")
print("  Display Packaging: Basic STD  HNA")
print("  Transit Package: 36")
print("  Label: Woven Label")
print("  Pack count: 2")

req = urllib.request.Request('http://127.0.0.1:8000/api/calculate', 
    data=json.dumps({
        'development': {
            'pack_count': '2'
        },
        'fabrication': [],
        'trims': [],
        'embellishments': [],
        'packing_label': {
            'display_packaging': 'Basic STD  HNA',
            'transit_package': '36',
            'label_type': 'Woven Label'
        }
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'})

resp = urllib.request.urlopen(req, timeout=5)
data = json.loads(resp.read().decode('utf-8'))

p = data['outputs']['packing_label']
print("\nResults:")
print(f"  Display Packaging - usage: {p['display_packaging']['default_usage']}, total: {p['display_packaging']['total']}")
print(f"  Transit Package - usage: {p['transit_package']['default_usage']}, total: {p['transit_package']['total']}")
print(f"  Label - usage: {p['label']['default_usage']}, total: {p['label']['total']}")

print("\nExpected:")
print("  Display Packaging - usage: 0.5, total: 0.05")
print("  Transit Package - usage: 1, total: 0.025")
print("  Label - usage: 1, total: 0.029")
