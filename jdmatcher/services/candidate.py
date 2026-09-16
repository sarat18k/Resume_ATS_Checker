import re


def extract_candidate_from_text(text: str) -> tuple[str, str]:
    """Regex/heuristic extraction without LLM (used by lightweight API endpoints)."""
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match.group() if email_match else "Unknown"
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if lines else "Unknown"
    return name, email


def enrich_name_email_from_text(
    name: str, email: str, resume_text: str
) -> tuple[str, str]:
    if name != "Unknown" and email != "Unknown":
        return name, email
    fallback_name, fallback_email = extract_candidate_from_text(resume_text)
    return (
        name if name != "Unknown" else fallback_name,
        email if email != "Unknown" else fallback_email,
    )
