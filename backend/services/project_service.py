"""
Project service for project management
"""
from sqlalchemy.orm import Session
from models import Project, User
from schemas import ProjectCreate, ProjectUpdate
from typing import Optional, Tuple, List
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class ProjectService:
    """Project service"""

    @staticmethod
    def create_project(
        db: Session,
        user_id: str,
        project_data: ProjectCreate,
    ) -> Tuple[bool, str, Optional[Project]]:
        """Create a new project"""
        try:
            project = Project(
                id=str(uuid.uuid4()),
                user_id=user_id,
                name=project_data.name,
                description=project_data.description,
                vibe_description=project_data.vibe_description,
                status="draft",
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            logger.info(f"Project created: {project.id} by user {user_id}")
            return True, "Project created successfully", project
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating project: {e}")
            return False, "Error creating project", None

    @staticmethod
    def get_project_by_id(db: Session, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_user_projects(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Project]:
        """Get all projects for a user"""
        return (
            db.query(Project)
            .filter(Project.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_project(
        db: Session,
        project_id: str,
        update_data: ProjectUpdate,
    ) -> Tuple[bool, str, Optional[Project]]:
        """Update project"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found", None

            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(project, key, value)

            project.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(project)
            logger.info(f"Project updated: {project.id}")
            return True, "Project updated successfully", project
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating project: {e}")
            return False, "Error updating project", None

    @staticmethod
    def delete_project(db: Session, project_id: str) -> Tuple[bool, str]:
        """Delete project"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found"

            db.delete(project)
            db.commit()
            logger.info(f"Project deleted: {project_id}")
            return True, "Project deleted successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting project: {e}")
            return False, "Error deleting project"

    @staticmethod
    def generate_project_code(
        db: Session,
        project_id: str,
        vibe_description: str,
    ) -> Tuple[bool, str, Optional[str]]:
        """Generate project code using AI"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found", None

            # TODO: Integrate with Google Gemini API
            # For now, return a placeholder
            generated_code = f"<!-- Generated code for: {vibe_description} -->"

            project.generated_code = generated_code
            project.status = "generated"
            project.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(project)
            logger.info(f"Code generated for project: {project_id}")
            return True, "Code generated successfully", generated_code
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating code: {e}")
            return False, "Error generating code", None

    @staticmethod
    def publish_project(db: Session, project_id: str) -> Tuple[bool, str]:
        """Publish project"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found"

            project.status = "published"
            project.published_at = datetime.utcnow()
            project.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Project published: {project_id}")
            return True, "Project published successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error publishing project: {e}")
            return False, "Error publishing project"

    @staticmethod
    def archive_project(db: Session, project_id: str) -> Tuple[bool, str]:
        """Archive project"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found"

            project.status = "archived"
            project.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Project archived: {project_id}")
            return True, "Project archived successfully"
        except Exception as e:
            db.rollback()
            logger.error(f"Error archiving project: {e}")
            return False, "Error archiving project"

    @staticmethod
    def count_user_projects(db: Session, user_id: str) -> int:
        """Count projects for a user"""
        return db.query(Project).filter(Project.user_id == user_id).count()

    @staticmethod
    def get_project_by_slug(db: Session, slug: str) -> Optional[Project]:
        """Get project by slug"""
        return db.query(Project).filter(Project.slug == slug).first()

    @staticmethod
    def duplicate_project(
        db: Session,
        project_id: str,
        user_id: str,
    ) -> Tuple[bool, str, Optional[Project]]:
        """Duplicate a project"""
        try:
            original_project = ProjectService.get_project_by_id(db, project_id)
            if not original_project:
                return False, "Project not found", None

            new_project = Project(
                id=str(uuid.uuid4()),
                user_id=user_id,
                name=f"{original_project.name} (Copy)",
                description=original_project.description,
                vibe_description=original_project.vibe_description,
                generated_code=original_project.generated_code,
                status="draft",
            )
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            logger.info(f"Project duplicated: {project_id} -> {new_project.id}")
            return True, "Project duplicated successfully", new_project
        except Exception as e:
            db.rollback()
            logger.error(f"Error duplicating project: {e}")
            return False, "Error duplicating project", None

    @staticmethod
    def export_project(db: Session, project_id: str) -> Tuple[bool, str, Optional[dict]]:
        """Export project as JSON"""
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Project not found", None

            export_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "vibe_description": project.vibe_description,
                "generated_code": project.generated_code,
                "status": project.status,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
            }
            logger.info(f"Project exported: {project_id}")
            return True, "Project exported successfully", export_data
        except Exception as e:
            logger.error(f"Error exporting project: {e}")
            return False, "Error exporting project", None
