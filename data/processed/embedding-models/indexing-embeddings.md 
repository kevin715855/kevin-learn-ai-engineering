# Indexing trong LlamaIndex  

## 1. Mục tiêu học tập  

- Hiểu **Index** là gì và vai trò của nó trong pipeline RAG.  
- Biết cách hoạt động của **Vector Store Index** và **Summary Index**.  
- Giải thích khái niệm **vector embedding** và lý do embedding cho phép semantic search.  
- Nắm được cách thực hiện top‑k retrieval và cách cấu hình `top_k`.  
- S능 dụng `VectorStoreIndex.from_documents` và `VectorStoreIndex(nodes)` để tạo index.  
- Nhận ra khi cần lưu trữ embedding để tiết kiệm thời gian và chi phí.  

## 2. Tổng quan  

Sau khi tài liệu đã được **load** và chuyển thành danh sách `Document` (hoặc `Node`), ta cần xây dựng một **Index** để mô hình ngôn ngữ lớn (LLM) có thể truy vấn hiệu quả.  
Index là cấu trúc dữ liệu lưu trữ thông tin về các đoạn văn (hoặc node) dưới dạng mà LLM có thể truy xuất nhanh, thường là các vector embedding.  

LlamaIndex cung cấp nhiều loại index; trong bài này chúng ta tập trung vào hai loại phổ biến nhất: **Vector Store Index** và **Summary Index**.  

## 3. Kiến thức cốt lõi  

### 3.1 Index là gì?  

- Một `Index` là một bộ sưu tập các đối tượng `Document` (hoặc `Node`) được tổ chức để **hỗ trợ truy vấn** bởi LLM.  
- Nó được thiết kế để **bù đắp** chiến lược truy vấn của bạn: tùy thuộc vào loại index, quá trình truy xuất sẽ khác nhau (ví dụ: tìm kiếm semantic vs trả về toàn bộ tài liệu).  

### 3.2 Vector Store Index  

#### 3.2.1 Quy trình hoạt động  

1. **Chia tài liệu thành Node** – mỗi node là một đoạn văn ngắn (thường là một câu hoặc một đoạn).  
2. **Tạo vector embedding** cho mỗi node bằng một mô hình embedding (ví dụ: `text-embedding-3-small` hoặc một mô hình HuggingFace).  
3. **Lưu trữ các vector embedding** trong một vector store (có thể là bộ nhớ trong‑memory, FAISS, Pinecone, …).  
4. Khi có một **query**, LLM cũng sẽ được chuyển thành embedding tương tự.  
5. Thực hiện phép toán toán học (thường là cosine similarity) để **xếp hạng** các node theo độ tương đồng semantic với query.  
6. Trả về **top‑k** node có độ tương đồng cao nhất.  

#### 3.2.2 Vector embedding  

- Embedding là **biểu diễn số học** của ý nghĩa (semantics) của một đoạn văn.  
- Hai đoạn văn có ý nghĩa gần nhau sẽ có embedding gần nhau trong không gian vector, dù chuỗi ký tự có thể rất khác.  
- Tính chất này cho phép **semantic search**: tìm kiếm dựa trên ý nghĩa thay vì khớp từ khóaExact.  

#### 3.2.3 Top‑k Retrieval  

- Sau khi tính độ similarity, index trả về **k** node có điểm số cao nhất.  
- Tham số `top_k` (hay `k`) kiểm soát số lượng kết quả trả về.  
- Đây là hình thức truy vấn đơn giản nhất trên vector index; các chiến lược phức tạp hơn (hybrid search, reranking…) được mô tả trong phần **querying**.  

#### 3.2.4 Cách sử dụng Vector Store Index  

```python
from llama_index.core import VectorStoreIndex

# Xây dựng từ danh sách Document
index = VectorStoreIndex.from_documents(documents)

# Hoặc trực tiếp từ danh sách Node (nếu bạn đã có nodes)
index = VectorStoreIndex(nodes)
```

- Sau khi index được tạo, nó đã **sẵn sàng** cho bước truy vấn (`querying`).  
- Tuy nhiên, việc tạo embedding có thể tốn thời gian và chi phí nếu dùng API hosted. Do đó, thường bạn sẽ **lưu trữ** embedding (vector store) trước để tái sử dụng.  

### 3.3 Summary Index  

- Loại index đơn giản nhất: **chỉ lưu trữ** toàn bộ các Document (hoặc Node) và trả về **全部** chúng khi có truy vấn.  
- Phù hợp khi mục tiêu là **tóm tắt** toàn bộ nội dung (ví dụ: tạo bản tóm tắt tài liệu).  
- Không thực hiện bất kỳ bước ranking hoặc embedding nào; do đó nhanh nhưng không cung cấp khả năng tìm kiếm semantic.  

### 3.4 Lưu trữ embedding (đọc thêm)  

- Để tiết kiệm thời gian và chi phí, bạn có thể lưu trữ các vector embedding vào một **vector store** ngoài (FAISS, Milvus, Pinecone, …) và sau đó chỉ cần load lại khi cần truy vấn.  
- LlamaIndex cung cấp các module hướng dẫn lưu trữ và tải lại embedding trong phần **[Storing embeddings](https://developers.llamaindex.ai/python/framework/understanding/rag/storing/)**.  

## 4. Ví dụ minh họa  

Giả sử chúng ta đã có danh sách `documents` sau khi đọc file PDF:  

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. Đọc tài liệu
documents = SimpleDirectoryReader("./data").load_data()

# 2. Tạo Vector Store Index
index = VectorStoreIndex.from_documents(documents)

# 3. Truy vấn đơn giản (top_k = 3)
query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("Cho tôi biết về cách hoạt động của embedding trong LlamaIndex")
print(response)
```

**Giải thích kết quả**  

- Bước 1: Tải tất cả file trong thư mục `data` thành danh sách `Document`.  
- Bước 2: `VectorStoreIndex.from_documents` tự động chia mỗi document thành nodes, tạo embedding cho mỗi node bằng mô hình mặc định (`text-embedding-ada-002`) và lưu trữ chúng trong vector store nội bộ.  
- Bước 3: Khi gọi `query_engine.query`, câu hỏi cũng được chuyển thành embedding, hệ thống tính độ similarity với tất cả node embedding, sắp xếp và trả về 3 node có độ similarity cao nhất (top‑k = 3).  
- Kết quả `response` sẽ là một chuỗi văn bản được tổng hợp từ những đoạn text tương ứng với 3 node đó, được LLM tạo ra dựa trên ngữ cảnh đã truy xuất.  

Nếu bạn muốn sử dụng **Summary Index** thay vì Vector Store Index:  

```python
from llama_index.core import SummaryIndex

summary_index = SummaryIndex.from_documents(documents)
# Truy vấn sẽ trả về toàn bộ documents
response = summary_index.as_query_engine().query("Tóm tắt tài liệu")
print(response)
```

Trong trường hợp này, bất kỳ truy vấn nào cũng sẽ khiến index trả về **tất cả** các document, cho phép bạn thực hiện tóm tắt hoặc các hoạt động cần toàn bộ bản ngữ.  

## 5. Tổng kết  

- **Index** là cấu trúc dữ liệu cho phép LLM truy xuất thông tin từ tài liệu đã load; hai loại phổ biến là **Vector Store Index** (dùng embedding và semantic search) và **Summary Index** (trả về toàn bộ tài liệu).  
- Vector Store Index hoạt động bằng cách chia tài liệu thành nodes, tạo **vector embedding** cho mỗi node, rồi thực hiện **top‑k semantic retrieval** dựa trên độ similarity cosine.  
- Embedding là biểu diễn số học của ý nghĩa; sự tương đồng trong không gian vector phản ánh ý nghĩa tương đồng trong văn bản, cho phép tìm kiếm sémantic mạnh mẽ hơn so với tìm kiếm từ khóa.  
- Tham số `top_k` kiểm soát số lượng kết quả trả về; mặc định thường là 1 hoặc có thể được đặt tùy ý.  
- Tạo index có thể tốn thời gian và chi phí; vì vậy nên **lưu trữ embedding** vào vector store ngoài để tái sử dụng.  
- Khi index đã sẵn sàng, bạn có thể ngay lập tức chuyển sang fase **querying** để nhận câu trả lời từ LLM dựa trên các đoạn văn bản đã được truy xuất.  

Bằng cách nắm vững các概念 trên, bạn sẽ能够构建高效的 RAG pipeline，利用 LlamaIndex 的索引功能实现语义检索和增强生成。祝学习愉快！