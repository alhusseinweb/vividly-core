"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    LoginRequest,
    RegisterRequest,
    TokenRefreshRequest,
    TokenResponse,
    AuthResponse,
    UserResponse,
)
from services import AuthService
from middleware import get_current_user
from models import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    success, message, user = AuthService.register(db, request)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    
    return AuthResponse(
        success=True,
        message=message,
        data={"user": user.to_dict()} if user else None,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    req: Request,
    db: Session = Depends(get_db),
):
    """
    Login user
    """
    # Get client info
    user_agent = req.headers.get("user-agent")
    client_host = req.client.host if req.client else None

    success, message, token_response = AuthService.login(
        db,
        request,
        user_agent=user_agent,
        ip_address=client_host,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    return AuthResponse(
        success=True,
        message=message,
        data={
            "access_token": token_response.access_token,
            "refresh_token": token_response.refresh_token,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
        },
    )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh access token
    """
    success, message, token_response = AuthService.refresh_token(db, request.refresh_token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    return AuthResponse(
        success=True,
        message=message,
        data={
            "access_token": token_response.access_token,
            "refresh_token": token_response.refresh_token,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
        },
    )


@router.post("/logout", response_model=AuthResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Logout user
    """
    # Get active sessions
    sessions = AuthService.get_active_sessions(db, str(current_user.id))
    
    if sessions:
        # Logout all sessions
        success, message = AuthService.revoke_all_sessions(db, str(current_user.id))
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            )
    
    return AuthResponse(
        success=True,
        message="Logged out successfully",
    )


@router.get("/me", response_model=AuthResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return AuthResponse(
        success=True,
        message="User information retrieved",
        data={"user": current_user.to_dict()},
    )


@router.get("/sessions", response_model=AuthResponse)
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all active sessions for current user
    """
    sessions = AuthService.get_active_sessions(db, str(current_user.id))
    
    return AuthResponse(
        success=True,
        message="Sessions retrieved",
        data={"sessions": [session.to_dict() for session in sessions]},
    )


@router.post("/revoke-all-sessions", response_model=AuthResponse)
async def revoke_all_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Revoke all sessions for current user
    """
    success, message = AuthService.revoke_all_sessions(db, str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
    
    return AuthResponse(
        success=True,
        message=message,
    )
