# Kỹ thuật ngữ cảnh (Context Engineering) cho AI Agent

## 1. Mục tiêu học tập

Sau bài học này, người học sẽ có thể:

- Giải thích tại sao việc quản lý **context window** là yếu tốthen chốt để AI agent hoạt động ổn định, tiết kiệm và chính xác trong môi trường thực tế.  
- Phân loại các thành phần xuất hiện trong context window và phân biệt **static context** (ngữ cảnh tĩnh) với **dynamic context** (ngữ cảnh động).  
- Áp dụng các kỹ thuật quản lý lịch sử trò chuyện (history), quyết định khi nào và cách truy xuất kiến thức (retrieval) để tối ưu uży dụng token.  
- Đánh giá và giám sát chất lượng ngữ cảnh trong sản xuất bằng phương pháp **probe‑based evaluation** và các chỉ số cụ thể (utilization rate, compression ratio, retrieval precision, context drift).  

## 2. Tổng quan

Khi AI agent “sập” trong production, nguyên nhân thường không nằm ở mô hình mà ở cách **context window** (cửa sổ ngữ cảnh) được sử dụng. Các token bị lãng phí bởi lịch sử lỗi thời, kết quả truy xuất trùng lặp hoặc đầu thô của công cụ làm mờ tín hiệu thực sự mà mô hình cần.  

**Context engineering** là quy trình ra quyết định có gì vào context window, gì được nén, gì được truy xuất khi cần và gì được loại bỏ hoàn toàn. Khi thực hiện tốt, mỗi token mang giá trị tín hiệu cao, chi phí المالي và lỗi nhận thức được giảm thiểu.

Bài học sẽ đi qua các thực hành cốt lõi:

1. Xem context window như tài nguyên hữu hạn (giống RAM).  
2. Ánh xạ và phân tách các lớp ngữ cảnh (system instructions, history, retrieved knowledge, working state).  
3. Quản lý lịch sử trò chuyện để tránh bloat và poisoning.  
4. Xây dựng truy xuất như một quyết định ngân sách token.  
5. Phân bổ token qua toàn bộ vòng lặp agent.  
6. Đánh giá chất lượng ngữ cảnh trong production bằng probe‑based test và các metrics cụ thể.  

## 3. Kiến thức cốt lõi

### 3.1 Context window là tài nguyên hữu hạn  

- **Chi phí tài chính**: Mô hình tính phí theo triệu token đầu vào; trong vòng lặp đa bước, chi phí tăng nhanh.  
- **Chi phí nhận thức**: Mô hình không xét tất cả token bình đ Aussage. Tokens ở đầu và cuối context otrzymują nhiều’attention hơn, medan các token ở giữa thường ít ảnh hưởng → đầu vào quá dài hoặc không cấu trúc tốt có thể suy giảm khả năng luận lý dù vẫn dưới ngưỡng token.  
- **Mô hình mental**: Context window ≈ RAM (nhanh, mạnh nhưng hữu hạn, được xóa giữa các phiên). Bộ nhớ ngoài (database, file system) là “đisk”: rẻ, lớn nhưng cần truy xuất cụ thể để sử dụng.  

### 3.2 Thành phần thường lấp đầy context window  

| Lớp | Mô tả | Tính chất |
|-----|-------|-----------|
| **System instructions** | Vai trò, quy tắc hành vi, mô tả công cụ, định dạng output, few‑shot examples. | Thường **static**, tốt để prefix‑caching. |
| **Conversation history** | Bản ghi lượt user, phản hồi agent, gọi công cụ và kết quả công cụ. | Lớp tăng nhanh nhất, thường **quản lý không tốt**. |
| **Retrieved knowledge** | Tài liệu, bản ghi DB, mục memory lấy từ kho ngoài. | Có thể dư thừa; mỗi chunk tiêu thụ ngân sách token. |
| **Working state** | Kết quả trung gian, scratchpad reasoning, tiến độ task. | Cần cho tính nhất quán đa bước, nhưng tốn nếu lưu trữ dưới dạng lời giải thích dài. |

Mục tiêu của việc audit là hiểu sự trade‑off giữa các lớp, không phải giảm mỗi lớp xuống thấp nhất. Lỗi thường xuất phát từ: (1) **include irrelevant content** (nhập nội dung không liên quan) hoặc (2) **exclude needed content** (loại bỏ nội dung cần thiết) – đều là quyết định kiến trúc, không phải do mô hình.

### 3.3 Phân tách Static vs Dynamic Context  

- **Static context** (ngữ cảnh tĩnh): system instructions, agent identity, tool schemas, quy tắc cố định → đặt ở đầu prompt để tận dụng **prefix caching** (prefix được tái sử dụng thay vì tính lại mỗi lần).  
- **Dynamic context** (ngữ cảnh động): đầu vào người dùng hiện tại, kết quả công cụ mới nhất, tài liệu được truy xuất cho bước reasoning hiện tại → nên được giữ **minimal**, chỉ chứa những gì cần cho bước tiếp theo.  

**Triển khai thực tiễn** – hai‑pass context assembly:

1. **Pass 1 (static)**: nạp system prompt, các instruction đã được cache, bản tóm tắt dài hạn.  
2. **Pass 2 (dynamic)**: tiêm task state hiện tại, kết quả truy xuất mới, lịch sử gần đây.  

Lợi ích: debug dễ dàng hơn – nếu lỗi xuất hiện, nguyên nhân hoặc nằm ở static (vấn đề prompt engineering) hoặc dynamic (vấn đề retrieval / history management).

### 3.4 Quản lý Lịch sử Trò chuyện (Conversation History)  

- **Cách tiếp cận naïve**: append mỗi lượt mới và gửi lại toàn bộ history → hoạt động tốt với phiên ngắn, nhưng với agent chạy lâu gây **context bloat** (lịch sử cũ, kết quả tool đã giải quyết, quyết định cũ) và **context poisoning** (sai lầm trước được giữ lại và được xem như sự thật, dẫn tới lỗi lan truyền).  

- **Các giải pháp**:
  - **Recency truncation**: giữ chỉ N lượt gần nhất → rẻ nhưng mất thông tin dài hạn.  
  - **Rolling summarization**: định kỳ nén các cuộc trao đổi cũ thành bản tóm tắt ngắn ghi lại quyết định, попытка, trạng thái hiện tại.  
  - **Anchored iterative summarization** (cạnh tấn): duy trì một **session‑state document có cấu trúc** (intent, decisions, actions, next steps) được cập nhật liên tục → giữ ý nghĩa mà tránh tràn context.  

### 3.5 Thiết kế Truy xuất như Quyết định Ngân sách  

- Truy xuất cho phép agent truy cập kiến thức vượt quá kích thước context window. Tuy nhiên, nếu xem truy xuất như bước “upstream” đơn giản (lấy chunks → inject → tiếp tục) mà không hỏi: *“Bao nhiều ngân sách token nên dành cho truy xuất?”* và *“Khi nào việc truy xuất thực sự có giá trị?”* thì chi phí sẽ tăng không contrôle.  

- **Chi phí thường bị低估**: trong workflow đa truy xuất, chi phí token-stack nhanh.  
- **Post‑retrieval filtering** (lọc sau truy xuất): punte chỉ giữ các chunk có related‑score cao trước khi inject → tối ưu cao.  

- **Cấu trúc chunk** quan trọng như lựa chọn:
  - **Semantic chunking**: chia tài liệu theo ranh giới chủ đề tự nhiên → giữ ngữ nghĩa và mạch lạc tốt hơn so với chunk cố độ dài.  
  - **Hybrid retrieval**: kết hợp tìm kiếm semantic với bộ lọc từ khóa hoặc metadata → xử lý trường hợp mà embeddings đơn thuần bỏ qua (ví dụ: “billing issues trong 30 ngày terakhir” cần cả semantic relevance và ràng buộc thời gian).  

- **Kích hoạt truy xuất**:
  - **Automatic retrieval**: chạy trước mỗi lượt agent → đơn giản nhưng có thể inject token vô ích.  
  - **Agent‑controlled retrieval**: agent quyết định khi gọi truy xuất như một công cụ → truy xuất có mục tiêu, bắn đúng thời điểm trong chain reasoning, nhưng yêu cầu model phải nhận ra khi cần truy xuất.  
  - Đối với hầu hết hệ thống production ổn định, **agent‑controlled retrieval** là lựa chọn mặc định tốt hơn.  

### 3.6 Phân bổ Token qua Toàn Bộ Vòng Lặp Agent  

- Quyết định về context ở từng bước chỉ giải quyết một phần vấn đề. Trong **multi‑step agent loop**, token tích lũy qua các vòng → cần xem toàn bộ run như đơn vị chi phí.  
- Nguyên nhân tiêu thụ token lớn nhất: system prompts và **tool outputs** (đặc biệt là kết quả search/API).  
- **Giải pháp efficace**: lọc và cắt bớt tool output ngay khi ingest (input‑side) thay vì tentativa nén sau; chỉ giữ phần thực sự cần cho bước kế tiếp.  
- Mục tiêu thực tiễn: duy trì **context utilization rate** khoảng **60‑80 %** (không tối đa hoá 100 %) để có dư phòng và giảm nguy cơ overflow.  
- **Dynamic allocation**: nhiệm vụ đơn → cấp context minimal; nhiệm vụ phức tạp đa b cấp → cấp context cao hơn, cân bằng giữa chi phí và khả năng.  

### 3.7 Đánh Giá và Giám sát Chất lượng Ngữ cảnh trong Production  

- Thất bại context engineering thường **ẩn** trong các đánh giá ngắn; agent có thể hoạt động tốt trong các phiên test ngắn nhưng giảm chất lượng khi chạy dài, và lỗi thường bị chênh lệch vào “sự lý do” thay vì “quản lý context”.  

- **Probe‑based evaluation**: sau mỗi bước nén hoặc truy xuất, đặt **câu hỏi định hướng** (probe) đòi hỏi thông tin cụ thể đã được lưu.  
  - **Recall probe**: agent có thể nhớ lại事実 cụ thể?  
  - **Artifact probe**: agent biết mình đã thay đổi file nào?  
  - **Continuation probe**: agent có thể tiếp tục một tác vụ đa bước từ nơi đã dừng?  
  Trả lời đúng → ngữ cảnh liên quan đã được bảo tồn; trả lời sai → rivel vấn đề trong nén hoặc truy xuất.  

- **Metrics cụ thể**值得跟踪：
  - **Context utilization rate** = (tokens đã dùng) / (tổng budget token) × 100 %  
  - **Compression ratio** = tokens trước nén / tokens sau nén  
  - **Retrieval precision** = (số chunk đã được model sử dụng thực sự) / (tổng số chunk đã inject)  
  - **Context drift** (language drift): signes như agent đọc lại file đã xử lý, khai báo lại quyết định cũ, hoặc dần lệch khỏi mục tiêu ban đầu. Các biểu hiện này xuất hiện trong **step‑level traces** trước khi làm giảm chất lượng output.  

- **Quy trình tối ưu hoá**:
  1. Xây dựng baseline metrics từ các phiên thực tế.  
  2. Xác đoán các đoạn có chi phí cao hoặc chất lượng thấp.  
  3. Áp dụng các bản sửa hướnged (ví dụ: tăng cường filter, thay đổi chiến lược summarization).  
  4. Đo lường lại影响.  

  Lưu ý: **over‑compression** có thể tiết kiệm token nhưng làm giảm accuracy – mục tiêu là tìm **minimum viable context** đủ để agent hoàn thành nhiệm vụ đúng mà không thừa.  

## 4. Ví dụ minh họa

Giả sử chúng ta xây dựng một AI agent hỗ trợ khách hàng cho một ngân hàng online. Agent cần:

1. Hiểu yêu cầu của người dùng (ví dụ: “Tôi muốn xem giao dịch thẻ crédito trong 30 ngày qua”).  
2. Truy xuất lịch sử giao dịch từ cơ sở dữ liệu.  
3. Tổng hợp kết quả và trả lời dưới dạng bảng ngắn gọn.

### 4.1 Xây dựng context window

| Lớp | Nội dung (ví dụ) | static / dynamic |
|-----|------------------|------------------|
| System instructions | “Bạn là trợ lý ngân hàng. Trả lời ngắn gọn, sử dụng bảng nếu cần.” | static |
| Tool schema | Mô tả API `get_transactions(start_date, end_date)` | static |
| Conversation history (last 2 turns) | User: “Xin chào”. Agent: “Chào bạn! Bạn cần hỗ trợ gì?” | dynamic |
| Retrieved knowledge | 15 bản ghi giao dịch (mỗi bản ~120 token) – sau lọc giữ 5 bản ghi liên quan nhất | dynamic |
| Working state | Bảng tóm tắt: “5 giao dịch, tổng cộng 12 triệu VND” | dynamic |

- **Pass 1 (static)**: nạp system instructions + tool schema (prefix‑cached).  
- **Pass 2 (dynamic)**: tiêm 2 lượt history gần nhất + 5 bản ghi giao dịch đã lọc + working state.  

Tổng token ước lượng: ~800 token (dưới 60‑80 % của một context window 2000 token), cho phép agent còn dư để thực hiện suy luận.

### 4.2 Quản lý lịch sử

Nếu cuộc hội thoại kéo dài 50 lượt, thay vì gửi toàn bộ 50 lượt, chúng ta áp dụng **anchored iterative summarization**:

- Mỗi 10 lượt, tạo một bản tóm tắt có cấu trúc:  
  ```json
  {
    "intent": "xem giao dịch thẻ",
    "decisions": ["lọc thời gian 30 ngày", "sử dụng API get_transactions"],
    "actions": ["gọi API", "lọc kết quả"],
    "next_steps": ["hiển thị bảng"]
  }
  ```
- Bản tóm tắt này (khoảng 80 token) thay thế cho 10 lượt history thô (khoảng 800 token) trong context window, giảm bướn và tránh nguy cơ “context poisoning” khi một lượt history cũ chứa thông tin sai.

### 4.3 Truy xuất như quyết định ngân sách

Thay vì tự động lấy toàn bộ 1000 bản ghi mỗi lượt, agent sẽ:

1. Phân tích意图 → nhận thấy cần *time range* và *card type*.  
2. Gọi công cụ `get_transactions` với tham số `start_date = today-30d`, `end_date = today`, `card_type = "credit"`.  
3. Sau khi nhận về 150 bản ghi, thực hiện **post‑retrieval filtering** bằng điểm số relevance (TF‑IDF hoặc embedding similarity) và giữ top‑5.  

Việc này chỉ tiêu tốn khoảng 600 token cho dữ liệu truy xuất (5 × 120) thay vì 18 000 token nếu lấy tất cả.

### 4.4 Đánh giá chất lượng

Sau mỗi lần truy xuất, chúng ta đặt **probe**:

- **Recall probe**: “Giao dịch cuối cùng trong khoảng thời gian này có giá trị bao nhiêu?” – agent phải trả lời số chính xác từ một trong 5 bản ghi đã giữ.  
- **Artifact probe**: “Bạn đã thay đổi file nào trong phiên này?” – agent trả lời “không” (vì chỉ đọc).  
- **Continuation probe**: Nếu người dùng hỏi tiếp “Cho tôi xem tổng chi tiêu theo danh mục”, agent phải tiếp tục từ trạng thái working state (bảng tóm tắt) mà không cần truy xuất lại toàn bộ lịch sử.  

Nếu probe trả lời sai, chúng ta biết rằng lỗi nằm ở bước nén hoặc lọc truy xuất và có thể điều chỉnh ngưỡng relevance hoặc tăng số lượng bản ghi giữ lại.

## 5. Tổng kết

- **Context engineering** là việc thiết kế có系統 thống kê nội dung, nén, truy xuất và ngân sách token để AI agent hoạt động tin cậy, tiết kiệm và chính xác trong môi trường thực tế.  
- Xem **context window** như **RAM**: tài nguyên hữu hạn có cả chi phí tài chính và nhận thức; chỉ giữ những mang giá trị tín hiệu cao.  
- Phân tách **static context** (cache‑able) và **dynamic context** (task‑dependent) giúp tối ưu prefix caching và đơn giản hoá debug.  
- Quản lý **lịch sử trò chuyện** bằng các phương pháp truncation, rolling summarization hoặc anchored iterative summarization để tránh bloat và lan truyền sai lầm.  
- Xây dựng **truy xuất** như một quyết định ngân sách: sử dụng post‑retrieval filtering, semantic/hybrid chunking và privilégié agent‑controlled retrieval khi hệ thống ổn định.  
- Phân bổ **token** qua toàn bộ vòng lặp agent: tập trung vào cắt bớt tool output ngay khi ingest, duy trì mức sử dụng 60‑80 % và cấp allocation linh hoạt dựa trên độ phức tạp của nhiệm vụ.  
- Đánh giá chất lượng ngữ cảnh trong sản xuất bằng **probe‑based test** (recall, artifact, continuation) và theo dõi các chỉ số: context utilization rate, compression ratio, retrieval precision, và context drift.  

Áp dụng thực nghiệm những nguyên tắc trên sẽ giúp bạn xây dựng AI agent không chỉ “hoạt động” trong môi trường thử nghiệm mà còn “bền bỉ” và “kéo dài” khi đối mặt với công việc thực tế, chi phí hợp lý và chất lượng cao.