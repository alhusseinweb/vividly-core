"""
Project schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema"""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    vibe_description: str = Field(..., min_length=10, max_length=2000)


class ProjectCreate(ProjectBase):
    """Project creation schema"""

    pass


class ProjectUpdate(BaseModel):
    """Project update schema"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    vibe_description: Optional[str] = Field(None, min_length=10, max_length=2000)
    status: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""

    id: str
    user_id: str
    slug: Optional[str]
    status: str
    generated_code: Optional[str]
    preview_url: Optional[str]
    live_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Project list response schema"""

    total: int
    page: int
    limit: int
    projects: list[ProjectResponse]


class ProjectDetailResponse(ProjectResponse):
    """Detailed project response schema"""

    views_count: int
    likes_count: int
    comments_count: int
    collaborators: list[str]
    tags: list[str]


class ProjectGenerateCodeRequest(BaseModel):
    """Generate code request schema"""

    vibe_description: str = Field(..., min_length=10, max_length=2000)
    language: str = Field("html", pattern="^(html|react|vue|svelte)$")
    framework: Optional[str] = None


class ProjectGenerateCodeResponse(BaseModel):
    """Generate code response schema"""

    project_id: str
    status: str
    generated_code: str
    preview_url: Optional[str]
    estimated_time: float  # in seconds


class ProjectPublishRequest(BaseModel):
    """Publish project request schema"""

    domain: Optional[str] = None
    enable_analytics: bool = True


class ProjectPublishResponse(BaseModel):
    """Publish project response schema"""

    project_id: str
    status: str
    live_url: str
    domain: str


class ProjectExportRequest(BaseModel):
    """Export project request schema"""

    format: str = Field("json", pattern="^(json|zip|tar)$")
    include_assets: bool = True


class ProjectExportResponse(BaseModel):
    """Export project response schema"""

    project_id: str
    export_url: str
    format: str
    size: float  # in MB
    created_at: datetime


class ProjectDuplicateResponse(BaseModel):
    """Duplicate project response schema"""

    original_id: str
    new_id: str
    new_project: ProjectResponse


class ProjectStatsResponse(BaseModel):
    """Project statistics response schema"""

    total_projects: int
    published_projects: int
    draft_projects: int
    archived_projects: int
    total_views: int
    total_likes: int
    average_generation_time: float


class ProjectSearchRequest(BaseModel):
    """Project search request schema"""

    query: str = Field(..., min_length=1, max_length=100)
    status: Optional[str] = None
    limit: int = Field(10, ge=1, le=100)


class ProjectSearchResponse(BaseModel):
    """Project search response schema"""

    total: int
    results: list[ProjectResponse]


class ProjectActivityResponse(BaseModel):
    """Project activity response schema"""

    id: str
    project_id: str
    action: str
    description: str
    created_at: datetime


class ProjectVersionResponse(BaseModel):
    """Project version response schema"""

    id: str
    project_id: str
    version_number: int
    generated_code: str
    created_at: datetime
    created_by: str


class ProjectCollaboratorResponse(BaseModel):
    """Project collaborator response schema"""

    user_id: str
    email: str
    first_name: str
    last_name: str
    role: str  # "owner", "editor", "viewer"
    joined_at: datetime


class ProjectAddCollaboratorRequest(BaseModel):
    """Add collaborator request schema"""

    email: str
    role: str = Field("editor", pattern="^(editor|viewer)$")


class ProjectRemoveCollaboratorRequest(BaseModel):
    """Remove collaborator request schema"""

    user_id: str


class ProjectUpdateCollaboratorRoleRequest(BaseModel):
    """Update collaborator role request schema"""

    user_id: str
    role: str = Field(..., pattern="^(editor|viewer)$")
