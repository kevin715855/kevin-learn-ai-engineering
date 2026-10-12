# Hướng dẫn gỡ lỗi, truy vết và giám sát mô hình LLM

## 1. Mục tiêu học tập

Sau khi hoàn thành bài học, người học sẽ có thể:

- Nắm vững khái niệm **debugging** (gỡ lỗi), **tracing** (truy vết) và **monitoring** (giám sát) trong ngữ cảnh các mô hình ngôn ngữ lớn (LLM).  
- Hiểu cách chúng ta có thể sử dụng **Weights & Biases (wandb)** trên nền tảng **CoreWeave Forge** để thu thập, trực quan hóa và phân tích dữ liệu từ quá trình suy luận LLM.  
- Áp dụng các kỹ thuật cơ bản để đo lường hiệu suất, phát hiện lỗi và cải thiện độ tin cậy của hệ thống LLM trong thực tế.

## 2. Tổng quan

Việc triển khai mô hình LLM trong sản xuất thường gặp thách thức như độ trễ không ổn định, đầu ra không mong muốn hoặc tiêu thụ tài nguyên vượt mức dự kiến. Để khắc phục những vấn đề này, nhóm phát triển cần có một quy trình **debugging**, **tracing** và **monitoring** đồng bộ. 

Bài học này dựa trên hướng dẫn có tiêu đề *“A guide to LLM debugging, tracing and monitoring”* được lưu trữ trên **Weights & Biases** qua trang **Forge** của CoreWeave. Mặc dù chúng ta không có nội dung chi tiết của hướng dẫn, nhưng chúng ta có thể tóm tắt các thành phần chung mà một hướng dẫn như vậy thường bao gồm:

- **Instrumentation**: thêm mã ghi log, đo thời gian và捕获 các sự kiện chính trong quá trình inference.  
- **Logging & Metrics**: thu thập các chỉ số như latency, throughput, token usage,以及模型输出的统计特性（例如，重复率、毒性分数）。  
- **Tracing**: xây dựng đồ thị gọi hàm (call graph) để xem luồng dữ liệu từ input qua các lớp transformer cho đến output, giúp xác định vị trí tắc nghẽn hoặc lỗi logic.  
- **Visualization & Alerts**: sử dụng công cụ như wandb để tạo bảng điều khiển (dashboard) hiển thị các chỉ số theo thời gian thực và thiết lập cảnh báo khi các chỉ số vượt ngưỡng cho phép.  
- **Experiment Tracking**: lưu trữ từng lần chạy (run) với các siêu tham số, phiên bản mô hình và kết quả đánh giá để dễ dàng so sánh và quay lại phiên bản tốt nhất.

## 3. Kiến thức cốt lõi

### 3.1. Debugging LLM

Debugging trong LLM tập trung vào việc tìm ra tại sao mô hình tạo ra đầu ra không mong muốn (ví dụ: trả lời sai, tạo ra nội dung nhạy cảm, hoặc lặp lại). Các bước thường见包括:

1. **Kiểm tra input**: xem liệu đầu vào có chứa lỗi chính tả, ngữ pháp không chuẩn hoặc ngữ cảnh thiếu sót không.  
2. **Giám sát logits**: nhìn vào phân phối xác suất của các token ở mỗi bước để xác định xem mô hình có “lúng túng” giữa nhiều lựa chọn hay không.  
3. **Kiểm tra phần mã hóa (tokenizer)**: đảm bảo rằng quá trình chia câu thành token không làm mất thông tin quan trọng.  

### 3.2. Tracing (Truy vết)

Tracing cho phép chúng ta ghi lại toàn bộ hành trình của một yêu cầu inference:

- **Span**: mỗi hoạt động (ví dụ: embedding, self‑attention, feed‑forward, projection) được biểu diễn bằng một span có timestamp và thời gian thực thi.  
- **Parent‑Child Relationship**: spans được kết hợp thành một cây gọi hàm, giúp nhìn thấy quais hoạt động chiếm maggiorn phần thời gian.  
- **Correlation ID**: một định danh duy nhất được gắn cho mỗi request để nối các log từ các dịch vụ khác nhau (API gateway, inference server, logging backend).  

### 3.3. Monitoring (Giám sát)

Giám sát tập trung vào việc đo lường các chỉ số sức khỏe của hệ thống trên thời gian thực:

| Chỉ số | Ý nghĩa | Cách thu thập |
|--------|---------|---------------|
| **Latency** (trễ) | Thời gian từ khi nhận request đến khi trả về response | Đo thời gian bắt đầu và kết thúc của toàn bộ span |
| **Throughput** | Số request xử lý được mỗi giây | Đếm số span hoàn thành trong cửa sổ thời gian |
| **Token usage** | Số token input + output | Tổng hợp từ tokenizer log |
| **Error rate** | Tỷ lệ request trả về lỗi (HTTP 5xx, exception) | Đếm span có trường `error=true` |
| **Output quality** | Các chỉ số nội dung (độ sôi nổi, toxic, повторения) | Tính toán后处理 trên output text |

Các chỉ số này thường được gửi tới một backend thời gian thực (ví dụ: wandb) để vẽ biểu đồ và tạo cảnh báo.

## 4. Ví dụ minh họa

Giả sử chúng ta có một endpoint inference `/generate` chạy trên CoreWeave Forge, và chúng ta muốn sử dụng wandb để ghi log và trace mỗi request. Dưới đây là một đoạn code Python minh họa cách instrumentation cơ bản (đo thời gian, log metrics và tạo span):

```python
import time
import wandb
from flask import Flask, request, jsonify

app = Flask(__name__)

# Khởi tạo wandb run (có thể reuse cho nhiều request)
wandb.init(project="llm-monitoring", name="forge-inference")

@app.route("/generate", methods=["POST"])
def generate():
    start = time.time()  # bắt đầu đo latency

    # 1. Đọc input
    data = request.get_json()
    prompt = data.get("prompt", "")
    max_new_tokens = data.get("max_new_tokens", 50)

    # 2. Gọi model (giả sử hàm `model.generate` đã được định nghĩa ailleurs)
    output_ids = model.generate(
        prompt,
        max_new_tokens=max_new_tokens,
        return_dict_in_generate=True,
        output_scores=True,
    )
    output_text = tokenizer.decode(output_ids.sequences[0], skip_special_tokens=True)

    # 3. Tính toán metrics
    latency_ms = (time.time() - start) * 1000
    input_tokens = len(tokenizer.encode(prompt))
    output_tokens = len(tokenizer.encode(output_text))
    total_tokens = input_tokens + output_tokens

    # 4. Ghi log tới wandb (tự động tạo một step cho mỗi request)
    wandb.log({
        "latency_ms": latency_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "request_id": wandb.run.id,  # sử dụng run ID làm correlation ID
    })

    # 5. Trả về kết quả
    return jsonify({
        "generated_text": output_text,
        "latency_ms": latency_ms,
        "token_usage": {"input": input_tokens, "output": output_tokens}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

**Giải thích ví dụ**:

- **Latency** được đo bằng `time.time()` trước và sau khi gọi model.  
- **Token usage** được tính bằng tokenizer để biết mô hình tiêu thụ bao nhiều token.  
- Mỗi request đều gọi `wandb.log` để gửi các chỉ số lên dashboard wandb; wandb tự động gán một **step** tăng dần, cho phép chúng ta vẽ biểu đồ theo thời gian.  
- `wandb.run.id` hoạt động như một **correlation ID**, giúp liên kết log này với các log khác (ví dụ: log từ máy chủ inference hoặc từ hệ thống queue) trong cùng một trace.

Trong môi trường thực tế trên **Forge**, chúng ta có thể triển khai đoạn code này như một service Docker, sau đó sử dụng wandb UI để:

- Xem biểu đồ latency trung bình và phân position (p50, p95, p99).  
- Thiết lập cảnh báo khi latency vượt qua 200ms hoặc error rate > 1%.  
- Truy vết từng request qua tab **Traces** của wandb để xem chi tiết từng span (nếu chúng ta mở rộng instrumentation để tạo span cho mỗi lớp transformer).

## 5. Tổng kết

- Debugging, tracing và monitoring là ba pilar nền tảng để duy trì độ tin cậy và hiệu suất của hệ thống LLM trong sản xuất.  
- Weights & Biases (wandb) cung cấp một nền tảng thống一 để **lưu trữ**, **trực quan hoá** và **cảnh báo** các chỉ số quan trọng, trong khi CoreWeave Forge cung cấp môi trường tính toán mạnh mẽ để chạy các workload inference.  
- Bằng cách thêm instrumentation đơn giản (đo thời gian, counting token, ghi log với wandb) vào mã inference, chúng ta có thể thu thập đủ dữ liệu để thực hiện debugging chi tiết, tracing đường đi thực thi và monitor sức khỏe hệ thống một cách tự động.  
- Những kỹ năng này giúp nhóm phát triển nhanh chóng tìm ra nguyên nhân gốc của vấn đề, tối ưu hóa tài nguyên và cung cấp trải nghiệm người dùng ổn định khi sử dụng các mô hình ngôn ngữ lớn.  

---  

*Lưu ý: Bài học này được biên soạn dựa trên thông tin có sẵn từ đường dẫn chỉ tới hướng dẫn “A guide to LLM debugging, tracing and monitoring” trên Weights & Biases qua Forge của CoreWeave. Các chi tiết cụ thể trong hướng dẫn gốc không được truy cập; vì vậy, bài học tập trung vào các khái niệm chung và phương pháp được công nhận trong cộng đồng AI Engineering.*