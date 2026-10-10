# Hướng dẫn tổng quan về Function Calling trong LLM

## 1. Mục tiêu học tập  
Sau khi đọc bài học này, bạn sẽ able to:  

- Nêu khái niệm **function calling** (tool use) và cách nó mở rộng khả năng của LLM.  
- So sánh function calling với **retrieval‑augmented generation (RAG)** và指出 khi nào nên dùng từng phương pháp.  
- Mô tả quy trình hai‑lần gọi LLM khi thực hiện một function call.  
- Liệt kê một số mô hình LLM thương mại và mã nguồn mở hỗ trợ function calling.  
- Giải thích cách kết hợp function calling với RAG để tạo RAG‑agent mạnh mẽ hơn.  

## 2. Tổng quan  
Các mô hình ngôn ngữ lớn (LLM) hiện nay có thể tạo ra văn bản nhưng thường bị giới hạn bởi kiến thức được huấn luyện trước. Khi ứng dụng cần thông tin **thực‑time** (giá cổ phiếu, trạng thái đơn hàng, dự báo thời tiết…) hoặc muốn thực hiện hành động bên ngoài (gọi API, điều khiển thiết bị…), chỉ dựa trên nội dung sinh ra từ LLM là không đủ.  

**Function calling** là kỹ thuật cho phép LLM “gọi” các hàm hoặc API bên ngoài dựa trên mô tả hàm được cung cấp trong prompt. Kỹ thuật này cho phép LLM:  

- Chọn hàm phù hợp với ý định của người dùng.  
- Truyền tham số vào hàm dưới dạng JSON có cấu trúc.  
- Nhận kết quả trả về và tiếp tục sinh phản hồi cuối cùng dựa trên dữ liệu thực tế.  

Do đó, function hoạt động như một “cầu nối” giữa świat ngôn ngữ của LLM và świat dữ liệu hoặc dịch vụ thực tế.

## 3. Kiến thức cốt lõi  

### 3.1 Định danh và gốc nguồn  
- Function calling còn được gọi là **tool use** hoặc **API calling**.  
- Ý tưởng xuất phát từ việc cung cấp cho LLM một “danh sách công cụ” (functions) kèm mô tả JSON schema; LLM sẽ quyết định có cần gọi công cụ nào không và trả về gọi đó dưới dạng JSON.  

### 3.2 So sánh với RAG  
| Yếu tố | Function Calling | Retrieval‑augmented Generation (RAG) |
|--------|------------------|--------------------------------------|
| Nguồn dữ liệu | API hoặc hàm thực thi trực tiếp (có thể thay đổi mỗi lần gọi) | Cơ sở dữ liệu vector đã được chuẩn bị trước (index, embeddings) |
| Thời gian truy cập | Thực‑time (khi gọi hàm) | Dựa trên dữ liệu đã được ingest trước; có thể cũ nếu không cập nhật thường xuyên |
| Phạm vi ứng dụng | Truy vấn dịch vụ ngoài, thực hiện hành động, tính toán phức tạp | Truy xuất thông tin từ tài liệu, cơ sở kiến thức tĩnh |
| Độ phức tạp triển khai | Cần định nghĩa schema hàm và xử lý kết quả trả về | Cần xây dựng pipeline ingest → embed → vector store → retrieve |

**Khi nào dùng function calling?**  
- Ứng dụng cần dữ liệu thay đổi nhanh (ví dụ: giá crypto, trạng thái flight).  
- Yêu cầu thực hiện một hành động bên ngoài (đặt vé, gửi email, kích hoạt thiết bị IoT).  

**Khi nào dùng RAG?**  
- Kho kiến thức lớn nhưng ít thay đổi (tài liệu sản phẩm, kiến thức pháp lý).  
- Muốn giảm chi phí gọi API nhiều lần bằng cách truy xuất từ một kho dữ liệu nội bộ.  

### 3.3 Quy trình hai‑lần gọi LLM  
Giả sử người dùng hỏi: “Hôm nay thời tiết ở Hà Nội như thế nào?” và chúng ta có hàm `get_current_weather(city)`.  

1. **Lần gọi thứ nhất** – Ứng dụng gửi prompt cùng với danh sách hàm (kèm schema) tới LLM.  
   - LLM phân tích ý định → xác định cần gọi hàm `get_current_weather`.  
   - LLM trả về một đối JSON, ví dụ:  

   ```json
   {
     "name": "get_current_weather",
     "arguments": { "city": "Hà Nội" }
   }
   ```

2. **Lực lượng ứng dụng** phân tích JSON, thực hiện hàm (gọi API thời tiết) và nhận kết quả (ví dụ: `{ "temperature": 28, "condition": "nắng" }`).  

3. **Lần gọi thứ hai** – Ứng dụng ghép kết quả hàm vào prompt gốc (thêm như “Thời tiết Hà Nội: 28°C, nắng”) và gửi lại cho LLM.  
   - LLM dựa trên thông tin thực tế này để sinh câu trả lời cuối cùng: “Hôm nay Hà Nội có nắng, nhiệt độ khoảng 28°C.”  

### 3.4 Kết hợp Function Calling với RAG (RAG‑Agent)  
Một **RAG‑Agent** sử dụng cả hai kỹ thuật:  

- **Bước truy xuất (RAG)**: Lấy phần tài liệu liên quan từ vector store dựa trên truy vấn của người dùng.  
- **Bước thực thi (Function Calling)**: Áp dụng một hàm đã định nghĩa trên dữ liệu đã lấy được (ví dụ: hàm `format_product_spec(spec)` để chuyển spec thô thành câu trả lời dễ đọc).  

Lợi thế:  
- Đảm bảo câu trả lời dựa trên cả **tri thức tĩnh** (tài liệu) và **dữ liệu động** (API).  
- Giảmภาร práce manual vì Agent tự quyết định khi nào cần truy xuất, khi nào cần gọi hàm.  

### 3.5 Một số LLM hỗ trợ Function Calling (trước ngày 17/05/2024)  

| Nhóm | Mô hình | Điểm nổi bật |
|------|---------|--------------|
| **Thương mại** | OpenAI GPT‑4, GPT‑3.5 Turbo | API chuẩn, trả về JSON `{name, arguments}`. |
|  | Google Gemini (Vertex AI, AI Studio) | Hỗ trợ khai báo function qua Vertex AI. |
|  | Anthropic Claude 3 series | Cung cấp endpoint cho tool use tương tự OpenAI. |
|  | Cohere Command R / Command R+ | API cho function calling, dễ integ vào Cohere Playground. |
| **Mã nguồn mở** | Mistral 7B‑Instruct | Đã thể hiện khả năng function calling qua các test community. |
|  | NexusRaven‑V2‑13B | Được tối ưu cho gọi công cụ bảo mật, vượt qua GPT‑4 trong một số benchmark. |
|  | Gorilla OpenFunctions (7B) | Được fine‑tune trên tài liệu API, sinh function call chính xác từ ngôn ngữ tự nhiên. |
|  | FireFunction V1 (based on Mixtral 8x7B) | Chất lượng gần GPT‑4 cho các task cấu trúc JSON và định tuyến quyết định. |
|  | Nous Hermes 2 Pro (7B) | 90% accuracy trên benchmark function calling, 81% trên JSON struct output. |

> **Lưu ý:** Danh sách trên dựa trên thông tin công khai từ nhà cung cấp và các báo cáo đánh giá tại thời điểm viết bài. Khi triển khai, bạn nên kiểm tra tài liệu phiên bản cụ thể để xác nhận hỗ trợ function calling.

## 4. Ví dụ minh họa  

### 4.1 Định nghĩa hàm thời tiết (JSON Schema)  

```json
{
  "name": "get_current_weather",
  "description": "Lấy dữ liệu thời tiết hiện tại cho một thành phố.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "Tên thành phố, ví dụ: Hà Nội, New York"
      }
    },
    "required": ["city"]
  }
}
```

### 4.2 Phản hồi LLM (lần gọi pertama)  

```json
{
  "name": "get_current_weather",
  "arguments": {
    "city": "Hà Nội"
  }
}
```

### 4.3 Kết quả từ API thời tiết (giả lập)  

```json
{
  "temperature": 27,
  "condition": "nhiều mây",
  "humidity": 78
}
```

### 4.4 Prompt lần gọi thứ hai (được enrich)  

```
Người dùng: Hôm nay thời tiết ở Hà Nội như thế nào?
Kết quả từ hàm: { "temperature": 27, "condition": "nhiều mây", "humidity": 78 }
```

### 4.5 Phản hồi cuối cùng từ LLM  

> “Hôm nay Hà Nội có nhiều mây, nhiệt độ khoảng 27°C và độ ẩm 78%.”  

Quá trình trên minh họa rõ ràng cách function calling cho phép LLM truy cập dữ liệu thực ‑time và tạo ra câu trả lời đáng tin cậy.

## 5. Tổng kết  

- **Function calling** cho phép LLM gọi các hàm hoặc API bên ngoài, таким образом mở rộng khả năng từ chỉ sinh ra văn bản sang thực hiện hành động và truy xuất dữ liệu động.  
- Kỹ thuật này complémentary với **RAG**: RAG cung cấp kiến thức tĩnh, còn function calling cung cấp dữ liệu real‑time và khả năng thực hiện thao tác.  
- Quy trình thực hiện bao gồm hai lần gọi LLM: lần đầu để xác định hàm và tham số, lần hai để sinh trả lời sau khi có kết quả hàm.  
- Nhiều LLM thương mại (GPT‑4, Gemini, Claude 3, Cohere Command) và mã nguồn mở (Mistral, NexusRaven, Gorilla OpenFunctions, FireFunction, Nous Hermes 2 Pro) đã hỗ trợ tính năng này.  
- Khi xây dựng **AI agent** hoặc **RAG‑agent**, kết hợp cả hai phương pháp sẽ cho ra hệ thống mạnh mẽ, linh hoạt và có thể đáp ứng các trường hợp sử dụng từ truy xuất tài liệu đến tương tác với dịch vụ bên ngoài.  

Bằng cách nắm vững nguyên tắc và quy trình trên, bạn sẽ có thể bắt đầu tích hợp function calling vào các ứng dụng LLM của mình và khai thác tối đa tiềm năng của mô hình ngôn ngữ lớn trong môi trường thực tế.