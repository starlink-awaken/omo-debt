# Contributing to omo-debt

Thank you for your interest in contributing to omo-debt! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/starlink-awaken/omostation.git
cd omostation/omo-debt

# Install dependencies
uv sync

# Run tests to verify setup
uv run pytest tests/unit/ -v
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions/improvements
- `refactor/` - Code refactoring

### 2. Make Changes

- Write clear, concise code
- Follow existing code style (ruff will check this)
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
uv run pytest tests/unit/ -v

# Run with coverage
uv run pytest tests/unit/ -v --cov=src/omo_debt

# Run specific test file
uv run pytest tests/unit/test_stage.py -v
```

### 4. Run Linter

```bash
# Check code style
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Check formatting
uv run ruff format --check .

# Auto-format
uv run ruff format .
```

### 5. Commit Changes

```bash
git add .
git commit -m "type(scope): description

Detailed explanation of changes...

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Commit message format:
- `feat(cli)`: New CLI feature
- `fix(scoring)`: Bug fix in scoring algorithm
- `docs(readme)`: Documentation update
- `test(stage)`: Test additions
- `refactor(core)`: Code refactoring

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style

### Python Style

- **Line length**: 120 characters
- **Target**: Python 3.10+
- **Linter**: ruff with project configuration
- **Formatting**: ruff format
- **Type hints**: Required for public APIs

### Imports

```python
# Standard library
import os
from pathlib import Path

# Third-party
import click
from rich.console import Console

# Local
from omo_debt.core import stage, scoring
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_score_v2(impact: int, frequency: int, cost: int, stage: str) -> DebtScore:
    """Calculate Pattern 09 v2.0 debt score.
    
    Args:
        impact: Impact score (1-10)
        frequency: Frequency score (1-10)
        cost: Remediation cost (1-10)
        stage: Project lifecycle stage
        
    Returns:
        DebtScore with base score, normalized score, and priority
        
    Raises:
        ValueError: If stage is unknown or scores out of range
    """
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/
│   ├── test_stage.py      # Stage identification tests
│   └── test_scoring.py    # Scoring algorithm tests
└── integration/           # Future integration tests
```

### Writing Tests

```python
def test_score_calculation():
    """Test basic score calculation."""
    result = calculate_score_v2(
        impact=9,
        frequency=8,
        cost=7,
        stage="rapid_evolution"
    )
    
    assert result.base_score == 8.10
    assert result.normalized_score == 8.10
    assert result.priority == "P0"
```

### Test Coverage

- Aim for >80% coverage on core modules
- Test edge cases and boundary conditions
- Include tests for error conditions

## Documentation

### README Updates

Update README.md when adding:
- New commands
- New options
- New features
- Breaking changes

### Code Comments

- Comment complex algorithms
- Explain "why" not "what"
- Keep comments up-to-date

### CHANGELOG

Update CHANGELOG.md for all user-facing changes:

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

## Pull Request Process

1. **Update tests**: Ensure all tests pass
2. **Update docs**: Update README, CHANGELOG, docstrings
3. **Run linter**: Ensure code passes ruff checks
4. **Describe changes**: Provide clear PR description
5. **Link issues**: Reference related issues if applicable

### PR Checklist

- [ ] Tests pass locally
- [ ] Linter passes (ruff check)
- [ ] Formatter passes (ruff format --check)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventions
- [ ] PR description is clear

## Pattern 09 v2.0 Specifics

### Core Algorithm Constraints

When modifying scoring or stage identification:

1. **Three-stage model**: Do not add/remove stages without design review
2. **Weight balance**: Weights must sum to 1.0 for each stage
3. **Normalization**: Factors must be justified with validation data
4. **Priority thresholds**: P0 ≥7.0, P1 ≥5.0, P2 <5.0

### Validation Requirements

New algorithm changes require:
- Cross-project validation (≥3 projects)
- Error analysis (target <20%)
- Documentation of reasoning

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/starlink-awaken/omostation/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md and inline docs

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to omo-debt!** 🎉
