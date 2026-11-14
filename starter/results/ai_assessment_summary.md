# Năm dimensions — AI assessment hoàn chỉnh

Nhãn AI đề xuất — CHƯA phải chấm thủ công bởi người học. Chỉ đánh giá evidence retrieval, không phải độ chính xác câu trả lời LLM.

Đã đánh giá AI: grounding 15/15, coherence 30/30, metadata 45/45. Không tạo human review hay chữ ký. Giữ nguyên nguồn/gold và retrieval baseline.

| Config | Retrieval DEV Hit@1 / Evidence Hit@3 | Retrieval TEST Hit@1 / Evidence Hit@3 | Coherence AI /2 | Metadata correctness / completeness | Grounding AI /2 | Data strategy impact |
|---|---|---|---|---|---|---|
| A | 9/15 / 11/15 | 4/5 / 4/5 | 1.00 | 15/15 / 15/15 | 1.80 | 250 chunks; 4.962s ingest warm |
| B | 7/15 / 11/15 | 4/5 / 4/5 | 1.00 | 15/15 / 15/15 | 2.00 | 309 chunks; 3.402s ingest warm |
| C | 7/15 / 11/15 | 4/5 / 4/5 | 1.00 | 15/15 / 15/15 | 2.00 | Dùng chung 309 chunks B; không ingest thêm |

C filter compliance TEST: 3/3 records, 1/1 câu; DEV: 2/2 câu. A/B không áp dụng filter nên NOT_APPLICABLE. Metadata đúng không có nghĩa là chunk liên quan hoặc trả lời đủ câu hỏi.

A–B: DEV Evidence Hit@3 bằng nhau nhưng A Hit@1 cao hơn 2/15, B giữ đủ Q16 và mất exact gold ở Q19. B–C: filter đổi một phần Top-3 Q06, aggregate không tăng; chương đúng vẫn có thể thiếu evidence Q11. Coherence mẫu đầu corpus đều 1/2 do ranh giới đứt câu/điều kiện; không đại diện cả tài liệu.

Grounding AI A=0/1/4 trường hợp điểm 0/1/2; B/C=0/0/5. Q19 B/C đủ ý khi đọc Top-3 chung nhưng Evidence Hit@3 vẫn 0. Tập TEST 5 câu nhỏ và đã được xem; không nhận là holdout mới hoặc chất lượng trả lời LLM.

Thời gian và dữ liệu tài nguyên lấy từ lượt reproduced đã lưu, không thay bằng thời gian mới. Chi phí API 0, chưa đo điện/phần cứng. Chi tiết từng nhãn: grounding_review.csv, coherence_review.csv, metadata_ai_review.csv. Phương pháp: verification/ai_assessment_method.json.
