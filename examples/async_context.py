"""
Async context isolation example for contexlog.

This example demonstrates how contexlog maintains separate contexts for
concurrent async tasks, ensuring that context from one task doesn't leak
into another.
"""

import asyncio
from tinystructlog import get_logger, set_log_context, log_context

log = get_logger(__name__)

async def process_user_request(user_id: str, request_id: str):
    """
    Simulate processing a user request with its own context.

    Each concurrent call to this function maintains its own isolated context.
    """
    # Set context for this specific request
    set_log_context(user_id=user_id, request_id=request_id)

    log.info("Starting request processing")
    await asyncio.sleep(0.1)  # Simulate async work

    log.info("Fetching user data")
    await asyncio.sleep(0.1)

    log.info("Processing business logic")
    await asyncio.sleep(0.1)

    log.info("Request completed")

async def process_with_temp_context(task_id: str):
    """
    Demonstrate temporary context using the log_context context manager.

    The context set within the 'with' block is automatically cleaned up
    when the block exits.
    """
    log.info(f"Task {task_id} started (no context yet)")

    # Temporary context for a specific operation
    with log_context(operation="data_fetch", task_id=task_id):
        log.info("Fetching data with temporary context")
        await asyncio.sleep(0.1)
        log.info("Data fetch complete")

    # Context is automatically cleaned up here
    log.info(f"Task {task_id} completed (context removed)")

async def main():
    """Run multiple concurrent async tasks with isolated contexts."""
    log.info("=== Example 1: Concurrent requests with isolated contexts ===")

    # Run multiple requests concurrently - each maintains its own context
    await asyncio.gather(
        process_user_request("user1", "req001"),
        process_user_request("user2", "req002"),
        process_user_request("user3", "req003"),
    )

    log.info("\n=== Example 2: Temporary context with context manager ===")

    # Run tasks with temporary contexts
    await asyncio.gather(
        process_with_temp_context("task1"),
        process_with_temp_context("task2"),
    )

if __name__ == "__main__":
    asyncio.run(main())
