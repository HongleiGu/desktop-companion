from docx import Document
from models import ParsedFile
from .utils import MAX_CHARS

def parse_docx(
    filename: str,
    content_type: str,
    raw_bytes: bytes,
) -> ParsedFile:
    from io import BytesIO
    doc = Document(BytesIO(raw_bytes))

    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n\n".join(paragraphs)

    if not text.strip():
        raise ValueError("DOCX contains no readable text")

    return ParsedFile(
        filename=filename,
        content_type=content_type,
        text=text[:MAX_CHARS],
        warnings=["Layout and tables are ignored"],
    )
