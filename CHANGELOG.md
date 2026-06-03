# Changelog

All notable changes to omo-debt will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-03

### Added

#### Core Features
- **Pattern 09 v2.0 Algorithm**: Lifecycle-aware technical debt scoring
  - Three-stage lifecycle model (rapid evolution / stable growth / maintenance)
  - Dynamic weight adjustment based on project stage
  - Normalization factors (1.0, 1.1, 1.2) for stage-specific scoring
  - Priority classification (P0/P1/P2) with threshold-based scoring

#### CLI Commands
- `identify-stage`: Project lifecycle stage identification
  - Git commit history analysis (6-month rolling window)
  - Monthly commit average calculation
  - Confidence scoring for boundary cases
  - Recommended weights and normalization factors

- `score`: Technical debt scoring
  - Multi-factor scoring (impact, frequency, cost)
  - Automatic stage detection via `--project-path`
  - Base score and normalized score calculation
  - Priority-based recommendations

- `compare`: Multi-debt comparison
  - Batch YAML file processing
  - Priority-based sorting
  - Rich table output with color-coded priorities
  - Multiple output formats (table/json/yaml)
  - Statistical summary of priority distribution

- `analyze`: Project health analysis
  - Comprehensive health scoring (0-100 scale)
  - Health grade assignment (优秀/良好/一般/较差/危险)
  - Debt distribution statistics by priority
  - Improvement recommendations
  - Markdown report export

#### User Experience
- Rich terminal formatting with tables and panels
- Color-coded priority indicators (🔴 P0 / 🟡 P1 / 🟢 P2)
- Verbose mode for detailed analysis
- Multiple output format support (table/json/yaml/markdown)

#### Testing & Quality
- 45+ unit tests across 2 test modules
- Core algorithm validation (stage identification, scoring)
- Edge case coverage (boundary commits, confidence scoring)
- Test coverage for all 4 CLI commands

#### Documentation
- Comprehensive README with usage examples
- Sample debt YAML files (3 examples across lifecycle stages)
- Health report example output
- Algorithm specification and formulas
- PyPI packaging metadata

### Technical Details
- **Python**: 3.10+ support (tested on 3.10-3.13)
- **Dependencies**: gitpython, pyyaml, rich, pydantic, tabulate, click
- **Build**: hatchling backend with uv package manager
- **Code Quality**: ruff linting (line-length 120, target py310)
- **Testing**: pytest with coverage reporting

### Validation
- Cross-project validation across 3 lifecycle stages
- gbrain (rapid_evolution): 37.3 commits/month → 8.10 P0 score
- omostation (stable_growth): 22.8 commits/month → 5.83 P1 score
- docs-archive (maintenance): 0.5 commits/month → maintenance weights
- Validation error: 11.7%-14.4% (< 20% threshold ✅)

### Milestones
- **M1**: Pattern 09 v2.0 Design & Validation (2026-06-03)
- **M2**: Cross-Project Validation (2026-06-03)
- **M3**: CLI Tool Implementation Sprint 1-3 (2026-06-03)

---

## [Unreleased]

### Planned for v0.2.0
- Sprint 4: Production deployment (CI/CD, PyPI release)
- Task 3.2: 4P3V1L1H framework integration (诚实度维度)
- Enhanced visualization (Mermaid debt distribution charts)
- Multi-language support (i18n)

### Planned for v1.0.0 (M4)
- OMO v3.0 formal release
- Pattern 09 v2.0 upgrade to official specification
- Production-grade stability and performance
- Complete API documentation

---

## Version History

- **0.1.0** (2026-06-03): Initial beta release, core features complete
- **Unreleased**: Sprint 4 in progress

---

**Created as part of OMO v2.0 → v3.0 evolution roadmap.**

## [0.2.0] - 2026-06-03

### Added - 4P3V1L1H Framework Integration

**Pattern 09 v2.1 升级：诚实度（Honesty）维度**

- **核心算法**：
  - 三维度模型：完整性(40%) + 一致性(35%) + 可验证性(25%)
  - 诚实度评分公式：`honesty = 0.40×completeness + 0.35×consistency + 0.25×verifiability`
  - 诚实度加成：`adjusted_score = base_score × (1 + (honesty-5)/20)`
  - 优先级降级规则：低诚实度债务自动降级

- **CLI 命令**：
  - 新增 `assess-honesty` 命令：诚实度维度评估
  - 支持多种输出格式（table/json/yaml）
  - 自动检测证据完整性

- **数据模型**：
  - 扩展债务 YAML 格式支持 `honesty` 字段
  - 包含完整性、一致性、可验证性子维度
  - 证据链接（commits/issues/references）

- **测试覆盖**：
  - 25 个单元测试（100% 通过）
  - 87% 代码覆盖率
  - 核心模块 93% 覆盖率

### Changed

- Pattern 09 v2.0 → v2.1 升级
- 4P3V1L → 4P3V1L1H 框架集成

### Technical Details

**完整性（Completeness）检测**：
- 代码覆盖率对比（问题文件 vs 债务清单）
- 关键区域覆盖（核心/安全/性能）
- 历史问题覆盖（披露 vs 隐藏）

**一致性（Consistency）检测**：
- 评分偏差检测（vs 同类债务平均分）
- 时间一致性（评分波动监控）
- 跨项目一致性（类似债务对比）

**可验证性（Verifiability）检测**：
- 证据完整性（影响/频率/成本三维证据）
- 数据溯源（commit/issue/doc 引用）

**影响范围**：
- 894 行核心代码
- 325 行测试代码
- 1 个新 CLI 命令
- 扩展 YAML 数据模型

