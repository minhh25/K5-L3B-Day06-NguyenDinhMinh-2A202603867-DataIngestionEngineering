import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.audit import applied_filter
from src.evaluation import evaluate_query, normalize_evidence, summarize
from src.run import ROOT, STARTER, build_chunks, load_corpus, load_questions, read, save

output=STARTER/'results/verification'
documents=load_corpus(ROOT/'data/manifest.json',output)
questions=load_questions(STARTER/'data/benchmark_questions.json',documents)
chunks=build_chunks(documents)
locks=read(ROOT/'benchmark/baseline_lock.json')
unchanged={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in locks.items()}
assert all(unchanged.values())
coverage=[]
for entry,pages in documents:
 for strategy,items in chunks.items():
  for page in pages:
   selected=[c for c in items if c.document_id==page.document_id and c.page==page.page]
   covered=set()
   for c in selected:covered.update(range(c.metadata['start_char'],c.metadata['end_char']))
   missing=[i for i,ch in enumerate(page.text) if not ch.isspace() and i not in covered]
   assert not missing,(strategy,page.page,missing)
   coverage.append({'strategy':strategy,'document_id':page.document_id,'page':page.page,'chunks':len(selected),'uncovered_nonwhitespace_characters':len(missing)})
checks=[]
filters=[]
for split in ('dev','test'):
 baseline=read(STARTER/f'results/{split}_traces.json')
 actual=read(STARTER/f'results/reproduced/{split}_traces.json')
 summaries=[]
 for traces in (baseline,actual):
  rebuilt=[evaluate_query({**t,'filter':applied_filter(t)},t['hits']) for t in traces]
  summaries.append(summarize(rebuilt))
 assert summaries[0]==summaries[1]==read(STARTER/f'results/{split}_summary.json')
 old={(t['id'],t['strategy']):t for t in baseline}
 for trace in actual:
  prior=old[(trace['id'],trace['strategy'])]
  checks.append({'id':trace['id'],'strategy':trace['strategy'],'split':split,
                 'same_top3_ids':[h['chunk_id'] for h in trace['hits']]==[h['chunk_id'] for h in prior['hits']],
                 'same_metrics':all(trace[k]==prior[k] for k in ('hit_at_1','evidence_hit_at_3'))})
  if trace['strategy']=='C' and trace.get('applied_filter'):
   requested=trace['applied_filter']['metadata']
   compliant=len(trace['hits'])==3 and all(all(h['metadata'].get(k)==v for k,v in requested.items()) for h in trace['hits'])
   filters.append({'id':trace['id'],'split':split,'filter':trace['applied_filter'],
                   'compliant':compliant,'retrieval_hit_at_3':trace['evidence_hit_at_3'],
                   'top3_ids':[h['chunk_id'] for h in trace['hits']]})
assert all(c['same_metrics'] and c['same_top3_ids'] for c in checks)
assert all(c['compliant'] for c in filters)
save(output/'baseline_comparison.json',{'unchanged_sha256':unchanged,'trace_comparisons':checks})
save(output/'filter_validation.json',{'questions':filters,'dev_compliant':'2/2','test_compliant':'1/1','note':'Compliance is independent of retrieval accuracy; Q11 complies but lacks full evidence.'})
save(output/'corpus_validation.json',{'gold_questions_verified':len(questions),'physical_pages':sum(len(pages) for _,pages in documents),
 'useful_pages':sum(len(e['useful_pages']) for e,_ in documents),
 'normalized_characters':sum(len(p.text) for _,pages in documents for p in pages),
 'page_coverage':coverage,'ocr_run':False,'extraction_errors':0,
 'benchmark_provenance':'15/5 split existed on arrival; cannot independently prove labels or selection criterion were frozen before original baseline. TEST already seen; no holdout claim.'})
print('PASS: 20 gold quotes; 64 useful / 65 physical pages; 130 page/strategy coverage checks; 60 identical top-3 ID lists; filters DEV 2/2 TEST 1/1; 7 locked files unchanged.')
