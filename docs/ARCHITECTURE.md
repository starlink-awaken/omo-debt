# omo-debt Architecture

> Architecture overview for **omo-debt**. For the full workspace architecture, see [`../../ARCHITECTURE.md`](../../ARCHITECTURE.md).

## Responsibilities

omo-debt is part of the eCOS v6 workspace. See [`../README.md`](../README.md) for a one-line description and [`../CAPABILITY-MAP.md`](../CAPABILITY-MAP.md) for capability mapping.

## Key Surfaces

- `src/omo_debt/` — debt scoring CLI
- `tests/unit/` — unit tests

## Design Notes

- Runtime facts (counts, ports, health) are intentionally not maintained here. Use the workspace registries and project source as the truth.
- For boundaries and call chains, read [`../BOUNDARY.md`](../BOUNDARY.md) and [`../CALLCHAIN.md`](../CALLCHAIN.md).
- For developer rules, read [`../AGENTS.md`](../AGENTS.md).
