# Chunk coherence — cùng 10 vị trí nguồn

Nhãn AI đề xuất — CHƯA phải chấm thủ công bởi người học. Chỉ đánh giá evidence retrieval, không phải độ chính xác câu trả lời LLM.

Bản Markdown bỏ khoảng trắng cuối dòng để trình bày; text gốc đầy đủ được giữ trong snapshot JSON.

Trước khi chấm: 10 useful page IDs đầu theo thứ tự (2–11); lấy offset floor(len(normalized_page)/2). Khi overlap, chọn chunk_index thấp nhất chứa offset. Không dựa retrieval/cosine.

Chấm toàn chunk riêng lẻ, không ghép chunk lân cận. 0: không hiểu vì đứt ý/chủ thể; 1: hiểu một phần nhưng thiếu ngữ cảnh; 2: tự hiểu và giữ trọn ý. Không dùng cosine. B=C vì cùng chunk/embedding; filter chỉ ảnh hưởng retrieval.

Mẫu đầu corpus và offset giữa trang thiên về các đoạn bị cắt; không đại diện mọi chương. Tất cả 10 mẫu còn ý đọc được nhưng thiếu đầu/cuối hoặc điều kiện, nên đề xuất mức 1; không suy ra hai chiến lược tương đương trên toàn bộ corpus.

Duyệt/sửa trong `coherence_review.csv`, điền human_score/human_reason/reviewer/reviewed_at rồi chạy `python -m src.audit`.

| Config | n | AI số điểm 0 / 1 / 2 | AI trung bình /2 | Người học duyệt |
|---|---|---|---|---|
| A | 10 | 0 / 10 / 0 | 1.00 | 10/10 |
| B | 10 | 0 / 10 / 0 | 1.00 | 10/10 |
| C | 10 | 0 / 10 / 0 | 1.00 | 10/10 |

## P02 — Config A

`luat_duong_bo_2026_p2_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 2; anchor 1183; chunk [700, 1500).

**AI đề xuất: 1/2.** Các khoản 4 và 5 vẫn tự giải thích kết cấu hạ tầng/hành lang, nhưng đầu bắt giữa từ “thuộc” của danh sách công trình và cuối dừng ở chức năng quản lý chưa hoàn tất khoản 6. Còn ý hiểu được, không giữ trọn toàn chunk. Đã đọc toàn bộ luat_duong_bo_2026_p2_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 2; đầu='u ộc hệ thống quản lý giao\nthông th'; cuối=' trưởng\nBộ Xây dựng thực hiện chức năng quản '.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Giữ được nội dung chính về hạ tầng và hành lang nhưng phần đầu và khoản 6 ở cuối bị cắt, nên chỉ đủ một phần.

```text
u ộc hệ thống quản lý giao
thông thông minh; nhà h ạt quản lý đường bộ; kho chứa trang thiết bị, vật tư dự
phòng trong lĩnh vực đường bộ; công trình kiểm soát tải trọng xe; trạm thu phí và
các công trình khác của đường bộ.
4. Kết cấu hạ tầng đường bộ bao gồm: công trình đường bộ; bến xe; bãi đỗ
xe; trạm dừng nghỉ; điểm dừng xe, đỗ xe; đất của đường bộ; hành lang an toàn
đường bộ và các công trình phụ trợ phục vụ cho hoạt động đường bộ.
5. Hành lang an toàn đường bộ là dải đất dọc hai bên đất của đường bộ, tính
từ mép ngoài phần đất để bảo vệ, bảo trì đường bộ ra hai bên để bảo đảm an toàn
giao thông đường bộ, bảo đảm tầm nhìn xe chạy và hạn chế ảnh hưởng đến môi
trường xung quanh.
6.2 Cơ quan quản lý đường bộ là cơ quan thuộc Bộ Xây dựng giúp Bộ trưởng
Bộ Xây dựng thực hiện chức năng quản
```

## P02 — Config B

`luat_duong_bo_2026_p2_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 2; anchor 1183; chunk [840, 1640).

**AI đề xuất: 1/2.** Các khoản 4–6 rõ chủ thể và nội dung, nhưng đầu chỉ còn đuôi danh sách công trình và cuối cắt ngay trong “đường” ở khoản 7. Ngữ cảnh đầu và định nghĩa cuối đều thiếu; không thể cho mức 2 toàn chunk. Đã đọc toàn bộ luat_duong_bo_2026_p2_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 2; đầu='ng trình kiểm soát tải trọng xe; tr'; cuối='ân dân cấp xã.\n7. Người quản lý, sử dụng đườn'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Khoản 4 đến 6 tương đối rõ nhưng đoạn mở đầu và phần khoản 7 ở cuối bị thiếu, nên chưa trọn ý.

```text
ng trình kiểm soát tải trọng xe; trạm thu phí và
các công trình khác của đường bộ.
4. Kết cấu hạ tầng đường bộ bao gồm: công trình đường bộ; bến xe; bãi đỗ
xe; trạm dừng nghỉ; điểm dừng xe, đỗ xe; đất của đường bộ; hành lang an toàn
đường bộ và các công trình phụ trợ phục vụ cho hoạt động đường bộ.
5. Hành lang an toàn đường bộ là dải đất dọc hai bên đất của đường bộ, tính
từ mép ngoài phần đất để bảo vệ, bảo trì đường bộ ra hai bên để bảo đảm an toàn
giao thông đường bộ, bảo đảm tầm nhìn xe chạy và hạn chế ảnh hưởng đến môi
trường xung quanh.
6.2 Cơ quan quản lý đường bộ là cơ quan thuộc Bộ Xây dựng giúp Bộ trưởng
Bộ Xây dựng thực hiện chức năng quản lý nhà nước về hoạt động đường bộ; cơ
quan chuyên môn thuộc Ủy ban nhân dân cấp tỉnh; Ủy ban nhân dân cấp xã.
7. Người quản lý, sử dụng đườn
```

## P02 — Config C

`luat_duong_bo_2026_p2_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 2; anchor 1183; chunk [840, 1640).

**AI đề xuất: 1/2.** Các khoản 4–6 rõ chủ thể và nội dung, nhưng đầu chỉ còn đuôi danh sách công trình và cuối cắt ngay trong “đường” ở khoản 7. Ngữ cảnh đầu và định nghĩa cuối đều thiếu; không thể cho mức 2 toàn chunk. Đã đọc toàn bộ luat_duong_bo_2026_p2_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 2; đầu='ng trình kiểm soát tải trọng xe; tr'; cuối='ân dân cấp xã.\n7. Người quản lý, sử dụng đườn'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung giống B, phần đầu và cuối vẫn bị cắt nên mức độ đầy đủ không thay đổi.

```text
ng trình kiểm soát tải trọng xe; trạm thu phí và
các công trình khác của đường bộ.
4. Kết cấu hạ tầng đường bộ bao gồm: công trình đường bộ; bến xe; bãi đỗ
xe; trạm dừng nghỉ; điểm dừng xe, đỗ xe; đất của đường bộ; hành lang an toàn
đường bộ và các công trình phụ trợ phục vụ cho hoạt động đường bộ.
5. Hành lang an toàn đường bộ là dải đất dọc hai bên đất của đường bộ, tính
từ mép ngoài phần đất để bảo vệ, bảo trì đường bộ ra hai bên để bảo đảm an toàn
giao thông đường bộ, bảo đảm tầm nhìn xe chạy và hạn chế ảnh hưởng đến môi
trường xung quanh.
6.2 Cơ quan quản lý đường bộ là cơ quan thuộc Bộ Xây dựng giúp Bộ trưởng
Bộ Xây dựng thực hiện chức năng quản lý nhà nước về hoạt động đường bộ; cơ
quan chuyên môn thuộc Ủy ban nhân dân cấp tỉnh; Ủy ban nhân dân cấp xã.
7. Người quản lý, sử dụng đườn
```

## P03 — Config A

`luat_duong_bo_2026_p3_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 3; anchor 1357; chunk [700, 1500).

**AI đề xuất: 1/2.** Có ý huy động nguồn lực và ưu tiên tuyến cao tốc, nhưng mất đầu điều kiện môi trường/chủ thể chính sách; cuối cắt giữa từ “hợp” trong mục tiêu kết hợp quốc phòng. Không xác định trọn phạm vi danh sách chính sách chỉ từ chunk. Đã đọc toàn bộ luat_duong_bo_2026_p3_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 3; đầu='ng với biến đổi khí hậu, thân thiện'; cuối='ới, đường ven biển để phục vụ mục tiêu\nkết hợ'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đọc được chính sách huy động nguồn lực nhưng mất ngữ cảnh đầu và phần kết hợp quốc phòng ở cuối.

```text
ng với biến đổi khí hậu, thân thiện với môi trường; kết nối đồng bộ các tuyến
đường bộ, các phương thức vận tải khác với vận tải đường bộ;
b) Xây dựng cơ chế đẩy mạnh huy động các nguồn lực xã hội, đa dạng các
hình thức, phương thức đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì kết
cấu hạ tầng đường bộ;
c) Ưu tiên phát tri ển các tuyến đường cao tốc, các công trình, dự án đường
bộ trọng điểm kết nối vùng, khu vực, đô thị lớn, trung tâm trong nước và quốc tế;
kết cấu hạ tầng đường bộ vùng đồng bào dân tộc thiểu số, miền núi, hải đảo, biên
giới; kết cấu hạ tầng đường bộ dễ tiếp cận và bảo đảm an toàn cho các đối tượng
dễ bị tổn thương; k ết cấu hạ tầng đường bộ tại các đô th ị để giảm ùn t ắc giao
thông; các tuyến đường tuần tra biên gi ới, đường ven biển để phục vụ mục tiêu
kết hợ
```

## P03 — Config B

`luat_duong_bo_2026_p3_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 3; anchor 1357; chunk [840, 1640).

**AI đề xuất: 1/2.** Giữ phần ưu tiên và mục tiêu quốc phòng trọn hơn A, song đầu mất ký hiệu/chủ thể của điểm b và cuối bỏ dở môi trường cạnh tranh khoản 2. Nội dung hiểu được từng ý, chưa tự chứa toàn bộ phạm vi/điều kiện. Đã đọc toàn bộ luat_duong_bo_2026_p3_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 3; đầu=') Xây dựng cơ chế đẩy mạnh huy động'; cuối='ình kinh doanh v ận tải; tạo môi trường cạnh\n'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung chính rõ hơn A, nhưng phần đầu và cuối khoản 2 chưa đầy đủ.

```text
) Xây dựng cơ chế đẩy mạnh huy động các nguồn lực xã hội, đa dạng các
hình thức, phương thức đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì kết
cấu hạ tầng đường bộ;
c) Ưu tiên phát tri ển các tuyến đường cao tốc, các công trình, dự án đường
bộ trọng điểm kết nối vùng, khu vực, đô thị lớn, trung tâm trong nước và quốc tế;
kết cấu hạ tầng đường bộ vùng đồng bào dân tộc thiểu số, miền núi, hải đảo, biên
giới; kết cấu hạ tầng đường bộ dễ tiếp cận và bảo đảm an toàn cho các đối tượng
dễ bị tổn thương; k ết cấu hạ tầng đường bộ tại các đô th ị để giảm ùn t ắc giao
thông; các tuyến đường tuần tra biên gi ới, đường ven biển để phục vụ mục tiêu
kết hợp phát triển kinh tế - xã hội với bảo đảm quốc phòng, an ninh.
2. Phát triển hợp lý các lo ại hình kinh doanh v ận tải; tạo môi trường cạnh
```

## P03 — Config C

`luat_duong_bo_2026_p3_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 3; anchor 1357; chunk [840, 1640).

**AI đề xuất: 1/2.** Giữ phần ưu tiên và mục tiêu quốc phòng trọn hơn A, song đầu mất ký hiệu/chủ thể của điểm b và cuối bỏ dở môi trường cạnh tranh khoản 2. Nội dung hiểu được từng ý, chưa tự chứa toàn bộ phạm vi/điều kiện. Đã đọc toàn bộ luat_duong_bo_2026_p3_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 3; đầu=') Xây dựng cơ chế đẩy mạnh huy động'; cuối='ình kinh doanh v ận tải; tạo môi trường cạnh\n'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Các đoạn trùng B và vẫn thiếu ngữ cảnh hai đầu, nên giữ mức 1.

```text
) Xây dựng cơ chế đẩy mạnh huy động các nguồn lực xã hội, đa dạng các
hình thức, phương thức đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì kết
cấu hạ tầng đường bộ;
c) Ưu tiên phát tri ển các tuyến đường cao tốc, các công trình, dự án đường
bộ trọng điểm kết nối vùng, khu vực, đô thị lớn, trung tâm trong nước và quốc tế;
kết cấu hạ tầng đường bộ vùng đồng bào dân tộc thiểu số, miền núi, hải đảo, biên
giới; kết cấu hạ tầng đường bộ dễ tiếp cận và bảo đảm an toàn cho các đối tượng
dễ bị tổn thương; k ết cấu hạ tầng đường bộ tại các đô th ị để giảm ùn t ắc giao
thông; các tuyến đường tuần tra biên gi ới, đường ven biển để phục vụ mục tiêu
kết hợp phát triển kinh tế - xã hội với bảo đảm quốc phòng, an ninh.
2. Phát triển hợp lý các lo ại hình kinh doanh v ận tải; tạo môi trường cạnh
```

## P04 — Config A

`luat_duong_bo_2026_p4_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 4; anchor 1272; chunk [700, 1500).

**AI đề xuất: 1/2.** Thời kỳ 10 năm, tầm nhìn 20–30 năm và rà soát 5 năm đọc được; đầu là mảnh cuối nội dung quy hoạch và cuối cắt giữa câu nội dung phát triển đô thị. Các ý độc lập có ích nhưng ranh giới không trọn. Đã đọc toàn bộ luat_duong_bo_2026_p4_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 4; đầu='án\nkết nối đường bộ với các phương '; cuối=' pháp luật có liên quan.\nNội dung về phát tri'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Các mốc thời gian quy hoạch đọc được, nhưng phần mở đầu và nội dung cuối không trọn vẹn.

```text
án
kết nối đường bộ với các phương thức vận tải khác, kết nối với hệ thống đô thị,
khu kinh tế, khu công nghiệp; xác định nhu cầu sử dụng đất, nhu cầu vốn đầu tư,
lộ trình thực hiện quy hoạch; giải pháp thực hiện quy hoạch;
c)4 Bộ Xây dựng tổ chức lập quy hoạch kết cấu hạ tầng đường bộ.
3. Thời kỳ quy hoạch kết cấu hạ tầng đường bộ là 10 năm, t ầm nhìn từ 20
năm đến 30 năm.
Quy hoạch kết cấu hạ tầng đường bộ được rà soát theo đ ịnh kỳ 05 năm để
điều chỉnh phù hợp với tình hình phát triển kinh tế - xã hội trong từng giai đoạn
và được công bố công khai.
4. Ủy ban nhân dân cấp tỉnh tổ chức lập nội dung về phát triển đường bộ trong
phương án phát triển mạng lưới giao thông trong quy hoạch theo quy định của pháp
luật về quy hoạch và quy định khác của pháp luật có liên quan.
Nội dung về phát tri
```

## P04 — Config B

`luat_duong_bo_2026_p4_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 4; anchor 1272; chunk [840, 1640).

**AI đề xuất: 1/2.** Khoản 3 và chủ thể UBND tại khoản 4 đủ ý, nhưng đầu cắt nhu cầu vốn và cuối cắt câu dẫn pháp luật liên quan của phát triển đô thị. Đánh giá toàn chunk còn thiếu đầu/cuối, không chấm riêng câu dễ hiểu. Đã đọc toàn bộ luat_duong_bo_2026_p4_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 4; đầu='t, nhu cầu vốn đầu tư,\nlộ trình thự'; cuối='hị và quy đ ịnh khác c ủa pháp lu ật có\nliên '.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Khoản 3 và 4 tương đối rõ nhưng phần vốn đầu tư và quy định cuối bị cắt.

```text
t, nhu cầu vốn đầu tư,
lộ trình thực hiện quy hoạch; giải pháp thực hiện quy hoạch;
c)4 Bộ Xây dựng tổ chức lập quy hoạch kết cấu hạ tầng đường bộ.
3. Thời kỳ quy hoạch kết cấu hạ tầng đường bộ là 10 năm, t ầm nhìn từ 20
năm đến 30 năm.
Quy hoạch kết cấu hạ tầng đường bộ được rà soát theo đ ịnh kỳ 05 năm để
điều chỉnh phù hợp với tình hình phát triển kinh tế - xã hội trong từng giai đoạn
và được công bố công khai.
4. Ủy ban nhân dân cấp tỉnh tổ chức lập nội dung về phát triển đường bộ trong
phương án phát triển mạng lưới giao thông trong quy hoạch theo quy định của pháp
luật về quy hoạch và quy định khác của pháp luật có liên quan.
Nội dung về phát triển đường bộ đô thị được xác định trong quy hoạch theo
quy định của pháp lu ật về quy hoạch đô thị và quy đ ịnh khác c ủa pháp lu ật có
liên
```

## P04 — Config C

`luat_duong_bo_2026_p4_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 4; anchor 1272; chunk [840, 1640).

**AI đề xuất: 1/2.** Khoản 3 và chủ thể UBND tại khoản 4 đủ ý, nhưng đầu cắt nhu cầu vốn và cuối cắt câu dẫn pháp luật liên quan của phát triển đô thị. Đánh giá toàn chunk còn thiếu đầu/cuối, không chấm riêng câu dễ hiểu. Đã đọc toàn bộ luat_duong_bo_2026_p4_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 4; đầu='t, nhu cầu vốn đầu tư,\nlộ trình thự'; cuối='hị và quy đ ịnh khác c ủa pháp lu ật có\nliên '. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung trùng B, vẫn mất thông tin ở ranh giới đoạn nên chỉ đạt mức 1.

```text
t, nhu cầu vốn đầu tư,
lộ trình thực hiện quy hoạch; giải pháp thực hiện quy hoạch;
c)4 Bộ Xây dựng tổ chức lập quy hoạch kết cấu hạ tầng đường bộ.
3. Thời kỳ quy hoạch kết cấu hạ tầng đường bộ là 10 năm, t ầm nhìn từ 20
năm đến 30 năm.
Quy hoạch kết cấu hạ tầng đường bộ được rà soát theo đ ịnh kỳ 05 năm để
điều chỉnh phù hợp với tình hình phát triển kinh tế - xã hội trong từng giai đoạn
và được công bố công khai.
4. Ủy ban nhân dân cấp tỉnh tổ chức lập nội dung về phát triển đường bộ trong
phương án phát triển mạng lưới giao thông trong quy hoạch theo quy định của pháp
luật về quy hoạch và quy định khác của pháp luật có liên quan.
Nội dung về phát triển đường bộ đô thị được xác định trong quy hoạch theo
quy định của pháp lu ật về quy hoạch đô thị và quy đ ịnh khác c ủa pháp lu ật có
liên
```

## P05 — Config A

`luat_duong_bo_2026_p5_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 5; anchor 1062; chunk [700, 1500).

**AI đề xuất: 1/2.** Tiêu đề Điều 7 cùng các cấm ở khoản 1–4 rõ ràng, nhưng đầu còn mảnh Điều 6 và cuối khoản 5 chỉ còn “bằng x”, mất phương tiện và điều kiện giấy phép. Không được khôi phục phần thiếu từ hiểu biết về luật. Đã đọc toàn bộ luat_duong_bo_2026_p5_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 5; đầu=' khác có liên quan.\n3. Chính phủ qu'; cuối='\nhiệu đường bộ.\n5. Kinh doanh v ận tải bằng x'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nêu được các hành vi bị cấm ở khoản 1 đến 4, nhưng khoản 5 bị cắt giữa nội dung.

```text
 khác có liên quan.
3. Chính phủ quy định chi tiết khoản 1 và khoản 2 Điều này; quy định việc
thu thập, quản lý, khai thác thông tin trong cơ sở dữ liệu đường bộ.
Điều 7. Các hành vi bị nghiêm cấm
1. Phá ho ại kết cấu hạ tầng đường bộ; khai thác, s ử dụng kết cấu hạ tầng
đường bộ trái quy định của pháp luật.
2. Đấu nối trái phép vào đường chính, đường nhánh; tháo dỡ, di chuyển trái
phép hoặc làm sai lệch công trình đường bộ.
3. Lấn, chiếm, sử dụng, xây dựng trái phép trong phạm vi bảo vệ kết cấu hạ
tầng đường bộ.
4. Lắp đặt, tháo dỡ, di chuyển, điều chỉnh, che khuất báo hiệu đường bộ trái
quy định của pháp lu ật; gắn, treo, l ắp vào báo hi ệu đường bộ nội dung không
liên quan t ới ý nghĩa, m ục đích c ủa báo hi ệu đường bộ hoặc làm sai l ệch báo
hiệu đường bộ.
5. Kinh doanh v ận tải bằng x
```

## P05 — Config B

`luat_duong_bo_2026_p5_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 5; anchor 1062; chunk [840, 1640).

**AI đề xuất: 1/2.** Điều 7 và khoản 1–4 đủ, đầu còn đuôi Điều 6, cuối khoản 5 dừng ở “kinh doanh không đúng”, mất đối tượng/phạm vi cấm. Chunk chứa ý rõ nhưng chưa bảo toàn điều kiện của ý cuối. Đã đọc toàn bộ luat_duong_bo_2026_p5_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 5; đầu='ơ sở dữ liệu đường bộ.\nĐiều 7. Các '; cuối='ịnh của pháp lu ật hoặc kinh\ndoanh không đúng'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Điều 7 và bốn khoản đầu dễ hiểu nhưng khoản 5 chưa nêu hết phạm vi cấm.

```text
ơ sở dữ liệu đường bộ.
Điều 7. Các hành vi bị nghiêm cấm
1. Phá ho ại kết cấu hạ tầng đường bộ; khai thác, s ử dụng kết cấu hạ tầng
đường bộ trái quy định của pháp luật.
2. Đấu nối trái phép vào đường chính, đường nhánh; tháo dỡ, di chuyển trái
phép hoặc làm sai lệch công trình đường bộ.
3. Lấn, chiếm, sử dụng, xây dựng trái phép trong phạm vi bảo vệ kết cấu hạ
tầng đường bộ.
4. Lắp đặt, tháo dỡ, di chuyển, điều chỉnh, che khuất báo hiệu đường bộ trái
quy định của pháp lu ật; gắn, treo, l ắp vào báo hi ệu đường bộ nội dung không
liên quan t ới ý nghĩa, m ục đích c ủa báo hi ệu đường bộ hoặc làm sai l ệch báo
hiệu đường bộ.
5. Kinh doanh v ận tải bằng xe ô tô, b ằng xe bốn bánh có gắn động cơ mà
không có gi ấy phép kinh doanh v ận tải theo quy đ ịnh của pháp lu ật hoặc kinh
doanh không đúng
```

## P05 — Config C

`luat_duong_bo_2026_p5_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 5; anchor 1062; chunk [840, 1640).

**AI đề xuất: 1/2.** Điều 7 và khoản 1–4 đủ, đầu còn đuôi Điều 6, cuối khoản 5 dừng ở “kinh doanh không đúng”, mất đối tượng/phạm vi cấm. Chunk chứa ý rõ nhưng chưa bảo toàn điều kiện của ý cuối. Đã đọc toàn bộ luat_duong_bo_2026_p5_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 5; đầu='ơ sở dữ liệu đường bộ.\nĐiều 7. Các '; cuối='ịnh của pháp lu ật hoặc kinh\ndoanh không đúng'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Giống cấu hình B, phần khoản 5 không đủ ý để chấm mức 2.

```text
ơ sở dữ liệu đường bộ.
Điều 7. Các hành vi bị nghiêm cấm
1. Phá ho ại kết cấu hạ tầng đường bộ; khai thác, s ử dụng kết cấu hạ tầng
đường bộ trái quy định của pháp luật.
2. Đấu nối trái phép vào đường chính, đường nhánh; tháo dỡ, di chuyển trái
phép hoặc làm sai lệch công trình đường bộ.
3. Lấn, chiếm, sử dụng, xây dựng trái phép trong phạm vi bảo vệ kết cấu hạ
tầng đường bộ.
4. Lắp đặt, tháo dỡ, di chuyển, điều chỉnh, che khuất báo hiệu đường bộ trái
quy định của pháp lu ật; gắn, treo, l ắp vào báo hi ệu đường bộ nội dung không
liên quan t ới ý nghĩa, m ục đích c ủa báo hi ệu đường bộ hoặc làm sai l ệch báo
hiệu đường bộ.
5. Kinh doanh v ận tải bằng xe ô tô, b ằng xe bốn bánh có gắn động cơ mà
không có gi ấy phép kinh doanh v ận tải theo quy đ ịnh của pháp lu ật hoặc kinh
doanh không đúng
```

## P06 — Config A

`luat_duong_bo_2026_p6_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 6; anchor 1223; chunk [700, 1500).

**AI đề xuất: 1/2.** Định nghĩa đường thôn, đô thị, chuyên dùng và đường địa phương còn trọn; đầu mất chủ thể đường xã, cuối chỉ dẫn danh sách trách nhiệm UBND chưa có các loại đường. Thiếu ngữ cảnh để hiểu toàn bộ chunk. Đã đọc toàn bộ luat_duong_bo_2026_p6_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 6; đầu=' với sự phát triển kinh tế\n- xã hội'; cuối='ỉnh có trách nhiệm quản lý các loại đường sau'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Một số loại đường được định nghĩa rõ nhưng thiếu phần đầu về đường xã và cuối về trách nhiệm quản lý.

```text
 với sự phát triển kinh tế
- xã hội của xã;
d) Đường thôn là đư ờng trong khu v ực thôn; đư ờng trục nối thôn v ới khu
vực sản xuất nông nghiệp, lâm nghiệp và cơ sở sản xuất, kinh doanh khác trên địa
bàn thôn;
đ) Đường đô thị là đường trong phạm vi địa giới hành chính nội thành, nội
thị, bao gồm: đường cao tốc đô thị, đường phố, đường ngõ, ngách, kiệt, hẻm trong
đô thị;
e) Đường chuyên dùng là đư ờng chuyên phục vụ giao thông cho m ột hoặc
một số cơ quan, tổ chức, cá nhân và đường nội bộ.
2. Đường địa phương bao gồm: đường tỉnh, đường đô thị, đường xã, đường thôn.
3. Bộ Xây dựng có trách nhi ệm quản lý qu ốc lộ, trừ quốc lộ quy định tại
điểm a khoản 4 Điều này và đường gom, đường bên quy định tại điểm c khoản 4
Điều này.
4. Ủy ban nhân dân cấp tỉnh có trách nhiệm quản lý các loại đường sau
```

## P06 — Config B

`luat_duong_bo_2026_p6_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 6; anchor 1223; chunk [840, 1640).

**AI đề xuất: 1/2.** Đường đô thị/chuyên dùng và trách nhiệm Bộ Xây dựng đọc được, nhưng mất đầu định nghĩa đường thôn; cuối cắt điều kiện của quốc lộ hoàn thành đầu tư. Chỉ hiểu được một phần các nhánh quản lý. Đã đọc toàn bộ luat_duong_bo_2026_p6_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 6; đầu='iệp, lâm nghiệp và cơ sở sản xuất, '; cuối='yến, đoạn tuyến quốc lộ đã hoàn thành vi ệc đ'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đọc được một số loại đường nhưng mất đầu định nghĩa đường thôn và cuối quy định quốc lộ.

```text
iệp, lâm nghiệp và cơ sở sản xuất, kinh doanh khác trên địa
bàn thôn;
đ) Đường đô thị là đường trong phạm vi địa giới hành chính nội thành, nội
thị, bao gồm: đường cao tốc đô thị, đường phố, đường ngõ, ngách, kiệt, hẻm trong
đô thị;
e) Đường chuyên dùng là đư ờng chuyên phục vụ giao thông cho m ột hoặc
một số cơ quan, tổ chức, cá nhân và đường nội bộ.
2. Đường địa phương bao gồm: đường tỉnh, đường đô thị, đường xã, đường thôn.
3. Bộ Xây dựng có trách nhi ệm quản lý qu ốc lộ, trừ quốc lộ quy định tại
điểm a khoản 4 Điều này và đường gom, đường bên quy định tại điểm c khoản 4
Điều này.
4. Ủy ban nhân dân cấp tỉnh có trách nhiệm quản lý các loại đường sau đây:
a) Quản lý đường tỉnh, quốc lộ đi qua đô thị loại đặc biệt; quốc lộ khi được
phân cấp; tuyến, đoạn tuyến quốc lộ đã hoàn thành vi ệc đ
```

## P06 — Config C

`luat_duong_bo_2026_p6_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 6; anchor 1223; chunk [840, 1640).

**AI đề xuất: 1/2.** Đường đô thị/chuyên dùng và trách nhiệm Bộ Xây dựng đọc được, nhưng mất đầu định nghĩa đường thôn; cuối cắt điều kiện của quốc lộ hoàn thành đầu tư. Chỉ hiểu được một phần các nhánh quản lý. Đã đọc toàn bộ luat_duong_bo_2026_p6_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 6; đầu='iệp, lâm nghiệp và cơ sở sản xuất, '; cuối='yến, đoạn tuyến quốc lộ đã hoàn thành vi ệc đ'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung giống B, cả đầu và cuối còn thiếu nên chỉ đủ đánh giá mức 1.

```text
iệp, lâm nghiệp và cơ sở sản xuất, kinh doanh khác trên địa
bàn thôn;
đ) Đường đô thị là đường trong phạm vi địa giới hành chính nội thành, nội
thị, bao gồm: đường cao tốc đô thị, đường phố, đường ngõ, ngách, kiệt, hẻm trong
đô thị;
e) Đường chuyên dùng là đư ờng chuyên phục vụ giao thông cho m ột hoặc
một số cơ quan, tổ chức, cá nhân và đường nội bộ.
2. Đường địa phương bao gồm: đường tỉnh, đường đô thị, đường xã, đường thôn.
3. Bộ Xây dựng có trách nhi ệm quản lý qu ốc lộ, trừ quốc lộ quy định tại
điểm a khoản 4 Điều này và đường gom, đường bên quy định tại điểm c khoản 4
Điều này.
4. Ủy ban nhân dân cấp tỉnh có trách nhiệm quản lý các loại đường sau đây:
a) Quản lý đường tỉnh, quốc lộ đi qua đô thị loại đặc biệt; quốc lộ khi được
phân cấp; tuyến, đoạn tuyến quốc lộ đã hoàn thành vi ệc đ
```

## P07 — Config A

`luat_duong_bo_2026_p7_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 7; anchor 1052; chunk [700, 1500).

**AI đề xuất: 1/2.** Các khoản 4–6 định nghĩa đường bên, công cộng, nội bộ đủ, nhưng đầu thiếu đầu câu đường nhánh và cuối chỉ có đầu định nghĩa đường dành riêng. Không tự hoàn tất hai ý ở ranh giới. Đã đọc toàn bộ luat_duong_bo_2026_p7_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 7; đầu='ường nhánh trước khi đấu nối vào đư'; cuối='y định tại khoản này.\n7. Đường dành riêng cho'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Các khoản 4 đến 6 rõ nhưng đầu về đường nhánh và cuối về đường dành riêng bị cắt.

```text
ường nhánh trước khi đấu nối vào đường chính.
Đường gom có thể là đường bên theo quy định tại khoản 4 Điều này.
4. Đường bên là đư ờng được xây dựng bên cạnh các đoạn đường chính để
ngăn cách giao thông khu vực hai bên đường với đường chính. Đường bên được
tách khỏi đường chính hoặc ngăn cách với đường chính bằng dải phân cách, tường
bảo vệ, rào chắn.
5. Đường dành cho giao thông công c ộng là đường phục vụ cho tất cả mọi
người, phương tiện giao thông đường bộ theo quy định của Luật này và quy định
khác của pháp luật có liên quan.
6. Đường nội bộ là đường trong phạm vi khu chung cư, đô thị, công nghiệp,
kinh tế, thương mại - dịch vụ, các cơ quan, tổ chức, đơn vị khác và chỉ phục vụ các
đối tượng được phép vào, ra bên trong phạm vi các khu vực quy định tại khoản này.
7. Đường dành riêng cho
```

## P07 — Config B

`luat_duong_bo_2026_p7_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 7; anchor 1052; chunk [840, 1640).

**AI đề xuất: 1/2.** Các định nghĩa công cộng/nội bộ còn rõ, nhưng đầu mất tên chủ thể đường bên; cuối chuyển sang Điều 10 rồi cắt yêu cầu xác định cấp kỹ thuật. Có thể hiểu các khoản giữa, không phải toàn chunk trọn ý. Đã đọc toàn bộ luat_duong_bo_2026_p7_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 7; đầu='xây dựng bên cạnh các đoạn đường ch'; cuối='huật của đường bộ phải được xác đ ịnh trong d'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Định nghĩa ở giữa hiểu được, song thiếu chủ thể đầu và quy định cấp kỹ thuật cuối.

```text
xây dựng bên cạnh các đoạn đường chính để
ngăn cách giao thông khu vực hai bên đường với đường chính. Đường bên được
tách khỏi đường chính hoặc ngăn cách với đường chính bằng dải phân cách, tường
bảo vệ, rào chắn.
5. Đường dành cho giao thông công c ộng là đường phục vụ cho tất cả mọi
người, phương tiện giao thông đường bộ theo quy định của Luật này và quy định
khác của pháp luật có liên quan.
6. Đường nội bộ là đường trong phạm vi khu chung cư, đô thị, công nghiệp,
kinh tế, thương mại - dịch vụ, các cơ quan, tổ chức, đơn vị khác và chỉ phục vụ các
đối tượng được phép vào, ra bên trong phạm vi các khu vực quy định tại khoản này.
7. Đường dành riêng cho người đi bộ, người đi xe đạp và các đường khác.
Điều 10. Cấp kỹ thuật của đường bộ
1. Cấp kỹ thuật của đường bộ phải được xác đ ịnh trong d
```

## P07 — Config C

`luat_duong_bo_2026_p7_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 7; anchor 1052; chunk [840, 1640).

**AI đề xuất: 1/2.** Các định nghĩa công cộng/nội bộ còn rõ, nhưng đầu mất tên chủ thể đường bên; cuối chuyển sang Điều 10 rồi cắt yêu cầu xác định cấp kỹ thuật. Có thể hiểu các khoản giữa, không phải toàn chunk trọn ý. Đã đọc toàn bộ luat_duong_bo_2026_p7_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 7; đầu='xây dựng bên cạnh các đoạn đường ch'; cuối='huật của đường bộ phải được xác đ ịnh trong d'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đoạn trùng B, các ý ở ranh giới vẫn chưa đầy đủ nên giữ mức 1.

```text
xây dựng bên cạnh các đoạn đường chính để
ngăn cách giao thông khu vực hai bên đường với đường chính. Đường bên được
tách khỏi đường chính hoặc ngăn cách với đường chính bằng dải phân cách, tường
bảo vệ, rào chắn.
5. Đường dành cho giao thông công c ộng là đường phục vụ cho tất cả mọi
người, phương tiện giao thông đường bộ theo quy định của Luật này và quy định
khác của pháp luật có liên quan.
6. Đường nội bộ là đường trong phạm vi khu chung cư, đô thị, công nghiệp,
kinh tế, thương mại - dịch vụ, các cơ quan, tổ chức, đơn vị khác và chỉ phục vụ các
đối tượng được phép vào, ra bên trong phạm vi các khu vực quy định tại khoản này.
7. Đường dành riêng cho người đi bộ, người đi xe đạp và các đường khác.
Điều 10. Cấp kỹ thuật của đường bộ
1. Cấp kỹ thuật của đường bộ phải được xác đ ịnh trong d
```

## P08 — Config A

`luat_duong_bo_2026_p8_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 8; anchor 1229; chunk [700, 1500).

**AI đề xuất: 1/2.** Quy tắc đường trùng và trường hợp không bắt buộc đặt tên đọc được, nhưng ngoại lệ dẫn điểm a khoản 1 không có trong chunk; cuối cắt giữa “Chính phủ”. Thiếu cả điều kiện dẫn chiếu và phần kết. Đã đọc toàn bộ luat_duong_bo_2026_p8_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 8; đầu=';\nb) Tên, số hiệu đường bộ tham gia'; cuối='h địa giới hành chính của địa phương.\n4. Chín'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Có quy tắc đặt tên đường nhưng thiếu điều kiện được dẫn chiếu và đoạn kết bị cắt.

```text
;
b) Tên, số hiệu đường bộ tham gia vào mạng lưới đường bộ quốc tế thực hiện
theo điều ước quốc tế giữa nước Cộng hòa xã h ội chủ nghĩa Việt Nam v ới các
quốc gia, tổ chức quốc tế có liên quan. Đường bộ kết nối vào mạng lưới đường bộ
quốc tế thì sử dụng cả tên, số hiệu đường bộ trong nước và tên, số hiệu đường bộ
quốc tế.
2. Trường hợp có tuyến, đoạn tuyến đường bộ đi trùng nhau thì sử dụng tên,
số hiệu đường bộ thuộc cấp quản lý cao hơn, trừ trường hợp quy định tại điểm a
khoản 1 Điều này.
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn,
đường nội bộ, đường chuyên dùng; không b ắt buộc đổi tên, s ố hiệu đường bộ
trong trường hợp đường đó đi qua đ ịa bàn đư ợc cấp có th ẩm quyền quyết định
giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.
4. Chín
```

## P08 — Config B

`luat_duong_bo_2026_p8_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 8; anchor 1229; chunk [840, 1640).

**AI đề xuất: 1/2.** Có kết khoản 4 và heading mục mới, song đầu thiếu chủ thể tên đường quốc tế, ngoại lệ điểm a khoản 1 ở ngoài chunk, cuối cắt tiêu đề Điều 12. Không coi việc có heading là đã đủ ngữ cảnh. Đã đọc toàn bộ luat_duong_bo_2026_p8_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 8; đầu=' Nam v ới các\nquốc gia, tổ chức quố'; cuối='Ạ TẦNG ĐƯỜNG BỘ\nĐiều 12. Quỹ đất dành cho kết'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đọc được một số quy định, nhưng phần đầu mất chủ thể và cuối cắt tiêu đề điều tiếp theo.

```text
 Nam v ới các
quốc gia, tổ chức quốc tế có liên quan. Đường bộ kết nối vào mạng lưới đường bộ
quốc tế thì sử dụng cả tên, số hiệu đường bộ trong nước và tên, số hiệu đường bộ
quốc tế.
2. Trường hợp có tuyến, đoạn tuyến đường bộ đi trùng nhau thì sử dụng tên,
số hiệu đường bộ thuộc cấp quản lý cao hơn, trừ trường hợp quy định tại điểm a
khoản 1 Điều này.
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn,
đường nội bộ, đường chuyên dùng; không b ắt buộc đổi tên, s ố hiệu đường bộ
trong trường hợp đường đó đi qua đ ịa bàn đư ợc cấp có th ẩm quyền quyết định
giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.
4. Chính phủ quy định chi tiết Điều này.
Mục 2
ĐẤT DÀNH CHO KẾT CẤU HẠ TẦNG ĐƯỜNG BỘ,
BẢO VỆ KẾT CẤU HẠ TẦNG ĐƯỜNG BỘ
Điều 12. Quỹ đất dành cho kết
```

## P08 — Config C

`luat_duong_bo_2026_p8_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 8; anchor 1229; chunk [840, 1640).

**AI đề xuất: 1/2.** Có kết khoản 4 và heading mục mới, song đầu thiếu chủ thể tên đường quốc tế, ngoại lệ điểm a khoản 1 ở ngoài chunk, cuối cắt tiêu đề Điều 12. Không coi việc có heading là đã đủ ngữ cảnh. Đã đọc toàn bộ luat_duong_bo_2026_p8_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 8; đầu=' Nam v ới các\nquốc gia, tổ chức quố'; cuối='Ạ TẦNG ĐƯỜNG BỘ\nĐiều 12. Quỹ đất dành cho kết'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung giống B, thiếu ngữ cảnh đầu và cuối nên chưa đạt mức 2.

```text
 Nam v ới các
quốc gia, tổ chức quốc tế có liên quan. Đường bộ kết nối vào mạng lưới đường bộ
quốc tế thì sử dụng cả tên, số hiệu đường bộ trong nước và tên, số hiệu đường bộ
quốc tế.
2. Trường hợp có tuyến, đoạn tuyến đường bộ đi trùng nhau thì sử dụng tên,
số hiệu đường bộ thuộc cấp quản lý cao hơn, trừ trường hợp quy định tại điểm a
khoản 1 Điều này.
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn,
đường nội bộ, đường chuyên dùng; không b ắt buộc đổi tên, s ố hiệu đường bộ
trong trường hợp đường đó đi qua đ ịa bàn đư ợc cấp có th ẩm quyền quyết định
giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.
4. Chính phủ quy định chi tiết Điều này.
Mục 2
ĐẤT DÀNH CHO KẾT CẤU HẠ TẦNG ĐƯỜNG BỘ,
BẢO VỆ KẾT CẤU HẠ TẦNG ĐƯỜNG BỘ
Điều 12. Quỹ đất dành cho kết
```

## P09 — Config A

`luat_duong_bo_2026_p9_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 9; anchor 1232; chunk [700, 1500).

**AI đề xuất: 1/2.** Danh sách đất và quy tắc quản lý sử dụng đất rõ trong khoản 1–2; đầu mất tên điều và cuối bỏ dở nghĩa vụ chủ bất động sản dành lối thoát nước. Không thể suy ra đầy đủ nghĩa vụ cuối từ đoạn này. Đã đọc toàn bộ luat_duong_bo_2026_p9_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 9; đầu='tầng đường bộ\n1. Đất dành cho kết c'; cuối='ống thoát nước đi qua phải dành một lối thoát'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Quy tắc sử dụng đất khá rõ nhưng đầu thiếu tên điều và cuối chưa hết nghĩa vụ thoát nước.

```text
tầng đường bộ
1. Đất dành cho kết cấu hạ tầng đường bộ bao gồm:
a) Đất của đường bộ gồm phần đất để xây dựng công trình đường bộ và phần
đất để bảo vệ, bảo trì đường bộ;
b) Đất để xây dựng bến xe; bãi đỗ xe; điểm dừng xe, đỗ xe; trạm dừng nghỉ;
các công trình phụ trợ phục vụ cho hoạt động đường bộ;
c) Hành lang an toàn đường bộ.
2. Việc quản lý, sử dụng đất dành cho k ết cấu hạ tầng đường bộ phải tuân
thủ quy định của pháp luật về đất đai, pháp luật về quy hoạch, pháp luật về quy
hoạch đô thị, pháp luật về xây dựng, quy định của Luật này và quy định khác của
pháp luật có liên quan.
3. Trường hợp do vị trí tự nhiên mà việc thoát nước từ công trình thuộc kết
cấu hạ tầng đường bộ buộc phải qua bất động sản khác thì ch ủ sở hữu bất động
sản có hệ thống thoát nước đi qua phải dành một lối thoát
```

## P09 — Config B

`luat_duong_bo_2026_p9_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 9; anchor 1232; chunk [841, 1641).

**AI đề xuất: 1/2.** Đọc trọn nghĩa vụ dành lối thoát nước ở khoản 3 nhưng đầu bắt giữa danh sách đất, cuối cắt nghĩa vụ người quản lý hạn chế thiệt hại. Hai ranh giới làm mất ý dù giữa chunk có nội dung độc lập. Đã đọc toàn bộ luat_duong_bo_2026_p9_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 9; đầu='để bảo vệ, bảo trì đường bộ;\nb) Đất'; cuối='ường bộ phải hạn chế đến mức thấp nhất thiệt '.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Khoản về lối thoát nước đầy đủ hơn, nhưng danh sách đất đầu và nghĩa vụ cuối bị cắt.

```text
để bảo vệ, bảo trì đường bộ;
b) Đất để xây dựng bến xe; bãi đỗ xe; điểm dừng xe, đỗ xe; trạm dừng nghỉ;
các công trình phụ trợ phục vụ cho hoạt động đường bộ;
c) Hành lang an toàn đường bộ.
2. Việc quản lý, sử dụng đất dành cho k ết cấu hạ tầng đường bộ phải tuân
thủ quy định của pháp luật về đất đai, pháp luật về quy hoạch, pháp luật về quy
hoạch đô thị, pháp luật về xây dựng, quy định của Luật này và quy định khác của
pháp luật có liên quan.
3. Trường hợp do vị trí tự nhiên mà việc thoát nước từ công trình thuộc kết
cấu hạ tầng đường bộ buộc phải qua bất động sản khác thì ch ủ sở hữu bất động
sản có hệ thống thoát nước đi qua phải dành một lối thoát nước thích hợp, không
được cản trở hoặc ngăn chặn hệ thống thoát nước.
Người quản lý, sử dụng đường bộ phải hạn chế đến mức thấp nhất thiệt
```

## P09 — Config C

`luat_duong_bo_2026_p9_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 9; anchor 1232; chunk [841, 1641).

**AI đề xuất: 1/2.** Đọc trọn nghĩa vụ dành lối thoát nước ở khoản 3 nhưng đầu bắt giữa danh sách đất, cuối cắt nghĩa vụ người quản lý hạn chế thiệt hại. Hai ranh giới làm mất ý dù giữa chunk có nội dung độc lập. Đã đọc toàn bộ luat_duong_bo_2026_p9_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 9; đầu='để bảo vệ, bảo trì đường bộ;\nb) Đất'; cuối='ường bộ phải hạn chế đến mức thấp nhất thiệt '. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đoạn trùng B, vẫn thiếu ý ở hai ranh giới nên chỉ đạt mức 1.

```text
để bảo vệ, bảo trì đường bộ;
b) Đất để xây dựng bến xe; bãi đỗ xe; điểm dừng xe, đỗ xe; trạm dừng nghỉ;
các công trình phụ trợ phục vụ cho hoạt động đường bộ;
c) Hành lang an toàn đường bộ.
2. Việc quản lý, sử dụng đất dành cho k ết cấu hạ tầng đường bộ phải tuân
thủ quy định của pháp luật về đất đai, pháp luật về quy hoạch, pháp luật về quy
hoạch đô thị, pháp luật về xây dựng, quy định của Luật này và quy định khác của
pháp luật có liên quan.
3. Trường hợp do vị trí tự nhiên mà việc thoát nước từ công trình thuộc kết
cấu hạ tầng đường bộ buộc phải qua bất động sản khác thì ch ủ sở hữu bất động
sản có hệ thống thoát nước đi qua phải dành một lối thoát nước thích hợp, không
được cản trở hoặc ngăn chặn hệ thống thoát nước.
Người quản lý, sử dụng đường bộ phải hạn chế đến mức thấp nhất thiệt
```

## P10 — Config A

`luat_duong_bo_2026_p10_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 10; anchor 1313; chunk [700, 1500).

**AI đề xuất: 1/2.** Điểm d về công trình bảo trì đọc được, nhưng đầu mất điều kiện đường đô thị, điểm c dẫn a/b nằm ngoài phần đủ nghĩa, cuối cắt quy tắc chọn đường theo cấp kỹ thuật. Thiếu các điều kiện quan trọng. Đã đọc toàn bộ luat_duong_bo_2026_p10_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 10; đầu=' với tường bao nhà ở, tường bao côn'; cuối=' bảo trì\nđường bộ được xác định theo đường có'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Có thông tin về công trình bảo trì nhưng thiếu điều kiện liên quan và quy tắc ở cuối.

```text
 với tường bao nhà ở, tường bao công trình
xây dựng khác, đường không có hè phố, đường nằm trong ngõ, ngách, kiệt, hẻm,
đường nội bộ khu dân cư đô thị thì được sử dụng một phần mặt đường khi thực hiện
bảo vệ, bảo trì đường đô thị;
c) Trường hợp không thu ộc quy đ ịnh tại điểm a và đi ểm b kho ản này thì
được xác định tương tự đường ngoài đô thị;
d) Phần đất để bảo vệ, bảo trì cầu, cống, rãnh, hố thu và các hạng mục công
trình của đường đô thị được xác định theo quy định tại điểm c khoản 1 Điều này.
Trường hợp cầu, cống, rãnh, hố thu và các hạng mục công trình của đường đô thị
nằm liền kề với công trình xây dựng khác thì phần đất để bảo vệ, bảo trì là ranh
giới của các công trình.
3. Tại các đo ạn đường chồng lấn, giao nhau, ph ần đ ất để bảo vệ, bảo trì
đường bộ được xác định theo đường có
```

## P10 — Config B

`luat_duong_bo_2026_p10_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 10; anchor 1313; chunk [841, 1641).

**AI đề xuất: 1/2.** Có ý ranh giới công trình liền kề và chọn cấp kỹ thuật cao hơn, nhưng đầu mất điều kiện sử dụng mặt đường, cuối bỏ dở ranh đường ngoài cùng. Các tham chiếu khiến chunk chỉ hiểu từng phần. Đã đọc toàn bộ luat_duong_bo_2026_p10_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 10; đầu='cư đô thị thì được sử dụng một phần'; cuối='c xác đ ịnh từ mép của\nđường ngoài cùng trở r'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Một số quy tắc ranh giới và cấp kỹ thuật rõ nhưng điều kiện đầu và cuối chưa đủ.

```text
cư đô thị thì được sử dụng một phần mặt đường khi thực hiện
bảo vệ, bảo trì đường đô thị;
c) Trường hợp không thu ộc quy đ ịnh tại điểm a và đi ểm b kho ản này thì
được xác định tương tự đường ngoài đô thị;
d) Phần đất để bảo vệ, bảo trì cầu, cống, rãnh, hố thu và các hạng mục công
trình của đường đô thị được xác định theo quy định tại điểm c khoản 1 Điều này.
Trường hợp cầu, cống, rãnh, hố thu và các hạng mục công trình của đường đô thị
nằm liền kề với công trình xây dựng khác thì phần đất để bảo vệ, bảo trì là ranh
giới của các công trình.
3. Tại các đo ạn đường chồng lấn, giao nhau, ph ần đ ất để bảo vệ, bảo trì
đường bộ được xác định theo đường có cấp kỹ thuật cao hơn; đối với các đường
liền kề nhau, phần đất để bảo vệ, bảo trì đư ờng bộ được xác đ ịnh từ mép của
đường ngoài cùng trở r
```

## P10 — Config C

`luat_duong_bo_2026_p10_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 10; anchor 1313; chunk [841, 1641).

**AI đề xuất: 1/2.** Có ý ranh giới công trình liền kề và chọn cấp kỹ thuật cao hơn, nhưng đầu mất điều kiện sử dụng mặt đường, cuối bỏ dở ranh đường ngoài cùng. Các tham chiếu khiến chunk chỉ hiểu từng phần. Đã đọc toàn bộ luat_duong_bo_2026_p10_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 10; đầu='cư đô thị thì được sử dụng một phần'; cuối='c xác đ ịnh từ mép của\nđường ngoài cùng trở r'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Giống B, các phần dẫn chiếu và kết luận ở ranh giới vẫn bị thiếu.

```text
cư đô thị thì được sử dụng một phần mặt đường khi thực hiện
bảo vệ, bảo trì đường đô thị;
c) Trường hợp không thu ộc quy đ ịnh tại điểm a và đi ểm b kho ản này thì
được xác định tương tự đường ngoài đô thị;
d) Phần đất để bảo vệ, bảo trì cầu, cống, rãnh, hố thu và các hạng mục công
trình của đường đô thị được xác định theo quy định tại điểm c khoản 1 Điều này.
Trường hợp cầu, cống, rãnh, hố thu và các hạng mục công trình của đường đô thị
nằm liền kề với công trình xây dựng khác thì phần đất để bảo vệ, bảo trì là ranh
giới của các công trình.
3. Tại các đo ạn đường chồng lấn, giao nhau, ph ần đ ất để bảo vệ, bảo trì
đường bộ được xác định theo đường có cấp kỹ thuật cao hơn; đối với các đường
liền kề nhau, phần đất để bảo vệ, bảo trì đư ờng bộ được xác đ ịnh từ mép của
đường ngoài cùng trở r
```

## P11 — Config A

`luat_duong_bo_2026_p11_fixed_1` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 11; anchor 1198; chunk [700, 1500).

**AI đề xuất: 1/2.** Tiêu đề Điều 15 và nguyên tắc ngoài đô thị ở điểm a đủ ngữ cảnh; đầu còn mảnh Điều 14, cuối cắt giữa từ “lang” và mất giới hạn so sánh đường đô thị. Không cho mức 2 dù điểm a đọc rõ. Đã đọc toàn bộ luat_duong_bo_2026_p11_fixed_1, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 11; đầu='ình đường bộ;\nd) Phần đất bảo vệ, b'; cuối='ng đỏ nhưng không lớn hơn chiều rộng hành lan'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nguyên tắc Điều 15 phần đầu rõ nhưng mảnh Điều 14 và giới hạn ở cuối chưa trọn.

```text
ình đường bộ;
d) Phần đất bảo vệ, bảo trì công trình kè, tường chắn được xác định từ mép
ngoài của bộ phận ngoài cùng của công trình ra xung quanh.
7. Chính phủ quy định chi tiết Điều này.
Điều 15. Hành lang an toàn đường bộ
1. Chiều rộng hành lang an toàn đư ờng bộ được xác đ ịnh theo nguyên t ắc
sau đây:
a) Đối với đường ngoài đô th ị, xác định từ mép ngoài ph ần đất để bảo vệ,
bảo trì đường bộ, theo quy mô, c ấp kỹ thuật của đường; trường hợp đường hiện
hữu chưa xác đ ịnh cấp kỹ thuật, thì căn c ứ chiều rộng mặt đường và tiêu chu ẩn
thiết kế đường để xác định cấp kỹ thuật tương ứng làm căn cứ xác định chiều rộng
hành lang an toàn đường bộ;
b) Đối với đường đô thị, xác định từ mép ngoài phần đất để bảo vệ, bảo trì
đường đô thị đến chỉ giới đường đỏ nhưng không lớn hơn chiều rộng hành lan
```

## P11 — Config B

`luat_duong_bo_2026_p11_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 11; anchor 1198; chunk [841, 1641).

**AI đề xuất: 1/2.** Điểm a/b của Điều 15 được giữ đầy đủ hơn A, nhưng đầu chỉ là đuôi Điều 14 và cuối cắt nguyên tắc cầu/bến phà ở điểm c. Đánh giá toàn chunk vẫn thiếu nội dung ở ranh giới. Đã đọc toàn bộ luat_duong_bo_2026_p11_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 11; đầu='quanh.\n7. Chính phủ quy định chi ti'; cuối='ều dọc, chiều\nngang công trình và phụ thuộc c'.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Điểm a và b khá đầy đủ nhưng đầu còn đoạn cũ và điểm c cuối bị cắt.

```text
quanh.
7. Chính phủ quy định chi tiết Điều này.
Điều 15. Hành lang an toàn đường bộ
1. Chiều rộng hành lang an toàn đư ờng bộ được xác đ ịnh theo nguyên t ắc
sau đây:
a) Đối với đường ngoài đô th ị, xác định từ mép ngoài ph ần đất để bảo vệ,
bảo trì đường bộ, theo quy mô, c ấp kỹ thuật của đường; trường hợp đường hiện
hữu chưa xác đ ịnh cấp kỹ thuật, thì căn c ứ chiều rộng mặt đường và tiêu chu ẩn
thiết kế đường để xác định cấp kỹ thuật tương ứng làm căn cứ xác định chiều rộng
hành lang an toàn đường bộ;
b) Đối với đường đô thị, xác định từ mép ngoài phần đất để bảo vệ, bảo trì
đường đô thị đến chỉ giới đường đỏ nhưng không lớn hơn chiều rộng hành lang
của đường ngoài đô thị cùng cấp;
c) Đối với cầu, bến phà, cầu phao đường bộ, xác định theo chiều dọc, chiều
ngang công trình và phụ thuộc c
```

## P11 — Config C

`luat_duong_bo_2026_p11_paragraph_800_2` — `luat_duong_bo_2026` — `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf` — trang PDF 11; anchor 1198; chunk [841, 1641).

**AI đề xuất: 1/2.** Điểm a/b của Điều 15 được giữ đầy đủ hơn A, nhưng đầu chỉ là đuôi Điều 14 và cuối cắt nguyên tắc cầu/bến phà ở điểm c. Đánh giá toàn chunk vẫn thiếu nội dung ở ranh giới. Đã đọc toàn bộ luat_duong_bo_2026_p11_paragraph_800_2, nguồn 2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf, PDF 11; đầu='quanh.\n7. Chính phủ quy định chi ti'; cuối='ều dọc, chiều\nngang công trình và phụ thuộc c'. C có ID/text hoàn toàn trùng B tại cùng anchor, nên coherence không đổi khi chỉ thay filter truy vấn.

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Nội dung trùng B, còn thiếu ý ở đầu và điểm c cuối nên giữ mức 1.

```text
quanh.
7. Chính phủ quy định chi tiết Điều này.
Điều 15. Hành lang an toàn đường bộ
1. Chiều rộng hành lang an toàn đư ờng bộ được xác đ ịnh theo nguyên t ắc
sau đây:
a) Đối với đường ngoài đô th ị, xác định từ mép ngoài ph ần đất để bảo vệ,
bảo trì đường bộ, theo quy mô, c ấp kỹ thuật của đường; trường hợp đường hiện
hữu chưa xác đ ịnh cấp kỹ thuật, thì căn c ứ chiều rộng mặt đường và tiêu chu ẩn
thiết kế đường để xác định cấp kỹ thuật tương ứng làm căn cứ xác định chiều rộng
hành lang an toàn đường bộ;
b) Đối với đường đô thị, xác định từ mép ngoài phần đất để bảo vệ, bảo trì
đường đô thị đến chỉ giới đường đỏ nhưng không lớn hơn chiều rộng hành lang
của đường ngoài đô thị cùng cấp;
c) Đối với cầu, bến phà, cầu phao đường bộ, xác định theo chiều dọc, chiều
ngang công trình và phụ thuộc c
```
