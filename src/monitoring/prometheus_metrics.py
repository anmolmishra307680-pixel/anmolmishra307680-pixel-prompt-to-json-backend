"""Prometheus metrics integration"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
active_connections = Gauge('active_connections', 'Active connections')
job_count = Counter('ai_jobs_total', 'Total AI jobs', ['job_type', 'status'])
job_duration = Histogram('ai_job_duration_seconds', 'AI job duration', ['job_type'])
compute_cost = Counter('compute_cost_total', 'Total compute cost', ['provider'])

class PrometheusMetrics:
    """Prometheus metrics collector"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def track_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Track HTTP request metrics"""
        request_count.labels(method=method, endpoint=endpoint, status=str(status_code)).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    def track_job(self, job_type: str, status: str, duration: float = 0):
        """Track AI job metrics"""
        job_count.labels(job_type=job_type, status=status).inc()
        if duration > 0:
            job_duration.labels(job_type=job_type).observe(duration)
    
    def track_compute_cost(self, provider: str, cost: float):
        """Track compute cost"""
        compute_cost.labels(provider=provider).inc(cost)
    
    def set_active_connections(self, count: int):
        """Set active connections gauge"""
        active_connections.set(count)
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format"""
        return generate_latest().decode('utf-8')
    
    def get_metrics_response(self) -> Response:
        """Get Prometheus metrics as FastAPI response"""
        metrics_data = generate_latest()
        return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)

# Global metrics instance
prometheus_metrics = PrometheusMetrics()