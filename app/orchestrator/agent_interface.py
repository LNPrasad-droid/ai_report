from __future__ import annotations
from abc import ABC, abstractmethod
from backend.app.orchestrator.execution_context import ExecutionContext
from backend.app.orchestrator.execution_result import ExecutionResult


class AgentInterface(ABC):
    """Abstract interface that all agents must implement.

    The orchestrator will interact with agents only through this interface.
    """

    @abstractmethod
    async def run(self, context: ExecutionContext) -> ExecutionResult:
        raise NotImplementedError
