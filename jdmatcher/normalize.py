"""Coerce LLM JSON fields into strings expected by domain models."""


def coerce_text_field(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            parts.append(f"**{key}**\n{_coerce_scalar(item)}")
        return "\n\n".join(parts)
    if isinstance(value, list):
        return "\n".join(f"- {_coerce_scalar(item)}" for item in value)
    return str(value).strip()


def _coerce_scalar(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def coerce_keyword_list(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value if str(v).strip())
    if isinstance(value, dict):
        return ", ".join(str(v) for v in value.values())
    return str(value).strip()
