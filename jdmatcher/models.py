from pydantic import BaseModel, Field, field_validator

from jdmatcher.normalize import coerce_keyword_list, coerce_text_field


class ResumeEvaluation(BaseModel):
    name: str = "Unknown"
    email: str = "Unknown"
    ats_score: int = Field(ge=0, le=100, default=0)
    ats_report: str = ""
    general_evaluation: str = ""
    personality_profile: str = ""
    missing_keywords: str = ""

    @field_validator(
        "name",
        "email",
        "ats_report",
        "general_evaluation",
        "personality_profile",
        mode="before",
    )
    @classmethod
    def _coerce_text_fields(cls, value):
        if isinstance(value, (dict, list)):
            return coerce_text_field(value)
        if value is None:
            return ""
        return value

    @field_validator("missing_keywords", mode="before")
    @classmethod
    def _coerce_keywords(cls, value):
        return coerce_keyword_list(value)
