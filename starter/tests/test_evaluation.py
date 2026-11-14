import unittest

from src.evaluation import evaluate_query, summarize


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.q = {'id':'Q', 'split':'dev', 'question':'What?', 'strategy':'A',
                  'gold_source_id':'doc', 'gold_page':2, 'evidence_quote':'đủ bằng chứng'}
        self.hit = {'chunk_id':'c', 'document_id':'doc', 'source':'doc.pdf', 'page':2,
                    'text':'ĐỦ\n bằng   chứng', 'metadata':{}}

    def score(self, hits):
        return evaluate_query(self.q, hits)

    def test_normalized_full_evidence(self):
        self.assertEqual(self.score([self.hit])['hit_at_1'], 1)

    def test_wrong_source_or_page(self):
        for changes in ({'document_id':'other'}, {'page':3}):
            self.assertEqual(self.score([{**self.hit, **changes}])['evidence_hit_at_3'], 0)

    def test_right_page_without_full_evidence(self):
        self.assertEqual(self.score([{**self.hit,'text':'đủ bằng'}])['hit_at_1'], 0)

    def test_split_evidence_not_joined(self):
        hits = [{**self.hit,'text':'đủ bằng'}, {**self.hit,'text':'chứng'}]
        self.assertEqual(self.score(hits)['evidence_hit_at_3'], 0)

    def test_rank_two_and_top_three_limit(self):
        wrong = {**self.hit, 'text':'irrelevant'}
        trace = self.score([wrong,self.hit])
        self.assertEqual((trace['hit_at_1'],trace['evidence_hit_at_3']), (0,1))
        self.assertEqual(self.score([wrong]*3+[self.hit])['evidence_hit_at_3'], 0)

    def test_alternative_gold_without_legacy_fields(self):
        self.q = {k:v for k,v in self.q.items() if not k.startswith('gold_') and k!='evidence_quote'}
        self.q['gold_evidence'] = [
            {'gold_source_id':'other','gold_page':8,'evidence_quote':'alternative'},
            {'gold_source_id':'doc','gold_page':2,'evidence_quote':'đủ bằng chứng'}]
        self.assertEqual(self.score([self.hit])['hit_at_1'], 1)

    def test_all_quotes_required_in_one_alternative(self):
        self.q['evidence_quote'] = ['đủ bằng', 'điều kiện']
        self.assertEqual(self.score([self.hit])['hit_at_1'], 0)
        self.hit['text'] += ' điều kiện'
        self.assertEqual(self.score([self.hit])['hit_at_1'], 1)

    def test_multi_page_chunk(self):
        self.q['gold_page'] = [2,3]
        self.hit.update(page=1, metadata={'page_start':1,'page_end':3})
        self.assertEqual(self.score([self.hit])['hit_at_1'], 1)
        self.hit['metadata']['page_end'] = 2
        self.assertEqual(self.score([self.hit])['hit_at_1'], 0)

    def test_invalid_gold_is_not_a_hit(self):
        for gold in ('', [], [''], [None]):
            self.q['evidence_quote'] = gold
            with self.assertRaises(ValueError): self.score([self.hit])

    def test_summary_split_and_config(self):
        a = self.score([self.hit])
        b = {**a,'split':'test','strategy':'B'}
        summary = summarize([a,b])
        self.assertEqual(summary['A']['dev']['hit_at_1_count'], 1)
        self.assertNotIn('test',summary['A'])
        self.assertEqual(summarize([]), {})


if __name__ == '__main__': unittest.main()
