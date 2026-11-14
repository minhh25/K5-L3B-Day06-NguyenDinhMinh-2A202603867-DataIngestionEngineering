import unittest

from src.chunking import fixed_size, by_paragraph
from src.metadata import attach_metadata
from src.models import DocumentPage
from src.store import PgVectorStore


class PipelineTests(unittest.TestCase):
    def test_stable_ids_and_coverage(self):
        page = DocumentPage('d','f.pdf',1,'Chương I\n'+ 'Nội dung. '*200)
        for fn in (lambda p:fixed_size(p,800,100), lambda p:by_paragraph(p,800)):
            chunks = fn(page)
            self.assertEqual([c.chunk_id for c in chunks],[c.chunk_id for c in fn(page)])
            attach_metadata([page],chunks,'hash')
            covered = set()
            for c in chunks:
                covered.update(range(c.metadata['start_char'],c.metadata['end_char']))
            self.assertTrue(all(i in covered for i,ch in enumerate(page.text) if not ch.isspace()))

    def test_chapter_boundaries_and_header(self):
        text = 'CÔNG BÁO/Số 1\n\nChương I\nMột.\n\nChương II\nHai.'
        page = DocumentPage('d','f.pdf',1,text)
        chunks = by_paragraph(page,800)
        attach_metadata([page],chunks,'hash')
        self.assertIsNone(chunks[0].metadata['chapter'])
        self.assertEqual(chunks[0].metadata['chapters'],['I','II'])
        separate = by_paragraph(page,22)
        attach_metadata([page],separate,'hash')
        self.assertIsNone(separate[0].metadata['chapter'])
        self.assertEqual(separate[-1].metadata['chapter'],'II')

    def test_store_rejects_bad_vectors_before_connect(self):
        store = PgVectorStore('unused',384)
        chunk = fixed_size(DocumentPage('d','f',1,'x'),800,100)[0]
        with self.assertRaises(ValueError): store.upsert('s',[chunk],[[1.]])
        vector = [0.1]*384
        with self.assertRaises(ValueError): store.upsert('s',[chunk,chunk],[vector,vector])
        with self.assertRaises(ValueError): store.search('s',[float('nan')]*384)


if __name__ == '__main__': unittest.main()
