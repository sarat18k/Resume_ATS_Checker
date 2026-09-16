class PdfTooLargeError(ValueError):
    """Raised when an uploaded PDF exceeds the configured size limit."""


class PdfExtractionError(ValueError):
    """Raised when text cannot be extracted from a PDF."""
