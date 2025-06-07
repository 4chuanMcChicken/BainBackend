import time
from typing import Callable
from fastapi import Request, Response
from loguru import logger


async def access_log_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware to log all HTTP requests with timing information"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # Calculate request processing time
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    
    # Construct and log the request details
    logger.info(
        f"method={request.method} path={request.url.path} "
        f"status_code={response.status_code} "
        f"duration={formatted_process_time}ms"
    )
    
    return response 