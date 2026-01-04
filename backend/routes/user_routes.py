"""
User management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from services import UserService
from schemas import (
    UserResponse,
    UserDetailResponse,
    UserListResponse,
    UserUpdate,
    ChangePasswordRequest,
    UserStatsResponse,
    UserSearchRequest,
    UserSearchResponse,
    DeactivateAccountRequest,
    DeleteAccountRequest,
    UserPreferencesResponse,
    UserPreferencesUpdate,
)
from middleware.auth_middleware import get_current_user
from models import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can list users")

    users = UserService.get_all_users(db, skip, limit)
    total = UserService.count_users(db)

    return UserListResponse(
        total=total,
        page=skip // limit + 1,
        limit=limit,
        users=users,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user information"""
    success, message, user = UserService.update_user(db, current_user.id, update_data)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user information (admin or self)"""
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message, user = UserService.update_user(db, user_id, update_data)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return user


@router.post("/me/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Change current user password"""
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    success, message = UserService.change_password(
        db,
        current_user.id,
        request.old_password,
        request.new_password,
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/me/deactivate")
async def deactivate_account(
    request: DeactivateAccountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deactivate current user account"""
    from utils.security import verify_password

    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    success, message = UserService.deactivate_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/me/delete")
async def delete_account(
    request: DeleteAccountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete current user account"""
    from utils.security import verify_password

    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    success, message = UserService.delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/{user_id}/deactivate")
async def deactivate_user_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deactivate user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can deactivate users")

    success, message = UserService.deactivate_user(db, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/{user_id}/activate")
async def activate_user_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Activate user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can activate users")

    success, message = UserService.activate_user(db, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/{user_id}/delete")
async def delete_user_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    success, message = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.get("/search/query", response_model=UserSearchResponse)
async def search_users(
    q: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search users by email or name"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can search users")

    results = UserService.search_users(db, q, limit)
    return UserSearchResponse(total=len(results), results=results)


@router.get("/stats/overview", response_model=UserStatsResponse)
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user statistics (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can view stats")

    total = UserService.count_users(db)
    active = UserService.count_active_users(db)

    return UserStatsResponse(
        total_users=total,
        active_users=active,
        inactive_users=total - active,
        verified_emails=0,  # TODO: Implement
        two_factor_enabled=0,  # TODO: Implement
        average_projects=0.0,  # TODO: Implement
    )


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
):
    """Get current user preferences"""
    return UserPreferencesResponse(
        email_notifications=True,  # TODO: Implement
        push_notifications=True,  # TODO: Implement
        marketing_emails=False,  # TODO: Implement
        theme="dark",  # TODO: Implement
        language="en",  # TODO: Implement
    )


@router.put("/me/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    preferences: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update current user preferences"""
    # TODO: Implement preferences storage
    return UserPreferencesResponse(
        email_notifications=preferences.email_notifications or True,
        push_notifications=preferences.push_notifications or True,
        marketing_emails=preferences.marketing_emails or False,
        theme=preferences.theme or "dark",
        language=preferences.language or "en",
    )
