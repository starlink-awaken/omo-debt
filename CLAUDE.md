# CLAUDE.md — OMO Debt AI Context

> Session loader for AI work inside `omo-debt`.
> Keep durable engineering rules in [`AGENTS.md`](AGENTS.md) and volatile facts in SSOT files.

## Load First

1. [`AGENTS.md`](AGENTS.md)
2. [`README.md`](README.md)
3. The source files and tests directly related to the task
4. Workspace context in [`../../CLAUDE.md`](../../CLAUDE.md) when the task crosses project boundaries

## Project Role

- Layer: L2
- Responsibility: 技术债务评分与分级 CLI
- Stack: Python / uv / pytest

## Commands

```bash
uv sync
uv run pytest "tests/unit/" -q
uv run ruff check "."
```

## Safe Editing Rules

- 评分算法版本以代码/测试/发布说明为准。
- 示例可以保留，测试数量不要写成事实快照。
- Do not commit, push, reset, or bump submodule pointers unless the user explicitly asks.
- Preserve unrelated dirty changes in this repository.
- Keep Markdown pointed at SSOT files instead of copying generated facts.

## Closeout

```bash
git status --short
uv run --with "pyyaml" python "../../bin/doc-ssot-lint.py" --json
```

Report the checks you actually ran and any pre-existing dirty state that remains.
