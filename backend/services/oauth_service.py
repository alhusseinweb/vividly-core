"""
OAuth service for GitHub and Google authentication
"""
import httpx
import logging
from typing import Optional, Tuple, Dict, Any
from config import settings
from sqlalchemy.orm import Session
from models import User
from utils.security import hash_password, create_access_token, create_refresh_token
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class OAuthService:
    """OAuth service for handling GitHub and Google authentication"""

    @staticmethod
    async def get_github_access_token(code: str) -> Optional[str]:
        """Exchange GitHub authorization code for access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": settings.GITHUB_CLIENT_ID,
                        "client_secret": settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                data = response.json()
                return data.get("access_token")
        except Exception as e:
            logger.error(f"Error getting GitHub access token: {e}")
            return None

    @staticmethod
    async def get_github_user(access_token: str) -> Optional[Dict[str, Any]]:
        """Get GitHub user information using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting GitHub user: {e}")
            return None

    @staticmethod
    async def get_github_user_email(access_token: str) -> Optional[str]:
        """Get GitHub user email"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                response.raise_for_status()
                emails = response.json()
                # Find primary email
                for email in emails:
                    if email.get("primary"):
                        return email.get("email")
                # If no primary, return first verified
                for email in emails:
                    if email.get("verified"):
                        return email.get("email")
                # Return first email
                if emails:
                    return emails[0].get("email")
        except Exception as e:
            logger.error(f"Error getting GitHub user email: {e}")
            return None

    @staticmethod
    async def authenticate_github_user(
        db: Session,
        code: str,
        ip_address: str = None,
        user_agent: str = None,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Authenticate user with GitHub OAuth"""
        try:
            # Get access token
            access_token = await OAuthService.get_github_access_token(code)
            if not access_token:
                return False, "Failed to get GitHub access token", None

            # Get user info
            github_user = await OAuthService.get_github_user(access_token)
            if not github_user:
                return False, "Failed to get GitHub user info", None

            # Get user email
            email = await OAuthService.get_github_user_email(access_token)
            if not email:
                email = github_user.get("email")

            if not email:
                return False, "Could not get user email from GitHub", None

            # Check if user exists
            from services.user_service import UserService

            user = UserService.get_user_by_email(db, email)

            if not user:
                # Create new user
                user = User(
                    id=str(uuid.uuid4()),
                    email=email,
                    password_hash=hash_password(str(uuid.uuid4())),  # Random password
                    first_name=github_user.get("name", "").split()[0] or "GitHub",
                    last_name=github_user.get("name", "").split()[-1] if len(github_user.get("name", "").split()) > 1 else "User",
                    avatar_url=github_user.get("avatar_url"),
                    bio=github_user.get("bio"),
                    is_active=True,
                    email_verified=True,
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"New user created via GitHub OAuth: {email}")

            # Create tokens
            access_token_str = create_access_token(user.id)
            refresh_token_str = create_refresh_token(user.id)

            # Create session
            from models import Session as SessionModel

            session = SessionModel(
                id=str(uuid.uuid4()),
                user_id=user.id,
                token=access_token_str,
                refresh_token=refresh_token_str,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.utcnow().replace(hour=datetime.utcnow().hour + 24),
            )
            db.add(session)
            db.commit()

            user.last_login = datetime.utcnow()
            db.commit()

            return True, "GitHub authentication successful", {
                "user_id": user.id,
                "email": user.email,
                "access_token": access_token_str,
                "refresh_token": refresh_token_str,
                "expires_in": 86400,
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error authenticating GitHub user: {e}")
            return False, "Error authenticating with GitHub", None

    @staticmethod
    async def get_google_access_token(code: str) -> Optional[Dict[str, Any]]:
        """Exchange Google authorization code for access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    },
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting Google access token: {e}")
            return None

    @staticmethod
    async def get_google_user(access_token: str) -> Optional[Dict[str, Any]]:
        """Get Google user information using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting Google user: {e}")
            return None

    @staticmethod
    async def authenticate_google_user(
        db: Session,
        code: str,
        ip_address: str = None,
        user_agent: str = None,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Authenticate user with Google OAuth"""
        try:
            # Get access token
            token_data = await OAuthService.get_google_access_token(code)
            if not token_data:
                return False, "Failed to get Google access token", None

            access_token = token_data.get("access_token")
            if not access_token:
                return False, "No access token in response", None

            # Get user info
            google_user = await OAuthService.get_google_user(access_token)
            if not google_user:
                return False, "Failed to get Google user info", None

            email = google_user.get("email")
            if not email:
                return False, "Could not get user email from Google", None

            # Check if user exists
            from services.user_service import UserService

            user = UserService.get_user_by_email(db, email)

            if not user:
                # Create new user
                name = google_user.get("name", "").split()
                first_name = name[0] if name else "Google"
                last_name = name[-1] if len(name) > 1 else "User"

                user = User(
                    id=str(uuid.uuid4()),
                    email=email,
                    password_hash=hash_password(str(uuid.uuid4())),  # Random password
                    first_name=first_name,
                    last_name=last_name,
                    avatar_url=google_user.get("picture"),
                    is_active=True,
                    email_verified=google_user.get("verified_email", False),
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"New user created via Google OAuth: {email}")

            # Create tokens
            access_token_str = create_access_token(user.id)
            refresh_token_str = create_refresh_token(user.id)

            # Create session
            from models import Session as SessionModel

            session = SessionModel(
                id=str(uuid.uuid4()),
                user_id=user.id,
                token=access_token_str,
                refresh_token=refresh_token_str,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.utcnow().replace(hour=datetime.utcnow().hour + 24),
            )
            db.add(session)
            db.commit()

            user.last_login = datetime.utcnow()
            db.commit()

            return True, "Google authentication successful", {
                "user_id": user.id,
                "email": user.email,
                "access_token": access_token_str,
                "refresh_token": refresh_token_str,
                "expires_in": 86400,
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error authenticating Google user: {e}")
            return False, "Error authenticating with Google", None
