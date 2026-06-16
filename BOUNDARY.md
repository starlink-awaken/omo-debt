# omo-debt — System Boundary

> 本文档描述 omo-debt 与 eCOS 系统其他部分的边界：暴露的接口、依赖的上游、影响的下游。
>
> 架构演进对比参见：[`docs/ARCHITECTURE-EVOLUTION.md`](../docs/ARCHITECTURE-EVOLUTION.md)

---

## 1. 暴露接口

### BOS URI



### 入口

- **CLI**: `omo-debt` identify-stage/score/compare/analyze/assess-honesty

## 2. 上游依赖

- omo (L2)

## 3. 下游影响

- .omo/debt/registry.yaml

## 4. 配置 / SSOT

- 项目源码：`projects/omo-debt/`
- 入口定义：`projects/omo-debt/pyproject.toml` 或 `package.json`
- 测试：`cd projects/omo-debt && uv run pytest tests/ -q`
