from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ONE_FRANC = Decimal(1)


def calculate_trip(
    *,
    distance_km: Decimal,
    consumption_l_per_100_km: Decimal,
    fuel_price_chf_per_l: Decimal,
    extra_costs_chf: Decimal,
    passenger_count: int,
) -> dict[str, Decimal | int]:
    """Calculate fuel cost and an equal rounded-up passenger contribution."""
    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero.")
    if consumption_l_per_100_km <= 0:
        raise ValueError("Fuel consumption must be greater than zero.")
    if not Decimal("1.0") <= fuel_price_chf_per_l <= Decimal("3.5"):
        raise ValueError("Fuel price must be between 1.0 and 3.5 CHF per liter.")
    if extra_costs_chf < 0:
        raise ValueError("Extra costs cannot be negative.")
    if not 1 <= passenger_count <= 8:
        raise ValueError("Passenger count must be between 1 and 8.")

    liters = distance_km * consumption_l_per_100_km / Decimal(100)
    fuel_cost = liters * fuel_price_chf_per_l
    total_cost = (fuel_cost + extra_costs_chf).quantize(CENT, rounding=ROUND_HALF_UP)
    passenger_share = (total_cost / passenger_count).quantize(
        ONE_FRANC, rounding=ROUND_CEILING
    )
    collected_total = passenger_share * passenger_count

    return {
        "distance_km": distance_km,
        "liters": liters,
        "fuel_cost_chf": fuel_cost.quantize(CENT, rounding=ROUND_HALF_UP),
        "extra_costs_chf": extra_costs_chf.quantize(CENT, rounding=ROUND_HALF_UP),
        "total_cost_chf": total_cost,
        "passenger_count": passenger_count,
        "passenger_share_chf": passenger_share,
        "collected_total_chf": collected_total,
        "rounding_surplus_chf": collected_total - total_cost,
    }
