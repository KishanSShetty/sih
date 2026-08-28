import requests
try:
    resp = requests.get("http://127.0.0.1:8002/health")
    print(f"Health check: {resp.status_code}")
    print(resp.json())
except Exception as e:
    print(f"Error: {e}")

try:
    resp = requests.post("http://127.0.0.1:8002/api/v1/detect", json={"text": "test", "source": "test"})
    print(f"Detect check: {resp.status_code}")
    print(resp.json())
except Exception as e:
    print(f"Error: {e}")
