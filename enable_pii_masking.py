"""
Enable PII Masking and Verify Settings
"""
from backend.app.database import SessionLocal
from backend.app import models

db = SessionLocal()

try:
    # Get or create settings
    settings = db.query(models.GlobalSettings).first()
    
    if not settings:
        print("⚠️  No settings found. Creating default settings...")
        settings = models.GlobalSettings(
            pii_masking_enabled=True,
            data_retention_days=30
        )
        db.add(settings)
        db.commit()
        print("✅ Created settings with PII masking ENABLED")
    else:
        print(f"Current PII Masking Status: {'ENABLED ✅' if settings.pii_masking_enabled else 'DISABLED ❌'}")
        
        if not settings.pii_masking_enabled:
            print("\n🔧 Enabling PII masking...")
            settings.pii_masking_enabled = True
            db.commit()
            print("✅ PII masking is now ENABLED")
        else:
            print("✅ PII masking is already enabled")
    
    print("\n📊 Current Settings:")
    print(f"   - PII Masking: {'ENABLED' if settings.pii_masking_enabled else 'DISABLED'}")
    print(f"   - Data Retention: {settings.data_retention_days} days")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()

print("\n✅ Ready to test PII masking!")
print("   Run: python add_test_pii_data.py")
