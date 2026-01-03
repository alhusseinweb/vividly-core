"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema"""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""

    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "currentPassword123",
                "new_password": "newPassword456",
                "confirm_password": "newPassword456",
            }
        }


class UserResponse(UserBase):
    """User response schema"""

    id: str
    is_active: bool
    email_verified: bool
    two_factor_enabled: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response schema"""

    subscription_tier: str
    subscription_status: str
    projects_count: int
    storage_used: float
    storage_limit: float


class UserListResponse(BaseModel):
    """User list response schema"""

    total: int
    page: int
    limit: int
    users: list[UserResponse]


class UserStatsResponse(BaseModel):
    """User statistics response schema"""

    total_users: int
    active_users: int
    inactive_users: int
    verified_emails: int
    two_factor_enabled: int
    average_projects: float


class Enable2FARequest(BaseModel):
    """Enable 2FA request schema"""

    password: str = Field(..., min_length=8)


class Enable2FAResponse(BaseModel):
    """Enable 2FA response schema"""

    secret: str
    qr_code: str
    backup_codes: list[str]


class Verify2FARequest(BaseModel):
    """Verify 2FA request schema"""

    code: str = Field(..., regex=r"^\d{6}$")


class DeactivateAccountRequest(BaseModel):
    """Deactivate account request schema"""

    password: str = Field(..., min_length=8)
    reason: Optional[str] = Field(None, max_length=500)


class DeleteAccountRequest(BaseModel):
    """Delete account request schema"""

    password: str = Field(..., min_length=8)
    confirmation: str = Field(..., regex=r"^DELETE$")
    reason: Optional[str] = Field(None, max_length=500)


class UserSearchRequest(BaseModel):
    """User search request schema"""

    query: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(10, ge=1, le=100)


class UserSearchResponse(BaseModel):
    """User search response schema"""

    total: int
    results: list[UserResponse]


class UserActivityResponse(BaseModel):
    """User activity response schema"""

    id: str
    action: str
    description: str
    ip_address: str
    user_agent: str
    created_at: datetime


class UserPreferencesResponse(BaseModel):
    """User preferences response schema"""

    email_notifications: bool
    push_notifications: bool
    marketing_emails: bool
    theme: str  # "light" or "dark"
    language: str  # "en", "ar", etc.


class UserPreferencesUpdate(BaseModel):
    """User preferences update schema"""

    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None
