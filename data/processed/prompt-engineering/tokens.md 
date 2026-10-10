# Hiểu về Token trong AI và Vai trò của AI Factory

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ能够:

- Giải thích **token** là gì và cách nó được tạo ra từ dữ liệu thô (tokenization).  
- Mô tả cách các mô hình AI sử dụng token trong giai đoạn **training**, **inference** và **reasoning**.  
- Phân tích vai trò của token trong kinh tế AI (chi phí, doanh giá trị và mô hình trả giá).  
- Liệt kê những yếu tố ảnh hưởng đến **cost‑per‑token** và cách NVIDIA’s full‑stack platform giúp tối ưu hoá chúng.  
- Áp dụng kiến thức này để đánh giá và chọn lựa giải pháp AI phù hợp với nhu cầu xử lý lớn.

## 2. Tổng quan

Trong mọi ứng dụng AI, dữ liệu đầu vào (văn bản, hình ảnh, âm thanh, video…) phải được chuyển đổi thành một dạng mà mô hình có thể “đọc” – đó là **token**. Token là những đơn vị dữ liệu tối thiểu được tạo ra qua quá trình **tokenization**. Việc xử lý token nhanh và rẻ là then chốt để AI có thể học hỏi, suy luận và tạo ra giá trị kinh tế.  

AI Factory – một loại trung tâm dữ liệu chuyên dụng – được thiết kế để xử lý khối lượng token lớn với chi phí thấp, тем самым “chuyển đổi” token thành **intelligence** (tri thức), tiền tệ của cách mạng công nghiệp mới do AI dẫn dắt.  

Bài học này sẽ dẫn bạn qua các khái niệm cơ bản, cách token được dùng trong các giai développment khác nhau, và giải thích tại sao tối ưu hoá token là điều then chốt để đạt được **lowest cost per token**.

## 3. Kiến thức cốt lõi

### 3.1 Token là gì và quá trình tokenization

- **Token** là một mảnh dữ liệu rời rạc (ví dụ: một từ, một phần từ, một pixel nhóm, hoặc một спектrogram slice) được biểu diễn bằng một con số nguyên.  
- **Tokenization** là bước chia dữ liệu thô thành chuỗi token dựa trên bộ từ vựng (vocabulary) của tokenizer.  
- Tokenizer có thể là:
  - **Word‑level** (mỗi từ là một token) – phù hợp với các ngôn ngữ có từ vựng vừa phải.  
  - **Subword‑level** (ví dụ: BPE, WordPiece) – chia từ dài thành các片段 như “dark” + “ness”.  
  - **Character‑level** hoặc **pixel/voxel‑level** – dùng cho hình ảnh, video, âm thanh.  

#### Ví dụ minh họa (văn bản)

| Từ gốc | Tokenization (subword) | Mã số token (giả định) |
|--------|------------------------|------------------------|
| darkness | “dark”, “ness” | 217, 655 |
| brightness | “bright”, “ness” | 491, 655 |
| lie (nghĩa “ngả”) | “lie” | 342 |
| lie (nghĩa “nói dối”) | “lie” (nhưng khác ngữ cảnh) | 874 |

- Giá trị số chung (`655` cho “ness”) cho phép mô hình nhận ra mối liên hệ ngữ nghĩa giữa các từ chứa phần đuôi này.  
- Khi cùng một chuỗi ký tự có nhiều ý nghĩa tùy vào bối cảnh, tokenizer có thể gán mã số khác nhau tùy thuộc vào cách mẫu đã được huấn luyện.

#### Dữ liệu hình ảnh và âm thanh

- **Hình ảnh/Video**: pixel (hoặc nhóm pixel) được gridding thành các ô, mỗi ô chuyển thành một token biểu diễn đặc trưng màu hoặc gradient.  
- **Âm thanh**: đoạn ngắn được biến thành spectrogram (hình ảnh của tần số theo thời gian), sau đó xử lý như ảnh; hoặc trực tuyến trích xuất **semantic token** (ngữ nghĩa) từ lời nói thay vì chỉ thông tin âm thanh.

### 3.2 Token trong quá trình Training

1. **Tokenization bộ dữ liệu huấn luyện** → nhận được hàng tỷ, thậm chí nghìn tỷ token.  
2. Mô hình (thường là Transformer) được **pretrained** bằng việc dự đoán token tiếp theo (next‑token prediction) trên một batch token.  
3. Khi dự đoán sai, trọng số được cập nhật qua back‑propagation; lặp lại cho tới khi mô hình đạt **model convergence** (mức độAccuracy mục tiêu).  
4. **Post‑training** (fine‑tuning) tập trung vào một bộ token phụ thuộc vào domain (luật, y tế, kinh doanh) hoặc vào một tác vụ cụ thể (reasoning, chat, перевод).  
5. Theo **pretraining scaling law**, semimet릭 số token huấn luyện tăng → chất lượng mô hình tốt hơn (trong giới hạn hợp lý).

### 3.3 Token trong Inference và Reasoning

- **Input**: Prompt (văn bản, hình ảnh, …) → tokenization → chuỗi **input tokens**.  
- Mô hình xử lý chúng (thông qua các lớp attention) và tạo ra **output tokens** (phản hồi).  
- Output tokens sau này được **detokenize** thành định dạng mà người dùng mong đợi (văn bản, hình ảnh, …).  

#### Context window

- Mỗi mô hình có giới hạn số token có thể xem cùng lúc → **context window**.  
  - Nhỏ (vài nghìn token) → đủ cho một câu hoặc một trang văn bản.  
  - Lớp (tens of thousands) → có thể tóm tắt một cuốn sách hoặc một podcast.  
  - Extremely large (≥1 triệu token) → cho phép phân tích tập dữ liệu khổng lồ trong một lần gọi.  

#### Reasoning tokens (Test‑time scaling)

- Mô hình LLM mới nhất có thể sinh ra **reasoning tokens** trong khi “nghĩ” về câu hỏi trước khi đưa ra câu trả lời cuối cùng.  
- Quy trình này có thể kéo dài từ vài phút tới vài giờ và tiêu tốn **>100×** tính toán so với một lượt inference thông thường, nhưng cung cấp câu trả lời chất lượng cao hơn cho các vấn đề phức tạp.  

### 3.4 Token và Kinh tế AI

| Giai đoạn | Vai trò của token |
|----------|-------------------|
| Pretraining / Post‑training | Token là **đầu tư** vàotri thức (intelligence). |
| Inference | Token決定 **chi phí** (compute) và **doanh thu** (mỗi token được giao dịch có giá trị). |

- Các **AI Factory** được xây dựng để chịu được lưu lượng inference cao, biến token thành **insights có thể bán**, do đó nhiều dịch vụ AI áp dụng mô hình trả giá dựa trên **số token nhập và xuất**.  
- Một số gói giá:
  - **Token chung** (input + output) – người dùng có thể dùng ít token cho prompt ngắn để sinh ra phản hồi dài (nghìn token output).  
  - **Giới hạn token mỗi phút** – để kiểm soát tài nguyên khi phục vụ nhiều người dùng đồng thời.  
- Chỉ số trải nghiệm người dùng:
  - **Time‑to‑first‑token (TTFT)** – latency từ khi gửi prompt tới khi bắt đầu nhận token đầu tiên.  
  - **Inter‑token latency** – tốc độ sinh ra token tiếp theo; ảnh hưởng tới cảm giác “mượt” khi đọc hoặc xem video được tạo.  
- Cân bằng giữa TTFT, inter‑token latency và **throughput** (số tokenFactory có thể sinh ra mỗi giây) tuỳ thuộc vào trường hợp sử dụng (chatbot cần TTFT thấp, mô hình suy luận sâu cần ưu tiên chất lượng token hơn là tốc độ).

### 3.5 Tối ưu hoá chi phí mỗi token (Cost‑per‑Token)

- **NVIDIA full‑stack AI platform** cung cấp:
  - **GPU hỗ trợ accelerate computing** (Hopper, Blackwell…) – tăng throughput, giảm latency.  
  - **Phần mềm & microservices** (NVIDIA NIM, TensorRT‑LLM, Triton Inference Server) – tối ưu hoá kernel, batching, và quantization.  
  - **Blueprint & workflows** – các mẫu cấu trúc để triển khai AI Factory dễ dàng, mở rộng theo nhu cầu.  

- Kết quả thực tế (được trích từ bài viết):
  - Tối ưu hoá phần mềm + sử dụng GPU thế hệ mới → **giảm chi phí mỗi token xuống 20×** so với quy trình chưa tối ưu trên GPU thế hệ cũ.  
  - Đồng thời tạo ra **doanh thu tăng 25×** trong vòng 4 tuần nhờ xử lý nhiều token hơn với cùng mức đầu tư.  

- Các yếu tố ảnh hưởng tới **cost‑per‑token**:
  1. **Hiệu suất phần cứng** (FLOPS, bandwidth, memory capacity).  
  2. **Hiệu suất phần mềm** (kernel fusion, quantization – FP8, INT4, sparsity).  
  3. **Kỹ thuật batching & pipelining** – xử lý nhiều request đồng thời để tối  hoá việc sử dụng GPU.  
  4. **Chọn tokenizer phù hợp** – vocab size nhỏ → ít token cần xử lý.  
  5. **Mô hình kiến trúc** – số layer, kích thước hidden size, sử dụng MoE (Mixture‑of‑Experts) để chỉ kích hoạt các expert cần thiết.  

- **Hướng dẫn thực hành** (tài liệu NVIDIA):
  - Tính toán **lowest cost per token** dựa trên công thức:  
    `Cost per token = (Total compute cost) / (Number of tokens processed)`  
  - Tối ưu hoá bằng cách giảm numerator (tối  hoá phần cứng + phần mềm) và tăng denominator (xử lý nhiều token hơn mỗi đơn vị thời gian).  
  - Tải về **Cost‑Latency‑Performance Optimization for AI Factories** ebook và tham khảo hướng dẫn trên `build.nvidia.com` để bắt đầu xây dựng AI Factory của riêng bạn.

## 4. Ví dụ minh họa

### Ví dụ 1: Tokenization từ “darkness”
```text
Input:  darkness
Tokenizer (WordPiece): ["dark", "ness"]
Token IDs: [217, 655]
```
- Mô hình học được rằng hai token `655` (ness) xuất hiện ở cả “darkness” và “brightness”, từ đó nắm bắt được phần đầu tử chung.

### Ví dụ 2: ẢnhRGB 64×64 được chia thành patch 8×8
- Mỗi patch (8×8×3 = 192 giá trị) được flatten → vector 192‑dim → qua một lớp linear projection => **1 token**.  
- Tổng số tokens = (64/8)×(64/8) = 8×8 = 64 token.  
- Transformer sau đó xử lý 64 token này như một chuỗi token thông thường.

### Ví dụ 3: Đoạn audio 1 giây được chuyển thành spectrogram
- STFT → magnitude spectrogram (128 bins × 200 frames).  
- Mỗi frame (128‑dim vector) được xem như 1 token → 200 token cho 1 giây âm thanh.  
- Những token này sau đó được đưa vào mô hình Transformer để nhận diện từ khóa hoặc tạo ra bản ghi âm mới.

## 5. Tổng kết

- **Token** là đơn vị dữ liệu cơ bản mà mọi mô hình AI sử dụng để biểu diễn văn bản, hình ảnh, âm thanh, video…  
- Quá trình **tokenization** chuyển dữ liệu thô thành chuỗi token; cách chọn tokenizer ảnh hưởng trực tiếp tới số token cần xử lý và vì vậy tới chi phí.  
- Trong **training**, mô hình học từ lượng lớn token (tỷ → nghìn tỷ) để nắm bắt mối quan hệ; trong **inference**, nó sinh ra token phản hồi và có thể tạo ra **reasoning tokens** cho suy luận sâu.  
- Token cũng định hình **kinh tế AI**: chi phí mỗi token决定ต้นทุน運用, còn số token được sinh ra và tiêu dùng quyết định doanh thu; các AI Factory được thiết kế để tối ưu hoá cả hai.  
- Để đạt **lowest cost per token**, cần kết hợp phần cứng GPU mạnh, phần mềm tối ưu (kernel fusion, quantization, batching), tokenizer hiệu quả và kiến trúc mô hình tiết kiệm (MoE, lớp ít hơn).  
- NVIDIA’s full‑stack platform (GPU, NIM, Triton, TensorRT‑LLM, blueprints) cung cấp mọi thành phần cần thiết để xây dựng, mở rộng và vận hành AI Factory với **cost per token** thấp nhất có thể.  

Bằng cách nắm vững lý thuyết và thực tiễn về token, bạn sẽ có thể đánh giá và thiết kế hệ thống AI đáp ứng được cả yêu cầu về hiệu suất và về chi phí, từ đó khai thác tối đa giá trị mà AI mang lại.