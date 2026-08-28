from typing import Dict, Any, List
import re

def categorize_intent(subject: str, text: str) -> str:
    """
    Lightweight intent classifier to tag emails based on content.
    """
    subject_lower = subject.lower()
    text_lower = text.lower()
    combined = subject_lower + " " + text_lower

    if any(w in combined for w in ['receipt', 'invoice', 'payment received', 'order confirmation', 'transaction', 'billing']):
        return "TRANSACTIONAL"
    if any(w in combined for w in ['login', 'password', 'verify account', '2fa', 'verification code', 'sign in']):
        return "ACCOUNT_NOTIFICATION"
    if any(w in combined for w in ['shipped', 'delivery', 'tracking', 'package']):
        return "DELIVERY"
    if any(w in combined for w in ['discount', 'offer', 'sale', 'save', 'cashback', 'promotional', 'free']):
        return "PROMOTIONAL"
    
    return "UNKNOWN"

def fuse_email_risk_scores(
    ml_content_score: float,
    ml_signals: Dict[str, float],
    auth_summary: Dict[str, Any],
    dns_summary: Dict[str, Any],
    links_info: List[Dict[str, Any]],
    impersonation_score: float = 0.0,
    email_context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Implements the Context-Aware Risk Fusion Engine (V7).
    De-couples Text Threat from Infrastructure Trust.
    """
    if email_context is None:
        email_context = {}
        
    subject = email_context.get("subject", "unknown")
    text = email_context.get("text", "")
    is_whitelisted = email_context.get("is_whitelisted", False)
    
    if is_whitelisted:
        return {
            "final_email_score": 0.0,
            "risk_level": "SAFE",
            "threat_classification": "Whitelisted Sender Domain",
            "trust_score": 100.0,
            "category": "KNOWN_SAFE",
            "weights": { "ml_content": 0.0, "auth": 0.0, "dns": 0.0 },
            "factors": ["+ Verified legitimate sender domain"]
        }

    category = categorize_intent(subject, text)
    factors = []

    # --- 1. BASE THREAT RISK ---
    # ML Signals
    t_urgency = ml_signals.get("urgency", 0.0)
    t_fear = ml_signals.get("fear", 0.0)
    t_authority = ml_signals.get("authority", 0.0)
    
    T_score = ml_content_score  # Overall text threat
    P_score = impersonation_score # Impersonation evidence
    
    # Link Analysis (L_score)
    L_score = 0.0
    domain_mismatch_found = False
    sender_domain = email_context.get("sender_domain", "").lower()
    
    for link in links_info:
        dest_domain = link.get("domain", "").lower()
        if dest_domain and sender_domain and dest_domain != sender_domain:
            # Simple mismatch heuristic (ignoring subdomains for now)
            if not dest_domain.endswith(f".{sender_domain}") and not sender_domain.endswith(f".{dest_domain}"):
                domain_mismatch_found = True
                L_score += 0.5
        if link.get("is_ip", False):
            L_score += 0.8
            
    L_score = min(L_score, 1.0)
    
    # Behavior (B_score) - combined urgency/fear
    B_score = (t_urgency + t_fear) / 2.0
    
    # Base Risk Fusion
    base_risk = (0.30 * T_score) + (0.15 * P_score) + (0.20 * L_score) + (0.10 * B_score)

    # --- 2. TRUST SCORE ---
    spf = auth_summary.get("spf_status", "NONE")
    dkim = auth_summary.get("dkim_status", "NONE")
    dmarc = auth_summary.get("dmarc_status", "NONE")
    
    A_score = 0.0 # Authentication Trust
    if "PASS" in spf: A_score += 0.33; factors.append("+ SPF PASS")
    elif "FAIL" in spf: factors.append("- SPF FAIL")
    
    if "PASS" in dkim: A_score += 0.33; factors.append("+ DKIM PASS")
    elif "FAIL" in dkim: factors.append("- DKIM FAIL")
        
    if "PASS" in dmarc: A_score += 0.34; factors.append("+ DMARC PASS")
    elif "FAIL" in dmarc: factors.append("- DMARC FAIL")
        
    # Infrastructure Trust
    D_trust = 0.0
    if dns_summary.get("has_mx", False): D_trust += 0.5
    else: factors.append("- Missing MX Records")
        
    if dns_summary.get("has_spf", False) or dns_summary.get("has_dmarc", False): D_trust += 0.5
    
    # Link consistency Trust
    C_trust = 1.0 if not domain_mismatch_found else 0.0
    if domain_mismatch_found:
        factors.append("- Destination links do not match sender domain")
    elif links_info and sender_domain:
        factors.append("+ Destination links match sender domain")
        
    # Domain Age Trust
    W_trust = 0.0
    domain_age_days = dns_summary.get("domain_age_days", -1)
    if domain_age_days >= 0:
        if domain_age_days < 30:
            W_trust = -0.4
            factors.append(f"- Domain registered very recently ({domain_age_days} days ago)")
        elif domain_age_days > 365:
            W_trust = 0.1
            factors.append("+ Domain is established (> 1 year)")
    
    trust_score_val = (0.40 * A_score) + (0.30 * D_trust) + (0.30 * C_trust) + W_trust
    trust_score_val = max(0.0, min(1.0, trust_score_val))
    
    # --- 3. CONTEXTUAL ADJUSTMENT ---
    context_adjustment = 0.0
    
    if category in ["TRANSACTIONAL", "ACCOUNT_NOTIFICATION", "PROMOTIONAL"]:
        if trust_score_val >= 0.7:
            # Legitimate intent, strong trust -> Dampen threat language (it's normal)
            context_adjustment -= 0.30
            factors.append(f"+ Legitimate {category.lower()} context verified by authentication")
        elif trust_score_val < 0.4 or domain_mismatch_found:
            # Transactional language but poor trust -> Phishing signal
            context_adjustment += 0.20
            factors.append(f"- Suspicious {category.lower()} language with unverified infrastructure")

    # Final Risk
    final_score = base_risk - (0.2 * trust_score_val) + context_adjustment
    final_score = min(max(final_score, 0.0), 1.0)
    
    # --- 4. SAFETY FLOORS (TRUST DOES NOT OVERRIDE CRITICAL THREATS) ---
    if domain_mismatch_found and ("FAIL" in dmarc or "FAIL" in spf):
        final_score = max(final_score, 0.85)
        factors.append("- CRITICAL: Auth failure combined with domain mismatch")
        
    if P_score > 0.8:
        final_score = max(final_score, 0.80)
        factors.append("- CRITICAL: High impersonation confidence")

    final_score = round(final_score, 4)
    trust_score_out = round(trust_score_val * 100, 1)

    # Assign Status Level
    if final_score >= 0.70:
        risk_level = "CRITICAL" if final_score >= 0.85 else "HIGH_RISK"
        classification = "High-Risk Email Threat (Phishing / Impersonation)"
    elif final_score >= 0.40:
        risk_level = "SUSPICIOUS"
        classification = "Suspicious Email Characteristics"
    else:
        risk_level = "SAFE"
        classification = "Clean / Nominal Risk"

    if not factors:
        factors.append("Nominal email indicators")

    return {
        "final_email_score": final_score,
        "trust_score": trust_score_out,
        "category": category,
        "risk_level": risk_level,
        "threat_classification": classification,
        "weights": { "base_risk": round(base_risk,2), "trust_deduction": round(trust_score_val,2), "context_adj": round(context_adjustment,2) },
        "factors": factors
    }
