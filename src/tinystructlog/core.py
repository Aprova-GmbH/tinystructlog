"""
contexlog - Minimalistic context-aware structured logging for Python.

This module provides thread-safe and async-aware logging utilities that allow you
to attach contextual information to log records. Context is automatically propagated
across async tasks and can be used to track requests, users, or any other identifiers
throughout your application.

Key Features:
    - Context variables using Python's contextvars for async/thread safety
    - Automatic context injection into log records
    - Colored terminal output with ANSI codes
    - Zero runtime dependencies
    - Full type hint support

Example:
    >>> from tinystructlog import get_logger, set_log_context
    >>> log = get_logger(__name__)
    >>> set_log_context(user_id="123", request_id="abc")
    >>> log.info("Processing request")
    [2024-01-17 10:30:45] [INFO] [module.function:10] [request_id=abc user_id=123] Processing request
"""

import contextvars
import logging
import os
import sys
from contextlib import contextmanager
from typing import Any

# A per-task/thread dict for arbitrary context (user_id, request_id, tenant, etc.)
_log_ctx: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "log_ctx", default=None
)


def set_log_context(**kwargs: Any) -> None:
    """
    Merge/override keys in the current logging context.

    Context variables are automatically injected into all log records within
    the current async task or thread. This is useful for tracking requests,
    users, tenants, or any other identifiers throughout your application.

    Args:
        **kwargs: Key-value pairs to add to the logging context. Values are
                 automatically converted to strings.

    Example:
        >>> set_log_context(user_id="123", tenant="acme")
        >>> log.info("User action")  # Will include user_id and tenant in output
    """
    cur = dict(_log_ctx.get() or {})
    cur.update({k: str(v) for k, v in kwargs.items()})
    _log_ctx.set(cur)


def clear_log_context(*keys: str) -> None:
    """
    Clear specific keys from context; if no keys provided, clear all.

    Args:
        *keys: Optional keys to remove from context. If not provided, all
              context is cleared.

    Example:
        >>> set_log_context(user_id="123", request_id="abc")
        >>> clear_log_context("request_id")  # Remove only request_id
        >>> clear_log_context()  # Remove all context
    """
    if keys:
        cur = dict(_log_ctx.get() or {})
        for k in keys:
            cur.pop(k, None)
        _log_ctx.set(cur)
    else:
        _log_ctx.set({})


@contextmanager
def log_context(**kwargs: Any):
    """
    Temporarily set context within a block; restores original context on exit.

    This context manager allows you to temporarily add context variables that
    are automatically restored when the block exits, even if an exception occurs.

    Args:
        **kwargs: Key-value pairs to temporarily add to the logging context.

    Example:
        >>> log = get_logger(__name__)
        >>> with log_context(operation="cleanup"):
        ...     log.info("Starting")  # Includes operation=cleanup
        ...     perform_cleanup()
        >>> log.info("Done")  # operation context is removed

    Yields:
        None
    """
    token = _log_ctx.set({**(_log_ctx.get() or {}), **{k: str(v) for k, v in kwargs.items()}})
    try:
        yield
    finally:
        _log_ctx.reset(token)


class ContextFilter(logging.Filter):
    """
    Logging filter that injects context variables into log records.

    This filter reads the current context from the ContextVar and:
    1. Injects each context key as an attribute on the log record
    2. Creates a 'context' attribute with space-separated key=value pairs
    3. Creates a 'context_str' attribute formatted as " [key=value ...]"

    The filter is automatically applied by get_logger() and enables context
    variables to be used in log format strings.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Inject context variables into the log record.

        Args:
            record: The log record to modify.

        Returns:
            True (always passes the record through).
        """
        ctx = _log_ctx.get() or {}

        # Inject individual context keys as record attributes
        for k, v in ctx.items():
            if not hasattr(record, k):
                setattr(record, k, v)

        # Create formatted context strings
        if ctx:
            record.context = " ".join(f"{k}={ctx[k]}" for k in sorted(ctx.keys()))
            record.context_str = f" [{record.context}]"
        else:
            record.context = ""
            record.context_str = ""
        return True


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds ANSI colors to log levels for terminal output.

    Format: [timestamp] [level] [module.funcName:lineno] [context] message

    Colors:
        - DEBUG: Cyan
        - INFO: Green
        - WARNING: Yellow
        - ERROR: Red
        - CRITICAL: Magenta

    The source location and context are dimmed for better readability.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    DIM = "\033[2m"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors.

        Args:
            record: The log record to format.

        Returns:
            The formatted log message with ANSI color codes.
        """
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"

        # Format the main message
        formatted = super().format(record)

        # Reset levelname for future use
        record.levelname = levelname

        return formatted


# Preset format constants (available since v0.1.1)
DEFAULT_FORMAT = (
    f"[%(asctime)s] [%(levelname)s] "
    f"{ColoredFormatter.DIM}[%(module)s.%(funcName)s:%(lineno)d]{ColoredFormatter.RESET}"
    f"{ColoredFormatter.DIM}%(context_str)s{ColoredFormatter.RESET} "
    f"%(message)s"
)

MINIMAL_FORMAT = "%(levelname)s: %(message)s"

DETAILED_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(process)d] "
    "[%(module)s.%(funcName)s:%(lineno)d]%(context_str)s %(message)s"
)

SIMPLE_FORMAT = "[%(levelname)s]%(context_str)s %(message)s"

DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"


def get_logger(
    name: str,
    fmt: str | None = None,
    datefmt: str | None = None,
) -> logging.Logger:
    """
    Get a configured logger with context support and colored output.

    This is the main entry point for creating loggers in your application.
    The logger is pre-configured with:
    - Context filtering (ContextFilter)
    - Colored output (ColoredFormatter)
    - Environment-based log level (LOG_LEVEL env var, defaults to INFO)
    - Stdout output

    Args:
        name: The logger name, typically __name__ of the calling module.
        fmt: Optional log format string. Supports all standard logging format attributes.
             Defaults to DEFAULT_FORMAT (v0.1.0 compatible format).
             Use preset constants (MINIMAL_FORMAT, DETAILED_FORMAT, SIMPLE_FORMAT) or
             provide a custom format string.
        datefmt: Optional date format string for %(asctime)s.
                Defaults to DEFAULT_DATEFMT ("%Y-%m-%d %H:%M:%S").

    Returns:
        A configured logging.Logger instance.

    Examples:
        >>> # Default format (v0.1.0 compatible)
        >>> log = get_logger(__name__)
        >>> log.info("Application started")

        >>> # Using preset formats
        >>> log = get_logger(__name__, fmt=MINIMAL_FORMAT)
        >>> log.info("Simple message")  # Output: INFO: Simple message

        >>> # Custom format
        >>> log = get_logger(__name__, fmt="[%(levelname)s] %(message)s")
        >>> log.info("Custom output")

        >>> # With context
        >>> set_log_context(request_id="abc123")
        >>> log.info("Processing request")

    Environment Variables:
        LOG_LEVEL: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  Defaults to INFO if not set.

    Note:
        Version 0.1.0 had an opinionated, hardcoded format. Starting with v0.1.1,
        you can customize the format while maintaining full backward compatibility.
    """
    log = logging.getLogger(name)

    # Parse log level from env, default INFO
    level = os.environ.get("LOG_LEVEL", "INFO")
    log.setLevel(level)

    if not log.handlers:
        # Use provided format or fall back to default
        log_format = fmt or DEFAULT_FORMAT
        log_datefmt = datefmt or DEFAULT_DATEFMT

        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = ColoredFormatter(log_format, datefmt=log_datefmt)
        handler.setFormatter(formatter)
        handler.addFilter(ContextFilter())
        log.addHandler(handler)

    log.propagate = True
    return log
