from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)


class DataSourceRun(Base):
    __tablename__ = "data_source_runs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('succeeded', 'failed')",
            name="ck_data_source_runs_status",
        ),
        CheckConstraint(
            "records_found >= 0 AND records_accepted >= 0",
            name="ck_data_source_runs_record_counts",
        ),
        Index("ix_data_source_runs_source_started", "source_id", "started_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("data_sources.id", ondelete="RESTRICT"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    records_found: Mapped[int] = mapped_column(Integer, nullable=False)
    records_accepted: Mapped[int] = mapped_column(Integer, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(500))


class FuelPriceObservation(Base):
    __tablename__ = "fuel_price_observations"
    __table_args__ = (
        CheckConstraint(
            "fuel_type IN ('bleifrei_95', 'bleifrei_98', 'diesel')",
            name="ck_fuel_price_observations_fuel_type",
        ),
        CheckConstraint(
            "price_per_liter >= 1.0 AND price_per_liter <= 3.5",
            name="ck_fuel_price_observations_price_range",
        ),
        CheckConstraint(
            "currency = 'CHF'",
            name="ck_fuel_price_observations_currency",
        ),
        Index("ix_fuel_price_latest_by_type", "fuel_type", "fetched_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("data_sources.id", ondelete="RESTRICT"), nullable=False
    )
    source: Mapped[DataSource] = relationship()
    run_id: Mapped[int] = mapped_column(
        ForeignKey("data_source_runs.id", ondelete="RESTRICT"), nullable=False
    )
    fuel_type: Mapped[str] = mapped_column(String(16), nullable=False)
    price_per_liter: Mapped[Decimal] = mapped_column(Numeric(6, 3), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, server_default="CHF"
    )
    valid_since: Mapped[date] = mapped_column(Date, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    source_note: Mapped[str | None] = mapped_column(String(500))
