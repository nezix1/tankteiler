# TankTeiler

TankTeiler is a planned mobile-first PWA for estimating a car trip's fuel cost
and splitting it between passengers, with fuel-price data for Switzerland.
This initial commit establishes repository and development infrastructure;
application code has not been added yet.

## Current status

- Project skeleton and local PostgreSQL service
- CI checks for repository hygiene and Docker Compose configuration
- Application services, migrations, and frontend are planned for later stages

## Requirements

- Docker Engine with the Docker Compose plugin
- Git

The initial infrastructure was prepared with Python 3.12+ and Node.js 20+ in
mind. Python and Node dependencies will be added with the relevant application
stages.

## Local setup

```sh
cp .env.example .env
# Edit .env and set a non-default local POSTGRES_PASSWORD.
docker compose up -d db
docker compose ps
```

Stop the database with `docker compose down`. Persisted local database data is
kept in the `postgres_data` volume; remove it only when you intentionally want
to delete the local database.

## Configuration

`.env.example` lists the local PostgreSQL settings. Keep real credentials and
API keys in `.env` or the deployment environment; `.env` is ignored by Git.
Never commit database dumps or raw downloaded source data.

## Development checks

Install Python 3.12+, Node.js, Docker Compose, and pre-commit. Gitleaks must
also be installed for its configured pre-commit hook.

```sh
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
docker compose config --quiet
```

The checks for application linting, tests, and image builds will be added as
backend and frontend application code is introduced.

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
