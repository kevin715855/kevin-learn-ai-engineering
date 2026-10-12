# Claude API: Lấy khóa và sử dụng API

## 1. Mục tiêu học tập
- Hiểu Claude API là gì và các mô hình có sẵn.
- Biết cách tạo tài khoản Anthropic, nạp credit và lấy khóa API.
- Thực hiện lệnh gọi API cơ bản bằng Postman (hoặc công cụ tương tự).
- Tuỳ chỉnh phản hồi của Claude bằng cách thay đổi prompt, system instructions và các tham số như temperature.
- Áp dụng Claude API vào ứng dụng nội bộ hoặc sản phẩm của riêng bạn.

## 2. Tổng quan
Claude là dòng mô hình AI của Anthropic, được huấn luyện bằng Constitutional AI để mang lại tính an toàn và khả năng reasoning mạnh. Claude API cho phép nhà phát triển tích hợp khả năng sinh văn bản,理解 tài liệu, xử lý hình ảnh, gọi công cụ và nhiều tính năng nâng cao vào ứng dụng của mình mà không cần người dùng truy cập Claude.ai trực tiếp. Bài học này hướng dẫn bạn từ việc lấy khóa API cho tới thực hiện第一次 gọi API thành công và tuỳ chỉnh hành vi của mô hình theo nhu cầu cụ thể.

## 3. Kiến thức cốt lõi

### 3.1 Claude API là gì
Claude API là giao diện lập trình ứng dụng (API) cho phép bạn gửi một **prompt** (đầu vào) tới mô hình Claude và nhận về một **response** (đầu ra). Bạn có thể sử dụng API để:
- Trả lời câu hỏi của khách hàng.
- Phân tích và tóm tắt tài liệu (PDF, văn bản).
- Sinh nội dung viết sáng tạo.
- Thực hiện quyết định phức tạp dựa trên logic.

### 3.2 Các mô hình Claude
| Mô hình | Đặc điểm chính | Trường hợp sử dụng phù hợp |
|---------|----------------|----------------------------|
| **Haiku** | Nhanh, thấp chi phí | Kiểm duyệt nội dung, trích xuất dữ liệu đơn giản |
| **Sonnet** | Cân bằng giữa thông minh và tốc độ | Mã hoá, phân tích dữ liệu, hầu hết các tác vụ thường ngày |
| **Opus** | Suy luận mạnh, chịu tải dài | Mã hoá tác cực, tác vụ cần suy luận sâu |
| **Fable** | Mạnh nhất, chất lượng đầu ra cao | Ứng dụng đòi hỏi reasoning phức tạp, tác vụ dài hạn |

Tất cả các mô hình chia sẻ cùng các tính năng core (Messages API, Vision, Document understanding, Citations, Extended thinking, Structured outputs, …) nhưng các mô hình cấp cao hơn trả về kết quả chính xác và tinh tế hơn.

### 3.3 Chi phí sử dụng
Claude API sử dụng mô hình trả trước *pay‑as‑you-go* dựa trên số **token** trong prompt (input) và trong response (output). Giá tính theotriệu token (≈750.000 từ):

| Mô hình | Giá input ($/triệu token) | Giá output ($/triệu token) |
|---------|---------------------------|----------------------------|
| Claude Fable 5.1 | 10 | 50 |
| Claude Opus 5.5 | 4 | 20 |
| Claude Sonnet 5.5 | 2 | 10 |
| Claude Haiku 5.5 | 0.10 | 0.50 |

Credit không thể hoàn lại và hết hạn sau 1 năm nếu không được sử dụng. Khi credit hết, tất cả các lệnh gọi sẽ bị từ chối cho tới khi nạp thêm.

### 3.4 Xác thực và cấu trúc yêu cầu
- **Endpoint**: `https://api.anthropic.com/v1/messages`
- **Phương thức HTTP**: `POST`
- **Headers bắt buộc**:
  - `x-api-key`: khóa API của bạn
  - `anthropic-version`: `2023-06-01` (hoặc phiên bản mới nhất trong tài liệu)
  - `content-type`: `application/json`
- **Body** (JSON) chứa tối thiểu:
  ```json
  {
    "model": "claude-sonnet-5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "Hello, world"
      }
    ]
  }
  ```
- Các tham số tùy chọn để tuỳ chỉnh: `system`, `temperature`, `top_p`, …

### 3.5 Tích hợp qua Zapier (tùy chọn)
Nếu bạn muốn nhanh chóng kết nối Claude với hơn 9.000 ứng dụng mà không viết code, Zapier cung cấp các sẵn có (Zap) như:
- Phân tích phản hồi Google Form và lưu vào Google Sheets.
- Tự độngSoạn thảo trả lời email trong Gmail.
- Tạo bài đăng LinkedIn từ bản ghi Airtable.
- Tạo bài đăng Facebook từ dữ liệu Google Sheets.

Zapier xử lý toàn bộ “plumbing” (xác thực, định dạng dữ liệu, gọi API) nên bạn chỉ cần tập trung vào lógica nghiệp vụ.

## 4. Ví dụ minh họa

### 4.1 Lấy khóa API (tóm tắt các bước)
1. Truy cập [Anthropic Console](https://console.anthropic.com/) và tạo tài khoản nhà phát triển.
2. Vào *Settings → Billing*, nhấn **Buy credits** và nạp tối th้อย $5.
3. Trong *Settings → API Keys*, nhấn **Create Key**, đặt tên (ví dụ: “Claude API Postman”) và **Add**.
4. Sao chép khóa hiển thị ngay lập tức và lưu trữ an toàn (password manager). Khóa sẽ không hiển thị lại sau khi đóng popup.

### 4.2 Gọi API đầu tiên bằng Postman
1. Mở Postman, tạo request mới → chọn **HTTP**.
2. Điền **URL**: `https://api.anthropic.com/v1/messages`.
3. Thêm headers:
   - `x-api-key`: <khóa của bạn>
   - `anthropic-version`: `2023-06-01`
   - `content-type`: `application/json`
4. Đặt method thành **POST**.
5. Trong tab **Body**, chọn **raw** → **JSON**, dán body mẫu:
   ```json
   {
     "model": "claude-sonnet-5",
     "max_tokens": 1024,
     "messages": [
       {
         "role": "user",
         "content": "Hello, world"
       }
     ]
   }
   ```
6. Nhấn **Send**. Nếu mọi thứ đúng, bạn sẽ nhận về HTTP 200 OK và phản hồi từ Claude, ví dụ:
   ```json
   {
     "id": "msg_01xxxxxx",
     "type": "message",
     "role": "assistant",
     "content": [
       {
         "type": "text",
         "text": "Hello! How can I assist you today?"
       }
     ],
     "model": "claude-sonnet-5",
     "stop_reason": "end_turn",
     "stop_sequence": null,
     "usage": {
       "input_tokens": 12,
       "output_tokens": 9
     }
   }
   ```

### 4.3 Thay đổi prompt và thêm system instruction
- Trong body, thay đổi `"content": "Hello, world"` thành `"content": "Describe the perfect dessert in a paragraph."`.
- Gửi lại → nhận được mô tả về món tráng miệng idéal.
- Thêm system instruction để buộc Claude luôn trả lời bằng câu hỏi:
  ```json
  {
    "model": "claude-sonnet-5",
    "max_tokens": 1024,
    "system": "Always answer the user prompt with a question, not an explanation.",
    "messages": [
      {
        "role": "user",
        "content": "Describe the perfect dessert in a paragraph."
      }
    ]
  }
  ```
- Gửi → Claude sẽ trả về một câu hỏi thay vì mô tả (ví dụ: “Bạn có muốn biết nguyên liệu nào để làm bánh này không?”).

### 4.4 Tuỳ chỉnh temperature
Thêm tham số `temperature` để điều khiển mức độ ngẫu nhiên:
```json
{
  "model": "claude-sonnet-5",
  "max_tokens": 1024,
  "temperature": 0.7,
  "messages": [
    {
      "role": "user",
      "content": "Write a short tagline for a coffee shop."
    }
  ]
}
```
- `temperature` gần 0 → phản hồi Deterministic, nhất quán.
- `temperature` cao (≥1) → phản hồi đa dạng, sáng tạo hơn.

### 4.5 Ví dụ tích hợp qua Zapier (mô tả ngắn)
1. Trong Zapier, tạo Zap mới.
2. Chọn trigger **Google Forms – New Form Response**.
3. Thêm action **Anthropic (Claude) – Create Message**, nhập prompt như:
   ```
   Summarize the following responses: {{Form Response}}
   ```
4. Thêm action **Google Sheets – Create Spreadsheet Row**, map output của Claude vào cột voulu.
5. Bật Zap → mỗi khi có phản hồi mới, Claude sẽ tóm tắt và lưu tự động vào Sheet.

## 5. Tổng kết
- Claude API cung cấp quyền truy cập mạnh mẽ vào khả năng reasoning, hiểu tài liệu và sinh nội dung của mô hình Claude qua các endpoint chuẩn REST.
- Quy trình sử dụng bao gồm: tạo tài khoản → nạp credit → lấy khóa API → cấu hình request (URL, headers, body) → gọi API và xử lý phản hồi.
- Bạn có thể thay đổi prompt, thêm system instructions, và các tham số như `temperature`, `max_tokens` để kiểm soát cách Claude trả lời.
- Đối với những ai muốn tránh viết code, Zapier cho phép kết nối Claude với hàng nghìn ứng dụng thông qua giao diện kéo‑thả, phù hợp với các nhiệm vụ tự động nhanh.
- Luôn bảo mật khóa API, theo dõi mức tiêu thụ credit để tránh gián đoạn dịch vụ. 

Bằng cách nắm vững các bước trên, bạn đã có thể bắt đầu tích hợp Claude API vào dự án của mình, từ prototyping nhanh cho tới sản xuất thực tế. Chúc bạn thành công!