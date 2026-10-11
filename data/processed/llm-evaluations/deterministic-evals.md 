# DeepEval DAG Metric – Đánh giá LLM có cấu trúc và xác định

## 1. Mục tiêu học tập
Sau bài học này, người học sẽ:
- Hiểu tại sao các chỉ số mặc định của DeepEval (LLM‑as‑a‑judge) có thể không đủ cho việc đánh giá cần tiêu chí cụ thể.
- Nắm rõ vấn đề khi người dùng tự xây dựng chỉ số tùy chỉnh (custom metrics) và tại sao điều đó dẫn đến mã nguồn phức tạp, không ổn định.
- Giải thích cách hoạt động của **DAG (Deep Acyclic Graph) metric**, bao gồm bốn loại node và cách chúng kết hợp thành một cây quyết định LLM‑powered.
- Viết một ví dụ đơn giản sử dụng DAGMetric để đánh giá một bản tóm tắt meeting transcript (kiểm tra наличие và thứ tự các phần intro‑body‑conclusion).
- Liệt kê những lợi ích bổ sung của DAGMetric (hoạt động tốt với LLM yếu, tận dụng hệ sinh thái DeepEval, debug dễ dàng).

## 2. Tổng quan
DeepEval là framework mã nguồn mở để đánh giá ứng dụng LLM (RAG, agents, chatbots…). Các chỉ số built‑in của nó (contextual recall, answer relevancy, answer correctness…) dựa trên kỹ thuật **Question‑Answer Generation (QAG)** – LLM-as‑a‑judge trả về phản hồi nhị phân “yes”/“no”, do đó kết quả khá ổn định và dễ hiểu.

Tuy nhiên, nhiều trường hợp sử dụng thực tế cần **tiêu chí phức tạp, có thứ tự và có điều kiện** (ví dụ: kiểm tra định dạng markdown, sự có mặt và thứ tự của các phần tiêu đề trong một bản tóm tắt). Khi chỉ depend vào LLM‑as‑a‑judge, kết quả có thể biến động và không đáp ứng yêu cầu determinism (kết quả nhất quán). Người dùng thường phải viết hàng trăm dòng prompt và logic điều kiện để “bù” cho sự thiếu sót của chỉ số built‑in, dẫn đến mã nguồn khó duy trì.

Để giải quyết vấn đề này, tác giả của DeepEval đã thiết kế **DAG metric** – một chỉ số có cấu trúc dạng **Decision Tree** được駕驭 bởi LLM, trong đó mỗi bước評価 được biểu diễn bằng một node. Node có thể:
- tách dữ liệu test case thành các đơn vị nguyên子 (Task node),
- đưa ra phán đoán nhị phân (Binary Judgment node),
- đưa ra phán đoán đa giá trị (Non‑Binary Judgment node),
- trả về điểm số cuối cùng (Verdict node).

Mọi node được kết nối thành một **Directed Acyclic Graph (DAG)**, đảm bảo không có vòng lặp và cho phép thực hiện song song, cache, và tracing dễ dàng.

## 3. Kiến thức cốt lõi

### 3.1 Vấn đề với chỉ số tùy chỉnh (custom metrics)
- **Yêu cầu déterminisme**: Khi đánh giá cần tuân thủ một quy trình cụ thể (ví dụ: kiểm tra có tất cả các phần headings → kiểm tra thứ tự → đánh giá chất lượng), chỉ số dựa trên LLM‑as‑a‑judge đơn không thể bảo证 mỗi bước sẽ cho kết quả nhất quán.
- **Công đoạn mã dài**: Người dùng thường viết hàng trăm dòng prompt và logic if‑else để mô phỏng quy trình trên, dẫn đến mã nguồn khó đọc, bảo trì và dễ lỗi.
- **Thiếu tận dụng hệ sinh thái**: Các giải pháp tự construits không hưởng dụng từ tính năng song song, cache, hoặc xử lý lỗi của DeepEval.

### 3.2 Giải pháp: DAG metric (Deep Acyclic Graph)
DAG metric được xây dựng trên bốn loại node cơ bản:

| Loại node | Mô tả | Vai trò trong cây quyết định |
|-----------|-------|------------------------------|
| **TaskNode** | Tách test case (input, actual_output, expected_output…) thành các atomic unit, ví dụ: trích xuất tất cả headings từ actual_output. | Cung cấp dữ liệu cho các node其後. |
| **BinaryJudgementNode** | Đặt câu hỏi có trả về **yes/no** (true/false). Kết quả quyết định哪個 child node sẽ được thực hiện tiếp theo. | Kiểm tra điều kiện sì/k não (ví dụ: “headings có đủ ba phần không?”). |
| **NonBinaryJudgementNode** | Đặt câu hỏi có trả về một chuỗi từ một danh sách có thể (ví dụ: “All correct”, “Two out of order”, “All out of order”). Mỗi kết quả trỏ tới một child node khác. | Phân loại mức độ đúng/sai trong trường hợp có nhiều mức độ. |
| **VerdictNode** | Node lá (leaf) trả về **điểm số cố định** hoặc điểm số được tính bởi G‑Eval dựa trên verdict của node cha. | Kết thúc một đường đi eval và cung cấp điểm số cuối cùng. |

- **Root node**: luôn là một TaskNode (không thể là VerdictNode).
- **Leaf nodes**: đều là VerdictNode.
- Đồ thị phải là **acyclic** (không có chu trình) để đảm bảo quá trình 평가 kết thúc.

### 3.3 Luật hoạt động
1. Test case được đưa vào root TaskNode → node sinh ra một label (ví dụ: “summary headings”).
2. Label này được przekaz vào các node con (Binary/NonBinary Judgement) dựa trên tiêu chí đã định.
3. Tùy thuộc vào kết quả yes/no hoặc một trong các chuỗi có thể, đồ thị nhảy tới node con tương ứng.
4. Cuối cùng tới một VerdictNode → trả về điểm số và lý do (reason).

### 3.4 Ưu điểm bổ sung
- **Tương thích với LLM yếu**: Vì việc đánh giá được chia thành nhiều bước nhỏ, mỗi bước chỉ cần LLM thực hiện một tác vụ đơn giản (trích xuất, yes/no, lựa chọn từ danh sách), do đó không cần mô hình mạnh mẽ.
- **Tích hợp hệ sinhatai DeepEval**: 
  - Các TaskNode cùng level chạy **song song** (parallel execution).  
  - **Quản lý chi phí** tự động (DeepEval theo dõi và tối ưu hoá lời gọi LLM).  
  - **Cache**: kết quả của một node được lưu và tái sử dụng nếu có trường hợp test case trùng lặp.  
  - **Xử lý lỗi**: lỗi trong bất kỳ node nào sẽ bị bubble up; có thể chọn bỏ qua để không ngừng toàn bộ quá trình eval.
- **Debug dễ dàng** (`verbose_mode`): 
  - Ghi lại toàn bộ đường đi evaluation (which nodes were visited).  
  - Hiển thị intermediate judgments để biết tại sao một test case thất bại.  
  - Cho thấy điểm cần chỉnh sửa ở mỗi bước.

## 4. Ví dụ minh họa

### Tình huống
Đánh giá một bản tóm tắt meeting transcript. Yêu cầu:
1. Tóm tắt **phải chứa** ba phần heading: `"intro"`, `"body"`, `"conclusion"`.
2. Những heading này **phải xuất hiện** theo thứ tự exact: `intro → body → conclusion`.
3. Nếuthiếu heading → điểm 0.  
   Nếu có đủ heading nhưng sai thứ tự → điểm 2 (hai項 fuori) hoặc 4 (một项 fuera).  
   Nếu đúng heading và thứ tự → điểm 10.

### Mã nguồn (Python)
```python
from deepeval.metrics.dag import (
    DeepAcyclicGraph,
    TaskNode,
    BinaryJudgementNode,
    NonBinaryJudgementNode,
    VerdictNode,
    DAGMetric,
)
from deepeval.test_case import LLMTestCaseParams   #假设已导入

# 1️⃣ Trích xuất tất cả heading từ actual_output
extract_headings_node = TaskNode(
    instructions="Extract all headings in `actual_output`",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    output_label="Summary headings",
    children=[],          # sẽ gán sau
)

# 2️⃣ Kiểm tra có đủ ba heading không (yes/no)
correct_headings_node = BinaryJudgementNode(
    criteria="Does the summary headings contain all three: 'intro', 'body', and 'conclusion'?",
    children=[
        # Nếu không đủ → điểm 0
        VerdictNode(verdict=False, score=0),
        # Nếu đủ →继续检查顺序
        VerdictNode(verdict=False, child=None),  # placeholder sẽ được thay bằng non‑binary node
    ],
)

# 3️⃣ Kiểm tra thứ tự heading (có 4 khả năng)
correct_order_node = NonBinaryJudgementNode(
    criteria=(
        "Are the summary headings in the correct order: "
        "'intro' => 'body' => 'conclusion'?"
    ),
    children=[
        VerdictNode(verdict="Yes", score=10),                         #全對
        VerdictNode(verdict="Two are out of order", score=4),         #兩項錯位
        VerdictNode(verdict="All out of order", score=2),             #全錯
    ],
)

# Gắn子节点
correct_headings_node.children[1].child = correct_order_node   #十分句的“yes”分支
extract_headings_node.children = [correct_headings_node, correct_order_node]

# 4️⃣ Xây dựng DAG và metric
dag = DeepAcyclicGraph(root_nodes=[extract_headings_node])
metric = DAGMetric(name="Summarization Headings Check", dag=dag)

# 5️⃣ Chạy đánh giá trên một test case (giả sử test_case đã được tạo)
metric.measure(test_case)
print(f"Score: {metric.score}")
print(f"Reason: {metric.reason}")
```

#### Giải thích luồng thực thi
1. **TaskNode** trích xuất headings → lưu trong label `Summary headings`.
2. BinaryJudgementNode kiểm tra xem label có đủ ba heading không.
   - Nếu **false** → langsung tới VerdictNode (điểm 0).
   - Nếu **true** → chuyển sang NonBinaryJudgementNode.
3. NonBinaryJudgementNode đánh giá thứ tự:
   - `"Yes"` → điểm 10  
   - `"Two are out of order"` → điểm 4  
   - `"All out of order"` → điểm 2  
4. Điểm số và lý do (reason) được trả về từ VerdictNode cuối cùng.

> Khi bật `verbose_mode=True` trên `DAGMetric`, người dùng sẽ thấy log giống:  
> ```
> [TaskNode] Extracted headings: ['intro', 'body', 'conclusion']  
> [BinaryJudgementNode] All three headings present? → Yes  
> [NonBinaryJudgementNode] Order correct? → Yes  
> [VerdictNode] Final score = 10
> ```

## 5. Tổng kết
- Các chỉ số built‑in của DeepEval dựa trên LLM‑as‑a‑judge hoạt động tốt với tiêu chí rộng và ổn định, nhưng **không đủ** cho những trường hợp cần quy trình đánh giá có cấu trúc, có điều kiện và **deterministic**.
- Việc tự xây dựng chỉ số tùy chỉnh thường dẫn đến mã nguồn dài, khó bảo trì và kết quả không ổn định.
- **DAG metric** giải quyết vấn đề này bằng cách mô hình hoá quá trình đánh giá như một **Decision Tree** có bốn loại node (Task, Binary Judgement, Non‑Binary Judgement, Verdict). Mỗi node là một bước đơn giản mà LLM có thể thực hiện, nên даже các LLM yếu cũng có thể đạt được kết quả ổn định.
- DAG được tích hợp sâu trong hệ sinhatai DeepEval → thực hiện song song tự động, quản lý chi phí, cache, và tracing lỗi, đồng thời cung cấp chế độ `verbose_mode` để debug dễ dàng.
- Ví dụ minh họa về kiểm tra heading của bản tóm tắt cho thấy chỉ với vài dòng code chúng ta có thể tạo ra một chỉ số đồng thời **để определить sự đủ và đúng thứ tự** và trả về điểm số spieg‑trong, reproducible.

> **Điểm cần nhớ**: DAG metric không thay thế LLM‑as‑a‑judge; nó chỉ **chia nhỏ** quá trình đánh giá thành các bước mà LSTM có thể làm một cách xác định, từ đó mang lại sự linh hoạt mà không 희생 tính ổn định và hiệu quả của DeepEval.