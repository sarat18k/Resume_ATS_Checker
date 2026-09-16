from jdmatcher.models import ResumeEvaluation
from jdmatcher.normalize import coerce_keyword_list, coerce_text_field


def format_ats_report(data: dict, score: int) -> str:
    suggestions = data.get("improvement_suggestions") or []
    if not isinstance(suggestions, list):
        suggestions = [str(suggestions)]
    suggestion_lines = "".join(f"- {item}\n" for item in suggestions)
    skills = data.get("key_skills_match") or []
    if not isinstance(skills, list):
        skills = [str(skills)]
    return f"""**ATS Score:** {score}%

**Summary:**
{coerce_text_field(data.get("summary_report") or "No summary provided.")}

**Matching Skills:**
{", ".join(str(s) for s in skills)}

**Missing Keywords:**
{coerce_keyword_list(data.get("missing_keywords"))}

**Suggestions:**
{suggestion_lines}
"""


def format_full_text_report(evaluation: ResumeEvaluation, filename: str, report_date: str) -> str:
    return f"""
JD MATCHER REPORT
==================================================
Candidate: {evaluation.name}
Email:     {evaluation.email}
File:      {filename}
Date:      {report_date}
==================================================

[ ATS SCORE: {evaluation.ats_score}% ]

--- ATS ANALYSIS ---
{evaluation.ats_report}

--- HR EVALUATION ---
{evaluation.general_evaluation}

--- PERSONALITY PROFILE (HEURISTIC) ---
{evaluation.personality_profile}

--- MISSING KEYWORDS ---
{evaluation.missing_keywords}
"""
