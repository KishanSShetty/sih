import re
import email
from email import policy
from email.parser import Parser
from typing import Dict, Any, List, Optional

try:
    import dkim
    HAS_DKIMPY = True
except ImportError:
    HAS_DKIMPY = False

def parse_raw_email_headers(raw_header_text: str) -> Dict[str, Any]:
    """
    Parses raw email header text to extract key authentication fields,
    Received IP chain, SPF/DKIM/DMARC status, and sender details.
    """
    if not raw_header_text or not isinstance(raw_header_text, str):
        return {
            "from": "unknown",
            "to": "unknown",
            "subject": "unknown",
            "return_path": "unknown",
            "message_id": "unknown",
            "spf_status": "NONE",
            "dkim_status": "NONE",
            "dmarc_status": "NONE",
            "origin_ip": "unknown",
            "received_chain": [],
            "auth_results": "No headers provided"
        }

    # Parse headers using standard library
    msg = Parser(policy=policy.default).parsestr(raw_header_text)

    sender_from = msg.get("From", "unknown")
    recipient_to = msg.get("To", "unknown")
    subject = msg.get("Subject", "unknown")
    return_path = msg.get("Return-Path", "unknown")
    message_id = msg.get("Message-ID", "unknown")
    auth_results = msg.get("Authentication-Results", "")

    # 1. Parse SPF / DKIM / DMARC from Authentication-Results header
    spf_status = "NONE"
    dkim_status = "NONE"
    dmarc_status = "NONE"

    auth_lower = auth_results.lower()
    
    # SPF match
    if "spf=pass" in auth_lower:
        spf_status = "PASS"
    elif "spf=fail" in auth_lower or "spf=softfail" in auth_lower:
        spf_status = "FAIL"
    elif "spf=neutral" in auth_lower or "spf=none" in auth_lower:
        spf_status = "NEUTRAL"

    # DKIM header status match
    if "dkim=pass" in auth_lower:
        dkim_status = "PASS"
    elif "dkim=fail" in auth_lower:
        dkim_status = "FAIL"

    # DMARC match
    if "dmarc=pass" in auth_lower:
        dmarc_status = "PASS"
    elif "dmarc=fail" in auth_lower:
        dmarc_status = "FAIL"

    # Fallback check for Received-SPF header
    received_spf = msg.get("Received-SPF", "").lower()
    if spf_status == "NONE" and received_spf:
        if "pass" in received_spf:
            spf_status = "PASS"
        elif "fail" in received_spf:
            spf_status = "FAIL"

    # 2. Extract Received IP Chain
    received_headers = msg.get_all("Received") or []
    received_chain = []
    origin_ip = "unknown"

    ip_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    for r_hdr in received_headers:
        found_ips = ip_regex.findall(str(r_hdr))
        for ip in found_ips:
            # Skip private/loopback IPs
            if not (ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172.16.")):
                received_chain.append(ip)

    if received_chain:
        # The earliest non-private IP in Received chain is the likely originating IP
        origin_ip = received_chain[-1]

    # 3. Optional Cryptographic DKIM Verification (If raw email bytes available)
    crypto_dkim_verified = False
    if HAS_DKIMPY and raw_header_text:
        try:
            # dkim.verify requires raw bytes containing both headers and body
            raw_bytes = raw_header_text.encode('utf-8', errors='ignore')
            if b"\r\n\r\n" in raw_bytes or b"\n\n" in raw_bytes:
                crypto_dkim_verified = dkim.verify(raw_bytes)
                if crypto_dkim_verified:
                    dkim_status = "PASS (VERIFIED)"
        except Exception:
            crypto_dkim_verified = False

    return {
        "from": str(sender_from),
        "to": str(recipient_to),
        "subject": str(subject),
        "return_path": str(return_path),
        "message_id": str(message_id),
        "spf_status": spf_status,
        "dkim_status": dkim_status,
        "dmarc_status": dmarc_status,
        "origin_ip": origin_ip,
        "received_chain": received_chain,
        "auth_results": str(auth_results) if auth_results else "Header parsed"
    }

def calculate_auth_score(auth_summary: Dict[str, Any]) -> float:
    """
    Computes S_auth authentication penalty score (0.0 = All Pass / Safe, 1.0 = All Fail / Dangerous)
    """
    spf = auth_summary.get("spf_status", "NONE")
    dkim_s = auth_summary.get("dkim_status", "NONE")
    dmarc = auth_summary.get("dmarc_status", "NONE")

    spf_penalty = 0.0 if "PASS" in spf else (0.8 if "FAIL" in spf else 0.3)
    dkim_penalty = 0.0 if "PASS" in dkim_s else (0.8 if "FAIL" in dkim_s else 0.3)
    dmarc_penalty = 0.0 if "PASS" in dmarc else (1.0 if "FAIL" in dmarc else 0.4)

    # Weighted Auth Score: SPF (30%), DKIM (30%), DMARC (40%)
    s_auth = (0.30 * spf_penalty) + (0.30 * dkim_penalty) + (0.40 * dmarc_penalty)
    return round(min(max(s_auth, 0.0), 1.0), 4)
