"""initial schema

Revision ID: 20260413_000001
Revises:
Create Date: 2026-04-13 21:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260413_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_users_username"), "admin_users", ["username"], unique=True)

    op.create_table(
        "freelancers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("whatsapp", sa.String(length=255), nullable=False),
        sa.Column("instagram", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("premium", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_freelancers_category"), "freelancers", ["category"], unique=False)
    op.create_index(op.f("ix_freelancers_city"), "freelancers", ["city"], unique=False)
    op.create_index(op.f("ix_freelancers_name"), "freelancers", ["name"], unique=False)
    op.create_index(op.f("ix_freelancers_premium"), "freelancers", ["premium"], unique=False)

    op.create_table(
        "businesses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_businesses_name"), "businesses", ["name"], unique=False)

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contact_messages_email"), "contact_messages", ["email"], unique=False)
    op.create_index(op.f("ix_contact_messages_sent_at"), "contact_messages", ["sent_at"], unique=False)

    op.create_table(
        "site_assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_site_assets_key"), "site_assets", ["key"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_site_assets_key"), table_name="site_assets")
    op.drop_table("site_assets")
    op.drop_index(op.f("ix_contact_messages_sent_at"), table_name="contact_messages")
    op.drop_index(op.f("ix_contact_messages_email"), table_name="contact_messages")
    op.drop_table("contact_messages")
    op.drop_index(op.f("ix_businesses_name"), table_name="businesses")
    op.drop_table("businesses")
    op.drop_index(op.f("ix_freelancers_premium"), table_name="freelancers")
    op.drop_index(op.f("ix_freelancers_name"), table_name="freelancers")
    op.drop_index(op.f("ix_freelancers_city"), table_name="freelancers")
    op.drop_index(op.f("ix_freelancers_category"), table_name="freelancers")
    op.drop_table("freelancers")
    op.drop_index(op.f("ix_admin_users_username"), table_name="admin_users")
    op.drop_table("admin_users")
