from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator


class FuelType(StrEnum):
    BLEIFREI_95 = "bleifrei_95"
    BLEIFREI_98 = "bleifrei_98"
    DIESEL = "diesel"


class TripCalculationRequest(BaseModel):
    distance_km: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    consumption_l_per_100_km: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    fuel_price_chf_per_l: Decimal = Field(
        ge=Decimal("1.0"),
        le=Decimal("3.5"),
        max_digits=4,
        decimal_places=3,
    )
    extra_costs_chf: Decimal = Field(
        default=Decimal(0), ge=0, max_digits=10, decimal_places=2
    )
    passenger_count: int = Field(ge=1, le=8)


class TripCalculationResponse(BaseModel):
    distance_km: Decimal
    liters: Decimal
    fuel_cost_chf: Decimal
    extra_costs_chf: Decimal
    total_cost_chf: Decimal
    passenger_count: int
    passenger_share_chf: Decimal
    collected_total_chf: Decimal
    rounding_surplus_chf: Decimal


class FuelPriceCreate(BaseModel):
    fuel_type: FuelType
    price_per_liter: Decimal = Field(
        ge=Decimal("1.0"),
        le=Decimal("3.5"),
        max_digits=4,
        decimal_places=3,
    )
    valid_since: date
    source_note: str | None = Field(default=None, max_length=500)


class FuelPriceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    source_slug: str = Field(validation_alias=AliasPath("source", "slug"))
    source_name: str = Field(validation_alias=AliasPath("source", "name"))
    run_id: int
    fuel_type: FuelType
    price_per_liter: Decimal
    currency: str
    valid_since: date
    fetched_at: datetime
    source_note: str | None

    @field_validator("fetched_at")
    @classmethod
    def normalize_fetched_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
