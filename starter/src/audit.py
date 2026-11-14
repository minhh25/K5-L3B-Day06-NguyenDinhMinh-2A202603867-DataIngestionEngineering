from collections import Counter
import csv
import hashlib
import re
from itertools import chain

from .evaluation import normalize_evidence
from .run import ROOT, STARTER, build_chunks, load_corpus, read, save, timestamp

RESULTS = STARTER / 'results'
NOTICE = 'Nhãn AI đề xuất — CHƯA phải chấm thủ công bởi người học. Chỉ đánh giá evidence retrieval, không phải độ chính xác câu trả lời LLM.'


def applied_filter(trace):
    return trace.get('applied_filter', trace.get('filter') if trace['strategy'] == 'C' else None)


def display_text(text):
    return '\n'.join(line.rstrip() for line in text.splitlines())


def human_reviewed(row):
    return (row.get('human_score') or '').strip() in ('0', '1', '2') and all(
        (row.get(key) or '').strip() for key in ('human_reason', 'reviewer', 'reviewed_at'))


def metadata_confirmation(path, expected_records=45):
    text = path.read_text() if path.exists() else ''
    def field(label):
        match = re.search(rf'^{label}:[ \t]*([^\n]*)$', text, re.MULTILINE)
        return match.group(1).strip() if match else ''
    status = field('Trạng thái').split('.')[0].strip()
    signed = bool(field('Người duyệt') and field('Ngày duyệt'))
    checked = bool(re.search(rf'^Đã đối chiếu {expected_records} bản ghi với trang PDF:\s*\[[xX]\]\s*$', text, re.MULTILINE))
    confirmed = status == 'ĐÃ DUYỆT' and signed and checked
    return {'confirmed': confirmed, 'reviewed_records': expected_records if confirmed else 0,
            'expected_records': expected_records, 'signed': signed, 'all_records_checked': checked,
            'status': status or 'CHƯA DUYỆT'}


def read_review_rows(path, keys):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        header = next((line for line in handle if line.strip()), '')
        reader = csv.DictReader(chain([header], handle))
        fields = [name.strip() for name in (reader.fieldnames or [])]
        required = set(keys) | {'ai_score','ai_reason','human_score','human_reason','reviewer','reviewed_at'}
        missing = required - set(fields)
        if missing:
            raise ValueError(f'{path.name}: missing review columns: {sorted(missing)}')
        if len(fields) != len(set(fields)):
            raise ValueError(f'{path.name}: duplicate CSV columns')
        reader.fieldnames = fields
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path.name}: invalid CSV column count near record {len(rows)+1}; check quotes and formatting')
            rows.append(row)
    return rows


def reviews(path, keys):
    rows = read_review_rows(path, keys)
    result = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        if key in result:
            raise ValueError(f'Duplicate review key: {key}')
        if row['ai_score'] not in ('0','1','2'):
            raise ValueError('AI score must be 0/1/2')
        if row['human_score']:
            if row['human_score'] not in ('0','1','2') or not all(row[k].strip() for k in ('human_reason','reviewer','reviewed_at')):
                raise ValueError('Human scores require reason, reviewer and reviewed_at')
        result[key] = row
    return result


def score_summary(rows):
    output = {}
    for config in 'ABC':
        selected = [r for r in rows if r['config'] == config]
        ai = Counter(int(r['ai_score']) for r in selected)
        human = [int(r['human_score']) for r in selected if human_reviewed(r)]
        output[config] = {'n':len(selected), 'ai_counts':{str(n):ai[n] for n in range(3)},
                          'ai_assessed':sum(bool(r.get('ai_reviewer') and r.get('ai_reviewed_at') and r.get('ai_reason')) for r in selected),
                          'ai_mean':sum(int(r['ai_score']) for r in selected)/len(selected) if selected else None,
                          'human_reviewed':len(human), 'human_mean':sum(human)/len(human) if human else None,
                          'human_counts': {str(n): human.count(n) for n in range(3)}}
    return output


def human_report_section(grounding, coherence, metadata):
    lines = ['<!-- HUMAN_REVIEW_START -->',
             'Điểm người học dưới đây chỉ lấy từ human_score 0/1/2 có đủ human_reason, reviewer và reviewed_at; không dùng điểm AI thay thế. Trung bình chỉ tính trên các nhãn đã duyệt, chưa phải trung bình đủ mẫu nếu còn thiếu.', '',
             '| Config | Grounding đã duyệt | Human 0 / 1 / 2 | Grounding human /2 | Coherence đã duyệt | Coherence human /2 |',
             '|---|---|---|---|---|---|']
    for config in 'ABC':
        g, c = grounding[config], coherence[config]
        counts = ' / '.join(str(g['human_counts'][str(i)]) for i in range(3)) if g['human_reviewed'] else 'CHƯA CÓ NHÃN'
        gm = f"{g['human_mean']:.2f}" if g['human_mean'] is not None else 'N/A'
        cm = f"{c['human_mean']:.2f}" if c['human_mean'] is not None else 'N/A'
        lines.append(f"| {config} | {g['human_reviewed']}/{g['n']} | {counts} | {gm} | {c['human_reviewed']}/{c['n']} | {cm} |")
    lines += ['', f"Metadata được người học xác nhận: {metadata['reviewed_records']}/{metadata['expected_records']} bản ghi; trạng thái {'ĐÃ DUYỆT' if metadata['confirmed'] else 'CHƯA HOÀN TẤT'}. Phiếu metadata xác nhận trọn bộ; chỉ đổi trạng thái không đủ nếu thiếu tên, ngày hoặc checkbox.",
              '<!-- HUMAN_REVIEW_END -->']
    return '\n'.join(lines)


def assessment_report(summary):
    retrieval = {split: read(RESULTS/f'{split}_summary.json') for split in ('dev','test')}
    ingest = read(RESULTS/'reproduced/ingest_summary.json')
    coverage = {kind: sum(s['ai_assessed'] for s in summary[kind].values()) for kind in ('grounding','coherence','metadata')}
    save(RESULTS/'ai_assessment_summary.json', {'label':'AI-assessed; not human-confirmed',
         'coverage':coverage, 'grounding':summary['grounding'], 'coherence':summary['coherence'],
         'metadata':summary['metadata'], 'retrieval':retrieval, 'data_strategy':ingest,
         'test_trace_sha256':summary['trace_sha256'],
         'review_csv_sha256':{name:hashlib.sha256((RESULTS/name).read_bytes()).hexdigest() for name in ('grounding_review.csv','coherence_review.csv','metadata_ai_review.csv')}})
    lines = ['# Năm dimensions — AI assessment hoàn chỉnh', '', NOTICE, '',
             f"Đã đánh giá AI: grounding {coverage['grounding']}/15, coherence {coverage['coherence']}/30, metadata {coverage['metadata']}/45. Không tạo human review hay chữ ký. Giữ nguyên nguồn/gold và retrieval baseline.", '',
             '| Config | Retrieval DEV Hit@1 / Evidence Hit@3 | Retrieval TEST Hit@1 / Evidence Hit@3 | Coherence AI /2 | Metadata correctness / completeness | Grounding AI /2 | Data strategy impact |',
             '|---|---|---|---|---|---|---|']
    for config in 'ABC':
        def metric(split):
            s = retrieval[split][config][split]
            return f"{s['hit_at_1_count']}/{s['total_questions']} / {s['evidence_hit_at_3_count']}/{s['total_questions']}"
        meta = summary['metadata'][config]
        stat = ingest['fixed_800_100' if config=='A' else 'paragraph_800']
        impact = f"{stat['chunks']} chunks; {stat['ingest_seconds']:.3f}s ingest warm" if config!='C' else 'Dùng chung 309 chunks B; không ingest thêm'
        lines.append(f"| {config} | {metric('dev')} | {metric('test')} | {summary['coherence'][config]['ai_mean']:.2f} | {meta['correctness_count']}/{meta['records']} / {meta['completeness_count']}/{meta['records']} | {summary['grounding'][config]['ai_mean']:.2f} | {impact} |")
    lines += ['', 'C filter compliance TEST: 3/3 records, 1/1 câu; DEV: 2/2 câu. A/B không áp dụng filter nên NOT_APPLICABLE. Metadata đúng không có nghĩa là chunk liên quan hoặc trả lời đủ câu hỏi.', '',
              'A–B: DEV Evidence Hit@3 bằng nhau nhưng A Hit@1 cao hơn 2/15, B giữ đủ Q16 và mất exact gold ở Q19. B–C: filter đổi một phần Top-3 Q06, aggregate không tăng; chương đúng vẫn có thể thiếu evidence Q11. Coherence mẫu đầu corpus đều 1/2 do ranh giới đứt câu/điều kiện; không đại diện cả tài liệu.', '',
              'Grounding AI A=0/1/4 trường hợp điểm 0/1/2; B/C=0/0/5. Q19 B/C đủ ý khi đọc Top-3 chung nhưng Evidence Hit@3 vẫn 0. Tập TEST 5 câu nhỏ và đã được xem; không nhận là holdout mới hoặc chất lượng trả lời LLM.', '',
              'Thời gian và dữ liệu tài nguyên lấy từ lượt reproduced đã lưu, không thay bằng thời gian mới. Chi phí API 0, chưa đo điện/phần cứng. Chi tiết từng nhãn: grounding_review.csv, coherence_review.csv, metadata_ai_review.csv. Phương pháp: verification/ai_assessment_method.json.']
    (RESULTS/'ai_assessment_summary.md').write_text('\n'.join(lines)+'\n')


def summary_table(summary):
    lines = ['| Config | n | AI số điểm 0 / 1 / 2 | AI trung bình /2 | Người học duyệt |',
             '|---|---|---|---|---|']
    for config, row in summary.items():
        counts = ' / '.join(str(row['ai_counts'][str(i)]) for i in range(3))
        lines.append(f"| {config} | {row['n']} | {counts} | {row['ai_mean']:.2f} | {row['human_reviewed']}/{row['n']} |")
    return lines


def render_grounding(traces, labels):
    expected = {(t['id'],t['strategy']) for t in traces}
    if set(labels) != expected or len(expected) != 15:
        raise ValueError('Grounding review must cover exactly 5 TEST questions × 3 configs')
    lines = ['# Grounding quality — 5 TEST × 3 cấu hình', '', NOTICE, '',
             'Bản Markdown bỏ khoảng trắng cuối dòng để trình bày; text gốc đầy đủ được giữ trong traces JSON.', '',
             'Thang điểm: 0 không có bằng chứng; 1 thiếu điều kiện/ngữ cảnh; 2 đủ để trả lời và truy nguồn.',
             'Đã đọc cả ba chunk mỗi trường hợp. Điểm dựa trên ý nghĩa và ngữ cảnh, không quy đổi từ hit tự động. Có thể dùng hai chunk trong grounding nếu liên kết đủ rõ; không dùng cách đó để nâng Evidence Hit@3.', '',
             'Sửa `grounding_review.csv`: điền human_score, human_reason, reviewer, reviewed_at rồi chạy `python -m src.audit`. Nhãn AI được giữ riêng. Bản phiếu ban đầu: `verification/manual_grounding_original.md`.', '']
    lines += summary_table(score_summary(labels.values()))
    for trace in traces:
        row = labels[(trace['id'],trace['strategy'])]
        lines += ['', f"## {trace['id']} — Config {trace['strategy']}", '',
                  f"Câu hỏi: {trace['question']}", '', f"Đáp án tham chiếu: {trace['expected_answer']}", '',
                  f"Gold: `{trace['gold_evidence']}`", '', f"Filter thực tế trong trace: `{applied_filter(trace)}`", '',
                  f"**AI đề xuất: {row['ai_score']}/2.** {row['ai_reason']}", '',
                  f"AI reviewer: {row.get('ai_reviewer', 'chưa ghi nhận')}; thời điểm AI: {row.get('ai_reviewed_at', 'chưa ghi nhận')}.", '',
                  f"Người học: {row['human_score'] or 'CHƯA DUYỆT'}. {row['human_reason']}"]
        for hit in trace['hits']:
            lines += ['',f"### Top {hit['rank']} — `{hit['chunk_id']}`", '',
                      f"Nguồn: `{hit['source']}`; document_id: `{hit['document_id']}`; trang PDF: {hit['page']}.", '',
                      '```text', display_text(hit['text']), '```']
    (RESULTS/'manual_grounding.md').write_text('\n'.join(lines)+'\n')


def render_coherence(selected, labels):
    if set(labels) != {(r['sample_id'],r['config']) for r in selected} or len(labels) != 30:
        raise ValueError('Coherence requires same 10 source positions × 3 configs')
    lines = ['# Chunk coherence — cùng 10 vị trí nguồn', '', NOTICE, '',
             'Bản Markdown bỏ khoảng trắng cuối dòng để trình bày; text gốc đầy đủ được giữ trong snapshot JSON.', '',
             read(RESULTS/'coherence_positions.json')['selection_rule'], '',
             'Chấm toàn chunk riêng lẻ, không ghép chunk lân cận. 0: không hiểu vì đứt ý/chủ thể; 1: hiểu một phần nhưng thiếu ngữ cảnh; 2: tự hiểu và giữ trọn ý. Không dùng cosine. B=C vì cùng chunk/embedding; filter chỉ ảnh hưởng retrieval.', '',
             'Mẫu đầu corpus và offset giữa trang thiên về các đoạn bị cắt; không đại diện mọi chương. Tất cả 10 mẫu còn ý đọc được nhưng thiếu đầu/cuối hoặc điều kiện, nên đề xuất mức 1; không suy ra hai chiến lược tương đương trên toàn bộ corpus.', '',
             'Duyệt/sửa trong `coherence_review.csv`, điền human_score/human_reason/reviewer/reviewed_at rồi chạy `python -m src.audit`.', '']
    lines += summary_table(score_summary(labels.values()))
    for item in selected:
        row = labels[(item['sample_id'],item['config'])]
        lines += ['',f"## {item['sample_id']} — Config {item['config']}", '',
                  f"`{item['chunk_id']}` — `{item['document_id']}` — `{item['source']}` — trang PDF {item['page']}; anchor {item['anchor_char']}; chunk [{item['metadata']['start_char']}, {item['metadata']['end_char']}).", '',
                  f"**AI đề xuất: {row['ai_score']}/2.** {row['ai_reason']}", '',
                  f"AI reviewer: {row.get('ai_reviewer', 'chưa ghi nhận')}; thời điểm AI: {row.get('ai_reviewed_at', 'chưa ghi nhận')}.", '',
                  f"Người học: {row['human_score'] or 'CHƯA DUYỆT'}. {row['human_reason']}", '',
                  '```text', display_text(item['text']), '```']
    (RESULTS/'chunk_coherence.md').write_text('\n'.join(lines)+'\n')


def metadata_audit(traces, documents, chunks):
    pages = {(p.document_id,p.page):p for _, doc in documents for p in doc}
    lookup = {c.chunk_id:c for items in chunks.values() for c in items}
    rows = []
    filtered = []
    reviewed_at = timestamp()
    for trace in traces:
        filters = applied_filter(trace)
        expected_filter = trace.get('requested_filter', trace.get('filter')) if trace['strategy'] == 'C' else None
        filter_contract_ok = filters == expected_filter
        compliance = []
        for hit in trace['hits']:
            page = pages.get((hit.get('document_id'),hit.get('page')))
            source_ok = bool(page and hit.get('source') == page.source)
            text_ok = bool(page and normalize_evidence(hit['text']) in normalize_evidence(page.text))
            chunk = lookup.get(hit['chunk_id'])
            chapter = hit.get('metadata',{}).get('chapter')
            chapter_correct = bool(chunk and chapter == chunk.metadata['chapter']) if chapter is not None else None
            filter_ok = all(hit.get('metadata',{}).get(k) == v for k,v in (filters or {}).get('metadata',{}).items()) if filters else None
            base_ok = bool(page and source_ok and text_ok and hit.get('document_id'))
            required_ok = base_ok and (filter_ok is not False) and (chapter_correct is not False)
            complete = all(isinstance(hit.get(k), str) and hit[k].strip() for k in ('document_id','source')) and type(hit.get('page')) is int and hit['page'] > 0
            if expected_filter:
                complete = complete and all(hit.get('metadata',{}).get(k) is not None for k in expected_filter['metadata'])
            status = lambda value: 'PASS' if value else 'FAIL'
            row = {'question_id':trace['id'],'config':trace['strategy'],'rank':hit['rank'],
                   'chunk_id':hit['chunk_id'],'document_id':hit.get('document_id'),
                   'source':hit.get('source'),'page':hit.get('page'),'chapter_in_trace':chapter,
                   'chapter_from_pdf_boundaries':chunk.metadata['chapter'] if chunk else None,
                   'source_correct':source_ok,'page_text_correct':text_ok,'base_complete_and_correct':base_ok,
                   'chapter_correct_if_present':chapter_correct,'filter_compliant':filter_ok,
                   'required_complete_and_correct':required_ok,
                   'document_id_status':status(page is not None), 'source_status':status(source_ok),
                   'pdf_page_status':status(text_ok), 'traceability_status':status(base_ok),
                   'chapter_status':status(chapter_correct) if chapter is not None else ('FAIL' if expected_filter else 'NOT_APPLICABLE'),
                   'completeness_status':status(complete),
                   'correctness_status':status(base_ok and chapter_correct is not False),
                   'filter_contract_status':status(filter_contract_ok),
                   'filter_compliance_status':status(filter_ok) if expected_filter else 'NOT_APPLICABLE',
                   'status':status(required_ok and complete and filter_contract_ok),
                   'ai_reviewer':'Codex AI — đối chiếu từng record với PDF, không phải human reviewer',
                   'ai_reviewed_at':reviewed_at,
                   'notes':(f"Đối chiếu {hit['chunk_id']} với {hit.get('source')}, trang PDF {hit.get('page')}: document_id/source/page và vị trí text được kiểm tra trực tiếp trên pypdf; "
                            + ('chapter không có trong baseline A, không bắt buộc vì không lọc. ' if chapter is None else f"chapter={chapter} được đối chiếu ranh giới heading trong PDF, không suy từ gold. ")
                            + (f'Filter chapter được áp dụng theo input câu hỏi: {filters}; kiểm tra giá trị trên chính hit. ' if expected_filter else 'Câu/config này không áp dụng filter: compliance NOT_APPLICABLE, không mặc định 100%. ')
                            + ('Chunk trang 23 thuộc Chương II là metadata đúng dù không trả lời câu về học sinh; metadata correctness không phải relevance.' if trace['id']=='Q18' and hit['page']==23 else 'Không dùng cosine hay retrieval hit để xác nhận metadata.'))}
            rows.append(row)
            compliance.append(filter_ok is True and filter_contract_ok)
        if expected_filter:
            filtered.append({'question_id':trace['id'],'config':trace['strategy'],
                             'filter':expected_filter,'returned':len(compliance),
                             'all_top3_compliant':len(compliance)==3 and all(compliance)})
    summary = {}
    for config in 'ABC':
        selected = [r for r in rows if r['config']==config]
        applied = [r for r in filtered if r['config']==config]
        summary[config] = {'records':len(selected),'base_correct':sum(r['base_complete_and_correct'] for r in selected),
                           'required_correct':sum(r['required_complete_and_correct'] for r in selected),
                           'ai_assessed':len(selected),
                           'correctness_count':sum(r['correctness_status']=='PASS' for r in selected),
                           'completeness_count':sum(r['completeness_status']=='PASS' for r in selected),
                           'record_pass_count':sum(r['status']=='PASS' for r in selected),
                           'filter_applicable_records':sum(r['filter_compliance_status']!='NOT_APPLICABLE' for r in selected),
                           'filter_compliant_records':sum(r['filter_compliance_status']=='PASS' for r in selected),
                           'chapter_present':sum(r['chapter_in_trace'] is not None for r in selected),
                           'filtered_questions':len(applied),'filter_compliant_questions':sum(r['all_top3_compliant'] for r in applied)}
    result = {'method':'AI-assisted review + deterministic document_id/source/page/text and chapter-boundary checks of baseline TEST top-3. Learner confirmation is recorded separately in metadata_human_review.md and audit_summary.json.',
              'summary':summary,'records':rows,'filtered_questions':filtered}
    save(RESULTS/'metadata_audit.json',result)
    with (RESULTS/'metadata_ai_review.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ['question_id','config','rank','chunk_id','status'], lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    lines = ['# Metadata usefulness — TEST Top-3', '', NOTICE, '',
             'Nguồn chấm: `test_traces.json` baseline; kiểm tra 45 bản ghi (15 mỗi config). Mỗi dòng đối chiếu document_id, tên PDF, trang vật lý và nội dung chunk với PDF; chapter có trong trace được đối chiếu ranh giới heading, không gán lại metadata vào trace gốc.', '',
             '| Config | Correctness | Completeness (trường bắt buộc) | Chapter có giá trị | Filter records | Filter questions |',
             '|---|---|---|---|---|---|']
    for config, s in summary.items():
        fc=f"{s['filter_compliant_questions']}/{s['filtered_questions']}" if s['filtered_questions'] else 'N/A — không áp dụng filter'
        fr = f"{s['filter_compliant_records']}/{s['filter_applicable_records']}" if s['filter_applicable_records'] else 'NOT_APPLICABLE'
        lines.append(f"| {config} | {s['correctness_count']}/{s['records']} | {s['completeness_count']}/{s['records']} | {s['chapter_present']}/{s['records']} | {fr} | {fc} |")
    lines += ['', 'C có một câu TEST dùng filter: Q17, chapter=IV được nêu ngay trong câu hỏi. Ba chunk đều chapter IV. Đây là filter compliance, không phải retrieval accuracy: đúng chương không bảo đảm có đủ evidence. A/B không áp dụng filter theo contract, nên compliance là N/A. Trong DEV có Q06 (II), Q11 (III); xem `verification/filter_validation.json`.', '',
              'document_id gắn với source_id trong manifest; source + page dẫn tới trang vật lý 1-based, khác số in Công báo (ví dụ PDF trang 52 in trang 53). Chapter giới hạn vùng tìm kiếm. Một corpus một PDF và 5 TEST cùng Chương IV hạn chế khả năng chứng minh lợi ích lọc; B/C bằng nhau trên aggregate.', '',
              'Baseline Paragraph: 247 chapter có giá trị / 62 null. Khi tái tạo thận trọng: 246 / 63 null; p1_paragraph_800_0 có phần lời mở đầu trước Chương I nên để null thay vì gán cả chunk vào I. Header Công báo riêng và chunk trộn chương giữ null, danh sách chapters mô tả các chương thật. Không tự gán chương toàn trang tại trang 5/40/61/62. Không đổi text, ID, benchmark hoặc baseline.', '',
              'Bảng sau là kiểm chứng máy hỗ trợ AI, cần học viên đối chiếu PDF. Muốn sửa nhận xét, lưu ý kiến trong `metadata_human_review.md` (không tự đổi trường máy đo).', '',
              'Đã AI-assess 45/45 record. PASS/FAIL đánh giá giá trị và trường cần thiết; NOT_APPLICABLE dùng cho chapter tùy chọn không có hoặc filter không áp dụng. Correctness đối chiếu giá trị với nguồn; completeness chỉ đo sự có mặt của trường bắt buộc. Không có lỗi trong mẫu này không chứng minh mọi chunk trong database đều đúng.', '',
              '| Câu | Config | Rank | Chunk | PDF page | Chapter trace | Correctness | Completeness | Filter |',
              '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['question_id']} | {r['config']} | {r['rank']} | `{r['chunk_id']}` | {r['page']} | {r['chapter_in_trace']} | {r['correctness_status']} | {r['completeness_status']} | {r['filter_compliance_status']} |")
    lines += ['', '## Nhận định từng record của AI', '']
    for r in rows:
        lines += [f"- {r['question_id']}/{r['config']}/Top-{r['rank']} — **{r['status']}**: {r['notes']}"]
    (RESULTS/'metadata_usefulness.md').write_text('\n'.join(lines)+'\n')
    return summary


def main():
    documents=load_corpus(ROOT/'data/manifest.json',RESULTS/'verification')
    chunks=build_chunks(documents)
    traces=read(RESULTS/'test_traces.json')
    grounding=reviews(RESULTS/'grounding_review.csv',('question_id','config'))
    coherence=reviews(RESULTS/'coherence_review.csv',('sample_id','config'))
    selected=read(RESULTS/'verification/coherence_selected_chunks.json')
    render_grounding(traces,grounding)
    render_coherence(selected,coherence)
    metadata=metadata_audit(traces,documents,chunks)
    gs, cs = score_summary(grounding.values()), score_summary(coherence.values())
    confirmation = metadata_confirmation(RESULTS/'metadata_human_review.md')
    summary = {'status':NOTICE,'trace_sha256':hashlib.sha256((RESULTS/'test_traces.json').read_bytes()).hexdigest(),
               'grounding':gs,'coherence':cs,'metadata':metadata,'metadata_human_confirmation':confirmation}
    save(RESULTS/'audit_summary.json', summary)
    assessment_report(summary)
    report_path = ROOT/'report/individual/2A202603867_NguyenDinhMinh.md'
    report_text = report_path.read_text()
    pattern = r'<!-- HUMAN_REVIEW_START -->.*?<!-- HUMAN_REVIEW_END -->'
    if re.search(pattern, report_text, re.DOTALL):
        report_path.write_text(re.sub(pattern, lambda _: human_report_section(gs, cs, confirmation), report_text, flags=re.DOTALL))
    print('Rendered 15 grounding reviews, 30 coherence reviews and 45 metadata records; human scores remain separate.')


if __name__ == '__main__': main()
