# tinystructlog

[![PyPI version](https://badge.fury.io/py/tinystructlog.svg)](https://badge.fury.io/py/tinystructlog)
[![Python versions](https://img.shields.io/pypi/pyversions/tinystructlog.svg)](https://pypi.org/project/tinystructlog/)
[![Build Status](https://github.com/Aprova-GmbH/tinystructlog/workflows/Tests/badge.svg)](https://github.com/Aprova-GmbH/tinystructlog/actions)
[![Coverage](https://codecov.io/gh/Aprova-GmbH/tinystructlog/branch/main/graph/badge.svg)](https://codecov.io/gh/Aprova-GmbH/tinystructlog)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Minimalistic context-aware structured logging for Python. Add contextual information to your logs effortlessly with thread-safe and async-safe context management.

## Features

- **🎯 Context-Aware**: Automatically inject contextual information (user IDs, request IDs, etc.) into all log messages
- **🔒 Thread & Async Safe**: Built on Python's `contextvars` for perfect isolation across threads and async tasks
- **🎨 Colored Output**: Beautiful ANSI-colored terminal output for better readability
- **🎛️ Flexible Formats**: Customizable output with sensible defaults and preset formats (v0.1.1+)
- **⚡ Zero Dependencies**: No runtime dependencies - just pure Python
- **📦 Minimal & Focused**: Does one thing well - context-aware logging
- **🔧 Zero Configuration**: Sensible defaults, works out of the box
- **💡 Type Hints**: Full type hint support for better IDE experience

## Installation

```bash
pip install tinystructlog
```

## Quick Start

```python
from tinystructlog import get_logger, set_log_context

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

## Why tinystructlog?

When building applications, especially web services or async workers, you often need to track context across multiple operations:

- **Multi-tenant applications**: Track which tenant each log belongs to
- **Request tracing**: Follow a request's journey through your application
- **User tracking**: Know which user triggered each log event
- **Distributed systems**: Correlate logs across different parts of your system

tinystructlog makes this trivial while staying out of your way.

## Advanced Usage

### Temporary Context

Use the `log_context` context manager for temporary context that automatically cleans up:

```python
from tinystructlog import get_logger, log_context

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
from tinystructlog import get_logger, set_log_context

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

### Custom Log Formats (v0.1.1+)

While tinystructlog comes with sensible defaults, you can customize the output format to match your needs:

#### Using Preset Formats

```python
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
```

#### Custom Format Strings

```python
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
```

#### Available Format Variables

Standard Python logging attributes:
- `%(asctime)s` - Timestamp (customize with `datefmt`)
- `%(levelname)s` - Log level (DEBUG, INFO, etc.)
- `%(module)s` - Module name
- `%(funcName)s` - Function name
- `%(lineno)d` - Line number
- `%(message)s` - Log message
- `%(process)d` - Process ID

tinystructlog-specific attributes:
- `%(context)s` - Raw context string (e.g., "key1=val1 key2=val2")
- `%(context_str)s` - Bracketed context (e.g., " [key1=val1 key2=val2]")
- Individual context keys as attributes

**Note:** Version 0.1.0 had an opinionated, hardcoded format. Starting with v0.1.1, you can customize it while maintaining full backward compatibility. The default format (when no `fmt` parameter is provided) remains identical to v0.1.0.

## Use Cases

- **Microservices**: Track requests across service boundaries
- **Multi-tenant SaaS**: Isolate logs by tenant
- **Async workers**: Track background job context
- **APIs**: Add request/user context to all endpoints
- **Data pipelines**: Track which dataset/batch is being processed

## Comparison with Alternatives

### vs. loguru

[loguru](https://github.com/Delgan/loguru) is popular for its simplicity and rich features. Key differences:

- **Dependencies**: tinystructlog has zero dependencies; loguru includes additional libraries
- **Context**: tinystructlog uses `contextvars` for automatic thread/async isolation; loguru requires explicit `bind()` calls
- **Focus**: tinystructlog focuses purely on context management; loguru provides rotation, retention, compression, and more
- **Integration**: tinystructlog works with standard logging infrastructure; loguru replaces it

Choose tinystructlog for minimal footprint and automatic context propagation. Choose loguru for rich features and advanced error handling.

See the [full comparison](https://tinystructlog.readthedocs.io/en/latest/comparison.html) for details on reproducing tinystructlog's format in loguru.

### vs. Standard logging

Standard library logging requires manual context passing or using filters on every logger. tinystructlog handles this automatically with proper async/thread safety.

### vs. structlog

structlog is feature-rich but heavier. tinystructlog is minimalistic (zero dependencies!) and focuses purely on context management with sensible defaults for common use cases.

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

Full documentation is available at [tinystructlog.readthedocs.io](https://tinystructlog.readthedocs.io)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Created by Andrey Vykhodtsev (Aprova GmbH)

Inspired by the need for simple, reliable context management in production Python applications.
