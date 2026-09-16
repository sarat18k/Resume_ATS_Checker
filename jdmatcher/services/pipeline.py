from jdmatcher.models import ResumeEvaluation
from jdmatcher.services.evaluation import evaluate_resume
from jdmatcher.services.pdf import extract_pdf_text


def evaluate_resume_pdf(
    pdf_bytes: bytes,
    jd_text: str,
    experience_level: str = "Any",
) -> ResumeEvaluation:
    resume_text = extract_pdf_text(pdf_bytes)
    return evaluate_resume(resume_text, jd_text, experience_level)
