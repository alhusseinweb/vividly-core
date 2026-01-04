"""
Code generation API routes using Google Gemini
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.gemini_service import GeminiService
from services.project_service import ProjectService
from utils.security import get_current_user
from models import User
from schemas import ProjectGenerateCodeRequest, ProjectGenerateCodeResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/codegen", tags=["code-generation"])

# Initialize Gemini
GeminiService.initialize()


@router.post("/html", response_model=ProjectGenerateCodeResponse)
async def generate_html_code(
    request: ProjectGenerateCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate HTML code from vibe description"""
    success, message, code = GeminiService.generate_html_code(request.vibe_description)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return ProjectGenerateCodeResponse(
        project_id="",
        status="generated",
        generated_code=code,
        preview_url=None,
        estimated_time=2.5,
    )


@router.post("/react", response_model=ProjectGenerateCodeResponse)
async def generate_react_code(
    request: ProjectGenerateCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate React component code from vibe description"""
    success, message, code = GeminiService.generate_react_code(request.vibe_description)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return ProjectGenerateCodeResponse(
        project_id="",
        status="generated",
        generated_code=code,
        preview_url=None,
        estimated_time=2.5,
    )


@router.post("/css")
async def generate_css_code(
    vibe_description: str,
    current_user: User = Depends(get_current_user),
):
    """Generate CSS from vibe description"""
    success, message, code = GeminiService.generate_css_from_vibe(vibe_description)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "generated",
        "generated_code": code,
    }


@router.post("/project-structure")
async def generate_project_structure(
    vibe_description: str,
    current_user: User = Depends(get_current_user),
):
    """Generate project structure from vibe description"""
    success, message, structure = GeminiService.generate_project_structure(vibe_description)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "generated",
        "structure": structure,
    }


@router.post("/optimize")
async def optimize_code(
    code: str,
    language: str = "html",
    current_user: User = Depends(get_current_user),
):
    """Optimize generated code"""
    success, message, optimized_code = GeminiService.optimize_code(code, language)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "optimized",
        "optimized_code": optimized_code,
    }


@router.post("/project/{project_id}/generate")
async def generate_code_for_project(
    project_id: str,
    language: str = "html",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate code for a specific project"""
    project = ProjectService.get_project_by_id(db, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Generate code based on language
    if language == "html":
        success, message, code = GeminiService.generate_html_code(project.vibe_description)
    elif language == "react":
        success, message, code = GeminiService.generate_react_code(project.vibe_description)
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Update project with generated code
    success, message, updated_project = ProjectService.update_project(
        db,
        project_id,
        {"generated_code": code, "status": "generated"},
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "project_id": project_id,
        "status": "generated",
        "generated_code": code,
        "language": language,
    }
