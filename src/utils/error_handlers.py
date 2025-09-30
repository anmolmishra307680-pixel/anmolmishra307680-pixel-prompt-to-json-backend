# errors.py
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("prompt_agent")

def register_exception_handlers(app):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(status_code=500, content={"error": "internal_server_error", "message": "An unexpected error occurred."})

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"error":"bad_request", "message": str(exc)})