# Publishing Guide for tinystructlog

This document contains all the instructions for publishing and maintaining the tinystructlog package.

## 1. Publishing to PyPI

### 1.1 Publishing a Release

Publishing is automated via GitHub Actions. Here's how to release:

```bash
cd /Users/vykhand/DEV/tinystructlog

# Make sure all tests pass
uv run pytest --cov=tinystructlog --cov-report=term-missing

# Make sure linting passes
uv run black --check src tests
uv run ruff check src tests

# Build package locally to verify
uv run python -m build
uv run twine check dist/*

# If all checks pass, create and push a version tag
git tag v0.1.0
git push origin v0.1.0
```

**What happens next:**
1. GitHub Actions workflow `.github/workflows/publish.yml` triggers automatically
2. Package is built
3. Package is uploaded to PyPI
4. GitHub Release is created with release notes

**Verify publication:**
- Check PyPI: https://pypi.org/project/tinystructlog/
- Install and test: `pip install tinystructlog`

### 1.2 Manual Publishing (Fallback)

If GitHub Actions fails, you can publish manually:

```bash
cd /Users/vykhand/DEV/tinystructlog

# Build the package
uv run python -m build

# Upload to PyPI
uv run twine upload dist/*
# Enter your PyPI API token when prompted (username: __token__)
```

---

## 2. Publishing Documentation

### 2.1 ReadTheDocs Setup (Recommended)

1. **Create ReadTheDocs Account**
   - Go to https://readthedocs.org/accounts/signup/
   - Sign up with GitHub
   - Authorize ReadTheDocs to access your GitHub account

2. **Import Project**
   - Click "Import a Project"
   - Select "Aprova-GmbH/tinystructlog"
   - Click "Next"

3. **Configure Project**
   - Name: `tinystructlog`
   - Repository URL: `https://github.com/Aprova-GmbH/tinystructlog`
   - Default branch: `main`
   - Click "Finish"

4. **Verify Build**
   - ReadTheDocs will automatically build from `.readthedocs.yaml`
   - Check build status: https://readthedocs.org/projects/tinystructlog/builds/
   - Once built, docs are live at: https://tinystructlog.readthedocs.io

5. **Configure Webhook (Automatic)**
   - ReadTheDocs automatically adds a webhook to your GitHub repo
   - Documentation rebuilds on every push to `main`

**Advanced Configuration (Optional):**
- Add custom domain: https://docs.readthedocs.io/en/stable/custom-domains.html
- Configure versions: Enable builds for tags to have versioned docs

### 2.2 GitHub Pages (Alternative)

If you prefer GitHub Pages instead of ReadTheDocs:

```bash
cd /Users/vykhand/DEV/tinystructlog

# Build documentation
cd docs
uv run sphinx-build -b html . _build/html

# Create gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
cp -r docs/_build/html/* .
touch .nojekyll  # Disable Jekyll processing

git add .
git commit -m "Initial documentation"
git push origin gh-pages

# Switch back to main
git checkout main
```

Then enable GitHub Pages:
1. Go to https://github.com/Aprova-GmbH/tinystructlog/settings/pages
2. Source: "Deploy from a branch"
3. Branch: `gh-pages` / `/ (root)`
4. Click "Save"

Docs will be available at: https://aprova-gmbh.github.io/tinystructlog/

**Automation:** You can use the `.github/workflows/docs.yml` workflow to auto-deploy on push.

---

## 3. Creating New Versions

Follow this process for each new release:

### 3.1 Update Version Number

Update version in **two files**:

**File 1: `pyproject.toml`**
```toml
[project]
name = "tinystructlog"
version = "0.2.0"  # <- Update this
```

**File 2: `src/tinystructlog/__init__.py`**
```python
__version__ = "0.2.0"  # <- Update this
```

**File 3: `docs/conf.py`**
```python
release = "0.2.0"  # <- Update this
version = "0.2.0"  # <- Update this
```

### 3.2 Update CHANGELOG.md

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-01-25

### Added
- New feature X
- Support for Y

### Changed
- Improved performance of Z

### Fixed
- Bug fix for issue #123

## [0.1.0] - 2026-01-17

### Added
- Initial release
- Context-aware logging with contextvars
- Colored terminal output
- Full async/thread safety
```

### 3.3 Commit Changes

```bash
cd /Users/vykhand/DEV/tinystructlog

git add pyproject.toml src/tinystructlog/__init__.py docs/conf.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push origin main
```

### 3.4 Run Tests

```bash
# Run full test suite
uv run pytest --cov=tinystructlog --cov-report=term-missing -v

# Run linters
uv run black --check src tests
uv run ruff check src tests

# Build and check package
uv run python -m build
uv run twine check dist/*
```

### 3.5 Create and Push Tag

```bash
# Create annotated tag with release notes
git tag -a v0.2.0 -m "$(cat <<'EOF'
Release v0.2.0

Added:
- New feature X
- Support for Y

Changed:
- Improved performance of Z

Fixed:
- Bug fix for issue #123
EOF
)"

# Push tag to trigger automated publishing
git push origin v0.2.0
```

### 3.6 Verify Release

1. **GitHub Actions:** Check https://github.com/Aprova-GmbH/tinystructlog/actions
2. **PyPI:** Verify at https://pypi.org/project/tinystructlog/
3. **GitHub Release:** Check https://github.com/Aprova-GmbH/tinystructlog/releases
4. **Documentation:** Verify at https://tinystructlog.readthedocs.io

### 3.7 Test Installation

```bash
# In a fresh virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate
pip install --upgrade tinystructlog

# Test import
python -c "from tinystructlog import get_logger; print(get_logger.__doc__)"

# Deactivate
deactivate
```

---

## 4. Semantic Versioning Guide

Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **PATCH** (0.1.0 → 0.1.1): Bug fixes, no API changes
- **MINOR** (0.1.0 → 0.2.0): New features, backward compatible
- **MAJOR** (0.9.0 → 1.0.0): Breaking changes, incompatible API changes

**Examples:**
- Fix typo in docstring: `0.1.0 → 0.1.1` (PATCH)
- Add new optional parameter: `0.1.0 → 0.2.0` (MINOR)
- Remove deprecated function: `0.9.0 → 1.0.0` (MAJOR)

---

## 5. Pre-Release Checklist

Before creating any release, verify:

- [ ] All tests pass (`pytest`)
- [ ] Code coverage ≥90% (`pytest --cov`)
- [ ] Linting passes (`black --check`, `ruff check`)
- [ ] Documentation builds (`sphinx-build -W -b html docs docs/_build/html`)
- [ ] CHANGELOG.md updated
- [ ] Version bumped in all 3 files
- [ ] README examples still work
- [ ] Package builds successfully (`python -m build`)
- [ ] Package metadata is valid (`twine check dist/*`)

---

## 6. Troubleshooting

### GitHub Actions Fails
- Check workflow logs: https://github.com/Aprova-GmbH/tinystructlog/actions
- Verify `PYPI_API_TOKEN` secret is set correctly
- Ensure PyPI token has correct scope

### PyPI Upload Fails
- Verify you're not re-uploading the same version
- Check token permissions
- Try manual upload with `twine upload dist/*`

### Documentation Build Fails
- Check ReadTheDocs build logs
- Verify all dependencies in `pyproject.toml` under `[project.optional-dependencies]`
- Test local build: `cd docs && sphinx-build -W -b html . _build/html`

### Tests Fail After Version Bump
- Ensure version string in `__init__.py` matches `pyproject.toml`
- Clear pytest cache: `rm -rf .pytest_cache`
- Reinstall package: `uv pip install -e .`

---

## 7. Maintaining Documentation Versions

ReadTheDocs can host multiple versions:

1. **Tag-based versions:** Every git tag creates a new doc version
2. **Enable in ReadTheDocs:**
   - Go to https://readthedocs.org/projects/tinystructlog/versions/
   - Activate versions you want to publish (e.g., `v0.1.0`, `v0.2.0`)
3. **Set default version:** Choose which version shows by default (usually `latest` or `stable`)

---

## Contact

For questions about publishing or releases:
- Email: vya@aprova.ch
- GitHub Issues: https://github.com/Aprova-GmbH/tinystructlog/issues
