# Bài học: Cửa sổ ngữ cảnh (Context Window) trong mô hình ngôn ngữ lớn

## 1. Mục tiêu học tập
- Định nghĩa **cửa sổ ngữ cảnh** và vai trò của nó trong các mô hình ngôn ngữ lớn (LLM).  
- Giải thích khái niệm **token**, cách mô hình biến đổi văn bản thành token và mối quan hệ giữa token và số từ.  
- Hiểu lý do tại sao mô hình có **độ dài tối đa** của cửa sổ ngữ cảnh và hoạt động của механизм self‑attention trong kiến trúc transformer.  
- Nhận ra các **thách thức** khi mở rộng cửa sổ ngữ cảnh: nhu cầu về tài nguyên tính toán, hiệu suất (lost‑in‑the‑middle) và an toàn (jailbreaking).  
- So sánh kích thước cửa sổ ngữ cảnh của các mô hình LLM nổi bật hiện nay (GPT, Llama, Mistral, Gemini, Claude).  

## 2. Tổng quan
Cửa sổ ngữ cảnh (context window) là lượng văn bản – đo bằng **token** – mà một LLM có thể “nhớ” hoặc xử lý đồng thời tại một thời điểm. Nó quyết định độ dài tối đa của đoạn hội thoại, tài liệu hoặc mã nguồn mà mô hình có thể xem xét mà không phải cắt bớt hoặc tóm tắt. Khi hiểu rõ khái niệm này, người lập trình và nhà nghiên cứu có thể tối ưu hóa prompt, lựa chọn mô hình phù hợp và đánh giá tác vụ như tóm tắt, sinh văn bản hoặc Retrieval‑Augmented Generation (RAG) một cách hiệu quả.

## 3. Kiến thức cốt lõi

### 3.1. Định nghĩa cửa sổ ngữ cảnh  
- Cửa sổ ngữ cảnh cũng gọi là **context length**.  
- Là bộ nhớ làm việc của mô hình: quyết định có thể xem xét bao nhiêu token đầu vào (prompt, hội thoại, tài liệu, mã).  
- Khi đầu vào vượt quá kích thước cửa sổ, mô hình phải **cắt bớt** (truncate) hoặc **tóm tắt** (summarize) trước khi suy diễn.

### 3.2. Token và quá trình token hóa  
- **Token** là đơn vị nhỏ nhất mà mô hình hiểu, không nhất thiết phải là một từ. Một token có thể là:  
  - Một ký tự đơn (ví dụ: “a”).  
  - Một phần từ (tiền tố, hậu tố).  
  - Một từ đầy đủ.  
  - Một cụm từ ngắn (hai‑ba từ).  
- Ví dụ minh họa (trích từ nguồn):  

  ```text
  “Jeff drove a car.”          → “a” là một từ → token riêng
  “Jeff is amoral.”            → “a” không phải từ, nhưng thay đổi nghĩa → hai token (“a” + “moral”)
  “Jeff loves his cat.”        → “a” là chữ trong “cat” → không cần token riêng
  ```

- Không có tỷ lệ từ‑token cố định; ước lượng thường dùng là **≈ 1.5 token / từ** cho tiếng Anh.  
- Công cụ như *Tokenizer Playground* trên Hugging Face giúp試 nghiệm cách khác nhau của các tokenizer.

### 3.3. Lý do mô hình có độ dài tối đa  
- Hầu hết LLM hiện nay dựa trên kiến trúc **transformer** và sử dụng **self‑attention** để tính toán mối quan hệ giữa mọi cặp token trong chuỗi.  
- Ma trận внимания có kích thước **O(n²)** với n = số token → yêu cầu tính toán tăng bậc hai khi độ dài chuỗi tăng.  
- Ngoài token đầu vào, cửa sổ còn lưu trữ:  
  - *System prompt* (đôi khi ẩn từ người dùng).  
  - Thông tin từ nguồn ngoài trong **RAG**.  
  - Các ký tự đặc biệt, ngắt dòng, định dạng.  

### 3.4. Ảnh hưởng của việc tăng kích thước cửa sổ  
- **Lợi ích**: xử lý đầu vào dài hơn → ít hallucination hơn, trả lời mạch lạc hơn, duy trì cuộc trò chuyện dài, phân tích chuỗi dữ liệu dài.  
- **Chi phí**:  
  - Tài nguyên tính toán tăng theo **bậc hai** (ví dụ: gấp hai độ dài token → cần gấp bốn lần мощность).  
  - Thời gian suy diễn chậm dần vì mỗi bước autoregressive phải tính attention với tất cả token trước đó.  
  - Tiềmangular tăng độ b attacking surface (jailbreaking).  

### 3.5. Thách thức khi mở rộng cửa sổ  
#### 3.5.1. Hiệu suất (Performance)  
- Nghiên cứu “Lost in the Middle” (2023) cho thấy LLM ít sử dụng thông tin nằm giữa đoạn văn bản dài; hiệu suất tốt nhất khi thông tin liên quan nằm đầu hoặc cuối.  
- Các kỹ thuật như **Rotary Position Embedding (RoPE)** giúp cải thiện attention đối với token cách xa nhau.  
- Các benchmark đo lường khả năng sử dụng context dài: **Needle‑in‑a‑Haystack (NIAH)**, **RULER**, **LongBench**.  

#### 3.5.2. An toàn và bảo mật (Safety & Cybersecurity)  
- Cửa sổ lớn hơn mở rộng *attack surface*; nghiên cứu từ Anthropic (2024) cho thấy tăng độ dài context cũng tăng khả năng bị **jailbreak** và tạo ra nội dung вредоносный.  

### 3.6. Kích thước cửa sổ ngữ cảnh của các mô hình LLM nổi bật (tháng 10/2024)  

| Nhà cung cấp / Série mô hình | Kích thước cửa sổ ngữ cảnh (tokens) | Ghi chú |
|------------------------------|--------------------------------------|---------|
| **GPT‑3.5** (ban đầu)        | 4,096                                | Sau này mở rộng thành 8,192 với GPT‑3.5‑Turbo |
| **GPT‑4** (ban đầu)          | 8,192                                | Cùng GPT‑4‑Turbo hiện nay mở rộng lên 128,000 (output còn limited ở 4,096) |
| **GPT‑4o / GPT‑4o‑mini**     | 128,000                              | Output tối đa 16,384 token |
| **O1 family**                | 128,000                              | Có khả năng output dài hơn GPT‑4o |
| **Llama 1**                  | 2,048                                | – |
| **Llama 2**                  | 4,096                                | – |
| **Llama 3** (2024)           | ~8,000                               | – |
| **Llama 3.1**                | 128,000                              | Long context window |
| **Llama 3.2**                | 128,000                              | – |
| **Mistral Large 2**          | 128,000                              | – |
| **Gemini 1.5 Pro**           | ≤ 2,000,000                          | Lớn nhất hiện tại trong các mô hình thương mại |
| **Gemini 1.5 Flash**         | 1,000,000                            | – |
| **Claude 3.5 Sonnet**        | ~200,000                             | – |
| **Claude Enterprise** (2024) | 500,000                              | Mở rộng qua gói doanh nghiệp |

> *Lưu ý*: Các con số có thể thay đổi khi các nhà cung cấp julkais bản cập nhật mới.

## 4. Ví dụ minh họa

### 4.1. Minh họa token hóa  
Xét ba câu sau (trích từ nguồn):

1. `"Jeff drove a car."`  
   - Từ “a” là một từ độc lập → được mã hoá thành **một token**.

2. `"Jeff is amoral."`  
   - Chuỗi “amoral” được tách thành “a” + “moral” → **hai token**.

3. `"Jeff loves his cat."`  
   - Chữ “a” chỉ là một phần trong từ “cat” → **không cần token riêng**.

### 4.2. Tài nguyên tính toán khi tăng độ dài  
Giả sử một mô hình xử lý **n** token cần **C·n²** đơn vị tính (C là hằng số).  
- Nếu tăng n từ 1.000 token lên 2.000 token (gấp đôi), lượng tính toán cần **gấp bốn lần** (2² = 4).  
- Do đó, việc tăng cửa sổ từ 8K → 32K token (gấp 4) sẽ cần **gấp 16 lần** tài nguyên so với bản 8K.

### 4.3. So sánh thực tiễn  
- Một tài liệu dài 100 000 từ (≈150 000 token) có thể được đưa vào **Gemini 1.5 Pro** (2 M token) mà không cần cắt.  
- T同样的一份文档若放进 **GPT‑4o** (128 K token) sẽ bị cắt bớt khoảng 22 K token (~15 % nội dung) hoặc buộc phải dùng technik tóm tắt/RAG trước khi đưa vào mô hình.  
- Đối với một cuộc trò chuyện dài 30 000 token, **Claude Enterprise** (500 K token) còn đủ dư cho nhiều turno hội thoại, còn **Llama 3** (~8 K) chỉ có thể duy trì khoảng 5‑6 lượt échanges trước khi phải cắt.

## 5. Tổng kết
- Cửa sổ ngữ cảnh quyết định lượng thông tin mô hình có thể xử lý đồng thời; nó được đo bằng **token**, không phải từ.  
- Token hóa là quá trình biến đổi văn bản thành các ID số; một token có thể biểu diễn ký tự, phần từ, từ cụm hoặc từ đơn tùy thuộc vào mô hình và tiếng-language.  
- Lý do giới hạn độ dài stems from the quadratic cost of the self‑attention mechanism in transformer architectures, plus dodatkovy components like system prompts and RAG data.  
- Mở rộng cửa sổ mang lại lợi ích về khả năng hiểu bối cảnh dài, nhưng đi kèm với chi phí tính toán cao hơn, tốc độ suy diễn chậm lại và rủi ro bảo mật tăng.  
- Các nhà cung cấp continuamente tăng kích thước cửa sổ: từ vài nghìn token (GPT‑3.5 ban đầu) đến hàng trăm nghìn (GPT‑4o, Llama 3.1) và甚至 lên tới hai triệu token (Gemini 1.5 Pro).  
- Khi thiết kế ứng dụng AI, cần **match** kích thước cửa sổ với độ dài dữ liệu thực tế, cân đối giữa hiệu quả, chi phí và an toàn, và cân nhāk sử dụng kỹ thuật như tóm tắt, RAG hoặc chọn mô hình có context window phù hợp.