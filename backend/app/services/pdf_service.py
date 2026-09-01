import pdfplumber
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF file.
    Joins pages with newlines and strips surrounding whitespace.
    """
    pages_text: list[str] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        if len(pdf.pages) == 0:
            raise ValueError("PDF has no pages.")

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pages_text.append(page_text.strip())

    return "\n\n".join(pages_text)

MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


class ResumeValidationError(Exception):
    """Raised when an uploaded resume fails validation or extraction."""


def validate_and_extract_resume(filename: str, file_bytes: bytes) -> str:
    """
    Run all upload checks (extension, size, extraction, empty-text)
    and return the cleaned resume text, or raise ResumeValidationError.
    """
    if not filename or not filename.lower().endswith(".pdf"):
        raise ResumeValidationError("Only PDF files are accepted")

    if len(file_bytes) > MAX_RESUME_SIZE_BYTES:
        raise ResumeValidationError("File size must be under 5MB")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as exc:
        raise ResumeValidationError(f"Could not read PDF: {exc}")

    if not resume_text.strip():
        raise ResumeValidationError(
            "PDF appears to be empty or contains no readable text."
        )

    return resume_text