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