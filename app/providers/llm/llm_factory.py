from typing import Optional
from backend.app.providers.llm.llm_interface import LLMProvider
from backend.app.providers.llm.ollama_provider import OllamaProvider
from backend.app.config import settings


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    # For now, only OllamaProvider is available. Switch based on name.
    name = (provider_name or '').lower()
    if name in ['', 'ollama', 'local']:
        return OllamaProvider(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, timeout=settings.OLLAMA_TIMEOUT)
    # Other providers can be added here
    return OllamaProvider(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, timeout=settings.OLLAMA_TIMEOUT)
