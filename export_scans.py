"""
Export Scan Results to CSV for PII Masking Demo
This script exports all scan results from the database to a CSV file
"""

import csv
from datetime import datetime
from backend.app.database import SessionLocal
from backend.app import models

def export_scan_results():
    """Export all scan results to CSV file"""
    db = SessionLocal()
    
    try:
        # Get all scan results
        scans = db.query(models.ScanResult).order_by(models.ScanResult.timestamp.desc()).all()
        
        # Create CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_results_export_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'URL/Text', 'Domain', 'Risk Score', 'Risk Level', 'Explanation', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for scan in scans:
                writer.writerow({
                    'ID': scan.id,
                    'URL/Text': scan.url[:100] + '...' if len(scan.url) > 100 else scan.url,
                    'Domain': scan.domain,
                    'Risk Score': f"{scan.risk_score:.2f}",
                    'Risk Level': scan.risk_level,
                    'Explanation': scan.explanation,
                    'Timestamp': scan.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        print(f"✅ Exported {len(scans)} scan results to: {filename}")
        print(f"\n📊 Summary:")
        print(f"   - Total scans: {len(scans)}")
        
        # Count masked entries
        masked_count = sum(1 for s in scans if '[EMAIL_REDACTED]' in s.url or '[PHONE_REDACTED]' in s.url)
        print(f"   - Entries with masked PII: {masked_count}")
        
        # Risk level breakdown
        safe = sum(1 for s in scans if s.risk_level == 'SAFE')
        suspicious = sum(1 for s in scans if s.risk_level == 'SUSPICIOUS')
        high_risk = sum(1 for s in scans if s.risk_level == 'HIGH_RISK')
        
        print(f"\n   Risk Level Breakdown:")
        print(f"   - SAFE: {safe}")
        print(f"   - SUSPICIOUS: {suspicious}")
        print(f"   - HIGH_RISK: {high_risk}")
        
        print(f"\n💡 Open '{filename}' in Excel or any text editor to view the data")
        print(f"   Look for [EMAIL_REDACTED] and [PHONE_REDACTED] to see PII masking in action!")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔒 SecureSentinel - Scan Results Export Tool")
    print("=" * 50)
    print()
    export_scan_results()
