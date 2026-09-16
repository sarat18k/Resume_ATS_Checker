import asyncio
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from apps.api.evaluation_service import (
    evaluate_many,
    extract_candidate_from_upload,
    extract_text_from_upload,
)
from apps.api.schemas import BatchEvaluationResponse, EvaluationError, EvaluationSuccess
from jdmatcher.exceptions import PdfExtractionError, PdfTooLargeError
from jdmatcher.services.pipeline import evaluate_resume_pdf
from jdmatcher.settings import get_settings
from jdmatcher.validation import normalize_experience_level

router = APIRouter(tags=["evaluation"])


def _require_jd(jd_text: str) -> None:
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")


def _parse_experience_level(experience_level: str) -> str:
    try:
        return normalize_experience_level(experience_level)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _sort_batch_results(
    results: list[EvaluationSuccess | EvaluationError],
) -> list[EvaluationSuccess | EvaluationError]:
    successes = [item for item in results if isinstance(item, EvaluationSuccess)]
    errors = [item for item in results if isinstance(item, EvaluationError)]
    successes.sort(key=lambda item: item.ats_score, reverse=True)
    return successes + errors


@router.get("/health")
def health_check():
    settings = get_settings()
    ready = bool(settings.openai_api_key)
    return {
        "status": "ok" if ready else "degraded",
        "openai_configured": ready,
        "ocr_enabled": settings.ocr_enabled,
        "api_auth_enabled": settings.api_auth_enabled,
    }


@router.post("/evaluate", response_model=BatchEvaluationResponse)
async def evaluate_resumes(
    jd_text: str = Form(...),
    experience_level: str = Form(default="Any"),
    resumes: List[UploadFile] = File(...),
):
    _require_jd(jd_text)
    level = _parse_experience_level(experience_level)
    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume file is required.")

    max_batch = get_settings().max_batch_resumes
    if len(resumes) > max_batch:
        raise HTTPException(
            status_code=400,
            detail=f"A maximum of {max_batch} resumes is allowed per request.",
        )

    uploads = [(resume.filename, await resume.read()) for resume in resumes]
    results = _sort_batch_results(await evaluate_many(uploads, jd_text, level))
    successes = [item for item in results if isinstance(item, EvaluationSuccess)]

    return BatchEvaluationResponse(
        total_resumes=len(resumes),
        successful=len(successes),
        failed=len(results) - len(successes),
        results=results,
    )


@router.post("/evaluate-single")
async def evaluate_single_resume(
    jd_text: str = Form(...),
    experience_level: str = Form(default="Any"),
    resume: UploadFile = File(...),
):
    _require_jd(jd_text)
    level = _parse_experience_level(experience_level)
    try:
        pdf_bytes = await resume.read()
        evaluation = await asyncio.to_thread(
            evaluate_resume_pdf, pdf_bytes, jd_text, level
        )
        payload = EvaluationSuccess.from_evaluation(resume.filename, evaluation)
        return {"status": "success", **payload.model_dump()}
    except PdfTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except PdfExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Error processing resume: {exc}"
        ) from exc


@router.post("/extract-text")
async def extract_text_endpoint(resume: UploadFile = File(...)):
    try:
        text = await extract_text_from_upload(await resume.read())
        return {"status": "success", "file": resume.filename, "text": text}
    except PdfTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except PdfExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {exc}") from exc


@router.post("/extract-candidate-info")
async def extract_info_endpoint(resume: UploadFile = File(...)):
    try:
        name, email = await extract_candidate_from_upload(await resume.read())
        return {
            "status": "success",
            "file": resume.filename,
            "name": name,
            "email": email,
        }
    except PdfTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except PdfExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error extracting info: {exc}") from exc
