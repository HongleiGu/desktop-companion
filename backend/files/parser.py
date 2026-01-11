from .parser_functions import *
import os

EXTENSION_PARSERS = {
  "txt": parse_text_file,
  "md": parse_text_file,
  "json": parse_text_file,
  "yaml": parse_text_file,
  "yml": parse_text_file,
  "xml": parse_text_file,

  "py": lambda *a: parse_text_file(*a, language="python"),
  "ts": lambda *a: parse_text_file(*a, language="typescript"),
  "cs": lambda *a: parse_text_file(*a, language="csharp"),
  # more languages can be added, no other changes needed

  "pdf": parse_pdf,
  "docx": parse_docx,
}

def parse_uploaded_file(
    filename: str,
    content_type: str,
    raw_bytes: bytes,
) -> ParsedFile:
    ext = os.path.splitext(filename)[1].lower().lstrip(".")

    if ext not in EXTENSION_PARSERS:
      raise ValueError(f"Unsupported file type: .{ext}")

    parser = EXTENSION_PARSERS[ext]

    return parser(
        filename=filename,
        content_type=content_type,
        raw_bytes=raw_bytes,
    )