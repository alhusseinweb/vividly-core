"""
Session model for user sessions and tokens
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid


class Session(Base):
    """Session model for managing user sessions"""
    __tablename__ = "sessions"

    # Primary Key
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Tokens
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)

    # Device Information
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_used_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", backref="sessions")

    def __repr__(self):
        return f"<Session {self.id}>"

    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
        }
