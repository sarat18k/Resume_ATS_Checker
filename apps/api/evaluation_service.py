import asyncio

from apps.api.schemas import EvaluationError, EvaluationSuccess
from jdmatcher.exceptions import PdfExtractionError, PdfTooLargeError
from jdmatcher.services.candidate import extract_candidate_from_text
from jdmatcher.services.pdf import extract_pdf_text
from jdmatcher.services.pipeline import evaluate_resume_pdf
from jdmatcher.settings import get_settings

_semaphore: asyncio.Semaphore | None = None


def _evaluation_semaphore() -> asyncio.Semaphore:
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(get_settings().max_concurrent_evaluations)
    return _semaphore


async def evaluate_pdf_bytes(
    filename: str,
    pdf_bytes: bytes,
    jd_text: str,
    experience_level: str,
) -> EvaluationSuccess | EvaluationError:
    try:
        async with _evaluation_semaphore():
            evaluation = await asyncio.to_thread(
                evaluate_resume_pdf, pdf_bytes, jd_text, experience_level
            )
        return EvaluationSuccess.from_evaluation(filename, evaluation)
    except PdfTooLargeError as exc:
        return EvaluationError(file=filename, message=str(exc))
    except PdfExtractionError as exc:
        return EvaluationError(file=filename, message=str(exc))
    except Exception as exc:
        return EvaluationError(file=filename, message=str(exc))


async def evaluate_many(
    items: list[tuple[str, bytes]],
    jd_text: str,
    experience_level: str,
) -> list[EvaluationSuccess | EvaluationError]:
    tasks = [
        evaluate_pdf_bytes(name, data, jd_text, experience_level)
        for name, data in items
    ]
    return list(await asyncio.gather(*tasks))


async def extract_text_from_upload(pdf_bytes: bytes) -> str:
    return await asyncio.to_thread(extract_pdf_text, pdf_bytes)


async def extract_candidate_from_upload(pdf_bytes: bytes) -> tuple[str, str]:
    resume_text = await asyncio.to_thread(extract_pdf_text, pdf_bytes)
    return await asyncio.to_thread(extract_candidate_from_text, resume_text)
