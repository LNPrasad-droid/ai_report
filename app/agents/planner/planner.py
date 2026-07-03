import logging
from typing import List
from backend.app.agents.planner.planner_interfaces import PlannerStrategy
from backend.app.agents.planner.planner_models import (
    PlannerRequest,
    PlannerOutput,
    AgentType,
    Intent,
    Priority,
)
from backend.app.agents.planner.planner_exceptions import PlanGenerationError

logger = logging.getLogger(__name__)


class RuleBasedPlanner(PlannerStrategy):
    """A simple rule-based planner.

    This implementation uses keyword matching to determine intent and
    which agents should participate. It is easily replaceable via the
    `PlannerStrategy` interface for future LLM-driven planners.
    """

    def __init__(self) -> None:
        # Define rules mapping intents to agents and priorities
        self.intent_rules = {
            Intent.analyze_area: {
                "agents": [AgentType.SatelliteAgent, AgentType.GISAgent, AgentType.MLAgent, AgentType.ReportAgent],
                "priority": Priority.high,
            },
            Intent.explain_concept: {
                "agents": [AgentType.RetrievalAgent, AgentType.ReportAgent],
                "priority": Priority.medium,
            },
            Intent.generate_report: {
                "agents": [AgentType.GISAgent, AgentType.MLAgent, AgentType.ReportAgent],
                "priority": Priority.high,
            },
            Intent.detect_anomalies: {
                "agents": [AgentType.SatelliteAgent, AgentType.GISAgent, AgentType.MLAgent, AgentType.ReportAgent],
                "priority": Priority.high,
            },
        }

        # Mapping of keywords to intents
        self.keyword_map = {
            Intent.analyze_area: ["health", "unhealthy", "disease", "detect", "identify", "show"],
            Intent.explain_concept: ["explain", "what is", "define", "meaning of", "how does"],
            Intent.generate_report: ["report", "generate report", "create report", "summary"],
            Intent.detect_anomalies: ["anomaly", "anomalies", "outlier", "hotspot", "unexpected"],
        }

    async def generate_plan(self, request: PlannerRequest) -> PlannerOutput:
        query = request.query.strip()
        logger.info("Generating plan for query: %s", query)

        try:
            intent = self._infer_intent(query)
            rule = self.intent_rules.get(intent)
            if rule is None:
                # Fallback to unknown intent
                intent = Intent.unknown
                agents = [AgentType.RetrievalAgent, AgentType.ReportAgent]
                priority = Priority.low
                reasoning = "No matching intent rules; defaulting to retrieval+report."
            else:
                agents = rule["agents"]
                priority = rule["priority"]
                reasoning = f"Matched intent '{intent}' using keyword rules."

            # Cap agents if requested
            if request.max_agents and len(agents) > request.max_agents:
                agents = agents[: request.max_agents]

            output = PlannerOutput(
                query=query,
                intent=intent,
                agents=agents,
                reasoning=reasoning,
                priority=priority,
            )
            logger.debug("Plan generated: %s", output.json())
            return output
        except Exception as exc:
            logger.exception("Failed to generate plan: %s", exc)
            raise PlanGenerationError(str(exc))

    def _infer_intent(self, query: str) -> Intent:
        q = query.lower()
        # simple keyword matching; first match wins
        for intent, keywords in self.keyword_map.items():
            for kw in keywords:
                if kw in q:
                    return intent
        return Intent.unknown
