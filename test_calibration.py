import requests
import json

url = "http://127.0.0.1:8002/api/v1/detect"

samples = [
    {
        "name": "🔥 Malicious Phishing (High Urgency + Fear)",
        "text": "Your account has been locked due to suspicious activity. Verify your identity in the next 60 minutes or it will be permanently deleted.",
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
