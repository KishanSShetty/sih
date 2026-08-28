import dns.resolver
from typing import Dict, Any, List
import whois
from datetime import datetime
import threading

def analyze_sender_domain_dns(domain: str) -> Dict[str, Any]:
    """
    Performs DNS record lookups (MX, TXT/SPF, DMARC) for a sender domain using dnspython.
    Additionally fetches WHOIS data to determine domain age and registrar.
    """
    if not domain or not isinstance(domain, str) or "." not in domain:
        return {
            "domain": domain or "unknown",
            "has_mx": False,
            "has_spf": False,
            "has_dmarc": False,
            "mx_records": [],
            "spf_record": "None",
            "dmarc_record": "None",
            "domain_age": "unknown",
            "domain_age_days": -1,
            "whois_registrar": "UNKNOWN",
            "dns_risk_score": 0.5
        }

    domain_clean = domain.strip().lower()

    mx_records = []
    has_mx = False
    try:
        answers_mx = dns.resolver.resolve(domain_clean, 'MX', lifetime=3.0)
        mx_records = [str(r.exchange) for r in answers_mx]
        has_mx = len(mx_records) > 0
    except Exception:
        has_mx = False

    spf_record = "None"
    has_spf = False
    try:
        answers_txt = dns.resolver.resolve(domain_clean, 'TXT', lifetime=3.0)
        for r in answers_txt:
            txt_str = str(r)
            if "v=spf1" in txt_str.lower():
                spf_record = txt_str
                has_spf = True
                break
    except Exception:
        has_spf = False

    dmarc_record = "None"
    has_dmarc = False
    try:
        dmarc_domain = f"_dmarc.{domain_clean}"
        answers_dmarc = dns.resolver.resolve(dmarc_domain, 'TXT', lifetime=3.0)
        for r in answers_dmarc:
            txt_str = str(r)
            if "v=dmarc1" in txt_str.lower():
                dmarc_record = txt_str
                has_dmarc = True
                break
    except Exception:
        has_dmarc = False

    # WHOIS Fetch with timeout (to prevent hanging real-time scanning)
    domain_age_days = -1
    whois_registrar = "UNKNOWN"
    domain_age_str = "unknown"
    
    def fetch_whois():
        nonlocal domain_age_days, whois_registrar, domain_age_str
        try:
            w = whois.whois(domain_clean)
            if w.registrar:
                whois_registrar = str(w.registrar)
            
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                delta = datetime.now() - creation_date
                domain_age_days = delta.days
                
                if domain_age_days < 30:
                    domain_age_str = f"{domain_age_days} Days (NEW)"
                elif domain_age_days < 365:
                    domain_age_str = f"{domain_age_days // 30} Months"
                else:
                    domain_age_str = f"{domain_age_days // 365} Years"
        except Exception as e:
            print(f"WHOIS lookup failed for {domain_clean}: {e}")

    # Run WHOIS in a thread with 2-second timeout
    whois_thread = threading.Thread(target=fetch_whois)
    whois_thread.start()
    whois_thread.join(timeout=2.0)

    # DNS Infrastructure Risk Penalty (No MX = 0.8, No SPF/DMARC = +0.2)
    dns_risk_score = 0.0
    if not has_mx:
        dns_risk_score += 0.5
    if not has_spf:
        dns_risk_score += 0.25
    if not has_dmarc:
        dns_risk_score += 0.25

    return {
        "domain": domain_clean,
        "has_mx": has_mx,
        "has_spf": has_spf,
        "has_dmarc": has_dmarc,
        "mx_records": mx_records[:3],
        "spf_record": spf_record,
        "dmarc_record": dmarc_record,
        "domain_age": domain_age_str,
        "domain_age_days": domain_age_days,
        "whois_registrar": whois_registrar,
        "dns_risk_score": round(min(dns_risk_score, 1.0), 2)
    }
