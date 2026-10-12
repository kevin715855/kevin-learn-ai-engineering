# Beyond the Window: Hướng dẫn đầy đủ về Mô hình Ngôn Ngữ Bối Cảnh Dài (Long Context Language Models) và Tác động của chúng tới AI  

## 1. Mục tiêu học tập  

Sau khi đọc bài học này, bạn sẽ có thể:  

- Giải thích tại sao cửa sổ bối cảnh (context window) ngắn hạn là rào cản cho nhiều tác vụ NLU và NLG.  
- Mô tả khái niệm **Long Context Language Model (LCLM)** và những lợi thế mà nó mang lại so với các mô hình truyền thống.  
- Nêu tên và nguyên lý hoạt động của một số kiến trúc LCLM tiêu biểu (Longformer, BigBird, RoFormer, Compressive Transformer, Retrieval‑augmented, …).  
- Nêu các thách thức chính khi mở rộng bối cảnh (phức tạp tính toán, bộ nhớ GPU, ổn định huấn luyện).  
- Nhận biết cách đánh giá LCLM (perplexity trên các benchmark dài, khả năng truy vấn thông tin, tổng hợp tài liệu dài).  
- Áp dụng một ví dụ thực tế bằng thư viện 🤗 Transformers để xử lý văn bản dài với mô hình LCLM.  

## 2. Tổng quan  

Các mô hình ngôn ngữ lớn (LLM) hiện nay hoạt động trong một “cửa sổ bối cảnh” hữu hạn – thường chỉ khoảng 2 000‑8 000 token (tương đương vài ngàn từ). Khi đầu vào vượt qua giới hạn này, mô hình chỉ có thể xem một phần của văn bản, dẫn tới mất mát thông tin quan trọng trong các tác vụ như tóm tắt tài liệu dài, trả lời câu hỏi dựa trên sách báo, hoặc duy trì cuộc trò chuyện xuyên dài.  

Nhờ các tiến bộ trong kiến trúc Attention và kỹ thuật nén bộ nhớ, ra đời **Long Context Language Model (LCLM)** – những mô hình có thể xử lý hàng trăm nghìn tới vài triệu token trong một lần truyền lan. Điều này mở ra khả năng đọc toàn bộ cuốn sách, phân tích bản báo tài chính hàng năm, hoặc duy trì “bộ nhớ” dài cho các tác tử hội thoại và tác nhân AI.  

Bài học này dựa trên bài survey “A Comprehensive Survey on Long Context Language Modeling” (M‑A‑P survey) và tóm tắt các điểm cần biết về LCLM: tại sao chúng cần thiết, cách chúng được xây dựng, những thách thức phải vượt qua và cách đánh giá hiệu quả của chúng.  

## 3. Kiến thức cốt lõi  

### 3.1. Vì sao cửa sổ bối cảnh ngắn hạn là vấn đề?  

| Nhiệm vụ | Giới hạn của context window ngắn | Hậu quả |
|----------|----------------------------------|---------|
| **Tóm tắt tài liệu dài** | Chỉ có thể xem mỗi đoạn (chunk) riêng | Mất sự liên quan toàn cục, không bắt được chủ đề sâu |
| **Trả lời câu hỏi dựa trên bản báo** | Cần tìm đoạn có chứa câu trả lời trước, sau đó đưa vào window | Thiếu bối cảnh suy luận, trả lời không đầy đủ |
| **Chatbot / agentes** | Nhớ chỉ vài lượt trò chuyện gần nhất | Quên mục tiêu lịch sử, không thể duy trì cuộc đối thoại dài |
| **Phân tích mã nguồn / log hệ thống** | File thường vượt qua vài nghìn token | Không thể xem toàn bộ logic hoặcpattern lỗi |

### 3.2. Định nghĩa Long Context Language Model  

Một LCLM là mô hình ngôn ngữ được thiết kế để **tăng kích thước cửa sổ bối cảnh** một cách hiệu quả, thường từ 32 k token tới 1 mille token hoặc hơn, mà không làm tăng đáng kể chi phí tính toán bậc hai (O(n²)) của Attention truyền thống.  

### 3.3. Các hướng tiếp cận chính để mở rộng bối cảnh  

| Nhóm | Ý tưởng core | Ví dụ mô hình |
|------|--------------|----------------|
| **Sparse Attention** | Chỉ tính Attention trên một subset稀疏的 token pairs (local + global) | Longformer (sliding window + global tokens), BigBird (random + window + global) |
| **Recurrence / Memory** | Lưu trữ biểu diễn đoạn trước và tái sử dụng qua các lớp hoặc thời gian | Compressive Transformer, Transformer-XL |
| **Hierarchical / Chunk‑wise** | Chia văn bản thành các khối, mã hóa từng khối rồi tổng hợp | Hierarchical Transformer, RAG‑based chunking |
| **Linear / Approximate Attention** | Biến đổi Attention thành O(n) qua kernel feature maps hoặc low‑rank | Linformer, Performer, FlashAttention‑2 (vẫn O(n²) nhưng tối ưu bộ nhớ) |
| **Retrieval‑augmented** | Truy xuất các đoạn liên quan từ một corpus extern và chỉ atención trên những đoạn đó | RETRO, REALM, RAG‑augmented LLMs |
| **Compressive / Sliding‑window + Summary** | Nén thông tin đoạn trước thành vectorSummary để làm “global token” | Longformer‑ED, Luna, Hyena (cấu trúc卷积+gating) |

> **Lưu ý:** Nhiều mô hình kết hợp nhiều ý tưởng (ví dụ: Longformer + global tokens + sliding window).

### 3.4. Thách thức khi mở rộng bối cảnh  

1. **Phức tạp tính toán Attention** – Attention đầy đủ vẫn O(n²) trong bộ nhớ và thời gian; các kỹ thuật sparse hoặc linear cần thiết kế kỹ để không làm giảm chất lượng mô hình.  
2. **Bộ nhớ GPU** – Dài hơn 32 k token thường đòi hỏi nhiều GB VRAM; kỹ thuật checkpointing, activation recomputation hoặc sharding được dùng.  
3. **Huấn luyện ổn định** – Mô hình có xu hướng “quên” token rất xa do gradient vanishing; cần điều chỉnh learning rate, sử dụng warm‑up dài, hoặc thêm loss auxiliar (ví dụ: predict next sentence).  
4. **Đánh giá** – Các benchmark tiêu chuẩn (GLUE, SuperGLUE) tập trung vào văn bản ngắn; cần tập dữ liệu dài như PG‑19, BookSum, SCROLLS, hoặc tạo ra tác vụ hợp성의pecific (long‑doc QA, multi‑session dialogue).  

### 3.5. Đánh giá hiệu quả của LCLM  

| Tiêu chí | Mô tả | Công cụ / Bộ dữ liệu thường dùng |
|----------|-------|----------------------------------|
| **Perplexity trên văn bản dài** | Đo durchschnitt surprisal khi dự đoán token tiếp theo trong đoạn văn bản > 32 k token | PG‑19, BookSum, arXiv‑2023 |
| **Khả năng truy vấn thông tin** | Đo F1 / Exact Match khi trả lời câu hỏi whose answer nằm ở khoảng cách xa trong tài liệu | HotpotQA (multi‑hop), Natural Questions (long version), QuALITY |
| **Tóm tắt toàn cục** | Đo ROUGE/L hoặc BERTScore giữa tóm tắt được tạo và parameter tham chiếu tài liệu đầy đủ | SummScreen, GovReport |
| **Cuộc trò chuyện kéo dài** | Đo độ nhất quán và độ retains thông tin qua nhiều turn (10‑50 turn) | ConvAI2 extended, MultiWOZ‑long |
| **Hiệu suất thời gian & bộ nhớ** | Đo throughput (token/s) và VRAM dùng trên phần cụm tertentu | Benchmark on A100 / H100 |

### 3.6. Taxonomy (phân loại) theo M‑A‑P survey  

1. **Full‑attention with efficient kernels** – FlashAttention, Block‑sparse Attention.  
2. **Sliding‑window + global tokens** – Longformer, BigBird.  
3. **Recurrent memory** – Transformer‑XL, Compressive Transformer.  
4. **Hierarchical chunking** – HG‑Transformer, MemTransformer.  
5. **Linear / low‑rank approximations** – Linformer, Performer, Reformer.  
6. **Retrieval‑augmented** – RETRO, REALM, RAG‑augmented LLMs.  
7. **Hybrid architectures** – Kết hợp 2 hoặc více phương pháp trên (ví dụ: Longformer + retrieval).  

## 4. Ví dụ minh họa  

### 4.1. Tải và sử dụng Longformer để mã hóa một tài liệu dài  

Longformer (của AllenAI) áp dụng **sliding‑window attention** (kích thước window = 512) đồng thời cho một số *global token* có thể xem toàn bộ序列. Điều này cho phép mô hình xử lý tới 16 384 token mà chỉ tiêu thụ bộ nhớ tuyến tính theo độ dài.  

```python
# Cài đặt thư viện cần thiết (chỉ chạy một lần)
# pip install transformers torch

from transformers import LongformerTokenizer, LongformerModel
import torch

# 1. Chuẩn bị tokenizer và model
tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
model     = LongformerModel.from_pretrained('allenai/longformer-base-4096')
model.eval()  # chế độ suy luận

# 2. Văn bản mẫu: một đoạn trích từ cuốn "Tuyệtverständnis" (khoảng 12 000 token)
long_text = """
... (đoạn văn bản thật dài, có thể lấy từ một file .txt hoặc một bài báo khoa học) ...
"""  # Thay chuỗi này bằng văn bản thực tế của bạn

# 3. Mã hóa đầu vào
inputs = tokenizer(
    long_text,
    return_tensors="pt",
    truncation=False,               # không cắt bớt, mô hình tự xử lý độ dài
    max_length=None                 # để None để tokenizer không giới hạn
)

# 4. Thiết lập global token (tùy chọn): ở đây ta đặt token đầu tiên (CLS) và một vài token vị trí quan trọng làm global
global_attention_mask = torch.zeros_like(inputs["input_ids"])
# Đặt token [CLS] (index 0) và một số token dự kiến quan trọng (ví dụ: mỗi 1000 token) thành global
global_attention_mask[:, 0] = 1
for i in range(1000, inputs["input_ids"].shape[1], 1000):
    global_attention_mask[:, i] = 1

# 5. Forward pass
with torch.no_grad():
    outputs = model(
        **inputs,
        global_attention_mask=global_attention_mask
    )

# outputs.last_hidden_state có shape (batch_size, seq_len, hidden_size)
sequence_output = outputs.last_hidden_state
print("Shape of encoded representation:", sequence_output.shape)
```

**Giải thích kết quả:**  

- `sequence_output` mang lại biểu diễn context‑aware cho mỗi token trong văn bản dài, cho phép bạn thực hiện các tác vụ tiếp theo như:  
  - **Trích xuất vector đại diện** (mean‑pooling hoặc lấy vector CLS) để dùng trong phân loại hoặc tìm kiếm benzer.  
  - **Question answering** bằng cách thêm một tầng classificação trên đầu để đoán vị trí bắt đầu/kết thúc của câu trả lời.  
  - **Tóm tắt** bằng cách feed sequence_output vào một decoder (ví dụ: LongformerForSeq2SeqLM).  

Lưu ý: Nếu bạn muốn xử lý hơn 16 k token, hãy chọn phiên bản `allenai/longformer-large-4096` (cùng window) và tăng giá trị `max_position_embeddings` trong cấu hình, hoặc dùng mô hình hỗ trợ lớn hơn như **LED** (Longformer Encoder‑Decoder) hoặc **BigBird** (có thể mở tới 4 k–8 k token với attention ngẫu nhiên).  

### 4.2. Ứng dụng thực tế: trả lời câu hỏi dựa trên báo cáo tài chính năm  

1. **Thu thập dữ liệu**: Tải báo cáo tài chính 2023 của một công ty (PDF → text) – thường ~ 50 000 token.  
2. **Chunking (tùy chọn)**: Nếu mô hình bạn dùng chỉ hỗ trợ 32 k token, chia báo cáo thành 2 phần, mỗi phần có một *global token* đại diện cho nội dung phần kia (kỹ thuật “compressive summary”).  
3. **Đưa vào Longformer** và đặt câu hỏi như: “What was the net revenue for Q3 2023?”  
4. **Mô hình** trả lời bằng cách trích xuất đoạn token chứa số đoán (ví dụ: “$1.2 billion”).  

Kết quả minh họa cho thấy LCLM có thể **đọc toàn bộ báo cáo mà không cần truy xuất riêng**, giảm lỗi do mất mát liên kết giữa các phần.  

## 5. Tổng kết  

- Cửa sổ bối cảnh ngắn hạn là rào cản cơ bản cho nhiều tác vụ AI hiện tại; các LCLM ra đời để vượt qua giới hạn này bằng cách mở khả năng xử lý đầu vào lên tới hàng trăm nghìn hoặc vài triệu token.  
- Các kiến trúc LCLM đa dạng: **sparse attention** (sliding‑window, global+, random), **recurrent/compressive memory**, **hierarchical chunking**, **linear/low‑rank approximations**, và **retrieval‑augmented**. Mỗi nhóm có trade‑off giữa độ chính xác, hiệu suất bộ nhớ và độ phức tạp triển khai.  
- Thách thức chủ yếu nằm ở **tính toán Attention bậc hai**, **bộ nhớ GPU**, và **ổn định huấn luyện trong chuỗi dài**; các giải pháp như FlashAttention, gradient checkpointing và các loss auxiliar đã giúp giảm thiểu.  
- Đánh giá LCLM cần dùng các benchmark dài (PG‑19, BookSum, SCROLLS, long‑form QA, multi‑session dialogue) thay vì chỉ依赖 GLUE/SuperGLUE.  
- Ví dụ thực tế với Longformer cho thấy cách tải model, thiết lập global attention, và lấy biểu diễn vector để tiếp tục các tác vụ downstream như QA hoặc tóm tắt.  

> **Takeaway:** Long Context Language Models không chỉ là một cải tiếnGradual; chúng thay đổi cách chúng ta thiết kế hệ thống AI — từ mô hình “nhìn qua lỗ hép” tới “có thể xem toàn bộ bức tranh”, mở ra cánh cửa cho các ứng dụng như phân tích tài liệu pháp lý, nghiên cứu khoa học lâu dài, và các trợ lý ảo có trí nhớ opravdico như con người.  

---  

*Bài học được biên soạn dựa trên nội dung bài báo “Beyond the Window: The Complete Guide to Long Context Language Models (And Why They’re Changing AI)” và tài liệu tham khảo từ survey “A Comprehensive Survey on Long Context Language Modeling”.*