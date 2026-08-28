import requests
import json

url = "http://127.0.0.1:8002/api/v1/detect"

samples = [
    {
        "name": "📦 Legitimate Marketing (High Urgency + Sale)",
        "text": "Flash Sale! 70% off everything for the next 2 hours only. Register now to claim your discount coupon!",
        "source": "content"
    }
]

for sample in samples:
    print(f"\n--- Testing: {sample['name']} ---")
    response = requests.post(url, json={
        "text": sample["text"],
        "source": sample["source"]
    })
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")
