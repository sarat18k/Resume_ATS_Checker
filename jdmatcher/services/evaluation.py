import json
import logging
import time

from jdmatcher.integrations.llm import llm_query
from jdmatcher.models import ResumeEvaluation
from jdmatcher.prompts.evaluation import build_evaluation_prompt
from jdmatcher.services.candidate import enrich_name_email_from_text
from jdmatcher.services.reporting import format_ats_report
from jdmatcher.settings import get_settings

logger = logging.getLogger(__name__)


def _clamp_score(value) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, score))


def evaluate_resume(
    resume_text: str,
    jd_text: str,
    experience_level: str = "Any",
) -> ResumeEvaluation:
    settings = get_settings()
    prompt = build_evaluation_prompt(
        resume_text, jd_text, experience_level, settings.limits
    )

    started = time.perf_counter()
    response = llm_query(prompt, json_mode=True)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    logger.info("Resume evaluation completed in %sms", elapsed_ms)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return ResumeEvaluation(
            name="Unknown",
            email="Unknown",
            ats_score=0,
            ats_report="Error parsing evaluation response.",
            general_evaluation="Error parsing evaluation response.",
            personality_profile="",
            missing_keywords="",
        )

    name, email = enrich_name_email_from_text(
        str(data.get("name") or "Unknown"),
        str(data.get("email") or "Unknown"),
        resume_text,
    )

    score = _clamp_score(data.get("ats_score", 0))
    payload = {
        "name": name,
        "email": email,
        "ats_score": score,
        "ats_report": format_ats_report(data, score),
        "general_evaluation": data.get("general_evaluation"),
        "personality_profile": data.get("personality_profile"),
        "missing_keywords": data.get("missing_keywords"),
    }
    return ResumeEvaluation.model_validate(payload)
