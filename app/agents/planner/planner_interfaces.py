from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol
from backend.app.agents.planner.planner_models import PlannerRequest, PlannerOutput


class PlannerStrategy(ABC):
    """Abstract strategy for planner implementations.

    Concrete planners must implement `generate_plan` so they can be
    swapped via dependency injection (Strategy pattern).
    """

    @abstractmethod
    async def generate_plan(self, request: PlannerRequest) -> PlannerOutput:
        raise NotImplementedError
