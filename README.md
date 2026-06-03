# omo-debt

Pattern 09 v2.0: Project lifecycle stage-aware technical debt scoring CLI tool.

## Installation

```bash
pip install omo-debt
```

## Usage

```bash
# Identify project stage
omo-debt identify-stage /path/to/project

# Calculate debt score
omo-debt score --impact 9 --frequency 8 --cost 7 --stage rapid-evolution

# Compare debt items
omo-debt compare debt1.yaml debt2.yaml

# Analyze project
omo-debt analyze /path/to/project
```

## Development

Created as part of M3 milestone (OMO v2.0 → v3.0 evolution).
