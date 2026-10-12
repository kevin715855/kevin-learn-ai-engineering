# Context Engineering – Thiết kế và tối ưu ngữ cảnh cho mô hình LLM

## 1. Mục tiêu học tập

- Hiểu khái niệm **Context Engineering** và tại sao nó thay thế ý tưởng truyền thống về Prompt Engineering.  
- Nhận ra các thành phần chính của một prompt well‑engineered: **System Prompt**, **Instructions**, **User Input**, **Structured Inputs & Outputs**, **Tools**, **RAG & Memory**, **States & Historical Context**.  
- Có thể áp dụng các kỹ thuật này vào một workflow agent thực tế (ví dụ: tạo kế hoạch tìm kiếm cho một deep‑research agent).  
- Đánh giá hiệu quả của ngữ cảnh thông qua các quy trình đánh giá (eval pipelines) và đo lường hiệu suất.

## 2. Tổng quan

Trong những năm qua, nhiều người bao gồm các nhà nghiên cứu AI hàng đầu đã dự đoánPrompt Engineering sẽ “chết”. Tuy nhiên, thực tế cho thấy nhu cầu tối ưu hóa cách chúng ta cung cấp thông tin cho LLM ngày càng tăng. Do đó, cộng đồng đã đổi tên quy trình này thành **Context Engineering** – một khái niệm rộng hơn bao gồm không chỉ việc thiết kế prompt mà còn quản lý toàn bộ **ngữ cảnh** (instructions, user data, tools, memory, structured I/O, …) để mô hình thực hiện tác vụ một cách hiệu quả.

Bài học này sẽ dẫn bạn qua ví dụ cụ thể từ một **multi‑agent deep research application** được xây dựng trong n8n. Các phần sau sẽ giải thích từng thành phần của prompt, minh họa bằng code và giải thích tại sao mỗi phần đều quan trọng trong quá trình Context Engineering.

---

## 3. Kiến thức cốt lõi

### 3.1 Định nghĩa Context Engineering  
> *Context Engineering* là quá trình **thiết kế và tối ưu hóa instructions và relevant context** cung給 LLMs và các mô hình AI nâng cao để chúng thực hiện任务 một cách hiệu quả. Định nghĩa này bao gồm cảLLM dựa trên văn bản và các mô hình đa phương tiện, đồng thời tä̈ng tới các quy trình liên quan như:
- Thiết kế và quản lý **prompt chains** (khi適用).  
- Tuning **instructions / system prompts**.  
- Quản lý các **dynamic elements** của prompt (ví dụ: user input, date/time).  
- Tìm kiếm và chuẩn bị **knowledge** (RAG).  
- **Query augmentation**.  
- Định nghĩa **tools** và hướng dẫn (trong hệ thống agentic).  
- Chuẩn bị và tối ưu **few‑shot demonstrations**.  
- **Structuring inputs and outputs** (delimiters, JSON schema).  
- Quản lý **short‑term memory** (state/historical context) và **long‑term memory** (vector store).  

Mục tiêu cuối cùng là tối ưu thông tin nằm trong **context window** của LLM, đồng thời lọc bỏ thông tin nhiễu (noise) thông qua đo lường hệ thống.

### 3.2 Các thành phần trong một prompt well‑engineered

| Thành phần | Vai trò | Ví dụ (trích từ deep‑research agent) |
|-----------|--------|--------------------------------------|
| **System Prompt** | Xác định vai trò, mục tiêu và các ràng buộc chung cho mô hình. | `You are an expert research planner...` |
| **Instructions** | Các yêu cầu cụ thể mà mô hình phải thực hiện. | `For each subtask, provide: 1. A unique string ID …` |
| **User Input** | Dữ liệu đầu vào từ người dùng, thường được delimit để tránh nhầm lẫn. | `<user_query> What's the latest dev news from OpenAI? </user_query>` |
| **Structured Inputs & Outputs** | Định dạng mong đợi (ID, tipo, priority, …) để đầu ra có thể parse dễ dàng. | `id: str`, `query: str`, `source_type: str …` + ví dụ JSON. |
| **Tools** | Các hàm hoặc dịch vụ cung cấp context động (date/time, truy cập vector store, …). | `{{ $now.toISO() }}` trong n8n để chèn thời gian hiện tại. |
| **RAG & Memory** | Truy xuất kiến thức liên quan hoặc lưu trữ kết quả trước để tái sử dụng, giảm latency & chi phí. | Vector store cache các sub‑queries đã được sinh ra. |
| **States & Historical Context** | Lưu trữ trạng thái trung gian (ví dụ: phiên bản sửa đổi của subtask) để cho agent có thể “hồi suy” và cải thiện kết quả. | Truy cập lại các subtask cũ, kết quả tìm kiếm trước khi tạo báo cáo cuối. |

### 3.3 Quy trình lặp đi lặp lại (iterative)  
1. **Thiết kế prompt ban đầu** (system prompt + instructions).  
2. **Chạy thử** và thu thập output.  
3. **Đánh giá** (eval pipeline): độ chính xác, độ đầy đủ, thời gian trả về, chi phí.  
4. **Cải thiện** bằng cách thêm/bớt context (ví dụ: khai báo priority scale, cung cấp ví dụ few‑shot).  
5. Lặp lại cho tới khi đạt tiêu chuẩn mong muốn.

---

## 4. Ví dụ minh họa – Xây dựng Search Planner Agent

### 4.1 System Prompt (trích nguyên bản)

```text
You are an expert research planner. Your task is to break down a complex research query (delimited by <user_query></user_query>) into specific search subtasks, each focusing on a different aspect or source type.

The current date and time is: {{ $now.toISO() }}

For each subtask, provide:
1. A unique string ID for the subtask (e.g., 'subtask_1', 'news_update')
2. A specific search query that focuses on one aspect of the main query
3. The source type to search (web, news, academic, specialized)
4. Time period relevance (today, last week, recent, past_year, all_time)
5. Domain focus if applicable (technology, science, health, etc.)
6. Priority level (1-highest to 5-lowest)

All fields (id, query, source_type, time_period, domain_focus, priority) are required for each subtask, except time_period and domain_focus which can be null if not applicable.

Create 2 subtasks that together will provide comprehensive coverage of the topic. Focus on different aspects, perspectives, or sources of information.

Each substask will include the following information:

id: str
query: str
source_type: str  # e.g., "web", "news", "academic", "specialized"
time_period: Optional[str] = None  # e.g., "today", "last week", "recent", "past_year", "all_time"
domain_focus: Optional[str] = None  # e.g., "technology", "science", "health"
priority: int  # 1 (highest) to 5 (lowest)

After obtaining the above subtasks information, you will add two extra fields. Those correspond to start_date and end_date. Infer this information given the current date and the time_period selected. start_date and end_date should use the format as in the example below:

"start_date": "2024-06-03T06:00:00.000Z",
"end_date": "2024-06-11T05:59:59.999Z",
```

#### Giải thích
- **Role definition**: “You are an expert research planner.”  
- **Dynamic context**: `{{ $now.toISO() }}` cung cấp thời gian hiện tại để agent có thể suy ra khoảng thời gian (`start_date`, `end_date`).  
- **Structured output spec**: mô tả chi tiết từng trường mà agent phải sinh ra.  
- **Constraints**: yêu cầu tạo **2 subtasks**, mỗi subtask phải có đầy đủ các trường (trừ `time_period` và `domain_focus` có thể `null`).

### 4.2 Instructions (trích)

```text
For each subtask, provide:
1. A unique string ID for the subtask (e.g., 'subtask_1', 'news_update')
2. A specific search query that focuses on one aspect of the main query
3. The source type to search (web, news, academic, specialized)
4. Time period relevance (today, last week, recent, past_year, all_time)
5. Domain focus if applicable (technology, science, health, etc.)
6. Priority level (1-highest to 5-lowest)

All fields (id, query, source_type, time_period, domain_focus, priority) are required for each subtask, except time_period and domain_focus which can be null if not applicable.

Create 2 subtasks that together will provide comprehensive coverage of the topic. Focus on different aspects, perspectives, or sources of information.
```

*Lưu ý*: Việc chỉ định **priority** là 1‑5 tránh việc modèle sử dụng thang đo khác (ví dụ: 1‑10) và đồng bộ hoá dữ liệu xuống các bước sau.

### 4.3 Structured Inputs & Outputs – ví dụ JSON

#### Định dạng fields (được đưa vào prompt như “hint”)

```text
Each substask will include the following information:

id: str
query: str
source_type: str  # e.g., "web", "news", "academic", "specialized"
time_period: Optional[str] = None  # e.g., "today", "last week", "recent", "past_year", "all_time"
domain_focus: Optional[str] = None  # e.g., "technology", "science", "health"
priority: int  # 1 (highest) to 5 (lowest)
```

#### JSON example được dùng để cấu hình tool output parser trong n8n

```json
{
  "subtasks": [
    {
      "id": "openai_latest_news",
      "query": "latest OpenAI announcements and news",
      "source_type": "news",
      "time_period": "recent",
      "domain_focus": "technology",
      "priority": 1,
      "start_date": "2025-06-03T06:00:00.000Z",
      "end_date": "2025-06-11T05:59:59.999Z"
    },
    {
      "id": "openai_official_blog",
      "query": "OpenAI official blog recent posts",
      "source_type": "web",
      "time_period": "recent",
      "domain_focus": "technology",
      "priority": 2,
      "start_date": "2025-06-03T06:00:00.000Z",
      "end_date": "2025-06-11T05:59:59.999Z"
    }
  ]
}
```

#### Kết quả sau khi parser hoạt động (trích từ n8n)

```json
[
  {
    "action": "parse",
    "response": {
      "output": {
        "subtasks": [
          {
            "id": "subtask_1",
            "query": "OpenAI recent announcements OR news OR updates",
            "source_type": "news",
            "time_period": "recent",
            "domain_focus": "technology",
            "priority": 1,
            "start_date": "2025-06-24T16:35:26.901Z",
            "end_date": "2025-07-01T16:35:26.901Z"
          },
          {
            "id": "subtask_2",
            "query": "OpenAI official blog OR press releases",
            "source_type": "web",
            "time_period": "recent",
            "domain_focus": "technology",
            "priority": 1.2,   // lưu ý: priority vẫn được chấp nhận vì là số
            "start_date": "2025-06-24T16:35:26.901Z",
            "end_date": "2025-07-01T16:35:26.901Z"
          }
        ]
      }
    }
  }
]
```

*Điểm quan trọng*: Việc cung cấp **JSON example** cho tool output parser giúp n8n tự động sinh ra schema, sau đó parse output của LLM thành cấu trúc có thể dùng tiếp trong workflow (ví dụ: gửi từng subtask tới agent tìm kiếm).

### 4.4 Tools – chèn ngày giờ động

Trong n8n, ta có thể chèn trực tiếp:

```text
The current date and time is: {{ $now.toISO() }}
```

Đây là một **tool** đơn giản nhưng rất mạnh mẽ: nó cung cấp context thời gian thực, cho phép LLM suy ra `start_date`/`end_date` dựa trên `time_period` (ví dụ: “recent” → 7 ngày qua). Nếu không có công cụ này, LLM sẽ phải “đoán” ngày tháng, dẫn đến truy vấn tìm kiếm không chính xác.

### 4.5 RAG & Memory – caching sub‑queries

- Khi cùng một câu hỏi (`user_query`) xuất hiện lại, chúng ta lưu trữ các `subtask` đã sinh ra vào **vector store**.  
- KhiAgent nhận được một query mới, trước hết tra vector store; nếu tìm thấy sub‑task tương tự, chúng ta tái sử dụng chúng thay vì gọi LLM lại → giảm latency và chi phí.  
- Đây là một dạng **Context Engineering** vì chúng ta chọn **context** (các sub‑task đã biết) thay vì sinh ra context mới mỗi lần.

### 4.6 States & Historical Context – cho fase sửa đổi

Trong quy trình nghiên cứu sâu, agent có thể cần **sửa đổi** kế hoạch tìm kiếm sau khi xem lại kết quả trung gian. Do đó, ta lưu trữ:
- Trạng thái của mỗi subtask (original, revised).  
- Kết quả tìm kiếm trung gian từ mỗi agent.  
- Những lần sửa đổi đã xảy ra.  

Khi进入 revision phase, agent được cung cấp toàn bộ lịch sử này để quyết định việc thay đổi query, thay đổi priority, hoặc bổ sung nguồn mới. Quá trình này đòi hỏi một **eval pipeline** để đo lường xem việc lưu trữ lịch sử có cải thiện chất lượng báo cáo cuối hay không.

---

## 5. Tổng kết

- **Context Engineering** là một mở rộng của Prompt Engineering, tập trung vào việc **thiết kế và tối ưu toàn bộ ngữ cảnh** (instructions, user input, tools, memory, structured I/O…) để LLM hoạt động hiệu quả.  
- Các thành phần chính bao gồm: **System Prompt**, **Instructions**, **User Input**, **Structured Inputs & Outputs**, **Tools**, **RAG & Memory**, **States & Historical Context**.  
- Trong ví dụ Search Planner Agent, chúng ta thấy cách mỗi thành phần đóng góp vào khả năng của LLM tạo ra **subtasks** có cấu trúc chuẩn, kèm theo `start_date`/`end_date` chính xác, và cách các kỹ thuật như tool output parser, caching và lưu trữ trạng thái giúp workflow trở nên **tự động**, **tín cậy** và **chi phí thấp**.  
- Để thành công, cần **lặp lại** quá trình thiết kế → đánh giá → cải thiện, đồng thời xây dựng **eval pipeline** để đo lường hiệu quả của các thay đổi về ngữ cảnh.

Bằng cách áp dụng các nguyên tắc trên, bạn sẽ có thể xây dựng các agent AI mạnh mẽ, linh hoạt và tối ưu cho những tác vụ phức tạp như nghiên cứu sâu, trò chuyện đa bậc, hoặc bất kỳ ứng dụng nào đòi hỏi sự kết hợp chặt chẽ giữa kiến thức bên ngoài và khả năng suy luận của LLM. Hãy bắt đầu bằng việc xác định vai trò cụ thể cho agent, cung cấp clear instructions, structured output spec và bổ sung các công cụ động (date/time, vector store…) – những bước này chính là lõi của **Context Engineering**.