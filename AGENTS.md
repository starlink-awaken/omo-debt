# AGENTS.md — OMO Debt

> eCOS v5 债务管理工具 · 技术债务 + 治理债务 + 改革债务 生命周期管理

## Quick Commands

```bash
cd projects/omo-debt
uv run pytest tests/ -q
uv run ruff check src/
```

## Architecture

OMO 治理体系中的债务子系统：

```
omo/                  ── OMO 治理引擎
omo-debt/             ── 债务生命周期管理（本仓）
omo-debt 原为 omo 的一部分，独立部署以解耦
```

### 债务类型

| 类型 | 说明 |
|:-----|:------|
| 技术债务 | 代码质量、测试覆盖、架构违规 |
| 治理债务 | 文档缺失、流程违规、SSOT 偏离 |
| 改革债务 | 遗留迁移、API 版本对齐、架构重构 |

## Dependencies

- Python >=3.10, uv

## Testing

```bash
uv run pytest tests/ -q
```

## Workspace-Wide Governance (2026-06-24)

This project follows the workspace-level governance conventions documented in the root `AGENTS.md`:

- **Agent Mutation Protocol**: Any autonomous agent/cron/daemon that modifies workspace state must emit `agent_mutation_intent`, avoid direct file I/O to `.omo/`/`spaces/`, and commit immediately. See `.omo/standards/agent-mutation-protocol.md` for the full protocol.
- **SSOT Guardian**: Run `python3 bin/ssot-guardian.py` from the workspace root before committing to detect task-count, current-wave, submodule-pointer, or direct-omo-io drift.
- **direct-omo-io**: Scripts must route writes to `.omo/` through `omo CLI`, `projects/omo` core, or `projects/c2g` ingress — never via raw `open()/mkdir()/write_text()`.
- **Submodule Governance**: Commit changes inside the submodule first, then bump the root-repo pointer; `git submodule status` with a `+` prefix indicates pending drift.
