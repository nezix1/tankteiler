# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- FastAPI backend with Decimal trip-cost calculations and whole-franc
  passenger-share rounding.
- Alembic schema for fuel-price observations, data-source runs, and a manual
  administrator source.
- Protected manual fuel-price API, latest-price lookup, and operator seed CLI.
- Backend test suite and CI test/image-build steps.

### Fixed

- Format bootstrap files with Prettier so repository checks pass.
- Provide a CI-only PostgreSQL password when validating the Compose configuration.
