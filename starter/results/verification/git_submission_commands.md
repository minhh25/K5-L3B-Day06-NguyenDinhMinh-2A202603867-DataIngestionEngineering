# Lệnh Git cho bộ nộp

Chạy từ repo root. Bộ nộp gồm code, manifest, benchmark/gold, traces, nhãn human/AI và báo cáo. PDF gốc và source extract toàn nguồn giữ local; các đoạn luật trong benchmark/audit theo căn cứ và attribution tại data/rights_review.md.

```bash
starter/.venv/bin/python starter/scripts/check_submission.py
git add --pathspec-from-file=starter/results/verification/commit_candidates.txt
git diff --cached --stat
git diff --cached --check
git commit -m "Complete Day 06 ingestion engineering lab"
git push origin main
```

Bản nháp/gợi ý, exports trùng, .env/.venv/.git/cache và bookkeeping được ignore. Luôn xem diff đã stage trước commit. Commit đã nộp được ghi trong STUDENT.md và lịch sử main. Push GitHub không tự thay thế thao tác nộp link theo kênh lớp.
