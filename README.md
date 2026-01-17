# contexlog

[![PyPI version](https://badge.fury.io/py/contexlog.svg)](https://badge.fury.io/py/contexlog)
[![Python versions](https://img.shields.io/pypi/pyversions/contexlog.svg)](https://pypi.org/project/contexlog/)
[![Build Status](https://github.com/Aprova-GmbH/contextlog/workflows/Tests/badge.svg)](https://github.com/Aprova-GmbH/contextlog/actions)
[![Coverage](https://codecov.io/gh/Aprova-GmbH/contextlog/branch/main/graph/badge.svg)](https://codecov.io/gh/Aprova-GmbH/contextlog)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Minimalistic context-aware structured logging for Python. Add contextual information to your logs effortlessly with thread-safe and async-safe context management.

## Features

- **🎯 Context-Aware**: Automatically inject contextual information (user IDs, request IDs, etc.) into all log messages
- **🔒 Thread & Async Safe**: Built on Python's `contextvars` for perfect isolation across threads and async tasks
- **🎨 Colored Output**: Beautiful ANSI-colored terminal output for better readability
- **⚡ Zero Dependencies**: No runtime dependencies - just pure Python
- **📦 Minimal & Focused**: Does one thing well - context-aware logging
- **🔧 Zero Configuration**: Sensible defaults, works out of the box
- **💡 Type Hints**: Full type hint support for better IDE experience

## Installation

```bash
pip install contexlog
```

## Quick Start

```python
from contexlog import get_logger, set_log_context

# Create a logger
log = get_logger(__name__)

# Log without context
log.info("Application started")

# Set context - will be included in all subsequent logs
set_log_context(user_id="12345", request_id="abc-def")

log.info("Processing request")
# Output: [2024-01-17 10:30:45] [INFO] [main.<module>:10] [request_id=abc-def user_id=12345] Processing request

log.error("An error occurred")
# Output: [2024-01-17 10:30:46] [ERROR] [main.<module>:11] [request_id=abc-def user_id=12345] An error occurred
```

## Why contexlog?

When building applications, especially web services or async workers, you often need to track context across multiple operations:

- **Multi-tenant applications**: Track which tenant each log belongs to
- **Request tracing**: Follow a request's journey through your application
- **User tracking**: Know which user triggered each log event
- **Distributed systems**: Correlate logs across different parts of your system

contexlog makes this trivial while staying out of your way.

## Advanced Usage

### Temporary Context

Use the `log_context` context manager for temporary context that automatically cleans up:

```python
from contexlog import get_logger, log_context

log = get_logger(__name__)

with log_context(operation="cleanup", task_id="task-123"):
    log.info("Starting cleanup")  # Includes operation and task_id
    perform_cleanup()
# Context automatically removed after the block

log.info("Done")  # No operation/task_id context
```

### Async Context Isolation

Each async task gets its own isolated context - no cross-contamination:

```python
import asyncio
from contexlog import get_logger, set_log_context

log = get_logger(__name__)

async def handle_request(user_id: str, request_id: str):
    set_log_context(user_id=user_id, request_id=request_id)
    log.info("Processing request")  # Each task logs its own context
    await do_work()

# These run concurrently, each with isolated context
await asyncio.gather(
    handle_request("user1", "req001"),
    handle_request("user2", "req002"),
)
```

### Web Framework Integration

Perfect for web applications - set context per request:

```python
from fastapi import FastAPI, Request
from contexlog import get_logger, set_log_context, clear_log_context
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

    response = await call_next(request)

    # Clean up after request
    clear_log_context()
    return response
```

### Configuration

Control log level via the `LOG_LEVEL` environment variable:

```bash
export LOG_LEVEL=DEBUG
python your_app.py
```

Supported levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## Use Cases

- **Microservices**: Track requests across service boundaries
- **Multi-tenant SaaS**: Isolate logs by tenant
- **Async workers**: Track background job context
- **APIs**: Add request/user context to all endpoints
- **Data pipelines**: Track which dataset/batch is being processed

## Comparison with Alternatives

### vs. Standard logging

Standard library logging requires manual context passing or using filters on every logger. contexlog handles this automatically with proper async/thread safety.

### vs. structlog

structlog is feature-rich but heavier. contexlog is minimalistic (zero dependencies!) and focuses purely on context management with sensible defaults for common use cases.

## API Reference

### `get_logger(name: str) -> logging.Logger`

Create a configured logger with context support.

### `set_log_context(**kwargs) -> None`

Set context variables that will be included in all subsequent log messages.

### `clear_log_context(*keys: str) -> None`

Clear specific context keys, or all context if no keys provided.

### `log_context(**kwargs) -> ContextManager`

Context manager for temporary context that automatically cleans up.

## Documentation

Full documentation is available at [contexlog.readthedocs.io](https://contexlog.readthedocs.io)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Created by Andrey Vykhodtsev (Aprova GmbH)

Inspired by the need for simple, reliable context management in production Python applications.
