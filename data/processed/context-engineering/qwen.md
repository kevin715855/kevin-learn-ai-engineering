# Qwen3 – Giới thiệu về série mô hình AI mở của Alibaba Cloud  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ能:  

- Giải thích Qwen3 là gì và tại sao nó được xem là một trong những LLM mở hàng đầu hiện nay.  
- Nêu tên và đặc điểm chính của tám mô hình Qwen3 (hai MoE và шесть dense).  
- Mô tả cơ chế “hybrid thinking” (Thinking Mode vs Non‑Thinking Mode) và cách người dùng có thể điều chỉnh ngân sách reasoning.  
- Nêu qua quá trình huấn luyện trước và sau huấn luyện của Qwen3, bao gồm các giai đoạn dữ liệu và phương pháp distillation.  
- Liệt kê các cách tiếp cận thực tế để bắt đầu sử dụng Qwen3 (Qwen Chat, API, tự triển khai).  
- Đánh giá lợi ích và hạn chế khi decidir sử dụng Qwen3 trong dự án AI.  

## 2. Tổng quan  

Qwen là系列 mô hình ngôn ngữ lớn (LLM) mã nguồn mở do Alibaba Cloud phát hành. Phiên bản mới nhất, **Qwen3**, bao gồm tám mô hình với quy mô từ 0,6 tỷ đến 235 tỷ tham số, hỗ trợ 119 ngôn ngữ và được cấp phép Apache 2.0 (cho phép sử dụng phi lợi nhuận, thương mại và nghiên cứu). Qwen3 đặc biệt nổi bật vì:  

- Kiến trúc hỗ trợ cả **dense** và **mixture‑of‑experts (MoE)**.  
- Mỗi mô hình có thể hoạt động ở hai chế độ: **Thinking Mode** (reasoning sâu) và **Non‑Thinking Mode** (phản hồi nhanh, ít tài nguyên).  
- Độ dài context lên tới 128 K token (cho các mô hình lớn) và 32 K token (cho các mô hình nhỏ).  
- Tối ưu cho **ứng dụng phi trú (agentic)** qua hỗ trợ Model Context Protocol (MCP).  

Bài học sẽ đưa người học qua từng thành phần trên để hiểu bản chất và cách áp dụng Qwen3 trong thực tế.

## 3. Kiến thức cốt lõi  

### 3.1. Tổng quan về cấu trúc mô hình  

| Nhóm mô hình | Ví dụ | Tổng tham số | Tham số hoạt động (active) | Kiến trúc | Context length |
|--------------|-------|--------------|----------------------------|-----------|----------------|
| MoE (flagship) | Qwen3‑235B‑A22B | 235 B | 22 B | Mixture‑of‑Experts | 128 K |
| MoE (nhẹ hơn) | Qwen3‑30B‑A3B | 30 B | 3 B | Mixture‑of‑Experts | 128 K |
| Dense (lớn) | Qwen3‑32B | 32 B | 32 B | Dense | 128 K |
| Dense (trung bình) | Qwen3‑14B | 14 B | 14 B | Dense | 128 K |
| Dense (nhỏ) | Qwen3‑8B | 8 B | 8 B | Dense | 128 K |
| Dense (siêu nhỏ) | Qwen3‑4B | 4 B | 4 B | Dense | 32 K |
| Dense (siêu nhỏ) | Qwen3‑1.7B | 1.7 B | 1.7 B | Dense | 32 K |
| Dense (siêu nhỏ) | Qwen3‑0.6B | 0.6 B | 0.6 B | Dense | 32 K |

- **Mixture‑of‑Experts (MoE)**: chỉ một phần các “experts” được kích hoạt cho mỗi token, giúp giảm chi phí tính toán जबकि giữ lại khả năng biểu diễn mạnh.  
- **Dense**: tất cả tham số tham gia tính toán, đơn giản hơn để triển khai nhưng tốn tài nguyên hơn tại cùng quy mô tham số.  

### 3.2. Chế độ “hybrid thinking”  

Mỗi mô hình Qwen3 tích hợp sẵn hai cách làm việc:  

- **Thinking Mode**: mô hình dành thời gian để suy luận (chain‑of‑thought) trước khi trả lời, thích hợp cho задач wymagające rozumowania, seperti toán, lập trình, hoặc suy luận phức tạp.  
- **Non‑Thinking Mode**: mô hình trả lời ngay lập tức với ít tài nguyên hơn, phù hợp cho các tác vụ đòi hỏi tốc độ (chatbot, tóm tắt ngắn).  

Người dùng có thể đặt **ngân sách reasoning** (reasoning budget) cho mỗi prompt – sematic là một con trượt trong Qwen Chat hoặc tham số khi gọi API – để cân bằng giữa độ sâu và chi phí/tốc độ.  

### 3.3. Quy trình huấn luyện  

1. **Pre‑training (3 этап)**  
   - **Giai đoạn 1**: >30 t znak token – mô hình získ básica kỹ năng ngôn ngữ và kiến thức chung.  
   - **Giai đoạn 2**: Thêm dữ liệu phong phú về STEM, mã nguồn và nhiệm vụ reasoning – nâng cao khả năng giải quyết vấn đềlogic.  
   - **Giai đoạn 3**: Dữ liệu bối cảnh dài (long‑context) – tạo ra mô hình cơ sở có context length 32 K.  

2. **Post‑training (4 этап)**  
   - **Giai đoạn 1‑2**: Sử dụng chuỗi suy luận (chain‑of‑thought) để phát triển khả năng reasoning.  
   - **Giai đoạn 3**: Thêm dữ liệu không reasoning để tạo ra phiên bản trả lời nhanh, ít tốn tài nguyên.  
   - **Giai đoạn 4**: Học tăng cường (reinforcement learning) để cải thiện hiệu suất, thêm khả năng agentic và sửa comportamento không mong muốn.  

Sau giai段 post‑training, hai mô hình nền tảng **Qwen3‑235B‑A22B** và **Qwen3‑32B** được **distillation** (steam distillation) để sinh ra các mô hình dense nhỏ hơn (30B‑A3B, 32B, 14B, 8B, 4B, 1.7B, 0.6B). Quá trình này giúp giữ lại phần lớn khả năng trong khi giảm kích thước và chi phí triển khai.  

### 3.4. Đa ngôn ngữ và hỗ trợ agentic  

- Qwen3 đã được huấn luyện trên **36 t tỷ token** bao gồm 119 ngôn ngữ và phương言, bao gồm nhiều ngôn ngữ ngoài họ châu âu (ví dụ: tiếng Việt, tiếng Thái, tiếng Ả Rập, v.v.).  
- Hỗ trợ **Model Context Protocol (MCP)** cho phép mô hình tương tác với công cụ bên ngoài (ví dụ: gọi API, truy cập cơ sở dữ liệu) – một yếu tố then chốt để xây dựng **AI agents** tự động.  

### 3.5. Giấy phép và lưu ý về nội dung  

- Phát hành dưới **Apache 2.0** → cho phép sử dụng tự do trong cả môi trường học術 và thương mại, miễn só tuân thủ điều khoản giấy phép.  
- Do được đào tạo bởi một công ty Trung Quốc, bộ conhecimento có thể có **cảm biến** đối với một số chủ đề mà chính phủ Trung Quốc hạn chế. Người dùng nên biết về giới hạn này khi triển khai trong ứng dụng toàn cầu.  

## 4. Ví dụ minh họa  

### 4.1. Chọn mô hình phù hợp với nhu cầu  

| Yêu cầu | Mô hình gợi ý | Lý do |
|---------|---------------|-------|
| Ứng dụng lý tưởng trên laptop cá nhân (RAM 16 GB) | Qwen3‑4B, Qwen3‑1.7B, hoặc Qwen3‑0.6B | Kích thước nhỏ (≤4 B), context 32 K, có thể chạy trên CPU/GPU trung bình. |
| Cần reasoning sâu cho bài toán olympiad hoặc sinh mã phức tạp | Qwen3‑235B‑A22B (Thinking Mode) hoặc Qwen3‑30B‑A3B (Thinking Mode) | MoE với số lượng experts lớn, khả năng reasoning mạnh. |
| Xây dựng chatbot trả lời nhanh, giá thành thấp | Qwen3‑8B hoặc Qwen3‑14B (Non‑Thinking Mode) | Dense, ít tham số, trả lời nhanh, đủ chất lượng cho hội thoại phổ thông. |
| Tích hợp vào workflow Zapier để gọi công cụ bên ngoài | Qwen3‑32B hoặc Qwen3‑30B‑A3B qua API (Alibaba Cloud Model Studio, OpenRouter, Lambda) | Hỗ trợ MCP, có sẵn endpoint API, dễ kết nối với Zapier. |

### 4.2. Sử dụng Qwen Chat để điều chỉnh ngân sách reasoning  

1. Mở <https://chat.qwen.ai/> và chọn một trong ba mô hình: Qwen3‑235B‑A22B, Qwen3‑30B‑A3B hoặc Qwen3‑32B.  
2. Giao diện hiện một **slider** označённый “Thinking Budget”.  
   - Đẩy sang bên **phải** → tăng thời gian reasoning → kết quả sâu hơn, nhưng trả lời chậm hơn và tốn nhiều token hơn.  
   - Đẩy sang bên **trái** → giảm thời gian reasoning → trả lời ngay lập tức, thích hợp cho câu hỏi đơn giản.  
3. Nhập prompt, ví dụ:  
   ```
   Giải thích brevemente vì sao hàm softmax thường được dùng trong lớp output của mạng neural cho bài toán phân loại đa lớp.
   ```  
   - Khi slider ở mức **Thinking**, mô hình sẽ cung cấp bước‑bước suy luận (softmax → chuẩn hóa xác suất → đặc điểm gradient).  
   - Khi slider ở mức **Non‑Thinking**, câu trả lời sẽ ngắn gọn: “Softmax chuyển logits thành phân phối xác suất, giúp mô hình chọn lớp có xác suất cao nhất.”  

### 4.3. Gọi Qwen3 qua API (ví dụ với OpenRouter)  

```python
import openai   # OpenRouter tương thích với API OpenAI

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"   # thay bằng key của bạn
)

response = client.chat.completions.create(
    model="qwen/qwen3-30b-a3b:free",   # tên model trên OpenRouter
    messages=[
        {"role": "system", "content": "Bạn là một trợ lí AI trả lời ngắn gọn."},
        {"role": "user",   "content": "Tác dụng chính của dropout trong học sâu là gì?"}
    ],
    temperature=0.2,
    max_tokens=150,
    # Tùy chọn reasoning budget (nếu nhà cung cấp hỗ trợ)
    extra_body={"reasoning_effort": "medium"}  
)

print(response.choices[0].message.content)
```
- Đoạn code trên cho thấy cách gọi một mô hình Qwen3 (ở đây là Qwen3‑30B‑A3B) qua OpenRouter.  
- Tham số `reasoning_effort` (hoặc tương đương tùy theo nhà cung cấp) cho phép điều chỉnh mức độ reasoning mà không cần thay đổi model.  

## 5. Tổng kết  

- Qwen3 là một keluarga LLM mở, đa dạng về kích thước và kiến trúc (dense & MoE), được cấp phép Apache 2.0, thích hợp cho cả nghiên cứu và ứng dụng thương mại.  
- Mỗi модель hỗ trợ **hai chế độ làm việc** (Thinking vs Non‑Thinking) và cho phép người dùng điều chỉnh **ngân sách reasoning** để cân bằng giữa chất lượng, tốc độ và chi phí.  
- Quy trình huấn luyện bao gồm ba giai đoạn pre‑training và bốn giai đoạn post‑training, kết thúc bằng distillation để tạo ra các phiên bản nhỏ hơn mà vẫn giữ khả năng cao.  
- Với hỗ trợ 119 ngôn ngữ, độ dài context lên tới 128 K token và tích hợp MCP, Qwen3 phù hợp cho **ứng dụng agentic**, **nhiệm vụ reasoning phức tạp** và **triển khai trên thiết bị có giới hạn tài nguyên**.  
- Khiตัดสินใจ sử dụng, cần lưu ý tới khả năng censura tiềm nhiên do nguồn gốc dữ liệu và kiểm tra giấy phép cũng như các yêu cầu về bảo mật dữ liệu nếu áp dụng trong môi trường quốc tế.  

Bằng cách nắm vững các điểm trên, người học có thể tự tin chọn và triển khai Qwen3 phù hợp với mục tiêu dự án AI của mình.