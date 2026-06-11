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
