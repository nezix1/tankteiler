from app.main import app
from app.models import DataSourceRun, FuelPriceObservation
from fastapi.testclient import TestClient
from sqlalchemy import func, select


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_trip_endpoint_returns_cost_breakdown(client: TestClient) -> None:
    response = client.post(
        "/api/v1/trips/calculate",
        json={
            "distance_km": "100",
            "consumption_l_per_100_km": "10",
            "fuel_price_chf_per_l": "1.50",
            "extra_costs_chf": "2.40",
            "passenger_count": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "distance_km": "100",
        "liters": "10",
        "fuel_cost_chf": "15.00",
        "extra_costs_chf": "2.40",
        "total_cost_chf": "17.40",
        "passenger_count": 2,
        "passenger_share_chf": "9",
        "collected_total_chf": "18",
        "rounding_surplus_chf": "0.60",
    }


def test_manual_price_requires_admin_key(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/fuel-prices",
        json={
            "fuel_type": "bleifrei_95",
            "price_per_liter": "1.789",
            "valid_since": "2026-10-01",
        },
    )

    assert response.status_code == 401


def test_manual_price_endpoint_is_disabled_without_configured_key(
    client: TestClient,
    monkeypatch,
) -> None:
    monkeypatch.delenv("ADMIN_API_KEY")
    response = client.post(
        "/api/v1/admin/fuel-prices",
        headers={"X-Admin-API-Key": "test-admin-key"},
        json={
            "fuel_type": "bleifrei_95",
            "price_per_liter": "1.789",
            "valid_since": "2026-10-01",
        },
    )

    assert response.status_code == 503


def test_manual_price_rejects_value_outside_sanity_range(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/admin/fuel-prices",
        headers={"X-Admin-API-Key": "test-admin-key"},
        json={
            "fuel_type": "bleifrei_95",
            "price_per_liter": "3.501",
            "valid_since": "2026-10-01",
        },
    )

    assert response.status_code == 422


def test_manual_price_records_observation_and_source_run(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/fuel-prices",
        headers={"X-Admin-API-Key": "test-admin-key"},
        json={
            "fuel_type": "bleifrei_95",
            "price_per_liter": "1.789",
            "valid_since": "2026-10-01",
            "source_note": "Verified by administrator",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["fuel_type"] == "bleifrei_95"
    assert body["price_per_liter"] == "1.789"
    assert body["currency"] == "CHF"
    assert body["valid_since"] == "2026-10-01"
    assert body["source_slug"] == "manual"
    assert body["source_note"] == "Verified by administrator"

    with app.state.testing_session_factory() as session:
        assert session.scalar(select(func.count()).select_from(DataSourceRun)) == 1
        observation = session.scalar(select(FuelPriceObservation))
        assert observation is not None
        assert observation.run_id == body["run_id"]


def test_latest_price_returns_404_when_no_price_exists(client: TestClient) -> None:
    response = client.get(
        "/api/v1/fuel-prices/latest",
        params={"fuel_type": "diesel"},
    )

    assert response.status_code == 404


def test_latest_price_returns_recorded_observation(client: TestClient) -> None:
    client.post(
        "/api/v1/admin/fuel-prices",
        headers={"X-Admin-API-Key": "test-admin-key"},
        json={
            "fuel_type": "diesel",
            "price_per_liter": "1.650",
            "valid_since": "2026-10-01",
        },
    )

    response = client.get(
        "/api/v1/fuel-prices/latest",
        params={"fuel_type": "diesel"},
    )

    assert response.status_code == 200
    assert response.json()["price_per_liter"] == "1.650"
    assert response.json()["fuel_type"] == "diesel"
