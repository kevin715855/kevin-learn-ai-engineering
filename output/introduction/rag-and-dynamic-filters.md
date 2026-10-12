# 4 Kỹ Thuật Quản Lý Context Mỗi AI Engineer Cần Biết  

## 1. Mục tiêu học tập  

Sau khi đọc bài học này, người học sẽ có thể:  

- Giải thích tại sao **context window** của mô hình LLM tương đương với RAM của CPU và tại sao kích thước lớn không luôn mang lại hiệu suất tốt.  
- Nhận biết bốn hiện tượng gây hại cho context: **Context Poisoning, Context Distraction, Context Confusion, Context Clash**.  
- Áp dụng bốn chiến lược quản lý context chính: **Write (External Memory), Select (Just‑in‑Time Retrieval), Compress and Prune, Isolate (Multi‑Agent)**.  
- Minh họa cách kết hợp các chiến lược trên để xây dựng AI agent ổn định trong các tác vụ dài hạn (ví dụ: agent debug log).  

## 2. Tổng quan  

Khi tương tác với một LLM, mọi thứ mà model “nhìn thấy” – prompt, lịch sử trò chuyện, kết quả gọi công cụ, tài liệu được đưa vào – đều nằm trong **context window**. Đây là bộ nhớ làm việc của model, tương tự như RAM của CPU. Tuy nhiên, context window có giới hạn token và ngay cả khi chưa vượt quá giới hạn, chất lượng suy luận có thể giảm dần do hiện tượng **context rot** (hiệu suất giảm khi có quá nhiều token, dù vẫn trong cửa sổ).  

Trong việc xây dựng AI agent dài hạn (ví dụ: agent thu thập và phân tích log để chẩn đoán sự interrom production), context window dễ bị lấp đầy bởi dữ liệu “rác”, dẫn tới các hiện tượng sai lệch như huyền tưởng, mất tập trung hoặc mâu thuẫn. Do đó, **context engineering** – nghệ thuật chọn lọc, nén và quản lý thông tin mà model thực sự cần xem – trở thành yếu tố then chốt để agent hoạt động ổn định và chính xác.  

Bài viết này tóm tắt bốn chiến lược được Owain Lewis mô tả trong bài báo “4 context engineering strategies every AI engineer needs to know”, với minh họa thực tế từ Claude Code (terminal AI agent) và từ trường hợp agent debug log của tác giả.  

## 3. Kiến thức cốt lõi  

### 3.1. Context window và tính stateless của LLM  

- Mỗi lần gọi API, chúng ta phải truyền **toàn bộ** lịch cuộc trò chuyện (prompt + câu trả lời trước đó + kết quả công cụ…) vào model.  
- Model không có bộ nhớ nội tại giữa các lượt gọi;一切 thông tin cần để sinh ra câu trả lời tiếp theo phải nằm trong context window của lượt gọi hiện tại.  

### 3.2. Ba hiện tượng tiêu cực khi context quá tải  

| Hiện tượng | Mô tả | Tác động |
|------------|-------|----------|
| **Context Poisoning** | Một chuỗi suy luận sai (huyền tưởng) masuk vào context và làm thay đổi mọi suy luận sau đó. | Dẫn tới kết quả sai lầm liên tục. |
| **Context Distraction** | Quá nhiều token không liên quan làm model mất tập trung vào thông tin cần thiết. | Giảm độ chính xác, tăng latency. |
| **Context Confusion** | Thông tin không liên quan nhưng vẫn có thể ảnh hưởng đến quyết định của model. | Model “lẫn lộn” giữa tín hiệu hữu ích và noise. |
| **Context Clash** | Hai phần trong context mâu thuẫn (ví dụ: hai đoạn log mô tả trạng thái khác nhau). | Model không thể xác định哪一份是 правильн٫, dẫn tới suy luận mâu thuẫn hoặc không chắc chắn. |

Nếu agent hoạt động tốt ở lượt đầu nhưng bắt đầu drift (suyGradually degrade) sau một số lượt, một trong四 현 tượng trên thường là nguyên nhân.  

### 3.3. Nguyên tắc “context is RAM”  

- **CPU** = LLM (thực hiện tính toán).  
- **RAM** = context window (bộ nhớ làm việc).  
- Để giảm tải RAM, chúng ta phải **lưu trữ** thông tin bên ngoài (disk, database), **tải** chỉ khi cần, **nén** hoặc **xóa** thông tin cũ, và **phân chia** công việc giữa nhiều agent (mỗi agent có riêng context window riêng).  

## 4. Ví dụ minh họa  

### 4.1. Tình huống ban đầu: Agent debug log  

- Yêu cầu: “Search the logs and tell me why this alert fired.”  
- Agent thu thập log từ nhiều nguồn → context window nhanh chóng đầy (nhiều hàng nghìn token).  
- Sau vài lượt trao đổi, agent bắt đầu hallucinate hoặc trả lời không chính xác do context rot và các hiện tượng trên.  

### 4.2. Áp dụng bốn chiến lược  

#### 1️⃣ Write – Lưu trạng thái bên ngoài  

- Agent sử dụng công cụ **TodoWrite** để ghi từng bướcdebug (ví dụ: “fixed auth.ts, need to check db.ts, then run tests”) vào tệp tin cấu trúc trên disk.  
- Khi cần xem tiến độ, agent đọc file todo thay vì giữ toàn bộ danh sách trong context.  
- **Lợi ích:** Giảm số token cần lưu trong context; thông tin vẫn có thể truy xuất khi cần.  

#### 2️⃣ Select – Truy vấn dữ liệu chỉ khi cần  

- Thay vì nạp toàn bộ source code vào context, agent dùng:  
  - `Glob('**/*.ts')` để lấy danh sách file TypeScript có thể liên quan.  
  - `Grep('auth')` trên danh sách đó để xác định file chứa mã xác thực.  
  - `Read('src/auth.ts')` chỉ đọc nội dung file cụ thể.  
- Khi agent cần biết về một công cụ, nó сначала đọc mô tả ngắn gọn (compressed summary); nếu quyết định sử dụng, mới tải toàn bộ định nghĩa công cụ.  
- **Lợi ích:** Context chỉ chứa những đoạn code/Logs thực sự liên quan; tránh việc dump 50 file ngay từ đầu.  

#### 3️⃣ Compress and Prune – Tóm tắt và xóa thông tin cũ  

- **Summarization:** Khi context window gần đầy, Claude Code tạo tóm tắt cuộc trò chuyện (giữ quyết策 kiến trúc, bỏ qua các bước khám pháThử). Tóm tắt có kích thước khoảng vài chục token thay vì hàng trăm nghìn token ban đầu.  
- **Pruning (context editing):** Các输出 của công cụ không còn cần (ví dụ: kết quả `ls -la` từ 10 turns trước) được xóa outright. Các log thô được nén thành một câu như:  
  ```
  Found 847 errors, 92% were Redis timeouts: org.redis.client.RedisTimeoutException: Redis server response timeout (3000 ms) occured for command: (GET)
  ```  
  sau đó xóa bản log gốc.  
- **Lợi ích:** Giảm token sử dụng xuống tới 84% trên các tác vụ chạy lâu, đồng thời giữ lại thông tin then chốt.  

#### 4️⃣ Isolate – Đóng góiงาน vào sub‑agent  

- Claude Code tạo các agent chuyên biệt:  
  - **Explore** – duyệt mã nguồn, tìm file.  
  - **Plan** – quyết định kiến trúc, chuỗi bước.  
  - **claude-code-guide** – tra cứu tài liệu.  
- Khi người dùng hỏi: “how does billing work?” và “what’s in the docs about webhooks?”, hai sub‑agent chạy **song song**, mỗi agent có context window riêng và chỉ trả về một tóm tắt ngắn gọn cho agent chính.  
- Prompt delegated tới sub‑agent được nén (ví dụ: “Find all API endpoints that modify user data”) thay vì chuyển toàn bộ lịch sử trò chuyện.  
- **Lợi ích:** Mỗi sub‑agent làm việc trong một không gian sạch, ít noise; tổng token tiêu thụ có thể lớn hơn nhưng chất lượng trả lời tốt hơn vì mỗi agent chỉ tập trung vào một hẹp范围.  

### 4.3. Kết quả sau khi áp dụng  

- Agent không còn “đột ngột”失焦 sau vài vòng đối話.  
- Thông tin quan trọng (mấu cơ của sự cố, quyết định kiến trúc) vẫn保存在 context dưới dạng tóm tắt hoặc file bên ngoài.  
- Dùng kèm một hoặc nhiều chiến lược (ví dụ: Write + Select + Compress) cho thấy sự cải thiện rõ rệt so với phương pháp “dump tất cả vào context”.  

## 5. Tổng kết  

- Context window của LLM là tài nguyên hữu hạn; **bigger ≠ better** nếu đầy nhiễu.  
- Quatre hiện tượng xấu (Poisoning, Distraction, Confusion, Clash) là nguồn gốc của drift và hallucination trong agent dài hạn.  
- Bốn chiến lược quản lý context hiệu quả:  
  1. **Write** – lưu trạng thái, kế hoạch, ghi chú vào file hoặc database bên ngoài.  
  2. **Select** – tải dữ liệu, mô tả công cụ chỉ khi cần (just‑in‑time retrieval).  
  3. **Compress and Prune** – tóm tắt lịch sử và xóa outputs cũ mà không còn giá trị.  
  4. **Isolate** – chia công việc thành nhiều sub‑agent, mỗi agent có context riêng.  
- Khi xây dựng AI agent, hãy xem context như một kho chứa tài nguyên cần được **lọc, nén và sắp xếp** thay vì Versuch lưu trữ mọi thứ. Áp dụng đúng các chiến lược trên sẽ giúp agent duy trì sự ổn định, chính xác và khả năng mở rộng trong các tác vụ thực tế dài hạn.