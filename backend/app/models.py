from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    domain = Column(String, index=True)
    risk_score = Column(Float)
    risk_level = Column(String)  # SAFE, SUSPICIOUS, HIGH_RISK
    explanation = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class BlockedDomain(Base):
    __tablename__ = "blocked_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class AllowedDomain(Base):
    __tablename__ = "allowed_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class GlobalSettings(Base):
    __tablename__ = "global_settings"

    id = Column(Integer, primary_key=True, index=True)
    retention_days = Column(Integer, default=30)
    pii_masking_enabled = Column(Integer, default=1) # 0=False, 1=True (using int for SQLite bool compatibility safety)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class EncryptionMetadata(Base):
    """
    Simulates Key Management Service (KMS) metadata.
    In a real scenario, this would track versions of keys used for column-level encryption.
    """
    __tablename__ = "encryption_keys"

    id = Column(String, primary_key=True, index=True) # UUID
    key_version = Column(Integer, autoincrement=True, unique=True)
    algorithm = Column(String, default="AES-256-GCM")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="ACTIVE") # ACTIVE, ROTATED

class UserAPIKey(Base):
    """
    Stores encrypted API keys for external integrations
    Examples: Gemini API, Email services, Slack webhooks, etc.
    """
    __tablename__ = "user_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)  # e.g., "gemini", "sendgrid", "slack"
    encrypted_key = Column(String)  # Encrypted API key
    key_version_id = Column(String)  # References encryption_keys.id
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Integer, default=1)  # 0=disabled, 1=enabled

