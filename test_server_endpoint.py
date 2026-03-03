"""
Test the server endpoint
"""
import requests
import json

url = "http://127.0.0.1:8000/api/calculate"

payload = {
    "development": {
        "gender": "Men",
        "silhouette": "Tank top/A Shirt",
        "seam": "Side Seam",
        "color_design": "Solid",
        "size": "S-XL",
        "pack_count": "1",
        "ideal_quantity": "More than 100,000",
        "coo": "BANGLADESH",
        "fabric_finishing": "Bio-Wash"
    },
    "fabrication": [{
        "fabric_type": "Jersey",
        "fabric_contents": "Cotton/Spandex 95/5",
        "using_part": "Body",
        "weight_gsm_override": "",
        "price_unit": "Price / YD",
        "price_value": "",
        "material_coo": "Local"
    }],
    "trims": [],
    "embellishments": [],
    "packing_label": {}
}

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
    print(f"\nResponse text:")
    print(response.text if 'response' in locals() else "No response")
