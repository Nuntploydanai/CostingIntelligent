"""
Quick test to verify server endpoints work
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("Testing Step 6 + Total Cost Summary endpoints...\n")

# Test 1: Get countries list
print("1. Testing /api/manufacturing/countries:")
try:
    r = requests.get(f"{BASE_URL}/api/manufacturing/countries")
    print(f"   Status: {r.status_code}")
    if r.ok:
        data = r.json()
        print(f"   Countries: {data.get('countries', [])}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Calculate manufacturing cost
print("\n2. Testing /api/manufacturing/calculate:")
try:
    r = requests.post(f"{BASE_URL}/api/manufacturing/calculate", json={"made_in": "INDIA"})
    print(f"   Status: {r.status_code}")
    if r.ok:
        data = r.json()
        print(f"   India manufacturing cost: {data.get('total_cost')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Full calculation with all steps
print("\n3. Testing /api/calculate (full calculation):")
try:
    payload = {
        "development": {
            "gender": "MEN",
            "silhouette": "Long Sleeve Shirt (Crew Neck)",
            "seam": "Side Seam",
            "color_design": "Solid",
            "size": "S-XL",
            "pack_count": "2",
            "ideal_quantity": "1000",
            "coo": "INDIA",
            "fabric_finishing": "Wicking"
        },
        "fabrication": [{
            "fabric_type": "Jersey",
            "fabric_contents": "Cotton/Spandex 95/5",
            "using_part": "Whole Garment",
            "material_coo": "Import",
            "weight_gsm_override": None,
            "price_unit": "Price / Lbs",
            "price_value": 2.63,
            "fabric_finishing": "Wicking",
            "color_design": "Solid"
        }],
        "trims": [{
            "trims_type": "Main Label",
            "garment_part": "Neck",
            "usage_override": None,
            "price_override": None,
            "material_coo": "Domestic"
        }],
        "embellishments": [{
            "printing_embroidery": "Rubber_Print",
            "dimension": "3X3 cm",
            "usage_unit": 1
        }],
        "packing_label": {
            "display_packaging": "Basic STD  HNA",
            "transit_package": "36",
            "label_type": "Woven Label"
        },
        "manufacturing": {
            "made_in": "INDIA"
        }
    }

    r = requests.post(f"{BASE_URL}/api/calculate", json=payload)
    print(f"   Status: {r.status_code}")
    if r.ok:
        data = r.json()

        # Check if manufacturing exists
        if 'manufacturing' in data.get('outputs', {}):
            mfg = data['outputs']['manufacturing']
            print(f"   ✓ Manufacturing found: {mfg.get('country')} = ${mfg.get('total_cost')}")

        # Check if total_cost_summary exists
        if 'total_cost_summary' in data.get('outputs', {}):
            summary = data['outputs']['total_cost_summary']
            print(f"   ✓ Total Cost Summary found:")
            print(f"      Grand Total: ${summary.get('grand_total')}")

        print("\n   Full response structure:")
        print(f"   Keys in outputs: {list(data.get('outputs', {}).keys())}")

except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("If server is not running, start it with:")
print("  cd basicshirts_web")
print("  python server.py")
print("="*60)
