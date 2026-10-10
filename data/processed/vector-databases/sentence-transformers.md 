# BERT: Mô hình Bidirectional Encoder Representations from Transformers

## 1. Mục tiêu học tập

- Hiểu BERT là gì và cách hoạt động của nó.  
- Nêu vai trò của BERT trong xử lý ngôn ngữ tự nhiên (NLP) và so sánh với các mô hình liên quan.  
- Giải thích tại sao BERT quan trọng và những ứng dụng thực tế phổ biến.  
- Nêu điểm khác biệt chính giữa BERT và GPT, Word2Vec, RoBERTa.  

## 2. Tổng quan

BERT (Bidirectional Encoder Representations from Transformers) là một **framework machine learning** do Google phát hành năm 2018. Mục tiêu của BERT là nâng cao khả năng hiểu **ngữ cảnh** của văn bản không có nhãn bằng cách học dự đoán từ có thể xuất hiện trước và sau một từ cụ thể (bidirectional). BERT chuyển đổi từ thành vector số, cho phép các mô hình machine learning xử lý dữ liệu văn bản như bất kỳ đặc trưng số nào khác.

## 3. Kiến thức cốt lõi

### 3.1 Nguyên lý hoạt động  

- BERT sử dụng **encoder** của kiến trúc Transformer.  
- Hai mục tiêu pre‑training không giám sát:  
  1. **Masked Language Modeling (MLM)**: một phần các token bị thay đổi bằng `[MASK]`; mô hình phải dự đoán token ban đầu dựa trên cả trái và phải.  
  2. **Next Sentence Prediction (NSP)**: đưa ra hai câu A và B, mô hình quyết định xem B có thực sự là câu tiếp theo của A hay không.  
- qua các lớp Transformer encoder, mỗi token nhận được **vector context‑aware** که tích hợp thông tin từ toàn bộ câu.

### 3.2 Input‑Output  

- Văn bản được token hóa (WordPiece) → mỗi token có embedding początkowy (token + segment + position).  
- Sau khi truyền qua các lớp encoder, mỗi token đầu ra là một vector biểu diễn nghĩa của từ trong câu cụ thể.  
- Vector đặc biệt `[CLS]` (được umieszcz ở đầu chuỗi) thường được dùng làm representation của toàn bộ câu cho các tác vụ classification.

### 3.3 Pre‑training và fine‑tuning  

- BERT được **pre‑train** trên khoadav corpus văn bản lớn (ví dụ: Wikipedia + BookCorpus) mà không cần nhãn.  
- Sau pre‑train, có thể **fine‑tune** trên một tập dữ liệu có nhãn cho một task cụ thể (phân loại cảm xúc, trả lời câu hỏi, nhận diện thực thể, …) bằng cách thêm một lớp dự đoán đơn giản trên đầu `[CLS]` hoặc trên các token.  
- Khi chỉ cần embedding, người dùng có thể lấy vector của mỗi token (hoặc `[CLS]`) làm đặc trưng đầu vào cho các mô hình downstream khác (SVM, logistic regression, …).

### 3.4 Ưu điểm  

- **Bidirectional**: mỗi từ được biết biết từ cả hai phía, khác với các mô hình đọc một chiều (ví dụ LSTM, GPT).  
- **Contextual embedding**: cùng một từ có vector khác nhau tùy thuộc vào câu (ví dụ từ “bank” có ý nghĩa ngân hàng hoặc bờ sông).  
- **Transfer learning mạnh**: pre‑train trên dữ liệu đa dạng cho hiệu năng cao trên nhiều benchmark NLP.

### 3.5 Ứng dụng thực tế  

- Xác định sentimento của Review phim (tích hợp/tiêu cực).  
- Hỗ trợ chatbot trả lời câu hỏi dựa trên cơ sở kiến thức.  
- Gợi ý từ khi soạn thảo email (smart compose).  
- Tóm tắt nhanh các hợp đồng pháp lý dài.  
- Phân biệt từ đồng âm dựa trên ngữ cảnh xung quanh.  

## 4. Ví dụ minh họa

### Ví dụ 1 – Phân loại sentimento Review phim  

1. **Câu**: “The movie was fantastic, I loved it!”  
2. Tokenization → sequence of WordPiece tokens.  
3. Sau BERT encoder, vector của token `[CLS]` tóm tắt toàn câu.  
4. Đưa vector `[CLS]` vào một lớp logistic regression (hoặc một lớp dense nhỏ) để dự đoán nhãn **positive** / **negative**.  

Kết quả: vì từ “fantastic”, “loved” mang ý nghĩa tích cực, BERT sẽ đưa vector `[CLS]` có hướng favorable → mô hình dự đoán “positive”.

### Ví dụ 2 – Từ đồng âm “bank”

- Câu A: “We went to the river bank.”  
  - Vector của “bank” sau BERT gần với “river”, “water”, “shore”.  
- Câu B: “I need to go to the bank to make a deposit.”  
  - Vector của “bank” sau BERT gần với “money”, “cash”, “account”.  

**Word2Vec** sẽ đưa ra một vector duy nhất cho “bank” trong cả hai câu, vì vậy không thể phân biệt hai nghĩa. BERT, ngược lại, tạo ra hai vector khác nhau, cho phép mô hình downstream hiểu đúng nghĩa dựa trên ngữ cảnh.

### Bảng so sánh BERT vs GPT (trích từ nguồn)

| **BERT** | **GPT** |
|---|---|
| **Bidirectional** – xử lý từ trái‑phải và phải‑trái, dùng **encoder** của Transformer. | **Autoregressive, unidirectional** – chỉ xử lý một chiều, dùng **decoder** của Transformer. |
| Ứng dụng: Google Docs, Gmail Smart Compose, tìm kiếm nâng cao, voice assistance, phân tích review. | Ứng dụng: xây dựng ứng dụng, sinh code ML, website, viết bài, podcast, soạn thảo tài liệu pháp lý. |
| GLUE score = 80.4 %; accuracy 93.3 % trên SQuAD. | TriviaAQ accuracy 64.3 %; LAMBADA accuracy 76.2 % (zero‑shot). |
| Huấn luyện qua **masked language modeling** + **next sentence prediction**. | Huấn luyện qua **autoregressive language modeling** (sinh text liên tục). |

### BERT vs Word2Vec  

- **Word2Vec**: một vector cố định cho mỗi từ, không phụ thuộc vào câu.  
- **BERT**: vector thay đổi theo câu → cho phép phân biệt nghĩa từ đồng âm và mô hình câu phức tạp hơn.

### BERT vs RoBERTa  

- RoBERTa (Robustly Optimized BERT Pretraining Approach) là phiên bản được tối ưu sau BERT.  
- Điểm khác biệt chính:  
  - Sử dụng **dynamic masking** thay vì static masking trong MLM.  
  - Loại bỏ mục tiêu **next sentence prediction**; huấn luyện trên câu hoàn chỉnh.  
  - Huấn luyện lâu hơn và trên dữ liệu lớn hơn → thường đạt hiệu suất tốt hơn trên các benchmark.  
- Do đó, BERT có thể xem là một mô hình **under‑trained** soцией RoBERTa, nhưng vẫn là nền tảng quan trọng và dễ tiếp cận.

## 5. Tổng kết

- BERT là một mô hình **encoder‑based Transformer** học biểu diễn từ **bidirectional** qua masked language modeling và next sentence prediction trên dữ liệu văn bản lớn không có nhãn.  
- Nó biến đổi văn bản thành các vector số, cho phép các mô hình machine learning xử lý ngôn ngữ tự nhiên như các đặc trưng số thông thường.  
- Ứng dụng thực tế bao gồm phân loại cảm xúc, hỗ trợ chatbot, gợi ý từ khi soạn thảo email, tóm tắt tài liệu pháp lý và phân biệt từ đồng âm.  
- So sánh với GPT, Word2Vec và RoBERTa giúp nhận ra điểm mạnh của BERT (contextual, bidirectional) và những trường hợp mà các mô hình khác có thể phù hợp hơn (GPT cho sinh text, RoBERTa cho hiệu năng tối ưu).  
- Khi sử dụng BERT trong thực tiễn, công việc phổ biến là lấy checkpoint pre‑train, rồi **fine‑tune** trên task cụ thể hoặc trích vector embedding để dùng làm đặc trưng cho các mô hình downstream.

> **Lưu ý**: Các số liệu và mô tả trên được trích trực tiếp từ nguồn H2O.ai Wiki về BERT; không thêm thông tin ngoài phạm vi đã cho.