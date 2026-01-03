"""
User service for user management
"""
from sqlalchemy.orm import Session
from models import User
from schemas import UserUpdate, UserCreate
from utils.security import hash_password, verify_password
from typing import Optional, Tuple, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class UserService:
    """User service"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(
        db: Session,
        user_id: str,
        update_data: UserUpdate,
    ) -> Tuple[bool, str, Optional[User]]:
        """Update user information"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found", None

            # Update fields
            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(user, key, value)

            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
            logger.info(f"User updated: {user.email}")
            return True, "User updated successfully", user
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {e}")
            return False, "Error updating user", None

    @staticmethod
    def change_password(
        db: Session,
        user_id: str,
        old_password: str,
        new_password: str,
    ) -> Tuple[bool, str]:
        """Change user password"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            # Verify old password
            if not verify_password(old_password, user.password_hash):
                return False, "Old password is incorrect"

            # Update password
            user.password_hash = hash_password(new_password)
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Password changed for user: {user.email}")
            return True, "Password changed successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error changing password: {e}")
            return False, "Error changing password"

    @staticmethod
    def delete_user(db: Session, user_id: str) -> Tuple[bool, str]:
        """Delete user account"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            db.delete(user)
            db.commit()
            logger.info(f"User deleted: {user.email}")
            return True, "User deleted successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user: {e}")
            return False, "Error deleting user"

    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> Tuple[bool, str]:
        """Deactivate user account"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            user.is_active = False
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"User deactivated: {user.email}")
            return True, "User deactivated successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating user: {e}")
            return False, "Error deactivating user"

    @staticmethod
    def activate_user(db: Session, user_id: str) -> Tuple[bool, str]:
        """Activate user account"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            user.is_active = True
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"User activated: {user.email}")
            return True, "User activated successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error activating user: {e}")
            return False, "Error activating user"

    @staticmethod
    def verify_email(db: Session, user_id: str) -> Tuple[bool, str]:
        """Verify user email"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            user.email_verified = True
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Email verified for user: {user.email}")
            return True, "Email verified successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error verifying email: {e}")
            return False, "Error verifying email"

    @staticmethod
    def enable_2fa(db: Session, user_id: str, secret: str) -> Tuple[bool, str]:
        """Enable 2FA for user"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            user.two_factor_enabled = True
            user.two_factor_secret = secret
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"2FA enabled for user: {user.email}")
            return True, "2FA enabled successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error enabling 2FA: {e}")
            return False, "Error enabling 2FA"

    @staticmethod
    def disable_2fa(db: Session, user_id: str) -> Tuple[bool, str]:
        """Disable 2FA for user"""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False, "User not found"

            user.two_factor_enabled = False
            user.two_factor_secret = None
            user.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"2FA disabled for user: {user.email}")
            return True, "2FA disabled successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error disabling 2FA: {e}")
            return False, "Error disabling 2FA"

    @staticmethod
    def count_users(db: Session) -> int:
        """Count total users"""
        return db.query(User).count()

    @staticmethod
    def count_active_users(db: Session) -> int:
        """Count active users"""
        return db.query(User).filter(User.is_active == True).count()

    @staticmethod
    def search_users(db: Session, query: str, limit: int = 10) -> List[User]:
        """Search users by email or name"""
        return (
            db.query(User)
            .filter(
                (User.email.ilike(f"%{query}%"))
                | (User.first_name.ilike(f"%{query}%"))
                | (User.last_name.ilike(f"%{query}%"))
            )
            .limit(limit)
            .all()
        )
