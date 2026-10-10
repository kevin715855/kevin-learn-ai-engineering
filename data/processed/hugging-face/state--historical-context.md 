# State, Memory, và Context trong AI Agents: Cách AI ghi nhớ những gì bạn đã hỏi

## 1. Mục tiêu học tập

Sau bài học này, người học sẽ:

- Nắm được ba khái niệm nền tảng **Context**, **State**, **Memory** trong thiết kế AI agent.  
- Hiểu vai trò cụ thể của mỗi khái niệm và cách chúng tương tác trong một quy trình thực tế (ví dụ: agent lập kế hoạch học tập).  
- Nhận biết những hậu quả khi một trong ba thành phần bị thiếu hoặc sử dụng sai.  
- Áp dụng kiến thức để phân tích, debug hoặc thiết kế agent đơn giản bằng cách quản lý context, state và memory một cách có hệ thống.

## 2. Tổng quan

Khi tương tác với một AI agent (chatbot, trợ lý ảo, hay workflow orchestrator), người dùng thường cảm thấy AI “ghi nhớ” những gì đã nói trước đó và có thể đưa ra phản hồi phù hợp. Trong thực tế, khả năng này không xuất phát từ một bộ nhøl giống con người mà từ ba cơ chế riêng biệt:

- **Context** – đoạn văn bản mà mô hình ngôn ngữ (LLM) có thể nhìn thấy ngay tại thời điểm thực hiện inference (prompt window).  
- **State** – trạng thái nội bộ của agent mô tảtask đang được thực hiện, bao gồm mục tiêu, các biến trung間 và tiến độ.  
- **Memory** – kho lưu trữ dài hạn (database, vector store, …) giữ lại thông tin về người dùng hoặc các phiên làm việc trước để tái sử dụng.

Bài học sẽ giải thích từng khái niệm qua ví dụ cụ thể của một **study‑plan agent** (agent giúp lập kế hoạch học tập 7 ngày), sau đó tổng kết cách chúng phối hợp và những lỗi thường gặp khi thiếu một trong ba thành phần.

## 3. Kiến thức cốt lõi

### 3.1 Context – “Những gì được nói ngay bây giờ”

- Định danh: Danh sách token (từ, dấu câu) mà LLM nhận làm input trong một lần gọi model.  
- Đặc điểm:  
  - Hạn chế bằng kích thước cửa sổ context (ví dụ: 4k, 8k, 32k token).  
  - Chứa toàn bộ lịch hội thoại gần đây, các chỉ dẫn hệ thống, và possibly các đoạn văn được truy xuất từ công cụ ngoài (retrieval).  
- Vai trò: Cung cấp “nguyên liệu” immediate để model sinh ra câu trả lời phù hợp. Nếu context thiếu thông tin cần thiết, model sẽ “đoán” hoặc trả lời không liên quan.  
- Minh họa (giả sử):  

  ```
  Prompt = 
  "Bạn là một agent lập kế hoạch học tập.
  Người dùng: Help me create a 7-day study plan for my exams.
  Agent: Sure! What subjects and how many hours per day can you study?
  Người dùng: Math, physics, and English. I can do 2 hours per day.
  Người dùng: Math is my weakest subject, please give it more time."
  ```

  Toàn bộ đoạn trên là **context** hiện tại mà model sẽ đọc để tạo phản hồi kế hoạch.

### 3.2 State – “Đang làm gì?”

- Định danh: Biểu diễn nội bộ (biến, đối tượng, JSON, …) mà agent duy trì để biết mình đang ở bước nào của một workflow.  
- Đặc điểm:  
  - Không phụ thuộc trực tiếp vào kích thước prompt; có thể lưu trữ trong RAM, trong process, hoặc trong một store tạm (ví dụ: Redis).  
  - Thường bao gồm: mục tiêu (goal), các input đã thu thập, các bước đã hoàn thành, và kế hoạch bước tiếp theo.  
- Vai trò: Đảm bảo agent không “quên” task mà đang thực hiện ngay cả khi conversation lan ra các Subject khác (side‑question).  
- Minh họa (pseudo‑code):

  ```python
  # State của study‑plan agent
  state = {
      "goal": "Build a 7‑day study schedule",
      "inputs": {
          "subjects": ["math", "physics", "english"],
          "hours_per_day": 2,
          "weak_subject": "math"
      },
      "progress": {
          "step": 2,               # 1: thu thập ràng buộc, 2: chia thời gian, 3: xếp lịch
          "time_allocation": {}    # sẽ được điền sau bước 2
      }
  }
  ```

  Khi người dùng hỏi “Also, do you think I should study in the morning or night?”, agent vẫn giữ `state` unchanged cho nhiệm vụ chính, trả lời câu hỏi side‑question, rồi tiếp tục từ bước hiện tại.

### 3.3 Memory – “Ghi nhớ cho lần sau”

- Định danh: Kho lưu trữ持久 (persistent) mà agent có thể ghi và đọc giữa các phiên làm việc (sessions).  
- Các hình thức thường见:  
  - Database quan hệ (SQL) lưu trữ thuộc tính người dùng.  
  - Vector store (FAISS, Pinecone, …) cho tìm kiếm semantic trên lịch sử hội thoại.  
  - Custom memory module (ví dụ: MemN2N, hoặc một simple key‑value store).  
- Vai trò: Cá nhân hoá phản hồi, giảm thiểu việc hỏi lại những thông tin đã biết, và cho phép agent cải thiện qua thời gian.  
- Minh họa (JSON được lưu sau khi tạo kế hoạch):

  ```json
  {
      "user_id": 123,
      "weak_subjects": ["math"],
      "average_daily_study_hours": 2,
      "last_plan_date": "2026-01-20",
      "preferred_subject_order": ["math", "physics", "english"]
  }
  ```

  Khi người dùng quay lại sau một tuần và nói “I’m starting a new semester. Help me plan my study routine again.”, agent sẽ truy xuất bản ghi trên, thấy rằng math luôn là subject yếu và tự động分配 nhiều thời gian cho math mà không cần người dùng lặp lại.

### 3.4 Ba thành phần làm việc cùng nhau (luồngTypical)

| Giai đoạn | Context (prompt) | State (internal) | Memory (persistent) |
|-----------|------------------|------------------|----------------------|
| Bắt đầu   | “Help me create a 7‑day study plan…” | Khởi tạo task `study_plan` với goal rỗng | Đọc Memory → có thể lấy `weak_subjects`, `hours_per_day` nếu có |
| Thu thập ràng buộc | Thêm “Math, physics, … 2h/day” | Cập nhật `inputs.subjects`, `inputs.hours_per_day` | Có thể lưu lại pattern “nguời dùng thường có 2h/ngày” |
| Thêm sở thích | Thêm “Math is my weakest …” | Đánh dấu `inputs.weak_subject = "math"` | Ghi lại `"weak_subjects": ["math"]` |
| Sinh kế hoạch | Toàn bộ đoạn hội thoại trên nằm trong context | Dựa vào `state` tính toán thời gian cho mỗi môn, tạo bảng 7‑ngày | Lưu kết quả plan và cập nhật thống kê người dùng |

## 4. Ví dụ minh họa

### 4.1 Mã giả đơn giản (Python‑like) cho study‑plan agent

```python
class StudyPlanAgent:
    def __init__(self, memory_store):
        self.memory = memory_store          # ví dụ: dict hoặc DB wrapper
        self.state = None                   # sẽ được tạo khi bắt đầu task

    def start_task(self, user_id, user_message):
        # 1️⃣ Load memory (long‑term)
        user_mem = self.memory.get(user_id, {})
        # 2️⃣ Initialize state (short‑term task)
        self.state = {
            "goal": "build_7day_plan",
            "inputs": {},
            "progress": {"step": 0}
        }
        # 3️⃣ Seed state with known memory (optional)
        if "weak_subjects" in user_mem:
            self.state["inputs"]["weak_subject"] = user_mem["weak_subjects"][0]
        if "average_daily_study_hours" in user_mem:
            self.state["inputs"]["hours_per_day"] = user_mem["average_daily_study_hours"]
        # 4️⃣ Return first reply (context will contain this exchange)
        return "Sure! What subjects and how many hours per day can you study?"

    def handle_message(self, user_message):
        # Context = all messages exchanged so far (simplified as a list)
        context = self._get_recent_dialogue()   # chưa cần triển khai chi tiết

        # Cập nhật state dựa trên nội dung tin nhắn mới (regex / intent detection)
        if "subject" in user_message.lower():
            self.state["inputs"]["subjects"] = self._extract_subjects(user_message)
        if "hour" in user_message.lower():
            self.state["inputs"]["hours_per_day"] = self._extract_number(user_message)
        if "weak" in user_message.lower():
            self.state["inputs"]["weak_subject"] = self._extract_weak_subject(user_message)

        # Nếu đủ thông tin, tạo kế hoạch
        if self._has_all_inputs(self.state["inputs"]):
            plan = self._generate_plan(self.state["inputs"])
            # Lưu kết quả vào memory cho lần sau
            self._update_memory(user_id, self.state["inputs"], plan)
            return plan
        else:
            # Vẫn thiếu thông tin → hỏi tiếp
            return self._next_question(self.state["inputs"])

    # … helper methods: _extract_subjects, _generate_plan, _update_memory, …
```

**Giải thích ngắn gọn:**

- `context` (ở đây là `_get_recent_dialogue()`) là toàn bộ tin nhắn mà agent nhìn thấy khi quyết định phản hồi tiếp theo.  
- `state` là đối tượng `self.state` chứa mục tiêu, các input đã thu thập và tiến độ công việc.  
- `memory` là `self.memory.get/upd` – kho lưu trữ dài hạn cho mỗi `user_id`.

### 4.2 Minh họa bằng hội thoại ngắn

| Người dùng | Agent (phản hồi) | Context hiện tại (tóm tắt) | State sau mỗi lượt |
|-----------|-------------------|---------------------------|--------------------|
| “Help me create a 7‑day study plan for my exams.” | “Sure! What subjects and how many hours per day can you study?” | [Yêu cầu khởi tạo] | `{goal: build_7day_plan, inputs:{}, progress:{step:0}}` |
| “Math, physics, and English. I can do 2 hours per day.” | “Got it. Any particular subject you find harder?” | + danh sách môn, giờ/ngày | `{inputs:{subjects:[math,physics,english], hours_per_day:2}}` |
| “Math is my weakest subject, please give it more time.” | (sinh ra kế hoạch 7‑ngày) | + câu chỉ ra môn yếu | `{inputs:{weak_subject:math}}` → plan được tạo |
| (Tuần sau) “I’m starting a new semester. Help me plan my study routine again.” | Agent truy xuất memory → thấy math là weak subject → đề xuất plan同様 không cần người dùng nói lại. | Chỉ có câu hỏi mới (memory đã cung khai wcześniej) | State khởi tạo lại, nhưng memory đã pre‑fill `weak_subject`. |

## 5. Tổng kết

- **Context** là “văn bản đang hiện thị trước eyes của LLM” – determines what the model can see right now.  
- **State** là “công việc mà agent đang thực hiện” – keeps track of goals, intermediate results, and progress, independent of prompt length.  
- **Memory** là “sổ note cá nhân của agent xuyên các phiên” – stores long‑term facts about users or past interactions to enable personalization and reduce repetitive questioning.  

Ba thành phần này **bù trừ** lẫn nhau:

- Thiếu **context** → model không có đủ dữ liệu để sinh phản hồi hợp lý (ví dụ: chỉ thấy “Math is my weakest…” mà không biết thời gian hoặc số ngày).  
- Thiếu **state** → agent có thể “mất tuyến” trong nhiệm vụ trung gian, đưa ra kế hoạch không đúng yêu cầu (ví dụ: chỉ给出 1‑ngày plan).  
- Thiếu **memory** → mỗi cuộc trò chuyện bắt đầu từ zero,Agent phải hỏi lại cùng các câu hỏi mỗi lần, dẫn đến trải nghiệm người dùng không mượt và tốn thời gian.

Trong thực tế, khi xây dựng AI agent thực thụ (tool‑calling, multi‑step workflows, copilots), việc **thiết kế duidelijk** cách lưu trữ, truy xuất và cập nhật ba thành phần này là chìa khóa để tạo ra hệ thống đáng tin cậy, nhất quán và “gần gũi” với người dùng.  

Khi bạn nhìn thấy bất kỳ hệ thống AI nào—từ trợ lý học tập, chatbot hỗ trợ khách hàng, cho tới hệ thống điều phối công việc—hãy nhớ: **context = what was said, state = what the agent is doing, memory = what survives for next time**. Nhận ra ba yếu tố này giúp bạn phân tích, gỡ lỗi và xây dựng agent tốt hơn.