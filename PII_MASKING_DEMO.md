# PII Masking Demo Guide for Teachers
# How to demonstrate privacy protection features

## Overview
This guide shows how SecureSentinel automatically masks Personally Identifiable Information (PII) 
in analyzed text to protect user privacy.

## What Gets Masked?
- Email addresses → [EMAIL_REDACTED]
- Phone numbers (10 digits) → [PHONE_REDACTED]

## Demo Scenarios

### Scenario 1: Phishing Email with PII
**Original Text:**
```
Dear Customer,

Your PayPal account has been suspended. Please verify your identity immediately.

Contact us at support@paypal-verify.com or call 9876543210 to restore access.

Your account email john.doe@gmail.com will be permanently locked in 24 hours.

Click here to verify: http://paypal-secure-login.tk/verify
```

**What Happens:**
1. Backend analyzes the text
2. Detects high risk (phishing)
3. Masks PII before storing:
   - support@paypal-verify.com → [EMAIL_REDACTED]
   - 9876543210 → [PHONE_REDACTED]
   - john.doe@gmail.com → [EMAIL_REDACTED]

**Stored in Database:**
```
Dear Customer,

Your PayPal account has been suspended. Please verify your identity immediately.

Contact us at [EMAIL_REDACTED] or call [PHONE_REDACTED] to restore access.

Your account email [EMAIL_REDACTED] will be permanently locked in 24 hours.

Click here to verify: http://paypal-secure-login.tk/verify
```

---

### Scenario 2: SMS Scam with Phone Number
**Original Text:**
```
URGENT: Your bank account has been compromised!
Call 1234567890 immediately to secure your funds.
Reply with your email: customer@bank.com
```

**Stored in Database:**
```
URGENT: Your bank account has been compromised!
Call [PHONE_REDACTED] immediately to secure your funds.
Reply with your email: [EMAIL_REDACTED]
```

---

### Scenario 3: Temporal Analysis Input
**Original Text:**
```
Your Netflix subscription payment failed.
Update your payment method at billing@netflix-update.com
or contact us at 5551234567 within 24 hours.
```

**Stored in Database:**
```
Your Netflix subscription payment failed.
Update your payment method at [EMAIL_REDACTED]
or contact us at [PHONE_REDACTED] within 24 hours.
```

---

## How to Demo This to Teachers

### Step 1: Enable PII Masking
1. Open Dashboard → Settings (or Privacy Center)
2. Enable "PII Masking"
3. Confirm it's active

### Step 2: Analyze Test Text
1. Go to **Temporal Analysis** page
2. Paste one of the test scenarios above
3. Click "Execute Analysis"

### Step 3: View Masked Data
**Option A: Dashboard Activity Log**
1. Go to Dashboard → Activity Insights
2. Click on the analyzed entry
3. Show that emails/phones are masked

**Option B: Export Database**
1. Use the export script (see below)
2. Open the CSV file
3. Show the masked entries

### Step 4: Compare Before/After
Create a side-by-side comparison:
- **Left**: Original input (show in notepad)
- **Right**: Database export (show masked version)

---

## Export Database for Demo

Run this command to export all scan results:
```bash
python export_scans.py
```

This creates `scan_results_export.csv` with columns:
- ID
- URL (with PII masked)
- Domain
- Risk Score
- Risk Level
- Explanation
- Timestamp

---

## Live Demo Script

**Say to Teachers:**

1. "I'll analyze a phishing email that contains sensitive information"
2. *Paste the email with real-looking email/phone*
3. "The system detects it as high-risk phishing"
4. "Now let me show you what gets stored in the database"
5. *Open exported CSV or Activity Log*
6. "Notice that all email addresses are replaced with [EMAIL_REDACTED]"
7. "And phone numbers are replaced with [PHONE_REDACTED]"
8. "This ensures that even if the database is compromised, no real PII is exposed"

---

## Key Points to Emphasize

✅ **Privacy by Design**: PII is masked BEFORE storage
✅ **Automatic**: No manual intervention needed
✅ **Irreversible**: Original PII cannot be recovered
✅ **Compliance**: Helps meet GDPR/privacy regulations
✅ **Selective**: Only masks PII, keeps threat data intact

---

## Additional Demo Ideas

### 1. Browser Extension Demo
- Visit a fake phishing site with email in URL
- Show extension blocks it
- Check dashboard - email is masked

### 2. Real-time Comparison
- Open two windows side-by-side
- Left: Temporal Analysis input
- Right: Database viewer showing masked output

### 3. Settings Toggle Demo
- Show with PII masking OFF (stores real data)
- Enable PII masking
- Analyze same text again
- Show difference in storage

---

## Sample Test Emails for Demo

### Test 1: Banking Scam
```
ALERT: Unusual activity detected on your account.
Verify your identity at security@chase-bank-verify.com
Or call our fraud department: 8005551234
Your registered email: victim@example.com
```

### Test 2: Tech Support Scam
```
Microsoft Security Alert!
Your computer has been infected with malware.
Call our support team immediately: 1-800-MICROSOFT (1800642767638)
Or email: support@microsoft-security.net
Reference ID: victim.name@company.com
```

### Test 3: Package Delivery Scam
```
Your package delivery failed!
Track your shipment: http://fedex-tracking.tk/track?email=customer@gmail.com
Contact support: 9998887776
Redeliver to: john.smith@workplace.com
```

---

## Expected Questions from Teachers

**Q: Can you recover the original PII?**
A: No, it's permanently masked. This is by design for privacy.

**Q: What if legitimate emails need to be stored?**
A: You can disable PII masking in settings for specific use cases.

**Q: Does masking affect threat detection?**
A: No, analysis happens BEFORE masking. Detection accuracy is unaffected.

**Q: What about other PII like names or addresses?**
A: Currently masks emails and phones. Can be extended to mask more patterns.

---

## Conclusion

This demo shows that SecureSentinel prioritizes user privacy by:
1. Detecting threats accurately
2. Masking sensitive information
3. Storing only anonymized data
4. Providing transparency through exports

Perfect for academic presentations on privacy-preserving security systems!
