from decimal import Decimal

import pytest
from app.domain.calculations import calculate_trip


def test_rounds_each_passenger_share_up_to_a_whole_franc() -> None:
    result = calculate_trip(
        distance_km=Decimal(100),
        consumption_l_per_100_km=Decimal(10),
        fuel_price_chf_per_l=Decimal("1.50"),
        extra_costs_chf=Decimal(0),
        passenger_count=4,
    )

    assert result["liters"] == Decimal(10)
    assert result["fuel_cost_chf"] == Decimal("15.00")
    assert result["total_cost_chf"] == Decimal("15.00")
    assert result["passenger_share_chf"] == Decimal(4)
    assert result["collected_total_chf"] == Decimal(16)
    assert result["rounding_surplus_chf"] == Decimal("1.00")


def test_includes_extra_costs_before_splitting_and_rounding() -> None:
    result = calculate_trip(
        distance_km=Decimal(100),
        consumption_l_per_100_km=Decimal(10),
        fuel_price_chf_per_l=Decimal("1.50"),
        extra_costs_chf=Decimal("2.40"),
        passenger_count=2,
    )

    assert result["total_cost_chf"] == Decimal("17.40")
    assert result["passenger_share_chf"] == Decimal(9)
    assert result["collected_total_chf"] == Decimal(18)
    assert result["rounding_surplus_chf"] == Decimal("0.60")


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("distance_km", Decimal(0), "Distance must be greater than zero."),
        (
            "consumption_l_per_100_km",
            Decimal(0),
            "Fuel consumption must be greater than zero.",
        ),
        (
            "fuel_price_chf_per_l",
            Decimal("3.51"),
            "Fuel price must be between 1.0 and 3.5 CHF per liter.",
        ),
        ("extra_costs_chf", Decimal("-0.01"), "Extra costs cannot be negative."),
    ],
)
def test_rejects_invalid_calculation_values(
    field: str,
    value: Decimal,
    message: str,
) -> None:
    values = {
        "distance_km": Decimal(10),
        "consumption_l_per_100_km": Decimal(5),
        "fuel_price_chf_per_l": Decimal("1.50"),
        "extra_costs_chf": Decimal(0),
        "passenger_count": 1,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        calculate_trip(**values)


@pytest.mark.parametrize("passenger_count", [0, 9])
def test_rejects_passenger_count_outside_supported_range(
    passenger_count: int,
) -> None:
    with pytest.raises(ValueError, match="Passenger count must be between 1 and 8."):
        calculate_trip(
            distance_km=Decimal(10),
            consumption_l_per_100_km=Decimal(5),
            fuel_price_chf_per_l=Decimal("1.50"),
            extra_costs_chf=Decimal(0),
            passenger_count=passenger_count,
        )
