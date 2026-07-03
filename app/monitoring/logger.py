"""Centralized structured logging utilities."""
import logging
import json
from typing import Any, Dict, Optional
from logging import LoggerAdapter
from uuid import uuid4
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # include extra fields if provided
        extra = getattr(record, "extra", None) or {}
        payload.update(extra)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def setup_monitoring_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root.handlers = []
    root.addHandler(handler)
    root.setLevel(level)


class MonitoringAdapter(LoggerAdapter):
    def process(self, msg: str, kwargs: Dict[str, Any]) -> (str, Dict[str, Any]):
        extra = kwargs.get("extra", {})
        # merge adapter's extra with call extra
        merged = {**self.extra, **extra}
        kwargs["extra"] = {"extra": merged}
        return msg, kwargs


def get_logger(agent_name: Optional[str] = None) -> MonitoringAdapter:
    setup_monitoring_logging()
    base = logging.getLogger(agent_name or "ai_report")
    return MonitoringAdapter(base, {"agent": agent_name or "unknown"})
