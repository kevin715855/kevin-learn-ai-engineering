# Retrieval‑Augmented Generation (RAG)

## 1. Mục tiêu học tập

Sau bài học này, người học sẽ:

- Hiểu khái niệm và mục tiêu của Retrieval‑Augmented Generation.
- Giải thích quy trình làm việc của RAG (từ retrieval, tiền xử lý tới grounded generation).
- Nhận ra lợi ích của RAG so với việc chỉ dùng LLM thuần túy, đặc biệt về tính chính xác, cập nhật và khả năng kiểm soát hallucination.
- Xác định một số thành phần và dịch vụ trên Google Cloud thường được dùng để xây dựng hệ thống RAG.
- Viết một ví dụ đơn giản minh họa cách kết hợp truy xuất dữ liệu và sinh văn bản bằng LLM.

## 2. Tổng quan

Retrieval‑Augmented Generation (RAG) là một khung công tác kết hợp hai điểm mạnh:

- **Hệ thống truy xuất thông tin** (công cụ tìm kiếm, cơ sở dữ liệu, knowledge base…) để lấy ra các tài liệu liên quan nhất với câu hỏi.
- **Mô hình ngôn ngữ lớn (LLM)** có khả năng sinh văn bản tự nhiên và hiểu ngữ cảnh.

Thông qua việc **cung cấp cho LLM những事実 (facts) đã được truy xuất trước**, RAG giúp sinh ra các câu trả lời mà:

- **Đúng facts** (giảm hallucination),
- **Liên tục cập nhật** (không bị hạn chế bằng dữ liệu huấn luyện cũ),
- **Phù hợp với nhu cầu cụ thể** của ứng dụng (do dữ liệu nguồn được tuỳ chỉnh).

## 3. Kiến thức cốt lõi

### 3.1 Quy trình làm việc của RAG

1. **Truy xuất và tiền xử lý**  
   - Truy vấn vào một kho dữ liệu (web pages, knowledge base, vector DB…) bằng thuật toán tìm kiếm (semantic, hybrid…).  
   - Kết quả trả về được tiền xử lý: tách từ (tokenization), stemming, loại bỏ stop‑words, sometimes chunking thành các đoạn ngắn để phù hợp với窗口 context của LLM.

2. **Grounded generation**  
   - Đoạn văn bản đã được tiền xử lý được chèn vào prompt (hoặc đưa vào bộ nhớ context) của LLM.  
   - LLM sinh ra câu trả lời dựa trên cả kiến thức nội pre‑train và thông tin được cung cấp, vì vậy đầu ra được “đóng kiếm” (grounded) trên các feit thực tế mà hệ thống đã truy xuất.

### 3.2 Tại sao nên dùng RAG?

| Lợi ích | Mô tả |
|---------|-------|
| **Truy cập thông tin mới nhất** | LLM chỉ biết đến dữ liệu khi huấn luyện; RAG cho phép cung cấp dữ liệu thực‑time hoặc dữ liệu riêng tư. |
| **Giảm hallucination** | Khi LLM nhận được facts rõ ràng, xác suất sinh ra thông tin sai lệch thấp hơn. |
| **Tìm kiếm vector và re‑ranking** | Vector database lưu trữ embeddings → tìm kiếm dựa trên độ similarity ngữ nghĩa; re‑ranker cải thiện độ liên quan của kết quả trả về. |
| **Nâng chất lượng sinh ra** | Đoạn context giàu facts giúp LLM tạo ra câu trả lời đồng mạch, mạch lạc và tuân thủ hướng dẫn. |
| **Đánh giá và tối ưu hoá** | Các chỉ số như coherence, fluency, groundedness, safety … cho phép đo lường và cải thiện hệ thống RAG qua việc điều chỉnh search engine, chuẩn bị source data, hoặc tối ưu hoá prompt. |
| **Ứng dụng rộng** | Có thể tích hợp vào chatbot, agent, hoặc bất kỳ ứng dụng LLM nào cần kiến thức ngoài bộ dữ liệu huấn luyện. |

### 3.3 Các thành phần liên quan trên Google Cloud

- **Gemini Enterprise Agent Platform – RAG Engine**: khung làm việc để phát triển ứng dụng LLM tăng cường bằng retrieved data.  
- **Agent Search on Gemini Enterprise Agent Platform**: công cụ tìm kiếm quản lý hoàn toàn, bao gồm semantic & hybrid search, để xây dựng RAG.  
- **Vector Search on Gemini Enterprise Agent Platform**: chỉ mục vector hiệu quả cao, hỗ trợ tìm kiếm semantic và hybrid trên lượng lớn embeddings.  
- **BigQuery**: kho dữ liệu lớn, có thể dùng để huấn luyện hoặc lưu trữ embeddings phục vụ Vector Search.  
- **Grounded Generation API**: cho phép sinh văn bản với sự căn cứ dựa trên Google Search, facts nội bộ hoặc engine tìm kiếm tùy chỉnh.  
- **AlloyDB AI**: cho phép chạy mô hình trong Agent Platform và truy vấn qua SQL thông thường.

## 4. Ví dụ minh họa

Giả sử chúng ta muốn xây dựng một chatbot trả lời câu hỏi về chính sách bảo hiểm nội bộ của công ty. Dưới đây là luồng xử lý đơn giản (giả sử đã có vector DB chứa các đoạn văn bản chính sách đã được embed):

```text
1. Người dùng hỏi: "Chính sách báo pierde tai nạn ở công ty như thế nào?"
2. Truy vấn vào Vector Search:
   - Đưa câu hỏi vào embedding model → vector q.
   - Tìm k nearest vectors trong DB → lấy ra 3 đoạn văn bản có độ similarity cao nhất.
3. Tiền xử lý retrieved chunks:
   - Tokenize, loại bỏ stop‑words, ghép lại thành một đoạn context ngắn.
4. Xây dựng prompt cho LLM (Gemini):
   ```
   Bạn là trợ lý bảo hiểm nội bộ. Dựa vào thông tin sau:
   <retrieved_chunks>
   Trả lời câu hỏi của người dùng một cách chính xác và ngắn gọn.
   ```
5. Gửi prompt đến LLM → nhận câu trả lời đã được "đóng kiếm" trên các feit đã truy xuất.
6. Trả lại câu trả lời cho người dùng.
```

**Kết quả mong đợi**: Chatbot sẽ cung cấp câu trả lời dựa trên nội dung chính sách mới nhất mà đã được lưu trong vector DB, thay vì dựa vào kiến thức cũ có thể đã lỗi thời trong LLM.

## 5. Tổng kết

- RAG kết hợp **truy xuất thông tin** và **sinh ngôn ngữ** để tạo ra câu trả lời chính xác, cập nhật và ít bị hallucination.  
- Quy trình bao gồm **truy xuất → tiền xử lý → grounded generation**, trong đó bước truy xuất quyết định chất lượng của context cung cấp cho LLM.  
- Lợi ích chính: truy cập dữ liệu mới, giảm sai sót, nâng chất lượng sinh văn bản, và khả năng mở rộng cho các ứng dụng chuyên biệt.  
- Trên Google Cloud, các dịch vụ như **RAG Engine**, **Agent Search**, **Vector Search**, **BigQuery**, **Grounded Generation API**, và **AlloyDB AI** cung cấp nền tảng để xây dựng, triển khai và tối  hoá hệ thống RAG.  
- Khi triển khai, cần chú ý tới việc chọn embedding model phù hợp, thiết kế chunking hợp lý, sử dụng re‑ranker để nâng độ liên quan, và đánh giá đầu ra bằng các chỉ số như groundedness, coherence, fluency để nâng bản chất của hệ thống.

Với những kiến thức trên, bạn đã có thể bắt đầu xây dựng một ứng dụng RAG cơ bản và постепенно mở rộng để đáp ứng các nhu cầu nghiệp vụ phức tạp.