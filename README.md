# Day 06 — Data Ingestion Engineering

Nguyễn Đình Minh · MSSV 2A202603867 · corpus văn bản hợp nhất Luật Đường bộ.

Pipeline Python chạy thực bằng `intfloat/multilingual-e5-small` (384 chiều) và PostgreSQL 16.16 / pgvector 0.8.7. Ba cấu hình chính thức: A fixed-size 800/100, B paragraph 800, C cùng index B + filter chapter được cung cấp trong câu hỏi. Baseline và gold được giữ nguyên, lần chạy kiểm chứng ở `starter/results/reproduced/`.

- [Setup và tất cả lệnh chạy](starter/README.md)
- [Manifest và cách lấy PDF](data/manifest.json) — nguồn: [congbao.chinhphu.vn](https://congbao.chinhphu.vn/cong-bao/cong-bao-so-528-vbhn-ngay-25-09-2026-47497.htm)
- [Benchmark và định nghĩa metric](benchmark/README.md)
- [Báo cáo cá nhân theo mẫu](report/individual/2A202603867_NguyenDinhMinh.md)
- [Grounding](starter/results/manual_grounding.md), [coherence](starter/results/chunk_coherence.md), [metadata](starter/results/metadata_usefulness.md)
- [Checklist nộp bài và file cần commit](starter/results/submission_checklist.md)

Chạy từ `starter/` sau khi cài dependencies và khởi động Docker:

```bash
python -m src.run all
python -m src.audit
python -m unittest discover -s tests -v
python scripts/validate_artifacts.py
```

Các phiếu đã lưu có đủ 15 grounding, 30 coherence và 45 metadata được học viên xác nhận; điểm AI và các điểm human do học viên nhập được giữ riêng. Thông tin lớp L3B đã đủ. Bộ nộp giữ đủ benchmark, traces và audit; PDF gốc/source extract không phân phối, có hướng dẫn tải và kiểm tra SHA256. Việc nộp link qua kênh lớp được ghi nhận riêng với push GitHub.

Đề bài và contract gốc giữ tại [GUIDE](GUIDE.md), [BENCHMARK](BENCHMARK.md), [RUBRIC](RUBRIC.md), [CHECKPOINTS](CHECKPOINTS.md), [RULES](RULES.md), [SUBMISSION](SUBMISSION.md).

AI-assessment đã hoàn tất **15/15 grounding, 30/30 coherence, 45/45 metadata**: [bảng đủ năm dimensions](starter/results/ai_assessment_summary.md). Điểm AI và human được giữ riêng; các trường human hiện đã được học viên điền đủ trong hai CSV và phiếu metadata. [Rà soát quyền dữ liệu](data/rights_review.md) có căn cứ chính thức cho nội dung luật, chưa xác nhận phân phối toàn file PDF.
