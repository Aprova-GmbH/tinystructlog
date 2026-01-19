Comparison with Other Libraries
================================

This page compares tinystructlog with other popular Python logging libraries to help you choose the right tool for your needs.

vs. loguru
----------

`loguru <https://github.com/Delgan/loguru>`_ is a popular alternative to Python's standard logging with a focus on simplicity and developer experience.

**When to choose tinystructlog:**

* **Zero dependencies**: tinystructlog has no runtime dependencies, making it ideal for environments where you want to minimize dependencies
* **Simpler mental model**: Single, focused API for context management using Python's ``contextvars``
* **Minimal footprint**: Smaller codebase focused purely on context-aware logging
* **Standard logging integration**: Works with Python's standard logging, making it easier to integrate with existing logging infrastructure

**When to choose loguru:**

* **Rich features**: Built-in rotation, retention, compression, serialization
* **Advanced error handling**: Enhanced exception formatting with ``backtrace`` and ``diagnose``
* **More flexible output**: Multiple sinks, custom handlers, structured JSON logging
* **Broader ecosystem**: More third-party integrations and community resources

**Reproducing tinystructlog's format in loguru:**

.. code-block:: python

    from loguru import logger
    import sys

    # Remove default handler
    logger.remove()

    # Add handler with tinystructlog-like format
    logger.add(
        sys.stdout,
        format="[{time:YYYY-MM-DD HH:MM:SS}] [{level}] [{name}.{function}:{line}] {extra} {message}",
        colorize=True
    )

    # Context binding in loguru
    context_logger = logger.bind(request_id="abc-def", user_id="12345")
    context_logger.info("Processing request")

**Key differences:**

* **Context management**: tinystructlog uses ``contextvars`` for automatic thread/async isolation; loguru requires explicit binding via ``bind()`` or ``contextualize()``
* **Dependencies**: tinystructlog has zero dependencies; loguru includes additional libraries for enhanced features
* **Configuration**: tinystructlog is pre-configured with sensible defaults; loguru requires removing default handlers and adding custom ones
* **API surface**: tinystructlog has 4 main functions; loguru has a larger API with many configuration options

vs. structlog
-------------

`structlog <https://www.structlog.org/>`_ is a feature-rich structured logging library with extensive customization options.

**When to choose tinystructlog:**

* **Simplicity**: Much smaller API surface and simpler mental model
* **Zero dependencies**: No external dependencies
* **Immediate productivity**: Works out of the box with sensible defaults
* **Lighter weight**: Minimal overhead for simple use cases

**When to choose structlog:**

* **Advanced structured logging**: Rich processors, formatters, and output options
* **Complex pipelines**: Need for sophisticated log processing chains
* **Extensive customization**: Highly configurable for specific requirements
* **Industry standard**: Well-established in production environments

vs. Standard logging
--------------------

Python's built-in ``logging`` module is the foundation of Python logging.

**When to choose tinystructlog:**

* **Context management**: Automatic context injection without manual filter setup
* **Async/thread safety**: Built on ``contextvars`` for proper isolation
* **Developer experience**: Colored output and sensible defaults out of the box
* **Less boilerplate**: No need to configure handlers, formatters, and filters manually

**When to choose standard logging:**

* **No dependencies**: Part of the standard library
* **Maximum control**: Full customization of every aspect
* **Ecosystem compatibility**: Works with all logging-compatible libraries
* **Long-term stability**: Part of Python's core

**Note:** tinystructlog is built on top of standard logging, so you get compatibility with the standard logging ecosystem while gaining the convenience of automatic context management.

Summary Table
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Feature
     - tinystructlog
     - loguru
     - structlog
     - standard logging
   * - Dependencies
     - Zero
     - Yes
     - Yes
     - Zero (stdlib)
   * - Context Management
     - Auto (contextvars)
     - Manual (bind)
     - Processors
     - Manual (filters)
   * - Configuration
     - Zero config
     - Custom setup
     - Extensive
     - Manual setup
   * - Async/Thread Safety
     - Built-in
     - Built-in
     - Built-in
     - Manual
   * - API Complexity
     - Minimal (4 functions)
     - Medium
     - High
     - High
   * - Colored Output
     - Yes (ANSI)
     - Yes
     - Yes (via processors)
     - No (manual)
   * - JSON/Structured
     - Context only
     - Full support
     - Full support
     - Limited
