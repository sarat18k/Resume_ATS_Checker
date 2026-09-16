from jdmatcher.exceptions import PdfExtractionError, PdfTooLargeError
from jdmatcher.integrations.extraction import extract_text_from_pdf
from jdmatcher.settings import get_settings


def ensure_pdf_size(pdf_bytes: bytes) -> None:
    max_bytes = get_settings().max_pdf_bytes
    if len(pdf_bytes) > max_bytes:
        mb = max_bytes // (1024 * 1024)
        raise PdfTooLargeError(f"PDF exceeds maximum size of {mb} MB.")


def extract_pdf_text(pdf_bytes: bytes) -> str:
    ensure_pdf_size(pdf_bytes)
    text = extract_text_from_pdf(pdf_bytes)
    if not text:
        raise PdfExtractionError("Could not extract text from PDF.")
    return text
