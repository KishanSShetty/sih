import requests
import json

url = "http://127.0.0.1:8002/api/v1/detect"
payload = {
    "text": "Your account session will expire immediately. Please update your credentials now to avoid being locked out permanentely.",
    "source": "manual"
}

resp = requests.post(url, json=payload)
print(json.dumps(resp.json(), indent=2))
