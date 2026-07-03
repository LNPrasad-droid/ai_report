class PlannerError(Exception):
    """Base exception for planner errors."""


class InvalidPlannerRequest(PlannerError):
    """Raised when incoming request is invalid."""


class PlanGenerationError(PlannerError):
    """Raised when the planner fails to generate a plan."""
