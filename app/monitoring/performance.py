"""Performance helpers (memory usage) with optional psutil dependency."""
from typing import Optional

try:
    import psutil
except Exception:
    psutil = None


def get_memory_usage_bytes() -> Optional[int]:
    if psutil is None:
        return None
    p = psutil.Process()
    return p.memory_info().rss
