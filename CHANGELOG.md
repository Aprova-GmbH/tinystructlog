# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-01-17

### Added
- Initial release of contexlog
- Core context management with `set_log_context()`, `clear_log_context()`, and `log_context()`
- Context-aware logger creation with `get_logger()`
- Thread-safe and async-safe context isolation using `contextvars`
- Colored terminal output with `ColoredFormatter`
- Context injection via `ContextFilter`
- Zero runtime dependencies
- Full type hints support (PEP 561)
- Comprehensive test suite with >90% coverage
- Documentation and examples
- MIT license

[Unreleased]: https://github.com/vykhand/contexlog/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vykhand/contexlog/releases/tag/v0.1.0
