# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-01-18

### Added
- Documentation update: added comparison with loguru

## [0.1.1] - 2026-01-18

### Added
- Custom log format support via `fmt` and `datefmt` parameters in `get_logger()`
- Preset format constants: `MINIMAL_FORMAT`, `DETAILED_FORMAT`, `SIMPLE_FORMAT`
- Exported `DEFAULT_FORMAT` and `DEFAULT_DATEFMT` constants for reference
- Comprehensive examples for custom formats in README and documentation

### Changed
- Documentation now explicitly states that v0.1.0 had an opinionated, hardcoded format
- Enhanced API documentation with custom format examples and usage patterns

### Note
- **Fully backward compatible** - default behavior unchanged from v0.1.0
- Calling `get_logger(__name__)` without parameters produces identical output to v0.1.0

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


[0.1.2]: https://github.com/vykhand/tinystructlog/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/vykhand/tinystructlog/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/vykhand/tinystructlog/releases/tag/v0.1.0
