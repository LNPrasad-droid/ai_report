import logging
from typing import Dict, Any
from backend.app.providers.llm.prompt_templates.general_prompt import build_general_prompt
from backend.app.providers.llm.prompt_templates.crop_health_prompt import build_crop_health_prompt

logger = logging.getLogger(__name__)


class ReportBuilder:
    def __init__(self, max_prompt_length: int = 4000):
        self.max_prompt_length = max_prompt_length

    def build_prompt(self, prompt_type: str, inputs: Dict[str, Any]) -> str:
        # Compress / summarize inputs into a concise context string
        context = self._compress_inputs(inputs)
        if prompt_type == 'crop_health':
            prompt = build_crop_health_prompt({'satellite': inputs.get('satellite'), 'gis': inputs.get('gis'), 'docs': inputs.get('docs')})
        else:
            prompt = build_general_prompt(context)
        # truncate if too long
        if len(prompt) > self.max_prompt_length:
            prompt = prompt[: self.max_prompt_length]
        logger.info('Built prompt length=%d', len(prompt))
        return prompt

    def _compress_inputs(self, inputs: Dict[str, Any]) -> str:
        # naive compression: stringify and keep first N chars of each section
        parts = []
        for k in ['planner', 'docs', 'satellite', 'gis', 'ml', 'trace']:
            v = inputs.get(k)
            if not v:
                continue
            s = str(v)
            parts.append(f"{k}: {s[:800]}")
        return "\n".join(parts)
