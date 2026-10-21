import argparse
from datetime import date
from decimal import Decimal

from app.db import SessionLocal
from app.schemas import FuelPriceCreate, FuelType
from app.services.fuel_prices import record_manual_price


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a manually verified fuel price in the database."
    )
    parser.add_argument(
        "--fuel-type",
        choices=[item.value for item in FuelType],
        required=True,
    )
    parser.add_argument(
        "--price-per-liter",
        type=Decimal,
        required=True,
    )
    parser.add_argument(
        "--valid-since",
        type=date.fromisoformat,
        required=True,
    )
    parser.add_argument("--source-note", required=True)
    args = parser.parse_args()
    price_input = FuelPriceCreate(
        fuel_type=args.fuel_type,
        price_per_liter=args.price_per_liter,
        valid_since=args.valid_since,
        source_note=args.source_note,
    )

    with SessionLocal() as session:
        observation = record_manual_price(
            session=session,
            fuel_type=price_input.fuel_type,
            price_per_liter=price_input.price_per_liter,
            valid_since=price_input.valid_since,
            source_note=price_input.source_note,
        )
    print(
        f"Recorded fuel price observation {observation.id} for {observation.fuel_type}."
    )


if __name__ == "__main__":
    main()
