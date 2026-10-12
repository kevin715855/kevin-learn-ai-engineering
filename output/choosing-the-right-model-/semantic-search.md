# Semantic Search

## 1. Mục tiêu học tập

Sau bài học này, người học sẽ:

- Hiểu ý nghĩa của semantic search và cách nó khác với keyword search.
- Giải thích cách hoạt động của semantic search dựa trên vector search và kNN.
- Nhận biết vai trò của context và searcher intent trong việc cải thiện kết quả tìm kiếm.
- Đưa ra các ví dụ thực tế về semantic search trong ứng dụng.
- Liệt kê lợi ích mà semantic search mang lại cho người dùng và doanh nghiệp.
- Nắm được cách triển khai semantic search trong Elasticsearch (ELSER).

## 2. Tổng quan

Semantic search là công nghệ tìm kiếm thông qua việc hiểu **nghĩa** của từ và cụm từ thay vì chỉ so sánh từ khóa literal. Nó kết hợp machine learning, artificial intelligence và vector search để đánh giá mức độ liên quan dựa trên ý định tìm kiếm (intent) và ngữ cảnh (context) của người dùng. Kết quả là trải nghiệm tìm kiếm gần似 với sự hiểu biết của con người, mang lại độ chính xác và sự phù hợp cao hơn.

## 3. Kiến thức cốt lõi

### 3.1 Định nghĩa

Semantic search là tập hợp các khả năng của công cụ tìm kiếm cho phép:

- Hiểu ý nghĩa của từ dựa trên ý định và ngữ cảnh của người dùng.
- Trả về nội dung khớp với **nghĩa** của truy vấn, không chỉ với từ khóa trùng khớp.

### 3.2 Nguyên lý hoạt động

Semantic search dựa trên **vector search**. Quy trình chính bao gồm các bước sau:

1. **Biến truy vấn thành embedding**  
   Khi người dùng gửi truy vấn, hệ thống biến nó thành một vector số (embedding) biểu diễn nghĩa và ngữ cảnh của từ.

2. **So sánh vector với kNN**  
   Thuật toán k‑nearest neighbor (kNN) so sánh vector truy vấn với các vector của tài liệu đã được lưu trữ, tìm ra những vector gần nhất (tức là có ý nghĩa gần giống nhất).

3. **Sắp xếp kết quả theo độ liên quan khái niệm**  
   Kết quả được xếp hạng dựa trên mức độ tương đồng ý nghĩa (conceptual relevance), không chỉ dựa trên sự trùng khớp từ khóa.

### 3.3 Context

Context bao gồm bất kỳ thông tin phụ trợ nào giúp xác định nghĩa của từ, ví dụ:

- Vị trí địa lý của người dùng (ví dụ: “football” 의미 soccer ở Mỹ, nhưng football ở Anh).
- Ngữ cảnh văn bản của từ trong truy vấn.
- Lịch sử tìm kiếm trước đó của người dùng.

Semantic search sử dụng các dấu hiệu context này để suy ra nghĩa đúng trong một tập dữ liệu lớn.

### 3.4 Searcher Intent

Intent là mục đích phía sau truy vấn của người dùng (thông tin, mua s물, navigational, transactional). Bằng cách phân tích intent, hệ thống có thể:

- Xếp hạng kết quả sao cho phù hợp với nhu cầu thực tế (ví dụ: ưu tiên sản phẩm có評分 cao khi intent là mua sắm).
- Tùy chỉnh kết quả dựa trên các cài đặt phân loại truy vấn (query categorization).

### 3.5 So sánh với Keyword Search

| Khía cạnh | Keyword Search | Semantic Search |
|----------|----------------|-----------------|
| Nguyên lý | Trả về kết quả trùng khớp từ khóa, từ đồng từ, hoặc từ tương tự. | Trả về kết quả khớp với **nghĩa** của truy vấn, dù không обязательно trùng khớp từ khóa. |
| Công cụ hỗ trợ | Query expansion, synonym, typo tolerance, tokenization, normalization. | Vector search, embeddings, kNN. |
| Ví dụ | “chocolate milk” và “milk chocolate” có thể được coi như cùng vì cùng từ khóa. | Hệ thống phân biệt vì thứ tự từ thay đổi nghĩa: “chocolate milk” = sữa có hương socola; “milk chocolate” = loại socola chứa sữa. |

### 3.6 Lợi ích

- **Dễ sử dụng cho khách hàng**: Khách hàng có thể nhập truy vấn mơ tả (lời bài hát, mô tả sản phẩm) và vẫn nhận được kết quả cụ thể.
- **Khái niệm vững chắc hơn từ khóa**: Vector biểu diễn từ như một khái niệm trong không gian đa chiều, cho phép liên kết từ với các từ có liên quan概念 (ví dụ: “car” cũng liên quan tới “driver”, “insurance”, “tires”, “electric”, …).
- **Tốt cho doanh nghiệp**: Hiểu intent giúp tăng conversion, giảm bounce rate, nâng cao sự hài lòng và lòng trung khách.

### 3.7 Triển khai trong Elasticsearch

Elasticsearch cung cấp mô hình **Elastic Learned Sparse EncodeR (ELSER)**, một NLP model zero‑shot được đào tạo sẵn để thực hiện semantic search mà không cần thêm training. ELSER hoạt động như một encoder tạo ra embeddings稀疏, cho phép tìm kiếm vector hiệu quả và dễ triển khai trong các ứng dụng AI search hoặc generative AI.

## 4. Ví dụ minh họa

### 4.1 Phân biệt “football” theo vị trí

- Người dùng ở Mỹ gõ “football” → hệ thống trả về kết quả về bóng đá ameryka (soccer).
- Người dùng ở Anh gõ cùng truy vấn → kết quả về bóng đá estilo Anh (rugby-style football).  
Điều này minh họa việc sử dụng **context** (vị trí địa lý) để suy ra nghĩa đúng.

### 4.2 “Chocolate milk” vs “Milk chocolate”

- Truy vấn “chocolate milk”: ý định là tìm đồ uống sữa có hương socola → kết quả về các loại sữa socola.
- Truy vấn “milk chocolate”: ý định là tìm loại socola chứa sữa → kết quả về thanh socola sữa.  
Mặc dù hai truy vấn chứa cùng bộ từ, thứ tự từ thay đổi ý nghĩa, và semantic search có thể phân biệt nhờ理解 câu trúc và context.

### 4.3 Truy vấn sản phẩm so sánh

- “Creuset vs. Staub dutch ovens”: hệ thống nhận diện intent là so sánh sản phẩm → ưu tiên bài viết, videoreview, bảng so sánh.
- “Best Staub deals” hoặc “Creuset discounts”: intent là mua sắm → ưu tiên trang bán hàng, mã giảm giá, sản phẩm khuyến mãi.

### 4.4 Predictive text (gợi ý tự động)

Khi người dùng bắt đầu gõ một từ trong ô tìm kiếm, hệ thống dựa trên:

- Lịch sử tìm kiếm cá nhân.
- Xu hướng tìm kiếm phổ biến.
- Context từ câu đang gõ.

→ đề xuất các hoàn thành truy vấn có khả năng phù hợp, giảm thời gian gõ và tăng tỉ lệ tìm thấy kết quả mong muốn.

## 5. Tổng kết

Semantic search nâng cao chất lượng tìm kiếm bằng cách:

- Biểu diễn từ và câu sebagai **vector embedding** thông qua machine learning.
- So sánh vector bằng **kNN** để tìm các tài liệu có ý nghĩa gần nhất.
- Tận dụng **context** (vị trí, lịch sử, ngữ cảnh văn bản) và **searcher intent** để xếp hạng kết quả phù hợp với nhu cầu thực tế.
- Khắc phục hạn chế của keyword search khi từ đồng dạng có nghĩa khác nhau tùy theo thứ tự hoặc ngữ cảnh.
- Mang lại lợi ích thực dụng: trải nghiệm người dùng tốt hơn, tăng conversion và satisfaction, hỗ trợ các tính năng như personalized search và predictive text.

Trong hệ thống Elasticsearch, mô hình **ELSER** cung cấp một cách đơn giản, không cần training thêm để áp dụng semantic search ngay trong các ứng dụng AI search và generative AI. Việc hiểu rõ các thành phần trên sẽ giúp người học thiết kế và tối ưu hóa hệ thống tìm kiếm phù hợp với mục tiêu kinh doanh và trải nghiệm người dùng.