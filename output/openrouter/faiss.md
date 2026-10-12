# Facebook AI Similarity Search (Faiss) – Công cụ tìm kiếm tương đồng hiệu quả

## 1. Mục tiêu học tập
- Hiểu khái niệm Faiss và vai trò của nó trong tìm kiếm tương đồng.
- Nắm được các thuật toán indexing chính (k‑means, product quantization, OPQ) và cách chúng ảnh hưởng đến tốc độ, bộ nhớ và độ chính xác.
- Biết cách chọn metric đo lường tương đồng (Euclidean, cosine, inner‑product) phù hợp với dữ liệu và ứng dụng.
- Nắm nổi bật về khả năng mở rộng, tốc độ (CPU/GPU), độ chính xác linh hoạt và đa dạng của Faiss.
- Thực hành cài đặt Faiss và sử dụng nó cùng với LangChain và OpenAI embeddings để xây dựng một hệ thống tìm kiếm văn bản đơn giản.

## 2. Tổng quan
Các công cụ tìm kiếm truyền thống hoạt động tốt khi cần tìm **khớp hoàn toàn** (exact match), nhưng gặp khó khăn khi phải xác định các mục **tương đồng** dựa trên nội dung như hình ảnh, video hoặc văn bản. Để vượt qua giới hạn này, Meta AI (trước đây là Facebook AI) ra mắt **Faiss** – một thư viện mã nguồn mở chuyên về **tìm kiếm vector mật độ** (dense vector similarity search) và clustering. Faiss cho phép xây dựng chỉ mục (index) từ hàng triệu đến hàng tỷ vector và thực hiện tìm kiếm nearest‑neighbor với tốc độ cao và sử dụng bộ nhớ hiệu quả, đồng thời hỗ trợ chạy trên CPU và GPU.

## 3. Kiến thức cốt lõi

### 3.1 Nguyên lý hoạt động cơ bản
Faiss hoạt động bằng cách:
1. **Chuyển đổi dữ liệu** (ảnh, văn bản, audio…) thành vector biểu diễn đặc trưng (embedding) bằng các mô hình như BERT, word2vec, hoặc các mạng neural.
2. **Xây dựng chỉ mục** (index) dựa trên các thuật toán grouping và mã hóa vector để giảm không gian tìm kiếm.
3. **Thực hiện truy vấn** nearest‑neighbor trên chỉ mục đó, trả về các vector có độ tương đồng cao nhất theo metric đã chọn.

### 3.2 Các thuật toán indexing chính
| Thuật toán | Mô tả ngắn gón | Ảnh hưởng |
|------------|----------------|-----------|
| **K‑means clustering** | Chia dữ liệu thành các cụm (clusters). Khi truy vấn, chỉ cần tìm kiếm trong các cụm gần vector truy vấn nhất. | Giảm không gian tìm kiếm → tốc độ tăng, nhưng độ phụ thuộc vào chất lượng cụm. |
| **Product Quantization (PQ)** | Chia mỗi vector thành các sub‑vector, mã hóa mỗi phần bằng một bảng mã (codebook). Vector được biểu diễn bằng các mã ngắn, tiết kiệm bộ nhớ. | Tiết kiệm bộ nhớ đáng kể; độ mất accuracy thường nhỏ nếu chọn đủ sub‑vector và codebook size. |
| **Optimized Product Quantization (OPQ)** | Variante của PQ thực hiện một bước quay (rotation) trước khi áp dụng PQ để dữ liệu phù hợp hơn với lưới lượng tử hóa. | Cải thiện độ chính xác của PQ mà không zwiększyć bộ nhớ đáng kể. |

### 3.3 Các metric đo lường tương đồng
- **Euclidean distance** – khoảng cách直线 giữa兩點, phù hợp khi mô hình vector mang ý nghĩa hình học (ví dụ: đặc trưng ảnh raw).  
- **Cosine similarity** – đo cosin của góc giữa hai vector, tập trung vào hướng hơn là độ dài; thường dùng với embedding văn bản.  
- **Inner‑product (dot product)** –equivalent với Euclidean khi vector đã được chuẩn hóa L2.

Người dùng có thể chọn metric nào nhất phù hợp với bài toán và loại embedding đang sử dụng.

### 3.4 Hỗ trợ phần cứng và khả năng mở rộng
- **CPU & GPU** – Faiss cung cấp phiên bản `faiss-cpu` và `faiss-gpu`. Trên phần cứng GPU Pascal‑class mới, tốc độ có thể lên tới **20×** so với phiên bản CPU.  
- **Scalability** – Các kỹ thuật như **inverted file (IVF)** và **hierarchical navigable small world (HNSW) graphs** giúp Faiss xử lý hiệu quả tập dữ liệu từ **triệu đến tỷ vector** mà vẫn duy trì thời gian truy vấn ngắn.  
- **Accuracy‑Speed trade‑off** – Tham số như `nlist` (số lượng clusters trong IVF), `m` (số sub‑vector trong PQ), và `efConstruction` trong HNSW cho phép điều chỉnh giữa độ Recall (ví dụ: 1‑recall@1) và thời gian truy vấn.

### 3.5 Đa dạng ứng dụng
Vì Faiss làm việc với bất kỳ vector nào, ta có thể áp dụng nó vào:
- **Hệ thống gợi ý** – tìm các sản phẩm, bài phim, bài viết tương đồng với hành vi người dùng.  
- **Tìm kiếm hình ảnh & video** – mã hóa đặc trưng visual/audio thành vector và tìm kiếm nearest‑neighbor.  
- **Phát hiện bất thường** – xác định những vector nằm xa cụm hàng suggère lỗi, gian lừa, hoặc lỗi chất lượng.  
- **Truy vấn thông tin** – tìm tài liệu có nghĩa gần nhất với truy vấn qua embedding semantics (BERT, Sentence‑Transformers, …).

## 4. Ví dụ minh họa
Dưới đây là cách cài đặt Faiss và một ví dụ đơn giản sử dụng **LangChain**, **OpenAI embeddings** để tạo chỉ mục từ bài viết Wikipedia về “Machine learning” và thực hiện truy vấn nearest‑neighbor.

### 4.1 Cài đặt
```bash
# Phiên bản CPU
pip install faiss-cpu

# Phiên bản GPU (nếu có GPU hỗ trợ CUDA)
pip install faiss-gpu

# Thư viện phụ trợ để làm việc với LangChain và OpenAI
pip install -U langchain-community langchain-openai tiktoken
```

### 4.2 Mã nguồn minh họa
```python
from langchain.document_loaders import WikipediaLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# 1. Tải nội dung từ Wikipedia (bài viết "Machine_learning")
loader = WikipediaLoader("Machine_learning")
document = loader.load()

# 2. Chia tài liệu thành các đoạn (chunk) để có vector có kích thước hợp lý
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(document)

# 3. Khởi tạo mô hình embedding (ở đây là OpenAI)
embeddings = OpenAIEmbeddings()

# 4. Tạo chỉ mục FAISS từ các đoạn văn và embedding tương ứng
db = FAISS.from_documents(docs, embeddings)
print(db.index.ntotal)          # Số vector trong chỉ mục

# 5. Thực hiện truy vấn similarity search
query = "What is machine learning?"
docs = db.similarity_search(query)
print(docs[0].page_content)    # Nội dung đoạn gần nhất với truy vấn
```

#### Giải thích từng bước
1. **WikipediaLoader** tải toàn bộ bài văn bản về *Machine learning*.  
2. **CharacterTextSplitter** chia thành các đoạn có kích thước 1000 ký tự (không chồng lấn) để mỗi đoạn được biểu diễn bằng một vector embedding không quá dài.  
3. **OpenAIEmbeddings** tạo vector biểu diễn (thường là 1536‑dim cho model `text-embedding-3-large`).  
4. `FAISS.from_documents` thực hiện hai việc: (a) biến mỗi đoạn thành vector bằng `embeddings`, (b) xây dựng chỉ mục (mặc định dùng `IndexFlatL2` nếu dữ liệu nhỏ; đối với dữ liệu lớn Faiss sẽ tự động chọn cấu trúc IVF/PQ để tối ưu).  
5. `db.index.ntotal` cho biết số vector đã được index.  
6. `similarity_search` thực hiện tìm nearest‑neighbor theo metric mặc định (L2/Euclidean) và trả về danh sách các đoạn đã được sắp xếp theo độ tương đồng; ta truy xuất nội dung đoạn đầu tiên (`docs[0].page_content`) để xem kết quả.

> **Lưu ý**: Để chạy được ví dụ này, bạn cần có một **API key** hợp lệ của OpenAI và thiết lập biến môi trường `OPENAI_API_KEY` hoặc truyền trực tiếp khi khởi tạo `OpenAIEmbeddings`.

### 4.3 Mở rộng (tùy chọn)
- Thay `IndexFlatL2` bằng `IVFFlat` hoặc `HNSWFlat` để thử nghiệm tốc độ trên tập dữ liệu lớn hơn:
  ```python
  index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
  index.train(vectors)
  index.add(vectors)
  db = FAISS(index, embeddings)
  ```
- Đánh giá độ recall bằng so sánh với tìm kiếm brute‑force trên một tập con nhỏ để chọn tham số `nlist`, `m`, v.v.

## 5. Tổng kết
- Faiss là thư viện mã nguồn mở của Meta AI chuyên về **tìm kiếm và clustering vector mật độ**, cung cấp các thuật toán indexing tiên进 (k‑means, product quantization, OPQ) để đạt được **tốc độ cao, bộ nhớ tối ưu và độ chính xác có thể điều chỉnh**.  
- Nó hỗ trợ nhiều **metric đo lường tương đồng** (Euclidean, cosine, inner‑product) và có thể chạy trên cả **CPU và GPU**, mở rộng hiệu quả từ vài triệu tới hàng tỷ vector.  
- Nhờ tính linh hoạt, Faiss được ứng dụng rộng rãi trong **hệ thống gợi ý**, **tìm kiếm hình ảnh/video**, **phát hiện bất thường**, và **truy vấn thông tin dựa trên ngữ nghĩa**.  
- Ví dụ thực hành với LangChain và OpenAI embeddings cho thấy cách nhanh chóng **tải dữ liệu, tạo vector, xây dựng chỉ mục và thực hiện truy vấn nearest‑neighbor** chỉ trong vài dòng code.  
- Khi làm việc với tập dữ liệu lớn, hãy cân bằng các tham số của IVF/HNSW/PQ để đạt được mức độ recall mong muốn trong giới hạn thời gian và bộ nhớ cho phép.  

Với những kiến thức trên, bạn đã có thể bắt đầu tích hợp Faiss vào các dự án AI cần tìm kiếm tương đồng hiệu quả. Hãy tiếp tục khám phá tài liệu chính thức trên [GitHub Faiss wiki](https://github.com/facebookresearch/faiss/wiki) và các tutorial liên quan để nâng cao kỹ năng áp dụng trong thực tế.