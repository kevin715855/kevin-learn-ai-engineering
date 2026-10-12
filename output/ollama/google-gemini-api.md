# Everything you need to know about the Gemini API as a developer (under 5 minutes)

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ có thể:
- Mô tả Gemini API là gì và những tính năng chính mà nó cung cấp.
- Liệt kê các mô hình Gemini mà API hiện hỗ trợ (Gemini 1.5 Flash và Gemini 1.5 Pro).
- Hướng dẫn cách lấy API key miễn phí từ Google AI Studio và thực hiện yêu cầu đầu tiên bằng Python.
- Giải thích mức phí sử dụng Gemini API, bao gồm gói miễn phí và gói trả phí, đồng thời biết về mức giảm giá gần đây của Gemini 1.5 Flash.
- Nêu ngắn gọn quy trình fine‑tuning miễn phí của Gemini 1.5 Flash trong AI Studio và lợi ích của việc này.

## 2. Tổng quan

Gemini là họ mô hình AI sinh tạo frontier của Google, được thiết kế để đa modal và có ngữ cảnh dài. Đối với nhà phát triển, Gemini API là điểm vào để tích hợp các khả năng này vào ứng dụng, từ tạo văn bản, xử lý hình ảnh/video/âm thanh, tới thực thi mã và fine‑tuning mô hình. Bài viết nguồn mô tả ngắn gọn các tính năng chính, cách bắt đầu sử dụng miễn phí, và một số trường hợp nâng cao như fine‑tuning.

## 3. Kiến thức cốt lõi

### 3.1 Gemini API cung cấp gì?

- **Fine‑tuning support** cho Gemini 1.5 Flash (có thể thực hiện miễn phí trong AI Studio).  
- **Context caching** – giảm chi phí triển khai sản xuất bằng cách lưu trữ lại ngữ cảnh được sử dụng thường xuyên.  
- **Code execution** – cho phép mô hình chạy mã để mở rộng khả năngReasoning.  
- **Structured outputs** – trích xuất dữ liệu có cấu trúc từ đầu vào (ví dụ: JSON).  
- **Video, image & audio understanding** – xử lý đa modal (vision, audio).  
- **Document processing** – hỗ trợ PDF lên tới 1.000 trang.  

Ngoài ra, API còn cung cấp hầu hết các tính năng mà nhà phát triển thường mong đợi từ một LLM API, cộng thêm những điểm mạnh riêng của Gemini như ngữ cảnh dài và khả năng hiểu video.

### 3.2 Các mô hình được hỗ trợ

Theo ngày 21 / 09 / 2024, Gemini API mặc định cung cấp hai biến體:
- **Gemini 1.5 Flash** – mô hình nhẹ, giá thành thấp, hỗ trợ fine‑tuning miễn phí.  
- **Gemini 1.5 Pro** – mô hình mạnh hơn, thường dùng cho workloads cần độ chính xác cao.  

Mỗi biến thể có thể có nhiều phiên bản (ví dụ: phiên bản mới hơn có cập nhật hiệu suất). Độ dài ngữ cảnh và khả năng fine‑tuning khác nhau giữa chúng; chi tiết có thể xem trên trang [Gemini models page](https://ai.google.dev/gemini-api/docs/models/gemini).

### 3.3 Cách bắt đầu (miễn phí)

1. **Lấy API key**  
   - Truy cập [Google AI Studio](https://aistudio.google.com/).  
   - Đăng nhập (miễn phí) và nhấn “Get API Key” ở góc trên bên trái để tạo key.  

2. **Cài đặt SDK Python**  
   ```bash
   pip install google-generativeai
   ```

3. **Cấu hình key** (giả sử key được lưu trong biến môi trường `API_KEY`):  
   ```python
   import google.generativeai as genai
   import os

   genai.configure(api_key=os.environ["API_KEY"])
   ```

4. **Gửi yêu cầu tạo nội dung đơn giản**  
   ```python
   model = genai.GenerativeModel("gemini-1.5-flash")
   response = model.generate_content("Explain how AI works")
   print(response.text)
   ```

5. **Tạo cuộc trò chuyện (chat)**  
   ```python
   model = genai.GenerativeModel("gemini-1.5-flash")
   chat = model.start_chat(
       history=[
           {"role": "user", "parts": "Hello"},
           {"role": "model", "parts": "Great to meet you. What would you like to know?"},
       ]
   )
   response = chat.send_message("I have 2 dogs in my house.")
   print(response.text)          # Trả lời về 2 chó
   response = chat.send_message("How many paws are in my house?")
   print(response.text)          # Tính số bàn chân (8)
   ```

   Đoạn code trên cho thấy cách duy trì lịch sử trò chuyện và gửi tin nhắn liên tiếp.

6. **Nguồn code mẫu**  
   - Repository official quickstart: <https://github.com/google-gemini/gemini-api-quickstart>.

### 3.4 Chi phí sử dụng

- **Free tier**: 1.500 request/ngày với Gemini 1.5 Flash (miễn phí vô hạn thời gian).  
- **Paid tier**: Giới hạn request cao hơn, dành cho workloads sản xuất.  
- Gemini 1.5 Flash hiện là LLM có giá thành tốt nhất trong lớp khả năng của nó và gần đây giá đã được giảm **70 %** (theo blog Google Developers).  
- Một cách biểu đạt khác: mỗi ngày bạn có thể sử dụng khoảng **1,5 tỷ token** miễn phí với Gemini 1.5 Flash.

### 3.5 Fine‑tuning Gemini 1.5 Flash

- Thực hiện miễn phí qua Google AI Studio tại đường dẫn <https://aistudio.google.com/app/tune>.  
- Mô hình sau khi fine‑tuned không gây phí sử dụng 추가 so với mô hình gốc – một lợi thế hiếm có trong hệ sinh thái AI.  
- AI Studio cung cấp bộ dữ liệu mẫu và chế độ “Structured prompting” giúp tạo bộ dữ liệu fine‑tuning dễ dàng.  
- Sau khi hoàn thành, mô hình tuned có thể thay thế trực tiếp (drop‑in) trong code hiện tại mà không cần sửa đổi.

## 4. Ví dụ minh họa

**Yêu cầu**: Viết một hàm Python nhận câu hỏi người dùng, gửi tới Gemini 1.5 Flash và trả về câu trả lời ngắn gọn.

```python
import os
import google.generativeai as genai

# 1. Lấy API key từ biến môi trường (đã thiết lập trước đó)
genai.configure(api_key=os.environ["API_KEY"])

# 2. Khởi tạo mô hình
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(question: str) -> str:
    """Gửi câu hỏi tới Gemini và trả về văn bản."""
    response = model.generate_content(question)
    return response.text.strip()

# Ví dụ sử dụng
if __name__ == "__main__":
    user_q = "What is the capital of Vietnam?"
    answer = ask_gemini(user_q)
    print(f"Q: {user_q}\nA: {answer}")
```

**Giải thích**:
- Dòng `genai.configure` thiết lập xác thực bằng API key.  
- `GenerativeModel("gemini-1.5-flash")` chọn mô hình Flash (miễn phí, hỗ trợ fine‑tuning).  
- Hàm `ask_gemini` gọi `generate_content` và trả về chuỗi văn bản đã loại bỏ khoảng trắng thừa.  
- Khi chạy, chương trình sẽ in ra câu trả lời cho câu hỏi “What is the capital of Vietnam?” (kết quả mong đợi là “Hà Nội”).

## 5. Tổng kết

- Gemini API cung cấp bộ công cụ đa modal (văn bản, hình ảnh, video, âm thanh, tài liệu) cùng với các tính năng nâng cao như fine‑tuning miễn phí, context caching, code execution và structured outputs.  
- Hai mô hình chính là Gemini 1.5 Flash (nhỏ, giá rẻ, fine‑tune miễn phí) và Gemini 1.5 Pro (mạnh hơn).  
- Bạn có thể bắt đầu ngay lập tức bằng cách lấy API key miễn phí từ Google AI Studio, sau đó chạy vài dòng code Python để tạo nội dung hoặc xây dựng chatbot.  
- Mức phí sử dụng rất linh hoạt: gói miễn phí cho 1.500 request/ngày (≈1,5 tỷ token/ngày) với Gemini 1.5 Flash, và gói trả phí cho nhu cầu sản xuất; giá của Flash đã giảm 70 % gần đây.  
- Fine‑tuning Gemini 1.5 Flash cũng miễn phí trong AI Studio và mô hình sau tuning có thể thay thế trực tiếp mà không tăng chi phí sử dụng.  

Với những điểm trên, Gemini API là một lựa chọn mạnh mẽ và tiết kiệm cho những nhà phát triển muốn tích hợp AI sinh tạo vào ứng dụng của mình. Hãy thử ngay hôm nay và khám phá những khả năng mà Gemini mang lại!