from jdmatcher.settings import Limits


def build_evaluation_prompt(
    resume_text: str,
    jd_text: str,
    experience_level: str,
    limits: Limits,
) -> str:
    return f"""
You are an expert recruiter and ATS analyzer. Compare the resume to the job description.

Target Experience Level: {experience_level}
(Strictly factor experience fit; deduct score if clearly under/over qualified.)

Return ONLY JSON with this exact structure:
{{
  "name": "candidate full name or Unknown",
  "email": "email or Unknown",
  "ats_score": <integer 0-100>,
  "key_skills_match": ["skill1", "skill2"],
  "missing_keywords": ["keyword1", "keyword2"],
  "summary_report": "3-5 sentences on fit including experience level",
  "improvement_suggestions": ["tip1", "tip2"],
  "general_evaluation": "ONE plain-text string (not a JSON object). Include: Overall Suitability, Strongest Points, Areas of Concern, Hiring Recommendation (Yes/No/Maybe). Use line breaks between sections.",
  "personality_profile": "ONE plain-text string (not a JSON object) with brief heuristic soft-skill notes only"
}}

IMPORTANT: general_evaluation and personality_profile must be strings, never nested objects.

Job Description:
{jd_text[: limits.jd_text]}

Resume:
{resume_text[: limits.resume_text]}
"""
