"""Request monitoring middleware"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from src.monitoring.prometheus_metrics import prometheus_metrics
from src.monitoring.sentry_config import capture_exception

class RequestMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to track requests and errors"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Track metrics
            duration = time.time() - start_time
            prometheus_metrics.track_request(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            
            return response
            
        except Exception as e:
            # Track error
            duration = time.time() - start_time
            prometheus_metrics.track_request(
                method=request.method,
                endpoint=request.url.path,
                status_code=500,
                duration=duration
            )
            
            # Capture with Sentry
            capture_exception(e, {
                "method": request.method,
                "path": request.url.path,
                "duration": duration
            })
            
            raise