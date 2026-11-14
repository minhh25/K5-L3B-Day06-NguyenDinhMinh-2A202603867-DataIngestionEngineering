import hashlib
import unittest

from src.audit import applied_filter
from src.evaluation import evaluate_query, summarize
from src.run import ROOT, STARTER, read


class BaselineTests(unittest.TestCase):
    def test_frozen_inputs_unchanged(self):
        for path, digest in read(ROOT/'benchmark/baseline_lock.json').items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest, path)

    def test_recomputed_metrics_match_baseline(self):
        questions = {q['id']:q for q in read(STARTER/'data/benchmark_questions.json')}
        for split in ('dev','test'):
            traces = read(STARTER/f'results/{split}_traces.json')
            rebuilt = [evaluate_query({**questions[t['id']],'strategy':t['strategy']},t['hits']) for t in traces]
            self.assertEqual(summarize(rebuilt), read(STARTER/f'results/{split}_summary.json'))

    def test_requested_filter_is_not_applied_filter(self):
        for t in read(STARTER/'results/test_traces.json'):
            if t['id']=='Q17':
                self.assertEqual(applied_filter(t), {'metadata':{'chapter':'IV'}} if t['strategy']=='C' else None)

    def test_known_split_evidence_failures_stay_failures(self):
        for t in read(STARTER/'results/dev_traces.json'):
            if t['id'] in ('Q10','Q12') or (t['id'] in ('Q11','Q14') and t['strategy'] in ('B','C')):
                self.assertEqual(t['evidence_hit_at_3'],0,(t['id'],t['strategy']))


if __name__ == '__main__': unittest.main()
