"""
Export RECENT Scan Results to CSV (Last 20 entries only)
Perfect for PII Masking Demo
"""

import csv
from datetime import datetime
from backend.app.database import SessionLocal
from backend.app import models

def export_recent_scans():
    """Export only the most recent 20 scan results"""
    db = SessionLocal()
    
    try:
        # Get only the last 20 scans
        scans = db.query(models.ScanResult).order_by(models.ScanResult.timestamp.desc()).limit(20).all()
        
        # Create CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recent_scans_PII_DEMO_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'URL/Text (First 200 chars)', 'Domain', 'Risk Score', 'Risk Level', 'Explanation', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for scan in scans:
                writer.writerow({
                    'ID': scan.id,
                    'URL/Text (First 200 chars)': scan.url[:200],
                    'Domain': scan.domain,
                    'Risk Score': f"{scan.risk_score:.2f}",
                    'Risk Level': scan.risk_level,
                    'Explanation': scan.explanation,
                    'Timestamp': scan.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        print(f"✅ Exported {len(scans)} RECENT scan results to: {filename}")
        print(f"\n📊 Summary:")
        print(f"   - Total scans exported: {len(scans)}")
        
        # Count masked entries
        masked_count = sum(1 for s in scans if '[EMAIL_REDACTED]' in s.url or '[PHONE_REDACTED]' in s.url)
        print(f"   - Entries with masked PII: {masked_count}")
        print(f"   - Entries without PII: {len(scans) - masked_count}")
        
        # Show sample
        print(f"\n📝 Sample Entry (First Row):")
        if scans:
            first = scans[0]
            print(f"   URL: {first.url[:100]}...")
            if '[EMAIL_REDACTED]' in first.url or '[PHONE_REDACTED]' in first.url:
                print(f"   ✅ PII IS MASKED!")
            else:
                print(f"   ⚠️  No PII found in this entry")
        
        print(f"\n💡 Open '{filename}' to see PII masking in action!")
        print(f"   Look for [EMAIL_REDACTED] and [PHONE_REDACTED]")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔒 SecureSentinel - Recent Scans Export (PII Demo)")
    print("=" * 60)
    print()
    export_recent_scans()
