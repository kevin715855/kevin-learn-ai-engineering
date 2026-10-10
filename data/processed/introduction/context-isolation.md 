# 4 chiến lược quản lý ngữ cảnh mà mọi AI Engineer cần biết

## 1. Mục tiêu học tập

Sau bài học này, bạn sẽ能够：

- Giải thích tại sao **context window** (cửa sổ ngữ cảnh) là bộ nhớ làm việc của mô hình LLM và tại sao nó dễ bị “saturate”.
- Nhận biết bốn dạng hỏng hóc của ngữ cảnh: **context poisoning, distraction, confusion, clash**.
- Áp dụng ba chiến lược chính – **Write (lưu trữ bên ngoài), Select (truy xuất theo nhu cầu), Compress and Prune (tóm tắt & cắt bớt)** – để giảm tải token trong cửa sổ.
- Thiết kế hệ thống **multi‑agent (Isolate)** để cô lập các tác vụ tốn nhiều token và nâng cao chất lượng trả lời.
- Kết hợp các chiến lược trên để xây dựng AI agent ổn định trong các luồng đối thoại dài (ví dụ: agent debug log sản xuất).

## 2. Tổng quan

Khi trò chuyện với một mô hình LLM, mọi thông tin – prompt trước đó, lịch sử hội thoại, kết quả gọi công cụ, tài liệu được truy xuất – đều được đưa vào **context window** trước khi mô hình sinh ra token tiếp theo. Andrej Karpathy so sánh LLM như một **CPU** và context window như **RAM**: mọi thứ phải “fit” vào bộ nhớ này để mô hình có thể xử lý.

Trong thực tế, cửa sổ thường có hạn (ví dụ: 32 k, 100 k hoặc 200 k token). Ngay trước khi đạt đến giới hạn, mô hình còn chịu 현象 **context rot** – chất lượng phản hồi suy giảm khi nhiều token dồn vào cửa sổ, dù vẫn còn chỗ trống. Điều này giống như việc tìm một ghi chú quan trọng trên bàn làm việc: với 10 tờ giấy dễ dàng, nhưng với 1.000 tờ thì gần như không thể.

Trong bài viết gốc, tác giả Owain Lewis mô tả việc xây dựng một AI agent giúp debug các sự cố sản xuất. Agent đó cần đọc logs từ nhiều nguồn, nhưng sau vài lượt trao đổi, cửa sổ context już đầy, dẫn đến việc agent “l locais”, bắt đầu pip tôt hoặc gây ra hallucination. Giải pháp không phải là đổi mô hình hay tăng dữ liệu, mà là **thinking lại cách quản lý ngữ cảnh** – chính là **context engineering**.

## 3. Kiến thức cốt lõi

### 3.1. Các vấn đề thường gặp với context window

| Vấn đề | Mô tả | Hậu quả |
|--------|-------|---------|
| **Context Poisoning** | Một hallucination (thông tin sai) xuất hiện trong context và lan truyền vào mọi suy luận tiếp theo. | Agent trả lời sai sự thực liền mạch. |
| **Context Distraction** | Quá nhiều thông tin (thường là noise) làmモデル pierde tập trung vào nội dung quan trọng. | Trả lời nông lành, bỏ qua điểm then chốt. |
| **Context Confusion** | Thông tin không related ảnh hưởng đến suy luận, khiếnmodel“suy nghĩ lẫn lộn”. | Kết quả không nhất quán, khó dự đoán. |
| **Context Clash** | Hai phần trong context mâu thuẫn (ví dụ: hai bản ghi log mô tả trạng thái khác nhau). | Model phải “chọn lẫn” và thường cho ra câu trả lời không chắc chắn. |

Nếu agent hoạt động tốt ở đầu conversation nhưng sau đó bắt đầu drift (suy giảm chất lượng), một trong bốn vấn đề trên thường là nguyên nhân.

### 3.2. Ba chiến lược cơ bản (Write – Select – Compress/Prune)

1. **Write (External Memory)**  
   - Ý tưởng: không giữ mọi thứ trong context; thay vào đó, ghi trạng thái quan trọng ra **bộ nhớ ngoài** (file, database, bộ nhớ phiên).  
   - Ví dụ thực tế:  
     - *Claude Code* ghi kế hoạch (plan) vào đĩa và sử dụng công cụ `TodoWrite` để lưu danh sách công việc.  
     - *Cursor* và *Windsurf* dùng *rules files*; *ChatGPT* lưu “memory” qua các phiên.  
   - Khi cần, agent đọc lại эти notes thay vì giữ chúng liên tục trong context,從而節省 token.

2. **Select (Just‑in‑Time Retrieval)**  
   - Không tải toàn bộ kho tài nguyên (codebase, documents) lên context từ đầu.  
   - Agent duy trì một **danh sách tham chiếu** (paths, query IDs) và chỉ tải nội dung khi thực sự cần.  
   - Thuật toán thường dùng trong *Claude Code*:  
     1. Cung cấp cho agent một **mô tả nén** của mỗi công cụ (ví dụ: “Dùng questool nếu người dùng hỏi về bài đăng LinkedIn”).  
     2. Khi agent dự đoán sẽ cần công cụ đó, nó **đọc lại mô tả đầy đủ** của công cụ (tool description) chỉ lúc đó.  
   - Điều này làm giảm đáng số lượng token phải phân tích mỗi lượt (ví dụ: thay vì phân tích 50 mô tả công cụ mỗi turn, chỉ phân tích 1‑2 cái thực sự liên quan).

3. **Compress and Prune**  
   - **Summarization** (tóm tắt): khi cửa sổ bắt đầu đầy, thay vì lỗi overflow, agent tóm tắt đoạn hội thoại trước – giữ lại các quyết策 kiến trúc, bỏ qua các chi khật khám phá.  
   - **Pruning** (cắt bớt): xóa các output công cụ không còn cần thiết.  
     - Ví dụ: kết quả `ls -la` từ 10 turns trước đã được dùng, nên có thể xóa an toàn.  
     - Một bản log 5.000 dòng có thể được nén thành “Tìm thấy 847 lỗi, 92% là Redis timeout …” rồi xóa bản log gốc.  
   - Nghiên cứu của Anthropic cho thấy việc chỉ **xóa stale tool outputs** có thể giảm token usage xuống **84%** trên các task chạy lâu.

### 3.3. Chiến lược isolates – Multi‑Agent Systems

Thay vì Kräfte một agent đơn phải xử lý hết mọi thông tin (gây ra cửa sổ to và nhiễu), chúng ta chia công việc ra cho **các agent phụ (sub‑agents)**, mỗi agent có **context window riêng** và chỉ xử lý một范围 hẹp (ví dụ: duyệt code, lên kế hoạch, tra cứu tài liệu).  

- **Orchestrator (agent chính)** gửi một prompt **rút gọn** cho sub‑agent (ví dụ: “Tìm tất cả API endpoint thay đổi dữ liệu người dùng”).  
- Sub‑agent thực hiện tìm kiếm trong codebase, sau đó trả về một **tóm tắt ngắn** (khoảng 500 token) cho orchestrator.  
- Orchestrator không thấy 30 file mà sub‑agent đã đọc; nó chỉ thấy kết quả đã được przetwar.  
- Mặc dù tổng số token tiêu thụ có thể tăng (do mỗi agent có自己的 window), nhưng chất lượng trả lời cao hơn vì mỗi agent làm việc trong một môi trường “sạch”.

## 4. Ví dụ minh họa

### Bài toán: AI agent giúp dev debug sản xuất qua logs

**Yêu cầu:**  
User hỏi: *“At 14:32 UTC, the checkout service started returning 503 errors. Why?”*  

**Quá trình mà không có context engineering (baseline):**  

1. User prompt (≈20 token)  
2. Agent quyết định gọi công cụ **FetchLogs** → trả về 200 000 token logs thô.  
3. Agent versucht suy luận direttamente trên toàn bộ logs → context window nhanh vượt quá giới hạn → mô hình bắt đầu hallucinate hoặc dừng lại.  

**Áp dụng 4 chiến lược:**  

| Bước | Chiến lược | Hành động chi tiết | Lượng token tiết kiệm/giải thích |
|------|------------|---------------------|-----------------------------------|
| 1 | **Write** | Agent ghi **hypothesis ban đầu** (“Có thể do Redis overload”) vào file `debug_hypothesis.txt` và lưu task state trong `todo.json`. | Không cần giữ hypothesis trong context mỗi lượt. |
| 2 | **Select** | Thay vì đọc toàn bộ file log, agent dùng `Glob '**/*.log'` để tìm file log liên quan, rồi `Grep 'checkout service'` để lấy dòng chỉ chứa service đó, cuối cùng `Read` từng đoạn ngắn (ví dụ: 2000 token) chỉ khi cần. | Chỉ load phần log thực sự liên quan (khoảng 5‑10 % tổng size). |
| 3 | **Compress & Prune** | Sau mỗi lần đọc một chunk log, agent tóm tắt thành “Found 847 errors, 92% Redis timeout: org.redis.client.RedisTimeoutException …” và xóa chunk gốc. Khi danh sách hipótesis thay đổi, agent cập nhật `todo.json` và xóa các hipótesis cũ. | Mỗi chunk sau khi nén chỉ còn ~50 token thay vì 2000 token; tổng token giảm >90 %. |
| 4 | **Isolate** | Agent chính orchestrator spawns hai sub‑agents: <br> - **LogExplorer** chịu trách nhiệm tìm và tóm tắt lỗi từ logs (sử dụng Select + Compress). <br> - **DocLookup** tra cứu trong tài liệu nội bộ về “Redis memory limit” và trả về cách khắc phục. <br> Mỗi sub‑agent trả về một bản tóm tắt ~400 token cho orchestrator. | Orchestrator chỉ cần xử lý tổng cộng ~800 token (hai tóm tắt) thay vì 200 000 token logs raw. |

**Kết quả:**  
- Orchestrator nhận được兩個 concise answer:  
  1. “Logs show 847 errors, 92% Redis timeout at 14:32‑14:47 UTC.”  
  2. “Doc says: increase Redis maxmemory or enable eviction policy; restart after config change.”  
- Từ những thông tin này, agent sinh ra câu trả lời cuối cùng:  
  > “Lỗi 503 do Redis hết bộ nhớ, gây timeout. Đã khắc phục bằng cách tăng limit bật chính sách eviction và restart service lúc 14:47 UTC.”  

Trong suốt quá trình, **context window** của agent chính luôn duy trì dưới 2 k token (prompt + hai tóm tắt + quelques notes), tránh được hiện tượng context rot và cho phản hồi chính xác, kịp thời.

## 5. Tổng kết

- **Context window** là bộ nhớ làm việc của LLM; nó có hạn và dễ bị phénomène **context rot** ngay trước khi đạt giới hạn.  
- Các biểu hiện xấu của context (poisoning, distraction, confusion, clash) khiến agent suy giảm chất lượng sau một số lượt trao đổi.  
- **Ba chiến lược cơ bản** để quản lý context:  
  1. **Write** – lưu trạng thái, kế hoạch, kết quả trung gian ra bộ nhớ ngoài (file, DB, memory).  
  2. **Select** – tải dữ liệu / tài liệu chỉ khi cần, giữ tham chiếu thay vì nội dung đầy đủ.  
  3. **Compress & Prune** – tóm tắt hội thoại và xóa output công cụ cũ khi không còn cần thiết.  
- Khi tác vụ phức tạp, **isolate** qua **multi‑agent systems** cho phép mỗi agent làm việc trong một “cửa sổ sạch”, orchestrator chỉ tổng hợp kết quả ngắn gọn.  
- Kết hợp các chiến lược này giúp **curb token usage**, **tránh hallucination**, và **trả lời chính xác** trong các luồng對話 dài – yêu cầu then chốt của bất kỳ AI Engineer nào muốn xây dựng agent ổn định, khả năng sản xuất cao.

> **Lưu ý thực tiễn:** bắt đầu bằng cách thêm một công cụ `write_to_file` và `read_from_file` vào agent của bạn, sau đó áp dụng Select (Glob/Grep/Read) để lấy dữ liệu chỉ khi cần. Khi cửa sổ bắt đầu đầy, bật tính năng tóm tắt tự động hoặc viết hàm prune riêng. Cuối cùng, 실험 với mô hình orchestrator‑sub‑agent để thấy sự cải thiện về chất lượng và chi phí token.