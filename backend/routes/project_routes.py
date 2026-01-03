"""
Project management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from services import UserService
from services.project_service import ProjectService
from schemas import (
    ProjectResponse,
    ProjectListResponse,
    ProjectDetailResponse,
    ProjectCreate,
    ProjectUpdate,
    ProjectGenerateCodeRequest,
    ProjectGenerateCodeResponse,
    ProjectPublishRequest,
    ProjectPublishResponse,
    ProjectExportRequest,
    ProjectExportResponse,
    ProjectDuplicateResponse,
    ProjectStatsResponse,
    ProjectSearchRequest,
    ProjectSearchResponse,
    ProjectActivityResponse,
    ProjectVersionResponse,
    ProjectCollaboratorResponse,
    ProjectAddCollaboratorRequest,
    ProjectRemoveCollaboratorRequest,
    ProjectUpdateCollaboratorRoleRequest,
)
from utils.security import get_current_user
from models import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project"""
    success, message, project = ProjectService.create_project(
        db, current_user.id, project_data
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return project


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List user's projects"""
    projects = ProjectService.get_user_projects(db, current_user.id, skip, limit)
    total = ProjectService.count_user_projects(db, current_user.id)

    return ProjectListResponse(
        total=total,
        page=skip // limit + 1,
        limit=limit,
        projects=projects,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project by ID"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check ownership or admin
    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message, updated_project = ProjectService.update_project(
        db, project_id, update_data
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/{project_id}/generate-code", response_model=ProjectGenerateCodeResponse)
async def generate_project_code(
    project_id: str,
    request: ProjectGenerateCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate project code using AI"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message, generated_code = ProjectService.generate_project_code(
        db, project_id, request.vibe_description
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return ProjectGenerateCodeResponse(
        project_id=project_id,
        status="generated",
        generated_code=generated_code,
        preview_url=None,  # TODO: Implement preview URL generation
        estimated_time=0.0,
    )


@router.post("/{project_id}/publish", response_model=ProjectPublishResponse)
async def publish_project(
    project_id: str,
    request: ProjectPublishRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Publish project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message = ProjectService.publish_project(db, project_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return ProjectPublishResponse(
        project_id=project_id,
        status="published",
        live_url=f"https://{project.slug}.vividly.app",  # TODO: Implement actual URL
        domain=request.domain or f"{project.slug}.vividly.app",
    )


@router.post("/{project_id}/archive")
async def archive_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Archive project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message = ProjectService.archive_project(db, project_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@router.post("/{project_id}/duplicate", response_model=ProjectDuplicateResponse)
async def duplicate_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Duplicate project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message, new_project = ProjectService.duplicate_project(
        db, project_id, current_user.id
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return ProjectDuplicateResponse(
        original_id=project_id,
        new_id=new_project.id,
        new_project=new_project,
    )


@router.post("/{project_id}/export", response_model=ProjectExportResponse)
async def export_project(
    project_id: str,
    request: ProjectExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export project"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success, message, export_data = ProjectService.export_project(db, project_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return ProjectExportResponse(
        project_id=project_id,
        export_url=f"https://vividly.app/exports/{project_id}.{request.format}",
        format=request.format,
        size=1.5,  # TODO: Calculate actual size
        created_at=project.updated_at,
    )


@router.get("/stats/overview", response_model=ProjectStatsResponse)
async def get_project_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project statistics"""
    # TODO: Implement statistics calculation
    return ProjectStatsResponse(
        total_projects=ProjectService.count_user_projects(db, current_user.id),
        published_projects=0,
        draft_projects=0,
        archived_projects=0,
        total_views=0,
        total_likes=0,
        average_generation_time=0.0,
    )


@router.get("/search/query", response_model=ProjectSearchResponse)
async def search_projects(
    q: str = Query(..., min_length=1, max_length=100),
    status: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search user's projects"""
    # TODO: Implement project search
    return ProjectSearchResponse(total=0, results=[])


@router.get("/{project_id}/versions", response_model=list[ProjectVersionResponse])
async def get_project_versions(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project versions"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # TODO: Implement version retrieval
    return []


@router.get("/{project_id}/collaborators", response_model=list[ProjectCollaboratorResponse])
async def get_project_collaborators(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project collaborators"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # TODO: Implement collaborators retrieval
    return []


@router.post("/{project_id}/collaborators", response_model=ProjectCollaboratorResponse)
async def add_project_collaborator(
    project_id: str,
    request: ProjectAddCollaboratorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add project collaborator"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # TODO: Implement add collaborator
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{project_id}/collaborators/{user_id}")
async def remove_project_collaborator(
    project_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove project collaborator"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # TODO: Implement remove collaborator
    return {"message": "Collaborator removed"}


@router.put("/{project_id}/collaborators/{user_id}")
async def update_project_collaborator_role(
    project_id: str,
    user_id: str,
    request: ProjectUpdateCollaboratorRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update project collaborator role"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # TODO: Implement update collaborator role
    return {"message": "Collaborator role updated"}
