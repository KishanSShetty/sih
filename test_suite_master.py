import requests
import json
import time
import sys

# --- COMPATIBILITY SHIM ---
# This ensures that even if you have mixed library versions, the script won't crash
try:
    import pyparsing
    if hasattr(pyparsing, "ParserElement"):
        pe = pyparsing.ParserElement
        mapping = [("set_name", "setName"), ("set_results_name", "setResultsName")]
        for snake, camel in mapping:
            if not hasattr(pe, snake) and hasattr(pe, camel): setattr(pe, snake, getattr(pe, camel))
            if not hasattr(pe, camel) and hasattr(pe, snake): setattr(pe, camel, getattr(pe, snake))
except ImportError:
    pass

# Configuration
API_URL = "http://127.0.0.1:8002/api/v1/detect"

TEST_CASES = [
    {
        "type": "🔥 PHISHING (High Threat)",
        "text": "URGENT: Your account session will expire in 10 minutes. Please verify your credentials immediately at secure-login-sentinel.com to avoid permanent suspension."
    },
    {
        "type": "📊 MARKETING (High Pressure)",
        "text": "Flash Sale! Our biggest discount of the year ends in 2 hours. Register now for a 70% off coupon on all services. Don't wait!"
    },
    {
        "type": "✅ SAFE (Clean)",
        "text": "Hi team, please find the meeting notes attached for our collaboration session on Friday. Let's touch base next week."
    },
    {
        "type": "🕵️ BRAND IMPERSONATION",
        "text": "Microsoft Security Alert: We detected an unauthorized login to your Microsoft Account from a new device. Verify your identity now: login-microsoft-security.net"
    }
]

def run_test_suite():
    print("="*60)
    print("🛡️  SECURESENTINEL MASTER TEST SUITE")
    print("="*60)
    print(f"Testing against: {API_URL}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)

    results = []
    
    for i, case in enumerate(TEST_CASES):
        print(f"\n[{i+1}/{len(TEST_CASES)}] Testing {case['type']}...")
        try:
            start_time = time.time()
            response = requests.post(API_URL, json={"text": case["text"], "source": "master_test_suite"}, timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "UNKNOWN")
                score = data.get("global_risk_score", 0.0)
                summary = data.get("explanation_summary", "No summary provided")
                
                # Check for triggers
                signals = data.get("signals", {})
                found_triggers = []
                for label, info in signals.items():
                    if info["probability"] > 0.4:
                        found_triggers.append(label.upper())

                results.append({
                    "case": case["type"],
                    "status": status,
                    "score": f"{score:.2f}",
                    "latency": f"{elapsed:.2f}s",
                    "triggers": ", ".join(found_triggers) if found_triggers else "NONE"
                })
                
                print(f"   ✅ SUCCESS: Score={score:.2f} | Status={status}")
                print(f"   💡 Result: {summary}")
            else:
                print(f"   ❌ FAILED: API returned status {response.status_code}")
                print(f"   📝 Response: {response.text}")
        except requests.exceptions.ConnectionError:
            print("   ⚠️  ERROR: Could not connect to the backend server. Is it running on port 8002?")
            break
        except Exception as e:
            print(f"   ⚠️  CRITICAL ERROR: {str(e)}")

    if results:
        print("\n" + "="*85)
        print(f"{'TEST CASE':<25} | {'STATUS':<12} | {'SCORE':<8} | {'LATENCY':<8} | {'TOP SIGNALS'}")
        print("-"*85)
        for r in results:
            print(f"{r['case']:<25} | {r['status']:<12} | {r['score']:<8} | {r['latency']:<8} | {r['triggers']}")
        print("="*85)
    else:
        print("\n❌ No results to display. Please verify backend connectivity.")

if __name__ == "__main__":
    run_test_suite()
