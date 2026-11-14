import csv
from pathlib import Path
import tempfile
import unittest

from scripts.check_submission import commit_exclusion, forbidden_path, readiness, review_status, student_confirmation
from src.audit import human_report_section, metadata_confirmation, reviews, score_summary


class SubmissionReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.fields = ['question_id', 'config', 'ai_score', 'ai_reason', 'human_score', 'human_reason', 'reviewer', 'reviewed_at']
        self.rows = [dict(question_id='fixture', config=c, ai_score='2', ai_reason='Fixture only',
                          human_score='', human_reason='', reviewer='', reviewed_at='') for c in 'ABC']
        self.expected = {('fixture', c) for c in 'ABC'}

    def status(self, rows):
        path = self.root/'review.csv'
        with path.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=self.fields, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        return review_status(path, ('question_id', 'config'), self.expected)

    def test_ai_scores_never_count_as_human(self):
        result = self.status(self.rows)
        self.assertEqual(result['human_reviewed'], 0)
        self.assertIsNone(result['summary']['A']['human_mean'])
        self.assertEqual(result['errors'], [])

    def test_bom_and_leading_blank_lines_work_in_both_review_readers(self):
        for key in ('question_id', 'sample_id'):
            path = self.root/f'{key}.csv'
            fields = [key if field=='question_id' else field for field in self.fields]
            row = {key:'fixture','config':'A','ai_score':'1','ai_reason':'Fixture',
                   'human_score':'0','human_reason':'Dòng một, có dấu phẩy\n\nDòng hai',
                   'reviewer':'Người kiểm thử','reviewed_at':'14/11/2026'}
            with path.open('w', encoding='utf-8-sig', newline='') as handle:
                handle.write('\r\n\r\n')
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
            self.assertEqual(reviews(path,(key,'config'))[('fixture','A')], row)
            status = review_status(path,(key,'config'),{('fixture','A')})
            self.assertEqual(status['human_reviewed'],1)
            self.assertEqual(status['errors'],[])

    def test_missing_header_column_is_reported_without_key_error(self):
        path = self.root/'missing.csv'
        path.write_text('config,ai_score\nA,1\n')
        for reader in (lambda:reviews(path,('question_id','config')),
                       lambda:review_status(path,('question_id','config'),self.expected)):
            with self.assertRaisesRegex(ValueError,'missing review columns'):
                reader()

    def test_malformed_csv_with_shifted_columns_is_rejected(self):
        path = self.root/'shifted.csv'
        path.write_text(','.join(self.fields)+'\nfixture,A,1,reason,1,reason,name,date,unexpected\n')
        for reader in (lambda:reviews(path,('question_id','config')),
                       lambda:review_status(path,('question_id','config'),self.expected)):
            with self.assertRaisesRegex(ValueError,'invalid CSV column count'):
                reader()

    def test_signed_zero_score_is_counted_without_using_ai_score(self):
        self.rows[0].update(human_score='0', human_reason='Fixture reason', reviewer='Fixture reviewer', reviewed_at='2026-11-14')
        result = self.status(self.rows)
        self.assertEqual(result['human_reviewed'], 1)
        self.assertEqual(result['summary']['A']['human_mean'], 0)
        self.assertEqual(result['summary']['A']['ai_mean'], 2)

    def test_unsigned_score_remains_pending(self):
        self.rows[0].update(human_score='2', human_reason='Draft')
        result = self.status(self.rows)
        self.assertEqual(result['human_reviewed'], 0)
        self.assertEqual(result['incomplete_reviews'], [['fixture', 'A']])

    def test_duplicate_and_missing_keys_cannot_complete_reviews(self):
        duplicated = self.status(self.rows + [self.rows[0]])
        self.assertTrue(duplicated['errors'])
        missing = self.status(self.rows[:2])
        self.assertTrue(missing['errors'])
        self.assertEqual(missing['expected'], 3)

    def test_metadata_requires_status_signature_and_all_records_checkbox(self):
        path = self.root/'metadata.md'
        path.write_text('Trạng thái: ĐÃ DUYỆT\n\nNgười duyệt:\n\nNgày duyệt:\n\nĐã đối chiếu 45 bản ghi với trang PDF: [x]\n')
        self.assertFalse(metadata_confirmation(path)['confirmed'])
        self.assertFalse(metadata_confirmation(path)['signed'])
        path.write_text('Trạng thái: ĐÃ DUYỆT\nNgười duyệt: Fixture reviewer\nNgày duyệt: 2026-11-14\nĐã đối chiếu 45 bản ghi với trang PDF: [x]\n')
        self.assertEqual(metadata_confirmation(path)['reviewed_records'], 45)
        path.write_text(path.read_text().replace('[x]', '[ ]'))
        self.assertEqual(metadata_confirmation(path)['reviewed_records'], 0)

    def test_student_class_must_be_supplied_even_with_signature(self):
        path = self.root/'STUDENT.md'
        path.write_text('- Họ và tên: Fixture name\n- MSSV: Fixture ID\n- Lớp: CHƯA CUNG CẤP\n'
                        '- Người xác nhận: Fixture reviewer\n- Ngày xác nhận: 2026-11-14\n'
                        '- [x] Tôi xác nhận họ tên, MSSV và lớp ở trên là chính xác.\n')
        self.assertFalse(student_confirmation(path)['confirmed'])
        self.assertIn('Lớp', student_confirmation(path)['missing_fields'])

    def test_complete_student_template_does_not_require_an_extra_signature(self):
        path = self.root/'STUDENT.md'
        path.write_text('- Họ và tên: Fixture name\n- MSSV: Fixture ID\n- Lớp: L3B\n')
        result = student_confirmation(path)
        self.assertTrue(result['confirmed'])
        self.assertFalse(result['signed'])
        self.assertFalse(result['repository_access_confirmed'])
        self.assertFalse(result['submission_confirmed'])

    def test_readiness_becomes_complete_only_when_all_conditions_are_recorded(self):
        reviews = {'grounding': {'human_reviewed':15, 'expected':15, 'errors':[]},
                   'coherence': {'human_reviewed':30, 'expected':30, 'errors':[]}}
        metadata = {'confirmed': True}
        student = {key: True for key in ('confirmed', 'repository_access_confirmed', 'submission_confirmed', 'final_commit_recorded')}
        result = readiness(True, reviews, metadata, student, [])
        self.assertFalse(result['human_review_pending'])
        self.assertEqual(result['readiness_status'], 'PASS')
        self.assertEqual(readiness(False, reviews, metadata, student, [])['readiness_status'], 'PARTIAL')
        for key in student:
            self.assertEqual(readiness(True, reviews, metadata, {**student, key:False}, [])['readiness_status'], 'PARTIAL')
        reviews['grounding']['human_reviewed'] = 14
        self.assertTrue(readiness(True, reviews, metadata, student, [])['human_review_pending'])

    def test_report_section_does_not_promote_ai_scores_to_human(self):
        summary = score_summary(self.rows)
        section = human_report_section(summary, summary, {'reviewed_records':0, 'expected_records':45, 'confirmed':False})
        self.assertIn('CHƯA CÓ NHÃN | N/A', section)
        self.assertIn('0/45', section)

    def test_forbidden_commit_paths(self):
        for path in ('starter/.venv/bin/python', '.env', 'starter/.env.local', '.git/config',
                     '__MACOSX/asset', 'starter/__pycache__/module.pyc', '.cache/model'):
            self.assertTrue(forbidden_path(path), path)
        self.assertFalse(forbidden_path('starter/.env.example'))
        self.assertFalse(forbidden_path('starter/src/metadata.py'))

    def test_source_and_trace_are_excluded_until_permission_is_verified(self):
        trace = self.root/'trace.json'
        trace.write_text('{"hits": [{"text": "fixture source content"}]}')
        self.assertIsNotNone(commit_exclusion('trace.json', self.root, False))
        self.assertIsNone(commit_exclusion('trace.json', self.root, True))
        self.assertIsNotNone(commit_exclusion('starter/data/source.pdf', self.root, False))
        summary = self.root/'summary.json'
        summary.write_text('{"total": 5, "has_text": true}')
        self.assertIsNone(commit_exclusion('summary.json', self.root, False))

    def test_repository_synthetic_example_does_not_require_pdf_permission(self):
        example = self.root/'data/format-example.json'
        example.parent.mkdir()
        example.write_text('{"warning": "Ví dụ giả lập", "page": {"text": "Synthetic fixture"}}')
        self.assertIsNone(commit_exclusion('data/format-example.json', self.root, False))

    def test_legal_text_scope_keeps_required_evidence_but_excludes_raw_source(self):
        self.assertIsNone(commit_exclusion('starter/data/benchmark_questions.json', self.root, False, True))
        self.assertIsNone(commit_exclusion('starter/results/dev_traces.json', self.root, False, True))
        self.assertIsNone(commit_exclusion('starter/results/grounding_review.csv', self.root, False, True))
        self.assertIsNotNone(commit_exclusion('starter/data/source.pdf', self.root, False, True))
        self.assertIsNotNone(commit_exclusion('starter/data/benchmark_source_extract.txt', self.root, False, True))
        self.assertIsNotNone(commit_exclusion('starter/.env', self.root, True, True))


if __name__ == '__main__':
    unittest.main()
