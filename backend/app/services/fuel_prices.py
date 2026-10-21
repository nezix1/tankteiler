from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DataSource, DataSourceRun, FuelPriceObservation
from app.schemas import FuelType


def record_manual_price(
    *,
    session: Session,
    fuel_type: FuelType,
    price_per_liter: Decimal,
    valid_since: date,
    source_note: str | None,
    fetched_at: datetime | None = None,
) -> FuelPriceObservation:
    """Store a manually entered price and its source-run audit record."""
    now = fetched_at or datetime.now(UTC)
    source = session.scalar(select(DataSource).where(DataSource.slug == "manual"))
    if source is None:
        raise RuntimeError(
            "The manual data source is missing. Apply database migrations first."
        )

    run = DataSourceRun(
        source_id=source.id,
        started_at=now,
        completed_at=now,
        status="succeeded",
        records_found=1,
        records_accepted=1,
    )
    session.add(run)
    session.flush()

    observation = FuelPriceObservation(
        source_id=source.id,
        run_id=run.id,
        fuel_type=fuel_type.value,
        price_per_liter=price_per_liter,
        currency="CHF",
        valid_since=valid_since,
        fetched_at=now,
        source_note=source_note,
    )
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation
