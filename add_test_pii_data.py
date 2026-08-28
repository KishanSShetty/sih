"""
Add Test Data with PII for Demo
This script adds sample phishing scenarios with PII to demonstrate masking
"""

import requests
import time

API_BASE = "http://127.0.0.1:8000/api/v1"

# Test scenarios with PII
test_scenarios = [
    {
        "name": "Banking Phishing",
        "text": """URGENT: Your Chase Bank account has been suspended due to suspicious activity.
        
Please verify your identity immediately by contacting us at security@chase-verify.com
or calling our fraud department at 8005551234.

Your registered email john.doe@gmail.com will be locked in 24 hours if not verified.

Click here to restore access: http://chase-secure-login.tk/verify"""
    },
    {
        "name": "PayPal Scam",
        "text": """Dear PayPal Customer,

Your account has been limited. To restore full access, please update your information.

Contact support: billing@paypal-security.net
Phone: 9876543210
Your account: customer@example.com

Verify now: http://paypal-verify-account.com/login"""
    },
    {
        "name": "Netflix Billing Scam",
        "text": """Your Netflix subscription payment has failed.

Update your payment method immediately to avoid service interruption.

Contact: support@netflix-billing.com
Call: 5551234567
Account email: user@company.com

Update payment: http://netflix-update-payment.tk"""
    },
    {
        "name": "Microsoft Tech Support Scam",
        "text": """CRITICAL SECURITY ALERT

Your Windows license has expired. Your computer is at risk!

Call Microsoft Support: 1-800-WINDOWS (18009463697)
Email: support@microsoft-security.net
Reference: admin@workplace.com

Renew now: http://microsoft-renew-license.com"""
    },
    {
        "name": "Package Delivery Scam",
        "text": """FedEx Delivery Notification

Your package delivery failed. Redeliver by confirming your details.

Track shipment: tracking@fedex-delivery.net
Call: 8887776665
Recipient: recipient@home.com

Reschedule: http://fedex-tracking.tk/redeliver"""
    }
]

def add_test_data():
    """Add test scenarios to database"""
    print("🧪 Adding Test Data with PII for Demo")
    print("=" * 50)
    print()
    
    success_count = 0
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"[{i}/{len(test_scenarios)}] Testing: {scenario['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/detect",
                json={"text": scenario["text"], "source": "demo"},
                timeout=10
            )
            
            if response.ok:
                data = response.json()
                risk = data.get('global_risk_score', 0)
                print(f"   ✅ Added - Risk Score: {risk*100:.1f}%")
                success_count += 1
            else:
                print(f"   ❌ Failed - Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print()
    print("=" * 50)
    print(f"✅ Successfully added {success_count}/{len(test_scenarios)} test scenarios")
    print()
    print("📊 Next Steps:")
    print("   1. Run: python export_scans.py")
    print("   2. Open the generated CSV file")
    print("   3. Look for [EMAIL_REDACTED] and [PHONE_REDACTED]")
    print()
    print("💡 You can also view the data in:")
    print("   - Dashboard → Activity Insights")
    print("   - Temporal Analysis → Session Trace Log")

if __name__ == "__main__":
    add_test_data()
