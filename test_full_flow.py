import urllib.request
import json

# Test the full sequence a browser would do
print('1. Loading dropdowns...')

# Load printing_embroidery dropdown
req = urllib.request.Request('http://127.0.0.1:8000/api/dropdown/printing_embroidery')
resp = urllib.request.urlopen(req, timeout=5)
pe_data = json.loads(resp.read().decode('utf-8'))
print('   printing_embroidery values:', pe_data['values'])

# Load usage_unit dropdown  
req = urllib.request.Request('http://127.0.0.1:8000/api/dropdown/usage_unit')
resp = urllib.request.urlopen(req, timeout=5)
uu_data = json.loads(resp.read().decode('utf-8'))
print('   usage_unit values:', uu_data['values'][:5], '...')

# Load dimensions for first type
first_type = pe_data['values'][0]
print(f'2. Loading dimensions for {first_type}...')
req = urllib.request.Request(f'http://127.0.0.1:8000/api/embellishment/dimensions?printing_embroidery={first_type}')
resp = urllib.request.urlopen(req, timeout=5)
dim_data = json.loads(resp.read().decode('utf-8'))
print('   dimensions:', dim_data['values'][:5], '...')

# Calculate with first dimension
first_dim = dim_data['values'][0]
print(f'3. Calculating with {first_type}, {first_dim}, usage=1...')
req = urllib.request.Request('http://127.0.0.1:8000/api/calculate', 
    data=json.dumps({
        'development': {},
        'fabrication': [],
        'trims': [],
        'embellishments': [{'printing_embroidery': first_type, 'dimension': first_dim, 'usage_unit': '1'}],
        'packing_label': {}
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=5)
calc_data = json.loads(resp.read().decode('utf-8'))
emb = calc_data['outputs']['embellishments']['rows'][0]
print('   price:', emb['default_price_each'])
print('   total:', emb['total_cost'])
print()
print('SUCCESS - backend works correctly!')
