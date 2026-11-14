# Đối chiếu nộp bài Day 06

Học viên: Nguyễn Đình Minh — 2A202603867 — L3B. Checklist dựa trên SUBMISSION.md, RUBRIC.md và file đã lưu; không tự tính điểm bài.

| Yêu cầu | Trạng thái | Minh chứng |
|---|---|---|
| Corpus ≥30 trang, nguồn/quyền và manifest | PASS cho phạm vi nộp | 65 trang vật lý, 64 trang hữu ích; data/manifest.json và data/rights_review.md; PDF gốc không phân phối, README có URL + SHA256 |
| Đọc/normalize/log/trace nguồn | PASS | src/ingestion.py; verification/corpus_validation.json; 130 kiểm tra coverage và 20/20 gold đúng trang |
| A/B/C chạy được, so sánh có kiểm soát | PASS | A fixed800/100, B paragraph800, C dùng cùng B + filter theo input; src/run.py và experiment_log.csv |
| Embedding thật, lưu bền vững, metadata filter | PASS | E5 384, PostgreSQL16.16/pgvector0.8.7; reproduced/all_run.json, verification/docker_storage.json |
| Idempotency và nguồn thay đổi | PASS | reproduced/engineering_verification.json; 250→250/309→309, synthetic5→1, schema thử nghiệm đã dọn |
| ≥20 câu, filter và split | PARTIAL về lịch sử chốt | 20 câu, 15DEV/5TEST, 3 filters có1TEST; benchmark/gold giữ nguyên. Không chứng minh hồi tố thời điểm chốt trước thử nghiệm, TEST đã được xem |
| Top-3 traces và retrieval metrics | PASS | dev/test_traces.json, dev/test_summary.json; 60/60 Top-3 ID sets tái lập |
| Coherence và grounding | PASS về phiếu đã lưu | 30/30 coherence và15/15 grounding có điểm/lý do/người/ngày do học viên nhập; AI và human báo riêng |
| Metadata usefulness | PASS về phiếu đã lưu | 45/45 metadata được học viên xác nhận; metadata_ai_review.csv, metadata_usefulness.md, metadata_human_review.md |
| Năm dimensions và trade-off | PASS | ai_assessment_summary.md/json; báo cáo cá nhân có A–B/B–C, Q09/Q10/Q11/Q12/Q14/Q16/Q19 và giới hạn mẫu nhỏ |
| Setup, dependencies, code, tests, báo cáo | PASS | README, starter/README, requirements, src, scripts, tests; report/individual/2A202603867_NguyenDinhMinh.md |
| Secrets và file không cần nộp | Kiểm tra trước commit | Chỉ stage allowlist; .env/.venv/.git/cache, PDF/source extract, drafts, exports trùng và bookkeeping giữ local |
| Repo/commit chốt | Ghi theo Git thực tế | STUDENT.md và lịch sử nhánh main; không tự ghi SHA chưa tồn tại |
| Người chấm truy cập / nộp link qua lớp | Chưa xác nhận | Push GitHub không đồng nghĩa đã nộp link theo kênh lớp |

## Kết quả và đường dẫn

- Retrieval DEV A9/15,11/15; B/C7/15,11/15. TEST A/B/C4/5,4/5. Không sửa gold hoặc baseline để tăng điểm.
- AI assessment15/15 grounding,30/30 coherence,45/45 metadata. Các phiếu human đã được học viên điền riêng, không lấy cột ai_* thay cho nhãn human.
- Log tests cuối: verification/submission_unit_tests.txt. Kết quả kiểm chứng nguồn và pipeline: verification/corpus_validation.json, verification/baseline_comparison.json, verification/mission_validation.json.
- Bộ kiểm tra đọc UTF-8/BOM và bỏ dòng trống trước header, báo rõ khi thiếu/thừa cột. Lần sửa CSV chỉ sửa định dạng, không thay điểm/lý do/tên/ngày.
- Chưa restart container trong bài kiểm chứng độ bền; đã kiểm tra commit qua kết nối mới và named volume. Không coi TEST5 câu là holdout mới hoặc kết luận tối ưu tổng quát.

## Phạm vi phân phối

Giữ benchmark/gold, Top-3 traces, nhãn human/AI và báo cáo để đáp ứng SUBMISSION.md. Các đoạn văn bản luật đi kèm attribution và căn cứ nguồn trong data/rights_review.md. Cờ permission_verified của toàn PDF vẫn false; selected_files_sharing_supported là đánh giá riêng cho các file văn bản được chọn.

PDF gốc và bản source extract toàn nguồn không được commit; người chấm tải PDF riêng theo starter/README và đối chiếu SHA256. Các chunk exports có thể tạo lại bằng ingest. Các bản nháp, gợi ý và log lịch sử vẫn còn trên máy, không bị xóa.

Allowlist tạm được tạo bằng `python scripts/check_submission.py` từ starter/: results/verification/commit_candidates.txt. Danh sách loại và trạng thái kỹ thuật cũng là output local, không commit những file bookkeeping này. Các phiếu và minh chứng chính thức được giữ trong Git.
