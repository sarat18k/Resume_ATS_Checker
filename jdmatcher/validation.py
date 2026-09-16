from jdmatcher.constants import EXPERIENCE_LEVELS


def normalize_experience_level(value: str) -> str:
    cleaned = (value or "").strip()
    if cleaned in EXPERIENCE_LEVELS:
        return cleaned
    allowed = ", ".join(EXPERIENCE_LEVELS)
    raise ValueError(f"Invalid experience_level. Allowed values: {allowed}")
