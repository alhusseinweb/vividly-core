"""
API routes
"""
from routes.auth import router as auth_router
from routes.user_routes import router as user_router
from routes.project_routes import router as project_router

__all__ = ["auth_router", "user_router", "project_router"]
