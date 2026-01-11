import chardet
from models import ParsedFile
from .utils import MAX_CHARS

def parse_text_file(
    filename: str,
    content_type: str,
    raw_bytes: bytes,
    language: str | None = None,
) -> ParsedFile:
    encoding = chardet.detect(raw_bytes)["encoding"] or "utf-8"
    text = raw_bytes.decode(encoding, errors="ignore")

    if not text.strip():
        raise ValueError("No readable text found")

    return ParsedFile(
        filename=filename,
        content_type=content_type,
        text=text[:MAX_CHARS],
        language=language,
        warnings=[],
    )
