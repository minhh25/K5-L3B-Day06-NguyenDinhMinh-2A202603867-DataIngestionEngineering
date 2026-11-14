import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.audit import human_report_section, human_reviewed, metadata_confirmation, read_review_rows, score_summary
from src.run import ROOT, STARTER, read, save

REPORT = 'report/individual/2A202603867_NguyenDinhMinh.md'
FORBIDDEN = {'.git', '.venv', '__MACOSX', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cache'}
SOURCE_ARTIFACTS = {'manual_grounding.md', 'chunk_coherence.md', 'manual_grounding_original.md',
                    'grounding_review.csv', 'coherence_review.csv', 'metadata_ai_review.csv'}


def review_status(path, keys, expected):
    errors, incomplete, grouped = [], [], {}
    for row in read_review_rows(path, keys):
        key = tuple((row.get(k) or '').strip() for k in keys)
        grouped.setdefault(key, []).append(row)
    rows = []
    for key, entries in grouped.items():
        if key not in expected or len(entries) != 1:
            errors.append(f'{path.name}: unexpected or duplicate key {key}')
            continue
        row = {k: (v or '').strip() for k, v in entries[0].items() if k is not None}
        if row['ai_score'] not in ('0', '1', '2'):
            errors.append(f'{path.name}: invalid AI score {key}')
            continue
        if row['human_score'] and row['human_score'] not in ('0', '1', '2'):
            errors.append(f'{path.name}: invalid human score {key}')
        if any(row[k] for k in ('human_score', 'human_reason', 'reviewer', 'reviewed_at')) and not human_reviewed(row):
            incomplete.append(list(key))
        rows.append(row)
    if set(grouped) != expected:
        errors.append(f'{path.name}: review coverage differs from source samples')
    summary = score_summary(rows)
    return {'expected': len(expected), 'human_reviewed': sum(s['human_reviewed'] for s in summary.values()),
            'summary': summary, 'incomplete_reviews': incomplete, 'errors': errors}


def student_confirmation(path):
    text = path.read_text()
    def field(label):
        match = re.search(rf'^(?:- )?{label}:[ \t]*([^\n]*)$', text, re.MULTILINE)
        return match.group(1).strip() if match else ''
    def checked(label):
        return bool(re.search(rf'^- \[[xX]\] {re.escape(label)}\s*$', text, re.MULTILINE))
    signed = bool(field('Người xác nhận') and field('Ngày xác nhận'))
    missing = [label for label in ('Họ và tên', 'MSSV', 'Lớp')
               if not field(label) or field(label).upper().startswith('CHƯA')]
    return {'confirmed': not missing,
            'missing_fields': missing, 'signed': signed,
            'repository_access_confirmed': checked('Repo truy cập được đối với người chấm.'),
            'submission_confirmed': checked('Đã nộp link repo theo kênh của lớp.'),
            'final_commit_recorded': bool(re.fullmatch(r'[0-9a-fA-F]{7,40}', field('Commit chốt bài')))}


def readiness(permission_verified, reviews, metadata, student, technical_errors):
    pending = any(r['human_reviewed'] != r['expected'] or r['errors'] for r in reviews.values()) or not metadata['confirmed']
    blockers = list(technical_errors)
    for condition, reason in [
        (permission_verified, 'Data sharing permission not verified'),
        (not pending, 'Learner reviews incomplete'),
        (student['confirmed'], 'Student identity/class not confirmed'),
        (student['repository_access_confirmed'], 'Grader repository access not confirmed'),
        (student['submission_confirmed'], 'Submission not confirmed'),
        (student['final_commit_recorded'], 'Final commit not recorded')]:
        if not condition:
            blockers.append(reason)
    return {'human_review_pending': bool(pending), 'readiness_status': 'PARTIAL' if blockers else 'PASS',
            'submission_readiness': 'PARTIAL: ' + '; '.join(blockers) if blockers else 'PASS: all recorded conditions met',
            'blocking_reasons': blockers}


def forbidden_path(name):
    path = Path(name)
    return bool(FORBIDDEN.intersection(path.parts) or path.name == '.DS_Store'
                or (path.name == '.env' or path.name.startswith('.env.')) and path.name != '.env.example'
                or path.suffix in ('.pyc', '.pyo'))


def contains_source_text(value):
    if isinstance(value, dict):
        return any((key in {'text', 'evidence_quote', 'gold_quote', 'anchor_text'} and bool(item))
                   or contains_source_text(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_source_text(item) for item in value)
    return False


def commit_exclusion(name, root, permission_verified, legal_text_allowed=False):
    path = root / name
    if forbidden_path(name) or path.is_symlink():
        return 'environment, repository internals, cache or symlink'
    if name == 'data/format-example.json':
        return None
    if permission_verified:
        return None
    if path.suffix.lower() == '.pdf' or path.name == 'benchmark_source_extract.txt':
        return 'original source file redistribution not verified'
    if legal_text_allowed and (name == 'starter/data/benchmark_questions.json'
                               or name.startswith('starter/results/') and path.suffix in ('.json','.csv','.md')):
        return None
    if name.startswith('starter/data/') and path.name != '.gitkeep':
        return 'source/gold sharing permission not verified'
    if path.name in SOURCE_ARTIFACTS or path.suffix.lower() == '.pdf':
        return 'source excerpts sharing permission not verified'
    if path.suffix == '.json' and path.is_file() and contains_source_text(read(path)):
        return 'source text in JSON; sharing permission not verified'
    return None


def artifact_consistency(root, reviews, metadata):
    errors = []
    saved = read(root/'starter/results/audit_summary.json')
    coverage = {kind:sum(row['ai_assessed'] for row in saved[kind].values()) for kind in ('grounding','coherence','metadata')}
    if coverage != {'grounding':15,'coherence':30,'metadata':45}:
        errors.append('AI assessment coverage is incomplete')
    assessment = read(root/'starter/results/ai_assessment_summary.json')
    if assessment['coverage'] != coverage:
        errors.append('AI assessment summary coverage disagrees')
    for name, digest in assessment['review_csv_sha256'].items():
        if hashlib.sha256((root/'starter/results'/name).read_bytes()).hexdigest() != digest:
            errors.append(f'AI assessment CSV changed since summary: {name}')
    for kind, status in reviews.items():
        if saved[kind] != status['summary']:
            errors.append(f'audit_summary.json differs from {kind} CSV; run python -m src.audit')
    if saved.get('metadata_human_confirmation') != metadata:
        errors.append('Metadata human confirmation differs from audit_summary.json')
    if saved['metadata'] != read(root/'starter/results/metadata_audit.json')['summary']:
        errors.append('Metadata machine summaries disagree')
    metadata_rows = read(root/'starter/results/metadata_audit.json')['records']
    metadata_csv = root/'starter/results/metadata_ai_review.csv'
    if metadata_csv.exists():
        with metadata_csv.open(newline='') as handle:
            actual = list(csv.DictReader(handle))
        fields = ('question_id','config','rank','chunk_id','status','chapter_status',
                  'correctness_status','completeness_status','filter_compliance_status','ai_reviewer','ai_reviewed_at')
        if [{k:r[k] for k in fields} for r in actual] != [{k:str(r[k]) for k in fields} for r in metadata_rows]:
            errors.append('Metadata AI CSV and JSON records disagree')
    else:
        errors.append('Metadata AI CSV missing')
    report = (root/REPORT).read_text()
    block = human_report_section(reviews['grounding']['summary'], reviews['coherence']['summary'], metadata)
    if block not in report:
        errors.append('Report human-score table is stale; run python -m src.audit')
    table_rows = [[cell.strip() for cell in line.strip('|').split('|')]
                  for line in report.splitlines() if line.startswith('| ')]
    for config in 'ABC':
        g, c = reviews['grounding']['summary'][config], reviews['coherence']['summary'][config]
        counts = ' / '.join(str(g['ai_counts'][str(i)]) for i in range(3))
        expected_ai = f"{counts}; {g['ai_mean']:.2f}".replace('.', ',') if g['ai_mean'] is not None else ''
        expected_coherence = f"{c['ai_mean']:.2f} ({c['n']})".replace('.', ',') if c['ai_mean'] is not None else ''
        if not any(len(row) == 5 and row[0] == config and row[1] == expected_coherence and row[4] == expected_ai for row in table_rows):
            errors.append(f'Report AI audit table differs from CSV: {config}')
        for split in ('dev', 'test'):
            metric = read(root/f'starter/results/{split}_summary.json')[config][split]
            reproduced = read(root/f'starter/results/reproduced/{split}_summary.json')[config][split]
            if metric != reproduced:
                errors.append(f'Baseline/reproduced summaries differ: {config}/{split}')
            expected = [f"{metric[k]}/{metric['total_questions']}" for k in ('hit_at_1_count', 'evidence_hit_at_3_count')]
            if not any(len(row) == 7 and row[:2] == [config, split.upper()]
                       and all(row[i+2].split()[0] == expected[i] for i in range(2)) for row in table_rows):
                errors.append(f'Report retrieval table differs from summaries: {config}/{split}')
    return errors


def main():
    output = STARTER/'results/verification'
    output.mkdir(parents=True, exist_ok=True)
    for name in ('commit_candidates.txt', 'git_status.txt', 'submission_checks.json', 'excluded_commit_candidates.json'):
        if not (output/name).exists():
            (output/name).write_text('{}\n' if name.endswith('.json') else '')
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=ROOT)
    paths = [p for p in git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode().split('\0') if p]
    tracked = set(git('ls-files', '-z').decode().split('\0'))
    manifest = read(ROOT/'data/manifest.json')
    permission = bool(manifest['sources']) and all(s.get('permission_verified') is True for s in manifest['sources'])
    legal_text_allowed = bool(manifest['sources']) and all(
        s.get('legal_text_reuse_basis_verified') is True and s.get('rights_sources') and s.get('rights_review_path')
        for s in manifest['sources'])
    required = ['README.md', 'STUDENT.md', 'data/manifest.json', 'benchmark/README.md', REPORT,
                'artifacts/experiment_log.csv', 'starter/results/manual_grounding.md',
                'starter/results/chunk_coherence.md', 'starter/results/metadata_usefulness.md',
                'starter/results/submission_checklist.md', 'starter/results/reproduced/all_run.json',
                'starter/results/reproduced/engineering_verification.json']
    missing = [p for p in required if not (ROOT/p).exists()]
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}',
                r'\bgh[pousr]_[A-Za-z0-9]{30,}', r'\bhf_[A-Za-z0-9]{20,}', r'\bAKIA[A-Z0-9]{16}\b']
    findings, links, exclusions = [], [], {}
    text_count = 0
    for name in sorted(set(paths)):
        path = ROOT/name
        if not path.is_file():
            continue
        reason = commit_exclusion(name, ROOT, permission, legal_text_allowed)
        if reason:
            exclusions[name] = reason
        if forbidden_path(name) or path.is_symlink():
            continue
        if path.suffix.lower() not in ('.py', '.md', '.json', '.csv', '.txt', '.yml', '.sql', '.example') and path.name != '.gitignore':
            continue
        text = path.read_text()
        text_count += 1
        if any(re.search(pattern, text) for pattern in patterns):
            findings.append({'file': name, 'pattern': 'credential-like content (value excluded)'})
            exclusions[name] = 'credential-like content'
        if path.suffix == '.md':
            for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
                if re.match(r'^(?:https?://|mailto:|#)', target):
                    continue
                target = target.split('#')[0].strip('<>')
                if target and not (path.parent/target).exists():
                    links.append({'file': name, 'target': target})
    sources = {s['source_path_or_url'] for s in manifest['sources']}
    for name in sources | {'starter/data/benchmark_source_extract.txt'}:
        if (ROOT/name).exists() and not permission:
            exclusions[name] = 'source sharing permission not verified'
    expected_grounding = {(t['id'], t['strategy']) for t in read(STARTER/'results/test_traces.json')}
    expected_coherence = {(r['sample_id'], r['config']) for r in read(STARTER/'results/verification/coherence_selected_chunks.json')}
    reviews = {
        'grounding': review_status(STARTER/'results/grounding_review.csv', ('question_id', 'config'), expected_grounding),
        'coherence': review_status(STARTER/'results/coherence_review.csv', ('sample_id', 'config'), expected_coherence)}
    metadata = metadata_confirmation(STARTER/'results/metadata_human_review.md')
    consistency = artifact_consistency(ROOT, reviews, metadata)
    tracked_forbidden = sorted(name for name in tracked if name and forbidden_path(name))
    tracked_excluded = sorted(tracked.intersection(exclusions))
    errors = []
    for items, label in [(missing, 'Required files missing'), (links, 'Broken local links'),
                         (findings, 'Potential secrets found'), (tracked_excluded, 'Excluded files already tracked'),
                         (tracked_forbidden, 'Forbidden paths already tracked')]:
        if items:
            errors.append(label)
    errors += consistency + [error for review in reviews.values() for error in review['errors']]
    result = {'required_missing': missing, 'broken_local_markdown_links': links, 'secret_scan_findings': findings,
              'text_files_scanned': text_count, 'tracked_forbidden_files': tracked_forbidden,
              'tracked_excluded_files': tracked_excluded, 'permission_verified': permission,
              'selected_files_sharing_supported': permission or legal_text_allowed,
              'distribution_scope': 'Legal-text benchmark/traces/audits with attribution; original PDF and full source extract remain local.',
              'human_reviews': reviews, 'metadata_human_confirmation': metadata,
              'student_confirmation': student_confirmation(ROOT/'STUDENT.md'),
              'ai_assessment_coverage':{**{kind:sum(s['ai_assessed'] for s in review['summary'].values()) for kind,review in reviews.items()},
                                        'metadata':sum(s['ai_assessed'] for s in read(STARTER/'results/audit_summary.json')['metadata'].values())},
              'artifact_consistency_errors': consistency, 'technical_checks_passed': not errors,
              'secret_scan_scope': 'Pattern scan of nonignored candidate text files; values excluded. Original source files remain local; legal-text artifacts require the recorded scope-specific reuse basis.'}
    result.update(readiness(permission or legal_text_allowed, reviews, metadata, result['student_confirmation'], errors))
    save(output/'submission_checks.json', result)
    save(output/'excluded_commit_candidates.json', exclusions)
    (output/'git_status.txt').write_text(git('status', '--short', '--untracked-files=all').decode())
    changed = git('ls-files', '--modified', '--others', '--exclude-standard', '-z').decode().split('\0')
    candidates = sorted({name for name in changed if name and name not in exclusions and not forbidden_path(name)})
    (output/'commit_candidates.txt').write_text('\n'.join(candidates)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
