"""
Real-time Email Scans API
Provides live feed of email scans for Temporal Analysis page
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from typing import List, Dict, Any
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/email-scans", tags=["email-scans"])

@router.get("/recent", response_model=List[Dict[str, Any]])
async def get_recent_email_scans(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get recent email scans for real-time display
    Filters for scans from Gmail source
    """
    try:
        # Get scans from last hour that came from Gmail
        one_hour_ago = datetime.now() - timedelta(hours=1)
        
        scans = db.query(models.ScanResult).filter(
            models.ScanResult.timestamp >= one_hour_ago
        ).order_by(
            models.ScanResult.timestamp.desc()
        ).limit(limit).all()
        
        result = []
        for scan in scans:
            # Check if this is an email scan (contains "Subject:" or "From:" or has sender populated)
            is_email = ("Subject:" in scan.url or "From:" in scan.url) or (scan.sender and scan.sender != "unknown")
            
            if is_email:
                subject = scan.subject if scan.subject and scan.subject != "unknown" else ""
                sender = scan.sender if scan.sender and scan.sender != "unknown" else ""
                
                # Fallback to URL parsing if old records
                if not subject and not sender:
                    lines = scan.url.split('\n')
                    for line in lines:
                        if line.startswith("Subject:"):
                            subject = line.replace("Subject:", "").strip()
                        elif line.startswith("From:"):
                            sender = line.replace("From:", "").strip()
                
                result.append({
                    "id": scan.id,
                    "subject": subject,
                    "sender": sender,
                    "risk_score": scan.risk_score,
                    "risk_level": scan.risk_level,
                    "explanation": scan.explanation,
                    "timestamp": scan.timestamp.isoformat() if scan.timestamp else None,
                    "spf_status": getattr(scan, "spf_status", "UNKNOWN"),
                    "dkim_status": getattr(scan, "dkim_status", "UNKNOWN"),
                    "dmarc_status": getattr(scan, "dmarc_status", "UNKNOWN"),
                    "origin_ip": getattr(scan, "origin_ip", "unknown"),
                    "received_chain": getattr(scan, "received_chain", "[]"),
                    "auth_results": getattr(scan, "auth_results", "UNKNOWN"),
                    "trust_score": getattr(scan, "trust_score", 0.0),
                    "category": getattr(scan, "category", "UNKNOWN"),
                    "domain_age_days": getattr(scan, "domain_age_days", -1),
                    "whois_registrar": getattr(scan, "whois_registrar", "UNKNOWN")
                })
        
        return result
        
    except Exception as e:
        print(f"Error fetching email scans: {e}")
        return []

@router.get("/stats")
async def get_email_scan_stats(db: Session = Depends(get_db)):
    """
    Get statistics about email scans
    """
    try:
        # Get scans from last 24 hours
        one_day_ago = datetime.now() - timedelta(days=1)
        
        total_scans = db.query(models.ScanResult).filter(
            models.ScanResult.timestamp >= one_day_ago
        ).count()
        
        phishing_detected = db.query(models.ScanResult).filter(
            models.ScanResult.timestamp >= one_day_ago,
            models.ScanResult.risk_score >= 0.7
        ).count()

        suspicious = db.query(models.ScanResult).filter(
            models.ScanResult.timestamp >= one_day_ago,
            models.ScanResult.risk_score >= 0.4,
            models.ScanResult.risk_score < 0.7
        ).count()

        safe = max(total_scans - phishing_detected - suspicious, 0)
        
        return {
            "total_scans": total_scans,
            "high_risk": phishing_detected,
            "suspicious": suspicious,
            "safe_emails": safe,
            "total_emails_scanned_24h": total_scans,
            "phishing_detected_24h": phishing_detected,
            "safe_emails_24h": safe,
            "detection_rate": (phishing_detected / total_scans * 100) if total_scans > 0 else 0
        }
        
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "total_scans": 0,
            "high_risk": 0,
            "suspicious": 0,
            "safe_emails": 0,
            "total_emails_scanned_24h": 0,
            "phishing_detected_24h": 0,
            "safe_emails_24h": 0,
            "detection_rate": 0
        }
