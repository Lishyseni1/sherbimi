"""add uploaded images table

Revision ID: 20260415_000002
Revises: 20260413_000001
Create Date: 2026-04-15 14:10:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260415_000002"
down_revision = "20260413_000001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "uploaded_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storage_key", sa.String(length=64), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("data", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_uploaded_images_storage_key"), "uploaded_images", ["storage_key"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_uploaded_images_storage_key"), table_name="uploaded_images")
    op.drop_table("uploaded_images")
