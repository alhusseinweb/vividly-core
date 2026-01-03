"""
Authentication Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # in seconds


class TokenRefreshRequest(BaseModel):
    """Token refresh request schema"""
    refresh_token: str


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Registration request schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class VerifyEmailRequest(BaseModel):
    """Verify email request schema"""
    token: str


class LogoutRequest(BaseModel):
    """Logout request schema"""
    refresh_token: Optional[str] = None


class AuthResponse(BaseModel):
    """Generic auth response schema"""
    success: bool
    message: str
    data: Optional[dict] = None


class SessionResponse(BaseModel):
    """Session response schema"""
    id: str
    user_agent: Optional[str]
    ip_address: Optional[str]
    is_active: bool
    created_at: str
    expires_at: str
    last_used_at: Optional[str]
