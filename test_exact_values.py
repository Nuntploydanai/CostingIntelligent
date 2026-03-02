import urllib.request
import json

# Test with exact values from dropdown
test_cases = [
    ('Rubber_Print', '3X3 cm', '1'),
    ('Rubber_Print', '1X1 cm', '1'),
    ('Heat_Transfer', '20X10 mm', '1'),
]

for pe, dim, usage in test_cases:
    print(f"\nTesting: {pe} + {dim} + usage={usage}")
    req = urllib.request.Request('http://127.0.0.1:8000/api/calculate', 
        data=json.dumps({
            'development': {},
            'fabrication': [],
            'trims': [],
            'embellishments': [{'printing_embroidery': pe, 'dimension': dim, 'usage_unit': usage}],
            'packing_label': {}
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=5)
    calc_data = json.loads(resp.read().decode('utf-8'))
    emb = calc_data['outputs']['embellishments']['rows'][0]
    print(f"  price: {emb['default_price_each']}")
    print(f"  total: {emb['total_cost']}")
