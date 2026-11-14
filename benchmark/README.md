# Benchmark đã cố định

File chuẩn duy nhất: [20 câu hỏi và gold](../starter/data/benchmark_questions.json), gồm 15 DEV (Q01–Q15) và 5 TEST (Q16–Q20). Không sao chép bộ gold sang file thứ hai để tránh sai khác.

- Q06 / Q11 / Q17 có filter chương II / III / IV được nêu trong chính câu hỏi. Chỉ C áp dụng, A/B không lọc.
- Cả 20 gold_quote đã kiểm tra với đúng source_id và trang PDF sau NFC/whitespace normalization. Kết quả: [corpus_validation.json](../starter/results/verification/corpus_validation.json).
- [baseline_lock.json](baseline_lock.json) lưu SHA256 PDF, benchmark, source extract và bốn file baseline. `python scripts/validate_artifacts.py` từ `starter/` kiểm tra không đổi chúng.
- Bộ split có sẵn khi tiếp nhận repo. Không có timestamp đủ để xác nhận độc lập việc chốt benchmark/tiêu chí chọn trước lần chạy ban đầu. TEST đã được xem; lần chạy reproduced là kiểm chứng tái lập, không phải holdout mới. Không thêm/sửa gold theo TEST.

Evaluator yêu cầu **một** chunk đúng document_id, phủ đủ gold_page và chứa đủ evidence. `gold_evidence` là danh sách các bộ thay thế, chấp nhận bất kỳ một bộ. Trong một bộ, danh sách `evidence_quote` là các đoạn **đều bắt buộc**, danh sách `gold_page` là các trang **đều phải được chunk phủ**; các trang/quote thay thế độc lập phải đặt trong các bộ khác nhau. `gold_source_id` có thể là một ID hoặc danh sách ID nguồn tương đương. Không ghép nhiều chunk để tính hit chính thức. Bằng chứng tương đương về ngữ nghĩa cần người chấm xác nhận và lưu riêng, không tự bỏ bớt gold.

Exact-match chỉ casefold, NFC và gộp whitespace. Không sửa được khoảng trắng chen trong từ do pypdf, lỗi OCR hay diễn đạt tương đương. Hit chỉ đúng trang là chưa đủ; gold dài có thể gây miss dù đủ ý trả lời. Đọc nhãn grounding riêng; không gọi metric retrieval là độ chính xác LLM.
