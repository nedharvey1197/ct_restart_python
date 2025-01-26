from prometheus_client import Counter, Histogram
import time

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')

class MetricsMiddleware:
    async def __call__(self, request: Request, call_next):
        request_count.inc()
        start_time = time.time()
        response = await call_next(request)
        request_latency.observe(time.time() - start_time)
        return response 