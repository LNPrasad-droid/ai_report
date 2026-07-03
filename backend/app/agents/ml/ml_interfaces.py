from __future__ import annotations
from typing import Protocol, Any, Dict


class ModelLoaderInterface(Protocol):
    async def load(self, storage_path: str) -> Any:
        ...
