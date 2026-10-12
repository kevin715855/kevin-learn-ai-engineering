# Chroma – Database vector native cho ứng dụng LLM  

## 1. Mục tiêu học tập  

Sau bài học này, bạn sẽ có thể:  

- Giải thích Chroma là gì và tại sao được gọi là *embedding database* cho LLM.  
- Một các thuộc tính chính của Chroma (lưu trữ vector, metadata, tìm kiếm gần nhất, tích hợp LangChain/LlamaIndex).  
- Cài đặt và sử dụng client Python/JS của Chroma để tạo collection, thêm dữ liệu và thực hiện truy vấn vector.  
- Xem qua một số dự án hackathon nổi bật đã ứng dụng Chroma để hiểu cách áp dụng trong thực tiễn.  

## 2. Tổng quan  

Chroma là một **database embedding nguồn mở**, ra mắt năm 2023, được thiết kế riêng để làm “knowledge base” có thể plugs‑in vào các mô hình ngôn ngữ lớn (LLM). Thay vì lưu trữ dữ liệu thô, Chroma giữ các **vector embedding** (biểu diễn số của văn bản, hình ảnh, …) cùng với metadata liên quan, cho phép tìm kiếm nhanh nhất bằng các thuật toán gần nhất (ví dụ: HNSW).  

Với Chroma, nhà phát triển có thể:  

- Lưu trữ kiến thức,事实, kỹ năng dưới dạng vector.  
- Truy xuất các đoạn văn bản hoặc bản ghi most‑relevant để cung cấp context cho LLM (kỹ thuật Retrieval‑Augmented Generation – RAG).  
- Tích hợp dễ dàng với các framework phổ biến như LangChain, LlamaIndex, Streamlit, hoặc trực tiếp qua API Python/JavaScript.  

Ngoài tài liệu chính thức, trang tecnologia Chroma trên lablab.ai còn liệt kê loạt tutorial, danh sách tài nguyên và các dự án hackathon cộng đồng đã xây dựng trên Chroma (ví dụ: TableKeeper, AuraLink, VoiceRAG, MIRROR, Bob Guardian, ReviewSquad).  

## 3. Kiến thức cốt lõi  

### 3.1. Embedding database là gì?  

- **Vector embedding**: biểu diễn số chiều cố định (thường 384‑768) của một đối tượng (câu, đoạn văn, hình ảnh…) được tạo bởi một mô hình embedding (ví dụ: Sentence‑Transformers, OpenAI Ada, BGE‑M3).  
- **Database vector**: lưu trữ các vector này cùng với metadata và cho phép truy vấn dựa trên khoảng cách (cosine similarity, inner product, L2 distance).  

Chroma thực hiện cả hai việc này và bổ sung:  

- **Persistent storage** (lưu trên đĩa) hoặc **in‑memory** cho phát triển nhanh.  
- **Lọc metadata** (where clause) trước khi tính similarity.  
- **HNSW index** (Hierarchical Navigable Small World) để tìm kiếm gần nhất trong sub‑linear time.  
- **API đơn giản**: `Client`, `Collection`, метод `add`, `query`, `get`, `delete`.  

### 3.2. Các thành phần chính  

| Thành phần | Mô tả |
|-----------|-------|
| **Client** | Đối tượng kết nối tới instance Chroma (local hoặc remote). |
| **Collection** | Tương đương một “bảng”: lưu trữ một tập hợp các embeddings cùng metadata. |
| **Embedding Function** | Hàm chuyển đổi raw data → vector. Chroma cung Các hàm sẵn có (default, OpenAI, Sentence‑Transformers) hoặc cho phép tự định nghĩa. |
| **Metadata** | Các cặp key‑value lưu kèm mỗi vector (ví dụ: `source`, `timestamp`, `category`). |
| **Query** | Truyền vector truy vấn + số lượng kết quả mong muốn (`n_results`) và các bộ lọc metadata → trả về danh sách (ids, documents, distances, metadata). |  

### 3.3. Tích hợp với LangChain & LlamaIndex  

- **LangChain**: `Chroma` là một `VectorStore` có thể được truyền vào `RetrievalQA`, `ConversationalRetrievalChain`, …  
- **LlamaIndex**: `ChromaVectorStore` cho phép xây dựng chỉ mục và thực hiện truy vấn trong pipeline `QueryEngine`.  

Các liên kết tài liệu được liệt kê trong phần “Helpful Resources” của nguồn.  

## 4. Ví dụ minh họa  

Dưới đây là một **minimal example** bằng Python showcasing cách:  

1. Khởi tạo client Chroma (persistent thư mục `./chroma_db`).  
2. Tạo một collection tên `demo_docs` với embedding function mặc định (Sentence‑Transformers `all-MiniLM-L6-v2`).  
3. Thêm ba đoạn văn bản cùng metadata.  
4. Thực hiện truy vấn vector để lấy hai đoạn paling gần với câu hỏi *"What is Chroma?"*  

```python
# pip install chromadb sentence-transformers
import chromadb
from chromadb.utils import embedding_functions

# 1. Khởi tạo client (lưu dữ liệu trên đĩa)
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Định dạng embedding function (mặc định dùng MiniLM)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Tạo hoặc lấy collection
collection = client.get_or_create_collection(
    name="demo_docs",
    embedding_function=ef,
    metadata={"hnsw:space": "cosine"}  # sử dụng cosine similarity
)

# 4. Thêm tài liệu
docs = [
    "Chroma là một embedding database nguồn mở cho LLM.",
    "Chroma giúp kiến thức trở thành plug‑in cho các mô hình ngôn ngữ lớn.",
    "Bạn có thể truy xuất các đoạn văn bản liên quan bằng cách tìm kiếm vector."
]
metadatas = [
    {"source": "intro", "topic": "overview"},
    {"source": "feature", "topic": "capability"},
    {"source": "usage", "topic": "query"}
]
ids = ["doc1", "doc2", "doc3"]

collection.add(
    documents=docs,
    metadatas=metadatas,
    ids=ids
)

# 5. Truy vấn vector
query_text = "What is Chroma?"
results = collection.query(
    query_texts=[query_text],
    n_results=2,               # lấy 2 kết quả tốt nhất
    where=None                 # không có bộ lọc metadata trong ví dụ này
)

print("Kết quả truy vấn:")
for idx, doc in enumerate(results["documents"][0]):
    print(f"{idx+1}. {doc} (distance: {results['distances'][0][idx]:.4f})")
    print(f"   Metadata: {results['metadatas'][0][idx]}")
```

**Kết quả mong muốn** (giả sử distances nhỏ):  

```
Kết quả truy vấn:
1. Chroma là một embedding database nguồn mở cho LLM. (distance: 0.12)
   Metadata: {'source': 'intro', 'topic': 'overview'}
2. Chroma giúp kiến thức trở thành plug‑in cho các mô hình ngôn ngữ lớn. (distance: 0.18)
   Metadata: {'source': 'feature', 'topic': 'capability'}
```

> **Lưu ý:**  
> - Nếu chưa có mô hình `sentence-transformers` được cài đặt, lệnh `pip install sentence-transformers` sẽ tải về mô hình mặc định.  
> - Thay đổi `embedding_function` sang một API external (OpenAI, Cohere…) chỉ cần truyền соответствующий `EmbeddingFunction` khi tạo collection.  

### 4.1. Ví dụ tích hợp LangChain (Python)  

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI   # hoặc bất kỳ LLM nào compatible

embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding,
    collection_name="demo_docs"
)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

answer = qa.run("What is Chroma?")
print(answer)
```

Các ví dụ trên chỉ cho thấy cách **đưa Chroma vào luồng RAG**: lưu trữ vector, truy vấnContext, và đưa kết quả vào LLM để sinh câu trả lời.  

## 5. Tổng kết  

- Chroma là một **embedding database nguồn mở** (2023) chuyên biệt cho việc lưu trữ và tìm kiếm vector, cho phép kiến thức trở thành *plug‑in* cho LLM.  
- Các tính năng核心: persistent storage, metadata filtering, HNSW index, API đơn giản (Python/JS), và tích hợp sẵn với LangChain, LlamaIndex.  
- Quy trình làm việc típ: tạo collection → thêm documents (kèm metadata và embeddings) → truy vấn vector → lấy context → đưa vào LLM (RAG).  
- Cộng đồng đã chứng minh sức mạnh của Chroma qua nhiều dự án hackathon (TableKeeper, AuraLink, VoiceRAG, MIRROR, Bob Guardian, ReviewSquad), thể hiện cách áp dụng trong các trường hợp quản lý bàn ăn, hỗ trợ người khiếm thị, hệ thống hỏi‑答 voix, tự động hoá workflow, và審查 code.  

Với kiến thức trên, bạn có thể bắt đầu xây dựng ứng dụng LLM có thể truy xuất conhecimento thực thời bằng Chroma, và khám phá sâu hơn qua các tutorial và tài nguyên đã được liệt kê trong phần “Helpful Resources”. Happy building!