# Nhúng (Embeddings) trong Machine Learning

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ có thể:

- Định nghĩa vector và embedding trong bối cảnh học máy.  
- Giải thích cách các vector cho phép thực hiện tìm kiếm tương đồng.  
- Mô tả quá trình tạo embedding bằng mô hình học sâu (deep learning).  

## 2. Tổng quan

Embedding là phương pháp biến đổi các đối tượng thực tế (văn bản, hình ảnh, âm thanh, video…) thành dạng số học – thường là một **vector** – để máy tính có thể xử lý. Khi các đối tượng được biểu diễn dưới dạng vector nằm trong một không gian đa chiều, các đối tượng có tính chất tương đồng sẽ nằm gần nhau. Nhờ tính chất này, embeddings trở thành nền tảng cho nhiều ứng dụng AI như tìm kiếm ngữ nghĩa, hệ thống đề xuất và các mô hình ngôn ngữ lớn (LLM).

## 3. Kiến thức cốt lõi

### 3.1 Vector là gì?

- Trong toán học, vector là một mảng số xác định vị trí của một điểm trong không gian đa chiều.  
- Ví dụ đơn giản: tọa độ kinh độ và vĩ độ của một thành phố là vector 2 chiều `{lat, lon}`.  
- Trong học máy, mỗi thành phần của vector phản hồi một **triệu chứng** (dimension) cụ thể của đối tượng (ví dụ: loại phim, năm ra mắt, tập số…).

### 3.2 Tìm kiếm tương đồng bằng vector

- Khi các đối tượng được chuyển thành vector, việc tìm kiếm đối tượng tương đương trở thành việc tìm các vector có khoảng cách nhỏ trong không gian vector.  
- Các thuật toán thường dùng là **cosine similarity**, **Euclidean distance**, hoặc tìm kiếm gần nhất (k‑NN) trong **vector database**.  

### 3.3 Cách tạo embedding

- Embedding được sinh ra bởi một lớp ẩn (hidden layer) trong một mạng neural (deep learning).  
- Lớp này tự động học cách ánh xạ đầu vào (từ, ảnh,…) thành vector sao cho các đặc trưng quan trọng được giữ lại.  
- Quá trình huấn luyện không yêu cầu người dùng chỉ định thủ công từng chiều; mạng học sendiri các chiều dựa trên dữ liệu đầu vào.  

### 3.4 Embedding trong mô hình ngôn ngữ lớn (LLM)

- LLM không chỉ embedding mỗi từ riêng lẻ mà còn embedding **bối cảnh** của từ (các từ xung quanh).  
- Nhờ đó, mô hình có thể理解 ý nghĩa của câu, đoạn hoặc bài viết hoàn chỉnh, từ đó thực hiện các tác vụ như tạo văn bản, trả lời câu hỏi, hoặc tìm kiếm ngữ nghĩa.  
- Việc lưu trữ các embedding của bối cảnh giúp giảm thời gian tính toán cho các truy vấn lặp lại.  

## 4. Ví dụ minh họa

### 4.1 Vector đơn giản – Tọa độ thành phố

| Thành phố | Vĩ độ (lat) | Kinh độ (lon) |
|-----------|------------|---------------|
| Vancouver | 49°15'40"N | 123°06'50"W |
| Burnaby   | 49°16'N    | 122°58'W      |
| Seattle   | 47°36'35"N | 122°19'59"W   |

- Vector Vancouver: `{49.2611, -123.1139}`  
- Vector Burnaby: `{49.2667, -122.9667}` → rất gần Vancouver (tương tự về vị trí).  
- Nếu thêm chiều **dân số** (population) thì vector thành `{lat, lon, population}` và Burnaby sẽ xa hơn vì dân số khác biệt lớn.

### 4.2 Vector đa chiều – Phim episodi

Chúng ta mô tả một bộ phim bằng 5 chiều: thể loại, năm ra mắt, độ dài tập, số mùa, số tập.

| phim          | thể loại | năm ra mắt | độ dài tập (phút) | số mùa | số tập |
|---------------|----------|------------|-------------------|--------|--------|
| Seinfeld      | Sitcom   | 1989       | 22‑24             | 9      | 180    |
| Wednesday     | Horror   | 2022       | 46‑57             | 1      | 8      |
| Cheers        | Sitcom   | 1982       | 21‑25             | 11     | 275    |

- Vector Seinfeld: `[Sitcom, 1989, 22‑24, 9, 180]`  
- Vector Wednesday: `[Horror, 2022, 46‑57, 1, 8]`  
- Vector Cheers: `[Sitcom, 1982, 21‑25, 11, 275]`  

Khi so sánh các vector này (ví dụ bằng cosine similarity), Seinfeld và Cheers có giá trị gần nhau hơn vì chúng cùng thể loại, năm ra mắt gần và độ dài tập tương tự, trong khi Wednesday nằm xa hơn.

### 4.3 Minh họa quá trình tạo embedding (giả lập code Python)

```python
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, GlobalAveragePooling1D

# Giả sử chúng ta có một bộ dữ liệu từ có chỉ số từ 0..vocab_size-1
vocab_size = 10000
embed_dim   = 128   # số chiều embedding

input_seq   = Input(shape=(None,), name='tokens')
x           = Embedding(input_dim=vocab_size,
                        output_dim=embed_dim,
                        name='token_embedding')(input_seq)
x           = GlobalAveragePooling1D()(x)   # trung bình các token → vector 문장
output      = Dense(64, activation='relu')(x)

model       = Model(inputs=input_seq, outputs=output)
model.summary()

# Sau khi huấn luyện, lớp 'token_embedding' là ma trận embedding
embedding_matrix = model.get_layer('token_embedding').get_weights()[0]
print("Shape of embedding matrix:", embedding_matrix.shape)  # (vocab_size, embed_dim)
```

- Lớp `Embedding` học **ma trận embedding** sao cho các từ có nghĩa gần nhau có vector gần nhau trong không gian 128‑chiều.  
- Sau huấn luyện, chúng ta có thể truy xuất vector của bất kỳ từ nào và sử dụng chúng cho tìm kiếm tương đồng hoặc làm đầu vào cho các lớp tiefer trong mạng.

## 5. Tổng kết

- Embedding là vector số học biểu diễn đối tượng thực tế, cho phép máy tính hiểu mối quan hệ và thực hiện tìm kiếm tương đồng.  
- Vector được định nghĩa bằng một loạt các chiều (triệu chứng), mỗi chiều phản hồi một đặc trưng cụ thể của đối tượng.  
- Embedding được tạo tự động bởi lớp ẩn trong mạng neural, không cần chỉ định thủ công từng chiều.  
- Trong LLM, embedding được mở rộng để bao gồm bối cảnh từ, giúp mô hình hiểu ý nghĩa cấp câu và đoạn.  
- Việc lưu trữ và truy vấn embedding trong **vector database** làm cho các ứng dụng AI trở nên nhanh chóng, tiết kiệm chi phí và dễ triển khai (ví dụ qua Cloudflare Workers AI + Vectorize).  

Những khái niệm trên là nền tảng để bạn hiểu và áp dụng embedding vào các dự án Machine Learning và AI thực tiễn.