# Fine‑tuning trong Machine Learning  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ能够:  

- Giải thích khái niệm **fine‑tuning** và cách nó liên quan đến **transfer learning**.  
- Phân biệt quá trình **pre‑training** (training ban đầu) và **fine‑tuning**.  
- Mô tả các bước làm việc của fine‑tuning: forward pass, loss function, backpropagation và gradient descent.  
- Nêu lợi thế của fine‑tuning so với việc huấn luyện mô hình từ đầu.  
- Giải thích các kỹ thuật **parameter‑efficient fine‑tuning (PEFT)** như partial fine‑tuning, additive fine‑tuning (prompt tuning, adapters, LoRA/QLoRA).  
- Nêu một số trường hợp áp dụng phổ biến của fine‑tuning trong LLM và visión máy tính.  

## 2. Tổng quan  

Fine‑tuning là quá trình **tiếp tục huấn luyện** một mô hình đã được **pre‑train** trên một tập dữ liệu lớn và đa dạng, nhằm điều chỉnh nó cho mộttask cụ thể hoặc một ngành nghề nhất định. Thay vì phải huấn luyện lại từ đầu một mô hình có hàng triệu,甚至 hàng tỷ tham số, chúng ta bắt đầu từ trọng số đã học được và chỉ cần cập nhật một phần (hoặc toàn bộ) chúng trên một tập dữ liệu nhỏ hơn, miền cụ thể.  

Kỹ thuật này cho phép chúng ta:

- Tận dụng kiến thức rộng lớn mà mô hình đã獲得 trong pre‑training.  
- Giảm lượng dữ liệu labeled và mức tài nguyên tính toán cần thiết.  
- Tránh hiện tượng **overfitting** khi huấn luyện trên dữ liệu quá nhỏ.  

## 3. Kiến thức cốt lõi  

### 3.1. Pre‑training vs. Fine‑tuning  

| Yếu tố | Pre‑training (Training ban đầu) | Fine‑tuning |
|--------|--------------------------------|------------|
| Trạng thái ban đầu của mô hình | Trọng số được khởi tạo ngẫu nhiên | Trọng số đã được cập nhật từ pre‑training |
| Tập dữ liệu | Tập dữ liệu **không có nhãn** (đối với LLM) hoặc **có nhãn** (đối với CV) thường rất lớn | Tập dữ liệu **nhỏ**, có nhãn, phản ánh task mục tiêu |
| Mục tiêu | Học được đặc trưng chung, ngôn ngữ, hoặc visão tổng quát | Điều chỉnh mô hình để phù hợp với style, kiến thức chuyên môn hoặc behavior cụ thể |
| Kỹ thuật học thường dùng | Self‑supervised learning (SSL) hoặc supervised learning | Supervised learning (SFT), reinforcement learning (RLHF), semi‑supervised learning, … |
| Chi phí | Tốn nhiều GPU‑hours, cần nhiều dữ liệu | Tốn ít hơn vì chỉ cập nhật phầnParameters và dữ liệu nhỏ |

### 3.2. Quy trình huấn luyện chung (forward‑pass → loss → backprop)  

1. **Forward pass** – Mô hình đưa ra dự đoán cho một batch mẫu.  
2. **Loss function** – Tính sai số giữa dự đoán và ground truth (label thật).  
3. **Backpropagation** – Tích gradient của loss относительно từng tham số bằng **gradient descent** ( hoặc các biến thể như Adam).  
4. **Cập nhật trọng số** – Tham số mới = tham số cũ – learning_rate × gradient.  
5. Lặp lại qua nhiều **epoch** cho tới khi loss ổn định.

### 3.3. Tại sao fine‑tuning giảm Overfitting?  

Huấn luyện một mô hình lớn từ đầu trên một tập dữ liệu nhỏ dễ dẫn tới **overfitting** – mô hình ghi nhớ noise thay vì học đặc trưng hữu ích. Với fine‑tuning, mô hình đã có kiến thức tổng quát từ pre‑training; chúng ta chỉ điều chỉnh nhẹ nhàng trọng số để thích hợp với task mới, do đó giữ lại khả năng generalize.

### 3.4. Parameter‑efficient fine‑tuning (PEFT)  

Khi mô hình có hàng tỷ tham số, fine‑tuning toàn bộ mạng có thể tốn kém. PEFT nhằm **chỉ cập nhật một bộ con nhỏ** của tham số mà vẫn đạt được hiệu suất tốt.

| Loại PEFT | Ý tưởng chính | Ưu điểm |
|-----------|--------------|---------|
| **Partial (Selective) fine‑tuning** | Cập nhật chỉ các lớp ngoài cùng (hoặc một số bias); các lớp sâu được “freeze”. | Giảm bộ nhớ và thời gian huấn luyện; giữ lại đặc trưng tổng quát từ pre‑training. |
| **Additive fine‑tuning** | Giữ nguyên trọng số pre‑train, thêm các module mới (prompt, adapters, LoRA). | Không thay đổi kiến thức gốc; dễ “plug‑and‑play” cho nhiều task. |
| **Prompt tuning** | Thêm **soft prompts** (vector có thể học) vào đầu input; freeze toàn bộ mô hình. | Extremely lightweight; cho phép chuyển đổi nhanh giữa các task. |
| **Adapters** | Chèn các lớp bottleneck nhỏ giữa các lớp transformer; chỉ train adapters. | Tham số train được giảm xuống ~3‑5% so với full fine‑tuning (ví dụ: 3.6% trên BERT). |
| **LoRA (Low‑Rank Adaptation)** | Phân tích ma trận trọng số thành hai ma trận低秩; chỉ train các ma trận này (delta weights). | Cắt giảm bộ nhớ GPU tới 1/10‑1/20; có thể “swap‑in” nhiều LoRA cho nhiều task mà không thay đổi trọng số gốc. |
| **QLoRA** | Kết hợp LoRA với **quantization** (giảm precision) trước khi áp dụng Low‑rank. | Tiết kiệm thêm bộ nhớ và thời gian tính toán. |

### 3.5. Các biến thể cụ thể trong LLM  

- **Instruction Tuning (SFT)** – Huấn luyện trên cặp *(prompt, response)* để mô hình học cách tuân thủ hướng dẫn (ví dụ: trả lời câu hỏi, tóm tắt, dịch).  
- **Reinforcement Learning from Human Feedback (RLHF)** – Sau SFT, thu thập xếp hạng của con người về output, huấn luyện một **reward model**, sau đó dùng RL để tối ưu reward. Giúp cải thiện tính-helpfulness, giảm hallucinations, cân đối bias.  

### 3.6. Các use case thường gặp  

| Mục tiêu | Ví dụ cụ thể |
|----------|--------------|
| **Tùy chỉnh style** | Đổi tone của chatbot thành trang trọng hoặc thân thiện. |
| **Chuyên môn hóa** | Fine‑tune LLM trên corpus pháp luật để tạo trợ lý pháp lý. |
| **Bổ sung kiến thức chuyên môn** | Thêm dữ liệu y tế, tài chính để mô hình hiểu thuật ngữ chuyên sâu. |
| **Few‑shot learning** | Cung cấp vài ví dụ-labeled để mô hình phân loại Main‑stream vs Spam. |
| **Xử lý edge cases** | Huấn luyện trên các câu dạng “lừa đảo” để mô hình nhận biết và từ chối. |
| **Integrate proprietary data** | Dùng dữ liệu nội bộ công ty để tinh chỉnh mô hình mà không phải xây dựng lại từ zero. |

## 4. Ví dụ minh họa  

### Tình huống  
Một công ty muốn tạo một chatbot hỗ trợ khách hàng trong ngành ngân hàng. Mô hình cơ sở là một LLM pre‑trained trên dữ liệu văn bản chung (tối đa 7B tham số).  

### Quy trình áp dụng  

1. **Thu thập dữ liệu** – 5.000 cặp *(prompt, response)* từ lịch sử chat thực tế, bao gồm các câu hỏi về số dư, chuyển khoản, lãi suất.  
2. **Instruction Tuning (SFT)** –  
   - Khởi tạo trainer với **learning_rate = 2e‑5**, **batch_size = 8**, **3 epochs**.  
   - Loss = cross‑entropy giữa output của mô hình và response thật.  
   - Thực hiện forward‑pass → loss → backprop → cập nhật trọng số toàn bộ (full fine‑tuning).  
3. **Kiểm tra catastrophic forgetting** – Đánh giá trên một tập benchmark chung (MMLU). Nếu điểm giảm >2%, giảm learning_rate hoặc chuyển sang PEFT.  
4. **Áp dụng LoRA (PEFT)** –  
   - Freeze toàn bộ trọng số LLM.  
   - Thêm hai ma trận **A (r×d)** và **B (d×r)** với rank r = 8 vào mỗi ma trận trọng số trong các lớp attention.  
   - Chỉ train A và B (khoảng 0,5% tổng parameters).  
   - Huấn luyện cùng dataset SFT với learning_rate = 1e‑4.  
5. **Kết hợp RLHF (tùy chọn)** – Thu thập xếp hạng human trên 1.000 output từ mô hình đã LoRA‑fine‑tuned, huấn luyện reward model, sau đó dùng PPO để tối ưu policy.  

### Kết quả mong đợi  
- Độ chính xác trên tập test ngân hàng ↑ 12% so với mô hình chỉ pre‑trained.  
- Điểm MMLU giảm <0,5% → ít forgetting.  
- Bộ nhớ GPU cần thiết giảm từ ~24GB (full fine‑tuning) xuống ~6GB khi dùng LoRA rank 8.  

## 5. Tổng kết  

- Fine‑tuning là kỹ thuật **tiếp tục huấn luyện** mô hình đã được pre‑train, cho phép chúng ta **tận dụng kiến thức tổng quát** và **tập trung vào task cụ thể** mà không cần chi phí lớn của việc train từ đầu.  
- Nó là một **phiên bản cụ thể** của transfer learning, với sự khác biệt chính nằm ở điểm bắt đầu (trọng số đã học) và dữ liệu huấn luyện (nhỏ, có nhãn).  
- Quá trình học vẫn включает forward‑pass, loss, backpropagation và gradient descent; tuy nhiên, vì bắt đầu từ một điểm đã tốt, việc hội tụ thường nhanh hơn và ít nguy cơ overfitting.  
- Khi mô hình rất lớn, **parameter‑efficient fine‑tuning** (PEFT) như partial fine‑tuning, additive methods (prompt tuning, adapters, LoRA/QLoRA) giúp giảm đáng kể tài nguyên tính toán và bộ nhớ mà vẫn giữ hoặc thậm chí nâng cao hiệu suất.  
- Trong ngữ cảnh LLM, **instruction tuning** và **RLHF** là hai bước quan trọng để mô hình trở thành trợ lý hữu ích, chính xác và an toàn cho các ứng dụng trò chuyện.  
- Các use case thực tế bao gồm tùy chỉnh style, chuyên môn hóa, bổ sung kiến thức chuyên môn, few‑shot learning, xử lý edge cases và tích hợp dữ liệu proprietary.  

Việc nắm vững khái niệm và các kỹ thuật fine‑tuning sẽ giúp các nhà phát triển AI **tối ưu hoá** mô hình cho nhu cầu kinh doanh cụ thể, tiết kiệm chi phí và thời gian, đồng thời duy trì hiệu suất cao trên nhiềudomain.