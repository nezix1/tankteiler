# TankTeiler

TankTeiler is a planned mobile-first PWA for estimating a car trip's fuel cost
and splitting it between passengers, with fuel-price data for Switzerland.
The current stage provides a calculation API and persisted manual fuel-price
observations; the frontend and external price providers are planned for later
stages.

## Current status

- FastAPI calculation API using exact decimal arithmetic
- PostgreSQL storage for manual price observations and source-run audit records
- Docker Compose development environment and Alembic migrations
- Frontend, user accounts, and external price providers are planned for later stages

## Requirements

- Docker Engine with the Docker Compose plugin
- Git

Python 3.12+ is needed for running the backend and development checks outside
Docker. Node.js is not yet required because the frontend has not been added.

## Local setup

```sh
cp .env.example .env
# Set POSTGRES_PASSWORD to a non-default local value.
# Set ADMIN_API_KEY to a long random value to enable API-based price entry.
docker compose up --build -d
docker compose ps
```

The API is available at `http://localhost:8000`; its interactive schema is at
`http://localhost:8000/docs`. Migrations run when the API container starts.
Stop the services with `docker compose down`. Persisted local database data is
kept in the `postgres_data` volume.

## Trip calculation API

`POST /api/v1/trips/calculate` accepts a distance, fuel consumption, manually
provided CHF/liter price, optional extra costs, and 1–8 passengers. It returns
fuel liters, a cost breakdown, each passenger's contribution rounded up to a
whole CHF, and the resulting rounding surplus. The price must be in the
configured sanity range of CHF 1.00–3.50 per liter.

## Manual fuel prices

The administrator endpoint is disabled unless `ADMIN_API_KEY` is configured.
Send the key in the `X-Admin-API-Key` header. Accepted records use CHF, include
both `valid_since` and server-recorded `fetched_at`, and create an audit entry in
`data_source_runs`.

```sh
curl --fail-with-body \
  -H "Content-Type: application/json" \
  -H "X-Admin-API-Key: $ADMIN_API_KEY" \
  -d "{\"fuel_type\":\"bleifrei_95\",\"price_per_liter\":\"$PRICE_PER_LITER\",\"valid_since\":\"$VALID_SINCE\",\"source_note\":\"$SOURCE_NOTE\"}" \
  http://localhost:8000/api/v1/admin/fuel-prices
```

Alternatively, record a manually verified value from inside the running
backend container:

```sh
docker compose exec api python -m app.seed_price \
  --fuel-type "$FUEL_TYPE" \
  --price-per-liter "$PRICE_PER_LITER" \
  --valid-since "$VALID_SINCE" \
  --source-note "$SOURCE_NOTE"
```

These commands require values supplied by the operator; the repository does
not include a production fuel price or seed one automatically.

## Configuration

`.env.example` lists the local PostgreSQL settings. Keep real credentials and
API keys in `.env` or the deployment environment; `.env` is ignored by Git.
Never commit database dumps or raw downloaded source data.

## Development checks

Install Python 3.12+ and pre-commit. Gitleaks must also be installed for its
configured pre-commit hook. Docker is required for Compose validation and image
builds.

```sh
cd backend
python -m pip install pre-commit
python -m pip install -e ".[dev]"
cd ..
pre-commit install
pre-commit run --all-files
python -m pytest -q backend/tests
POSTGRES_PASSWORD=ci-only docker compose config --quiet
```

CI runs repository hooks, backend tests, PostgreSQL migrations, Compose
validation, and a backend image build. Frontend checks will be added when the
frontend is introduced.

## Data and licensing

The application is MIT-licensed. Third-party datasets and map content retain
their own terms and attribution requirements. No external data provider is
integrated in this bootstrap stage; provider terms must be verified before
implementation.

## GitHub setup

After the bootstrap commit is pushed:

1. Enable Secret scanning and Dependabot security updates in repository settings.
2. Add branch protection for `main`: require pull requests, require the
   `Repository checks` status, and disallow force-pushes.
3. Enable Dependabot version updates; this repository currently configures
   GitHub Actions updates. Add Python and npm ecosystems when their manifests
   are introduced.
4. Create project milestones and a GitHub Project board for the planned stages.

## Project documentation

- [Project prompt and requirements](docs/ai-prompt.md)
- [Architecture and planned decisions](ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)
