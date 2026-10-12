# LLM Inference Trilemma: Throughput, Latency, và Chi phí

## 1. Mục tiêu học tập

- Nắm rõ sựConflict ba chiều giữa throughput, latency và chi phí khi triển khai mô hình LLM trong môi trường product.  
- Phân tích bốn thành phần chi phí thực tế (CapEx, OpEx, Opportunity Cost, Engineering Cost).  
- Xác định các lever kỹ thuật chính (kiến trúc mô hình, quantization, chiến lược parallelism, batching & scheduling) ảnh hưởng đến cả hiệu suất và chi phí.  
- Xác định khi nào nên ưu tiên throughput và khi nào nên ưuinten latency dựa trên đặc điểm workload.  
- Áp dụng quyết định hệ thống (Little’s Law, Roofline Model, quá trình benchmarking) để taille deployment một cách kinh tế nhất.  

## 2. Tổng quan

Trong dịch vụ web truyền thống, mở rộng thường đơn giản là thêm cân bằng tải và tăng số instance CPU khi lưu lượng tăng. Tuy nhiên, inference LLM không tuân theo quy luật này vì:

- **Stateful**: mỗi request cần duy trì trạng thái (KV cache) trên GPU.  
- **Bottleneck bởi bandwidth bộ nhớ** thay vì sức mạnh tính toán thô.  
- **Gắn liền với phần cứng cụ thể** (NVLink, InfiniBand) khiến việc chia sẻ tài nguyên giữa các mô hình bị hạn chế.  

Do đó, việc mở rộng LLM inference trở thành bài toán tối ưu đa chiều: nâng throughput thường làm tăng latency, giảm latency thường làm tăng chi phí, và attempts to cut cost force trade‑offs giữa hai kia. Ba chiều này được gọi là **trilemma**.

## 3. Kiến thức cốt lõi

### 3.1. Chi phí thực tế trong LLM inference  

Chi phí inference không chỉ là “$/token” mà là tổng của bốn chiều:

| Chiều | Mô tả | Ví dụ |
|-------|-------|-------|
| **Capital Cost (CapEx)** | Chi phí mua phần cứng node hoàn chỉnh (ví dụ: 8‑GPU H100 node). Không thể mua “½ node” do các GPU được kết nối bởi NVLink. | Một node 8×H100 mà mô hình 70B chỉ cần 4 GPU vẫn phải trả toàn bộ giá node. |
| **Operational Cost (OpEx)** | Điện, làm mát, hoặc phí thuê cloud hàng giờ. Node H100 tiêu thụ 10‑12 kW → điện hàng năm khoảng một vài nghìn USD; cloud trả theo giờ nhưng vẫn có “idling tax”. | Thuê H100 trên cloud trong giờ baixa thì仍需 trả phí即使 không có request. |
| **Opportunity Cost** | Lỗ hình do GPUIdle (ví dụ: 3 am) khi không có traffic. Do không dễ dán chia sẻ node giữa các mô hình mà không mất hiệu suất, idle GPU thành “ghost in the machine”. | Autoscaling giảm replica xuống 1 giữa 2 am‑6 am Pacific để lấy lại thời gian GPU idle. |
| **Engineering Cost** | Chi phí nhân lực chuyên biệt để tinh chỉnh stack (vLLM, TensorRT‑LLM, profiling with Nsight, quản lý CUDA). Tối ưu hóa có thể tốn tuầnuman‑giờ nhưng tiết kiệm chi phí phần cứng mỗi tháng. |Một nhóm dành 2‑3 tuần để tìm cấu hình quantization + parallelism tốt nhất cho mô hình 70B. |

### 3.2. Các lever ảnh hưởng chi phí  

#### 3.2.1. Kiến trúc mô hình – Dense vs. MoE  
- **Dense** (ví dụ: Llama 3 70B): tất cả tham số được kích hoạt mỗi token → chi phí tuyến tính với dung lượng HBM. Cần VRAM ≈ 2× model size (BF16) → 140 GB → ít nhất 2×H100 hoặc 1×MI300X.  
- **MoE** (DeepSeek‑V3, Mixtral): chỉ một_subset expert được kích hoạt mỗi token → tổng tham số lớn nhưng VRAM mỗi token thấp. Tuy nhiên, việc route expert giữa các GPU gây **all‑to‑all communication** → ảnh hưởng đến latency khi interconnect không đủ nhanh.  

#### 3.2.2. Quantization  
- **FP8 (E4M3/E5M2)** giảm bộ nhớ 2× so với BF16,Cho phép đặt model trên ít GPU hơn hoặc tăng batch size. Trên H100/H200/B300/MI300X, FP8 cũng tăng decode throughput khoảng 2× với mất độ chính xác nhỏ.  
- **INT4/GPTQ/AWQ** nén 4× nhưng suy giảm độ chính xác trên tác dụng reasoning multi‑step. Các định dạng block‑scaled như MXFP4/NVFP4 còn thiếu hỗ trợ rộng rãi (cần Blackwell hoặc MI350X).  

#### 3.2.3. Chiến lược Parallelism  
| Kiểu | Nguyên lý | Ưu điểm | Nhược điểm |
|------|-----------|----------|------------|
| **Tensor Parallelism (TP)** | Chia ma trận trọng số trong mỗi layer trên các GPU trong cùng một node NVLink. | Giảm latency per‑token (mỗi GPU xử lý toàn bộ token). | Cần AllReduce cao bandwidth; mở rộng kém trên >8 GPU. |
| **Expert Parallelism (EP)** | Đặt từng expert MoE trên GPU khác nhau. | Tiết kiệm bandwidth vì chỉ expert được kích hoạt truyền dữ liệu. | Tải không均衡 (hot experts). |
| **Data Parallelism (DP)** | Chạy nhiều replica độc lập, mỗi replica xử lý một subset request. | Tăng throughput tuyến tính; không có communication между GPU. | Tăng VRAM dùng (mỗi replica giữ một bản mô hình). |

Chọn TP khi latency ưu tiên (ví dụ: chat), chọn EP+DP khi throughput ưu tiên (ví dụ: batch synthesis) và kết hợp chúng sao cho phù hợp với kiến trúc mô hình.

#### 3.2.4. Batching và Scheduling  
- **Batch size (B)** là điểm giao叠 giữa throughput và latency.  
- Trong giai đoạn **decode** (memory‑bound), tải weight từ HBM là coût cố định → tăng B cho tới **B_sat** (batch size tại điểm knees) daje almost‑linear throughput gain mà latency quase không đổi.  
- Sau B_sat, hệ thống trở thành **compute‑bound** → latency tăng parecchio (hockey‑stick).  
- Kỹ thuật như **continuous batching**, **chunked prefill** (ở vLLM) dịch chuyển điểm knees sang phải, mở rộng vùng hoạt động hiệu quả.  

### 3.3. Khi nào ưu tiên throughput vs. latency  

#### 3.3.1. Latency‑Sensitive Workloads  
- Interactive chat, code completion, real‑time agents, search augmentation.  
- Chỉ số chính: **TTFT (Time‑To‑First‑Token)** và **ITL (Inter‑Token‑Latency)** (thường nhìn P99).  
- Các biện pháp tối ưu:  
  - Giữ batch size **dưới B_sat** để tránh queuing làm tăng TTFT.  
  - Dùng **TP** trên một node NVLink để giảm ITL.  
  - Áp dụng **chunked prefill** để ngăn chặn một prompt lớn “hijack” GPU.  
  - Xem xét **speculative drafting** (draft model) để giảm ITL với chi phí compute tăng.  
  - Cấp slightly **over‑provision** (thêm GPU head‑room) để chịu bursts mà không tạo queue.  

#### 3.3.2. Throughput‑Sensitive Workloads  
- Batch summarization, offline data extraction, synthetic data generation, evaluation pipelines.  
- Chỉ số chính: **tokens/s** (hoặc tokens/$) ; latency của từng request là thứ hai miễn là tổng thời gian hoàn thành jobs chấp nhận được.  
- Các biện pháp tối ưu:  
  - Đẩy batch size **vào vùng compute‑bound** (bá B_sat) để tối ưu FLOPS mỗi byte weight.  
  - Mở rộng bằng **DP** (thêm replica) để tăng throughput tuyến tính.  
  - Tăng limit **concurrent token processing** trong prefill để giữ Tensor Core bận.  
  - Sử dụng **quantization mạnh** (INT4/GPTQ) nếu chất lượng cho phép – mô hình nhỏ hơn cho phép batch size lớn hơn → lợi nhuận tokens/dollar lớn.  
  - Chấp nhận **queuing** như một tài sản: giữ GPU luôn bận, mục tiêu là thời gian hoàn thành toàn bộ job ngắn nhất.  

#### 3.3.3. The Hybrid Reality  
Hầu hệ thống production kết hợp cả hai: traffic tương tác trong ngày (latency‑sensitive) và jobs batch đêm (throughput‑sensitive). Chiến lược tối ưu:  

- **Dynamic autoscaling** phản ứng theo queue depth (reactive) và dự báo trafic (predictive).  
- **Priority queuing** – phục vụ request interactive trước, chạy batch trong nền khi có sức dư.  
- **Cấu hình workload‑specific** – chạy nhiều instance vLLM, mỗi instance có bộ tuning riêng (latency‑optimized vs throughput‑optimized).  

### 3.4. Quyết định Framework  

1. **Characterize your workload**  
   - Phân phối độ dài input (ISL) và output (OSL).  
   - Yêu cầu QPS (trung bình và cao điểm).  
   - SLO latency: TTFT, ITL tại p50, p95, p99.  

2. **Select model & quantization**  
   - Chọn mô hình nhỏ nhất đáp ứng yêu cầu chất lượng.  
   - Thử **FP8** đầu tiên (loss ≈0); nếu chất lượng giảm đáng chỉ, chuyển sang BF16.  

3. **Benchmark on candidate hardware**  
   - Chạy sweep ISL/OSL ở nhiều mức QPS trên ít nhất hai loại phần cứng (ví dụ: H100 vs MI300X).  
   - Lưu throughput thực δυợng dưới tải pracy.  

4. **Find the knee (B_sat)**  
   - Với mỗi phần cứng, xác định QPS tối đa mà latency vẫn trong SLO → đây là **sustainable capacity per instance**.  

5. **Size your deployment**  
   - Sử dụng **Little’s Law**: `Concurrency = QPS × AvgLatency`.  
   - Nếu mỗi instance hỗ trợ tối đa batch size = 32 và latency target = 2 s → QPS max per instance = 32 / 2 = 16.  
   - Để đòi hỏi peak QPS = 100 → cần `ceil(100 / 16) ≈ 7` instances, cộng thêm 20‑30% head‑room cho burst.  

6. **Calculate total cost**  

   ```
   TCO_per_token = (Capital + Operational + Engineering Cost) / Total Lifetime Throughput
   ```

   - So sánh TCO giữa các lựa chọn phần cứng; GPU rẻ nhất không phải luôn là triển khai rẻ nhất do chi phí OpEx, Opportunity và Engineering.  

7. **Plan for autoscaling**  
   - Thiết kế chính sách scale‑up/scale‑down dựa trên lưu lượng thực tế;  
   - Trong thời gian low‑traffic,เติม capacity trống bằng các workload batch để giảm opportunity cost.  

### 3.5. Build for Your Workload, Not the Benchmark  

- Các con số trên tạp chí (benchmark) thường đo trong điều kiện ideal (batching lớn, không có spike).  
- Thực tế, bạn phải **benchmark trên chính xác prompt, traffic pattern và phần cứng** bạn sẽ dùng.  
- Khi các công cụ như vLLM, TensorRT‑LLMcontinues to mature, cơ bản vật lý của LLM inference (memory‑bound decode, compute‑bound prefill) không thay đổi.  
- Do đó, **stop guessing, start benchmarking, tune to the metrics that matter to your business**.  

## 4. Ví dụ minh họa  

### 4.1. Lựa chọn kiến mô hình và VRAM  

- **Mô hình dense**: Llama 3 70B (BF16) → cần ~140 GB VRAM. Trên một node 2×H100 (160 GB HBM) có thể chạy; trên 1×MI300X (192 GB) cũng đủ.  
- **Mô hình MoE**: DeepSeek‑V3 (671B tổng, ~37B active mỗi token) trong FP8 → ~74 GB VRAM cho active weights, nhưng tổng weight file ~800 GB cần 8×H100 node để lưu trữ toàn bộ model. Tuy nhiên mỗi token chỉ cần tải ~37B → tính toán thấp, nhưng truyền expert giữa GPU đòi hỏi NVLink/InfiniBand cao.  

### 4.2. Hiệu ứng quantization  

- Chuyển Llama 3 70B từ BF16 sang FP8 → dung lượng VRAM giảm từ 140 GB xuống ~70 GB → cùng một node 2×H100 có thể tăng batch size từ 16 lên 32 trong cùng mức latency (do bộ nhớ không còn là bottleneck).  
- Trên H100, FP8 cũng nâng decode throughput khoảng 2× (ví dụ: từ 800 token/s lên 1600 token/s) với độ chính xác giảm <0.5% trên benchmark MMLU.  

### 4.3. Cấu hình parallelism cho hai loại workload  

| Workload | Mục tiêu | Kiến trúc gợi ý |
|----------|----------|----------------|
| Interactive chat (latency‑sensitive) | Giảm TTFT & ITL | **TP = 8** trên một node 8‑GPU H100 (một replica). Batch size giữ ở 4‑8 (dưới B_sat). Bật chunked prefill (512‑token chunks). |
| Offline batch summarization (throughput‑sensitive) | Tăng tokens/s | **DP = 4** (4 replicas) trên 2 node 4‑GPU mỗi node (mỗi node dùng TP=4 để vừa vừa). Batch size mỗi replica đẩy tới 64‑128 (vào vùng compute‑bound). Sử dụng quantization INT4 nếu chất lượng cho phép. |

### 4.4. Tính toán số instance với Little’s Law  

Giả sử:  

- Target средня latency = 2 s (TTFT + ITL).  
- Mỗi GPU có thể xử lý tối đa batch size = 32 mà không vượt qua B_sat.  

QPS tối đa mỗi instance = batch size / latency = 32 / 2 = 16 req/s.  

Nếu peak QPS dự kiến = 50 → số instances cần = ceil(50 / 16) = 4.  
Thêm 25% head‑room → 5 instances.  

### 4.5. Biểu đồ batch‑size vs latency / throughput (mô tả)  

- **Trục X**: batch size (B).  
- **Trục Y bên trái**: latency (ms).  
- **Trục Y bên phải**: throughput (token/s).  
- Đường 증가 latency почти flat tới B_sat (ví dụ: B_sat ≈ 32) sau đó tăng sharply (hockey‑stick).  
- Đường throughput tăng tuyến tính tới B_sat, sau đó tăng chậm hơn vì compute‑bound.  
- Các kỹ attribué như continuous batching shifts B_sat sang phải, mở rộng khu vực “near‑free throughput”.  

## 5. Tổng kết  

- Trilemma **throughput‑latency‑cost** là thách thức không thể lược bỏ khi triển khai LLM inference; mỗi quyết策 kiến trúc, quantization, parallelism, batching đều di chuyển trọng lực giữa ba chiều này.  
- Chi phí thực tế bao gồm **CapEx, OpEx, Opportunity Cost và Engineering Cost**; hiểu từng thành phần giúp đưa ra quyết định tài chính chính xác.  
- Các **lever** chính (kiến trúc mô hình, quantization, chiến lược parallelism, batching & scheduling) có thể được điều chỉnh để tối ưu cho một mục tiêu cụ thể – latency hoặc throughput – phụ thuộc vào workload.  
- Quyết định hệ thống dựa trên **workload characterization → model & quantization selection → hardware benchmarking → tìm điểm knees → tính nhu cầu instance qua Little’s Law → tính tổng TCO → lên kế hoạch autoscaling** cho phép xây dựng triển khai dựa trên thực nghiệm, không chỉ dựa vào con số trên tạp chí.  
- Cuối cùng, **build for your workload, not the benchmark**: chỉ bằng việc đo lường thực tế trên prompt, traffic pattern và phần cứng bạn sẽ sử dụng mới đạt được cân bằng tối ưu giữa throughput, latency và chi phí.