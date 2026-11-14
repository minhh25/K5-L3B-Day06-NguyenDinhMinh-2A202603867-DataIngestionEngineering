
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader
from .models import DocumentPage


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    reader = PdfReader(path)
    pages = []

    for page_number, pdf_page in enumerate(reader.pages, start=1):
        extraction_error = None
        try:
            text = pdf_page.extract_text() or ""
        except Exception as exc:
            text = ""
            extraction_error = type(exc).__name__

        document_page = DocumentPage(
            document_id=document_id,
            source=source,
            page=page_number,
            text=text,
            metadata={
                "page_number": page_number,
                "has_text": bool(text.strip()),
                "needs_ocr": not bool(text.strip()),
                "extraction_error": extraction_error
            }
        )

        pages.append(document_page)

    return pages


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
