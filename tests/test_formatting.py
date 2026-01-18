"""Tests for log formatters and filters."""

import logging

from tinystructlog import clear_log_context, set_log_context
from tinystructlog.core import ColoredFormatter, ContextFilter


class TestContextFilter:
    """Tests for ContextFilter class."""

    def test_filter_injects_context_attributes(self):
        """Test that ContextFilter injects context as record attributes."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        context_filter.filter(record)

        assert hasattr(record, "user_id")
        assert hasattr(record, "request_id")
        assert record.user_id == "123"
        assert record.request_id == "abc"

    def test_filter_creates_context_string(self):
        """Test that ContextFilter creates formatted context string."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        context_filter.filter(record)

        assert hasattr(record, "context")
        assert hasattr(record, "context_str")
        # Keys are sorted alphabetically
        assert record.context == "request_id=abc user_id=123"
        assert record.context_str == " [request_id=abc user_id=123]"

    def test_filter_empty_context(self):
        """Test that ContextFilter handles empty context correctly."""
        clear_log_context()

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        context_filter.filter(record)

        assert record.context == ""
        assert record.context_str == ""

    def test_filter_returns_true(self):
        """Test that ContextFilter always returns True (passes record through)."""
        clear_log_context()

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        result = context_filter.filter(record)
        assert result is True

    def test_filter_sorted_keys(self):
        """Test that context keys are sorted alphabetically."""
        clear_log_context()
        set_log_context(zebra="z", alpha="a", middle="m")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        context_filter.filter(record)

        assert record.context == "alpha=a middle=m zebra=z"


class TestColoredFormatter:
    """Tests for ColoredFormatter class."""

    def test_formatter_adds_colors_to_debug(self):
        """Test that ColoredFormatter adds cyan color to DEBUG level."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="test.py",
            lineno=10,
            msg="Debug message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert "\033[36m" in formatted  # Cyan color code
        assert "DEBUG" in formatted
        assert "\033[0m" in formatted  # Reset code

    def test_formatter_adds_colors_to_info(self):
        """Test that ColoredFormatter adds green color to INFO level."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Info message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert "\033[32m" in formatted  # Green color code
        assert "INFO" in formatted

    def test_formatter_adds_colors_to_warning(self):
        """Test that ColoredFormatter adds yellow color to WARNING level."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=10,
            msg="Warning message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert "\033[33m" in formatted  # Yellow color code
        assert "WARNING" in formatted

    def test_formatter_adds_colors_to_error(self):
        """Test that ColoredFormatter adds red color to ERROR level."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert "\033[31m" in formatted  # Red color code
        assert "ERROR" in formatted

    def test_formatter_adds_colors_to_critical(self):
        """Test that ColoredFormatter adds magenta color to CRITICAL level."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.CRITICAL,
            pathname="test.py",
            lineno=10,
            msg="Critical message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert "\033[35m" in formatted  # Magenta color code
        assert "CRITICAL" in formatted

    def test_formatter_restores_levelname(self):
        """Test that ColoredFormatter restores original levelname after formatting."""
        formatter = ColoredFormatter("[%(levelname)s] %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        original_levelname = record.levelname
        formatter.format(record)

        # Levelname should be restored to original
        assert record.levelname == original_levelname

    def test_formatter_with_context(self):
        """Test that ColoredFormatter works with context attributes."""
        clear_log_context()
        set_log_context(user_id="123")

        # Apply context filter first
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        context_filter = ContextFilter()
        context_filter.filter(record)

        # Then format with ColoredFormatter
        formatter = ColoredFormatter("[%(levelname)s]%(context_str)s %(message)s")
        formatted = formatter.format(record)

        assert "user_id=123" in formatted
        assert "Test message" in formatted

    def test_formatter_timestamp(self):
        """Test that ColoredFormatter includes timestamp when configured."""
        formatter = ColoredFormatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        # Should contain timestamp in YYYY-MM-DD HH:MM:SS format
        import re

        assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", formatted)

    def test_context_filter_default_behavior_v010_compatible(self):
        """Test that default ContextFilter produces exact v0.1.0 output (backward compatibility)."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Create ContextFilter with default parameters (no arguments)
        context_filter = ContextFilter()
        context_filter.filter(record)

        # Verify exact v0.1.0 behavior
        # Keys are alphabetically sorted
        assert record.context == "request_id=abc user_id=123"
        # Bracketed with leading space
        assert record.context_str == " [request_id=abc user_id=123]"
        # Individual attributes injected
        assert record.user_id == "123"
        assert record.request_id == "abc"
