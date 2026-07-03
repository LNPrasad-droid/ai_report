from typing import Dict
from backend.app.providers.llm.prompt_templates.base_prompt import render_template

GENERAL_TEMPLATE = '''
You are an expert remote sensing analyst. Produce a concise structured JSON report.

Context:
{context}

Provide output as JSON with keys: executive_summary, technical_analysis, findings, recommendations, confidence.
'''


def build_general_prompt(context: Dict) -> str:
    return render_template(GENERAL_TEMPLATE, {"context": context})
