"""
contexlog - Minimalistic context-aware structured logging for Python.

A lightweight logging library that provides thread-safe and async-aware context
management for structured logging. Perfect for tracking requests, users, and other
identifiers across your application.

Features:
    - Zero runtime dependencies
    - Context-aware logging using contextvars
    - Thread-safe and async-safe
    - Colored terminal output
    - Type hints support
    - Minimal configuration required

Example:
    >>> from tinystructlog import get_logger, set_log_context
    >>> log = get_logger(__name__)
    >>> set_log_context(user_id="123", request_id="abc-def")
    >>> log.info("Processing user request")
    [2024-01-17 10:30:45] [INFO] [main.<module>:4] [request_id=abc-def user_id=123] Processing user request
"""

from .core import (
    DEFAULT_DATEFMT,
    DEFAULT_FORMAT,
    DETAILED_FORMAT,
    MINIMAL_FORMAT,
    SIMPLE_FORMAT,
    ColoredFormatter,
    ContextFilter,
    clear_log_context,
    get_logger,
    log_context,
    set_log_context,
)

__version__ = "0.1.1"
__all__ = [
    "get_logger",
    "set_log_context",
    "clear_log_context",
    "log_context",
    "ContextFilter",
    "ColoredFormatter",
    "DEFAULT_FORMAT",
    "MINIMAL_FORMAT",
    "DETAILED_FORMAT",
    "SIMPLE_FORMAT",
    "DEFAULT_DATEFMT",
]
