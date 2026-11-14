
import re

from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    if size <= 0:
        raise ValueError("size must be greater than 0")

    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be >= 0 and < size")

    text = page.text

    if not text or not text.strip():
        return []

    chunks = []
    step = size - overlap

    for index, start in enumerate(range(0, len(text), step)):
        end = min(start + size, len(text))
        chunk_text = text[start:end]

        if not chunk_text.strip():
            continue

        chunk = Chunk(
            chunk_id=f"{page.document_id}_p{page.page}_fixed_{index}",
            document_id=page.document_id,
            source=page.source,
            page=page.page,
            text=chunk_text,
            metadata={
                **page.metadata,
                "strategy": "fixed_size",
                "chunk_index": index,
                "start_char": start,
                "end_char": end,
                "chunk_size": size,
                "overlap": overlap
            }
        )

        chunks.append(chunk)

        if end == len(text):
            break

    return chunks


def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    if max_size <= 0:
        raise ValueError("max_size must be greater than 0")

    text = page.text

    if not text or not text.strip():
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    groups = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_size:
            if current:
                groups.append(current)
                current = ""

            for start in range(0, len(paragraph), max_size):
                part = paragraph[start:start + max_size]

                if part.strip():
                    groups.append(part)

            continue

        if not current:
            current = paragraph
        elif len(current) + 2 + len(paragraph) <= max_size:
            current += "\n\n" + paragraph
        else:
            groups.append(current)
            current = paragraph

    if current:
        groups.append(current)

    chunks = []

    for index, chunk_text in enumerate(groups):
        chunk = Chunk(
            chunk_id=f"{page.document_id}_p{page.page}_paragraph_{max_size}_{index}",
            document_id=page.document_id,
            source=page.source,
            page=page.page,
            text=chunk_text,
            metadata={
                **page.metadata,
                "strategy": "by_paragraph",
                "chunk_index": index,
                "max_size": max_size,
                "char_count": len(chunk_text)
            }
        )

        chunks.append(chunk)

    return chunks



def by_article(pages: list[DocumentPage], max_size: int = 800) -> list[Chunk]:
    if max_size <= 0:
        raise ValueError("max_size must be greater than 0")

    if not pages:
        return []

    pattern = re.compile(r"^\s*Điều\s+(\d+)\s*\.\s*(.*)$", re.IGNORECASE)
    sections = []
    current_lines = []
    current_article = None
    current_title = None

    for page in pages:
        if not page.text.strip():
            continue

        for line in page.text.splitlines():
            line = line.strip()

            if not line:
                continue

            if re.match(r"^CÔNG BÁO/Số\s+", line):
                continue

            match = pattern.match(line)

            if match:
                if current_lines:
                    sections.append(
                        (current_article, current_title, current_lines)
                    )

                current_article = int(match.group(1))
                current_title = line
                current_lines = []

            current_lines.append((line, page))

    if current_lines:
        sections.append((current_article, current_title, current_lines))

    chunks = []

    for article_number, title, lines in sections:
        header = title if title else ""
        parts = []
        current_text = ""
        current_pages = []

        def flush():
            nonlocal current_text, current_pages

            if current_text.strip():
                parts.append((current_text.strip(), current_pages.copy()))

            current_text = ""
            current_pages = []

        for line, page in lines:
            if line == header and not current_text:
                candidate = line
            elif current_text:
                candidate = current_text + "\n" + line
            else:
                candidate = line

            if len(candidate) <= max_size:
                current_text = candidate
                current_pages.append(page)
                continue

            if current_text:
                flush()

            remaining = line

            while remaining:
                prefix = ""

                if header and remaining != header:
                    prefix = header + "\n"

                available = max_size - len(prefix)

                if available <= 0:
                    prefix = ""
                    available = max_size

                if len(remaining) <= available:
                    current_text = prefix + remaining
                    current_pages = [page]
                    break

                split_at = remaining.rfind(" ", 0, available + 1)

                if split_at <= 0:
                    split_at = available

                part = remaining[:split_at].strip()

                if part:
                    parts.append((prefix + part, [page]))

                remaining = remaining[split_at:].strip()

        flush()

        for index, (text, used_pages) in enumerate(parts):
            first_page = min(p.page for p in used_pages)
            last_page = max(p.page for p in used_pages)
            source_page = used_pages[0]

            article_id = (
                str(article_number)
                if article_number is not None
                else "preamble"
            )

            chunks.append(
                Chunk(
                    chunk_id=(
                        f"{source_page.document_id}"
                        f"_article_{article_id}_{index}"
                    ),
                    document_id=source_page.document_id,
                    source=source_page.source,
                    page=first_page,
                    text=text,
                    metadata={
                        **source_page.metadata,
                        "strategy": "by_article",
                        "article": article_number,
                        "article_title": title,
                        "page_start": first_page,
                        "page_end": last_page,
                        "chunk_index": index,
                        "max_size": max_size,
                        "char_count": len(text)
                    }
                )
            )

    return chunks


def by_paragraph_overlap(
    page: DocumentPage,
    max_size: int = 800,
    overlap: int = 100
) -> list[Chunk]:
    if max_size <= 0:
        raise ValueError("max_size must be greater than 0")

    if overlap < 0 or overlap >= max_size:
        raise ValueError("overlap must be >= 0 and < max_size")

    text = page.text

    if not text or not text.strip():
        return []

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    groups = []
    current = ""

    for paragraph in paragraphs:
        if current:
            current += "\n\n" + paragraph
        else:
            current = paragraph

    step = max_size - overlap

    for start in range(0, len(current), step):
        end = min(start + max_size, len(current))
        part = current[start:end]

        if part.strip():
            groups.append((start, end, part))

        if end == len(current):
            break

    chunks = []

    for index, (start, end, chunk_text) in enumerate(groups):
        chunks.append(
            Chunk(
                chunk_id=f"{page.document_id}_p{page.page}_paragraph_overlap_{max_size}_{overlap}_{index}",
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata={
                    **page.metadata,
                    "strategy": "paragraph_overlap",
                    "chunk_index": index,
                    "max_size": max_size,
                    "overlap": overlap,
                    "start_char": start,
                    "end_char": end,
                    "char_count": len(chunk_text)
                }
            )
        )

    return chunks
