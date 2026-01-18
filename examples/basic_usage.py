"""
Basic usage example for contexlog.

This example demonstrates the fundamental features of contexlog including
setting context, logging with context, and clearing context.
"""

from tinystructlog import get_logger, set_log_context, clear_log_context

# Create a logger for this module
log = get_logger(__name__)

def main():
    """Demonstrate basic contexlog usage."""
    # Basic logging without context
    log.info("Application starting")

    # Set context that will be included in all subsequent log messages
    set_log_context(user_id="user123", session_id="session456")
    log.info("User logged in")

    # Context persists across log calls
    log.debug("Processing user request")
    log.info("Request completed successfully")

    # Add more context (merges with existing)
    set_log_context(action="purchase", item_id="item789")
    log.info("User initiated action")

    # Clear specific context keys
    clear_log_context("action", "item_id")
    log.info("Action completed, context cleaned up")

    # Clear all context
    clear_log_context()
    log.info("All context cleared")

if __name__ == "__main__":
    main()
