import re

from .models import Chunk, DocumentPage


CHAPTER = re.compile(r'^Chương\s+([IVX]+)\s*$', re.MULTILINE)
HEADER = re.compile(r'^CÔNG BÁO/[^\n]*(?:\n|$)')


def chapter_spans(pages: list[DocumentPage]) -> dict[int, list[dict]]:
    spans = {}
    current = None
    for page in sorted(pages, key=lambda p: p.page):
        header = HEADER.match(page.text)
        start = header.end() if header else 0
        items = []
        for match in CHAPTER.finditer(page.text):
            if match.start() > start:
                items.append({'start': start, 'end': match.start(), 'chapter': current})
            current = match.group(1)
            start = match.start()
        items.append({'start': start, 'end': len(page.text), 'chapter': current})
        spans[page.page] = items
    return spans


def attach_metadata(pages: list[DocumentPage], chunks: list[Chunk], snapshot: str) -> None:
    lookup = {p.page: p for p in pages}
    spans = chapter_spans(pages)
    offsets = {}
    for chunk in chunks:
        page = lookup[chunk.page]
        start = (chunk.metadata['start_char'] if chunk.metadata.get('strategy') == 'fixed_size'
                 else page.text.find(chunk.text, offsets.get(chunk.page, 0)))
        if start < 0:
            raise ValueError(f'Cannot locate chunk in normalized page: {chunk.chunk_id}')
        end = start + len(chunk.text)
        offsets[chunk.page] = end
        chapters = set()
        unknown = False
        for span in spans[chunk.page]:
            left, right = max(start, span['start']), min(end, span['end'])
            if left < right and page.text[left:right].strip():
                if span['chapter'] is None:
                    unknown = True
                else:
                    chapters.add(span['chapter'])
        chapter = next(iter(chapters)) if len(chapters) == 1 and not unknown else None
        chunk.metadata.update({
            'chapter': chapter,
            'chapters': sorted(chapters),
            'chapter_status': 'single' if chapter else 'mixed_or_unknown_or_header',
            'start_char': start,
            'end_char': end,
            'snapshot_sha256': snapshot,
        })
