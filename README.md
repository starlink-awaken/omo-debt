# omo-debt

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
