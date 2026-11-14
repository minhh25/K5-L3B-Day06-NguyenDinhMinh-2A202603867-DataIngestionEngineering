import unittest
from unittest.mock import MagicMock, patch

from src.evaluation import evaluate_query
from src.metadata import attach_metadata
from src.models import Chunk, DocumentPage
from src.store import PgVectorStore


class ChapterMetadataTests(unittest.TestCase):
    def chunk(self, page, text):
        return Chunk('c', page.document_id, page.source, page.page, text)

    def test_transition_page_preserves_previous_chapter_until_heading(self):
        first = DocumentPage('d', 'source.pdf', 4, 'Chương I\nNội dung chương một.')
        transition = DocumentPage('d', 'source.pdf', 5,
                                  'CÔNG BÁO/Số 1\nTiếp chương một.\nChương II\nNội dung chương hai.')
        before = self.chunk(transition, 'Tiếp chương một.')
        after = self.chunk(transition, 'Chương II\nNội dung chương hai.')
        attach_metadata([first, transition], [before, after], 'snapshot')
        self.assertEqual(before.metadata['chapter'], 'I')
        self.assertEqual(after.metadata['chapter'], 'II')

    def test_chunk_crossing_two_chapters_stays_null(self):
        page = DocumentPage('d', 'source.pdf', 1, 'Chương I\nNội dung cũ.\nChương II\nNội dung mới.')
        chunk = self.chunk(page, 'Nội dung cũ.\nChương II\nNội dung mới.')
        attach_metadata([page], [chunk], 'snapshot')
        self.assertIsNone(chunk.metadata['chapter'])
        self.assertEqual(chunk.metadata['chapters'], ['I', 'II'])

    def test_header_only_chunk_does_not_inherit_chapter(self):
        first = DocumentPage('d', 'source.pdf', 1, 'Chương IV\nNội dung.')
        page = DocumentPage('d', 'source.pdf', 2, 'CÔNG BÁO/Số 528-VBHN/Ngày 25-09-2026 3')
        header = self.chunk(page, page.text)
        attach_metadata([first, page], [header], 'snapshot')
        self.assertIsNone(header.metadata['chapter'])
        self.assertEqual(header.metadata['chapters'], [])

    def test_preamble_mixed_with_first_heading_is_not_assigned_to_chapter(self):
        page = DocumentPage('d', 'source.pdf', 1, 'Lời mở đầu.\nChương I\nNội dung.')
        chunk = self.chunk(page, page.text)
        attach_metadata([page], [chunk], 'snapshot')
        self.assertIsNone(chunk.metadata['chapter'])
        self.assertEqual(chunk.metadata['chapters'], ['I'])

    def test_unknown_chapter_is_not_invented(self):
        page = DocumentPage('d', 'source.pdf', 8, 'Nội dung không có heading được xác minh.')
        chunk = self.chunk(page, page.text)
        attach_metadata([page], [chunk], 'snapshot')
        self.assertIsNone(chunk.metadata['chapter'])

    def test_new_document_does_not_inherit_another_documents_chapter(self):
        first = DocumentPage('a', 'a.pdf', 1, 'Chương IV\nNội dung a.')
        second = DocumentPage('b', 'b.pdf', 1, 'Chưa có heading của b.')
        chunk_a, chunk_b = self.chunk(first, first.text), self.chunk(second, second.text)
        attach_metadata([first], [chunk_a], 'a')
        attach_metadata([second], [chunk_b], 'b')
        self.assertIsNone(chunk_b.metadata['chapter'])

    def test_filter_without_results_returns_empty_without_retry_or_fallback(self):
        connection, cursor = MagicMock(), MagicMock()
        connection.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchall.return_value = []
        with patch('src.store.psycopg.connect') as connect:
            connect.return_value.__enter__.return_value = connection
            hits = PgVectorStore('unit-test-only', 384).search(
                'paragraph_800', [0.1] * 384, filters={'metadata': {'chapter': 'MISSING'}})
        self.assertEqual(hits, [])
        self.assertEqual(connect.call_count, 1)
        self.assertEqual(cursor.execute.call_count, 1)
        self.assertIn('chapter', cursor.execute.call_args.args[1])
        self.assertIn('MISSING', cursor.execute.call_args.args[1])
        result = evaluate_query({'id': 'unit', 'split': 'test', 'question': 'Test',
                                 'gold_source_id': 'd', 'gold_page': 1, 'evidence_quote': 'evidence'}, hits)
        self.assertEqual((result['hit_at_1'], result['evidence_hit_at_3']), (0, 0))


if __name__ == '__main__':
    unittest.main()
