import argparse
from dataclasses import asdict
from datetime import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
from zoneinfo import ZoneInfo

import psycopg
from dotenv import load_dotenv

from .chunking import fixed_size, by_paragraph
from .evaluation import evaluate_query, normalize_evidence, summarize
from .ingestion import load_pdf, normalize_text
from .metadata import attach_metadata
from .store import PgVectorStore

ROOT = Path(__file__).resolve().parents[2]
STARTER = ROOT / 'starter'
MODEL = 'intfloat/multilingual-e5-small'
REVISION = '614241f622f53c4eeff9890bdc4f31cfecc418b3'
CONFIGS = {'A': 'fixed_800_100', 'B': 'paragraph_800', 'C': 'paragraph_800'}


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def read(path):
    return json.loads(Path(path).read_text())


def timestamp():
    return datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()


def database_url():
    load_dotenv(STARTER / '.env')
    url = os.getenv('DATABASE_URL')
    if not url:
        raise ValueError('DATABASE_URL missing; copy starter/.env.example to starter/.env')
    return url


def load_corpus(manifest_path: Path, output: Path):
    manifest = read(manifest_path)
    documents = []
    logs = []
    for entry in manifest['sources']:
        path = ROOT / entry['source_path_or_url']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry['snapshot_sha256']:
            raise ValueError('Source snapshot changed; review and update manifest before ingest')
        pages = load_pdf(path, entry['source_id'], path.name)
        for page in pages:
            page.text = normalize_text(page.text)
            logs.append({'document_id': page.document_id, 'page': page.page,
                         'characters': len(page.text), **page.metadata})
        save(output / 'ingestion_pages.json', logs)
        if len(pages) != entry['physical_pages']:
            raise ValueError('Manifest physical_pages disagrees with PDF')
        useful = entry['useful_pages']
        if len(useful) != len(set(useful)) or any(type(n) is not int or not 1 <= n <= len(pages) for n in useful):
            raise ValueError('Invalid useful page IDs')
        if any(not pages[n-1].text.strip() for n in useful):
            raise ValueError('Useful page without text: inspect ingestion_pages.json; OCR required')
        if sum(len(p.text) for p in pages) != entry['normalized_characters']:
            raise ValueError('Manifest normalized character count disagrees with extraction')
        if any(p.metadata['extraction_error'] for p in pages):
            raise ValueError('PDF extraction errors: inspect ingestion_pages.json')
        documents.append((entry, pages))
    if sum(len(e['useful_pages']) for e, _ in documents) < 30:
        raise ValueError('Corpus needs at least 30 useful content pages')
    if len({e['source_id'] for e, _ in documents}) != len(documents):
        raise ValueError('Duplicate source IDs in manifest')
    return documents


def build_chunks(documents):
    result = {'fixed_800_100': [], 'paragraph_800': []}
    for entry, pages in documents:
        for name, fn in [('fixed_800_100', lambda p: fixed_size(p, 800, 100)),
                         ('paragraph_800', lambda p: by_paragraph(p, 800))]:
            chunks = [chunk for page in pages for chunk in fn(page)]
            attach_metadata(pages, chunks, entry['snapshot_sha256'])
            for chunk in chunks:
                chunk.metadata.update({'embedding_model': MODEL, 'embedding_revision': REVISION})
            result[name].extend(chunks)
    return result


def load_questions(path, documents):
    questions = read(path)
    if len({q['id'] for q in questions}) != len(questions):
        raise ValueError('Duplicate benchmark question ID')
    if sum(q['split'] == 'dev' for q in questions) < 15 or sum(q['split'] == 'test' for q in questions) < 5:
        raise ValueError('Benchmark requires >=15 dev and >=5 test questions')
    filtered = [q for q in questions if q.get('filter')]
    if len(filtered) < 3 or not any(q['split'] == 'test' for q in filtered):
        raise ValueError('Benchmark requires >=3 filter questions including test')
    pages = {(p.document_id, p.page): p for _, doc in documents for p in doc}
    for question in questions:
        if not all(isinstance(question.get(k), str) and question[k].strip()
                   for k in ('id', 'question', 'expected_answer')):
            raise ValueError('Benchmark requires nonempty id, question and expected_answer')
        if question['split'] not in ('dev', 'test'):
            raise ValueError('Question split must be dev or test')
        trace = evaluate_query(question, [])
        for gold in trace['gold_evidence']:
            sources = gold['gold_source_id'] if isinstance(gold['gold_source_id'], list) else [gold['gold_source_id']]
            numbers = gold['gold_page'] if isinstance(gold['gold_page'], list) else [gold['gold_page']]
            quotes = gold['evidence_quote'] if isinstance(gold['evidence_quote'], list) else [gold['evidence_quote']]
            source_texts = []
            for source in sources:
                source_texts.append(normalize_evidence(' '.join(pages[(source, n)].text for n in numbers)))
            if not any(all(normalize_evidence(q) in text for q in quotes) for text in source_texts):
                raise ValueError(f"Gold evidence absent from PDF: {question['id']}")
        filters = question.get('filter')
        if filters:
            if set(filters) != {'metadata'} or set(filters['metadata']) != {'chapter'}:
                raise ValueError('Official benchmark only permits explicit chapter filters')
            if f"Chương {filters['metadata']['chapter']}" not in question['question']:
                raise ValueError('Chapter filter must be supplied explicitly in the question')
    return questions


def make_embedder():
    from .embeddings import MyEmbedder
    embedder = MyEmbedder(MODEL, revision=REVISION)
    if embedder.dimensions != 384:
        raise ValueError('Official model must produce 384 dimensions')
    return embedder


def ingest(store, embedder, chunks, output):
    stats = {}
    for strategy, items in chunks.items():
        started = time.perf_counter()
        vectors = embedder.embed_documents([c.text for c in items])
        store.upsert(strategy, items, vectors)
        elapsed = time.perf_counter() - started
        lengths = sorted(len(c.text) for c in items)
        stats[strategy] = {'chunks': len(items), 'characters': sum(lengths),
                           'min_characters': min(lengths), 'max_characters': max(lengths),
                           'mean_characters': sum(lengths)/len(lengths),
                           'median_characters': lengths[len(lengths)//2],
                           'ingest_seconds': elapsed, 'paid_api_cost': 0,
                           'cost_note': 'Local inference; electricity/hardware cost not measured'}
        save(output / (strategy + '_chunks.json'), [asdict(c) for c in items])
        print(f'{strategy}: {len(items)} chunks, {elapsed:.2f}s', flush=True)
    save(output / 'ingest_summary.json', stats)


def validate_index(store, chunks):
    with psycopg.connect(store.database_url) as conn:
        for strategy, expected in chunks.items():
            stored = conn.execute('SELECT chunk_id,text,metadata FROM lab_chunks WHERE strategy=%s', (strategy,)).fetchall()
            lookup = {r[0]: r for r in stored}
            if set(lookup) != {c.chunk_id for c in expected}:
                raise ValueError('Index IDs differ from corpus; run ingest before eval/verify')
            for chunk in expected:
                _, text, metadata = lookup[chunk.chunk_id]
                if text != chunk.text or any(metadata.get(k) != chunk.metadata[k] for k in ('snapshot_sha256','embedding_model','embedding_revision','chapter')):
                    raise ValueError('Index text/provenance/metadata differ from corpus; run ingest')


def evaluate(store, embedder, questions, split, output):
    for subset in (['dev', 'test'] if split == 'both' else [split]):
        traces = []
        started = time.perf_counter()
        for question in [q for q in questions if q['split'] == subset]:
            vector = embedder.embed_query(question['question'])
            for config, strategy in CONFIGS.items():
                filters = question.get('filter') if config == 'C' else None
                hits = store.search(strategy, vector, top_k=3, filters=filters)
                trace = evaluate_query({**question, 'strategy': config}, hits)
                trace.update({'filter': filters, 'requested_filter': question.get('filter'),
                              'applied_filter': filters, 'storage_strategy': strategy})
                traces.append(trace)
        save(output / f'{subset}_traces.json', traces)
        save(output / f'{subset}_summary.json', summarize(traces))
        save(output / f'{subset}_runtime.json', {'seconds': time.perf_counter()-started})
        print(f'{subset}: {len(traces)} traces', flush=True)


def report(output):
    merged = []
    for subset in ('dev', 'test'):
        path = output / f'{subset}_traces.json'
        if path.exists():
            for old in read(path):
                question = {key: old[key] for key in ('id', 'split', 'strategy', 'question', 'expected_answer', 'gold_evidence')}
                question['filter'] = old.get('applied_filter', old.get('filter'))
                merged.append(evaluate_query(question, old['hits']))
    if not merged:
        raise ValueError('No traces in output directory; run eval first')
    save(output / 'retrieval_summary.json', summarize(merged))
    lines = ['# Retrieval report', '', 'Recomputed from saved top-3; does not assign manual scores.', '',
             '| Config | Split | Hit@1 | Evidence Hit@3 |', '|---|---|---|---|']
    for strategy, splits in summarize(merged).items():
        for subset, metrics in splits.items():
            total = metrics['total_questions']
            lines.append(f"| {strategy} | {subset} | {metrics['hit_at_1_count']}/{total} | {metrics['evidence_hit_at_3_count']}/{total} |")
    (output / 'retrieval_report.md').write_text('\n'.join(lines)+'\n')


def main():
    parser = argparse.ArgumentParser(description='Day 06: real E5 + pgvector, official A/B/C')
    parser.add_argument('command', nargs='?', default='all', choices=['ingest', 'eval', 'report', 'verify', 'all'])
    parser.add_argument('--manifest', type=Path, default=ROOT / 'data/manifest.json')
    parser.add_argument('--questions', type=Path, default=STARTER / 'data/benchmark_questions.json')
    parser.add_argument('--output', type=Path, default=STARTER / 'results/reproduced')
    parser.add_argument('--split', choices=['dev', 'test', 'both'], default='both')
    args = parser.parse_args()
    args.output = args.output.resolve()
    baseline = (STARTER / 'results').resolve()
    if args.output == baseline:
        parser.error('Use a separate output directory to preserve baseline files')
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    try:
        if args.command == 'report':
            report(args.output)
            return
        documents = load_corpus(args.manifest, args.output)
        questions = load_questions(args.questions, documents)
        store = PgVectorStore(database_url(), 384)
        store.create_schema()
        chunks = build_chunks(documents)
        embedder = make_embedder()
        if args.command in ('ingest', 'all'):
            ingest(store, embedder, chunks, args.output)
        validate_index(store, chunks)
        if args.command in ('verify', 'all'):
            from .verification import verify
            save(args.output / 'engineering_verification.json', verify(store, embedder, chunks))
        if args.command in ('eval', 'all'):
            evaluate(store, embedder, questions, args.split, args.output)
            report(args.output)
        with psycopg.connect(store.database_url, connect_timeout=5) as conn:
            versions = conn.execute("SELECT current_setting('server_version'), extversion FROM pg_extension WHERE extname='vector'").fetchone()
        save(args.output / f'{args.command}_run.json', {
            'recorded_at': timestamp(), 'command': args.command, 'model': MODEL,
            'revision': REVISION, 'dimensions': 384, 'metric': 'cosine', 'search': 'exact SQL scan',
            'postgresql': versions[0], 'pgvector': versions[1], 'python': platform.python_version(),
            'packages': {n: importlib.metadata.version(n) for n in ['sentence-transformers','transformers','torch','psycopg','pypdf','python-dotenv','numpy']},
            'device': str(embedder.model.device), 'max_sequence_length': embedder.model.max_seq_length,
            'elapsed_seconds': time.perf_counter()-started,
            'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
            'secrets': 'Environment values intentionally excluded'})
    except Exception as exc:
        detail = str(exc) if isinstance(exc, ValueError) else 'Check input files, model cache and local database; credentials excluded.'
        save(args.output / 'error.json', {'recorded_at': timestamp(), 'command': args.command,
             'error_type': type(exc).__name__, 'message': detail})
        print(f'ERROR ({type(exc).__name__}): {detail} See error.json. No mock fallback.', file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == '__main__':
    main()
