from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict
from backend.app.providers.llm.llm_models import GenerateRequest, GenerateResponse


class LLMProvider(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def list_models(self) -> Dict[str, Any]:
        raise NotImplementedError
