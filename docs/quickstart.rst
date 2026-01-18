Quick Start Guide
=================

Installation
------------

Install ``tinystructlog`` using pip:

.. code-block:: bash

    pip install tinystructlog

Requirements: Python 3.11 or higher.

Basic Usage
-----------

The simplest way to get started:

.. code-block:: python

    from tinystructlog import get_logger, set_log_context

    # Create a logger
    log = get_logger(__name__)

    # Log without context
    log.info("Application started")

    # Set context that will be included in all subsequent logs
    set_log_context(user_id="12345", request_id="abc-def")

    log.info("Processing request")
    log.error("An error occurred")

Output will look like:

.. code-block:: text

    [2024-01-17 10:30:45] [INFO] [__main__:5] Application started
    [2024-01-17 10:30:46] [INFO] [__main__:10] [request_id=abc-def user_id=12345] Processing request
    [2024-01-17 10:30:47] [ERROR] [__main__:11] [request_id=abc-def user_id=12345] An error occurred

Setting Context
---------------

Use ``set_log_context()`` to add or update context variables:

.. code-block:: python

    from tinystructlog import set_log_context, get_logger

    log = get_logger(__name__)

    # Set initial context
    set_log_context(user_id="user123")
    log.info("User logged in")

    # Add more context (merges with existing)
    set_log_context(session_id="sess456")
    log.info("Session created")  # Will have both user_id and session_id

    # Override existing values
    set_log_context(user_id="user789")
    log.info("Context updated")  # user_id is now user789

Clearing Context
----------------

Remove specific keys or clear all context:

.. code-block:: python

    from tinystructlog import clear_log_context, set_log_context, get_logger

    log = get_logger(__name__)

    set_log_context(user_id="123", session_id="abc")
    log.info("With full context")

    # Clear specific keys
    clear_log_context("session_id")
    log.info("Session cleared")  # Only has user_id

    # Clear all context
    clear_log_context()
    log.info("All context cleared")  # No context

Temporary Context
-----------------

Use the ``log_context`` context manager for temporary context:

.. code-block:: python

    from tinystructlog import log_context, get_logger

    log = get_logger(__name__)

    with log_context(operation="cleanup", task_id="task-123"):
        log.info("Starting cleanup")  # Includes operation and task_id
        perform_cleanup()
        log.info("Cleanup completed")
    # Context automatically removed after the block

    log.info("Back to normal")  # No operation/task_id

Async Usage
-----------

``tinystructlog`` is fully async-safe with automatic context isolation:

.. code-block:: python

    import asyncio
    from tinystructlog import get_logger, set_log_context

    log = get_logger(__name__)

    async def handle_request(user_id: str, request_id: str):
        # Each task gets isolated context
        set_log_context(user_id=user_id, request_id=request_id)
        log.info("Processing request")
        await asyncio.sleep(1)
        log.info("Request completed")

    # Run multiple tasks concurrently - contexts won't interfere
    async def main():
        await asyncio.gather(
            handle_request("user1", "req001"),
            handle_request("user2", "req002"),
            handle_request("user3", "req003"),
        )

    asyncio.run(main())

Web Framework Integration
--------------------------

Example with FastAPI:

.. code-block:: python

    from fastapi import FastAPI, Request
    from tinystructlog import get_logger, set_log_context, clear_log_context
    import uuid

    app = FastAPI()
    log = get_logger(__name__)

    @app.middleware("http")
    async def add_context(request: Request, call_next):
        # Add request context
        set_log_context(
            request_id=str(uuid.uuid4()),
            path=request.url.path,
            method=request.method,
        )

        log.info("Request started")
        response = await call_next(request)
        log.info("Request completed", extra={"status": response.status_code})

        # Clean up after request
        clear_log_context()
        return response

    @app.get("/")
    async def root():
        log.info("Handling root endpoint")
        return {"message": "Hello World"}

Example with Flask:

.. code-block:: python

    from flask import Flask, request, g
    from tinystructlog import get_logger, set_log_context, clear_log_context
    import uuid

    app = Flask(__name__)
    log = get_logger(__name__)

    @app.before_request
    def before_request():
        set_log_context(
            request_id=str(uuid.uuid4()),
            path=request.path,
            method=request.method,
        )
        log.info("Request started")

    @app.after_request
    def after_request(response):
        log.info("Request completed", extra={"status": response.status_code})
        clear_log_context()
        return response

    @app.route("/")
    def home():
        log.info("Handling home page")
        return "Hello, World!"

Configuration
-------------

Log Level
~~~~~~~~~

Control the log level using the ``LOG_LEVEL`` environment variable:

.. code-block:: bash

    export LOG_LEVEL=DEBUG
    python your_app.py

Supported levels: ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``

Default is ``INFO``.

Colored Output
~~~~~~~~~~~~~~

Colored output is enabled by default when logging to a terminal. Colors are automatically disabled when output is redirected to a file or pipe.

Custom Log Formats (v0.1.1+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While tinystructlog comes with sensible defaults, you can customize the output format.

**Using Preset Formats:**

.. code-block:: python

    from tinystructlog import get_logger, MINIMAL_FORMAT, DETAILED_FORMAT, SIMPLE_FORMAT

    # Minimal format - just level and message
    log = get_logger(__name__, fmt=MINIMAL_FORMAT)
    log.info("Clean output")
    # Output: INFO: Clean output

    # Detailed format - includes process ID
    log = get_logger(__name__, fmt=DETAILED_FORMAT)
    log.info("Detailed output")
    # Output: [2026-01-18 10:30:45] [INFO] [12345] [module.function:10] Message

    # Simple format - level and context only
    log = get_logger(__name__, fmt=SIMPLE_FORMAT)
    log.info("Simple output")
    # Output: [INFO] Message

**Custom Format Strings:**

.. code-block:: python

    from tinystructlog import get_logger

    # Fully custom format
    log = get_logger(__name__, fmt="%(levelname)s | %(message)s")
    log.info("Custom")
    # Output: INFO | Custom

    # Custom with timestamp
    log = get_logger(__name__,
        fmt="[%(asctime)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    log.info("Time only")
    # Output: [10:30:45] Time only

**Available Format Variables:**

Standard Python logging attributes:

* ``%(asctime)s`` - Timestamp (customize with ``datefmt``)
* ``%(levelname)s`` - Log level (DEBUG, INFO, etc.)
* ``%(module)s`` - Module name
* ``%(funcName)s`` - Function name
* ``%(lineno)d`` - Line number
* ``%(message)s`` - Log message
* ``%(process)d`` - Process ID

tinystructlog-specific attributes:

* ``%(context)s`` - Raw context string (e.g., "key1=val1 key2=val2")
* ``%(context_str)s`` - Bracketed context (e.g., " [key1=val1 key2=val2]")
* Individual context keys as attributes

.. note::
   **Backward Compatibility:** Version 0.1.0 had an opinionated, hardcoded format. Starting with v0.1.1, you can customize it while maintaining full backward compatibility. The default format (when no ``fmt`` parameter is provided) remains identical to v0.1.0.

Next Steps
----------

* Check out the :doc:`api` for detailed API reference
* See :doc:`examples` for more advanced usage patterns
