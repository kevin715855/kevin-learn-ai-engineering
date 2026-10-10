# Similarity Search – Nguyên lý và ứng dụng

## 1. Mục tiêu học tập
Sau bài học này, người học sẽ能够:
- Giải thích khái niệm similarity search và vai trò của vector embeddings.
- Mô tả các cách biểu diễn dữ liệu dưới dạng vector (Word2Vec, GLoVE, Universal Sentence Encoder, CNN).
- Định nghĩa và so sánh các khoảng cách thường dùng: Euclidean, Manhattan, Cosine similarity, Chebyshev.
- Nguyên lý hoạt động của hai thuật toán tìm kiếm láng giềng gần nhất: k‑NN và Approximate Nearest Neighbor (ANN) cùng với các kỹ thuật indexes (KD‑Tree, Ball Tree, VP‑Tree, LSH, k‑means).
- Liệt kê các ứng dụng thực tiễn của similarity search trong hệ thống gợi ý, truy xuất hình ảnh/video, xử lý ngôn ngữ tự nhiên, phát hiện gian lận và y tế.
- Nhận ra thách thức về truy vấn mơ hồ và vấn đề mở rộng quy mô (scalability) khi làm việc với tập dữ liệu lớn.

## 2. Tổng quan
Trong thời đại dữ liệu lớn, việc tìm các mục tương tự nhau trong khối lượng thông tin khổng lesso trở thành một thao tác cơ bản. Similarity search (tìm kiếm similarity) cho phép hệ thống đo lường mức độ gần gũi giữa các đối tượng dựa trên ý nghĩa ngữ nghĩa thay vì chỉ so sánh từ khóa hoặc giá trị cụ thể. Quá trình này bao gồm ba bước chính:
1. **Biến đổi đối tượng thực tế thành vector embedding** – một danh sách số liên tục biểu diễn đặc trưng sâu sắc.
2. **Tính khoảng cách giữa các vector** bằng một **distance metric** (Euclidean, Manhattan, Cosine, Chebyshev …).
3. **Chọn ra các vector có khoảng cách nhỏ nhất** (k‑NN) hoặc một ước lượng nhanh (ANN) để trả về kết quả tương tự.

## 3. Kiến thức cốt lõi

### 3.1 Vector Representations (Biểu diễn vector)
- **Vector embedding** là các số liên tục được học từ mô hình trên dữ liệu lớn, nắm bắt ý nghĩa ngữ nghĩa của từ, câu, hình ảnh …
- Các mô hình phổ biến:
  - **Word2Vec** – biến đổi từ thành vector, nắm quan hệ ngữ nghĩa giữa các từ.
  - **GLoVE (Global Vectors for Word Representation)** – dựa trên thống kê toàn cầu của từ trong corpus.
  - **Universal Sentence Encoder (USE)** – tạo embedding cho whole sentence, phản ánh nghĩa của câu.
  - **CNN như VGG** – sinh embedding cho hình ảnh, phản ánh đặc trưng 시각.

### 3.2 Distance Metrics (Chỉ số khoảng cách)
|Metric|Công thức / Ý tưởng|Khi nào dùng|Ưu điểm|Nhược điểm|
|---|---|---|---|---|
|**Euclidean**|√Σ(xᵢ‑yᵢ)²|Dữ liệu dense, liên tục, khi khoảng cách hình học có ý nghĩa|Đơn giản, dễ giải thích|Hiệu suất giảm ở không gian rất cao (curse of dimensionality)|
|**Manhattan (L1)**|Σ|xᵢ‑yᵢ|Dữ liệu dạng lưới, di chuyển theo hướng nghiêng – orthogonal|Kháng outliers tốt hơn Euclidean trong một số trường hợp|K пря̀n tới việc chuẩn hoá đặc trưng, không trực quan cho dữ liệu phi‑lưới|
|**Cosine similarity**|cosθ = (A·B) / (‖A‖‖B‖)|Dữ liệu text高维稀疏, quan tâm tới hướng vector hơn độ lớn|Không phụ thuộc vào độ lớn vector, tốt với text|Cần chuẩn hoá nếu độ lớn mang thông tin|
|**Chebyshev**|maxᵢ|xᵢ‑yᵢ|Bàn cờ, robot di chuyển trong lưới cho phép đi chéo|Đơn giản tính toán|Thông dụng thấp trong dữ liệu tự nhiên, không trực quan cho liên tục|

Lựa chọn metric phụ thuộc vào đặc trưng dữ liệu và yêu cầu ứng dụng (ví dụ: Euclidean cho ảnh, Cosine cho văn bản).

### 3.3 Thuật toán tìm kiếm láng giềng gần nhất
- **k‑Nearest Neighbors (k‑NN)**  
  - Tính khoảng cách từ vector truy vấn tới **mọi** vector trong tập dữ liệu, sắp xếp và lấy **k** phần tử nhỏ nhất.  
  - Ưu điểm: triển khai dễ, không cần huấn luyện mô hình.  
  - Nhược điểm: chi phí O(N) mỗi truy vấn → không phù hợp với dữ liệu lớn.  
  - Trường hợp dùng: tập dữ liệu nhỏ, cần kết quả Exact NN (ví dụ: hệ thống gợi ý cho nhóm người dùng hạn chế).

- **Approximate Nearest Neighbor (ANN)**  
  - Trao đổi một phần độ chính xác để đạt tốc độ cao trên dữ liệu tỷ lệ tỉ.  
  - Các kỹ thuật chỉ số (index):
    - **KD‑Tree, Ball Tree, VP‑Tree** – chia không gian vector thành các vùng để loại bỏ những vùng không cần tìm.  
    - **Locality‑Sensitive Hashing (LSH)** – mã hoá vector sao cho các vector tương tự có khả năng rơi vào cùng một bucket.  
    - **k‑means clustering** – vector được gom thành cụm; tìm kiếm chỉ trong cụm gần truy vấn nhất.  
  - Ưu điểm: tốc độ rất nhanh, mở rộng được tới tỉ vector.  
  - Nhược điểm: kết quả là *ước lượng* – có thể bỏ qua một vài láng giềng thực sự closest.  
  - Trường hợp dùng: công cụ tìm kiếm web, hệ thống gợi ý lớn, truy vấn thời gian thực.

### 3.4 Thư viện hỗ trợ thực tiễn
- **FAISS** (Facebook AI Similarity Search) – tối ưu cho GPU/CPU, tìm kiếm nhanh trên billions of vectors.  
- **Annoy** (Approximate Nearest Neighbors Oh Yeah) – C++ với binding Python, tiêu thụ bộ nhớ thấp, tìm kiếm nhanh.  
- **HNSWlib** – triển khai Hierarchical Navigable Small World graphs, cung cấp trade‑off tốt giữa tốc độ và recall.

## 4. Ví dụ minh họa
Giả sử chúng ta có một bộ dữ liệu sản phẩm điện tử, mỗi sản phẩm được mô tả bằng tiêu đề ngắn. Các bước thực hiện similarity search để gợi ý sản phẩm tương tự:

1. **Chuyển đổi tiêu đề thành vector** bằng Universal Sentence Encoder → mỗi tiêu đề thành vector 512‑dimension.
2. **Chọn metric**: vì là text, dùng Cosine similarity.
3. **Xây dựng chỉ số** với FAISS (IndexFlatIP để tìm inner product, tương đương Cosine khi vector đã chuẩn hoá).
4. **Truy vấn**: khi người dùng xem sản phẩm “Tai nghe Bluetooth XYZ”, ta chuyển tiêu đề này thành vector và truy vấn chỉ số để lấy k=5 vector có Cosine similarity cao nhất.
5. **Trả về** 5 sản phẩm có tiêu đề gần nhất trong không gian embedding → những sản phẩm có tính năng, thương hiệu, hoặc mức giá tương tự.

Nếu tập dữ liệu lớn (>10 triệu sản phẩm), thay vì IndexFlatIP ta có thể dùng **IndexIVFFlat** (phiên bản quantized của FAISS) hoặc **HNSW** để giảm thời gian truy vấn còn dưới 10ms mà vẫn giữ recall ở mức 90%+.

## 5. Tổng kết
- Similarity search dựa trên **vector embedding** để biểu diễn ý nghĩa ngữ nghĩa của đối tượng.
- **Distance metric** quyết định cách đo lường sự tương đồng; việc lựa chọn phù hợp phụ thuộc vào loại dữ liệu và mục tiêu ứng dụng.
- **k‑NN** cung cấp kết quả chính xác nhưng tốn kém khi dữ liệu lớn; **ANN** (KD‑Tree, LSH, HNSW…) cung cấp trade‑off tốc độ‑chính xác thích hợp với hệ thống sản xuất.
- Công cụ như **FAISS, Annoy, HNSWlib** giúp triển khai hiệu quả trong thực tế.
- Ứng dụng rộng: hệ thống gợi ý, truy xuất hình ảnh/video, NLP (tìm kiếm ngữ nghĩa, phân loại văn bản), phát hiện gian lận, y tế và genomics.
- Thách thức chính bao gồm **xử lý truy vấn mơ hồ** (từ chung tới cụ thể) và **scalability** khi làm việc với billions of vectors; việc chọn metric và chỉ số ANN là chìa khóa để vượt qua.

Với những kiến thức trên, người học có thể bắt đầu xây dựng hệ thống similarity search thực tế, chọn mô hình embedding, metric và thuật toán tìm kiếm phù hợp với bài toán cụ thể của mình.