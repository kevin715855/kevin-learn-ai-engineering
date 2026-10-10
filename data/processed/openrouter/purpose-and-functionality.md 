# Vector Databases – Cơ bản và ứng dụng trong AI  

## 1. Mục tiêu học tập  

Sau khi hoàn thành bài học, người học sẽ có thể:  

- Giải thích khái niệm **vector database** và so sánh với cơ sở dữ liệu quan hệ hoặc NoSQL truyền thống.  
- Mô tả ba giai đoạn chính của một truy vấn trong vector database: *indexation*, *inquiry* và *post‑production*.  
- Trình bày cách **vector search** hoạt động và tại sao việc này thay đổi cách tìm kiếm dữ liệu có chiều cao.  
- Liệt kê 12 use case tiêu biểu và đưa ra ví dụ cụ thể cho từng trường hợp.  
- Minh họa cách vector database hỗ trợ **Retrieval Augmented Generation (RAG)** và phối hợp với Large Language Model (LLM).  
- Đánh giá lợi ích và thách thức chính khi triển khai vector database.  
- Xác định các tiêu chí cần xem xét khi chọn một vector database phù hợp với dự án.  
- Nhìn về xu hướng phát triển của vector database trong thời đại AI.  

## 2. Tổng quan  

Trong các hệ thống AI/ML hiện nay, mô hình thường biểu diễn dữ liệu dưới dạng **vector embedding** – một mảng số có thể đạt hàng chục hay hàng trăm chiều. Những vector này chứa thông tin ngữ nghĩa (semantic) giúp model nhận diện mối quan hệ, similarity và patterns. Tuy nhiên, việc lưu trữ và truy xuất hàng tỷ vector bằng cách sử dụng các cơ sở dữ liệu truyền thống (rows/columns, JSON documents) là không hiệu quả vì chúng không được tối ưu cho phép toán **tìm kiếm gần nhất (nearest‑neighbor)** trong không gian vector cao chiều.  

Vector database ra đời để đáp ứng nhu cầu này: đây là một hệ thống lưu trữ chuyên biệt, chỉ xử lý **vector embeddings**, đồng thời cung cấp các thuật toán chỉ mục (index) và truy vấn tiên tiến để thực hiện similarity search với tốc độ cao và khả năng mở rộng lớn.  

## 3. Kiến thức cốt lõi  

### 3.1. Định dạng và đặc điểm của vector embedding  

- Mỗi embedding là một vector **float32** (hoặc các kiểu số khác) trong không gian **Rⁿ**, n thường từ 128 đến 1024 hoặc hơn.  
- Các vector có ý nghĩa tương đồng sẽ nằm gần nhau trong không gian này (ví dụ: “cat” và “kitten” có khoảng cách Euclidean nhỏ).  

### 3.2. Cách vector database làm việc  

1. **Indexation**  
   - Khi vector được đưa vào DB, một bộ chỉ mục được xây dựng (ví dụ: KD‑tree, Ball tree, LSH, hoặc các thuật toán ANN như HNSW, IVF‑PQ).  
   - Mục tiêu là chuyển vector nguyên bản thành cấu trúc dữ liệu cho phép truy vấn gần nhất trong thời gian sub‑linear.  

2. **Inquiry (Truy vấn)**  
   - Vector truy vấn (query vector) được chuyển qua cùng bộ chỉ mục.  
   - DB tính toán khoảng cách (thường là cosine similarity, inner product hoặc Euclidean) giữa query và các vector đã được chỉ mục để tìm ra **k nearest neighbors**.  

3. **Post‑production**  
   - Kết quả nearest neighbor có thể được lọc, tái‑xếp hạng (re‑rank) hoặc combined với metadata trước khi trả về người dùng.  

### 3.3. So sánh với cơ sở dữ liệu truyền thống  

|                     | Cơ sở dữ liệu quan hệ / NoSQL | Vector database |
|---------------------|------------------------------|-----------------|
| **Kiểu dữ liệu**    | Chuỗi, số, JSON, bảng       | Vector embeddings (float) |
| **Truy vấn chính**  | Tìm kiếm exact match, range  | Tìm kiếm nearest neighbor (similarity) |
| **Thuật toán**      | B‑tree, hash, inverted index | Tree‑based, LSH, ANN (HNSW, IVF) |
| **Tối ưu cho**      | Transactional workloads      | Similarity search trên high‑dimensional data |

### 3.4. Vector database trong Retrieval‑Augmented Generation (RAG)  

- **Bước 1:** Xây dựng corpus (tài liệu, FAQ, mã nguồn…) và chuyển mỗi đoạn thành embedding bằng cùng mô hình embedding mà LLM sẽ sử dụng.  
- **Bước 2:** Lưu trữ các embedding này vào vector database (kèm metadata như đoạn văn bản gốc).  
- **Bước 3:** Khi người dùng đặt câu hỏi, hệ thống tạo embedding của câu hỏi và truy vấn vector database để lấy **k đoạn 가장相似**.  
- **Bước 4:** Những đoạn này được đưa vào prompt của LLM như “context”, giúp model sinh ra câu trả lời dựa trên cả kiến thức nội bộ và kiến thức ngoài (từ corpus).  

### 3.5. 12 use case tiêu biểu  

| # | Use case | Mô tả ngắn |
|---|----------|------------|
| 1 | **NLP** – similarity, sentiment, semantic search | Tìm tài liệu/sentence có ý nghĩa gần nhất bằng word/sentence embeddings. |
| 2 | **Phát hiện bất thường & gian lành** | So sánh vector của sự kiện hiện tại với vector “bình thường”; các điểm xa được coi là outliers. |
| 3 | **Nâng cao mô hình ML** | Lưu trữ embeddings của middle‑layer để fine‑tune hoặc phân tích feature importance. |
| 4 | **Hệ thống gợi ý** | Gợi ý sản phẩm/bài viết dựa trên similarity giữa vector người dùng và vector item. |
| 5 | **Nhận diện hình ảnh** | Vector đặc trưng từ CNN dùng để tìm ảnh có nội dung 시각 tương tự. |
| 6 | **Quảng cáo cá nhân hoá** | Giống như gợi ý: quảng cáo được chọn dựa trên độ gần với sở thích người dùng (vector). |
| 7 | **Phân cụm & phân loại** | Nhóm các vector gần nhau (clustering) hoặc quyết định nhãn dựa trên vector láng giềng. |
| 8 | **Phân tích đồ thị** | Lưu embeddings của node/edge để đo độ tương đồng giữa cấu trúc đồ thị. |
| 9 | **Y tế** – patient similarity | Biểu diễn triệu disease, gen… thành vector để tìm bệnh nhân có hồ sơ tương tự và tham chiếu liệu pháp. |
|10 | **Xe tự hành** | Lidar/radar/camera → vector đặc trưng → tìm đối tượng, tín hiệu, boc tắc trong môi trường. |
|11 | **Công cụ tìm kiếm** | Tăng độ chính xác bằng cách tìm video/hình ảnh có semantic gần query thay vì chỉ dựa trên từ khóa. |
|12 | **Streaming nhạc & multimedia** | Vector từ thuộc tính (giống, nhạc cụ, tempo) → gợi ý bài hát có “cảm giác” tương tự. |

### 3.6. Lợi ích  

- **Scalability** – قادر على lưu billions of vectors mà vẫn duy trì thời gian truy vấn gần O(log n) hoặc sub‑linear.  
- **Tốc độ similarity search** – nhờ các chỉ mục tiên tiến (HNSW, IVF‑PQ) nên truy vấn thường trong miligiây ngay cả trên tập dữ liệu lớn.  
- **Linh hoạt dữ liệu** – chấp nhận cả dữ liệu có cấu trúc (metadata) và phi cấu trúc (raw embeddings).  
- **Hỗ trợ high‑dimensional** – tối ưu cho các embedding từ transformer, CNN, …  

### 3.7. Thách thức chính  

| Thách thức | Mô tả |
|------------|-------|
| **Chi phí tính toán** | Tìm kiếm nearest neighbor trên billions of vectors vẫn tiêu tốn CPU/GPU, đặc biệt khi cần độ chính xác cao. |
| **Độ trễ (latency)** | Khi dữ liệu cực lớn hoặc truy vấn phức tạp (k lớn, các bước re‑rank) có thể tăng thời gian phản hồi. |
| **Cập nhật / xóa** | Giữ tính nhất quán của chỉ mục khi insert/delete là phức tạp; nhiều DB chỉ hỗ trợ append‑only hoặc cần rebuild périodic. |
| **Sparsity** | Trong không gian rất cao chiều, hầu hết thành phần là 0 → gây lãng phí bộ nhớ và làm chậm chỉ mục nếu không dùng kỹ thuật nén. |
| **Phức tạp triển khai** | Cần kiến thức về chỉ mục ANN, tuning tham số (efConstruction, M, nlist…) và có thể đòi hỏi phần cứng chuyên dụng. |
| **Hạn chế giao dịch** | Hầu hết không hỗ trợ ACID đầy đủ; do đó không thích hợp cho các workloads yêu cầu tính nhất quán mạnh. |

### 3.8. Cách chọn vector database phù hợp  

1. **Scalability & performance** – Kiểm tra tỷ lệ vector/second mà DB có thể ingest và latency query tại 규모 mong đợi.  
2. **Mô hình dữ liệu & indexing** – Xem DB có hỗ trợ schema linh hoạt, metadata filters, và các chỉ mục như HNSW, IVF‑PQ, ScaNN.  
3. **Dễ sử dụng** – Thư viện client (Python, Java, Go), documentation rõ ràng, công cụ quản lý (CLI, UI).  
4. **Tích hợp** – Có API REST/gRPC, connectors cho Spark, Kafka, hoặc SDK cho các framework ML (TensorFlow, PyTorch, HuggingFace).  
5. **Cộng đồng & hỗ trợ** – Số lượng issue active, fréquence releases, tài liệu hướng dẫn, và mức độ hỗ trợ commercial nếu cần.  
6. **Giấy phép & chi phí** – So sánh giữa bản quyền mở source (Apache, MIT) và bản thương lượng (giá per‑node, lưu lượng).  

## 4. Ví dụ minh họa (pseudo‑code Python + FAISS)  

```python
# 1. Chuẩn bị embeddings cho một đoạn văn bản kecil
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')   # 384‑dim embedding
corpus = [
    "Vector databases enable fast similarity search.",
    "RAG combines retrieval with generation.",
    "FAISS is a library for efficient vector search."
]
embeddings = model.encode(corpus)               # shape (3, 384)
embeddings = np.asarray(embeddings).astype('float32')

# 2. Xây dựng chỉ mục FAISS (IndexFlatL2 – brute‑force, dùng để minh họa)
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)                  # L2 distance
index.add(embeddings)                           # lưu vectors vào index

# 3. Truy vấn: tìm đoạn gần nhất với câu hỏi
query = "How does retrieval‑augmented generation work?"
q_emb = model.encode([query]).astype('float32')
D, I = index.search(q_emb, k=2)                 # D: distances, I: indices

print("Kết quả tìm nearest:")
for idx, dist in zip(I[0], D[0]):
    print(f"- {corpus[idx]} (distance={dist:.4f})")
```

**Giải thích:**  

- Bước 1 tạo vector embedding cho mỗi câu trong corpus.  
- Bước 2 xây dựng chỉ mục tuyến tính (IndexFlatL2) – trong thực tế người ta sẽ chọn HNSW hoặc IVF‑PQ để tăng tốc.  
- Bước 3 biến câu hỏi thành embedding và tìm 2 vector gần nhất; kết quả trả về là các câu có nội dung liên quan nhất, minh họa cho cách vector database cung cấp **context** cho LLM trong RAG.  

## 5. Tổng kết  

- Vector database là hệ thống lưu trữ đặc biệt dành cho **vector embeddings**, cho phép truy vấn similarity với tốc độ cao và khả năng mở rộng lớn.  
- Hoạt động qua ba giai đoạn: **indexation → inquiry → post‑production**, dựa trên các thuật toán chỉ mục tiên tiến (tree‑based, LSH, ANN).  
- So sánh với DB truyền thống: thay vì tìm kiếm exact match, vector database tìm **nearest neighbor** trong không gian vector cao chiều.  
- Vector database đóng vai trò then chốt trong **RAG**, cung cấp context ngoài cho LLM để giảm hallucination và tăng độ tin cậy.  
- 12 use case chính thể hiện sự áp dụng rộng rãi: từ NLP, phát hiện bất thường, gợi ý, y tế, xe tự hành cho tới multimedia streaming.  
- Lợi ích nổi bật bao gồm scalability, tốc độ similarity search, và sự linh hoạt xử lý dữ liệu phi cấu trúc; thách thức bao gồm chi phí tính toán, độ trễ, cập nhật/sửa, sparsity và độ phức tạp triển khai.  
- Khi chọn một vector database, cần xem xét scalability, mô hình dữ liệu & indexing, độ dễ sử dụng, khả năng tích hợp, cộng đồng hỗ trợ và chi phí giấy phép.  
- Xu hướng chỉ cho thấy vector database sẽ ngày càng phổ biến, trở thành thành phần không thể thiếu trong các hệ thống AI‑ready data qua việc hỗ trợ hiệu quả cho embedding, similarity search và RAG.  

---  

*Bài học này cung cấp cái nhìn toàn diện về vector database, từ nguyên lý hoạt động đến cách áp dụng thực tiễn, giúp người học nắm vững kiến thức cần thiết để xây dựng và vận hành các giải pháp AI hiện đại.*