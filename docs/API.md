# omo-debt API / Usage Reference

> Quick reference for using **omo-debt** programmatically and from the command line.

## Command Line

- `uv run python -m omo_debt` — CLI
- `uv run pytest tests/unit/` — tests

## Programmatic API

Import `omo_debt.scorer` for programmatic scoring.

## Configuration

- Stack: python
- Dependencies: see [`../pyproject.toml`](../pyproject.toml) (Python) or [`../package.json`](../package.json) (TypeScript).
- Environment variables and ports: see workspace `protocols/port-registry.yaml` and root `.env.example`.

## Tests

See [`../README.md`](../README.md) for the test command.
