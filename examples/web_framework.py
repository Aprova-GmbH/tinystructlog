"""
Web framework integration example for contexlog.

This example demonstrates how to integrate contexlog with a web framework
like FastAPI to automatically add request context to all log messages.

Note: This is a demonstration. To run this example, install FastAPI and uvicorn:
    pip install fastapi uvicorn
"""

from tinystructlog import get_logger, set_log_context, clear_log_context
import uuid

# Uncomment these imports if you want to run this example
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import uvicorn

log = get_logger(__name__)

# Example FastAPI application (commented out to avoid import errors)
"""
app = FastAPI(title="Contexlog Demo API")

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    '''
    Middleware that adds request context to all log messages.

    This ensures every log message during request processing includes
    the request ID, making it easy to trace all logs for a specific request.
    '''
    # Generate a unique request ID
    request_id = str(uuid.uuid4())

    # Set context for this request
    set_log_context(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    log.info("Request started")

    try:
        response = await call_next(request)
        log.info(f"Request completed with status {response.status_code}")
        return response
    except Exception as e:
        log.error(f"Request failed with error: {e}")
        raise
    finally:
        # Clean up context after request
        clear_log_context()

@app.get("/")
async def root():
    '''Root endpoint.'''
    log.info("Handling root request")
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    '''Get user endpoint with additional context.'''
    # Add user_id to the existing request context
    set_log_context(user_id=user_id)

    log.info("Fetching user data")
    # Simulate some processing
    log.debug("Querying database")
    log.info("User data retrieved")

    return {"user_id": user_id, "name": "Example User"}

@app.post("/orders")
async def create_order(order_data: dict):
    '''Create order endpoint.'''
    # Generate order ID and add to context
    order_id = str(uuid.uuid4())
    set_log_context(order_id=order_id)

    log.info("Creating new order")
    log.debug(f"Order data: {order_data}")

    # Simulate order processing
    log.info("Validating order")
    log.info("Processing payment")
    log.info("Order created successfully")

    return {"order_id": order_id, "status": "created"}

if __name__ == "__main__":
    # Run the application
    log.info("Starting FastAPI application with contexlog")
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Standalone example without FastAPI dependency
def simulate_web_request():
    """Simulate a web request with context."""
    request_id = str(uuid.uuid4())

    # Set request context
    set_log_context(request_id=request_id, method="GET", path="/api/users/123")

    log.info("Request started")

    # Add user context during processing
    set_log_context(user_id="123")
    log.info("Fetching user data")
    log.debug("Querying database")
    log.info("User data retrieved")

    # Clear context after request
    clear_log_context()
    log.info("Request completed (context cleared)")

if __name__ == "__main__":
    print("=== Simulated Web Request Example ===")
    print("(For full FastAPI example, uncomment the code above and install fastapi + uvicorn)\n")

    simulate_web_request()
