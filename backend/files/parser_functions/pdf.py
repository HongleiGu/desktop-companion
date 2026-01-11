from pypdf import PdfReader
from io import BytesIO
from models import ParsedFile
from .utils import MAX_CHARS, MIN_TEXT_THRESHOLD

def parse_pdf(
    filename: str,
    content_type: str,
    raw_bytes: bytes,
) -> ParsedFile:
    reader = PdfReader(BytesIO(raw_bytes))

    pages_text = []
    warnings = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages_text.append(text)

    full_text = "\n\n".join(pages_text).strip()

    if len(full_text) < MIN_TEXT_THRESHOLD:
        raise ValueError(
            "PDF contains little or no extractable text "
            "(possibly scanned or image-based)."
        )

    return ParsedFile(
        filename=filename,
        content_type=content_type,
        text=full_text[:MAX_CHARS],
        warnings=warnings,
    )
