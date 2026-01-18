"""Tests for context management functionality."""

import asyncio

import pytest

from tinystructlog import clear_log_context, log_context, set_log_context
from tinystructlog.core import _log_ctx


class TestSetLogContext:
    """Tests for set_log_context function."""

    def test_set_single_value(self):
        """Test setting a single context value."""
        clear_log_context()  # Start fresh
        set_log_context(user_id="123")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123"}

    def test_set_multiple_values(self):
        """Test setting multiple context values at once."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc", tenant="acme")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123", "request_id": "abc", "tenant": "acme"}

    def test_merge_values(self):
        """Test that calling set_log_context merges with existing context."""
        clear_log_context()
        set_log_context(user_id="123")
        set_log_context(request_id="abc")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123", "request_id": "abc"}

    def test_override_values(self):
        """Test that calling set_log_context overrides existing values."""
        clear_log_context()
        set_log_context(user_id="123")
        set_log_context(user_id="456")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "456"}

    def test_converts_values_to_strings(self):
        """Test that values are converted to strings."""
        clear_log_context()
        set_log_context(user_id=123, count=456, flag=True)
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123", "count": "456", "flag": "True"}


class TestClearLogContext:
    """Tests for clear_log_context function."""

    def test_clear_all(self):
        """Test clearing all context."""
        set_log_context(user_id="123", request_id="abc")
        clear_log_context()
        ctx = _log_ctx.get()
        assert ctx == {}

    def test_clear_specific_key(self):
        """Test clearing a specific context key."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc", tenant="acme")
        clear_log_context("request_id")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123", "tenant": "acme"}

    def test_clear_multiple_keys(self):
        """Test clearing multiple specific keys."""
        clear_log_context()
        set_log_context(user_id="123", request_id="abc", tenant="acme", session="xyz")
        clear_log_context("request_id", "session")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123", "tenant": "acme"}

    def test_clear_nonexistent_key(self):
        """Test clearing a key that doesn't exist (should not error)."""
        clear_log_context()
        set_log_context(user_id="123")
        clear_log_context("nonexistent")
        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123"}


class TestLogContext:
    """Tests for log_context context manager."""

    def test_temporary_context(self):
        """Test that context is temporary within the block."""
        clear_log_context()
        set_log_context(user_id="123")

        with log_context(request_id="abc"):
            ctx = _log_ctx.get()
            assert ctx == {"user_id": "123", "request_id": "abc"}

        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123"}

    def test_restores_context_after_exception(self):
        """Test that context is restored even if exception occurs."""
        clear_log_context()
        set_log_context(user_id="123")

        try:
            with log_context(request_id="abc"):
                ctx = _log_ctx.get()
                assert ctx == {"user_id": "123", "request_id": "abc"}
                raise ValueError("Test error")
        except ValueError:
            pass

        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123"}

    def test_nested_context_managers(self):
        """Test that nested context managers work correctly."""
        clear_log_context()
        set_log_context(user_id="123")

        with log_context(request_id="abc"):
            ctx = _log_ctx.get()
            assert ctx == {"user_id": "123", "request_id": "abc"}

            with log_context(operation="delete"):
                ctx = _log_ctx.get()
                assert ctx == {"user_id": "123", "request_id": "abc", "operation": "delete"}

            ctx = _log_ctx.get()
            assert ctx == {"user_id": "123", "request_id": "abc"}

        ctx = _log_ctx.get()
        assert ctx == {"user_id": "123"}


class TestAsyncContextIsolation:
    """Tests for context isolation in async tasks."""

    @pytest.mark.asyncio
    async def test_async_task_isolation(self):
        """Test that context is isolated between async tasks."""
        clear_log_context()
        results = []

        async def task_with_context(task_id: str):
            set_log_context(task_id=task_id)
            await asyncio.sleep(0.01)  # Simulate async work
            ctx = _log_ctx.get()
            results.append(ctx.get("task_id"))

        # Run multiple tasks concurrently
        await asyncio.gather(
            task_with_context("task1"),
            task_with_context("task2"),
            task_with_context("task3"),
        )

        # Each task should have its own context
        assert set(results) == {"task1", "task2", "task3"}

    @pytest.mark.asyncio
    async def test_async_context_manager_isolation(self):
        """Test that log_context works correctly in async contexts."""
        clear_log_context()

        async def async_operation(op_id: str):
            with log_context(operation=op_id):
                await asyncio.sleep(0.01)
                ctx = _log_ctx.get()
                return ctx.get("operation")

        results = await asyncio.gather(
            async_operation("op1"),
            async_operation("op2"),
            async_operation("op3"),
        )

        assert set(results) == {"op1", "op2", "op3"}

        # Original context should be empty after all tasks complete
        ctx = _log_ctx.get()
        assert ctx == {}
