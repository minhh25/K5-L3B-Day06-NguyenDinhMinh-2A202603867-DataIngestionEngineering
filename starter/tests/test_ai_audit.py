import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.audit import metadata_audit, score_summary
from src.models import Chunk, DocumentPage


class AIAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.page = DocumentPage('fixture', 'fixture.pdf', 1, 'Chương I\nNội dung giả lập để kiểm thử.')
        self.chunk = Chunk('fixture_c', 'fixture', 'fixture.pdf', 1, self.page.text, {'chapter':'I'})
        self.hit = {'rank':1,'chunk_id':self.chunk.chunk_id, 'document_id':'fixture', 'source':'fixture.pdf',
                    'page':1, 'text':self.page.text, 'metadata':{}}

    def audit(self, trace):
        with patch('src.audit.RESULTS', self.output):
            metadata_audit([trace], [({}, [self.page])], {'fixture':[self.chunk]})
        return json.loads((self.output/'metadata_audit.json').read_text())

    def test_missing_optional_chapter_is_not_a_fake_filter_pass(self):
        result = self.audit({'id':'fixture', 'strategy':'A', 'filter':None, 'applied_filter':None, 'hits':[self.hit]})
        row = result['records'][0]
        self.assertEqual(row['completeness_status'], 'PASS')
        self.assertEqual(row['chapter_status'], 'NOT_APPLICABLE')
        self.assertEqual(row['filter_compliance_status'], 'NOT_APPLICABLE')
        self.assertEqual(result['summary']['A']['filtered_questions'], 0)

    def test_missing_required_chapter_fails_completeness_separately(self):
        filters = {'metadata':{'chapter':'I'}}
        result = self.audit({'id':'fixture','strategy':'C','filter':filters,'applied_filter':filters,'hits':[self.hit]})
        row = result['records'][0]
        self.assertEqual(row['correctness_status'], 'PASS')
        self.assertEqual(row['completeness_status'], 'FAIL')
        self.assertEqual(row['chapter_status'], 'FAIL')
        self.assertEqual(row['filter_compliance_status'], 'FAIL')
        self.assertEqual(row['status'], 'FAIL')

    def test_empty_filtered_retrieval_is_not_vacuously_compliant(self):
        filters = {'metadata':{'chapter':'I'}}
        trace = {'id':'fixture','strategy':'C','filter':filters,'applied_filter':filters,'hits':[]}
        result = self.audit(trace)
        self.assertFalse(result['filtered_questions'][0]['all_top3_compliant'])
        self.assertEqual(result['summary']['C']['filter_compliant_questions'], 0)

    def test_ai_reviewer_fields_never_count_as_human_review(self):
        rows = [{'config':c,'ai_score':'2','ai_reason':'Fixture only','ai_reviewer':'Fixture AI',
                 'ai_reviewed_at':'2026-11-14','human_score':'','human_reason':'','reviewer':'','reviewed_at':''} for c in 'ABC']
        summary = score_summary(rows)
        for config in 'ABC':
            self.assertEqual(summary[config]['ai_assessed'], 1)
            self.assertEqual(summary[config]['human_reviewed'], 0)
            self.assertIsNone(summary[config]['human_mean'])


if __name__ == '__main__':
    unittest.main()
