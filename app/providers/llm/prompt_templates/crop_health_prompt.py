from typing import Dict
from backend.app.providers.llm.prompt_templates.base_prompt import render_template

CROP_HEALTH_TEMPLATE = '''
You are an expert agronomist. Given the following inputs, summarize crop health and provide actionable recommendations.

Satellite metadata: {satellite}
GIS statistics (indices): {gis}
Retrieved documents summary: {docs}

Return JSON: executive_summary, technical_analysis, findings (list), recommendations (list), confidence.
'''


def build_crop_health_prompt(context: Dict) -> str:
    return render_template(CROP_HEALTH_TEMPLATE, context)
