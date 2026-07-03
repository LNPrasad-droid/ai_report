from typing import Dict


def render_template(template: str, context: Dict) -> str:
    # Simple templating using format; future: Jinja2
    try:
        return template.format(**context)
    except Exception:
        # Fallback: concatenate key-values
        parts = [f"{k}: {v}" for k, v in context.items()]
        return "\n".join(parts)
