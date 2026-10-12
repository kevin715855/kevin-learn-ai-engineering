# Structured Output (Đầu ra có cấu trúc)

## 1. Mục tiêu học tập
Sau khi học bài này, bạn sẽ có thể:
- Giải thích khái niệm Structured Output và tại sao nó được gọi là “constrained decoding based on grammar”.
- Mô tả cách hoạt động của Structured Output ở mức token (logits processor) và tại sao nó có thể ép mô hình trả về theo một schema cụ thể.
- Viết và sử dụng các mô hình Pydantic (hoặc tương đương) để định dạng đầu ra của LLM.
- Đánh giá lợi ích và hạn chế của Structured Output, đặc biệt là ảnh hưởng đến độ chính xác và cách giảm thiểu bằng Schema‑Guided Reasoning (SGR).
- Liệt kê một số triển khai phổ biến của Structured Output trên các nền tảng cloud và local.

## 2. Tổng quan
Structured Output là kỹ thuật bắt buộc LLM sinh ra chuỗi text mà chỉ tuân thủ một schema được xác định trước (ví dụ: JSON schema, Pydantic model). Khi áp dụng, mô hình không thể sinh ra token ngoài bộ cho phép → đầu ra luôn có cấu trúc và có thể được trực tiếp chuyển đổi thành đối tượng lập trình mà không cần bước phân tích phức tạp (regex, split, v.v.).  

Kỹ thuật này được phổ biến bởi OpenAI nhưng hiện nay đã có trong nhiều dịch vụ云 (Mistral, Google Gemini) và các thư viện local như XGrammar, Outlines. Tuy nhiên, việc ép constraints có thể làm giảm khả năng “suy nghiego” của mô hình, vì vậy thường được kết hợp với Schema‑Guided Reasoning (SGR) để duy trì độ chính xác.

## 3. Kiến thức cốt lõi

### 3.1 Nguyên lý hoạt động
- Khi LLM tạo ra từng token, nó đưa ra xác suất cho tất cả các token trong từ vựng.
- Structured Output chèn một **logits processor** (ví dụ: lớp `Guidance` trong ví dụ) để **mask** (đặt giá trị -∞) cho những token không cho phép theo schema.
- Kết quả là chỉ những token thỏa mãn grammar/schema được cho phép sinh ra → đầu ra tuân thủ строго về cú pháp (JSON, field types, v.v.).
- Ở mức triển khai, thường chuyển schema thành **JSON Schema** rồi truyền vào engine deducing (xgrammar, outlines, …).

### 3.2 Định nghĩa schema bằng Pydantic (Python)
```python
from pydantic import BaseModel
from typing import Literal, List

class SqlResponse(BaseModel):
    sql_query: str
    query_type: Literal["read", "write", "delete", "update"]
    tables: List[str]

class ComponentResponse(BaseModel):
    height_mm: float
    width_mm: float
    depth_mm: float
    number_of_pins: int
    component_type: Literal["AC/DC", "DC/DC"]
```
- Mỗi lớp là một schema; khi yêu cầu LLM trả về `SqlResponse`, đầu ra sẽ là một đối tượng có các trường `sql_query`, `query_type`, `tables` với kiểu dữ liệu đã được khai báo.
- Các engine hỗ trợ Structured Output sẽ tự động chuyển lớp Pydantic này thành JSON Schema trước khi đưa vào model.

### 3.3 Ví dụ thực tế: trích xuất sự kiện lịch từ tin nhắn
Giả sử chúng ta muốn lấy dữ liệu lịch từ tin nhắn chat.

```python
# Định dạng đầu ra mong muốn
class CalendarEvent(BaseModel):
    title: str
    start: str   # ISO‑8601
    end: str
    participants: List[str]
```

Khi LLM được hướng dẫn trả về theo schema `CalendarEvent`, chúng ta có thể nhận được đối tượng trực tiếp:

```json
{
  "title": "Team sync",
  "start": "2025-10-02T10:00:00Z",
  "end": "2025-10-02T11:00:00Z",
  "participants": ["Alice", "Bob"]
}
```
Sau khi parse, `event.participants` sẽ là list `['Alice', 'Bob']` – không cần regex hay tách chuỗi thủ công.

### 3.4 Ví dụ local: buộc mô hình trả lời bằng ngôn ngữ Gruzi (Georgian)
Dưới đây là cách sử dụng `LogitsProcessor` để hạn chế từ vựng chỉ cho phép các ký tự Gruzi và dấu câu.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor
import torch
import regex

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

# Tạo mask cho các token không thuộc bảng Gruzi
alphabet = re.compile(r'[\u10A0-\u10FF]+')
punctuation = regex.compile(r'^\P{L}+$')

drop_mask = torch.zeros(1, tokenizer.vocab_size, dtype=torch.bool, device="cuda:0")
for token, idx in tokenizer.get_vocab().items():
    s = token.lstrip('▁')
    if alphabet.match(s) or punctuation.match(s):
        continue
    drop_mask[0][idx] = True
drop_mask[0][tokenizer.eos_token_id] = False   # luôn cho phép token kết thúc

class Guidance(LogitsProcessor):
    def __call__(self, input_ids, scores):
        return scores.masked_fill(drop_mask, float('-inf'))

# Prompt
messages = [
    {"role": "user", "content": "Write me a mayonnaise recipe. Please answer in Georgian"}
]
tokens = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")

generated_ids = model.generate(
    tokens,
    max_new_tokens=1000,
    do_sample=True,
    num_beams=5,
    renormalize_logits=True,
    logits_processor=[Guidance()]
)

decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])
```
**Lưu ý:** Mặc dù kết quả sẽ chỉ chứa ký tự Gruzi, nhưng vì model chưa được đào tạo cho ngôn ngữ này, nội dung có thể trở nên **gibberish** (không có nghĩa). Đây là một trong những **caveat** chính của Structured Output: việc ép format không tự động cung cấp kỹ năng linguistics cho mô hình.

## 4. Ví dụ minh họa (tích hợp)
### 4.1 Sử dụng Pydantic để định dạng đầu vào/đầu ra của một agent
```python
from pydantic import BaseModel, Field
from typing import Literal

class AgentResponse(BaseModel):
    action: Literal["search", "answer", "clarify"] = Field(
        ..., description="What the agent should do next"
    )
    payload: str = Field(..., description="Content associated with the action")
```
Khi agent nhận được JSON tuân thủ schema này, chúng ta có thể ngay lập tức thực hiện:
- Nếu `action == "search"` → thực hiện tìm kiếm với `payload` là từ khóa.
- Nếu `action == "answer"` → trả về `payload` làm câu trả lời cuối cùng.
- Nếu `action == "clarify"` → hỏi lại người dùng để làm rõ `payload`.

### 4.2 Kết hợp với Schema‑Guided Reasoning (SGR)
SGR đề xuất đưa **reasoning steps** vào schema trước khi sinh câu trả lời cuối cùng. Ví dụ:
```python
class ReasonedAnswer(BaseModel):
    steps: List[str]                       # chuỗi suy luận intermédiaires
    final_answer: str                      # kết quả sau khi suy luận
```
LLM trước tiên sinh ra `steps` (mỗi bước là một câu reasoning), sau đó dựa trên các bước đó produce `final_answer`. Vì việc sinh `steps` không bị hạn chế quá chặt, mô hình vẫn có không gian để “nghĩ”, giảm thiểu việc mất độ chính xác do constrained decoding.

## 5. Tổng kết
- **Structured Output** là phương pháp ép LSTM/LLM sinh ra text tuân thủ một schema qua **constrained decoding** (logits processor).  
- Nó giúp **tiếp cận langsung** đầu ra dưới dạng đối tượng lập trình (Pydantic, dataclass, …) mà không cần phân tích chuỗi phức tạp.  
- Khi áp dụng, cần lưu ý:
  - Không cung cấp thêm kỹ năng ngôn ngữ hoặc kiến域 cho model → có thể sinh ra nội dung không anlam nếu model chưa được huấn luyện cho định dạng đó.  
  - Giới hạn quá chặt có thể làm giảm độ chính xác vì model không được tự do “suy nghiego” trước khi trả lời.  
  - Một số API (OpenAI, Mistral, Gemini) sẽ tự chèn description vào prompt; cần kiểm tra nếu tự triển khai.  
- Để cân bằng giữa **định dạng chắc chắn** và **độ chính xác**, thường kết hợp Structured Output với **Schema‑Guided Reasoning (SGR)**.  
- Các triển khai phổ biến bao gồm: OpenAI Structured Outputs, Mistral Structured Outputs, Google Gemini Structured Outputs, cũng như thư viện local XGrammar và Outlines.  

Với những điểm trên, bạn có thể tự tin áp dụng Structured Output vào các hệ thống AI assistant để duy trì độ tin cậy của dữ liệu đầu ra, đồng thời luôn cân nhắc đến các giới hạn và biện pháp bổ trợ như SGR để giữ hiệu suất tổng thể của mô hình.