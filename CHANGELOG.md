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
