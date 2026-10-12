# Kỹ thuật Context trong các hệ thống AI Agent  

## 1. Mục tiêu học tập  

Sau khi đọc bài học này, bạn sẽ có thể:  

- Giải thích khái niệm **context engineering** và vai trò của nó đối với các LLM agent.  
- Phân biệt các loại context thường gặp (instructions, knowledge, tools) và cách chúng ảnh hưởng đến hiệu suất agent.  
- Mô tả bốn chiến lược chính của context engineering – **write, select, compress, isolate** – cùng các kỹ thuật đi kèm (scratchpad, memory, RAG, summarization, trimming, multi‑agent, sandbox, state).  
- Minh hoạ cách LangGraph và LangSmith hỗ trợ triển khai từng chiến lược trên.  
- Áp dụng ít nhất một phương pháp để giảm thiểu vấn đề tràn context window trong một agent đơn giản.  

## 2. Tổng quan  

LLM hoạt động như một “CPU” và context window của nó tương đương với RAM – là bộ nhớ làm việc có dung lượng hữu hạn. Khi agent thực hiện các nhiệm vụ dài, chúng phải gọi LLM lẫn lẫn với các tool calls,从而 tích lũy rất nhiều token. Nếu không quản lý tốt, context window có thể bị tràn, gây ra hiện tượng **context poisoning, distraction, confusion hoặc clash**, đồng thời làm tăng chi phí và latency.  

**Context engineering** là nghệ thuật và khoa học điền vào context window *đúng* lượng thông tin *đúng* thời điểm để agent luôn có đủ bối cảnh cần thiết mà không bị quá tải.  

Bài học này tóm tắt các loại context thường gặp, phân loại bốn chiến lược chính (write, select, compress, isolate) và示范 cách LangGraph/LangSmith giúp thực hiện chúng trong thực tiễn.  

## 3. Kiến thức cốt lõi  

### 3.1. Các loại context trong LLM application  

| Loại | Mô tả | Ví dụ |
|------|-------|-------|
| **Instructions** | Prompt, few‑shot examples, mô tả tool, 기억| System prompt, ví dụ poucos-shot, mô tả công cụ |
| **Knowledge** | Fact, conhecimento được lưu trữ dài hạn | Cơ sở tri thức, vector DB, knowledge graph |
| **Tools** | Phản hồi từ tool calls (JSON, kết quả tìm kiếm…) | Kết quả API search, output của công cụ mã |

### 3.2. Ba vấn đề phổ biến khi context quá lớn  

1. **Context Poisoning** – thông tin sai (hallucination) lọt vào context và làm sai hướng suy luận.  
2. **Context Distraction** – quá nhiều dư thông tin làm model mất trọng điểm.  
3. **Context Confusion / Clash** – thông tin mâu thuẫn hoặc không liên quan gây nhầm lẫn.  

### 3.3. Ba nguyên tắc quản lý context  

- **Write**: lưu thông tin *ngoài* context window để tái sử dụng sau.  
- **Select**: đưa vào context chỉ những phần cần thiết cho bước tiếp theo.  
- **Compress**: giảm bớt token trong context mà vẫn giữ lại thông tin則 cần.  
- **Isolate**: tách context ra thành các phần độc lập (ví dụ qua multi‑agent, sandbox, state object).  

## 4. Ví dụ minh họa  

### 4.1. Write Context – Scratchpad & Memory  

**Scratchpad (short‑term)**  
- Triển khai như một tool gọi để ghi vào file hoặc như một trường trong runtime state object của LangGraph.  
- Khi agent thực hiện một bước, nó có thể ghi tóm tắt suy nghĩ vào scratchpad; bước kế tục đọc lại mà không phải trả lại toàn bộ lịch sử.  

**Memory (long‑term)**  
- Sử dụng LangGraph long‑term memory hoặc LangMem để lưu trữ những “memory” được tạo tự động (ví dụ: phản hồi từ người dùng, kết quả trung gian).  
- Các memory có thể được chia thành *episodic* (few‑shot), *procedural* (hướng dẫn) và *semantic* (fact).  

> **Ví dụ code (LangGraph pseudo)**  

```python
from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    scratchpad: List[str]      # write‑once, read‑many
    memories: List[str]        # long‑term store
    messages: List[str]        # exposición ao LLM

def write_scratchpad(state: AgentState) -> AgentState:
    state["scratchpad"].append("Plan: search for latest papers")
    return state

def read_scratchpad(state: AgentState) -> AgentState:
    # select context from scratchpad before LLM call
    state["messages"].append(state["scratchpad"][-1])
    return state

graph = StateGraph(AgentState)
graph.add_node("write", write_scratchpad)
graph.add_node("select", read_scratchpad)
graph.add_edge("write", "select")
```

### 4.2. Select Context – RAG cho tool description  

Khi agent có danh sách tool lớn, chúng ta áp dụng **Retrieval‑Augmented Generation (RAG)** trên mô tả tool để chỉ lấy những tool phù hợp nhất với câu hỏi hiện tại.  

- Tạo vector embedding cho mỗi mô tả tool.  
- Khi agent cần chọn tool, truy vấn vector DB với embedding của prompt → trả về top‑k tool.  

> **Kết quả nghiên cứu:** một số bài báo gần đây cho thấy độ chính xác выбора tool tăng **3×** khi dùng RAG so với việc đưa toàn bộ danh sách vào prompt.  

### 4.3. Compress Context – Summarization & Trimming  

**Summarization**  
- Sau mỗi N turn, chạy một mô hình tóm tắt (recursive hoặc hierarchical) trên danh sách `messages` để tạo bản tóm tắt ngắn gọn, thay thế phần cũ trong state.  

**Trimming**  
- Loại bỏ các message cũ nhất (hard‑coded heuristic) hoặc sử dụng mô hình **context pruner** (ví dụ: Provence) để giữ lại chỉ những token có điểm relevance cao.  

> **Ví dụ LangGraph:** trong mỗi node, gọi utility `trim_messages(state["messages"], max_tokens=2048)` trước khi truyền vào LLM.  

### 4.4. Isolate Context – Multi‑agent & Sandbox  

**Multi‑agent**  
- Chia một task lớn thành các sub‑agent, mỗi agent có riêng instructions, tools và riêng context window.  
- LangGraph cung cấp thư viện `langgraph-supervisor-py` và `langgraph-swarm-py` để xây dựng mô hình supervisor‑worker hoặc swarm.  

**Sandbox (Environment isolation)**  
- Chạy tool calls bên trong môi trường bị cô lập (E2B, Pyodide). Kết quả (ví dụ: hình ảnh, audio) được lưu trong state object mà không gửi trực tiếp vào LLM, từ đó giảm bớt token lourd.  

> **Ví dụ:** Một HuggingFace `CodeAgent` sinh mã, gửi mã tới E2B sandbox để thực thi, sau đó chỉ trả về giá trị cần thiết (ví dụ: số liệu thống kê) vào state để LLM tiếp tục.  

### 4.5. Hỗ trợ từ LangSmith & LangGraph  

| Mục đích | Công cụ | Cách hoạt động |
|----------|---------|----------------|
| **Giám sát token usage** | LangSmith tracing | Ghi lại số token mỗi LLM call, giúp xác địnhจุด cần compress hoặc isolate. |
| **Đánh giá tác động của context engineering** | LangSmith agent evaluation | So sánhMetrics (accuracy, latency, cost) trước và sau khi áp dụng một chiến lược (ví dụ: thêm summarization). |
| **Quản lý scratchpad & memory** | LangGraph state + checkpoints | Lưu trạng thái ở mỗi node, cho phép read/write scratchpad ở bất kỳ bước nào. |
| **Tool selection bằng RAG** | LangGraph Bigtool | Thư viện cung cấp semantic search trên mô tả tool để fetch top‑k tool mỗi bước. |
| **Xây dựng multi‑agent** | langgraph‑supervisor / langgraph‑swarm | Định nghĩa supervisor node phân công công việc cho worker agents, mỗi worker có riêng state và context window. |

## 5. Tổng kết  

- **Context engineering** là việc quản lý thông tin đưa vào context window của LLM agent để tránh quá tải, улучшять chất lượng suy luận và giảm chi phí.  
- Ba loại context cơ bản: **instructions, knowledge, tools**; mỗi loại có thể được **write, select, compress, isolate**.  
- Các kỹ thuật phổ biến: scratchpad & memory (write/select), RAG cho tool/knowledge (select), summarization & trimming (compress), multi‑agent, sandbox, state object (isolate).  
- **LangGraph** cung cấp lớp trừu tượng thấp‑level (state object, checkpoints, long‑term memory) cùng các thư viện hỗ trợ (Bigtool, supervisor, swarm) để triển khai mọi chiến lược trên.  
- **LangGraph** + **LangSmith** tạo thành một vòng lặp phản hồi: đo lường token usage → xác định điểm bottlenecks → áp dụng phương pháp context engineering → đánh giá cải thiện → lặp lại.  

Với những nguyên tắc và công cụ trên, bạn có thể bắt đầu xây dựng các agent mạnh mẽ, capaces của xử lý nhiệm vụ dài hạn mà không gặp phải vấn đề tràn context window hoặc suy giảm hiệu suất do “context noise”.  

---  

*Bài học này được biên soạn dựa trên nội dung nguồn từ blog LangChain về “Context Engineering for Agents”. Các liên kết và hình ảnh trong nguồn đã được loại bỏ để tập trung vào kiến thức cốt lõi.*