"""
Authentication service
"""
from sqlalchemy.orm import Session
from models import User, Session as SessionModel
from schemas import LoginRequest, RegisterRequest, TokenResponse
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from datetime import datetime, timedelta
from config import settings
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""

    @staticmethod
    def register(db: Session, request: RegisterRequest) -> Tuple[bool, str, Optional[User]]:
        """
        Register a new user
        """
        # Check if passwords match
        if request.password != request.confirm_password:
            return False, "Passwords do not match", None

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            return False, "User with this email already exists", None

        try:
            # Create new user
            user = User(
                email=request.email,
                password_hash=hash_password(request.password),
                first_name=request.first_name,
                last_name=request.last_name,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User registered: {user.email}")
            return True, "User registered successfully", user
        except Exception as e:
            db.rollback()
            logger.error(f"Error registering user: {e}")
            return False, "Error registering user", None

    @staticmethod
    def login(
        db: Session,
        request: LoginRequest,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[TokenResponse]]:
        """
        Login user
        """
        # Find user by email
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            logger.warning(f"Login attempt with non-existent email: {request.email}")
            return False, "Invalid email or password", None

        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt with inactive user: {user.email}")
            return False, "User account is inactive", None

        # Verify password
        if not verify_password(request.password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {user.email}")
            return False, "Invalid email or password", None

        try:
            # Create tokens
            access_token = create_access_token({"sub": str(user.id)})
            refresh_token = create_refresh_token({"sub": str(user.id)})

            # Create session
            session = SessionModel(
                user_id=user.id,
                access_token=access_token,
                refresh_token=refresh_token,
                user_agent=user_agent,
                ip_address=ip_address,
                expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
            db.add(session)

            # Update last login
            user.last_login_at = datetime.utcnow()
            db.commit()
            db.refresh(user)

            logger.info(f"User logged in: {user.email}")

            return True, "Login successful", TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Error logging in user: {e}")
            return False, "Error logging in", None

    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> Tuple[bool, str, Optional[TokenResponse]]:
        """
        Refresh access token
        """
        # Verify refresh token
        payload = verify_token(refresh_token)
        if payload is None:
            return False, "Invalid refresh token", None

        # Check token type
        if payload.get("type") != "refresh":
            return False, "Invalid token type", None

        # Get user
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found", None

        try:
            # Create new access token
            new_access_token = create_access_token({"sub": str(user.id)})

            logger.info(f"Token refreshed for user: {user.email}")

            return True, "Token refreshed successfully", TokenResponse(
                access_token=new_access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False, "Error refreshing token", None

    @staticmethod
    def logout(db: Session, session_id: str) -> Tuple[bool, str]:
        """
        Logout user
        """
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if session:
                session.is_active = False
                db.commit()
                logger.info(f"User logged out: session {session_id}")
            return True, "Logged out successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error logging out: {e}")
            return False, "Error logging out"

    @staticmethod
    def get_user_from_token(db: Session, token: str) -> Optional[User]:
        """
        Get user from access token
        """
        payload = verify_token(token)
        if payload is None:
            return None

        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def get_active_sessions(db: Session, user_id: str) -> list:
        """
        Get all active sessions for a user
        """
        sessions = (
            db.query(SessionModel)
            .filter(SessionModel.user_id == user_id, SessionModel.is_active == True)
            .all()
        )
        return sessions

    @staticmethod
    def revoke_all_sessions(db: Session, user_id: str) -> Tuple[bool, str]:
        """
        Revoke all sessions for a user
        """
        try:
            db.query(SessionModel).filter(SessionModel.user_id == user_id).update(
                {"is_active": False}
            )
            db.commit()
            logger.info(f"All sessions revoked for user: {user_id}")
            return True, "All sessions revoked"
        except Exception as e:
            db.rollback()
            logger.error(f"Error revoking sessions: {e}")
            return False, "Error revoking sessions"
