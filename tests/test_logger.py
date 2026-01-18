"""Tests for logger creation and configuration."""

import logging
import os
import re

from tinystructlog import clear_log_context, get_logger, set_log_context
from tinystructlog.core import ColoredFormatter, ContextFilter


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_logger_instance(self):
        """Test that get_logger returns a logging.Logger instance."""
        log = get_logger("test")
        assert isinstance(log, logging.Logger)

    def test_logger_name(self):
        """Test that logger has the correct name."""
        log = get_logger("my.module")
        assert log.name == "my.module"

    def test_logger_has_handler(self):
        """Test that logger is configured with a handler."""
        log = get_logger("test.handler")
        assert len(log.handlers) > 0

    def test_logger_has_context_filter(self):
        """Test that logger has ContextFilter applied."""
        log = get_logger("test.filter")
        handler = log.handlers[0]
        filters = handler.filters
        assert any(isinstance(f, ContextFilter) for f in filters)

    def test_logger_has_colored_formatter(self):
        """Test that logger uses ColoredFormatter."""
        log = get_logger("test.formatter")
        handler = log.handlers[0]
        assert isinstance(handler.formatter, ColoredFormatter)

    def test_logger_no_duplicate_handlers(self):
        """Test that calling get_logger multiple times doesn't add duplicate handlers."""
        log1 = get_logger("test.duplicate")
        handler_count1 = len(log1.handlers)

        log2 = get_logger("test.duplicate")
        handler_count2 = len(log2.handlers)

        assert handler_count1 == handler_count2

    def test_logger_propagates(self):
        """Test that logger propagates is set to True."""
        log = get_logger("test.propagate")
        assert log.propagate is True


class TestLogLevelConfiguration:
    """Tests for LOG_LEVEL environment variable configuration."""

    def test_default_log_level(self):
        """Test that default log level is INFO when LOG_LEVEL not set."""
        # Save original value
        original = os.environ.get("LOG_LEVEL")
        if "LOG_LEVEL" in os.environ:
            del os.environ["LOG_LEVEL"]

        log = get_logger("test.default_level")
        assert log.level == logging.INFO

        # Restore original value
        if original:
            os.environ["LOG_LEVEL"] = original

    def test_custom_log_level_debug(self):
        """Test that LOG_LEVEL=DEBUG sets log level to DEBUG."""
        original = os.environ.get("LOG_LEVEL")
        os.environ["LOG_LEVEL"] = "DEBUG"

        log = get_logger("test.debug_level")
        assert log.level == logging.DEBUG

        # Restore original value
        if original:
            os.environ["LOG_LEVEL"] = original
        else:
            del os.environ["LOG_LEVEL"]

    def test_custom_log_level_warning(self):
        """Test that LOG_LEVEL=WARNING sets log level to WARNING."""
        original = os.environ.get("LOG_LEVEL")
        os.environ["LOG_LEVEL"] = "WARNING"

        log = get_logger("test.warning_level")
        assert log.level == logging.WARNING

        # Restore original value
        if original:
            os.environ["LOG_LEVEL"] = original
        else:
            del os.environ["LOG_LEVEL"]


class TestLoggingWithContext:
    """Tests for logging with context integration."""

    def test_log_includes_context(self, caplog):
        """Test that log records include context information."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc")

        log = get_logger("test.with_context")
        with caplog.at_level(logging.INFO):
            log.info("Test message")

        # Check that the log record was created
        assert len(caplog.records) == 1
        record = caplog.records[0]

        # Check that context attributes are present
        assert hasattr(record, "user_id")
        assert hasattr(record, "request_id")
        assert record.user_id == "123"
        assert record.request_id == "abc"

        # Check formatted context strings
        assert hasattr(record, "context")
        assert hasattr(record, "context_str")
        assert "user_id=123" in record.context
        assert "request_id=abc" in record.context

    def test_log_without_context(self, caplog):
        """Test that logging works without any context set."""
        clear_log_context()

        log = get_logger("test.no_context")
        with caplog.at_level(logging.INFO):
            log.info("Test message")

        assert len(caplog.records) == 1
        record = caplog.records[0]

        # Context attributes should be empty strings
        assert record.context == ""
        assert record.context_str == ""

    def test_different_log_levels(self, caplog):
        """Test that different log levels work correctly."""
        clear_log_context()
        log = get_logger("test.levels")

        # Set logger level to DEBUG to capture all messages
        log.setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG):
            log.debug("Debug message")
            log.info("Info message")
            log.warning("Warning message")
            log.error("Error message")
            log.critical("Critical message")

        assert len(caplog.records) == 5
        assert caplog.records[0].levelname == "DEBUG"
        assert caplog.records[1].levelname == "INFO"
        assert caplog.records[2].levelname == "WARNING"
        assert caplog.records[3].levelname == "ERROR"
        assert caplog.records[4].levelname == "CRITICAL"


class TestCustomFormats:
    """Tests for custom format support (v0.1.1+)."""

    def test_custom_format_parameter(self, capsys):
        """Test that get_logger respects custom fmt parameter."""
        from tinystructlog import get_logger

        log = get_logger("test.custom_fmt_v2", fmt="%(levelname)s: %(message)s")
        log.info("Test message")

        captured = capsys.readouterr()
        # Check the actual stdout output (with ANSI codes)
        assert "INFO" in captured.out
        assert "Test message" in captured.out
        # Verify it uses custom format (minimal, no timestamp)
        # The custom format should not contain brackets with dates
        assert (
            "[2024" not in captured.out
            and "[2025" not in captured.out
            and "[2026" not in captured.out
        )

    def test_custom_datefmt_parameter(self, capsys):
        """Test that get_logger respects custom datefmt parameter."""
        from tinystructlog import get_logger

        log = get_logger(
            "test.custom_datefmt_v2", fmt="[%(asctime)s] %(message)s", datefmt="%H:%M:%S"
        )
        log.info("Test message")

        captured = capsys.readouterr()
        # Should contain time in HH:MM:SS format (no date)
        assert re.search(r"\[\d{2}:\d{2}:\d{2}\]", captured.out)
        # Should not contain full date
        assert not re.search(r"\d{4}-\d{2}-\d{2}", captured.out)

    def test_default_format_unchanged(self, capsys):
        """Test that default behavior matches v0.1.0 (backward compatibility)."""
        from tinystructlog import clear_log_context, get_logger, set_log_context

        clear_log_context()
        set_log_context(user_id="123")

        # Call without any format parameters (default behavior)
        log = get_logger("test.default_unchanged_v2")
        log.info("Test message")

        captured = capsys.readouterr()
        # Should contain all default format elements
        assert "INFO" in captured.out
        assert "test_logger" in captured.out
        assert "user_id=123" in captured.out
        assert "Test message" in captured.out

    def test_minimal_format_preset(self, capsys):
        """Test that MINIMAL_FORMAT preset works correctly."""
        from tinystructlog import MINIMAL_FORMAT, get_logger

        log = get_logger("test.minimal_v2", fmt=MINIMAL_FORMAT)
        log.info("Simple message")

        captured = capsys.readouterr()
        # The minimal format should produce "INFO: Simple message"
        # (with ANSI color codes for INFO)
        assert "INFO" in captured.out
        assert "Simple message" in captured.out
        assert ":" in captured.out

    def test_detailed_format_preset(self, capsys):
        """Test that DETAILED_FORMAT preset works correctly."""
        from tinystructlog import DETAILED_FORMAT, clear_log_context, get_logger, set_log_context

        clear_log_context()
        set_log_context(test_key="test_value")

        log = get_logger("test.detailed_v2", fmt=DETAILED_FORMAT)
        log.info("Detailed message")

        captured = capsys.readouterr()
        # Should contain process ID
        assert re.search(r"\[\d+\]", captured.out)
        # Should contain context
        assert "test_key=test_value" in captured.out
        # Should contain message
        assert "Detailed message" in captured.out

    def test_simple_format_preset(self, capsys):
        """Test that SIMPLE_FORMAT preset works correctly."""
        from tinystructlog import SIMPLE_FORMAT, clear_log_context, get_logger, set_log_context

        clear_log_context()
        set_log_context(key="value")

        log = get_logger("test.simple_v2", fmt=SIMPLE_FORMAT)
        log.info("Simple")

        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "key=value" in captured.out
        assert "Simple" in captured.out

    def test_format_constants_exported(self):
        """Test that format constants are properly exported."""
        from tinystructlog import (
            DEFAULT_DATEFMT,
            DEFAULT_FORMAT,
            DETAILED_FORMAT,
            MINIMAL_FORMAT,
            SIMPLE_FORMAT,
        )

        # Verify they are strings
        assert isinstance(DEFAULT_FORMAT, str)
        assert isinstance(MINIMAL_FORMAT, str)
        assert isinstance(DETAILED_FORMAT, str)
        assert isinstance(SIMPLE_FORMAT, str)
        assert isinstance(DEFAULT_DATEFMT, str)

        # Verify MINIMAL_FORMAT is actually minimal
        assert MINIMAL_FORMAT == "%(levelname)s: %(message)s"

        # Verify DEFAULT_DATEFMT is correct
        assert DEFAULT_DATEFMT == "%Y-%m-%d %H:%M:%S"
