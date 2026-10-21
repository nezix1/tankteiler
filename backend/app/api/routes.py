import os
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.domain.calculations import calculate_trip
from app.models import FuelPriceObservation
from app.schemas import (
    FuelPriceCreate,
    FuelPriceRead,
    FuelType,
    TripCalculationRequest,
    TripCalculationResponse,
)
from app.services.fuel_prices import record_manual_price

router = APIRouter()
SessionDependency = Annotated[Session, Depends(get_session)]


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/v1/trips/calculate",
    response_model=TripCalculationResponse,
    tags=["trips"],
)
def calculate_trip_cost(
    request: TripCalculationRequest,
) -> TripCalculationResponse:
    calculation = calculate_trip(
        distance_km=request.distance_km,
        consumption_l_per_100_km=request.consumption_l_per_100_km,
        fuel_price_chf_per_l=request.fuel_price_chf_per_l,
        extra_costs_chf=request.extra_costs_chf,
        passenger_count=request.passenger_count,
    )
    return TripCalculationResponse(**calculation)


@router.get(
    "/api/v1/fuel-prices/latest",
    response_model=FuelPriceRead,
    tags=["fuel prices"],
)
def get_latest_fuel_price(
    fuel_type: FuelType,
    session: SessionDependency,
) -> FuelPriceRead:
    price = session.scalar(
        select(FuelPriceObservation)
        .where(FuelPriceObservation.fuel_type == fuel_type.value)
        .order_by(
            FuelPriceObservation.fetched_at.desc(),
            FuelPriceObservation.id.desc(),
        )
        .limit(1)
    )
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fuel price is available for this fuel type.",
        )
    return FuelPriceRead.model_validate(price)


@router.post(
    "/api/v1/admin/fuel-prices",
    response_model=FuelPriceRead,
    status_code=status.HTTP_201_CREATED,
    tags=["fuel prices"],
)
def create_manual_fuel_price(
    request: FuelPriceCreate,
    session: SessionDependency,
    admin_api_key: Annotated[str | None, Header(alias="X-Admin-API-Key")] = None,
) -> FuelPriceRead:
    configured_key = os.getenv("ADMIN_API_KEY")
    if not configured_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Manual fuel-price entry is disabled.",
        )
    if admin_api_key is None or not secrets.compare_digest(
        admin_api_key, configured_key
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin API key.",
        )
    price = record_manual_price(
        session=session,
        fuel_type=request.fuel_type,
        price_per_liter=request.price_per_liter,
        valid_since=request.valid_since,
        source_note=request.source_note,
    )
    return FuelPriceRead.model_validate(price)
