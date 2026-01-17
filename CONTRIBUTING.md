# Contributing to contexlog

Thank you for your interest in contributing to contexlog! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Python version and OS
- Code samples or test cases if possible

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Use cases and examples
- Potential implementation approach (optional)

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
2. **Set up the development environment**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/contexlog.git
   cd contexlog
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Make your changes**:
   - Write clear, readable code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow the existing code style

4. **Run tests and checks**:
   ```bash
   # Run tests with coverage
   pytest

   # Format code with Black
   black src tests examples

   # Lint with Ruff
   ruff check src tests examples

   # Type check (optional)
   mypy src
   ```

5. **Ensure all tests pass** and coverage remains >90%

6. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference related issues (e.g., "Fix #123: ...")

7. **Push to your fork** and submit a pull request

8. **Respond to review feedback** - we'll review your PR and may suggest changes

## Development Guidelines

### Code Style

- **Python version**: 3.11+
- **Line length**: 100 characters (Black default)
- **Formatting**: Use Black for code formatting
- **Linting**: Code must pass Ruff checks
- **Type hints**: Add type hints to all public APIs

### Testing

- Write tests for all new functionality
- Maintain test coverage >90%
- Use pytest for testing
- Test both sync and async code paths
- Test error conditions and edge cases

### Documentation

- Update README.md for user-facing changes
- Add docstrings (Google style) to all public functions and classes
- Update API documentation in `docs/` if needed
- Add examples for new features

### Commit Messages

Use clear, descriptive commit messages:

```
Add support for custom formatters

- Implement CustomFormatter class
- Add tests for custom formatter
- Update documentation with examples

Fixes #123
```

## Project Structure

```
contexlog/
├── src/contexlog/      # Source code
│   ├── __init__.py     # Package exports
│   ├── core.py         # Main implementation
│   └── py.typed        # Type hint marker
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Usage examples
└── .github/workflows/  # CI/CD workflows
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `src/contexlog/__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.x.0`
4. Push tag: `git push origin v0.x.0`
5. GitHub Actions will automatically build and publish to PyPI

## Questions?

Feel free to open an issue for questions or join discussions in GitHub Discussions (if enabled).

## License

By contributing to contexlog, you agree that your contributions will be licensed under the Apache License 2.0.
