from backend.app.providers.llm.llm_exceptions import LLMError


class ReportError(Exception):
    pass


class PromptGenerationError(ReportError):
    pass


class ReportGenerationError(ReportError):
    pass
