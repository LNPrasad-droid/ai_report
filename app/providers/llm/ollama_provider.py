import logging
import httpx
import asyncio
import time
from typing import Dict, Any
from backend.app.providers.llm.llm_interface import LLMProvider
from backend.app.providers.llm.llm_models import GenerateRequest, GenerateResponse
from backend.app.providers.llm.llm_exceptions import LLMConnectionError, LLMTimeoutError, InvalidResponseError
from backend.app.config import settings

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = None, model: str = None, timeout: int = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = timeout or settings.OLLAMA_TIMEOUT
        self.client: httpx.AsyncClient | None = None

    async def initialize(self) -> None:
        if self.client:
            return
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        # simple health check
        try:
            await self.health_check()
            logger.info("OllamaProvider initialized, base_url=%s model=%s", self.base_url, self.model)
        except Exception as exc:
            logger.exception("OllamaProvider initialization failed: %s", exc)
            raise LLMConnectionError(str(exc))

    async def health_check(self) -> Dict[str, Any]:
        # call /api/models to see available models
        url = "/api/models"
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
        except httpx.ReadTimeout:
            raise LLMTimeoutError("Ollama health check timed out")
        except Exception as exc:
            raise LLMConnectionError(str(exc))

    async def list_models(self) -> Dict[str, Any]:
        return await self.health_check()

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        await self.initialize()
        payload = {
            "model": request.model or self.model,
            "prompt": request.prompt,
            "temperature": request.temperature or settings.OLLAMA_TEMPERATURE,
            "top_p": request.top_p or settings.OLLAMA_TOP_P,
            "max_tokens": request.max_tokens or settings.OLLAMA_NUM_PREDICT,
        }

        # retries with exponential backoff
        retries = 3
        backoff = 1
        for attempt in range(1, retries + 1):
            try:
                t0 = time.time()
                r = await self.client.post('/api/generate', json=payload)
                r.raise_for_status()
                elapsed = time.time() - t0
                data = r.json()
                # Ollama returns {'text': '...'} or streaming; handle common shapes
                text = data.get('text') if isinstance(data, dict) else str(data)
                if text is None:
                    raise InvalidResponseError('No text in response')
                return GenerateResponse(text=text, model=payload['model'], generation_time_seconds=elapsed, metadata=data)
            except httpx.ReadTimeout:
                logger.warning('Ollama generate timeout, attempt %s', attempt)
                if attempt == retries:
                    raise LLMTimeoutError('Ollama generate timed out')
            except (httpx.HTTPError, InvalidResponseError) as exc:
                logger.warning('Ollama generate error (attempt %s): %s', attempt, exc)
                if attempt == retries:
                    raise LLMConnectionError(str(exc))
            await asyncio.sleep(backoff)
            backoff *= 2
