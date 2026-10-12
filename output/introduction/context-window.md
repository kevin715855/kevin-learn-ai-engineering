# Bài học: Context Window trong mô hình ngôn ngữ lớn (LLM)

## 1. Mục tiêu học tập
Sau khi đọc bài học này, bạn sẽ có thể:
- Giải thích khái niệm **context window** (context length) của LLM và tại sao nó quan trọng.
- Mô tả cách token hoạt động và mối quan hệ giữa token, từ và ký tự.
- Liệt kê các lý do khiến mô hình có giới hạn độ dài context tối đa.
- Nhận ra thách thức khi mở rộng context window (tài nguyên tính toán, hiệu suất, an ninh).
- So sánh kích thước context window của một số mô hình LLM nổi bật hiện nay (GPT, Llama, Mistral, Gemini, Claude).

## 2. Tổng quan
Trong các mô hình ngôn ngữ lớn, **context window** xác định lượng văn bản (được đo bằng token) mà mô hình có thể “nhớ” và xử lý đồng thời tại một thời điểm. Nó tương đương với bộ nhớ làm việc của mô hình và ảnh hưởng trực tiếp đến khả năng xử lý cuộc trò chuyện dài, tài liệu hoặc mã nguồn. Khi đầu vào vượt quá kích thước context window, cần cắt bớt (truncate) hoặc tóm tắt để mô hình tiếp tục hoạt động.

## 3. Kiến thức cốt lõi

### 3.1. Định nghĩa và vai trò
- Context window (hoặc context length) = số token tối đa mà LLM có thể xem xét trong một lần suy luận.
- Càng lớn context window, mô hình có thể đưa vào đầu vào nhiều thông tin hơn → thường dẫn đến độ 정확 cao hơn, ít hallucination hơn, trả lời mạch lạc hơn và cho phép trò chuyện dài.
- Tuy nhiên, việc tăng kích thước này không miễn phí: yêu cầu tính toán tăng mạnh và có thể mở rộng bề mặt tấn công (attack surface).

### 3.2. Tokenization – đơn vị thực tế của context
- LLM không làm việc với từ hoặc ký tự đơn lẻ mà làm việc với **token**.
- Một token có thể là:
  - Một ký tự đơn (ví dụ: “a” trong “cat” khi không mang ý nghĩa riêng).
  - Một phần của từ (tiền tố, hậu tố).
  - Một từ hoàn chỉnh.
  - Một cụm từ ngắn (hai‑ba từ).
- Do không có tỷ lệ từ‑token cố định, thường ước lượng **~1,5 token/từ** cho mục đíchทั่วไป.
- Công cụ trực quan hóa như **Tokenizer Playground** trên Hugging Face giúp thấy cách các mô hình khác nhau chia thành token.

### 3.3. Tại sao mô hình có giới hạn context length tối đa?
- Hầu hết LLM hiện nay dựa trên kiến trúc **Transformer** với cơ chế **self‑attention**.
- Self‑attention tính toán mối quan hệ giữa mọi cặp token trong chuỗi → độ phức tạp tính toán tăng **bậc hai** theo độ dài chuỗi (O(n²)).
- Khi độ dài context tăng:
  - Yêu cầu tính toán (và chi phí) tăng gấp bốn lần khi số token gấp đôi.
  - Thời gian suy luận chậm dần vì mỗi bước tạo token mới phải xem xét lại tất cả token trước đó.
  - Trong chatbot, ngoài đầu vào người dùng còn có **system prompt**, dữ liệu từ **RAG**, và các ký tự định dạng cũng chiếm phần context.
- Đối với các mô hình khác (diffusion models dùng cho sinh ảnh), context length áp dụng cho số pixel mà self‑attention phải xử lý.

### 3.4. Thách thức khi mở rộng context window

#### 3.4.1. Thách thức về hiệu suất
- Nghiên cứu năm 2023 (“Lost in the Middle”) chỉ ra rằng LLM thường **không sử dụng mạnh mẽ** thông tin ở giữa đoạn dài; hiệu suất tốt nhất khi thông tin liên quan nằm ở đầu hoặc cuối context.
- Các kỹ thuật như **Rotary Position Embedding (RoPE)** giúp cải thiện khả năng atención trên khoảng cách lớn, nhưng vấn đề “lost in the middle” vẫn còn.
- Các benchmark (NIAH, RULER, LongBench) được thiết kế để đo khả năng tìm và sử dụng thông tin trong đoạn dài.

#### 3.4.2. Thách thức về an ninh và cybersecurity
- Context window mở rộng cũng mở rộng **attack surface** – powierzchon tấn công.
- Nghiên cứu của Anthropic (2024) cho thấy độ dài context lớn hơn làm tăng khả năng “jailbreaking” (tiếp cận hạn chế) và dẫn đến phản hồi có hại.
- Vì vậy, việc tăng context length phải đi kèm với các biện pháp giảm thiểu rủi ro (lọc prompt, giám sát output, v.v.).

### 3.5. Kích thước context window của một số mô hình LLM nổi bật (tháng 10/2024)

| Hãng / série | Mô hình | Context window (tokens) | Ghi chú |
|--------------|---------|------------------------|---------|
| **OpenAI – GPT** | GPT‑3.5 (ban đầu) | 4 096 | sau đó mở rộng lên 8 192 (GPT‑3.5‑Turbo) |
| | GPT‑4 / GPT‑4‑Turbo | 128 000 | output tối đa 4 096 token |
| | GPT‑4o / GPT‑4o‑mini | 128 000 | output tối đa 16 384 token |
| | O‑1 series | 128 000 | output context length lớn hơn |
| **Meta – Llama** | Llama (origin) | 2 048 | |
| | Llama 2 | 4 096 | |
| | Llama 3 (initial) | ~8 000 | |
| | Llama 3.1 | 128 000 | |
| | Llama 3.2 | 128 000 | |
| **Mistral AI** | Mistral Large 2 | 128 000 | flagship model |
| **Google – Gemini** | Gemini 1.5 Pro | ≤ 2 000 000 | lớn nhất trong các mô hình thương mại |
| | Gemini 1.5 Flash | 1 000 000 | |
| **Anthropic – Claude** | Claude 3.5 Sonnet | ~200 000 | |
| | Claude Enterprise (tháng 9/2024) | 500 000 | mở rộng qua gói doanh nghiệp |

> **Lưu ý:** Các con số trên có thể thay đổi khi các nhà phát hành phát hành bản bản mới; hãy luôn tham khảo tài liệu chính xác nhất từ nhà cung cấp.

## 4. Ví dụ minh họa

### Ví dụ 1: Cách token chia từ
Giả sử câu tiếng Anh:  

```
Jeff drove a car.
```

- Khi sử dụng bộ tokenizer phổ biến (ví dụ: GPT‑2 BPE), mỗi từ thường trở thành một token riêng:  
  `["Jeff", "drove", "a", "car", "."]` → **5 tokens**.  
  Tuy nhiên, nếu dùng tokenizer khác, dấu chấm có thể được gộp vào từ trước hoặc được bỏ qua, làm thay đổi số token.

### Ví dụ 2: Ảnh hưởng của context window tới chatbot
Giả sử một chatbot có context window = 4096 token.  
- Mỗi lượt trao đổi (câu hỏi + câu trả lời) tiêu thụ khoảng 150 token (kèm system prompt, định dạng).  
- Với 4096 token, bot có thể duy trì khoảng **27 lượt trao đổi** trước khi bắt buộc phải cắt bớt hoặc tóm tắt lịch sử trò chuyện.  
- Nếu tăng context window lên 32768 token, cùng lượng token mỗi lượt cho phép gần **200 lượt trao đổi**, giúp cuộc trò chuyện dài hơn mà không mất thông tin trước đó.

## 5. Tổng kết
- **Context window** là khía vervolgens Then decide final answer. Let's craft final output in Vietnamese markdown as required.



# Bài học: Context Window trong mô hình ngôn ngữ lớn (LLM)

## 1. Mục tiêu học tập
Sau khi đọc bài học này, bạn sẽ có thể:
- Giải thích khái niệm **context window** (context length) của LLM và tại sao nó quan trọng.  
- Mô tả cách token hoạt động và mối quan hệ giữa token, từ và ký tự.  
- Liệt kê các lý do khiến mô hình có giới hạn độ dài context tối đa.  
- Nhận ra thách thức khi mở rộng context window (tài nguyên tính toán, hiệu suất, an ninh).  
- So sánh kích thước context window của một số mô hình LLM nổi bật hiện nay (GPT, Llama, Mistral, Gemini, Claude).  

## 2. Tổng quan
Trong các mô hình ngôn ngữ lớn, **context window** xác định lượng văn bản (được đo bằng token) mà mô hình có thể “nhớ” và xử lý đồng thời tại một thời điểm. Nó tương đương với bộ nhớ làm việc của mô hình và ảnh hưởng trực tiếp đến khả năng xử lý cuộc trò chuyện dài, tài liệu hoặc mã nguồn. Khi đầu vào vượt quá kích thước context window, cần cắt bớt (truncate) hoặc tóm tắt để mô hình tiếp tục hoạt động.  

## 3. Kiến thức cốt lõi  

### 3.1. Định nghĩa và vai trò  
- **Context window** (hoặc context length) = số token tối đa mà LLM có thể xem xét trong một lần suy luận.  
- Càng lớn context window, mô hình có thể đưa vào đầu vào nhiều thông tin hơn → thường dẫn đến độ chính xác cao hơn, ít hallucination hơn, trả lời mạch lạc hơn và cho phép trò chuyện dài.  
- Tuy nhiên, việc tăng kích thước này không miễn phí: yêu cầu tính toán tăng mạnh và có thể mở rộng bề mặt tấn công (attack surface).  

### 3.2. Tokenization – đơn vị thực tế của context  
- LLM không làm việc với từ hoặc ký tự đơn lẻ mà làm việc với **token**.  
- Một token có thể là:  
  - Một ký tự đơn (ví dụ: “a” trong “cat” khi không mang ý nghĩa riêng).  
  - Một phần của từ (tiền tố, hậu tố).  
  - Một từ hoàn chỉnh.  
  - Một cụm từ ngắn (hai‑ba từ).  
- Do không có tỷ lệ từ‑token cố định, thường ước lượng **~1,5 token/từ** cho mục đíchทั่วไป.  
- Công cụ trực quan hoá như **Tokenizer Playground** trên Hugging Face giúp thấy cách các mô hình khác nhau chia thành token.  

### 3.3. Tại sao mô hình có giới hạn context length tối đa?  
- Hầu hết LLM hiện nay dựa trên kiến trúc **Transformer** với cơ chế **self‑attention**.  
- Self‑attention tính toán mối quan hệ giữa mọi cặp token trong chuỗi → độ phức tạp tính toán tăng **bậc hai** theo độ dài chuỗi (O(n²)).  
- Khi độ dài context tăng:  
  - Yêu cầu tính toán (và chi phí) tăng gấp bốn lần khi số token gấp đôi.  
  - Thời gian suy luận chậm dần vì mỗi bước tạo token mới phải xem xét lại tất cả token trước đó.  
  - Trong chatbot, ngoài đầu vào người dùng còn có **system prompt**, dữ liệu từ **RAG**, và các ký tự định dạng cũng chiếm phần context.  
- Đối với các mô hình khác (diffusion models dùng cho sinh ảnh), context length áp dụng cho số pixel mà self‑attention phải xử lý.  

### 3.4. Thách thức khi mở rộng context window  

#### 3.4.1. Thách thức về hiệu suất  
- Nghiên cứu năm 2023 (“Lost in the Middle”) chỉ ra rằng LLM thường **không sử dụng mạnh mẽ** thông tin ở giữa đoạn dài; hiệu suất tốt nhất khi thông tin liên quan nằm ở đầu hoặc cuối context.  
- Các kỹ thuật như **Rotary Position Embedding (RoPE)** giúp cải thiện khả năng atención trên khoảng cách lớn, nhưng vấn đề “lost in the middle” vẫn còn.  
- Các benchmark (NIAH, RULER, LongBench) được thiết kế để đo khả năng tìm và sử dụng thông tin trong đoạn dài.  

#### 3.4.2. Thách thức về an ninh và cybersecurity  
- Context window mở rộng cũng mở rộng **attack surface** – powierzchon tấn công.  
- Nghiên cứu của Anthropic (2024) cho thấy độ dài context lớn hơn làm tăng khả năng “jailbreaking” (tiếp cận hạn chế) và dẫn đến phản hồi có hại.  
- Vì vậy, việc tăng context length phải đi kèm với các biện pháp giảm thiểu rủi ro (lọc prompt, giám sát output, v.v.).  

### 3.5. Kích thước context window của một số mô hình LLM nổi bật (tháng 10/2024)  

| Hãng / séries | Mô hình | Context window (tokens) | Ghi chú |
|---------------|---------|------------------------|---------|
| **OpenAI – GPT** | GPT‑3.5 (ban đầu) | 4 096 | sau đó mở rộng lên 8 192 (GPT‑3.5‑Turbo) |
| | GPT‑4 / GPT‑4‑Turbo | 128 000 | output tối đa 4 096 token |
| | GPT‑4o / GPT‑4o‑mini | 128 000 | output tối đa 16 384 token |
| | O‑1 series | 128 000 | output context length lớn hơn |
| **Meta – Llama** | Llama (origin) | 2 048 | |
| | Llama 2 | 4 096 | |
| | Llama 3 (initial) | ~8 000 | |
| | Llama 3.1 | 128 000 | |
| | Llama 3.2 | 128 000 | |
| **Mistral AI** | Mistral Large 2 | 128 000 | flagship model |
| **Google – Gemini** | Gemini 1.5 Pro | ≤ 2 000 000 | lớn nhất trong các mô hình thương mại |
| | Gemini 1.5 Flash | 1 000 000 | |
| **Anthropic – Claude** | Claude 3.5 Sonnet | ~200 000 | |
| | Claude Enterprise (tháng 9/2024) | 500 000 | mở rộng qua gói doanh nghiệp |

> **Lưu ý:** Các con số trên có thể thay đổi khi các nhà phát hành phát hành bản bản mới; hãy luôn tham khảo tài liệu chính xác nhất từ nhà cung cấp.  

## 4. Ví dụ minh họa  

### Ví dụ 1: Cách token chia từ  
Giả sử câu tiếng Anh:  

```
Jeff drove a car.
```

- Khi sử dụng bộ tokenizer phổ biến (ví dụ: GPT‑2 BPE), mỗi từ thường trở thành một token riêng:  
  `["Jeff", "drove", "a", "car", "."]` → **5 tokens**.  
- Tuy nhiên, nếu dùng tokenizer khác, dấu chấm có thể được gộp vào từ trước hoặc được bỏ qua, làm thay đổi số token.  

### Ví dụ 2: Ảnh hưởng của context window tới chatbot  
Giả sử một chatbot có context window = 4096 token.  
- Mỗi lượt trao đổi (câu hỏi + câu trả lời) tiêu thụ khoảng 150 token (kèm system prompt, định dạng).  
- Với 4096 token, bot có thể duy trì khoảng **27 lượt trao đổi** trước khi bắt buộc phải cắt bớt hoặc tóm tắt lịch sử trò chuyện.  
- Nếu tăng context window lên 32768 token, cùng lượng token mỗi lượt cho phép gần **200 lượt trao đổi**, giúp cuộc trò chuyện dài hơn mà không mất thông tin trước đó.  

## 5. Tổng kết  
- **Context window** quyết định lượng thông tin mà một LLM có thể xử lý đồng thời; nó ảnh hưởng trực tiếp đến chất lượng trả lời, khả năng duy trì cuộc trò chuyện và chi phí tính toán.  
- Token là đơn vị thực tế của context; không có tỷ lệ từ‑token cố định nhưng trung bình khoảng 1,5 token/từ là ước lượng thường dùng.  
- Giới hạn context length xuất phát từ tính chất bậc hai của self‑attention trong kiến trúc Transformer và từ các nhu cầu thực tế như system prompt, dữ liệu RAG và ký tự định dạng.  
- Mở rộng context window mang lại lợi ích nhưng đồng thời đưa ra thách thức về hiệu suất (tài nguyên tính toán, thời gian suy luận, hiện tượng “lost in the middle”) và an ninh (mở rộng bề mặt tấn công, khả năng jailbreaking).  
- Các mô hình LLM hàng đầu hiện nay cung cấp context window từ vài nghìn token (GPT‑3.5 ban đầu) tới hơn 2 triệu token (Gemini 1.5 Pro), cho thấy xu hướng tăng mạnh nhưng cũng cần cân nhắc trade‑offs khi ứng dụng trong thực tiễn.  

---  
*Bài học này được viết dựa trên nguồn tài liệu từ IBM Think về “What is a context window?” và không thêm thông tin bên ngoài phạm vi đã cho.*