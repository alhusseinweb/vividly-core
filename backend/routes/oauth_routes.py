"""
OAuth authentication routes for GitHub and Google
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from services.oauth_service import OAuthService
from config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth/oauth", tags=["oauth"])


@router.get("/github/authorize")
async def github_authorize():
    """Redirect to GitHub OAuth authorization"""
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={settings.GITHUB_CLIENT_ID}&"
        f"redirect_uri={settings.GITHUB_REDIRECT_URI}&"
        f"scope=user:email&"
        f"state=vividly_github_oauth"
    )
    return {"authorization_url": github_auth_url}


@router.get("/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """GitHub OAuth callback"""
    if state != "vividly_github_oauth":
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    ip_address = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None

    success, message, data = await OAuthService.authenticate_github_user(
        db, code, ip_address, user_agent
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "message": message,
        "user_id": data["user_id"],
        "email": data["email"],
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "expires_in": data["expires_in"],
    }


@router.get("/google/authorize")
async def google_authorize():
    """Redirect to Google OAuth authorization"""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"state=vividly_google_oauth"
    )
    return {"authorization_url": google_auth_url}


@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """Google OAuth callback"""
    if state != "vividly_google_oauth":
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    ip_address = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None

    success, message, data = await OAuthService.authenticate_google_user(
        db, code, ip_address, user_agent
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "message": message,
        "user_id": data["user_id"],
        "email": data["email"],
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "expires_in": data["expires_in"],
    }
