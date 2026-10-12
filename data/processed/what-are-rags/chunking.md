# RecursiveCharacterTextSplitter – Phân đoạn tài liệu dài cho mô hình ngôn ngữ lớn

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ có thể:

- Giải thích tại sao mô hình ngôn ngữ lớn (LLM) cần phải xử lý văn bản trong một “cửa sổ context” có giới hạn.  
- Mô tả cách “chunking” giúp vượt qua giới hạn này bằng cách chia tài liệu thành các phần nhỏ hơn.  
- Hiểu nguyên lý hoạt động của `RecursiveCharacterTextSplitter` trong LangChain, bao gồm việc sử dụng đệ quy và danh sách ký tự phân tách.  
- Triển khai một ví dụ thực tế: chia một đoạn essay của Paul Graham thành các chunk không vượt quá 100 ký tự và kiểm tra kết quả.  
- Đánh giá ảnh hưởng của tham số `chunk_overlap` và khi nào nên điều chỉnh `chunk_size`.  

## 2. Tổng quan

Các LLM hiện đại (ví dụ: GPT‑3.5‑turbo) chỉ có thể “nhìn” một số lượng token nhất định trong một lần suy luận – được gọi là **context window**. Khi tài liệu đầu vào dài hơn cửa sổ này, mô hình sẽ không thể xử lý toàn bộ nội dung một lúc.  

Để khắc phục, chúng ta áp dụng **chunking**: chia tài liệu thành các đoạn (chunks) nhỏ đủ để vừa nằm trong context window, sau đó cho mô hình xử lý từng chunk một (hoặc kết hợp chúng trong các kỹ thuật như Retrieval‑Augmented Generation).  

LangChain cung cấp nhiều phương pháp chunking khác nhau, trong đó `RecursiveCharacterTextSplitter` được khuyên dùng vì nó tự động thử các ký tự phân tách từ rộng đến hẹp (dòng mới → dấu cách → chuỗi rỗng) và sử dụng đệ quy để đảm bảo mỗi chunk không vượt quá kích thước được chỉ định.

## 3. Kiến thức cốt lõi

### 3.1. Context window và nhu cầu chunking  
- **Context window**: số token tối đa mà LSTM/Transformer có thể nhận làm đầu vào cùng một lúc (ví dụ: 4096 token ≈ 3500 từ cho gpt-3.5-turbo).  
- Khi văn bản > context window → cần **chia nhỏ** (chunking) để mỗi phần vừa dentro của cửa sổ.

### 3.2. Nguyên tắc hoạt động của `RecursiveCharacterTextSplitter`  
1. **Đầu vào**: một chuỗi văn bản lớn và các tham số:  
   - `chunk_size`: kích thước tối đa (theo đơn vị đo độ dài, thường là số ký tự).  
   - `chunk_overlap`: số ký tự chồng lặp giữa các chunk liên tiếp (mặc định 0).  
   - `length_function`: hàm dùng để đo độ dài (thường là `len`).  
2. **Danh sách ký tự phân tách** (theo thứ tự ưu tiên): `["\n\n", "\n", " ", ""]`.  
3. **Thuật toán đệ quy**:  
   - Thử tách bằng ký tự đầu tiên (`\n\n`).  
   - Nếu kết quả nào vẫn dài > `chunk_size`, áp dụng lại cùng quy trình trên đoạn đó với ký tự tiếp theo (`\n`).  
   - Tiếp tục cho đến khi mọi đoạn đều ≤ `chunk_size`.  
4. **Gộp (merge)**: Sau khi đạt được các đoạn thỏa mãn kích thước, chúng được gộp lại sao cho không vượt quá `chunk_size`, đồng thời giữ lại thứ tự ban đầu.

### 3.3. Ý nghĩa của `chunk_overlap`  
- Khi `chunk_overlap > 0`, mỗi chunk sẽ chứa một phần nội dung của chunk trước và sau.  
- Điều này giúp duy trì ngữ cảnh khi các chunk được xử lý độc lập (ví dụ: trong vector database hoặc RAG), giảm nguy cơ mất thông tin ở ranh giới.

## 4. Ví dụ minh họa

### 4.1. Chuẩn bị dữ liệu

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """What I Worked On

February 2021

Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined made them deep.

The first programs I tried writing were on the IBM 1401 that our school district used for what was then called "data processing." This was in 9th grade, so I was 13 or 14. The school district's 1401 happened to be in the basement of our junior high school, and my friend Rich Draves and I got permission to use it. It was like a mini Bond villain's lair down there, with all these alien-looking machines — CPU, disk drives, printer, card reader — sitting up on a raised floor under bright fluorescent lights.
"""
```

### 4.2. Tạo splitter và thực hiện chia

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    length_function=len,
)

texts = text_splitter.split_text(text)
print(f"Số chunk: {len(texts)}")   # 11
print("Chunk đầu tiên:")
print(repr(texts[0]))             # 'What I Worked On\n\nFebruary 2021'
```

**Kết quả** (được rút gọn để見得清楚):

```
Số chunk: 11
Chunk đầu tiên:
'What I Worked On\n\nFebruary 2021'
```

Mỗi chuỗi trong `texts` có độ dài ≤ 100 ký tự, và chúngTogether lại ricostituent exactement le texte d'origine (sans overlap).

### 4.3. Minh họa quá trình đệ quy (tóm tắt)

| Bước | Ký tự thử | Kết quả tách | Ghi chú |
|------|-----------|--------------|---------|
| 1 | `\n\n` | 4 đoạn (hai đoạn ngắn, hai đoạn dài) | Hai đoạn ngắn → gộp thành chunk 1 |
| 2 | `\n` (trên đoạn dài còn lại) | 2 đoạn (một đơn ký tự, một đoạn >100) | Đơn ký tự → good split; đoạn còn lại cần xử lý tiếp |
| 3 | `" "` (dấu cách) trên đoạn >100 | Nhiều đoạn, mỗi đoạn ≤100 | Sau khi gộp lại → các chunk cuối cùng |

Sau qua các bước đệ quy và gộp, chúng ta được 11 chunk, mỗi chunk không vượt quá 100 ký tự – chính xác như kết quả in ra.

### 4.4. Thử với `chunk_overlap` khác

```python
text_splitter_overlap = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,   # 20 ký tự chồng lặp
    length_function=len,
)

texts_overlap = text_splitter_overlap.split_text(text)
print(f"Số chunk có overlap: {len(texts_overlap)}")
print("Hai chunk đầu tiên:")
print(repr(texts_overlap[0]))
print(repr(texts_overlap[1]))
```

Kết quả sẽ cho thấy mỗi chunk bắt đầu bằng 20 ký tự cuối của chunk trước, giúp giữ lại mảnh ngữ cảnh khi các chunk được lưu trữ hoặc truy xuất độc lập (ví dụ trong vector DB).

## 5. Tổng kết

- LLM chỉ có thể xử lý một lượng token hữu hạn (context window); khi tài liệu vượt qua giới hạn này, ta phải **chia nhỏ** (chunking).  
- `RecursiveCharacterTextSplitter` của LangChain thực hiện chunking bằng cách **đệ quy** qua một danh sách ký tự phân tách (`\n\n`, `\n`, space, ""), từng bước giảm kích thước các đoạn cho tới khi mỗi chunk thỏa mãn `chunk_size`.  
- Thuật toán luôn đảm bảo mỗi chunk không vượt quá kích thước được chỉ định, đồng thời giữ nguyên thứ tự và nội dung gốc.  
- Tham số `chunk_overlap` cho phép tạo ra sự chồng lặp giữa các chunk, hữu khi các chunk sẽ được lưu trữ hoặc truy xuất độc lập (ví dụ trong hệ thống Retrieval‑Augmented Generation).  
- Khi lựa chọn `chunk_size`, cần cân bằng giữa giới hạn context window của mô hình và mức độ chi tiết cần保留; việc làm chunk quá lớn có thể vượt qua window, quá nhỏ có thể làm mất mcontextual liên hệ.

Với kiến thức trên, bạn đã sẵn sàng áp dụng `RecursiveCharacterTextSplitter` để chuẩn bị dữ liệu cho các ứng dụng LLM như truy vấn tài liệu, tạo embedding, hoặc xây dựng hệ thống RAG. Happy chunking!