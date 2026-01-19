tinystructlog - Context-Aware Logging
======================================

Welcome to **tinystructlog**, a minimalistic context-aware structured logging library for Python.

Overview
--------

``tinystructlog`` makes it effortless to add contextual information to your logs. Perfect for multi-tenant applications, microservices, async workers, and any application where you need to track request IDs, user IDs, or other contextual data across your application.

Key Features
------------

* 🎯 **Context-Aware**: Automatically inject contextual information into all log messages
* 🔒 **Thread & Async Safe**: Built on Python's ``contextvars`` for perfect isolation
* 🎨 **Colored Output**: Beautiful ANSI-colored terminal output for better readability
* ⚡ **Zero Dependencies**: No runtime dependencies - just pure Python
* 📦 **Minimal & Focused**: Does one thing well - context-aware logging
* 🔧 **Zero Configuration**: Sensible defaults, works out of the box
* 💡 **Type Hints**: Full type hint support for better IDE experience

Quick Example
-------------

.. code-block:: python

    from tinystructlog import get_logger, set_log_context

    log = get_logger(__name__)

    # Log without context
    log.info("Application started")

    # Set context - will be included in all subsequent logs
    set_log_context(user_id="12345", request_id="abc-def")

    log.info("Processing request")
    # Output: [2024-01-17 10:30:45] [INFO] [main:10] [request_id=abc-def user_id=12345] Processing request

Installation
------------

Install via pip:

.. code-block:: bash

    pip install tinystructlog

Python 3.11+ is required.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   examples
   comparison

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
