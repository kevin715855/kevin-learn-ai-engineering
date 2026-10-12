# Streaming Responses trong AI: Cách các mô hình LLM tạo đầu ra thời gian thực

## 1. Mục tiêu học tập
- Hiểu khái niệm streaming response và tại sao nó tạo cảm giác “gõ 실시간” khi tương tác với LLM.  
- Biết cách LLMs sinh ra token một cách tuần tự và cách các chunk được gửi tới client.  
- Nắm vững các công nghệ hỗ trợ streaming: Server‑Sent Events (SSE), WebSocket, lập trình bất đồng bộ.  
- Giải thích vai trò của kiến trúc Transformer và các chiến lược decoding trong việc tối ưu pipeline streaming.  
- Thực hiện ví dụ mã nguồn trong Python, JavaScript và Java để gọi API streaming và hiển thị kết quả即时.  

## 2. Tổng quan
Khi người dùng gửi một câu hỏi tới một mô hình ngôn ngữ lớn (LLM) như GPT‑4, Bard… thay vì chờ đợi toàn bộ câu trả lời được tạo ra rồi mới hiển thị, hệ thống có thể trả về từng phần (token) ngay khi chúng được sinh ra. Cơ chế này được gọi **streaming response**. Nó làm tăng trải nghiệm người dùng bằng cách giảm thời gian phản hồi cảm nhận, tạo cảm giác như đang trò chuyện thực tế.  

Bài học này sẽ khai thác cách hoạt động của streaming từ cấp sinh token, qua các API và giao thức truyền dữ liệu, cho tới các tối ưu hóa ở mức mô hình và ví dụ mã nguồn thực tiễn.

## 3. Kiến thức cốt lõi

### 3.1 Token‑by‑Token Generation  
LLMs sinh ra văn bản dưới dạng chuỗi **token**. Một token có thể là:
- Một từ nguyên vẹn (ví dụ: “happy”)  
- Một phần từ (ví dụ: “happ-” trong “happiness”)  
- Một ký tự đơn lẻ (ví dụ: “a”, dấu phẩy “,”)  

Khi nhận được query, mô hình bắt đầu dự đoán token đầu tiên. Ngay sau khi token đó được xác định, nó được gửi ngay tới client. Quá trình lặp lại cho tới khi đạt được token kết thúc (ví dụ: `<|endoftext|>`). Do đó, luồng token được truyền liên tục tạo thành **streaming response**.

### 3.2 Streaming APIs  
Nhiều nhà cung cấp LLM (OpenAI, Azure, …) cung cấp tham số `stream` trong API. Khi `stream=True`:
1. Client gửi request kèm tham số stream.  
2. Server bắt đầu sinh token và đẩy chúng ra ngay khi sẵn sàng.  
3. Client nhận từng chunk và cập nhật giao diện theo thời gian thực.  

### 3.3 Công nghệ truyền stream  
- **Server‑Sent Events (SSE)**: giao thức HTTP đơn hướng cho phép server push dữ liệu dưới dạng các sự kiện `data:`. Mỗi sự kiện tương ứng với một chunk token.  
  ```text
  data: Hello
  data: how
  data: are
  data: you?
  ```
- **WebSocket**: kênh Full‑duplex, thường dùng trong ứng dụng cần tương tác hai chiều mạnh (soạn thảo cộng đồng, dashboard trực tiếp).  
- **Lập trình bất đồng bộ**: frameworks như `asyncio` (Python) hoặc `Node.js` cho phép server xử lý nhiều request đồng thời mà không block quá trình sinh token tiếp theo.

### 3.4 Tối ưu hoá pipeline trong LLM  
- **Kiến trúc Transformer**: xử lý song song đầu vào nhưng sinh ra output tuần tự; mỗi token phụ thuộc vào bối cảnh các token trước đó.  
- **Chiến lược decoding**:  
  - *Beam Search*: duy trì nhiều speculation, chọn chuỗi có xác suất cao nhất.  
  - *Sampling* (Top‑k, Nucleus): giới hạn tập token xem xét để cân bằng giữa chất lượng và sự đa dạng.  
Các chiến lược này giúp tạo token nhanh, ổn định và phù hợp với việc stream.

## 4. Ví dụ minh họa  

### 4.1 SSE mẫu (giả định server trả về)
```
data: Hello

data: how

data: are

data: you?
```

### 4.2 Python – gọi OpenAI API với streaming
```python
import openai

# Call the OpenAI API with streaming enabled
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True  # Enable streaming
)

# Stream the response token by token
for chunk in response:
    print(chunk.choices[0].delta.get("content", ""), end="", flush=True)
```

### 4.3 JavaScript (Node.js) – sử dụng fetch + ReadableStream
```javascript
const fetch = require('node-fetch');

async function getStreamedResponse() {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer YOUR_API_KEY`
        },
        body: JSON.stringify({
            model: 'gpt-4',
            messages: [{ role: 'user', content: 'Tell me a story' }],
            stream: true
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        console.log(decoder.decode(value, { stream: true }));
    }
}

getStreamedResponse();
```

### 4.4 Java – sử dụng HttpURLConnection
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class StreamingResponse {
    public static void main(String[] args) {
        try {
            URL url = new URL("https://api.openai.com/v1/chat/completions");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Authorization", "Bearer YOUR_API_KEY");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            String body = "{\"model\": \"gpt-4\", \"messages\": [{\"role\": \"user\", \"content\": \"Tell me a story\"}], \"stream\": true}";
            conn.getOutputStream().write(body.getBytes());

            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

> **Lưu ý**: Thay `YOUR_API_KEY` bằng khóa thực tế và đảm biến môi trường có thư viện cần thiết (openai cho Python, node-fetch cho JS, etc.).

## 5. Tổng kết
- Streaming response cho phép LLM trả về kết quả **ngay khi mỗi token được sinh**, tạo cảm giác tương tác mượt mà và thời gian thực.  
- Quy trình bao gồm sinh token tuần tự, gửi qua API có tham số `stream`, và sử dụng các công thái truyền stream như SSE, WebSocket hoặc kết nối HTTP thông thường.  
- Kiến trúc Transformer và các chiến lược decoding (Beam Search, Sampling) là nền tảng tối ưu hoá quá trình sinh token để đáp ứng yêu cầu tốc độ và chất lượng.  
- Các ví dụ mã nguồn trong Python, JavaScript, Java minh họa cách thực hiện streaming trên phía client.  
- Lợi ích rõ rệt là thời gian phản hồi cảm nhận ngắn, trải nghiệm người dùng tốt hơn và sử dụng tài nguyên hiệu quả; thách thức chính là phụ thuộc vào mạng lưới, cần xử lý lỗi đàs độ và tăng độ phức tạp triển khai.  

Với kiến thức trên, bạn có thể tích hợp streaming vào các ứng dụng AI chatbot, trợ lý ảo hoặc bất kỳ hệ thống tương tác nào muốn mang lại trải nghiệm “gõ real‑time” cho người dùng. Hãy thử áp dụng và phản hồi kết quả trong dự án của bạn!