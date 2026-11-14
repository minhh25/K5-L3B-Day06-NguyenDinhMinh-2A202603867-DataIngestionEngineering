# Báo cáo cá nhân — Day 6

## Dữ liệu và pipeline

Bài toán là xây kho evidence truy vết được cho câu hỏi tiếng Việt về Luật Đường bộ và đo tác động của cách chia dữ liệu/lọc chương. Không sinh câu trả lời LLM trong benchmark. Học viên: **Nguyễn Đình Minh — 2A202603867** (do học viên cung cấp); lớp **L3B** theo thông tin học viên đã điền trong STUDENT.md.

Kiến trúc: PDF + manifest → pypdf/NFC theo trang → fixed/paragraph + metadata spans → E5 passage embeddings → PostgreSQL/pgvector → E5 query + Top-3 A/B/C → evaluator và audit. Gold chỉ đi vào evaluator; không đi vào embedding câu hỏi hay tạo filter. C dùng cùng bảng/index B, thêm điều kiện SQL khi câu hỏi nêu chương. Lỗi backend dừng pipeline và ghi lỗi đã loại credentials, không fallback mock.

Chủ đề hẹp: văn bản hợp nhất Luật Đường bộ 144/2026/VBHN-LQ-VPQH. Nguồn: [Công báo Chính phủ số 528-VBHN](https://congbao.chinhphu.vn/cong-bao/cong-bao-so-528-vbhn-ngay-25-09-2026-47497.htm), [trang văn bản và tải PDF riêng](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-144-2026-vbhn-lq-vpqh-470557/68753.htm), do học viên cung cấp và AI đối chiếu ngày 14/11/2026. Trang nguồn ghi yêu cầu dẫn nguồn khi phát hành lại thông tin; chưa xác minh giấy phép riêng PDF. Không suy ra quyền tái phân phối không hạn chế hoặc ngày hiệu lực. Tải PDF qua công cụ duyệt bị HTTP 502, nên chưa xác nhận hash remote bằng hash local. Định danh và viewer 65 trang khớp nguồn; checksum bản local được khóa trong [manifest](../../data/manifest.json).


Rà soát quyền dữ liệu bổ sung: đã đối chiếu Điều 15(2) trong bản hợp nhất Luật Sở hữu trí tuệ 160/2026/VBHN-LQ-VPQH trên nguồn Công báo chính thức, thấy căn cứ cho nhóm nội dung văn bản luật không thuộc bảo hộ quyền tác giả. Đây là suy luận theo phạm vi nội dung luật, không tự coi là giấy phép cho toàn PDF local, hình thức xuất bản hay mọi thành phần website. Chi tiết URL, trang và điều kiện attribution tại [rights_review.md](../../data/rights_review.md). Vì phạm vi phân phối toàn file chưa xác minh, `permission_verified=false`; PDF gốc và bản trích xuất toàn nguồn tiếp tục nằm ngoài commit; benchmark/gold, traces và audit chứa các đoạn luật được đưa vào bộ nộp theo căn cứ tái sử dụng nội dung luật, kèm attribution.

PDF có 65 trang vật lý, 158.019 ký tự sau chuẩn hóa. Tính 64 trang nội dung hữu ích (2–65): có điều/khoản liên quan; loại trang 1 tiêu đề/căn cứ/chú thích khỏi phép đếm. Giữ trang 1 khi chunk để tái tạo nguyên baseline, không nhân bản corpus. Không trang rỗng/lỗi trích xuất trong lần chạy; không OCR. NFC, chuẩn hóa newline và whitespace ngang, giữ phân trang và các khoảng trắng chen trong từ do pypdf. Kiểm tra máy 20/20 gold có trong đúng source/page. [Corpus validation](../../starter/results/verification/corpus_validation.json) cũng kiểm tra toàn bộ ký tự khác whitespace được ít nhất một chunk phủ trên 65 trang × 2 chiến lược (130 kiểm tra). Người học vẫn cần spot-check PDF và chứng nhận quyền dữ liệu.

Model local: `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, 384 chiều, Sentence Transformers 6.3.0; `passage:` cho document, `query:` cho câu hỏi, normalize embeddings. Python 3.13.3, pypdf 6.21.4, transformers 5.23.0, torch 2.15.0, psycopg 3.3.8, python-dotenv 1.2.4, numpy 2.5.4. Model max sequence length 512 tokens; giữ cùng chính sách giữa A/B/C. Chưa đo riêng số token bị truncation. Chạy MPS trên macOS. Không gọi dịch vụ embedding trả phí, API cost=0; không đo điện năng/khấu hao.

Vector store: PostgreSQL 16.16 (Debian), pgvector 0.8.7, image `pgvector/pgvector:0.8.7-pg16`; cosine exact SQL search `embedding <=> query`, không có ANN vector index. Bảng `lab_chunks`, khóa `(strategy, chunk_id)`; filter bằng SQL tham số hóa. Container healthy, volume `day6_student_starter_pg_data` gắn `/var/lib/postgresql/data`. Dữ liệu commit được đọc qua kết nối mới; chưa thực hiện bài test restart container. [Minh chứng volume](../../starter/results/verification/docker_storage.json).

Metadata cơ bản `document_id: string`, `source: string`, `page: integer` truy vết về PDF vật lý 1-based. `chapter: string|null` là trường lọc hữu ích, lấy từ heading `Chương I…VI` và offset nội dung, không lấy từ gold; `chapters: string[]` ghi phạm vi thật cho chunk trộn. Ranh giới chương ở PDF trang 1, 5, 40, 48, 61, 62; trang chuyển chương không tự nhận một chương cho cả trang. Snapshot SHA256, start/end_char và model revision phục vụ tái lập. PDF page 52 là số in Công báo 53; mọi gold/trace dùng số vật lý.

Baseline Paragraph có 247 chunk chapter khác null, 62 null. Bản tái tạo giữ nguyên ID/text, sửa `luat_duong_bo_2026_p1_paragraph_800_0` có preamble trước Chương I từ I sang null, thành 246 có chapter / 63 null. Trong số null có 61 chunk chỉ header Công báo, một chunk preamble và một chunk trộn I/II tại trang 5. Chương tái tạo có thể giảm recall ở phần không phân loại được; không gán giá trị giả để filter đẹp hơn. Không thay đổi metric hay các file baseline.

[Setup/run](../../starter/README.md). Lệnh đầy đủ đã chạy từ repo root:

```bash
HF_HUB_OFFLINE=1 starter/.venv/bin/python -m starter.src.run all --output starter/results/reproduced
```

Idempotency: ingest rồi embed/upsert toàn bộ cùng nguồn lần nữa giữ 250 fixed, 309 paragraph; IDs và metadata khớp builder, không duplicate, mọi vector 384 chiều. Test nguồn thay đổi dùng tài liệu tổng hợp và embedding thật trong schema tạm: 5 chunks → 1 chunk, xóa 4 IDs lỗi thời, cập nhật text của ID còn lại; dọn schema sau kiểm tra. Không sửa PDF. [Engineering verification](../../starter/results/reproduced/engineering_verification.json). Không upsert từng minibatch vì cơ chế pruning theo tài liệu sẽ xóa chunk trước. Nguồn biến đổi cần manifest snapshot mới; tài liệu bị bỏ hoàn toàn khỏi manifest cần thao tác xóa có chủ đích, chưa tự động reconcile corpus removal.

## Cấu hình và benchmark

| Config | Index/chunking | Tham số | Metadata/filter |
|---|---|---|---|
| A | fixed_800_100 | 800 ký tự, overlap 100, riêng từng trang | Không lọc |
| B | paragraph_800 | Gộp đoạn theo dòng trống, max 800; đoạn quá dài bị cắt cứng, không overlap | Không lọc |
| C | Cùng index và embeddings B | Không tạo index C khác | Chỉ filter chapter có trong câu hỏi; câu không filter chạy như B |

Article-aware (`article_800`, 247 chunks) và paragraph overlap chỉ là thử nghiệm bổ sung, không thay A/B/C. Official A+B lưu vật lý **559 vectors**; C tái sử dụng 309 của B. Database còn 247 article và 3 fixed_test = **809 vectors**. Con số 806 là A+B+article, không phải số vectors của ba cấu hình chính thức.

[Benchmark cố định](../../starter/data/benchmark_questions.json): 20 câu, 15 DEV Q01–Q15 / 5 TEST Q16–Q20. Có direct/paraphrase/condition/exception/filter, không có câu không đáp án. Q06 Chương II, Q11 Chương III và Q17 Chương IV có filter nêu rõ ngay trong câu hỏi; A/B bỏ filter, C mới áp dụng. DEV có 2 câu filter, TEST có 1. Gold và PDF chưa thay đổi; [bảy hash khóa](../../benchmark/baseline_lock.json) đều giữ nguyên. `gold_evidence` hỗ trợ nhiều bộ thay thế, nhưng không thêm gold sau khi xem TEST. [Định nghĩa evaluator](../../benchmark/README.md).

Giới hạn provenance: bộ câu hỏi/split và kết quả đã tồn tại trước khi AI tiếp tục. Không có bằng chứng độc lập rằng học viên chốt câu hỏi và tiêu chí chọn trước lần thử đầu. TEST đã được xem trước lần hoàn thiện này. Lần chạy reproduced là kiểm chứng cùng benchmark, không phải holdout mới. Không dùng TEST để chỉnh chunking/gold/filter. Nếu làm thực nghiệm mới, đề xuất chốt trước thứ tự: Evidence Hit@3 DEV → Hit@1 DEV → grounding người học đã duyệt → tài nguyên; đây là đề xuất cho lần sau, không giả nhận đã đăng ký trước.

## Kết quả

Chạy kiểm chứng thực ngày 14/11/2026. Baseline và reproduced bằng nhau ở toàn bộ 60 bộ Top-3 IDs và các metric; metadata provenance mới được lưu riêng. [So sánh](../../starter/results/verification/baseline_comparison.json).

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian ingest | Chi phí API |
|---|---|---|---|---|---|---|
| A | DEV | 9/15 (60,0%) | 11/15 (73,3%) | 250 | 4,962 s | 0 |
| B | DEV | 7/15 (46,7%) | 11/15 (73,3%) | 309 | 3,402 s | 0 |
| C | DEV | 7/15 (46,7%) | 11/15 (73,3%) | 309 dùng chung B | Không ingest thêm | 0 |
| A | TEST | 4/5 (80%) | 4/5 (80%) | 250 | Dùng index trên | 0 |
| B | TEST | 4/5 (80%) | 4/5 (80%) | 309 | Dùng index trên | 0 |
| C | TEST | 4/5 (80%) | 4/5 (80%) | 309 dùng chung B | Dùng index B | 0 |

Thời gian chỉ của lần chạy mới, không giả lập thời gian baseline. [Ingest summary](../../starter/results/reproduced/ingest_summary.json): A tổng 176.519 ký tự (tính overlap), min/median/max=101/800/800, trung bình 706,08; B tổng 157.839 ký tự, min/median/max=3/796/800, trung bình 510,81. C không thêm vector. B nhiều hơn A 59 chunks (+23,6%) nhưng ít ký tự đưa qua model hơn vì không overlap và có header riêng. Thời gian một lượt warm cache theo thứ tự A rồi B không đủ kết luận B nhanh hơn tổng quát.

[Run metadata](../../starter/results/reproduced/all_run.json): tổng pipeline 28,880 s (gồm load, ingest, verify re-embedding và retrieval), process peak RSS 949.960.704 bytes, không gồm bộ nhớ Docker/GPU toàn hệ thống. DEV retrieval cả ba cấu hình 0,724 s, TEST 0,234 s, gồm query embedding và truy vấn; chưa đo per-config latency hoặc khoảng tin cậy. Điện/năng lượng/chi phí phần cứng chưa đo.

**Bảng AI dưới đây giữ riêng các nhãn đề xuất, không phải điểm human. Số lượng và điểm người học đã duyệt được báo riêng ngay sau bảng; grounding chỉ đo bằng chứng retrieval, không phải độ chính xác câu trả lời LLM.**

| Strategy | Coherence AI trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ | Grounding AI: số điểm 0 / 1 / 2; trung bình /2 |
|---|---|---|---|---|
| A | 1,00 (10) | 15/15 | N/A — không áp dụng | 0 / 1 / 4; 1,80 |
| B | 1,00 (10) | 15/15 | N/A — không áp dụng | 0 / 0 / 5; 2,00 |
| C | 1,00 (10) | 15/15 | TEST 1/1; DEV 2/2 | 0 / 0 / 5; 2,00 |


**Lượt AI re-assessment đã hoàn tất 15/15 grounding, 30/30 coherence và 45/45 metadata.** Đã đọc lại cả Top-3 từng câu, toàn chunk từng anchor và các trang PDF liên quan. Điểm không đổi sau tái kiểm tra, nhưng lý do được viết lại, lưu đầy đủ chunk IDs, ai_reviewer và ai_reviewed_at; người chấm là Codex AI. Không có human_score, reviewer của học viên hoặc chữ ký nào được AI tạo. Bản nhãn cũ được lưu để đối chiếu; xem [phương pháp](../../starter/results/verification/ai_assessment_method.json), [tổng hợp 5 dimensions](../../starter/results/ai_assessment_summary.md), [JSON tổng hợp](../../starter/results/ai_assessment_summary.json).

Metadata correctness và completeness đều 15/15 mỗi config trong mẫu: correctness so giá trị với PDF, completeness đo sự có mặt của trường bắt buộc. Chapter thiếu ở A không bắt buộc khi không lọc, được ghi NOT_APPLICABLE; B/C có chapter 15/15. C-Q17 filter PASS trên 3/3 records và 1/1 câu; A/B compliance NOT_APPLICABLE. [45 AI record reviews](../../starter/results/metadata_ai_review.csv) ghi PASS/FAIL/NOT_APPLICABLE riêng cho ID, nguồn, trang, truy vết, chapter và filter. Q18 B/C Top-3 ở trang 23/Chương II có metadata đúng dù không liên quan câu về học sinh; không lẫn metadata correctness với relevance.

<!-- HUMAN_REVIEW_START -->
Điểm người học dưới đây chỉ lấy từ human_score 0/1/2 có đủ human_reason, reviewer và reviewed_at; không dùng điểm AI thay thế. Trung bình chỉ tính trên các nhãn đã duyệt, chưa phải trung bình đủ mẫu nếu còn thiếu.

| Config | Grounding đã duyệt | Human 0 / 1 / 2 | Grounding human /2 | Coherence đã duyệt | Coherence human /2 |
|---|---|---|---|---|---|
| A | 5/5 | 0 / 1 / 4 | 1.80 | 10/10 | 1.00 |
| B | 5/5 | 0 / 0 / 5 | 2.00 | 10/10 | 1.00 |
| C | 5/5 | 0 / 0 / 5 | 2.00 | 10/10 | 1.00 |

Metadata được người học xác nhận: 45/45 bản ghi; trạng thái ĐÃ DUYỆT. Phiếu metadata xác nhận trọn bộ; chỉ đổi trạng thái không đủ nếu thiếu tên, ngày hoặc checkbox.
<!-- HUMAN_REVIEW_END -->

- [Grounding chi tiết](../../starter/results/manual_grounding.md): đọc đủ ba chunk của cả 15 trường hợp, đối chiếu câu hỏi/đáp án/gold. A-Q16=1 vì thiếu vế giấy vận tải là bằng chứng hợp đồng. B/C-Q16=2 vì chunk chứa đủ định nghĩa. B/C-Q19=2 dù Evidence Hit@3=0: Top-3 có chủ thể Điều 73 và đầu khoản 2, Top-1 có danh sách dịch vụ gồm sửa chữa, cùng trang; AI đánh giá đủ bằng chứng khi đọc chung. Không ghép để tính hit tự động. Các câu Q17/Q18/Q20 có lập luận và chỉ rõ phần không liên quan trong từng trace, không chỉ quy đổi từ metric.
- [Coherence](../../starter/results/chunk_coherence.md): chọn trước khi chấm 10 useful pages đầu (2–11), anchor=floor(len(normalized_page)/2), chọn chunk_index thấp nhất phủ anchor khi overlap. Mỗi chunk được đọc riêng, không cosine. C=B do cùng chunk. Các mẫu đều mức 1 vì có ý đọc được nhưng đứt đầu/cuối hoặc thiếu điều kiện; mẫu nhỏ, tập trung đầu tài liệu và giữa trang, không suy ra toàn corpus. [Vị trí nguồn](../../starter/results/coherence_positions.json), [30 chunk snapshots](../../starter/results/verification/coherence_selected_chunks.json).
- [Metadata](../../starter/results/metadata_usefulness.md): 5 TEST × Top-3 × 3 = 45 records đúng document_id/source/page và nội dung có trên trang PDF, chapter đúng khi có/được yêu cầu. A baseline không có chapter trong 15 hits nhưng không lọc nên không coi thiếu trường bắt buộc. B/C 15/15 có chapter. Compliance chỉ tính câu thực áp dụng filter: C-Q17=1/1, DEV C-Q06/Q11=2/2. Q11 tuân thủ chapter III nhưng Evidence Hit@3=0; compliance không chứng minh retrieval chính xác. [Filter checks](../../starter/results/verification/filter_validation.json).

Trace đầy đủ: baseline [DEV](../../starter/results/dev_traces.json), [TEST](../../starter/results/test_traces.json); reproduced [DEV](../../starter/results/reproduced/dev_traces.json), [TEST](../../starter/results/reproduced/test_traces.json). Điểm chỉnh/dựng lại trong [grounding CSV](../../starter/results/grounding_review.csv), [coherence CSV](../../starter/results/coherence_review.csv), [metadata review](../../starter/results/metadata_human_review.md). Trường human_score/human_reason/reviewer/reviewed_at cho phép duyệt mà không xóa nhãn AI; `python -m src.audit` báo riêng số đã duyệt và trung bình human. Nguy cơ thiên lệch: AI vừa hỗ trợ code vừa đề xuất nhãn, không blind theo chiến lược và đã xem gold; cần người học kiểm tra độc lập.

## Phân tích và kết luận

**A–B, chunking:** DEV Hit@1 giảm 2/15 khi chuyển A→B, Evidence Hit@3 cùng 11/15 nhưng không cùng lỗi. A miss Q01/Q09/Q10/Q12; B miss Q10/Q11/Q12/Q14. B phục hồi Q01/Q09 và mất Q11/Q14. TEST A miss Q16; B miss Q19. Vì PDF ít dòng trống, paragraph_800 thường gặp đoạn vượt 800 rồi cắt cứng; tên “paragraph” không đảm bảo trọn câu. A có overlap cứu một số điều kiện nhưng vẫn cắt từ và tăng số ký tự embed. B có 61 header-only chunks và đoạn rất ngắn (3 ký tự), là chi phí và nhiễu có thể giảm trong thực nghiệm DEV mới. Không thay baseline để che lỗi.

**B–C, metadata:** cùng chunks/model/store/gold, chỉ khác filter có nguồn từ câu hỏi. Aggregate DEV/TEST không đổi; Q06 Top-3 đổi sau filter nhưng hit vẫn giữ. Q11/Q17 Top-3 giữ; các câu không filter giống B. Một PDF và TEST toàn Chương IV khiến khó chứng minh lợi ích lọc; muốn đánh giá tốt hơn cần tập câu đa chương/tài liệu chưa dùng chỉnh và mẫu filter lớn hơn. Không kết luận metadata vô dụng chỉ vì metric bằng nhau: source/page truy vết được và chapter kiểm soát phạm vi, nhưng null có thể loại bằng chứng đúng.

[Chẩn đoán chi tiết với text, ID và trang](../../starter/results/verification/error_analysis.json):

| Câu | Minh chứng | Chẩn đoán |
|---|---|---|
| Q09 DEV | p40_paragraph_800_1 giữ đủ Điều 44; A Top-3 là p47_fixed_2, p41_fixed_1, p40_fixed_2 | B/C Top-1 hit; A vừa không có một fixed chunk chứa trọn gold dài, vừa xếp các đoạn vận hành/đầu tư/tiêu chuẩn vào Top-3. Không coi đúng trang 40 là đủ hit. |
| Q10 DEV | p43_fixed_1/_2; p43_paragraph_800_2/_3 | Gold danh sách hai loại cao tốc bị tách; một chunk thiếu đầu điều kiện, chunk kia thiếu kết thúc. Không một chunk đúng trang chứa trọn gold. |
| Q11 DEV | p44_fixed_2 hit; p44_paragraph_800_2/_3 miss | Paragraph có mốc 60 phút nhưng cắt cuối câu “quyết định của mình”; gold đầy đủ không nằm trong một chunk. Filter chương đúng không sửa được split evidence. |
| Q12 DEV | p45_fixed_1; p45_paragraph_800_1/_2 | Gold về trạm dừng nghỉ dài, nằm qua ranh giới chunk; đúng trang/chủ đề vẫn không phải hit chính thức. |
| Q14 DEV | p50_paragraph_800_1 kết thúc “dịch vụ”, _2 bắt đầu “vận tải;” và không vào Top-3 | Snapshot DB không có Paragraph chunk chứa trọn exact gold; đây đồng thời là split evidence và thiếu phần tiếp trong retrieval. Fixed p50_fixed_1 và supplemental article_57_0 mới có đủ. Không giữ chẩn đoán ban đầu rằng full evidence đã có trong một Paragraph chunk nhưng chỉ xếp hạng thấp. |
| Q16 TEST | p52_fixed_2 dừng “là b ằng ch”; p52_paragraph_800_3 đủ | A không đủ vế chức năng hợp đồng, grounding AI 1; B/C giữ đủ, grounding 2. |
| Q19 TEST | p58_fixed_2 đủ; p58_paragraph_800_2/_3 tách chủ thể/danh sách | A hit; B/C exact miss nhưng top-3 đọc chung có đủ ý, grounding AI đề xuất 2, cần người học duyệt. |

Prefix `luat_duong_bo_2026_` được lược trong bảng cho dễ đọc; JSON/trace lưu đầy đủ. Q14 đã được kiểm tra cả snapshot trước thay đổi lẫn text builder trùng baseline; không sửa gold để biến miss thành hit.

Exact-match chỉ NFC/casefold/gộp whitespace, không hiểu ngữ nghĩa; khoảng trắng chen giữa từ, gold quá rộng hoặc bằng chứng hợp lệ khác chưa gán nhãn gây false negative. Nhiều bộ gold thay thế được hỗ trợ trong code nhưng chỉ người chấm xác nhận mới được coi là equivalent; không tự gộp Top-3 cho metric chính. Gold nguồn/trang chỉ là điều kiện cần. Điểm thấp có thể phản ánh chunking và chính sách nhãn cùng lúc.

Nếu cần chọn cấu hình vận hành tạm thời trên corpus này, đề xuất A vì DEV Hit@3 bằng B/C, Hit@1 cao hơn và ít vectors hơn; B/C có grounding AI tốt hơn trong 5 TEST và giữ trọn một số định nghĩa, cần người học xác nhận trước quyết định cuối. Đây là quyết định mô tả sau khi đã biết TEST, không tuyên bố lựa chọn trước TEST hay A tốt nhất tổng quát. Năm câu TEST, cùng chủ đề với DEV (còn chung trang 52), không độc lập hoàn toàn; chưa có khoảng tin cậy hay phép kiểm định khác biệt. Coherence cùng điểm không đủ kết luận hai chunking ngang nhau.

Cải tiến cho lần nghiên cứu mới: bỏ header và chú thích có kiểm chứng, sentence/article-aware chunk có overlap, giữ điều kiện/ngoại lệ cùng chủ thể và đánh giá chapter spans khi chunk qua ranh giới; chọn tham số chỉ trên DEV. Sau khi chốt phải tạo TEST mới chưa xem, nhiều chương/tài liệu và nhiều câu filter. Article/overlap hiện chỉ là phương án bổ sung, chưa benchmark đầy đủ theo cùng contract nên không báo là cấu hình đã thắng.


Rà soát kỹ thuật cuối: [bộ tests cuối khi nộp](../../starter/results/verification/submission_unit_tests.txt), gồm kiểm tra AI không biến thành human, missing optional/required chapter và trường hợp filter không trả kết quả. Phát hiện và sửa lỗi exporter metadata đọc `rows[0]` khi toàn bộ retrieval rỗng; khi rỗng vẫn xuất CSV header, filter compliance không được tính 100% theo phép đúng rỗng. Fixture thiếu rank đã được sửa trong test, không phải lỗi của trace thật. Không refactor chunking/model/store hoặc chỉnh gold để nâng điểm.

Lần kiểm chứng pipeline mới tại [mission_check](../../starter/results/mission_check/all_run.json) dùng cùng model thật và PostgreSQL, chạy lại ingest, idempotency, nguồn thay đổi trong schema tạm, DEV/TEST và report. Kết quả so sánh tại [mission_validation.json](../../starter/results/verification/mission_validation.json). Bảng thời gian/chi phí ở trên vẫn là số của reproduced cũ, không bị thay bằng lượt mới.

Bài học rút ra: (1) tên paragraph không bảo đảm trọn câu nếu PDF thiếu ranh giới đoạn; (2) metadata đúng và lọc đúng không cứu được gold bị tách; (3) grounding Top-3 và exact hit một chunk đo hai điều khác nhau; (4) nhãn AI cần provenance và kiểm tra độc lập, không thay chữ ký của người học; (5) hướng dẫn tải nguồn/checksum chưa tự hoàn thành yêu cầu chia sẻ toàn bộ artifacts.

Hoàn tất phần kỹ thuật/AI assessment; các phiếu đã ghi nhận grounding human 15/15, coherence human 30/30 và metadata 45/45 theo dữ liệu học viên tự nhập. Phạm vi nộp loại PDF gốc và source extract toàn nguồn, đồng thời giữ đủ benchmark/gold/trace/audit được phép theo căn cứ nội dung luật. Việc nộp link qua kênh lớp được ghi nhận riêng với việc đưa code lên GitHub. Không có mục nào được đánh dấu đã nộp chỉ vì code/tests qua.

AI hỗ trợ bằng Codex; toàn bộ số liệu run/embedding/store là thực, không mock, nhãn audit ghi rõ AI đề xuất. Các phiếu human đã được học viên điền đủ và lớp L3B đã được cung cấp. Thông tin repo/commit chốt ở STUDENT.md; học viên còn thực hiện nộp link qua kênh lớp. [Đối chiếu rubric và công việc còn lại](../../starter/results/submission_checklist.md).
