"""Initial schema creation

Revision ID: 001
Revises: 
Create Date: 2026-01-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema"""
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("two_factor_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("two_factor_secret", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create projects table
    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("vibe_description", sa.Text(), nullable=False),
        sa.Column("slug", sa.String(200), nullable=True, unique=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("generated_code", sa.Text(), nullable=True),
        sa.Column("preview_url", sa.String(500), nullable=True),
        sa.Column("live_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_sessions_user_id", "sessions", ["user_id"])
    op.create_index("idx_sessions_token", "sessions", ["token"])
    op.create_index("idx_projects_user_id", "projects", ["user_id"])
    op.create_index("idx_projects_status", "projects", ["status"])
    op.create_index("idx_projects_slug", "projects", ["slug"])


def downgrade() -> None:
    """Drop initial schema"""
    # Drop indexes
    op.drop_index("idx_projects_slug")
    op.drop_index("idx_projects_status")
    op.drop_index("idx_projects_user_id")
    op.drop_index("idx_sessions_token")
    op.drop_index("idx_sessions_user_id")
    op.drop_index("idx_users_email")

    # Drop tables
    op.drop_table("projects")
    op.drop_table("sessions")
    op.drop_table("users")
