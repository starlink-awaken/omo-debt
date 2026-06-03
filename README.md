# omo-debt

Pattern 09 v2.0: Project lifecycle stage-aware technical debt scoring CLI tool.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

## 📖 Overview

`omo-debt` is a CLI tool that implements **Pattern 09 v2.0**, a lifecycle-aware technical debt scoring model. It automatically adjusts debt priorities based on project maturity stages:

- **Rapid Evolution** (>30 commits/month): Frequency-focused (weights 0.35/0.40/0.25, norm 1.0)
- **Stable Growth** (10-30 commits/month): Balanced approach (weights 0.40/0.30/0.30, norm 1.1)
- **Maintenance** (<10 commits/month): Impact-prioritized (weights 0.50/0.20/0.30, norm 1.2)

## 🚀 Quick Start

### Installation

```bash
pip install omo-debt
```

### Basic Usage

```bash
# Identify project stage
omo-debt identify-stage /path/to/project

# Score a debt item
omo-debt score --impact 9 --frequency 8 --cost 7 --stage rapid_evolution

# Compare multiple debt items
omo-debt compare debt1.yaml debt2.yaml debt3.yaml

# Analyze project health
omo-debt analyze /path/to/project --debt-file debts.yaml
```

## 📋 Commands

### 1. `identify-stage` - Project Stage Identification

Analyzes Git commit history to determine project lifecycle stage.

```bash
omo-debt identify-stage /path/to/project [--months 6] [--verbose]
```

### 2. `score` - Debt Scoring

Calculates weighted debt score using Pattern 09 v2.0 algorithm.

```bash
omo-debt score --impact 9 --frequency 8 --cost 7 --stage rapid_evolution
```

### 3. `compare` - Multi-Debt Comparison

Compares multiple debt items and ranks by priority.

```bash
omo-debt compare debt1.yaml debt2.yaml debt3.yaml [--format table|json|yaml]
```

### 4. `analyze` - Project Health Analysis

Generates comprehensive debt health report.

```bash
omo-debt analyze /path/to/project --debt-file debts.yaml [--output report.md]
```

See [USAGE.md](docs/USAGE.md) for detailed documentation.

## 🧮 Pattern 09 v2.0 Algorithm

### Scoring Formula

```python
base_score = impact × w_impact + frequency × w_freq + cost × w_cost
normalized_score = base_score × normalization_factor
priority = "P0" if score ≥ 7.0 else "P1" if score ≥ 5.0 else "P2"
```

See [ALGORITHM.md](docs/ALGORITHM.md) for full details.

## 📊 Examples

See [examples/](examples/) directory for:
- Sample debt YAML files
- Health report output
- Multi-project comparisons

## 🏗️ Development

```bash
# Install with uv
uv sync

# Run tests
uv run pytest tests/unit/ -v

# Run linter
uv run ruff check .
```

## 📄 License

MIT License

## 📧 Contact

- Author: starlink-awaken
- Part of OMO v2.0 → v3.0 evolution

---

**Created as M3 milestone deliverable (2026-06-03)**

