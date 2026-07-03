"""FastAPI middleware for observability: request IDs, timing, logging and error capture."""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from uuid import uuid4
import time
import logging
from backend.app.monitoring.logger import get_logger
from backend.app.monitoring.metrics import MetricsCollector
from backend.app.monitoring.execution_trace import ExecutionTraceRepository
from backend.app.monitoring.performance import get_memory_usage_bytes
from backend.app.core.logger import request_context

logger = get_logger("MonitoringMiddleware")


class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        # propagate job and correlation ids if provided as headers
        job_id = request.headers.get("X-Job-Id")
        correlation_id = request.headers.get("X-Correlation-Id") or request.headers.get("X-CorrelationID")
        path = request.url.path
        method = request.method
        start = time.time()
        mem_before = get_memory_usage_bytes()

        # attach request information to state for downstream handlers
        request.state.request_id = request_id
        request.state.job_id = job_id
        request.state.correlation_id = correlation_id
        request.state.user = getattr(request.state, "user", None)

        if request.state.user is not None:
            user_id = getattr(request.state.user, "uid", None)
            user_email = getattr(request.state.user, "email", None)
            user_role = getattr(request.state.user, "role", None)
        else:
            user_id = None
            user_email = None
            user_role = None

        try:
            response = await call_next(request)
            status_code = response.status_code
            success = 200 <= status_code < 400
        except Exception as exc:
            status_code = 500
            success = False
            logger.error("Unhandled exception", extra={"request_id": request_id, "path": path, "error": str(exc)})
            # record metric for failure
            await MetricsCollector.record(agent_name=None, metric_type="request_failure", value=1, request_id=request_id, tags={"path": path, "method": method})
            raise
        finally:
            end = time.time()
            duration = end - start
            mem_after = get_memory_usage_bytes()
            mem_delta = None
            if mem_before is not None and mem_after is not None:
                mem_delta = mem_after - mem_before

            # record metrics
            await MetricsCollector.record(agent_name=None, metric_type="request_duration_seconds", value=duration, request_id=request_id, tags={"path": path, "method": method})
            if mem_delta is not None:
                await MetricsCollector.record(agent_name=None, metric_type="memory_delta_bytes", value=mem_delta, request_id=request_id, tags={"path": path})

            # structured log
            ctx = request_context.get({})
            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                    "status_code": status_code,
                    "duration_seconds": duration,
                    "memory_delta": mem_delta,
                    "user_id": ctx.get("user_id"),
                    "user_email": ctx.get("user_email"),
                    "user_role": ctx.get("user_role"),
                },
            )

        return response
