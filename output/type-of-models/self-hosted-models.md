# Hướng dẫn tự host mô hình ngôn ngữ lớn (LLM) trên Kubernetes với Plural

## 1. Mục tiêu học tập

- Hiểu lý do tại sao các doanh nghiệp chọn tự host LLM thay vì dùng dịch vụ đám mây.
- Nắm được các lợi thế chính về bảo mật, chi phí và tùy chỉnh khi tự host.
- Biết cách lựa chọn và triển khai các giải pháp tự host phổ biến: OpenLLM + Yatai, Ray Serve và Hugging Face TGI.
- Hiểu yêu cầu phần cứng, phần mềm và các kỹ thuật tối ưu hoá để đạt hiệu suất tốt.
- Nắm được quy trình triển khai một ứng dụng LLM cơ bản trên Kubernetes bằng Plural.

## 2. Tổng quan

Trong thời đại dữ liệu, mô hình ngôn ngữ lớn (LLM) như ChatGPT đã trở thành công cụ then chốt để tự động hoá công việc, tạo nội dung và hỗ trợ quyết định. Tuy nhiên, việc sử dụng các dịch vụ đám mây công khai (OpenAI, ChatGPT…) thường gây ra lo ngại về bảo mật dữ liệu, chi phí sử dụng và sự phụ thuộc vào nhà cung cấp. Đối với các ngành có quy định chặt chẽ (y tế, tài chính…) hoặc các tổ chức muốn kiểm soát hoàn toàn cơ sở hạ tầng, việc **tự host LLM** trên môi trường riêng – thường là Kubernetes – là giải pháp đáp ứng nhu cầu về:

- **Bảo mật và tuân thủ**: dữ liệu luôn nằm trong hạ tầng nội bộ, không được truyền ra bên ngoài.
- **Quản lý chi phí**: sau khoản đầu tư ban đầu, chi phí hoạt động trở nên có thể dự đoán, đặc biệt khi sử dụng LLM thường xuyên.
- **Tùy chỉnh và mở rộng**: khả năng tích hợp với các công cụ nội bộ, mở rộng mô hình, thay đổi cấu trúc serving mà không bị giới hạn bởi API của nhà cung cấp.

Bài học này sẽ cung cấp một cái nhìn toàn diện về các công cụ phổ biến (OpenLLM, Ray Serve, Hugging Face TGI), cách Plural đơn giản hoá việc triển khai chúng trên Kubernetes, và các yếu tố cần cân nhắc trước khi quyết định tự host.

## 3. Kiến thức cốt lõi

### 3.1 Lý do chọn tự host LLM

| Yếu tố | Mô tả |
|--------|-------|
| **Bảo mật và quyền sở hữu dữ liệu** | Khi dùng dịch vụ đám mây, dữ liệu đầu vào (ví dụ: tin nhắn khách hàng, tài liệu nội bộ) có thể được lưu lại và sử dụng để huấn luyện mô hình. Tự host giữ dữ liệu hoàn toàn trong hệ thống nội bộ, đáp ứng yêu cầu GDPR, HIPAA, PCI‑DSS… |
| **Chi phí dài hạn** | Dịch vụ đám mây thường tính phí theo token hoặc thời gian sử dụng. Khi lượng truy vấn cao, chi phí có thể tăng nhanh. Tự host cần đầu tư phần cứng ban đầu nhưng sau đó chỉ phải trả cho điện, lưu trữ và bảo trì, leading to predictable OPEX. |
| **Tùy chỉnh và mở rộng** | Các nền tảng tự host cho phép thay đổi cấu hình serving (batch size, token streaming, quantization…) và tích hợp với các pipeline nội bộ (data ingestion, fine‑tuning, monitoring) mà không bị hạn chế bởi API công khai. |
| **Tránh vendor lock‑in** | Sử dụng mã nguồn mở và chuẩn Kubernetes giúp di chuyển giữa các nhà cung cấp hạ tầng hoặc đưa hệ thống on‑prem mà không phải viết lại ứng dụng. |

### 3.2 Các thách thức khi tự host

- **Yếu tố phần cứng**: Mô hình lớn (7B+ tham số) đòi hỏi RAM lớn (32 GB – ≥128 GB) và GPU mạnh (NVIDIA A100, RTX 4090…) để đạt latency chấp nhận được.
- **Kỹ năng đội ngũ**: Cần biết về Kubernetes, containerization, và các công cụ serving (Ray, BentoML, TGI…).
- **Quản lý phiên bản và cập nhật**: Các mô hình và thư viện có sự thay đổi thường xuyên; cần có quy trình CI/CD để cập nhật an toàn.
- **Giám sát và логистика**: Để đảm bảo SLA, cần tích hợp monitoring (Prometheus/Grafana), logging và autoscaling.

### 3.3 Giải pháp tự host phổ biến

| Công cụ | Điểm mạnh | Trường hợp sử dụng phù hợp |
|---------|-----------|----------------------------|
| **OpenLLM + Yatai** | - Đơn giản hoá serving qua một lệnh (`openllm start`).<br>- Hỗ trợ REST/gRPC, Web UI, client Python/JS.<br>- Tích hợp LangChain, BentoML, HuggingFace Agents.<br>- Quantization, token streaming, LoRA adapters (experimental).<br>- Yatai cung cấp khả năng mở rộng đa GPU/node trên Kubernetes, tương tự BentoCloud nhưng phí thấp hơn. | Ứng dụng RAG, chatbot nội bộ, khi muốn nhanh chóng triển khai và thử nghiệm mà không cần deep knowledge về serving infra. |
| **Ray Serve** | - Framework-agnostic: có thể serve PyTorch, TensorFlow, Scikit‑Learn, hoặc logic Python tùy chỉnh.<br>- Tích hợp sẵn dynamic batching, response streaming, multi‑node/multi‑GPU serving.<br>- Độ ổn định cao (được OpenAI sử dụng internally).<br>- Dashboard và metrics qua Prometheus.<br>- Hátshausen: cung cấp toàn bộ stack data‑processing, training, tuning, serving. | Khi cần một nền tảng thống nhất để xử lý dữ liệu, huấn luyện mô hình và serving trong cùng một cluster; phù hợp với workloads phức tạp và yêu cầu tối ưu hiệu suất cao. |
| **Hugging Face Text Generation Inference (TGI)** | - Đóng gói toàn bộ server trong container (Rust/Python/gRPC).<br>- Rất nhanh để chạy các mô hình HF pre‑trained (ví dụ: Llama‑2, Mistral).<br>- Hỗ trợ token streaming, quantization (bitsandbytes).<br>- Ít cấu hình ban đầu, thích hợp cho “off‑the‑shelf” serving. | Khi chỉ cần chạy một hoặc vài mô hình HF mà không muốn đầu tư vào việc xây dựng pipeline serving phức tạp. |

### 3.4 Yêu cầu phần cứng và phần mềm

- **RAM**:  
  - 7B‑model: ≥16 GB (chậm), khuyến nghị 32 GB+.  
  - 13B‑model: ≥32 GB, khuyến nghị 64 GB+.  
  - 40B‑model: ≥64 GB, thường cần 128 GB + để đạt latency tốt.  
- **GPU**: Đối với inference, một GPU có VRAM ≥ 24 GB (RTX 3090/4090, A100 40 GB) cung cấp throughput tốt. Đối với training/fine‑tuning, cần nhiều GPU hơn hoặc sử dụng técnicas như model parallelism.  
- **Storage**: SSD nhanh để load model weights và lưu trữ vector database (nếu dùng RAG).  
- **Phần mềm**: Docker/Kubernetes (phiên bản 1.24+), CUDA toolkit phù hợp với driver GPU, và các thư viện phục vụ (OpenLLM, Ray, TGI). Các công cụ監控: Prometheus, Grafana, Loki.  

### 3.5 Kỹ thuật tối ưu hoá hiệu suất

| Kỹ thuật | Mô tả |
|----------|-------|
| **Batching** | Xử lý nhiều request cùng một lúc để tăng throughput, giảm latency trung bình khi có lưu lượng đồng thời cao. |
| **Token streaming** | Trả về kết quả từng token thay vì chờ toàn bộ chuỗi, cải thiện trải nghiệm người dùng (đáp ứng nhanh hơn). |
| **Quantization** (int8, int4, bitsandbytes) | Giảm kích thước mô hình và RAM cần thiết, thường trade‑off độ chính xác nhẹ. |
| **Kernel optimization & model parallelism** | Sử dụng các kernel tối hoá (FlashAttention, Triton) và chia mô hình thành nhiều shard chạy trên nhiều GPU để giảm bộ nhớ mỗi GPU và tăng tốc tính toán. |
| **Caching & pre‑heating** | Lưu trữ kết quả của các truy vấn thường gặp trong Redis/Memcached; “pre‑heat” model bằng một số câu query ban đầu để giảm latency lần đầu. |
| **Container image optimization** | Sử dụng base image nhỏ (Distroless, Alpine), loại bỏ các package không cần thiết, áp dụng multi‑stage build để giảm kích thước image và thời gian pull. |
| **Streaming model weights** | Tải trọng số mô hình từ lưu trữ từng phần thay vì 전부 vào RAM, hữu ích khi RAM hạn chế và mô hình rất lớn. |

### 3.6 Quy trình triển khai cơ bản trên Kubernetes bằng Plural

1. **Chuẩn bị cluster**  
   - Tạo hoặc kết nối một cluster Kubernetes (có thể trên AWS EKS, GCP GKE, Azure AKS, hoặc on‑prem).  
   - Đảm bảo node có GPU được khai báo (`nvidia.com/gpu`) và đã cài đặt driver NVIDIA + device plugin.

2. **Cài đặt các ứng dụng từ Plural Marketplace**  
   - `plural bundle install ray` – triển khai Ray cluster với operator, dashboard và autoscaling.  
   - `plural bundle install yatai` – triển khai Yatai (BentoCloud open‑source) trên cùng cluster.  
   - `plural bundle install tgi` – triển khai Hugging Face TGI qua Helm chart (có sẵn trong marketplace).  

3. **Chuẩn bị model**  
   - Pull model từ Hugging Face (`mistralai/Mistral-7B-v0.1` hoặc `meta-llama/Llama-2-7b-chat-hf`).  
   - Nếu muốn quantization, sử dụng `bitsandbytes` hoặc `gguf` format.  
   - Lưu model vào một PVC hoặc sử dụng registry OCI (ví dụ: `ghcr.io/yourorg/llm-model:7b-q4`).  

4. **Cấu hình serving**  
   - **OpenLLM**:  
     ```bash
     openllm start mistral --model-repo /mnt/models/mistral \
                         --api-backend auto \
                         --port 8000
     ```  
   - **Ray Serve**: tạo deployment script Python, sau đó `serve run serve_script.py:entrypoint`.  
   - **TGI**:  
     ```bash
     text-generation-launcher \
       --model-id mistralai/Mistral-7B-v0.1 \
       --port 8080 \
       --max-batch-token-count 512 \
       --max-input-length 1024 \
     ```  

5. **Expose service**  
   - Tạo `Service` loại `LoadBalancer` hoặc `NodePort` và/hoặc `Ingress` (NGINX, Contour) để truy cập từ bên ngoài cluster.  

6. **Giám sát & scaling**  
   - Kết hợp Prometheus + Grafana để theo dõi latency, request/sec, GPU utilization.  
   - Kích hoạt Horizontal Pod Autoscaler (HPA) dựa trên metric `request_per_second` hoặc GPU utilization.  

7. **Kiểm thử**  
   - Gửi request test qua `curl` hoặc Python client:  
     ```bash
     curl -X POST http://<llm-service>/generate \
          -H "Content-Type: application/json" \
          -d '{"prompt":"Explain quantum computing in simple terms.", "max_new_tokens":128}'
     ```  
   - Kiểm tra latency, độ chính sách và tiêu thụ tài nguyên.  

## 4. Ví dụ minh họa

**Mục tiêu**: Triển khai một chatbot nội bộ sử dụng mô hình Mistral‑7B qua OpenLLM + Yatai trên cluster Kubernetes được quản lý bởi Plural.

**Bước 1 – Cài đặt Yatai**  
```bash
plural bundle install yatai
# Kiểm tra pod
kubectl get pods -n yatai
```

**Bước 2 – Chuẩn bị model PVC**  
```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mistral-7b-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: standard
EOF
```

**Bước 3 – Deploy OpenLLM với Yatai**  
```bash
# Tạo một ApplicationCustomResource (ACR) cho OpenLLM
cat <<EOF | kubectl apply -f -
apiVersion: core.plural.sh/v1alpha1
kind: Application
metadata:
  name: mistral-openllm
spec:
  chart: openllm
  values:
    replicaCount: 2
    model:
      name: mistralai/Mistral-7B-v0.1
      pvcName: mistral-7b-pvc
    service:
      type: ClusterIP
      port: 8000
    resources:
      limits:
        nvidia.com/gpu: 1
        memory: 32Gi
      requests:
        nvidia.com/gpu: 1
        memory: 16Gi
EOF
```

**Bước 4 – Expose qua Ingress**  
```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mistral-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: llm.internal.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mistral-openllm
            port:
              number: 8000
EOF
```

**Bước 5 – Kiểm thử**  
```bash
curl -s -X POST http://llm.internal.example.com/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt":"What is the capital of Vietnam?","max_new_tokens":32}' | jq .
```

**Kết quả mong đợi** (ví dụ):
```json
{
  "generated_text": "The capital of Vietnam is Hanoi."
}
```

Trong ví dụ này, chúng ta thấy cách Plural giúp giảm bớt công việc quản lý underlying infra (Ray, Yatai, TGI) và tập trung vào việc cấu hình model và serving logic.

## 5. Tổng kết

- Tự host LLM mang lại **kiểm soát dữ liệu**, **tiết kiệm chi phí dài hạn** và **khả năng tùy chỉnh cao**, đặc biệt quan trọng đối với các ngành có yêu cầu tuân thủ chặt chẽ.  
- Các giải pháp mã nguồn mở như **OpenLLM + Yatai**, **Ray Serve** và **Hugging Face TGI** cung cấp những mức độ khác nhau về sự đơn giản, khả năng mở rộng và tính năng serving, cho phép đội ngũ chọn dựa trên mức độ kiểm soát và sự phức tạp mà họ chấp nhận.  
- Yếu tố phần cứng (RAM, GPU) và kỹ thuật tối ưu hoá (batching, token streaming, quantization, model parallelism) trực tiếp ảnh hưởng đến latency và throughput; vì vậy cần đánh giá nhu cầu trước khi quyết định mô hình và hạ tầng.  
- **Plural** hoạt động như một “control plane” trên Kubernetes, cho phép triển khai nhanh các stack serving thông qua Marketplace, tự động hóa việc quản lý lifecycle (upgrade, scaling, monitoring) và giải phóng đội ngũ để tập trung vào xây dựng ứng dụng LLM thay vì維護 infra.  

Với kiến thức trên, bạn đã có thể đưa ra quyết định có reason-based về việc tự host LLM, lựa chọn công cụ phù hợp và triển khai một hệ dienst ổn định, bảo mật và tối ưu hoá trên môi trường Kubernetes. Chúc bạn thành công trong triển khai!