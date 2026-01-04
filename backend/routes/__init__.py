"""
API routes
"""
from routes.auth import router as auth_router
from routes.user_routes import router as user_router
from routes.project_routes import router as project_router
from routes.oauth_routes import router as oauth_router
from routes.codegen_routes import router as codegen_router

__all__ = ["auth_router", "user_router", "project_router", "oauth_router", "codegen_router"]
