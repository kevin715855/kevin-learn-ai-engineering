# Cơ sở dữ liệu vector và ứng dụng trong AI

## 1. Mục tiêu học tập
- Hiểu tại sao cơ sở dữ liệu vector là thành phần quan trọng trong các ứng dụng AI mở rộng.
- Đọc được quy trình lưu trữ, truy vấn vector và cách nó thay đổi so với cách truy vấn truyền thống.
- Nắm vững khái niệm Retrieval‑Augmented Generation (RAG) và cách áp dụng nó trong chatbot, hỏi‑đáp.
- Giải thích các thuật ngữ chính: index, vector embedding, dimensions, distance metric.
- Thực hành ví dụ đơn giản về việc chuyển đổi văn bản thành vector và truy vấn tìm kiếm tương tự.

## 2. Tổng quan
Cơ sở dữ liệu vector (vector database) lưu trữ dữ liệu dưới dạng **vector embedding** – một mảng số biểu thị đặc trưng của đối tượng (văn bản, hình ảnh, âm thanh, …) mà một mô hình học máy đã học được. Khi có một truy vấn, thay vì phải quét toàn bộ bộ dữ liệu hay chạy lại mô hình, chúng ta chỉ cần so sánh vector truy vấn với các vector đã lưu và lấy những vector “gần nhất” theo một khoảng cách xác định. Nhờ đó, các tác vụ như tìm kiếm ngữ nghĩa, phân loại, hệ thống gợi ý và phát hiện bất thường trở nên nhanh chóng và hiệu quả hơn.

Vector database cũng là nền tảng cho **Retrieval Augmented Generation (RAG)** – kỹ thuật bổ sung ngữ cảnh cho mô hình ngôn ngữ lớn (LLM) bằng cách truy xuất các đoạn văn liên quan từ kho vector và chèn chúng vào prompt trước khi đưa vào LLM.

## 3. Kiến thức cốt lõi

### 3.1 Vector database là gì?
- Là một hệ thống lưu trữ tối ưu để **tìm kiếm nearest‑neighbor** trong không gian vector.
- Mỗi bản ghi là một vector embedding (một mảng số thực) kèm theo metadata (ID, nội dung gốc, …).
- Hỗ trợ các thao tác: **insert**, **update**, **delete**, và soprattutto **query** (tìm vector gần nhất).

### 3.2 Quy trình làm việc của vector search
1. **Chuyển đổi dữ liệu ban đầu** → vector embedding qua một mô hình embedding (ví dụ: mô hình text‑embedding của Workers AI).  
2. **Lưu trữ vector** vào index của Vectorize (mỗi index là một cơ sở dữ liệu độc lập).  
3. **Chuyển truy vấn** (câu hỏi, hình ảnh, …) cùng mô hình embedding → vector truy vấn.  
4. **Truy vấn Vectorize** → trả về danh sách các vector có khoảng cách nhỏ nhất tới vector truy vấn.  
5. **Lấy lại đối tượng gốc** từ storage (R2, KV, D1…) dựa trên ID của các vector trả về và đưa cho người dùng.

> Nếu không có vector database, mỗi lần truy vấn buộc phải gửi toàn bộ dataset kèm truy vấn tới mô hình → tốn thời gian, tài nguyên và thường vượt quá giới hạn đầu vào của mô hình.

### 3.3 Retrieval Augmented Generation (RAG)
- Mục tiêu: cung cấp **bối cảnh bổ sung** cho LLM để câu trả lời chính xác và liên quan hơn.
- Quy trình:
  1. Tạo vector embedding từ corpus (tài liệu sản phẩm, nghiên cứu, …) và lưu vào Vectorize.  
  2. Khi người dùng gửi prompt:
     - Embedding prompt bằng cùng mô hình.  
     - Tìm kiếm semantic trong Vectorize → lấy các vector gần nhất.  
     - Ánh xạ vector về nội dung gốc (nếu không được lưu kèm metadata).  
     - Ghép nội dung đó vào prompt gốc → gửi vào LLM.  
- Kết quả: LLM sinh ra câu trả lời dựa trên cả câu hỏi và bối cảnh đã được truy xuất trước.

### 3.4 Terminology quan trọng
| Thuật ngữ | Giải thích |
|-----------|------------|
| **Index / Database** | Trong Vectorize, mỗi index là một cơ sở dữ liệu độc lập; hệ thống tự động tối ưu và tái‑xây dựng khi chèn dữ liệu mới. |
| **Vector embedding** | Biểu diễn số (mảng float) của đối tượng do mô hình học máy sinh ra; là một **one‑way representation** – không thể ngược lại được đối tượng gốc từ vector alone. |
| **Dimensions** | Chiều dài của vector (số thành phần float). Được xác định bởi mô hình embedding; càng nhiều chiều có thể tăng độ chính xác nhưng cũng tăng bộ nhớ, tính toán và latency. |
| **Distance metric** | Hàm đo khoảng cách giữa hai vector, quyết định “similarity”. Các chỉ số phổ biến: Cosine, Euclidean (L2), Dot Product. Lựa chọn phụ thuộc vào loại embedding và bài toán (ví dụ: Cosine thường tốt cho văn bản). |

## 4. Ví dụ minh họa

### 4.1 Tạo vector embedding từ một câu văn
Giả sử chúng ta sử dụng mô hình text‑embedding của Workers AI, đầu ra là vector 768 chiều. Câu `"This is a story about an orange cloud"` được biểu diễn như sau (được rút gọn đểแสดง ý tưởng):

```json
[-0.019273685291409492, -0.01913292706012726, /* 764 giá trị giữa */, 0.0007094172760844231, 0.043409910053014755]
```

### 4.2 Lưu trữ và truy vấn
1. **Insert** vector trên vào index `my-docs`.  
2. Khi người dùng truy vấn với câu `"tale of a cloud"` → mô hình sinh vector truy vấn `q`.  
3. Vectorize thực hiện tìm kiếm nearest‑neighbor (ví dụ sử dụng Cosine distance) và trả về danh sách ID, kèm khoảng cách:
   ```
   [
     { id: "doc-42", score: 0.92 },   // cosine similarity cao → rất proches
     { id: "doc-07", score: 0.78 },
     { id: "doc-99", score: 0.65 }
   ]
   ```
4. Ứng dụng lấy ra các tài liệu gốc tương ứng (`doc-42`, `doc-07`, …) từ R2/KV/D1 và trả về cho người dùng.

### 4.3 Ví dụ RAG đơn giản
- **Corpus**: hướng dẫn sử dụng sản phẩm Cloudflare (mỗi trang được chuyển thành vector và lưu).  
- **Prompt người dùng**: `"Cách cấu hình Worker để gọi API Vectorize?"`  
1. Embedding prompt → vector `p`.  
2. Tìm kiếm trong index → trả về các đoạn về "Worker", "Vectorize", "binding".  
3. Ghép các đoạn đó vào prompt:  
   ```
   [Nội dung trích từ hướng dẫn]  
   Câu hỏi: Cách cấu hình Worker để gọi API Vectorize?
   ```
4. LLM nhận được prompt giàu bối cảnh và sinh ra câu trả lời chi tiết, chính xác hơn so với chỉ dựa vào câu hỏi gốc.

## 5. Tổng kết
- Cơ sở dữ liệu vector cho phép **truy xuất nhanh** các dữ liệu tương tự bằng cách làm việc trong không gian embedding thay vì trên dữ liệu thô.  
- Quy trình vector search bao gồm: embed → lưu → truy vấn embedding → lấy nearest‑neighbor → lấy đối tượng gốc.  
- RAG sử dụng vector database để **bổ sung ngữ cảnh** cho LLM, cải thiện chất lượng sinh văn bản trong chatbot và hỏi‑đáp.  
- Các thành phần cần nắm vững: index/database, vector embedding, dimensions, và distance metric – mỗi ảnh hưởng trực tiếp đến hiệu quả và chi phí của hệ thống.  
- Việc hiểu rõ những khái niệm trên sẽ giúp bạn thiết kế và triển khai các ứng dụng AI mở rộng, từ tìm kiếm ngữ nghĩa đến hệ thống gợi ý và sinh nội dung tăng cường.