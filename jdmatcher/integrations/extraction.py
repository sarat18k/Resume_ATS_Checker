import io
import logging

import fitz
from pdfminer.high_level import extract_text

from jdmatcher.settings import get_settings

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_file) -> str:
    """PDFMiner -> PyMuPDF -> optional OCR fallback."""
    try:
        pdf_bytes = pdf_file.read()
    except Exception:
        pdf_bytes = pdf_file

    try:
        text = extract_text(io.BytesIO(pdf_bytes))
        if text and len(text.strip()) > 50:
            return text.strip()
    except Exception:
        pass

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text("text") for page in doc).strip()
        if text and len(text) > 50:
            return text
    except Exception:
        pass

    settings = get_settings()
    if not settings.ocr_enabled:
        logger.info("OCR disabled; skipping OCR fallback")
        return ""

    try:
        from jdmatcher.integrations.ocr import extract_text_with_ocr

        return extract_text_with_ocr(pdf_bytes, settings.max_ocr_pages)
    except Exception as exc:
        logger.error("OCR error: %s", exc)

    return ""
