import logging
import sys
import contextvars


request_context: contextvars.ContextVar[dict] = contextvars.ContextVar("request_context", default={})


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = request_context.get({})
        record.request_id = ctx.get("request_id", "-")
        record.user_id = ctx.get("user_id", "-")
        record.user_email = ctx.get("user_email", "-")
        record.user_role = ctx.get("user_role", "-")
        return True


def setup_logging() -> None:
    """Configure basic logging for the application.

    This uses the standard library logger and writes to stdout so containers
    and platforms can capture structured logs.
    """
    fmt = (
        "%(asctime)s %(levelname)s [%(name)s] "
        "[request_id=%(request_id)s user_id=%(user_id)s user_email=%(user_email)s user_role=%(user_role)s] "
        "%(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))
    handler.addFilter(RequestContextFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # Avoid adding duplicate handlers during reloads
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)


def set_request_context(**values) -> None:
    ctx = request_context.get({}).copy()
    ctx.update(values)
    request_context.set(ctx)


def clear_request_context() -> None:
    request_context.set({})
