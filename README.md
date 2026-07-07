# omo-debt

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributing](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Security](https://img.shields.io/badge/security-policy-blue.svg)](SECURITY.md)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple.svg)](https://docs.astral.sh/uv/)

    > X · 技术债务评分与分级 CLI
    > Metadata SSOT: [`../../docs/project-registry.yaml`](../../docs/project-registry.yaml)

    ## What It Owns

    技术债务评分与分级 CLI.

    ## Quick Start

    ```bash
    uv sync
uv run pytest "tests/unit/" -q
uv run ruff check "."
    ```

    ## Key Surfaces

    - `src/omo_debt/`
- `tests/unit/`
- `pyproject.toml`

    ## Documentation

    - Developer guide: [`AGENTS.md`](AGENTS.md)
    - AI context loader: [`CLAUDE.md`](CLAUDE.md) when present
    - Workspace architecture: [`../../ARCHITECTURE.md`](../../ARCHITECTURE.md)
    - Layer placement: [`../../LAYER-INDEX.md`](../../LAYER-INDEX.md)


## Notes

- Pattern and scoring examples remain valid as examples; algorithm truth lives in source and tests.

    ## SSOT Rules

    Runtime facts, counts, ports, health, and generated inventories are intentionally not maintained here. Use the workspace registries and project source as the truth.
## Project Governance

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)
- [Code of Conduct](CODE_OF_CONDUCT.md)