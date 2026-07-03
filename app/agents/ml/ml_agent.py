from backend.app.orchestrator.agent_interface import AgentInterface
from backend.app.orchestrator.execution_result import ExecutionResult, AgentStatus
from backend.app.agents.ml.ml_service import MLService
from datetime import datetime


class MLAgent(AgentInterface):
    def __init__(self, service: MLService = None):
        self.service = service or MLService()
        self.name = "MLAgent"

    async def run(self, context):
        start = datetime.utcnow()
        try:
            # expect context.intermediate_results to contain 'gis' features
            gis = context.intermediate_results.get("GISAgent") or {}
            # compute features
            from backend.app.agents.ml.feature_pipeline import compute_indices

            features = compute_indices(gis)
            from backend.app.agents.ml.ml_models import PredictRequest

            req = PredictRequest(job_id=context.metadata.get("job_id") if context.metadata else None, features=features, crop=context.metadata.get("crop") if context.metadata else "unknown")
            res = await self.service.predict(req)
            end = datetime.utcnow()
            return ExecutionResult(
                agent_name=self.name,
                status=AgentStatus.success,
                start_time=start,
                end_time=end,
                duration_seconds=(end - start).total_seconds(),
                output=res.model_dump(),
            )
        except Exception as exc:
            end = datetime.utcnow()
            return ExecutionResult(
                agent_name=self.name,
                status=AgentStatus.failed,
                start_time=start,
                end_time=end,
                duration_seconds=(end - start).total_seconds(),
                output=None,
                error=str(exc),
            )
