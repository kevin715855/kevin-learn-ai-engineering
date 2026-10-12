# Retrieval‑Augmented Generation (RAG) – Kết hợp truy xuất và sinh tạo trong AI  

## 1. Mục tiêu học tập  
Sau bài học này, bạn sẽ có thể:  

- Giải thích khái niệm Retrieval‑Augmented Generation (RAG) và vai trò của nó trong hệ sinh thái LLM.  
- Mô tả quy trình hoạt động của RAG bao gồm bước truy xuất, tiền xử lý và grounded generation.  
- Liệt kê các lợi ích chính của RAG so với việc chỉ dùng LLM độc lập (thông tin mới nhất, giảm hallucination, tăng độ zwią vụ và chất lượng).  
- Xác định các thành phần công nghệ thường được sử dụng trong RAG (vector database, semantic search, hybrid search, re‑ranker) và cách chúng hỗ trợ quá trình truy xuất.  
- Nêu tên một số sản phẩm và dịch vụ Google Cloud liên quan đến việc triển khai RAG (Gemini RAG Engine, Agent Search, Vector Search, BigQuery, Grounded Generation API, AlloyDB AI).  

## 2. Tổng quan  
Retrieval‑Augmented Generation (RAG) là một kiến trúc AI kết hợp **hệ thống truy xuất thông tin** (công cụ tìm kiếm, cơ sở dữ liệu, knowledge base…) với **mô hình ngôn ngữ lớn (LLM)** để tạo ra câu trả lời **đúng, mới nhất và liên quan** tới nhu cầu cụ thể của người dùng.  
Thay vì dựa ausschließlich trên kiến thức mà LLM đã học trong giai đoạn huấn luyện (which may be outdated or contain errors), RAG cung cấp **nguồn dữ liệu bên ngoài** hiện tại để “đóng gói” (ground) đầu vào của LLM. Kết quả là các phản hồi được làm giàu bằng facts thực tế, giảm nguy cơ hallucination và nâng cao trải nghiệm người dùng.  

## 3. Kiến thức cốt lõi  

### 3.1 Quy trình hoạt động của RAG  
RAG thường thực hiện qua hai giai đoạn chính:

| Giai đoạn | Mô tả chi tiết |
|----------|----------------|
| **Retrieval và pre‑processing** | 1. Nhận câu hỏi hoặc prompt từ người dùng.<br>2. Truy vấn vào một kho dữ liệu ngoài (web, knowledge base, cơ sở dữ liệu…) bằng các thuật toán tìm kiếm mạnh mẽ (vector search, semantic search, hybrid search).<br>3. Lấy ra các đoạn văn bản (chunks) liên quan nhất.<br>4. Tiền xử lý các chunks: tokenization, stemming, loại bỏ stop‑words, parfois normalization. |
| **Grounded generation** | 1. Ghép các chunks đã xử lý vào prompt ban đầu (thường dưới dạng “context + question”).<br>2. Đưa prompt giàu context này vào LLM (đã được huấn luyện trước).<br>3. LLM sinh ra câu trả lời dựa hoàn toàn trên thông tin đã cung cấp, đảm bảo output được “grounded” bằng facts từ kho dữ liệu. |

### 3.2 Tại sao nên dùng RAG?  

| Lợi ích | Giải thích |
|--------|------------|
| **Truy cập thông tin mới nhất** | LLM chỉ biết tới dữ liệu huấn luyện; RAG cho phép truy xuất dữ liệu thời gian thực (tin tức, tài liệu nội bộ…) → câu trả lời luôn up‑to‑date. |
| **Giảm hallucination** | Khi LLM nhận facts cụ thể làm input, xác suất tạo ra thông tin sai lệch được giảm đáng kể. |
| **Tăng độ liên quan và chất lượng** | Các kỹ thuật tìm kiếm hiện đại (vector DB, semantic search, re‑ranker) đảm bảo chỉ những đoạn văn bản thực sự liên quan mới được đưa vào LLM, làm tăng coherence và fluency của output. |
| **Mở rộng khả năng xử lý đa modal** | Vector database có thể lưu trữ embeddings của ảnh, audio, video cùng với text; do đó RAG có thể truy xuất và sử dụng thông tin đa modal. |
| **Đo lường và tối ưu hóa** | Nền tảng như Gemini cung cấp các metrics (coherence, fluency, groundedness, safety, instruction_following, question_answering_quality…) để đánh giá chất lượng RAG và hướng dẫn tối ưu (tuning search engine, curating source data, refining chunking, rewriting user query). |

### 3.3 Thành phần công nghệ thường thấy trong RAG  

- **Vector database** – lưu trữ các embedding vector trong không gian cao dimension; cho phép truy xuất nhanh dựa trên similarity semantic.  
- **Semantic search** – tìm kiếm dựa trên ý nghĩa hơn là trên từ khóaExact.  
- **Hybrid search** – kết hợp semantic search và keyword search để tận dụng lợi thế của cả hai.  
- **Re‑ranker** – mô hình phụ tái điểm số các kết quả ban đầu để đưa những đoạn最相关的 lên top.  
- **Chunking strategies** – cách chia tài liệu thành các đoạn nhỏ (fixed‑size, sliding window, semantic‑based) để tối ưu việc truy xuất và giảm số token gửi vào LLM.  

### 3.4 RAG trong hệ sinh thái Google Cloud  

| Sản phẩm / Dịch vụ | Vai trò trong RAG |
|--------------------|-------------------|
| **Gemini RAG Engine** | Framework để xây dựng ứng dụng LLM có context‑augmented, quản lý toàn bộ luồng retrieval‑augmented generation. |
| **Agent Search** (Gemini platform) | Dịch vụ tìm kiếm totalmente managed, xây dựng sẵn cho RAG; cung cấp semantic & hybrid search và re‑ranking tự động. |
| **Vector Search** (Gemini platform) | Đánh chỉ vector siêu hiệu quả, cung cấp search và recall cao cho lượng lớn embeddings. |
| **BigQuery** | Kho dữ liệu lớn dùng để huấn luyện mô hình embedding hoặc làm nguồn cho Vector Search. |
| **Grounded Generation API** | Cho phép gọi LLM ở chế độ high‑fidelity, grounding bằng Google Search, facts inline hoặc search engine tự bringen. |
| **AlloyDB AI** | Chạy các mô hình (Gemini hoặc custom) và truy xuất qua SQL phổ biến, giúp tích hợp RAG vào ứng dụng hiện có. |

### 3.5 Đánh giá và tối ưu RAG  

- Các metrics phổ biến: **coherence**, **fluency**, **groundedness**, **safety**, **instruction_following**, **question_answering_quality**.  
- Quá trình tối ưu có thể bao gồm:  
  - Điều chỉnh cấu hình search engine (số lượng vectors retrieved, threshold similarity).  
  - Chuẩn hoá và làm sạch nguồn dữ liệu (loại bỏ trùng lặp, định dạng nhất quán).  
  - Cải thiện chiến lược chunking (kích thước chunk, overlap).  
  - Tái viết hoặc sửa lỗi chính tả truy vấn trước khi tìm kiếm (query rewriting, spell‑correction).  

## 4. Ví dụ minh họa  

### 4.1 Trình tự hoạt động (giả lập pseudo‑code)

```python
# 1. Nhận câu hỏi từ người dùng
question = "Làm thế nào để請求報銷醫療費用？"

# 2. Truy xuất các đoạn văn bản liên quan từ knowledge base
retrieved_chunks = vector_search.search(
    query=question,
    top_k=5,                     # lấy 5 đoạn最相似
    reranker=True                # áp dụng re‑ranker để sắp xếp lại
)

# 3. Tiền xử lý (tokenization, loại stop‑words) – thường được thực hiện bên trong engine
context = "\n".join(retrieved_chunks)

# 4. Tạo prompt grounding
prompt = f"""Bạn là một trợ lý hỗ trợ請求報銷. Dựa vào thông tin sau:
{context}

Câu hỏi: {question}
Trả lời:"""

# 5. Gửi prompt tới LLM (Gemini) và nhận output
answer = gemini_llm.generate(prompt)

print(answer)
```

**Giải thích:**  
- Bước 2 sử dụng **vector search** để lấy ra các đoạn tài liệu (có thể là quy trình請求報銷, biểu mẫu, chính sách nội bộ) mà meaning‑wise最相似 với câu hỏi.  
- Bước 3‑4 ghép các đoạn đó thành **context** và đưa vào LLM như một phần của prompt, đảm bảo rằng LLM chỉ sinh ra câu trả lời dựa trên facts đã cung cấp.  
- Kết quả là một phản hồi **đúng**, **chi tiết** và **liên quan** tới quy trình請求報銷 cụ thể của công ty.  

### 4.2 Minh họa về giảm hallucination  

| Không dùng RAG (LLM only) | Dùng RAG |
|---------------------------|----------|
| **Câu hỏi:** “Năm 2024, công ty C đã ra mắt sản phẩm nào?”<br>**LLM trả lời:** “Công ty C ra mắt sản phẩm X vào tháng 3/2024.” (thông tin giả, vì dữ liệu huấn luyện chỉ đến năm 2023) | **Câu hỏi:** 同上<br>**RAG:** truy xuất từ báo cáo tài chính Q1‑2024 của công ty C → lấy đoạn “Công ty C ra mắt sản phẩm Y vào ngày 15/01/2024”.<br>**LLM trả lời:** “Công ty C ra mắt sản phẩm Y vào ngày 15/01/2024.” (đúng, dựa trên fact thực tế) |

## 5. Tổng kết  

- Retrieval‑Augmented Generation (RAG) kết hợp **hệ thống truy xuất thông tin mạnh mẽ** (vector DB, semantic/hybrid search, re‑ranker) với **LLM** để tạo ra output **đúng, mới nhất và liên quan**.  
- Quy trình bao gồm **retrieval + pre‑processing** để lấy các đoạn văn bản liên quan, tiếp theo là **grounded generation** khi LLM sinh ra câu trả lời dựa trên các đoạn đó.  
- RAG giúp **cập nhật kiến thức**, **giảm hallucination**, **tăng độ liên quan và chất lượng**, đồng thời cho phép xử lý **đa modal** và **tối ưu đo lường** bằng các metrics cụ thể.  
- Trong hệ sinh thái Google Cloud, các dịch vụ như **Gemini RAG Engine**, **Agent Search**, **Vector Search**, **BigQuery**, **Grounded Generation API** và **AlloyDB AI** cung cấp đầy đủ công cụ cần thiết để xây dựng, triển khai và tối ưu hóa hệ thống RAG.  
- Việc áp dụng RAG phù hợp với các trường hợp sử dụng như chatbot nội bộ, trợ lý pháp lý, hệ thống hỗ trợ quyết định, nơi cần truy cập dữ liệu mới nhất và đặc thù mà LLMalone không thể cung cấp.  

Bằng cách nắm vững các khái niệm và quy trình trên, bạn có thể bắt đầu thiết kế và triển khai các ứng dụng AI có khả năng **sinh tạo có cơ sở** (grounded generation) trên dữ liệu thực tế của doanh nghiệp.