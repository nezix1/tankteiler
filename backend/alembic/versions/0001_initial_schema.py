"""Create source audit and fuel price tables.

Revision ID: 0001_initial_schema
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "data_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.UniqueConstraint("slug", name="uq_data_sources_slug"),
    )
    op.create_table(
        "data_source_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("records_found", sa.Integer(), nullable=False),
        sa.Column("records_accepted", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.String(length=500), nullable=True),
        sa.CheckConstraint(
            "status IN ('succeeded', 'failed')",
            name="ck_data_source_runs_status",
        ),
        sa.CheckConstraint(
            "records_found >= 0 AND records_accepted >= 0",
            name="ck_data_source_runs_record_counts",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["data_sources.id"], ondelete="RESTRICT"
        ),
    )
    op.create_index(
        "ix_data_source_runs_source_started",
        "data_source_runs",
        ["source_id", "started_at"],
    )
    op.create_table(
        "fuel_price_observations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("fuel_type", sa.String(length=16), nullable=False),
        sa.Column("price_per_liter", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
            server_default="CHF",
        ),
        sa.Column("valid_since", sa.Date(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_note", sa.String(length=500), nullable=True),
        sa.CheckConstraint(
            "fuel_type IN ('bleifrei_95', 'bleifrei_98', 'diesel')",
            name="ck_fuel_price_observations_fuel_type",
        ),
        sa.CheckConstraint(
            "price_per_liter >= 1.0 AND price_per_liter <= 3.5",
            name="ck_fuel_price_observations_price_range",
        ),
        sa.CheckConstraint(
            "currency = 'CHF'",
            name="ck_fuel_price_observations_currency",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["data_sources.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["run_id"], ["data_source_runs.id"], ondelete="RESTRICT"
        ),
    )
    op.create_index(
        "ix_fuel_price_latest_by_type",
        "fuel_price_observations",
        ["fuel_type", "fetched_at"],
    )
    op.bulk_insert(
        sa.table(
            "data_sources",
            sa.column("slug", sa.String()),
            sa.column("name", sa.String()),
        ),
        [{"slug": "manual", "name": "Manual administrator entry"}],
    )


def downgrade() -> None:
    op.drop_index("ix_fuel_price_latest_by_type", table_name="fuel_price_observations")
    op.drop_table("fuel_price_observations")
    op.drop_index("ix_data_source_runs_source_started", table_name="data_source_runs")
    op.drop_table("data_source_runs")
    op.drop_table("data_sources")
