import io
import logging

import easyocr
import fitz
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

_OCR_READER = None


def _get_reader():
    global _OCR_READER
    if _OCR_READER is None:
        logger.info("Initializing EasyOCR reader...")
        _OCR_READER = easyocr.Reader(["en"], gpu=False)
    return _OCR_READER


def extract_text_with_ocr(pdf_bytes: bytes, max_pages: int) -> str:
    logger.info("Falling back to OCR extraction (max %s pages)...", max_pages)
    reader = _get_reader()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = []
    for page_index, page in enumerate(doc):
        if page_index >= max_pages:
            logger.warning("OCR page limit reached (%s pages)", max_pages)
            break
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        result = reader.readtext(np.array(img), detail=0)
        full_text.extend(result)
    return "\n".join(full_text)
