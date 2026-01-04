"""
Project model
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid


class Project(Base):
    """Project model"""
    __tablename__ = "projects"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Basic Information
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(255), unique=True, nullable=True, index=True)
    vibe_description = Column(Text, nullable=False)

    # Status & Content
    status = Column(String(50), default="draft", nullable=False)  # draft, generating, ready, published, archived
    generated_code = Column(Text, nullable=True)
    preview_url = Column(Text, nullable=True)
    live_url = Column(Text, nullable=True)

    # Metadata
    language = Column(String(50), default="html", nullable=False)  # html, react, vue, svelte
    framework = Column(String(100), nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    collaborators = Column(JSON, default=list, nullable=False)

    # Statistics
    views_count = Column(Integer, default=0, nullable=False)
    likes_count = Column(Integer, default=0, nullable=False)
    comments_count = Column(Integer, default=0, nullable=False)

    # Publishing
    published_at = Column(DateTime, nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    enable_analytics = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Project {self.name}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "vibe_description": self.vibe_description,
            "status": self.status,
            "generated_code": self.generated_code,
            "preview_url": self.preview_url,
            "live_url": self.live_url,
            "language": self.language,
            "framework": self.framework,
            "tags": self.tags,
            "collaborators": self.collaborators,
            "views_count": self.views_count,
            "likes_count": self.likes_count,
            "comments_count": self.comments_count,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "is_public": self.is_public,
            "enable_analytics": self.enable_analytics,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
