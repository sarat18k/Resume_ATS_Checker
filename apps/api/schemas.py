from typing import Literal

from pydantic import BaseModel, Field

from jdmatcher.models import ResumeEvaluation


class EvaluationSuccess(BaseModel):
    file: str
    status: Literal["success"] = "success"
    name: str
    email: str
    ats_score: int = Field(ge=0, le=100)
    ats_report: str
    general_evaluation: str
    personality_profile: str
    missing_keywords: str

    @classmethod
    def from_evaluation(cls, filename: str, evaluation: ResumeEvaluation) -> "EvaluationSuccess":
        return cls(
            file=filename,
            name=evaluation.name,
            email=evaluation.email,
            ats_score=evaluation.ats_score,
            ats_report=evaluation.ats_report,
            general_evaluation=evaluation.general_evaluation,
            personality_profile=evaluation.personality_profile,
            missing_keywords=evaluation.missing_keywords,
        )


class EvaluationError(BaseModel):
    file: str
    status: Literal["error"] = "error"
    message: str


class BatchEvaluationResponse(BaseModel):
    total_resumes: int
    successful: int
    failed: int
    results: list[EvaluationSuccess | EvaluationError]
