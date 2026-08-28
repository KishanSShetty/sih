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
            # Check if this is an email scan (contains "Subject:" or "From:")
            is_email = "Subject:" in scan.url or "From:" in scan.url
            
            if is_email:
                # Extract email metadata
                lines = scan.url.split('\n')
                subject = ""
                sender = ""
                
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
                    "timestamp": scan.timestamp.isoformat(),
                    "content_preview": scan.url[:200] + "..." if len(scan.url) > 200 else scan.url
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
        
        return {
            "total_emails_scanned_24h": total_scans,
            "phishing_detected_24h": phishing_detected,
            "safe_emails_24h": total_scans - phishing_detected,
            "detection_rate": (phishing_detected / total_scans * 100) if total_scans > 0 else 0
        }
        
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "total_emails_scanned_24h": 0,
            "phishing_detected_24h": 0,
            "safe_emails_24h": 0,
            "detection_rate": 0
        }
