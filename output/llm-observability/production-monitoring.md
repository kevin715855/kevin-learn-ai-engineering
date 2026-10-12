# LLM Observability – Giám sát và hiểu hành vi mô hình ngôn ngữ lớn trong production  

## 1. Mục tiêu học tập  

Sau khi học xong bài này, bạn sẽ:  

- Giải thích ý nghĩa của **LLM observability** và vì sao nó khác biệt so với giám sát phần mềm truyền thống.  
- Nhận diện ba chiều quan trọng (operational, quality, safety) và sáu cột則 (performance monitoring, drift detection, hallucination tracking, cost analysis, latency monitoring, safety & compliance monitoring).  
- Liệt kê các chỉ số (metrics) cần theo dõi cho từng chiều và cột.  
- Mô tả quy trình triển khai LLM observability từ giai đoạn instrument pipeline tới tích hợp với AI governance.  
- Phân biệt LLM observability với truyền thống ML monitoring và hiểu tại sao cần có cả observability và supervision trong sản xuất.  

## 2. Tổng quan  

Các mô hình LLM (Large Language Model) có tính **phi xác định** (non‑deterministic): cùng một prompt có thể cho ra các phản hồi khác nhau tùy vào temperature, context window, hoặc các biến thiên ngầm. Do đó, giám sát chỉ dựa trên latency, error rate hoặc throughput (như trong phần mềm truyền thống) không đủ để phát hiện các lỗi nh량 hoặc nguy hiểm như **hallucination**, rò rỉ dữ liệu, hoặc偏 bias.  

**LLM observability** là disciplina chuyên môn trong AI observability, tập trung thu thập, phân tích và giải thích các tín hiệu (signals) cho thấy mô hình LLM đang hoạt động **đúng, an toàn và phù hợp với mục tiêu kinh doanh**. Nó mở rộng ba trụ cột truyền thống (logs, metrics, traces) bằng việc đánh giá ngữ nghĩa output, theo dõi chất lượng prompt‑response, và giám sát các hành vi có hại.  

## 3. Kiến thức cốt lõi  

### 3.1 Ba chiều của LLM Observability  

| Chiều | Mô tả | Câu hỏi trả lời |
|-------|-------|-----------------|
| **Operational observability** | Theo dõi hạ tầng và hiệu suất mô hình: latency, throughput, error rate, tài nguyên, chi phí. | “Model có đang chạy?” |
| **Quality observability** | Đánh giá nội dung ngữ nghĩa của output: accuracy, relevance, coherence, groundedness, consistency. | “Model có tạo ra output tốt?” |
| **Safety observability** | Giám sát hành vi có hại: hallucination, vi phạm policy, rò rỉ PII, bias amplification, prompt injection. | “Model có hoạt động an toàn?” |

Ba chiều này **liên kết**; chỉ quan tâm một chiều không đủ để đánh giá toàn diện.  

### 3.2 Sáu cột则 (pillars) của LLM Observability  

1. **Performance Monitoring** – latency (TTFT, end‑to‑end), throughput, error rate, tài nguyên GPU/CPU.  
2. **Drift Detection** – phát hiện thay đổi về input, output, retrieval, hành vi so với baseline (Jensen‑Shannon divergence, embedding distance, …).  
3. **Hallucination Tracking** – groundedness evaluation, consistency checking, factual verification, confidence calibration.  
4. **Cost Analysis** – token input/output, cost per interaction, cost‑efficiency, waste identification.  
5. **Latency Monitoring** – queue time, TTFT, inter‑token latency, end‑to‑end latency; theo dõi tại các percentile (p50, p95, p99).  
6. **Safety & Compliance Monitoring** – toxicity detection, PII exposure, policy compliance, prompt injection detection, bias monitoring.  

### 3.3 Các chỉ số (metrics) quan trọng  

| Nhóm | Chỉ số | Ý nghĩa |
|------|--------|---------|
| **Quality** | Answer relevance, Faithfulness/Groundedness, Completeness, Coherence, Toxicity score | Đánh giá độ tốt của phản hồi. |
| **Operational** | TTFT, Tokens/second, Request success rate, Token utilization | Hiệu suất và khả năng mở rộng. |
| **Business** | Cost per conversation, Resolution rate, User satisfaction signals, Escalation rate | Tác động tới kinh nghiệm người dùng và chi phí. |
| **Safety** | Hallucination rate, Guardrail trigger rate, Prompt injection detection rate, PII leak rate | Mức độ rủi ro và vi phạm. |

### 3.4 LLM Observability vs. Traditional ML Monitoring  

| Yếu tố | Traditional ML Monitoring | LLM Observability |
|--------|---------------------------|-------------------|
| **Input** | Structured, fixed‑dimension → theo dõi distribution của từng feature. | Unstructured natural language → cần embedding, topic classification, semantic evaluation. |
| **Output** | Numerical / categorical → accuracy, precision, recall tính toán được khi có ground truth. | Free‑form text → cần judgment về relevance, coherence, factual accuracy (thường dùng LLM‑as‑judge). |
| **Failure modes** | Predictable (wrong class, sai số regression). | Hallucination trông giống câu đúng; lỗi ngầm, context‑dependent. |
| **Statefulness** | Stateless – mỗi prediction độc lập. | Stateful – cuộc trò chuyện đa luồng, agent workflow; cần đánh giá toàn bộ interaction. |
| **Cost structure** | Rẻ per prediction → cost monitoring thường là thứ hai. | Đắt và biến động theo token → cost monitoring bắt buộc từ ngày đầu. |

### 3.5 Công cụ và nền tảng  

- **Dedicated AI Observability Platforms** – Arize, Fiddler, Langfuse (dashboard, alerting, trace visualization).  
- **Open‑source Frameworks** – OpenTelemetry (với extension AI), Langfuse, Phoenix (tùy chỉnh cao, cần đầu tư engineering).  
- **Integrated AI Trust Platforms** – kết hợp observabilité + evaluation + supervision (ví dụ: Swept AI) để can thiệp thực thời trước khi output đến người dùng.  

### 3.6 Quy trình triển khai LLM Observability  

1. **Instrument your LLM pipeline** – ghi log mọi prompt, response với trace ID duy nhất;捕获 model version, temperature, token counts; đo latency ở từng giai đoạn; gán cost dựa trên token × giá.  
2. **Establish baselines** – trong giai đoạn rollout hoặc pilot, thu thập giá trị bình thường cho mỗi metric (latency, token consumption, hallucination rate, …) để làm tham chiếu phát hiện drift.  
3. **Configure automated evaluation** – kết hợp rule‑based (PII, banned terms), classifier‑based (hallucination, toxicity), LLM‑as‑judge (relevance, accuracy), và reference‑based (so sánh với golden answer hoặc retrieved context).  
4. **Build alerting & escalation** – định nghĩa ngưỡng dựa trên tác động kinh doanh (ví dụ: 10% tăng hallucination rate có thể chấp nhận được cho chatbot sáng tạo nhưng không cho hệ thống y tế); thiết lập quy trình điều tra và can thiệp (tune prompt, rollback model, …).  
5. **Create feedback loops** – chuyển lỗi production thành test case; sử dụng drift pattern để điều chỉnh prompt hoặc retrieval pipeline; phân tích cost để tối ưu context window hoặc chọn model hiệu quả hơn; lấy tín hiệu удовлетворенnost người dùng để ưu ý cải thiện chất lượng.  
6. **Integrate with Governance** – kết nối dashboard và audit log tới AI governance đểチーム compliance, risk, và exécutive có thể truy cập báo cáo, giám sát xu hướng, và liên kết hành vi mô hình với kết quả kinh doanh.  

### 3.7 Từ Observability tới Supervision  

- **Observability** trả lời: “Model đang làm gì?” (detect hallucination, drift, …).  
- **Supervision** trả lời: “Model được phép làm gì?” (can thiệp thực thời để chặn output có hại trước khi đến người dùng).  
- Các组织 thường trải qua 4 giai đoạn:  
  1. No monitoring → chỉ phát hiện qua khiếu nại người dùng.  
  2. Basic monitoring → chỉ latency/errors.  
  3. LLM observability → thêm quality, safety, cost, drift.  
  4. Active supervision → observability + can thiệp thực thời.  

## 4. Ví dụ minh họa  

Giả sử chúng ta đang xây dựng một chatbot hỗ trợ khách hàng cho một công ty bảo hiểm. Pipeline đơn giản gồm:  

1. Nhận tin nhắn từ người dùng → **prompt**.  
2. Truy xuất cơ sở kiến thức (RAG) → **context**.  
3. Gửi prompt + context tới LLM → **response**.  
4. Áp dụng guardrail (toxicity, PII) → **final output** gửi lại người dùng.  

**Instrumentation (pseudo‑code Python)**  

```python
import uuid
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# ---- OpenTelemetry setup (for demonstration) ----
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

def call_llm(prompt: str, context: str, model_version: str, temperature: float):
    trace_id = str(uuid.uuid4())
    with tracer.start_as_current_span("llm_inference") as span:
        span.set_attribute("trace.id", trace_id)
        span.set_attribute("model.version", model_version)
        span.set_attribute("temperature", temperature)

        # 1. Measure retrieval latency
        t0 = time.time()
        retrieved_context = retrieve_from_kb(context)   # giả định hàm này
        span.set_attribute("retrieval.latency_ms", (time.time() - t0) * 1000)

        # 2. Build final prompt
        final_prompt = f"""Bạn là trợ lý bảo hiểm.
Ngữ cảnh: {retrieved_context}
Câu hỏi: {prompt}
Trả lời ngắn gọn, chính xác."""

        # 3. Call LLM (mock)
        t1 = time.time()
        raw_response = llm_generate(final_prompt, temperature)   # giả định hàm này
        span.set_attribute("llm.latency_ms", (time.time() - t1) * 1000)
        span.setAttribute("llm.input_tokens", count_tokens(final_prompt))
        span.setAttribute("llm.output_tokens", count_tokens(raw_response))

        # 4. Guardrail check (toxicity, PII)
        guardrail_start = time.time()
        safe_response = apply_guardrail(raw_response)   # trả về None nếu vi phạm
        span.setAttribute("guardrail.latency_ms", (time.time() - guardrail_start) * 1000)
        span.setAttribute("guardrail.passed", safe_response is not None)

        # 5. Evaluate quality (example: groundedness)
        quality_start = time.time()
        grounded_score = groundedness_eval(safe_response, retrieved_context)
        span.setAttribute("quality.groundedness", grounded_score)
        span.setAttribute("quality.eval.latency_ms", (time.time() - quality_start) * 1000)

        # 6. Cost estimation (假设 $0.00001 per token)
        cost = (span.attributes["llm.input_tokens"] + span.attributes["llm.output_tokens"]) * 0.00001
        span.setAttribute("cost.usd", cost)

        return safe_response or "Xin lỗi, tôi không thể trả lời lúc này."
```

**Giải thích ngắn:**  

- Mỗi lượt gọi LLM được gói trong một **span** OpenTelemetry, mang `trace.id` để liên hệ tất cả các giai đoạn (retrieval, LLM, guardrail, evaluation).  
- Các thuộc tính (attributes) ghi lại latency, token counts, model version, temperature – đây là dữ liệu cho **performance monitoring** và **cost analysis**.  
- Sau khi lấy phản hồi, chúng ta tính **groundedness score** (so sánh với context) → chỉ số cho **quality observability**.  
- Guardrail trả về `None` nếu phát hiện toxicity hoặc PII → contributo tới **safety observability**.  
- Tổng chi phí ước tính dựa trên số token → dùng cho **cost analysis**.  

Trong thực tế, chúng ta sẽ xuất các span này tới một backend observability (ví dụ: Langfuse, Arize) để xây dựng dashboard, thiết lập cảnh báo trên các ngưỡng như:  

- `hallucination_rate > 2%` → alert.  
- `guardrail.passed = false` → alert safety.  
- `cost.usd per request > $0.005` → alert cost.  

## 5. Tổng kết  

- **LLM observability** là khả năng giám sát, đo lường và hiểu hành vi của mô hình ngôn ngữ lớn trong môi trường sản xuất, mở rộng ba trụ cột truyền thống bằng đánh giá ngữ minh, chất lượng và an toàn.  
- Nó bao gồm **ba chiều** (operational, quality, safety) và **sáu cột则** (performance monitoring, drift detection, hallucination tracking, cost analysis, latency monitoring, safety & compliance monitoring).  
- Các chỉ số cần theo dõi bao gồm latency (TTFT, end‑to‑end), token consumption, answer relevance/faihfulness, hallucination rate, guardrail trigger rate, và cost per interaction.  
- So sánh với traditional ML monitoring, LLM observability phải xử lý input unstructured, output free‑text, failure modes không determinist, trạng thái hội thoại, và chi phí biến đổi theo token.  
- Quy trình triển khai bắt đầu bằng **instrument pipeline**, tạo **baselines**, thiết **automated evaluation**, định nghĩa **alerting & escalation**, xây dựng **feedback loops**, và cuối cùng **tích hợp với AI governance**.  
- Kết hợp observability với **supervision** cho phép can thiệp thực thời (ví dụ: chặn hallucination trước khi tới người dùng), nâng cấp từ đơn giản “detect” sang “prevent”.  

Việc đầu tư vào LLM observability từ đầu không chỉ giúp phát hiện sớm các vấn đề chất lượng, chi phí và rủi ro mà còn tạo nền tảng để cải tiến liên tục và đáp ứng yêu cầu về tuân thủ và quản trị AI trong doanh nghiệp.