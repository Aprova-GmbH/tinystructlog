Usage Examples
==============

This page contains comprehensive examples for common use cases.

FastAPI Integration
-------------------

Complete example with FastAPI middleware for request tracing:

.. code-block:: python

    from fastapi import FastAPI, Request, HTTPException
    from contexlog import get_logger, set_log_context, clear_log_context
    import uuid
    import time

    app = FastAPI()
    log = get_logger(__name__)

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Set context for this request
        set_log_context(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
            client_ip=request.client.host if request.client else None,
        )

        start_time = time.time()
        log.info("Request started")

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            log.info(
                "Request completed",
                extra={
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                }
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as e:
            duration = time.time() - start_time
            log.error(
                f"Request failed: {str(e)}",
                extra={"duration_ms": round(duration * 1000, 2)},
                exc_info=True
            )
            raise

        finally:
            # Clean up context
            clear_log_context()

    @app.get("/users/{user_id}")
    async def get_user(user_id: str):
        # Add user_id to existing context
        set_log_context(user_id=user_id)

        log.info("Fetching user data")
        # Simulate database query
        user = {"id": user_id, "name": "John Doe"}

        log.info("User data retrieved")
        return user

    @app.post("/users")
    async def create_user(user_data: dict):
        log.info("Creating new user")
        # Your logic here
        new_user_id = str(uuid.uuid4())
        set_log_context(user_id=new_user_id)

        log.info("User created successfully")
        return {"id": new_user_id, **user_data}

Async Worker Tasks
------------------

Example for background task processing with context isolation:

.. code-block:: python

    import asyncio
    from contexlog import get_logger, set_log_context, log_context
    import uuid

    log = get_logger(__name__)

    async def process_job(job_id: str, job_type: str, data: dict):
        """Process a single job with isolated context."""
        # Each job gets its own context
        set_log_context(
            job_id=job_id,
            job_type=job_type,
            worker_id="worker-1"
        )

        log.info("Job started")

        try:
            # Simulate processing
            await asyncio.sleep(1)

            # Add progress context
            with log_context(stage="validation"):
                log.info("Validating job data")
                await asyncio.sleep(0.5)

            with log_context(stage="execution"):
                log.info("Executing job")
                await asyncio.sleep(0.5)
                # Your processing logic here

            log.info("Job completed successfully")
            return {"status": "success", "job_id": job_id}

        except Exception as e:
            log.error(f"Job failed: {str(e)}", exc_info=True)
            return {"status": "failed", "job_id": job_id, "error": str(e)}

    async def worker_main():
        """Main worker loop processing multiple jobs concurrently."""
        jobs = [
            {"id": str(uuid.uuid4()), "type": "email", "data": {}},
            {"id": str(uuid.uuid4()), "type": "report", "data": {}},
            {"id": str(uuid.uuid4()), "type": "export", "data": {}},
        ]

        # Process all jobs concurrently - each maintains isolated context
        results = await asyncio.gather(
            *[process_job(job["id"], job["type"], job["data"]) for job in jobs]
        )

        log.info(f"Processed {len(results)} jobs")
        return results

    if __name__ == "__main__":
        asyncio.run(worker_main())

Multi-Tenant Application
-------------------------

Example for a multi-tenant SaaS application:

.. code-block:: python

    from contexlog import get_logger, set_log_context, log_context
    from typing import Optional

    log = get_logger(__name__)

    class TenantContext:
        """Context manager for tenant operations."""

        def __init__(self, tenant_id: str, user_id: Optional[str] = None):
            self.tenant_id = tenant_id
            self.user_id = user_id

        def __enter__(self):
            context = {"tenant_id": self.tenant_id}
            if self.user_id:
                context["user_id"] = self.user_id
            set_log_context(**context)
            log.info("Tenant context activated")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            log.info("Tenant context deactivated")
            # Context will be automatically cleared by caller

    class TenantService:
        """Service that operates within tenant context."""

        def get_tenant_data(self, tenant_id: str, user_id: str):
            with TenantContext(tenant_id, user_id):
                log.info("Fetching tenant data")
                # All logs here will include tenant_id and user_id

                self._validate_access()
                data = self._query_database()
                self._audit_access()

                log.info("Tenant data retrieved successfully")
                return data

        def _validate_access(self):
            log.info("Validating tenant access")
            # Validation logic

        def _query_database(self):
            with log_context(operation="database_query"):
                log.info("Executing database query")
                # Query logic
                return {"data": "example"}

        def _audit_access(self):
            log.info("Recording access audit")
            # Audit logic

    # Usage
    service = TenantService()
    service.get_tenant_data(tenant_id="tenant-123", user_id="user-456")

Distributed Tracing
-------------------

Example for distributed tracing across services:

.. code-block:: python

    import httpx
    from contexlog import get_logger, set_log_context, clear_log_context
    import uuid

    log = get_logger(__name__)

    class DistributedTracingClient:
        """HTTP client that propagates trace context."""

        def __init__(self):
            self.client = httpx.AsyncClient()

        async def request(self, method: str, url: str, **kwargs):
            # Generate or use existing trace ID
            import contexlog.core as ctx_module
            context = ctx_module._log_ctx.get({})
            trace_id = context.get("trace_id", str(uuid.uuid4()))

            if "trace_id" not in context:
                set_log_context(trace_id=trace_id)

            # Add trace headers
            headers = kwargs.get("headers", {})
            headers.update({
                "X-Trace-ID": trace_id,
                "X-Span-ID": str(uuid.uuid4()),
            })
            kwargs["headers"] = headers

            log.info(f"Sending {method} request to {url}")

            try:
                response = await self.client.request(method, url, **kwargs)
                log.info(
                    f"Request completed with status {response.status_code}",
                    extra={"status_code": response.status_code}
                )
                return response
            except Exception as e:
                log.error(f"Request failed: {str(e)}", exc_info=True)
                raise

    async def service_a():
        """First service in the chain."""
        trace_id = str(uuid.uuid4())
        set_log_context(
            trace_id=trace_id,
            service="service-a",
            operation="process_order"
        )

        log.info("Service A: Processing order")

        # Call service B
        client = DistributedTracingClient()
        await client.request("POST", "http://service-b/process", json={"order_id": "123"})

        log.info("Service A: Order processing complete")
        clear_log_context()

Database Operations
-------------------

Example for database operations with connection pooling:

.. code-block:: python

    from contexlog import get_logger, log_context
    import asyncpg
    import time

    log = get_logger(__name__)

    class DatabasePool:
        """Database connection pool with context logging."""

        def __init__(self, dsn: str):
            self.dsn = dsn
            self.pool = None

        async def initialize(self):
            with log_context(operation="db_pool_init"):
                log.info("Initializing database pool")
                self.pool = await asyncpg.create_pool(self.dsn)
                log.info("Database pool initialized")

        async def execute_query(self, query: str, *args, query_name: str = None):
            """Execute a query with detailed logging."""
            with log_context(
                operation="db_query",
                query_name=query_name or "unnamed"
            ):
                start_time = time.time()
                log.info(f"Executing query: {query_name or query[:50]}")

                try:
                    async with self.pool.acquire() as conn:
                        result = await conn.fetch(query, *args)
                        duration = time.time() - start_time

                        log.info(
                            "Query completed",
                            extra={
                                "rows_returned": len(result),
                                "duration_ms": round(duration * 1000, 2)
                            }
                        )
                        return result

                except Exception as e:
                    duration = time.time() - start_time
                    log.error(
                        f"Query failed: {str(e)}",
                        extra={"duration_ms": round(duration * 1000, 2)},
                        exc_info=True
                    )
                    raise

    # Usage
    async def main():
        db = DatabasePool("postgresql://localhost/mydb")
        await db.initialize()

        # Each query gets detailed context
        users = await db.execute_query(
            "SELECT * FROM users WHERE active = $1",
            True,
            query_name="get_active_users"
        )

Error Handling and Debugging
-----------------------------

Example for comprehensive error handling:

.. code-block:: python

    from contexlog import get_logger, set_log_context, log_context
    import traceback

    log = get_logger(__name__)

    class ErrorHandler:
        """Centralized error handling with context."""

        def handle_error(self, error: Exception, context_info: dict):
            """Handle error with full context."""
            # Add error context
            set_log_context(
                error_type=type(error).__name__,
                error_id=str(uuid.uuid4()),
                **context_info
            )

            log.error(
                f"Error occurred: {str(error)}",
                extra={
                    "traceback": traceback.format_exc(),
                    "error_args": error.args,
                },
                exc_info=True
            )

            # Log recovery attempt
            with log_context(stage="recovery"):
                log.info("Attempting error recovery")
                self._attempt_recovery(error)

        def _attempt_recovery(self, error: Exception):
            # Recovery logic
            pass

    # Usage
    def risky_operation():
        try:
            set_log_context(operation="risky_operation", attempt=1)
            log.info("Starting risky operation")

            # Your code here
            result = perform_operation()

            log.info("Operation completed successfully")
            return result

        except Exception as e:
            handler = ErrorHandler()
            handler.handle_error(e, {"operation": "risky_operation"})
            raise
