"""Tests for logger creation and configuration."""

import logging
import os

from contexlog import clear_log_context, get_logger, set_log_context
from contexlog.core import ColoredFormatter, ContextFilter


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
