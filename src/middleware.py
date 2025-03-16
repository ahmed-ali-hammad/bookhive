import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response

from src.app_logging import LoggingConfig

logging.getLogger("uvicorn.access").disabled = True

logger = LoggingConfig.get_logger(__name__)


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next) -> Response:
        """
        Custom logging middleware for logging HTTP request and response details.

        This middleware logs the following details for each incoming request:
        - HTTP method (e.g., GET, POST)
        - URL path of the request
        - Response status code
        - Time taken to process the request (in seconds)

        Parameters:
        - request (Request): The incoming HTTP request object.
        - call_next: The function to pass the request to the next middleware or route handler.

        Returns:
        - response: The HTTP response object returned by the next middleware or route handler.

        Notes:
        - The processing time is calculated by measuring the time before and after the request is handled.
        - The log message includes the request method, URL, response status, and processing time rounded to 4 decimal places.
        """
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f"{request.method} - {request.url.path} - Response status [{response.status_code}] - completed after {round(processing_time,4)}s"
        logger.info(message)
        return response

    # Adds CORS middleware to allow cross-origin requests from any origin with any method
    # and any headers, as well as enabling credentials.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
