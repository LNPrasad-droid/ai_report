class LLMError(Exception):
    pass


class LLMConnectionError(LLMError):
    pass


class LLMTimeoutError(LLMError):
    pass


class PromptGenerationError(LLMError):
    pass


class InvalidResponseError(LLMError):
    pass


class ReportGenerationError(LLMError):
    pass
