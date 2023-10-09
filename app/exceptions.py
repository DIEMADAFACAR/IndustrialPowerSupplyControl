from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc}")
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)


async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {exc}")
    return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)


async def custom_starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"Starlette HTTP Exception: {exc}")
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
