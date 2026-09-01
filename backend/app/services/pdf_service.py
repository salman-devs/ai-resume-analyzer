import pdfplumber
import io
import docx


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


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract all text from a DOCX file.
    Joins paragraphs with newlines and strips surrounding whitespace.
    """
    document = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]

    if not paragraphs:
        raise ValueError("DOCX has no readable paragraphs.")

    return "\n\n".join(paragraphs)


MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


class ResumeValidationError(Exception):
    """Raised when an uploaded resume fails validation or extraction."""

SUPPORTED_EXTENSIONS = (".pdf", ".docx")


def validate_and_extract_resume(filename: str, file_bytes: bytes) -> str:
    """
    Run all upload checks (extension, size, extraction, empty-text)
    and return the cleaned resume text, or raise ResumeValidationError.
    """
    if not filename or not filename.lower().endswith(SUPPORTED_EXTENSIONS):
        raise ResumeValidationError("Only PDF or DOCX files are accepted")

    if len(file_bytes) > MAX_RESUME_SIZE_BYTES:
        raise ResumeValidationError("File size must be under 5MB")

    try:
        if filename.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_bytes)
        else:
            resume_text = extract_text_from_docx(file_bytes)
    except ResumeValidationError:
        raise
    except Exception as exc:
        raise ResumeValidationError(f"Could not read file: {exc}")

    if not resume_text.strip():
        raise ResumeValidationError(
            "File appears to be empty or contains no readable text."
        )

    return resume_text