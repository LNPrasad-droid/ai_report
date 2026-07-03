from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    SatelliteAgent = "SatelliteAgent"
    GISAgent = "GISAgent"
    MLAgent = "MLAgent"
    ReportAgent = "ReportAgent"
    RetrievalAgent = "RetrievalAgent"
    NotificationAgent = "NotificationAgent"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Intent(str, Enum):
    analyze_area = "analyze_area"
    explain_concept = "explain_concept"
    generate_report = "generate_report"
    detect_anomalies = "detect_anomalies"
    unknown = "unknown"


class PlannerRequest(BaseModel):
    query: str = Field(..., description="User natural language request")
    max_agents: Optional[int] = Field(10, description="Optional cap on number of agents")


class PlannerOutput(BaseModel):
    query: str
    intent: Intent
    agents: List[AgentType]
    reasoning: Optional[str]
    priority: Priority
