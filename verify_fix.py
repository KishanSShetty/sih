
import urllib.request
import json
import time

url = "http://127.0.0.1:8002/api/v1/detect"
headers = {"Content-Type": "application/json"}

test_cases = [
    {
        "name": "Financial Phishing",
        "url": "http://secure-chase-online-banking-verify.top/login",
        "expected_score": 0.90
    },
    {
        "name": "Credential Harvesting (Microsoft)",
        "url": "https://microsoft-office-365-update.xyz/account/repair",
        "expected_score": 0.90
    },
    {
        "name": "Piracy Site",
        "url": "https://tamilrockers-free-movie-download.com/latest-hd",
        "expected_score": 0.95
    },
    {
        "name": "Suspicious TLD (.date)",
        "url": "http://my-gift-card-win.date/claim",
        "expected_score": 0.85
    }
]

print("--- STARTING VERIFICATION ---")
all_passed = True

for case in test_cases:
    data = {"text": case["url"]}
    json_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                resp_body = response.read()
                data = json.loads(resp_body)
                score = data.get('max_risk_score', 0)
                
                print(f"\nTEST: {case['name']}")
                print(f"URL: {case['url']}")
                print(f"Score: {score} (Expected >= {case['expected_score']})")
                
                if score >= case['expected_score']:
                    print("✅ PASS")
                else:
                    print("❌ FAIL")
                    all_passed = False
                    
                # Print explanation
                explanation = [l for l in data.get('labels', {}).values() if l['probability'] > 0]
                # print(f"Explanation: {explanation}")

            else:
                print(f"Error: {response.status}")
                all_passed = False
    except Exception as e:
        print(f"Request failed for {case['name']}: {e}")
        all_passed = False

print("\n--------------------------------")
if all_passed:
    print("🎉 ALL TESTS PASSED")
else:
    print("⚠️ SOME TESTS FAILED")
