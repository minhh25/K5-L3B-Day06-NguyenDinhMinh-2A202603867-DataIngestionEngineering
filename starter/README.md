# Lab Day 06 — E5 + PostgreSQL/pgvector

Pipeline thực tế cho ba cấu hình chính thức: A=`fixed_800_100`, B=`paragraph_800`, C dùng đúng index B và chỉ lọc chapter khi câu hỏi yêu cầu. Các thử nghiệm Article/Paragraph Overlap được giữ riêng.

## Cấu trúc và dữ liệu

- `src/`: ingestion, chunking, embeddings, metadata, store, evaluation, run, verification, audit.
- `tests/`: kiểm thử metric, ranh giới chương, ID, vector validation, baseline regression.
- `data/`: PDF nguồn, 20 benchmark questions, source extract. Manifest ở `../data/manifest.json`, mô tả benchmark ở `../benchmark/README.md`.
- `results/{dev,test}_{traces,summary}.json`: baseline bất biến.
- `results/reproduced/`: lần chạy lại, traces, thời gian, engineering verification và phiên bản; chunk exports lớn giữ local và có thể tạo lại.
- `results/verification/`: kiểm chứng gold, coverage, filters, baseline hash, Docker volume và chẩn đoán lỗi.
- `results/*review.csv`, `manual_grounding.md`, `chunk_coherence.md`, `metadata_usefulness.md`: phiếu nhãn AI và cơ chế duyệt của học viên.
- Báo cáo: `../report/individual/2A202603867_NguyenDinhMinh.md`; checklist nộp: `results/submission_checklist.md`.

Nguồn: [Công báo Chính phủ](https://congbao.chinhphu.vn/cong-bao/cong-bao-so-528-vbhn-ngay-25-09-2026-47497.htm). Chọn văn bản 144/2026/VBHN-LQ-VPQH, tải **PDF riêng 65 trang** tại [trang văn bản](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-144-2026-vbhn-lq-vpqh-470557/68753.htm). Đặt basename như manifest, kiểm tra SHA256 trước ingest. Nguồn yêu cầu ghi công lao `congbao.chinhphu.vn` khi phát hành lại thông tin; giấy phép riêng PDF chưa xác minh. Bản nguồn giữ nguyên, không suy đoán hiệu lực pháp lý. Chi tiết quyền và cách lấy ở manifest.

## Kiểm tra bản tải và chuẩn bị file nộp

PDF gốc và source extract giữ local và được `.gitignore` loại khỏi commit. Bộ nộp giữ benchmark/gold, trace Top-3 và các phiếu audit chứa các đoạn luật, dựa trên căn cứ tái sử dụng nội dung luật đã xác minh trong `../data/rights_review.md`, kèm attribution. `permission_verified=false` vẫn áp dụng cho toàn file PDF; `selected_files_sharing_supported` mô tả riêng phạm vi các file được chọn.

Các bản nháp `*_human_draft.csv`, `*_suggestions.csv`, lượt `review_check`, chunk exports có thể tái tạo và bookkeeping của phiên làm việc được ignore, không bị xóa khỏi máy. Dùng danh sách do `scripts/check_submission.py` sinh tại `results/verification/commit_candidates.txt` để stage; log trạng thái tạm không được commit. Không đóng gói toàn workspace vì `.gitignore` không tự lọc một lệnh ZIP tùy ý.

Nếu không phân phối nguồn, người chấm tải PDF riêng qua hai link Công báo ở trên, đặt đúng đường dẫn manifest và kiểm tra SHA256 bằng lệnh sau từ `starter/`. Lệnh chỉ kiểm tra file đã tải, không sửa nguồn:

```bash
python - <<'PYCODE'
import hashlib
import json
from pathlib import Path

manifest = json.loads(Path('../data/manifest.json').read_text())
for source in manifest['sources']:
    path = Path('..') / source['source_path_or_url']
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != source['snapshot_sha256']:
        raise SystemExit(f'SHA256 mismatch: {path.name}')
    print(f'SHA256 OK: {path.name} {actual}')
PYCODE
```

Gold, traces và audit chính thức đã được chọn trong bộ nộp; chỉ PDF gốc, bản source extract toàn nguồn và các bản xuất trùng không phân phối. Người chấm cần tải PDF và khớp SHA256 trước khi chạy tests/audit có kiểm tra trực tiếp nguồn. Sau đó có thể tái tạo chunk exports bằng `python -m src.run ingest`.

## Setup từ thư mục starter

Đã kiểm chứng trên macOS, Python 3.13.3, Apple MPS. Cần Docker Desktop/Engine + Compose. Model local, không dùng API key. Lần đầu cần mạng để tải image, packages và model; cần đủ RAM cho PyTorch.

```bash
cd starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
docker compose -p day6_student_starter up -d --wait
python scripts/check_setup.py
```

Giữ `DATABASE_URL` trong `.env`, không commit file này. `EMBEDDING_MODEL` trong template không override model chính thức: CLI cố định `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, 384 chiều; documents dùng `passage:`, queries dùng `query:`, normalize vector. Maximum sequence length 512 tokens của model được ghi trong run metadata. Không đổi model giữa cấu hình.

Compose mở PostgreSQL tại `127.0.0.1:55433`, dùng named volume `day6_student_starter_pg_data`; không chạy `down -v` trên dữ liệu cần giữ. Image `pgvector/pgvector:0.8.7-pg16`; PostgreSQL thực tế 16.16, pgvector 0.8.7. Bảng `lab_chunks`, cosine exact search; PK `(strategy, chunk_id)`.

## Chạy và kiểm chứng

```bash
python -m src.run all
# Hoặc từng bước, cùng output directory:
python -m src.run ingest --output results/reproduced
python -m src.run verify --output results/reproduced
python -m src.run eval --split dev --output results/reproduced
python -m src.run eval --split test --output results/reproduced
python -m src.run report --output results/reproduced
python -m src.audit
python -m unittest discover -s tests -v
python scripts/validate_artifacts.py
python scripts/check_submission.py
```

`python -m src.run` mặc định tương đương `all`: ingest → verify → eval → retrieval report. Dùng `--output results/run_02` nếu cần giữ lần reproduced cũ; chương trình từ chối ghi thẳng lên thư mục baseline `results/`. Khi model đã có cache, có thể thêm `HF_HUB_OFFLINE=1` trước lệnh. Không có mock fallback. Khi lỗi, lệnh trả exit code 1 và ghi `error.json` đã loại thông tin kết nối; lỗi đọc trang nằm trong `ingestion_pages.json`. File lỗi cũ được giữ làm lịch sử, cần đọc cùng run timestamp.

`eval` xác minh text, IDs, source snapshot, chapter và model revision khớp index trước khi truy xuất. Không tự suy filter từ gold; chỉ nhận chapter có sẵn trong câu hỏi. Traces lưu đủ text, ID, score, metadata của Top-3, requested/applied filter và nhãn metric riêng DEV/TEST.

Ingest truyền **toàn bộ chunks của mỗi tài liệu/chiến lược** trong một lần upsert (không ghi từng minibatch embedding). Ghi lại cùng nguồn cập nhật các ID có sẵn và xóa ID lỗi thời theo document_id. Khi tài liệu đổi, cập nhật SHA256, page statistics và version manifest sau khi kiểm tra nội dung; không sửa benchmark để chạy theo TEST. Nếu tài liệu không còn text hữu ích, pipeline dừng trước khi thay dữ liệu. Tài liệu bị loại hoàn toàn khỏi manifest cần quản lý/xóa tường minh; không tự xóa tài liệu khác trong database. `article_800`/`fixed_test` được giữ nguyên.

Chapter lấy từ heading và offset thực của chunk sau NFC; chunk chỉ có Công báo, chưa thuộc chương, hoặc chứa hai chương nhận null. `chapters` liệt kê phạm vi có thật, không dùng làm filter chính thức. B/C cùng chunk và embedding, coherence giống nhau. Baseline từng có 62 Paragraph null; tái tạo sửa một chunk preamble gán I thành null, tổng 63; không đổi text/IDs/metrics.

## Học viên duyệt nhãn

Đọc trọn Top-3 trong `results/manual_grounding.md` (15 trường hợp), các chunk ở cùng 10 vị trí trong `results/chunk_coherence.md` (30 nhãn), rồi điền `human_score`, `human_reason`, `reviewer`, `reviewed_at` tại hai CSV review. Chạy `python -m src.audit` để tái tổng hợp. Nhãn AI giữ nguyên và số người học đã duyệt báo riêng; không mặc định nhãn AI là nhãn thủ công. Duyệt metadata ở `results/metadata_human_review.md`. AI assessment đã có đủ 15/15 grounding, 30/30 coherence và 45/45 metadata, cùng reviewer AI và thời điểm thực; xem `results/ai_assessment_summary.md` và `results/metadata_ai_review.csv`. Các kết quả này không tự trở thành human review.

`audit` dựng bảng audit và chỉ cập nhật vùng `HUMAN_REVIEW_START`/`HUMAN_REVIEW_END` của báo cáo cá nhân từ điểm human đã được ký đủ; bảng AI và số liệu retrieval/tài nguyên giữ nguyên. `run report` dựng bảng metric từ traces. Kết luận phân tích vẫn cần học viên tự cập nhật khi nhãn đổi.

Metadata chỉ được ghi nhận 45/45 khi phiếu có đủ `Trạng thái: ĐÃ DUYỆT`, Người duyệt, Ngày duyệt và checkbox `[x]` đối chiếu 45 bản ghi. Điểm CSV chỉ tính khi có human_score 0/1/2, human_reason, reviewer, reviewed_at; điểm 0 có ký xác nhận vẫn là một nhãn hợp lệ. `check_submission.py` đọc các phiếu thật và kiểm tra CSV/summary/bảng báo cáo; exit 0 chỉ nghĩa kiểm tra kỹ thuật qua, `readiness_status` vẫn PARTIAL nếu thiếu nhãn, quyền dữ liệu, xác nhận sinh viên hoặc điều kiện nộp bài trong STUDENT.md.

Dừng database và giữ dữ liệu: `docker compose -p day6_student_starter stop`.

Rà soát quyền dữ liệu: [data/rights_review.md](../data/rights_review.md) lưu căn cứ chính thức cho phạm vi nội dung văn bản luật và điều kiện attribution; quyền phân phối toàn PDF vẫn chưa được xác nhận nên giữ permission_verified=false.

Lệnh Git để học viên tự quyết định chốt/nộp: [git_submission_commands.md](results/verification/git_submission_commands.md). Commit dùng danh sách file đã kiểm tra, không có PDF gốc hoặc secrets. Kiểm chứng pipeline mới nhất: `python -m src.run all --output results/mission_check`; kết quả cũ ở reproduced được giữ nguyên.
