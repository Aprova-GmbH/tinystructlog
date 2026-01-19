# Quick Reference Guide

**tinystructlog** - Quick commands and workflows for daily development

---

## Daily Development

### Running Tests

```bash
# Run all tests
uv run pytest -v

# Run with coverage report
uv run pytest --cov=tinystructlog --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_logger.py -v

# Run tests matching pattern
uv run pytest -k "test_context" -v
```

### Code Quality

```bash
# Format code (auto-fix)
uv run black src tests

# Check formatting (no changes)
uv run black --check src tests

# Lint code
uv run ruff check src tests

# Auto-fix linting issues
uv run ruff check --fix src tests
```

### Building Documentation

```bash
# Build docs
uv run sphinx-build -b html docs docs/_build/html

# Build with warnings as errors
uv run sphinx-build -W -b html docs docs/_build/html

# Open built docs
open docs/_build/html/index.html  # macOS
xdg-open docs/_build/html/index.html  # Linux
```

### Local Package Testing

```bash
# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Build package locally
uv run python -m build

# Check package metadata
uv run twine check dist/*

# Test import
python -c "from tinystructlog import get_logger; print('OK')"
```

---

## Publishing a New Release

```bash
# 1. Update version in 3 files:
#    - pyproject.toml (line 3)
#    - src/tinystructlog/__init__.py (line 33)
#    - docs/conf.py (lines 18-19)

# 2. Update CHANGELOG.md with changes

# 3. Run tests
cd /Users/vykhand/DEV/tinystructlog
uv run pytest --cov=tinystructlog --cov-report=term-missing
uv run black --check src tests
uv run ruff check src tests

# 4. Commit version bump
git add pyproject.toml src/tinystructlog/__init__.py docs/conf.py CHANGELOG.md
git commit -m "Bump version to X.Y.Z"
git push origin main

# 5. Create and push tag (this triggers automatic publishing)
git tag vX.Y.Z
git push origin vX.Y.Z

# Done! GitHub Actions will:
# - Build package
# - Publish to PyPI
# - Create GitHub release
# - ReadTheDocs will rebuild docs automatically
```

---

## Verify Release

```bash
# Check GitHub Actions
open https://github.com/Aprova-GmbH/tinystructlog/actions

# Check PyPI
open https://pypi.org/project/tinystructlog/

# Check Docs
open https://tinystructlog.readthedocs.io

# Test installation
pip install --upgrade tinystructlog
python -c "from tinystructlog import get_logger; print('OK')"
```

---

## Git Workflows

### Common Git Operations

```bash
# Check status
git status

# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Add feature X"

# Push branch
git push origin feature/my-feature

# Switch back to main
git checkout main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline --graph --decorate
```

### Fixing Mistakes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard uncommitted changes
git checkout -- file.py

# Amend last commit message
git commit --amend -m "Better message"

# View what changed in last commit
git show HEAD
```

---

## Project Structure

```
tinystructlog/
├── src/tinystructlog/      # Source code
│   ├── __init__.py          # Package entry point
│   └── core.py              # Core logging implementation
├── tests/                   # Test suite
│   ├── test_context.py      # Context management tests
│   ├── test_formatting.py   # Formatter tests
│   └── test_logger.py       # Logger tests
├── docs/                    # Sphinx documentation
│   ├── conf.py              # Sphinx configuration
│   ├── index.rst            # Documentation homepage
│   ├── api.rst              # API reference
│   ├── quickstart.rst       # Quick start guide
│   └── examples.rst         # Usage examples
├── .github/workflows/       # GitHub Actions
│   └── publish.yml          # PyPI publishing workflow
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project README
├── PUBLISHING.md            # Detailed publishing guide
└── QUICK_REFERENCE.md       # This file
```

---

## Important Files

- **`pyproject.toml`**: Package metadata, dependencies, build config, tool settings
- **`src/tinystructlog/__init__.py`**: Version number, public API exports
- **`docs/conf.py`**: Documentation version (must match pyproject.toml)
- **`.github/workflows/publish.yml`**: Automated PyPI publishing on git tags
- **`README.md`**: Package documentation on GitHub/PyPI

---

## Semantic Versioning

- **Patch** (0.1.0 → 0.1.1): Bug fixes only, no API changes
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.9.0 → 1.0.0): Breaking changes, incompatible API changes

**Examples:**
- Fix typo in docstring → Patch (0.1.1)
- Add new optional parameter → Minor (0.2.0)
- Remove deprecated function → Major (1.0.0)

---

## Troubleshooting

### Tests Failing

```bash
# Clear pytest cache
rm -rf .pytest_cache __pycache__

# Reinstall package in editable mode
uv pip install -e ".[dev]"

# Run with verbose output
uv run pytest -vv
```

### Build Failures

```bash
# Clean build artifacts
rm -rf dist/ build/ *.egg-info

# Rebuild from scratch
uv run python -m build
```

### Documentation Build Errors

```bash
# Clean docs build
rm -rf docs/_build

# Rebuild with full traceback
uv run sphinx-build -b html docs docs/_build/html --traceback
```

### Import Errors

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify package installed
uv pip list | grep tinystructlog

# Reinstall
uv pip uninstall tinystructlog
uv pip install -e ".[dev]"
```

---

## Emergency: Manual Publishing

If GitHub Actions fails, publish manually:

```bash
# Build package
uv run python -m build

# Upload to PyPI
uv run twine upload dist/*
# Username: __token__
# Password: pypi-AgE... (your PyPI token)
```

---

## Useful Links

- **Repository**: https://github.com/Aprova-GmbH/tinystructlog
- **PyPI Package**: https://pypi.org/project/tinystructlog/
- **Documentation**: https://tinystructlog.readthedocs.io
- **Issues**: https://github.com/Aprova-GmbH/tinystructlog/issues
- **GitHub Actions**: https://github.com/Aprova-GmbH/tinystructlog/actions

---

## Quick Cheat Sheet

```bash
# Pre-commit checklist
uv run pytest --cov=tinystructlog --cov-report=term-missing
uv run black --check src tests
uv run ruff check src tests
uv run sphinx-build -W -b html docs docs/_build/html

# Release checklist
# 1. Update version in: pyproject.toml, src/tinystructlog/__init__.py, docs/conf.py
# 2. Update CHANGELOG.md
# 3. Run tests and checks (above)
# 4. Commit: git add . && git commit -m "Bump version to X.Y.Z"
# 5. Tag: git tag vX.Y.Z
# 6. Push: git push origin main --tags
```
