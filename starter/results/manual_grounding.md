# Grounding quality — 5 TEST × 3 cấu hình

Nhãn AI đề xuất — CHƯA phải chấm thủ công bởi người học. Chỉ đánh giá evidence retrieval, không phải độ chính xác câu trả lời LLM.

Bản Markdown bỏ khoảng trắng cuối dòng để trình bày; text gốc đầy đủ được giữ trong traces JSON.

Thang điểm: 0 không có bằng chứng; 1 thiếu điều kiện/ngữ cảnh; 2 đủ để trả lời và truy nguồn.
Đã đọc cả ba chunk mỗi trường hợp. Điểm dựa trên ý nghĩa và ngữ cảnh, không quy đổi từ hit tự động. Có thể dùng hai chunk trong grounding nếu liên kết đủ rõ; không dùng cách đó để nâng Evidence Hit@3.

Sửa `grounding_review.csv`: điền human_score, human_reason, reviewer, reviewed_at rồi chạy `python -m src.audit`. Nhãn AI được giữ riêng. Bản phiếu ban đầu: `verification/manual_grounding_original.md`.

| Config | n | AI số điểm 0 / 1 / 2 | AI trung bình /2 | Người học duyệt |
|---|---|---|---|---|
| A | 5 | 0 / 1 / 4 | 1.80 | 5/5 |
| B | 5 | 0 / 0 / 5 | 2.00 | 5/5 |
| C | 5 | 0 / 0 / 5 | 2.00 | 5/5 |

## Q16 — Config A

Câu hỏi: Giấy vận tải trong vận tải hàng hóa bằng ô tô có chức năng chứng minh điều gì?

Đáp án tham chiếu: Xác nhận người lái xe đã nhận hàng với số lượng, chủng loại, tình trạng hàng hóa để vận tải đến nơi trả hàng và là bằng chứng của hợp đồng vận tải hàng hóa.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 52, 'evidence_quote': '1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng chứng của hợp đồng vận tải hàng hóa.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 1/2.** Giấy vận tải xác nhận đã nhận hàng, loại/lượng/tình trạng và nơi trả hàng xuất hiện ở Top-1, nhưng mệnh đề về bằng chứng hợp đồng bị cắt ngay giữa từ ở cuối chunk. Top-2 là trách nhiệm đơn vị và dẫn chiếu Điều 56; Top-3 là quyền đơn vị về khai hàng, thanh toán, kiểm tra, không hoàn thiện chức năng hợp đồng. Vì thiếu một vế expected answer, Top-3 chỉ đủ một phần; không lấy câu đầy đủ ngoài trace từ PDF để nâng điểm. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p52_fixed_2 (PDF 52); luat_duong_bo_2026_p53_fixed_1 (PDF 53); luat_duong_bo_2026_p53_fixed_2 (PDF 53).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 1. Đồng ý mức 1: có thông tin nhận hàng và nơi trả nhưng thiếu phần chứng minh hợp đồng do đoạn trích bị cắt.

### Top 1 — `luat_duong_bo_2026_p52_fixed_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 52.

```text
a) Thanh toán tiền cước chuyến đi theo giá vé niêm yết hoặc theo thoả thuận
với đơn vị kinh doanh vận tải;
b) Chấp hành quy định về vận tải; thực hiện đúng hướng dẫn của lái xe, nhân
viên phục vụ trên xe ô tô;
c) Không mang theo hàng hóa cấm lưu thông, hàng hóa nguy hiểm, động vật
hoang dã; hàng có mùi hôi thối hoặc động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường;
d) Xuất trình giấy tờ chứng minh thuộc đối tượng được miễn, giảm giá vé
với đơn vị cung cấp dịch vụ vận tải theo quy định của pháp luật;
đ) Thực hiện phòng, chống dịch bệnh theo quy định của pháp luật.
Điều 61. Vận tải hàng hóa bằng xe ô tô
1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với
số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng
ch
```

### Top 2 — `luat_duong_bo_2026_p53_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
hịu trách nhiệm hoặc liên đới chịu trách nhiệm về hành vi vi phạm của
người lao động, người đại diện của đơn vị kinh doanh vận tải hàng hóa bằng xe ô
tô gây ra theo quy định của pháp luật.
3. Việc vận tải hàng hóa b ằng xe ô tô th ực hiện theo quy đ ịnh tại Điều 56
của Luật này, thực hiện đầy đủ các yêu cầu, điều kiện về bảo đảm trật tự, an toàn
giao thông đường bộ theo quy định của pháp luật về trật tự, an toàn giao thông
đường bộ và quy định khác của pháp luật có liên quan. Khi vận tải hàng hóa trên
đường bộ phải có giấy vận tải theo quy định của pháp luật.
4. Bộ trưởng Bộ Xây dựng37 quy định về tổ chức và quản lý hoạt động vận
tải hàng hóa bằng xe ô tô.
Điều 62. Quy ền và nghĩa v ụ của đơn v ị kinh doanh v ận tải hàng hóa
bằng xe ô tô
1. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô c
```

### Top 3 — `luat_duong_bo_2026_p53_fixed_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
n v ị kinh doanh v ận tải hàng hóa
bằng xe ô tô
1. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có quyền sau đây:
a) Yêu cầu người thuê vận tải cung cấp thông tin c ần thiết về hàng hóa để
ghi vào giấy vận tải và có quyền kiểm tra tính xác thực của thông tin đó;
b) Yêu cầu người thuê vận tải thanh toán đủ tiền cước và chi phí phát sinh;
yêu c ầu ngư ời thuê v ận tải bồi thư ờng thi ệt hại do vi ph ạm thỏa thu ận trong
hợp đồng;
c) Từ chối vận tải nếu người thuê v ận tải không giao hàng hóa theo th ỏa
thuận trong hợp đồng;
d) Yêu cầu giám định hàng hóa khi cần thiết;
đ) Lưu giữ hàng hóa trong trường hợp người thuê vận tải không thanh toán
đủ tiền cước và chi phí phát sinh theo thoả thuận trong hợp đồng.
2. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có nghĩa vụ sau đây:

37 Cụm từ “B
```

## Q16 — Config B

Câu hỏi: Giấy vận tải trong vận tải hàng hóa bằng ô tô có chức năng chứng minh điều gì?

Đáp án tham chiếu: Xác nhận người lái xe đã nhận hàng với số lượng, chủng loại, tình trạng hàng hóa để vận tải đến nơi trả hàng và là bằng chứng của hợp đồng vận tải hàng hóa.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 52, 'evidence_quote': '1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng chứng của hợp đồng vận tải hàng hóa.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 giữ toàn bộ khoản 1 Điều 61: nhận hàng với số lượng/chủng loại/tình trạng, vận tải đến nơi trả hàng và làm bằng chứng hợp đồng. Top-2 nói nghĩa vụ có giấy vận tải; Top-3 nói cấp giấy vận tải cho lái xe, chỉ là ngữ cảnh phụ. Đầu Top-1 bị cắt ở nội dung hành khách nhưng định nghĩa cần trả lời đã nguyên vẹn và đúng nguồn/trang; không thiếu vế expected answer. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p52_paragraph_800_3 (PDF 52); luat_duong_bo_2026_p53_paragraph_800_2 (PDF 53); luat_duong_bo_2026_p54_paragraph_800_1 (PDF 54).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: đoạn trích nêu đủ các chức năng của giấy vận tải, bao gồm bằng chứng hợp đồng.

### Top 1 — `luat_duong_bo_2026_p52_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 52.

```text
 lưu thông, hàng hóa nguy hiểm, động vật
hoang dã; hàng có mùi hôi thối hoặc động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường;
d) Xuất trình giấy tờ chứng minh thuộc đối tượng được miễn, giảm giá vé
với đơn vị cung cấp dịch vụ vận tải theo quy định của pháp luật;
đ) Thực hiện phòng, chống dịch bệnh theo quy định của pháp luật.
Điều 61. Vận tải hàng hóa bằng xe ô tô
1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với
số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng
chứng của hợp đồng vận tải hàng hóa.
```

### Top 2 — `luat_duong_bo_2026_p53_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
ằng xe ô
tô gây ra theo quy định của pháp luật.
3. Việc vận tải hàng hóa b ằng xe ô tô th ực hiện theo quy đ ịnh tại Điều 56
của Luật này, thực hiện đầy đủ các yêu cầu, điều kiện về bảo đảm trật tự, an toàn
giao thông đường bộ theo quy định của pháp luật về trật tự, an toàn giao thông
đường bộ và quy định khác của pháp luật có liên quan. Khi vận tải hàng hóa trên
đường bộ phải có giấy vận tải theo quy định của pháp luật.
4. Bộ trưởng Bộ Xây dựng37 quy định về tổ chức và quản lý hoạt động vận
tải hàng hóa bằng xe ô tô.
Điều 62. Quy ền và nghĩa v ụ của đơn v ị kinh doanh v ận tải hàng hóa
bằng xe ô tô
1. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có quyền sau đây:
a) Yêu cầu người thuê vận tải cung cấp thông tin c ần thiết về hàng hóa để
ghi vào giấy vận tải và có quyền kiểm tra tính xá
```

### Top 3 — `luat_duong_bo_2026_p54_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 54.

```text
a) Không được để tổ chức, cá nhân không có gi ấy phép kinh doanh v ận tải
bằng xe ô tô lo ại hình v ận tải hàng hóa thay mình th ực hiện điều hành phương
tiện và lái xe hoặc quyết định giá cước để vận tải hàng hóa;
b) Không được sử dụng người không có giấy phép lái xe hoặc có giấy phép
lái xe nhưng không phù hợp với loại xe, người có giấy phép lái xe bị trừ hết điểm,
người đang bị tước hoặc bị thu hồi giấy phép lái xe để điều khiển phương tiện vận
tải hàng hóa;
c) Cung cấp phương tiện đúng loại, thời gian, địa điểm và giao hàng hóa cho
người nhận hàng theo thỏa thuận trong hợp đồng; cấp giấy vận tải cho lái xe trước
khi thực hiện vận tải;
d) Hướng dẫn, kiểm tra vi ệc xếp, dỡ hàng hóa trên phương ti ện bảo đảm
không vượt quá khối lượng hàng hóa chuyên chở cho phép tham gia giao thông,
vượt
```

## Q16 — Config C

Câu hỏi: Giấy vận tải trong vận tải hàng hóa bằng ô tô có chức năng chứng minh điều gì?

Đáp án tham chiếu: Xác nhận người lái xe đã nhận hàng với số lượng, chủng loại, tình trạng hàng hóa để vận tải đến nơi trả hàng và là bằng chứng của hợp đồng vận tải hàng hóa.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 52, 'evidence_quote': '1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng chứng của hợp đồng vận tải hàng hóa.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 giữ toàn bộ khoản 1 Điều 61: nhận hàng với số lượng/chủng loại/tình trạng, vận tải đến nơi trả hàng và làm bằng chứng hợp đồng. Top-2 nói nghĩa vụ có giấy vận tải; Top-3 nói cấp giấy vận tải cho lái xe, chỉ là ngữ cảnh phụ. Đầu Top-1 bị cắt ở nội dung hành khách nhưng định nghĩa cần trả lời đã nguyên vẹn và đúng nguồn/trang; không thiếu vế expected answer. Đã đối chiếu lại cả ba chunk C với B: ID/text trùng; chỉ Q17 thực áp dụng filter chapter IV, các câu còn lại không filter. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p52_paragraph_800_3 (PDF 52); luat_duong_bo_2026_p53_paragraph_800_2 (PDF 53); luat_duong_bo_2026_p54_paragraph_800_1 (PDF 54).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: bằng chứng đầy đủ như cấu hình B; các đoạn liên quan đáp ứng câu hỏi.

### Top 1 — `luat_duong_bo_2026_p52_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 52.

```text
 lưu thông, hàng hóa nguy hiểm, động vật
hoang dã; hàng có mùi hôi thối hoặc động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường;
d) Xuất trình giấy tờ chứng minh thuộc đối tượng được miễn, giảm giá vé
với đơn vị cung cấp dịch vụ vận tải theo quy định của pháp luật;
đ) Thực hiện phòng, chống dịch bệnh theo quy định của pháp luật.
Điều 61. Vận tải hàng hóa bằng xe ô tô
1. Giấy vận tải là giấy tờ để xác nhận việc người lái xe đã nhận hàng hóa với
số lượng, chủng loại, tình tr ạng hàng hóa đ ể vận tải đến nơi tr ả hàng; là b ằng
chứng của hợp đồng vận tải hàng hóa.
```

### Top 2 — `luat_duong_bo_2026_p53_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
ằng xe ô
tô gây ra theo quy định của pháp luật.
3. Việc vận tải hàng hóa b ằng xe ô tô th ực hiện theo quy đ ịnh tại Điều 56
của Luật này, thực hiện đầy đủ các yêu cầu, điều kiện về bảo đảm trật tự, an toàn
giao thông đường bộ theo quy định của pháp luật về trật tự, an toàn giao thông
đường bộ và quy định khác của pháp luật có liên quan. Khi vận tải hàng hóa trên
đường bộ phải có giấy vận tải theo quy định của pháp luật.
4. Bộ trưởng Bộ Xây dựng37 quy định về tổ chức và quản lý hoạt động vận
tải hàng hóa bằng xe ô tô.
Điều 62. Quy ền và nghĩa v ụ của đơn v ị kinh doanh v ận tải hàng hóa
bằng xe ô tô
1. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có quyền sau đây:
a) Yêu cầu người thuê vận tải cung cấp thông tin c ần thiết về hàng hóa để
ghi vào giấy vận tải và có quyền kiểm tra tính xá
```

### Top 3 — `luat_duong_bo_2026_p54_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 54.

```text
a) Không được để tổ chức, cá nhân không có gi ấy phép kinh doanh v ận tải
bằng xe ô tô lo ại hình v ận tải hàng hóa thay mình th ực hiện điều hành phương
tiện và lái xe hoặc quyết định giá cước để vận tải hàng hóa;
b) Không được sử dụng người không có giấy phép lái xe hoặc có giấy phép
lái xe nhưng không phù hợp với loại xe, người có giấy phép lái xe bị trừ hết điểm,
người đang bị tước hoặc bị thu hồi giấy phép lái xe để điều khiển phương tiện vận
tải hàng hóa;
c) Cung cấp phương tiện đúng loại, thời gian, địa điểm và giao hàng hóa cho
người nhận hàng theo thỏa thuận trong hợp đồng; cấp giấy vận tải cho lái xe trước
khi thực hiện vận tải;
d) Hướng dẫn, kiểm tra vi ệc xếp, dỡ hàng hóa trên phương ti ện bảo đảm
không vượt quá khối lượng hàng hóa chuyên chở cho phép tham gia giao thông,
vượt
```

## Q17 — Config A

Câu hỏi: Trong Chương IV về vận tải đường bộ, đơn vị vận tải được miễn bồi thường hàng hóa ký gửi khi thiệt hại do nguyên nhân bất khả kháng không?

Đáp án tham chiếu: Có. Nguyên nhân bất khả kháng là một trong các trường hợp được miễn bồi thường thiệt hại hàng hóa ký gửi.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 56, 'evidence_quote': '7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi trong các trường hợp sau đây: a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao hụt ở mức cho phép; b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối với hàng hóa ký gửi; c) Do nguyên nhân bất khả kháng;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 chứa khoản 7 nêu rõ đơn vị kinh doanh vận tải được miễn bồi thường hàng hóa ký gửi và điểm c bất khả kháng. Cả chủ thể, đối tượng và ngoại lệ đều có, đủ trả lời có/không. Top-2 là trách nhiệm bồi thường hàng hóa thông thường, không dùng thay ngoại lệ; Top-3 nêu quy trình ký gửi, không thêm điều kiện làm đảo nghĩa. Không coi chỉ đúng Chương IV là đủ điểm. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p56_fixed_2 (PDF 56); luat_duong_bo_2026_p54_fixed_1 (PDF 54); luat_duong_bo_2026_p56_fixed_1 (PDF 56).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: nguồn chỉ rõ trường hợp bất khả kháng được miễn bồi thường hàng hóa ký gửi.

### Top 1 — `luat_duong_bo_2026_p56_fixed_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
ản.
5. Người nhận hàng hóa ký gửi phải xuất trình giấy tờ tùy thân khi nhận hàng.
6. Việc bồi thường thiệt hại hàng hóa ký g ửi thực hiện theo quy đ ịnh của
pháp luật về dân sự và quy định khác của pháp luật có liên quan, trừ trường hợp
quy định tại khoản 7 Điều này.
7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi
trong các trường hợp sau đây:
a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao
hụt ở mức cho phép;
b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối
với hàng hóa ký gửi;
c) Do nguyên nhân bất khả kháng;
d) Do lỗi của người thuê vận tải, người áp tải hàng hóa của người thuê vận tải
hoặc người nhận hàng hóa.
Điều 69. Hoạt động vận tải người bệnh bằng xe ô tô cứu thương
1. Dịch vụ vận tải người bệnh là việ
```

### Top 2 — `luat_duong_bo_2026_p54_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 54.

```text
, kiểm tra vi ệc xếp, dỡ hàng hóa trên phương ti ện bảo đảm
không vượt quá khối lượng hàng hóa chuyên chở cho phép tham gia giao thông,
vượt quá tải trọng, khổ giới hạn của đường bộ hoặc quá kích thước giới hạn cho
phép xếp hàng c ủa xe và th ực hiện các ch ỉ dẫn an toàn trong quá trình v ận tải,
giao nhận hàng hóa;
đ) Bồi thường thiệt hại do người lao động, người đại diện của đơn vị kinh
doanh vận tải hàng hóa bằng xe ô tô gây ra trong quá trình vận tải hàng hóa theo
quy định của pháp luật.
Điều 63. Quyền và nghĩa vụ của người lái xe vận tải hàng hóa bằng xe ô tô
1. Người lái xe vận tải hàng hóa bằng xe ô tô có quyền sau đây:
a) Từ chối điều khiển phương tiện khi phát hiện phương tiện không bảo đảm
các điều kiện về an toàn; phương tiện không có thiết bị giám sát hành trình, thiết
bị ghi n
```

### Top 3 — `luat_duong_bo_2026_p56_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
thuận giữa
người kinh doanh vận tải và người gửi hàng.
2. Chỉ được nhận vận tải hàng hóa có kích thư ớc, trọng lượng phù hợp với
phương tiện và không thuộc hàng hóa cấm lưu thông, hàng hóa nguy hiểm, động
vật hoang dã, hàng có mùi hôi th ối, động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường.
3. Người có hàng hóa ký gửi phải lập tờ khai gửi hàng hoá, trong đó kê khai
tên, số lượng, khối lượng hàng hoá; tên, địa chỉ, số định danh cá nhân của người
gửi và người nhận hàng hóa.
4. Đơn vị kinh doanh vận tải có trách nhiệm kiểm tra hàng hóa ký g ửi theo
tờ khai gửi hàng hóa và xác nhận vào tờ khai gửi hàng hóa. Tờ khai gửi hàng hóa
được lập thành 02 bản, mỗi bên giữ một bản.
5. Người nhận hàng hóa ký gửi phải xuất trình giấy tờ tùy thân khi nhận hàng.
6. Việc bồi thường
```

## Q17 — Config B

Câu hỏi: Trong Chương IV về vận tải đường bộ, đơn vị vận tải được miễn bồi thường hàng hóa ký gửi khi thiệt hại do nguyên nhân bất khả kháng không?

Đáp án tham chiếu: Có. Nguyên nhân bất khả kháng là một trong các trường hợp được miễn bồi thường thiệt hại hàng hóa ký gửi.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 56, 'evidence_quote': '7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi trong các trường hợp sau đây: a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao hụt ở mức cho phép; b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối với hàng hóa ký gửi; c) Do nguyên nhân bất khả kháng;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 có câu dẫn khoản 7 và điểm c về nguyên nhân bất khả kháng trong danh sách miễn bồi thường ký gửi. Top-2 dẫn chiếu khoản 7 sau quy trình tờ khai/nhận hàng; Top-3 về quyền đơn vị vận tải, không cung cấp ngoại lệ khác cần thiết. Các đầu/cuối chunk bị cắt không làm mất quan hệ chủ thể–miễn bồi thường–bất khả kháng cần cho câu hỏi hẹp này. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p56_paragraph_800_3 (PDF 56); luat_duong_bo_2026_p56_paragraph_800_2 (PDF 56); luat_duong_bo_2026_p53_paragraph_800_3 (PDF 53).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: đoạn trích có quy định miễn bồi thường và lý do bất khả kháng.

### Top 1 — `luat_duong_bo_2026_p56_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
định tại khoản 7 Điều này.
7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi
trong các trường hợp sau đây:
a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao
hụt ở mức cho phép;
b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối
với hàng hóa ký gửi;
c) Do nguyên nhân bất khả kháng;
d) Do lỗi của người thuê vận tải, người áp tải hàng hóa của người thuê vận tải
hoặc người nhận hàng hóa.
Điều 69. Hoạt động vận tải người bệnh bằng xe ô tô cứu thương
1. Dịch vụ vận tải người bệnh là việc tổ chức, cá nhân sử dụng xe ô tô c ứu
```

### Top 2 — `luat_duong_bo_2026_p56_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
và không thuộc hàng hóa cấm lưu thông, hàng hóa nguy hiểm, động
vật hoang dã, hàng có mùi hôi th ối, động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường.
3. Người có hàng hóa ký gửi phải lập tờ khai gửi hàng hoá, trong đó kê khai
tên, số lượng, khối lượng hàng hoá; tên, địa chỉ, số định danh cá nhân của người
gửi và người nhận hàng hóa.
4. Đơn vị kinh doanh vận tải có trách nhiệm kiểm tra hàng hóa ký g ửi theo
tờ khai gửi hàng hóa và xác nhận vào tờ khai gửi hàng hóa. Tờ khai gửi hàng hóa
được lập thành 02 bản, mỗi bên giữ một bản.
5. Người nhận hàng hóa ký gửi phải xuất trình giấy tờ tùy thân khi nhận hàng.
6. Việc bồi thường thiệt hại hàng hóa ký g ửi thực hiện theo quy đ ịnh của
pháp luật về dân sự và quy định khác của pháp luật có liên quan, trừ trường hợp
quy
```

### Top 3 — `luat_duong_bo_2026_p53_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
c thực của thông tin đó;
b) Yêu cầu người thuê vận tải thanh toán đủ tiền cước và chi phí phát sinh;
yêu c ầu ngư ời thuê v ận tải bồi thư ờng thi ệt hại do vi ph ạm thỏa thu ận trong
hợp đồng;
c) Từ chối vận tải nếu người thuê v ận tải không giao hàng hóa theo th ỏa
thuận trong hợp đồng;
d) Yêu cầu giám định hàng hóa khi cần thiết;
đ) Lưu giữ hàng hóa trong trường hợp người thuê vận tải không thanh toán
đủ tiền cước và chi phí phát sinh theo thoả thuận trong hợp đồng.
2. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có nghĩa vụ sau đây:
```

## Q17 — Config C

Câu hỏi: Trong Chương IV về vận tải đường bộ, đơn vị vận tải được miễn bồi thường hàng hóa ký gửi khi thiệt hại do nguyên nhân bất khả kháng không?

Đáp án tham chiếu: Có. Nguyên nhân bất khả kháng là một trong các trường hợp được miễn bồi thường thiệt hại hàng hóa ký gửi.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 56, 'evidence_quote': '7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi trong các trường hợp sau đây: a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao hụt ở mức cho phép; b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối với hàng hóa ký gửi; c) Do nguyên nhân bất khả kháng;'}]`

Filter thực tế trong trace: `{'metadata': {'chapter': 'IV'}}`

**AI đề xuất: 2/2.** Top-1 có câu dẫn khoản 7 và điểm c về nguyên nhân bất khả kháng trong danh sách miễn bồi thường ký gửi. Top-2 dẫn chiếu khoản 7 sau quy trình tờ khai/nhận hàng; Top-3 về quyền đơn vị vận tải, không cung cấp ngoại lệ khác cần thiết. Các đầu/cuối chunk bị cắt không làm mất quan hệ chủ thể–miễn bồi thường–bất khả kháng cần cho câu hỏi hẹp này. Đã đối chiếu lại cả ba chunk C với B: ID/text trùng; chỉ Q17 thực áp dụng filter chapter IV, các câu còn lại không filter. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p56_paragraph_800_3 (PDF 56); luat_duong_bo_2026_p56_paragraph_800_2 (PDF 56); luat_duong_bo_2026_p53_paragraph_800_3 (PDF 53).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: các đoạn bằng chứng tương tự B và đủ để kết luận.

### Top 1 — `luat_duong_bo_2026_p56_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
định tại khoản 7 Điều này.
7. Đơn vị kinh doanh vận tải được miễn bồi thường thiệt hại hàng hóa ký gửi
trong các trường hợp sau đây:
a) Do đặc tính tự nhiên hoặc khuyết tật vốn có của hàng hóa ký gửi hoặc hao
hụt ở mức cho phép;
b) Do việc bắt giữ hoặc cưỡng chế của cơ quan nhà nước có thẩm quyền đối
với hàng hóa ký gửi;
c) Do nguyên nhân bất khả kháng;
d) Do lỗi của người thuê vận tải, người áp tải hàng hóa của người thuê vận tải
hoặc người nhận hàng hóa.
Điều 69. Hoạt động vận tải người bệnh bằng xe ô tô cứu thương
1. Dịch vụ vận tải người bệnh là việc tổ chức, cá nhân sử dụng xe ô tô c ứu
```

### Top 2 — `luat_duong_bo_2026_p56_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
và không thuộc hàng hóa cấm lưu thông, hàng hóa nguy hiểm, động
vật hoang dã, hàng có mùi hôi th ối, động vật, hàng hóa khác có ảnh hưởng đến
sức khỏe của hành khách, môi trường.
3. Người có hàng hóa ký gửi phải lập tờ khai gửi hàng hoá, trong đó kê khai
tên, số lượng, khối lượng hàng hoá; tên, địa chỉ, số định danh cá nhân của người
gửi và người nhận hàng hóa.
4. Đơn vị kinh doanh vận tải có trách nhiệm kiểm tra hàng hóa ký g ửi theo
tờ khai gửi hàng hóa và xác nhận vào tờ khai gửi hàng hóa. Tờ khai gửi hàng hóa
được lập thành 02 bản, mỗi bên giữ một bản.
5. Người nhận hàng hóa ký gửi phải xuất trình giấy tờ tùy thân khi nhận hàng.
6. Việc bồi thường thiệt hại hàng hóa ký g ửi thực hiện theo quy đ ịnh của
pháp luật về dân sự và quy định khác của pháp luật có liên quan, trừ trường hợp
quy
```

### Top 3 — `luat_duong_bo_2026_p53_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 53.

```text
c thực của thông tin đó;
b) Yêu cầu người thuê vận tải thanh toán đủ tiền cước và chi phí phát sinh;
yêu c ầu ngư ời thuê v ận tải bồi thư ờng thi ệt hại do vi ph ạm thỏa thu ận trong
hợp đồng;
c) Từ chối vận tải nếu người thuê v ận tải không giao hàng hóa theo th ỏa
thuận trong hợp đồng;
d) Yêu cầu giám định hàng hóa khi cần thiết;
đ) Lưu giữ hàng hóa trong trường hợp người thuê vận tải không thanh toán
đủ tiền cước và chi phí phát sinh theo thoả thuận trong hợp đồng.
2. Đơn vị kinh doanh vận tải hàng hóa bằng xe ô tô có nghĩa vụ sau đây:
```

## Q18 — Config A

Câu hỏi: Nếu cơ sở giáo dục tự tổ chức xe đưa đón học sinh, phải đáp ứng quy định nào?

Đáp án tham chiếu: Phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 57, 'evidence_quote': 'a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non, học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 có khoản 2 cùng hai nhánh phân biệt cơ sở giáo dục tự tổ chức phải đáp ứng vận tải nội bộ, còn đơn vị kinh doanh phải đáp ứng kinh doanh vận tải. Đây là đúng điều kiện của câu hỏi. Top-2 có tiêu đề Điều 70 sau phần xe cứu thương; Top-3 là mô tả vận tải nội bộ người, chỉ hỗ trợ ngữ cảnh. Cuối Top-1 cắt khoản 3 về an toàn, nhưng không mất quy định được hỏi ở điểm a khoản 2. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p57_fixed_1 (PDF 57); luat_duong_bo_2026_p57_fixed_0 (PDF 57); luat_duong_bo_2026_p49_fixed_3 (PDF 49).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: nêu đúng yêu cầu đối với cơ sở giáo dục tự tổ chức vận tải.

### Top 1 — `luat_duong_bo_2026_p57_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
 trẻ em mầm non, học sinh bằng xe
ô tô
1. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô là hoạt
động sử dụng xe ô tô đ ể đưa đón trẻ em mầm non, học sinh đi lại giữa nơi ở và
nơi học tập hoặc tham gia các hoạt động khác.
2. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô do cơ
sở giáo dục tự tổ chức hoặc do đơn vị kinh doanh vận tải thực hiện và được quy
định như sau:
a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non,
học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;
b) Trường hợp đơn vị kinh doanh vận tải thực hiện đưa đón trẻ em mầm non,
học sinh bằng xe ô tô phải đáp ứng quy định về hoạt động kinh doanh vận tải bằng
xe ô tô.
3. Hoạt động vận tải đưa đón tr ẻ em mầm non, học sinh bằng xe ô tô ph ải
tuân thủ q
```

### Top 2 — `luat_duong_bo_2026_p57_fixed_0`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
CÔNG BÁO/Số 528-VBHN/Ngày 25-09-2026 58

thương có thiết bị y tế chuyên dùng để vận tải người bệnh cấp cứu hoặc vận tải
người bệnh.
2. Cơ sở khám bệnh, chữa bệnh, tổ chức, cá nhân cung c ấp dịch vụ vận tải
người bệnh và sử dụng xe ô tô c ứu thương để vận tải người bệnh phải đáp ứng
điều kiện theo quy định của pháp luật về khám bệnh, chữa bệnh và quy định khác
của pháp luật có liên quan.
3. Xe ô tô cứu thương vận tải người bệnh phải có dấu hiệu nhận diện, niêm
yết thông tin, lắp thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái
xe theo quy định của pháp luật về trật tự, an toàn giao thông đường bộ và quy định
khác của pháp luật có liên quan.
Điều 70. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe
ô tô
1. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe
```

### Top 3 — `luat_duong_bo_2026_p49_fixed_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 49.

```text
chức sử dụng xe ô tô, xe bốn bánh có gắn động cơ để vận tải
cán bộ, công nhân viên, người lao động hoặc trẻ em mầm non, học sinh, sinh viên
của cơ quan, tổ chức đó;
b) Hoạt động vận tải hàng hóa nội bộ bằng xe ô tô, bằng xe bốn bánh có gắn
động cơ là việc cơ quan, tổ chức, cá nhân sử dụng xe ô tô chở hàng, xe ô tô chuyên
dùng, xe bốn bánh có gắn động cơ để vận tải sản phẩm, hàng hóa do cơ quan, t ổ
chức, cá nhân đó sản xuất hoặc trang thiết bị, dụng cụ, nguyên vật liệu, nhiên liệu
```

## Q18 — Config B

Câu hỏi: Nếu cơ sở giáo dục tự tổ chức xe đưa đón học sinh, phải đáp ứng quy định nào?

Đáp án tham chiếu: Phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 57, 'evidence_quote': 'a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non, học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 giữ trọn điểm a khoản 2 về cơ sở giáo dục tự tổ chức và vận tải nội bộ, có điểm b đối chiếu với đơn vị kinh doanh và khoản 3 về an toàn. Top-2 có tiêu đề Điều 70, dù phần đầu nói xe cứu thương; Top-3 trang 23 nói tổ chức giao thông và không được dùng để suy ra nghĩa vụ giáo dục. Đáp án có điều kiện và nguồn đủ trong Top-1/2. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p57_paragraph_800_2 (PDF 57); luat_duong_bo_2026_p57_paragraph_800_1 (PDF 57); luat_duong_bo_2026_p23_paragraph_800_3 (PDF 23).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: có đủ điều kiện vận tải nội bộ và phân biệt trường hợp thuê đơn vị kinh doanh.

### Top 1 — `luat_duong_bo_2026_p57_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
a đón trẻ em mầm non, học sinh đi lại giữa nơi ở và
nơi học tập hoặc tham gia các hoạt động khác.
2. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô do cơ
sở giáo dục tự tổ chức hoặc do đơn vị kinh doanh vận tải thực hiện và được quy
định như sau:
a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non,
học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;
b) Trường hợp đơn vị kinh doanh vận tải thực hiện đưa đón trẻ em mầm non,
học sinh bằng xe ô tô phải đáp ứng quy định về hoạt động kinh doanh vận tải bằng
xe ô tô.
3. Hoạt động vận tải đưa đón tr ẻ em mầm non, học sinh bằng xe ô tô ph ải
tuân thủ quy định của pháp luật về trật tự, an toàn giao thông đường bộ.
Điều 71. Dịch vụ hỗ trợ vận tải đường bộ
Dịch vụ hỗ trợ vận tải đường bộ bao g
```

### Top 2 — `luat_duong_bo_2026_p57_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
thương có thiết bị y tế chuyên dùng để vận tải người bệnh cấp cứu hoặc vận tải
người bệnh.
2. Cơ sở khám bệnh, chữa bệnh, tổ chức, cá nhân cung c ấp dịch vụ vận tải
người bệnh và sử dụng xe ô tô c ứu thương để vận tải người bệnh phải đáp ứng
điều kiện theo quy định của pháp luật về khám bệnh, chữa bệnh và quy định khác
của pháp luật có liên quan.
3. Xe ô tô cứu thương vận tải người bệnh phải có dấu hiệu nhận diện, niêm
yết thông tin, lắp thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái
xe theo quy định của pháp luật về trật tự, an toàn giao thông đường bộ và quy định
khác của pháp luật có liên quan.
Điều 70. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe
ô tô
1. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô là hoạt
động sử dụng xe ô tô đ ể đư
```

### Top 3 — `luat_duong_bo_2026_p23_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 23.

```text
bộ; chiều đi,
tốc độ các phương tiện cơ giới tham gia giao thông đường bộ;
b) Tổ chức phân làn, phân luồng trên tuyến đường đang đầu tư xây dựng và
tại các tuyến đường bộ kết nối;
c) Quy định giao thông tại các nút giao, vị trí đấu nối với đường khác; quy
định về tránh, vượt xe trên đường, các điểm được phép dừng xe, đỗ xe trên đường,
vị trí đón, trả khách;
d) Quy định khổ giới hạn và tải trọng cho phép phương ti ện tham gia giao
thông đường bộ an toàn;
đ) Quy định thời gian cho phép tham gia giao thông; th ời gian cho phép đi
theo các hướng của đèn tín hiệu giao thông;
e) Quy định thời gian bật, tắt hệ thống chiếu sáng trên đường;
g) Quy định về các trường hợp tạm dừng khai thác m ột phần hoặc toàn bộ
tuyến đường;
```

## Q18 — Config C

Câu hỏi: Nếu cơ sở giáo dục tự tổ chức xe đưa đón học sinh, phải đáp ứng quy định nào?

Đáp án tham chiếu: Phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 57, 'evidence_quote': 'a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non, học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 giữ trọn điểm a khoản 2 về cơ sở giáo dục tự tổ chức và vận tải nội bộ, có điểm b đối chiếu với đơn vị kinh doanh và khoản 3 về an toàn. Top-2 có tiêu đề Điều 70, dù phần đầu nói xe cứu thương; Top-3 trang 23 nói tổ chức giao thông và không được dùng để suy ra nghĩa vụ giáo dục. Đáp án có điều kiện và nguồn đủ trong Top-1/2. Đã đối chiếu lại cả ba chunk C với B: ID/text trùng; chỉ Q17 thực áp dụng filter chapter IV, các câu còn lại không filter. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p57_paragraph_800_2 (PDF 57); luat_duong_bo_2026_p57_paragraph_800_1 (PDF 57); luat_duong_bo_2026_p23_paragraph_800_3 (PDF 23).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: thông tin cần trả lời đầy đủ và nhất quán với B.

### Top 1 — `luat_duong_bo_2026_p57_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
a đón trẻ em mầm non, học sinh đi lại giữa nơi ở và
nơi học tập hoặc tham gia các hoạt động khác.
2. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô do cơ
sở giáo dục tự tổ chức hoặc do đơn vị kinh doanh vận tải thực hiện và được quy
định như sau:
a) Trường hợp cơ sở giáo dục tự tổ chức hoạt động đưa đón trẻ em mầm non,
học sinh phải đáp ứng quy định về hoạt động vận tải nội bộ bằng xe ô tô;
b) Trường hợp đơn vị kinh doanh vận tải thực hiện đưa đón trẻ em mầm non,
học sinh bằng xe ô tô phải đáp ứng quy định về hoạt động kinh doanh vận tải bằng
xe ô tô.
3. Hoạt động vận tải đưa đón tr ẻ em mầm non, học sinh bằng xe ô tô ph ải
tuân thủ quy định của pháp luật về trật tự, an toàn giao thông đường bộ.
Điều 71. Dịch vụ hỗ trợ vận tải đường bộ
Dịch vụ hỗ trợ vận tải đường bộ bao g
```

### Top 2 — `luat_duong_bo_2026_p57_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 57.

```text
thương có thiết bị y tế chuyên dùng để vận tải người bệnh cấp cứu hoặc vận tải
người bệnh.
2. Cơ sở khám bệnh, chữa bệnh, tổ chức, cá nhân cung c ấp dịch vụ vận tải
người bệnh và sử dụng xe ô tô c ứu thương để vận tải người bệnh phải đáp ứng
điều kiện theo quy định của pháp luật về khám bệnh, chữa bệnh và quy định khác
của pháp luật có liên quan.
3. Xe ô tô cứu thương vận tải người bệnh phải có dấu hiệu nhận diện, niêm
yết thông tin, lắp thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái
xe theo quy định của pháp luật về trật tự, an toàn giao thông đường bộ và quy định
khác của pháp luật có liên quan.
Điều 70. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe
ô tô
1. Hoạt động vận tải đưa đón trẻ em mầm non, học sinh bằng xe ô tô là hoạt
động sử dụng xe ô tô đ ể đư
```

### Top 3 — `luat_duong_bo_2026_p23_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 23.

```text
bộ; chiều đi,
tốc độ các phương tiện cơ giới tham gia giao thông đường bộ;
b) Tổ chức phân làn, phân luồng trên tuyến đường đang đầu tư xây dựng và
tại các tuyến đường bộ kết nối;
c) Quy định giao thông tại các nút giao, vị trí đấu nối với đường khác; quy
định về tránh, vượt xe trên đường, các điểm được phép dừng xe, đỗ xe trên đường,
vị trí đón, trả khách;
d) Quy định khổ giới hạn và tải trọng cho phép phương ti ện tham gia giao
thông đường bộ an toàn;
đ) Quy định thời gian cho phép tham gia giao thông; th ời gian cho phép đi
theo các hướng của đèn tín hiệu giao thông;
e) Quy định thời gian bật, tắt hệ thống chiếu sáng trên đường;
g) Quy định về các trường hợp tạm dừng khai thác m ột phần hoặc toàn bộ
tuyến đường;
```

## Q19 — Config A

Câu hỏi: Đơn vị kinh doanh dịch vụ bãi đỗ xe có được cung cấp dịch vụ sửa chữa phương tiện không?

Đáp án tham chiếu: Có. Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ là một trong các dịch vụ được phép thực hiện.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 58, 'evidence_quote': '2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các dịch vụ sau đây: a) Trông giữ phương tiện giao thông đường bộ; b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 giữ tiêu đề Điều 73, chủ thể đơn vị dịch vụ bãi đỗ xe, câu dẫn khoản 2 và điểm b bảo dưỡng/sửa chữa phương tiện; quan hệ được phép thực hiện dịch vụ rõ ràng. Top-2 là các nghĩa vụ trông giữ tiếp theo ở trang 59, Top-3 dừng ở đầu Điều 73 nên không cần dùng để bổ sung quyền. Không thiếu thông tin cốt lõi. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p58_fixed_2 (PDF 58); luat_duong_bo_2026_p59_fixed_0 (PDF 59); luat_duong_bo_2026_p58_fixed_1 (PDF 58).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: nguồn nêu rõ bãi đỗ xe được cung cấp dịch vụ bảo dưỡng, sửa chữa.

### Top 1 — `luat_duong_bo_2026_p58_fixed_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
 đầu mối kết nối giao thông.
Điều 73. Dịch vụ bãi đỗ xe
1. Đơn v ị kinh doanh d ịch vụ bãi đỗ xe được thành l ập theo quy đ ịnh của
pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các dịch vụ sau đây:
a) Trông giữ phương tiện giao thông đường bộ;
b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;
c) Cung cấp nhiên liệu, năng lượng cho phương tiện giao thông đường bộ;
d) Dịch vụ khác theo quy định của pháp luật.
3. Đơn vị kinh doanh dịch vụ bãi đỗ xe có quyền và nghĩa vụ sau đây:
a) Bảo đảm an ninh, trật tự, vệ sinh môi trường và phòng, chống cháy, nổ tại
bãi đỗ xe;
b) Niêm yết công khai nội quy, giá dịch vụ tại bãi đỗ xe, tên và số điện thoại cơ
quan quản lý nhà nước có thẩm quyền để chủ xe phản ánh, khiếu nại khi cần thiết;
```

### Top 2 — `luat_duong_bo_2026_p59_fixed_0`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 59.

```text
CÔNG BÁO/Số 528-VBHN/Ngày 25-09-2026 60

c) Bồi thường thiệt hại nếu để xảy ra mất mát, hư hỏng phương tiện giao thông
đường bộ nhận trông giữ;
d) Thu tiền trông giữ phương tiện giao thông đường bộ;
đ) Không được để các chủ phương tiện kinh doanh vận tải sử dụng bãi đỗ xe để
đón, trả khách hoặc xếp, dỡ hàng hóa, đóng gói, sang tải hàng hóa;
e) Từ chối phục vụ đối với chủ phương tiện giao thông đường bộ không chấp
hành nội quy bãi đỗ xe;
g) Chịu sự kiểm tra, giám sát của cơ quan nhà nước có thẩm quyền.
Điều 74. Dịch vụ đại lý vận tải hàng hóa
1. Đơn vị kinh doanh dịch vụ đại lý vận tải hàng hóa được thành lập theo quy
định của pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Dịch vụ đại lý vận tải hàng hóa là việc tổ chức, cá nhân được đơn vị kinh
doanh vận tải thuê thực hiện một hoặc
```

### Top 3 — `luat_duong_bo_2026_p58_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
e ra, vào bến xe hàng
theo quy định của pháp luật về giá.
5. Đơn vị kinh doanh dịch vụ trạm dừng nghỉ có quyền, nghĩa vụ sau đây:
a) T ổ chức d ịch v ụ phục v ụ người và phương ti ện tham gia giao thông
đường bộ;
b) Thực hiện công việc theo hợp đồng ủy thác với đơn vị kinh doanh vận tải.
6. Ủy ban nhân dân c ấp tỉnh căn cứ vào loại bến xe để định giá dịch vụ xe
ra, vào bến xe theo quy định của pháp luật về giá.
7. Ủy ban nhân dân c ấp tỉnh bố trí quỹ đất xây dựng bến xe khách, b ến xe
hàng hoặc điểm trung chuyển hành khách tại các khu vực trung tâm của đô thị để
kết nối liên thông giữa các phương thức vận tải hành khách trong và ngoài đô thị.
Bến xe khách phải được bố trí ổn định tại khu vực đầu mối kết nối giao thông.
Điều 73. Dịch vụ bãi đỗ xe
1. Đơn v ị kinh doanh d ịch vụ bãi đỗ xe đượ
```

## Q19 — Config B

Câu hỏi: Đơn vị kinh doanh dịch vụ bãi đỗ xe có được cung cấp dịch vụ sửa chữa phương tiện không?

Đáp án tham chiếu: Có. Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ là một trong các dịch vụ được phép thực hiện.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 58, 'evidence_quote': '2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các dịch vụ sau đây: a) Trông giữ phương tiện giao thông đường bộ; b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 nêu điểm b bảo dưỡng/sửa chữa nhưng bị mất chủ thể ở đầu khoản 2. Top-3 cùng trang 58 giữ tiêu đề Điều 73 và câu dẫn đơn vị dịch vụ bãi đỗ xe được thực hiện các; nối hai đoạn trong chính Top-3 xác định được dịch vụ sửa chữa thuộc đúng chủ thể. Top-2 tiếp các nghĩa vụ trông giữ rồi sang Điều 74, không thay đổi kết luận. Đủ bằng chứng khi đọc cả bộ, nhưng không một chunk giữ đủ gold nên Evidence Hit\@3 vẫn 0; đây là đánh giá ngữ nghĩa AI, không sửa metric. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p58_paragraph_800_3 (PDF 58); luat_duong_bo_2026_p59_paragraph_800_1 (PDF 59); luat_duong_bo_2026_p58_paragraph_800_2 (PDF 58).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: tuy thông tin nằm ở nhiều đoạn nhưng kết hợp lại xác định rõ quyền cung cấp dịch vụ.

### Top 1 — `luat_duong_bo_2026_p58_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
 dịch vụ sau đây:
a) Trông giữ phương tiện giao thông đường bộ;
b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;
c) Cung cấp nhiên liệu, năng lượng cho phương tiện giao thông đường bộ;
d) Dịch vụ khác theo quy định của pháp luật.
3. Đơn vị kinh doanh dịch vụ bãi đỗ xe có quyền và nghĩa vụ sau đây:
a) Bảo đảm an ninh, trật tự, vệ sinh môi trường và phòng, chống cháy, nổ tại
bãi đỗ xe;
b) Niêm yết công khai nội quy, giá dịch vụ tại bãi đỗ xe, tên và số điện thoại cơ
quan quản lý nhà nước có thẩm quyền để chủ xe phản ánh, khiếu nại khi cần thiết;
```

### Top 2 — `luat_duong_bo_2026_p59_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 59.

```text
c) Bồi thường thiệt hại nếu để xảy ra mất mát, hư hỏng phương tiện giao thông
đường bộ nhận trông giữ;
d) Thu tiền trông giữ phương tiện giao thông đường bộ;
đ) Không được để các chủ phương tiện kinh doanh vận tải sử dụng bãi đỗ xe để
đón, trả khách hoặc xếp, dỡ hàng hóa, đóng gói, sang tải hàng hóa;
e) Từ chối phục vụ đối với chủ phương tiện giao thông đường bộ không chấp
hành nội quy bãi đỗ xe;
g) Chịu sự kiểm tra, giám sát của cơ quan nhà nước có thẩm quyền.
Điều 74. Dịch vụ đại lý vận tải hàng hóa
1. Đơn vị kinh doanh dịch vụ đại lý vận tải hàng hóa được thành lập theo quy
định của pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Dịch vụ đại lý vận tải hàng hóa là việc tổ chức, cá nhân được đơn vị kinh
doanh vận tải thuê thực hiện một hoặc nhiều công đoạn trong quá trình v ận tải
```

### Top 3 — `luat_duong_bo_2026_p58_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
 d ịch v ụ phục v ụ người và phương ti ện tham gia giao thông
đường bộ;
b) Thực hiện công việc theo hợp đồng ủy thác với đơn vị kinh doanh vận tải.
6. Ủy ban nhân dân c ấp tỉnh căn cứ vào loại bến xe để định giá dịch vụ xe
ra, vào bến xe theo quy định của pháp luật về giá.
7. Ủy ban nhân dân c ấp tỉnh bố trí quỹ đất xây dựng bến xe khách, b ến xe
hàng hoặc điểm trung chuyển hành khách tại các khu vực trung tâm của đô thị để
kết nối liên thông giữa các phương thức vận tải hành khách trong và ngoài đô thị.
Bến xe khách phải được bố trí ổn định tại khu vực đầu mối kết nối giao thông.
Điều 73. Dịch vụ bãi đỗ xe
1. Đơn v ị kinh doanh d ịch vụ bãi đỗ xe được thành l ập theo quy đ ịnh của
pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các
```

## Q19 — Config C

Câu hỏi: Đơn vị kinh doanh dịch vụ bãi đỗ xe có được cung cấp dịch vụ sửa chữa phương tiện không?

Đáp án tham chiếu: Có. Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ là một trong các dịch vụ được phép thực hiện.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 58, 'evidence_quote': '2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các dịch vụ sau đây: a) Trông giữ phương tiện giao thông đường bộ; b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 nêu điểm b bảo dưỡng/sửa chữa nhưng bị mất chủ thể ở đầu khoản 2. Top-3 cùng trang 58 giữ tiêu đề Điều 73 và câu dẫn đơn vị dịch vụ bãi đỗ xe được thực hiện các; nối hai đoạn trong chính Top-3 xác định được dịch vụ sửa chữa thuộc đúng chủ thể. Top-2 tiếp các nghĩa vụ trông giữ rồi sang Điều 74, không thay đổi kết luận. Đủ bằng chứng khi đọc cả bộ, nhưng không một chunk giữ đủ gold nên Evidence Hit\@3 vẫn 0; đây là đánh giá ngữ nghĩa AI, không sửa metric. Đã đối chiếu lại cả ba chunk C với B: ID/text trùng; chỉ Q17 thực áp dụng filter chapter IV, các câu còn lại không filter. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p58_paragraph_800_3 (PDF 58); luat_duong_bo_2026_p59_paragraph_800_1 (PDF 59); luat_duong_bo_2026_p58_paragraph_800_2 (PDF 58).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: có thể nối các đoạn để xác định đúng chủ thể và dịch vụ được phép thực hiện.

### Top 1 — `luat_duong_bo_2026_p58_paragraph_800_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
 dịch vụ sau đây:
a) Trông giữ phương tiện giao thông đường bộ;
b) Bảo dưỡng, sửa chữa phương tiện giao thông đường bộ;
c) Cung cấp nhiên liệu, năng lượng cho phương tiện giao thông đường bộ;
d) Dịch vụ khác theo quy định của pháp luật.
3. Đơn vị kinh doanh dịch vụ bãi đỗ xe có quyền và nghĩa vụ sau đây:
a) Bảo đảm an ninh, trật tự, vệ sinh môi trường và phòng, chống cháy, nổ tại
bãi đỗ xe;
b) Niêm yết công khai nội quy, giá dịch vụ tại bãi đỗ xe, tên và số điện thoại cơ
quan quản lý nhà nước có thẩm quyền để chủ xe phản ánh, khiếu nại khi cần thiết;
```

### Top 2 — `luat_duong_bo_2026_p59_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 59.

```text
c) Bồi thường thiệt hại nếu để xảy ra mất mát, hư hỏng phương tiện giao thông
đường bộ nhận trông giữ;
d) Thu tiền trông giữ phương tiện giao thông đường bộ;
đ) Không được để các chủ phương tiện kinh doanh vận tải sử dụng bãi đỗ xe để
đón, trả khách hoặc xếp, dỡ hàng hóa, đóng gói, sang tải hàng hóa;
e) Từ chối phục vụ đối với chủ phương tiện giao thông đường bộ không chấp
hành nội quy bãi đỗ xe;
g) Chịu sự kiểm tra, giám sát của cơ quan nhà nước có thẩm quyền.
Điều 74. Dịch vụ đại lý vận tải hàng hóa
1. Đơn vị kinh doanh dịch vụ đại lý vận tải hàng hóa được thành lập theo quy
định của pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Dịch vụ đại lý vận tải hàng hóa là việc tổ chức, cá nhân được đơn vị kinh
doanh vận tải thuê thực hiện một hoặc nhiều công đoạn trong quá trình v ận tải
```

### Top 3 — `luat_duong_bo_2026_p58_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 58.

```text
 d ịch v ụ phục v ụ người và phương ti ện tham gia giao thông
đường bộ;
b) Thực hiện công việc theo hợp đồng ủy thác với đơn vị kinh doanh vận tải.
6. Ủy ban nhân dân c ấp tỉnh căn cứ vào loại bến xe để định giá dịch vụ xe
ra, vào bến xe theo quy định của pháp luật về giá.
7. Ủy ban nhân dân c ấp tỉnh bố trí quỹ đất xây dựng bến xe khách, b ến xe
hàng hoặc điểm trung chuyển hành khách tại các khu vực trung tâm của đô thị để
kết nối liên thông giữa các phương thức vận tải hành khách trong và ngoài đô thị.
Bến xe khách phải được bố trí ổn định tại khu vực đầu mối kết nối giao thông.
Điều 73. Dịch vụ bãi đỗ xe
1. Đơn v ị kinh doanh d ịch vụ bãi đỗ xe được thành l ập theo quy đ ịnh của
pháp luật về doanh nghiệp, pháp luật về hợp tác xã.
2. Đơn vị kinh doanh dịch vụ bãi đỗ xe được thực hiện các
```

## Q20 — Config A

Câu hỏi: Xe cứu hộ giao thông đường bộ có được dùng để kinh doanh vận tải hàng hóa bằng ô tô không?

Đáp án tham chiếu: Không. Tổ chức, cá nhân kinh doanh cứu hộ không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 61, 'evidence_quote': 'c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Điểm c trong Top-1 cấm nguyên văn dùng xe cứu hộ kinh doanh vận tải hàng hóa bằng ô tô; khoản 2 ngay sau xác nhận ngữ cảnh tổ chức/cá nhân dịch vụ cứu hộ. Top-2 nói xe cứu thương, Top-3 định nghĩa kinh doanh vận tải nên không dùng thay lệnh cấm. Dù đầu chunk mất đầu khoản 1, câu c tự đủ cho câu hỏi về xe cứu hộ và truy được trang 61. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p61_fixed_1 (PDF 61); luat_duong_bo_2026_p56_fixed_3 (PDF 56); luat_duong_bo_2026_p48_fixed_2 (PDF 48).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: quy định cấm dùng xe cứu hộ để kinh doanh vận tải hàng hóa được trích rõ.

### Top 1 — `luat_duong_bo_2026_p61_fixed_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 61.

```text
vụ cứu hộ giao thông đường bộ phải
đáp ứng các yêu cầu sau đây:
a) Được thành lập theo quy định của pháp luật về doanh nghiệp, pháp luật về
hợp tác xã;
b) Phải bảo đảm an toàn giao thông, an toàn lao đ ộng trong quá trình th ực
hiện cứu hộ;
c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.
2. Tổ chức, cá nhân kinh doanh dịch vụ cứu hộ giao thông đường bộ có trách
nhiệm thực hiện quy định của pháp luật về trật tự, an toàn giao thông đường bộ.
Điều 80. Dịch vụ phần mềm hỗ trợ kết nối vận tải bằng xe ô tô
1. Phần mềm hỗ trợ kết nối vận tải bằng xe ô tô là giao thức kết nối giữa đơn
vị kinh doanh vận tải, người lái xe với hành khách hoặc người thuê vận tải diễn
ra trong môi trường điện tử.
2. Tổ chức, cá nhân kinh doanh v ận tải bằng xe ô tô sử dụng phần mềm hỗ
trợ k
```

### Top 2 — `luat_duong_bo_2026_p56_fixed_3`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 56.

```text
.
Điều 69. Hoạt động vận tải người bệnh bằng xe ô tô cứu thương
1. Dịch vụ vận tải người bệnh là việc tổ chức, cá nhân sử dụng xe ô tô c ứu
```

### Top 3 — `luat_duong_bo_2026_p48_fixed_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 48.

```text
inh doanh v ận tải hàng hoá. Kinh doanh v ận
tải bằng xe ô tô, bằng xe bốn bánh có gắn động cơ là việc tổ chức, cá nhân thực
hiện ít nhất một trong các công đoạn gồm: điều hành phương tiện và lái xe hoặc
quyết định giá cước vận tải để vận tải hành khách, hàng hóa trên đường bộ nhằm
mục đích sinh l ợi, trừ các hoạt động vận tải nội bộ được quy định tại khoản 12
Điều này.
6. Kinh doanh vận tải hành khách bằng xe ô tô gồm: kinh doanh vận tải hành
khách theo tuyến cố định, kinh doanh vận tải hành khách công cộng bằng xe buýt,
kinh doanh vận tải hành khách bằng xe taxi, kinh doanh vận tải hành khách theo hợp
đồng và loại hình kinh doanh vận tải hành khách mới theo quy định của Chính phủ.
7. Kinh doanh vận tải hành khách theo tuyến cố định là loại hình kinh doanh
vận tải hành khách sử dụng xe ô
```

## Q20 — Config B

Câu hỏi: Xe cứu hộ giao thông đường bộ có được dùng để kinh doanh vận tải hàng hóa bằng ô tô không?

Đáp án tham chiếu: Không. Tổ chức, cá nhân kinh doanh cứu hộ không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 61, 'evidence_quote': 'c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 có trọn lệnh cấm tại điểm c và khoản 2 về tổ chức/cá nhân kinh doanh cứu hộ. Top-2 có tiêu đề Điều 79 và câu dẫn chủ thể, giúp xác định ngữ cảnh mà đầu Top-1 đã mất; Top-3 là các cấm trong vận tải hàng hóa nói chung, không được dùng để khái quát thêm. Không thiếu yếu tố để trả lời không và dẫn nguồn đúng. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p61_paragraph_800_2 (PDF 61); luat_duong_bo_2026_p61_paragraph_800_1 (PDF 61); luat_duong_bo_2026_p54_paragraph_800_1 (PDF 54).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: quy định cấm và ngữ cảnh dịch vụ cứu hộ đủ để trả lời.

### Top 1 — `luat_duong_bo_2026_p61_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 61.

```text
ợp tác xã;
b) Phải bảo đảm an toàn giao thông, an toàn lao đ ộng trong quá trình th ực
hiện cứu hộ;
c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.
2. Tổ chức, cá nhân kinh doanh dịch vụ cứu hộ giao thông đường bộ có trách
nhiệm thực hiện quy định của pháp luật về trật tự, an toàn giao thông đường bộ.
Điều 80. Dịch vụ phần mềm hỗ trợ kết nối vận tải bằng xe ô tô
1. Phần mềm hỗ trợ kết nối vận tải bằng xe ô tô là giao thức kết nối giữa đơn
vị kinh doanh vận tải, người lái xe với hành khách hoặc người thuê vận tải diễn
ra trong môi trường điện tử.
2. Tổ chức, cá nhân kinh doanh v ận tải bằng xe ô tô sử dụng phần mềm hỗ
trợ kết nối vận tải bằng xe ô tô ph ải tuân th ủ các quy định về kinh doanh, điều
kiện kinh doanh vận tải bằng xe ô tô, pháp luật về giao dịch điệ
```

### Top 2 — `luat_duong_bo_2026_p61_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 61.

```text
4. Đơn v ị kinh doanh dịch vụ cho thuê phương ti ện để kinh doanh vận tải
bằng xe ô tô, vận tải nội bộ phải đáp ứng các yêu cầu sau đây:
a) Được thành lập theo quy định của pháp luật về doanh nghiệp, pháp luật về
hợp tác xã. Đối với nhà cung cấp dịch vụ nước ngoài chỉ được cung cấp dịch vụ
thông qua thành lập liên doanh với đối tác Việt Nam theo tỷ lệ vốn góp theo quy
định của điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam là thành
viên và quy định của pháp luật có liên quan;
b) Phải ký kết hợp đồng cho thuê phương ti ện không kèm người lái xe v ới
bên thuê.
Điều 79. Dịch vụ cứu hộ giao thông đường bộ
1. Tổ chức, cá nhân kinh doanh d ịch vụ cứu hộ giao thông đường bộ phải
đáp ứng các yêu cầu sau đây:
a) Được thành lập theo quy định của pháp luật về doanh nghiệp, pháp luật về
h
```

### Top 3 — `luat_duong_bo_2026_p54_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 54.

```text
a) Không được để tổ chức, cá nhân không có gi ấy phép kinh doanh v ận tải
bằng xe ô tô lo ại hình v ận tải hàng hóa thay mình th ực hiện điều hành phương
tiện và lái xe hoặc quyết định giá cước để vận tải hàng hóa;
b) Không được sử dụng người không có giấy phép lái xe hoặc có giấy phép
lái xe nhưng không phù hợp với loại xe, người có giấy phép lái xe bị trừ hết điểm,
người đang bị tước hoặc bị thu hồi giấy phép lái xe để điều khiển phương tiện vận
tải hàng hóa;
c) Cung cấp phương tiện đúng loại, thời gian, địa điểm và giao hàng hóa cho
người nhận hàng theo thỏa thuận trong hợp đồng; cấp giấy vận tải cho lái xe trước
khi thực hiện vận tải;
d) Hướng dẫn, kiểm tra vi ệc xếp, dỡ hàng hóa trên phương ti ện bảo đảm
không vượt quá khối lượng hàng hóa chuyên chở cho phép tham gia giao thông,
vượt
```

## Q20 — Config C

Câu hỏi: Xe cứu hộ giao thông đường bộ có được dùng để kinh doanh vận tải hàng hóa bằng ô tô không?

Đáp án tham chiếu: Không. Tổ chức, cá nhân kinh doanh cứu hộ không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.

Gold: `[{'gold_source_id': 'luat_duong_bo_2026', 'gold_page': 61, 'evidence_quote': 'c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.'}]`

Filter thực tế trong trace: `None`

**AI đề xuất: 2/2.** Top-1 có trọn lệnh cấm tại điểm c và khoản 2 về tổ chức/cá nhân kinh doanh cứu hộ. Top-2 có tiêu đề Điều 79 và câu dẫn chủ thể, giúp xác định ngữ cảnh mà đầu Top-1 đã mất; Top-3 là các cấm trong vận tải hàng hóa nói chung, không được dùng để khái quát thêm. Không thiếu yếu tố để trả lời không và dẫn nguồn đúng. Đã đối chiếu lại cả ba chunk C với B: ID/text trùng; chỉ Q17 thực áp dụng filter chapter IV, các câu còn lại không filter. Minh chứng theo thứ tự Top-1/2/3: luat_duong_bo_2026_p61_paragraph_800_2 (PDF 61); luat_duong_bo_2026_p61_paragraph_800_1 (PDF 61); luat_duong_bo_2026_p54_paragraph_800_1 (PDF 54).

AI reviewer: Codex AI — đọc lại evidence, không phải human reviewer; thời điểm AI: 2026-11-14T16:20:01.865017+07:00.

Người học: 2. Đồng ý mức 2: bằng chứng nêu đầy đủ lệnh cấm và phù hợp với câu hỏi.

### Top 1 — `luat_duong_bo_2026_p61_paragraph_800_2`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 61.

```text
ợp tác xã;
b) Phải bảo đảm an toàn giao thông, an toàn lao đ ộng trong quá trình th ực
hiện cứu hộ;
c) Không được sử dụng xe cứu hộ để kinh doanh vận tải hàng hóa bằng xe ô tô.
2. Tổ chức, cá nhân kinh doanh dịch vụ cứu hộ giao thông đường bộ có trách
nhiệm thực hiện quy định của pháp luật về trật tự, an toàn giao thông đường bộ.
Điều 80. Dịch vụ phần mềm hỗ trợ kết nối vận tải bằng xe ô tô
1. Phần mềm hỗ trợ kết nối vận tải bằng xe ô tô là giao thức kết nối giữa đơn
vị kinh doanh vận tải, người lái xe với hành khách hoặc người thuê vận tải diễn
ra trong môi trường điện tử.
2. Tổ chức, cá nhân kinh doanh v ận tải bằng xe ô tô sử dụng phần mềm hỗ
trợ kết nối vận tải bằng xe ô tô ph ải tuân th ủ các quy định về kinh doanh, điều
kiện kinh doanh vận tải bằng xe ô tô, pháp luật về giao dịch điệ
```

### Top 2 — `luat_duong_bo_2026_p61_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 61.

```text
4. Đơn v ị kinh doanh dịch vụ cho thuê phương ti ện để kinh doanh vận tải
bằng xe ô tô, vận tải nội bộ phải đáp ứng các yêu cầu sau đây:
a) Được thành lập theo quy định của pháp luật về doanh nghiệp, pháp luật về
hợp tác xã. Đối với nhà cung cấp dịch vụ nước ngoài chỉ được cung cấp dịch vụ
thông qua thành lập liên doanh với đối tác Việt Nam theo tỷ lệ vốn góp theo quy
định của điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam là thành
viên và quy định của pháp luật có liên quan;
b) Phải ký kết hợp đồng cho thuê phương ti ện không kèm người lái xe v ới
bên thuê.
Điều 79. Dịch vụ cứu hộ giao thông đường bộ
1. Tổ chức, cá nhân kinh doanh d ịch vụ cứu hộ giao thông đường bộ phải
đáp ứng các yêu cầu sau đây:
a) Được thành lập theo quy định của pháp luật về doanh nghiệp, pháp luật về
h
```

### Top 3 — `luat_duong_bo_2026_p54_paragraph_800_1`

Nguồn: `2026_528-VBHN_144_2026_VBHN-LQ-VPQH.pdf`; document_id: `luat_duong_bo_2026`; trang PDF: 54.

```text
a) Không được để tổ chức, cá nhân không có gi ấy phép kinh doanh v ận tải
bằng xe ô tô lo ại hình v ận tải hàng hóa thay mình th ực hiện điều hành phương
tiện và lái xe hoặc quyết định giá cước để vận tải hàng hóa;
b) Không được sử dụng người không có giấy phép lái xe hoặc có giấy phép
lái xe nhưng không phù hợp với loại xe, người có giấy phép lái xe bị trừ hết điểm,
người đang bị tước hoặc bị thu hồi giấy phép lái xe để điều khiển phương tiện vận
tải hàng hóa;
c) Cung cấp phương tiện đúng loại, thời gian, địa điểm và giao hàng hóa cho
người nhận hàng theo thỏa thuận trong hợp đồng; cấp giấy vận tải cho lái xe trước
khi thực hiện vận tải;
d) Hướng dẫn, kiểm tra vi ệc xếp, dỡ hàng hóa trên phương ti ện bảo đảm
không vượt quá khối lượng hàng hóa chuyên chở cho phép tham gia giao thông,
vượt
```
