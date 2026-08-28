"""
Test PII Masking Directly
"""
import re

test_text = """URGENT: Your Chase Bank account has been suspended.
Contact us at security@chase-verify.com or calling our fraud department at 8005551234.
Your registered email john.doe@gmail.com will be locked."""

print("Original Text:")
print(test_text)
print("\n" + "="*50 + "\n")

# Test email masking
masked_text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REDACTED]', test_text)
print("After Email Masking:")
print(masked_text)
print("\n" + "="*50 + "\n")

# Test phone masking
masked_text = re.sub(r'\b\d{10}\b', '[PHONE_REDACTED]', masked_text)
print("After Phone Masking:")
print(masked_text)
print("\n" + "="*50 + "\n")

# Check if masking worked
if '[EMAIL_REDACTED]' in masked_text and '[PHONE_REDACTED]' in masked_text:
    print("✅ PII Masking regex is working correctly!")
else:
    print("❌ PII Masking regex failed!")
    if '[EMAIL_REDACTED]' not in masked_text:
        print("   - Email masking failed")
    if '[PHONE_REDACTED]' not in masked_text:
        print("   - Phone masking failed")
