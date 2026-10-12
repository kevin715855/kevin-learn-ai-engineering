# ReAct Prompting: Kết hợp reasoning và acting trong Large Language Models

## 1. Mục tiêu học tập
- Hiểu khái niệm ReAct và cách nó kết hợp reasoning (suy luận) và action (hành động) trong mô hình ngôn ngữ lớn (LLM).
- Giải thích luồng práce của ReAct: thought → action → observation và vai trò của từng bước.
- Áp dụng ReAct để xây dựng một agent đơn giản sử dụng LangChain và công cụ tìm kiếm ngoài.
- Nhận biết ưu điểm, hạn chế của ReAct so với các kỹ thuật prompting khác như Chain‑of‑Thought (CoT) và Act‑only.

## 2. Tổng quan
ReAct (Reason+Act) là một khung pracy được提出 bởi Yao et al., 2022 để khắc phục nhược điểm của LLM khi chỉ dựa trên kiến thức nội tại (ví dụ: CoT) – dễ mắc phải hallucination và không thể truy cập thông tin mới. ReAct cho phép LLM tạo ra **reasoning traces** (những bước suy luận dưới dạng văn bản) và **task‑specific actions** (hành động) xen kẽ, từ đó có thể truy cập nguồn ngoài như cơ sở conoscenza, công cụ tìm kiếm hoặc môi trường mô phỏng để thu thập thông tin cần thiết và cập nhật kế hoạch thực thi.

Khung này đã được chứng minh hiệu quả trên các tác vụ biết thức (question answering, fact verification) và quyết định (text‑based game, môi trường mua sắm trực tuyến), đồng thời nâng cao khả năng giải thích và độ tin cậy của LLM.

## 3. Kiến thức cốt lõi

### 3.1 Thành phần chính của ReAct
| Thành phần | Mô tả |
|-----------|-------|
| **Thought (Reasoning trace)** | Văn bản tự do mô tả suy luận, phân解 câu hỏi, lập kế hoạch, hoặc tổng hợp thông tin. |
| **Action** | Lệnh gọi một công cụ bên ngoài (ví dụ: `Search[query]`, `Lookup[entity]`, `Calculator[expr]`). |
| **Observation** | Kết quả trả về từ môi trường/công cụ sau khi thực hiện Action. |
| **Finish** | Action đặc biệt signal kết thúc và trả về câu trả lời cuối cùng. |

Các bước được lặp lại cho đến khi model tạo ra một `Finish` action chứa đáp án cuối cùng.

### 3.2 Lý do ReAct hoạt động tốt
- **Reasoning** giúp định hướng những thông tin cần tra cứu, giảm thiểu việc tìm kiếm vô hướng.
- **Acting** cung cấp truy cập đến kiến thức bên ngoài, bù đắp cho nhược điểm của LLM về việc lưu trữ và cập nhật kiến thức.
- Sự xen kẽ giữa thinking và acting cho phép model **điều chỉnh kế hoạch** khi nhận được thông tin mới (ví dụ: sửa lại truy vấn khi kết quả tìm kiếm không liên quan).

### 3.3 So sánh với các phương pháp khác
| Phương pháp | Ưu điểm | Nhược điểm |
|------------|---------|------------|
| **Act‑only** | Đơn giản, chỉ thực hiện hành động. | Không có suy luận → khó chia thành sub‑goals, dễ bỏ qua bối cảnh. |
| **Chain‑of‑Thought (CoT)** | Tuyệt vời cho suy luận nội tại (toán học,常识). | Không truy cập được thông tin mới → dễ sinh hallucination khi kiến thức cũ không đủ. |
| **ReAct** | Kết hợp cả hai: suy luận hướng dẫn action, action cung cấpevidence. | Phụ thuộc strongly vào chất lượng của công cụ ngoại vi; nếu kết quả tìm kiếm không hữu ích, suy luận có thể bị lệch. |
| **ReAct + CoT + Self‑Consistency** | Tận dụng điểm mạnh của cả hai, giảm lỗi qua sampling nhiều lần. | Độ phức tạp tăng, cần nhiều lần chạy model. |

## 4. Ví dụ minh họa

### 4.1 Minh họa ReAct trên HotpotQA (trích từ bài báo)

**Câu hỏi**  
```
Aside from the Apple Remote, what other devices can control the program Apple Remote was originally designed to interact with?
```

**Các bước thought‑action‑observation (rút gọn)**  

```
Thought 1: Tìm hiểu về Apple Remote và chương trình mà nó được thiết kế để điều khiển.
Action 1: Search[Apple Remote]
Observation 1: Apple Remote là điều khiển từ xa được dùng với Front Row, một ứng dụng播放 медиа trên macOS.

Thought 2: Cần tìm Front Row để biết những thiết bị nào có thể điều khiển nó.
Action 2: Search[Front Row]
Observation 2: Front Row có thể được điều khiển qua Apple Remote, đồng thời cũng hỗ trợ điều khiển qua phím tùy chọn trên keyboard và một số thiết bị Bluetooth.

Thought 3: Vì vậy, ngoài Apple Remote, các thiết bị như keyboard Bluetooth cũng có thể điều khiển chương trình ban đầu.
Action 3: Finish[Keyboard Bluetooth (và các thiết bị tương tự)]
```

Qua quá trình này, model đã **tra cứu** thông tin cần thiết (Apple Remote → Front Row) rồi **suy luận** để đưa ra đáp án cuối cùng.

### 4.2 Xây dựng ReAct Agent với LangChain (trích từ tài liệu)

```python
%%capture
# Cài đặt các thư viện cần thiết
!pip install --upgrade openai
!pip install --upgrade langchain
!pip install --upgrade python-dotenv
!pip install google-search-results

# Import thư viện
import openai
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from dotenv import load_dotenv
load_dotenv()

# Load API keys (cần có OPENAI_API_KEY và SERPER_API_KEY trong .env)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
```

```python
# Cấu hình LLM, công cụ và agent
llm = OpenAI(model_name="text-davinci-003", temperature=0)
tools = load_tools(["google-serper", "llm-math"], llm=llm)
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)
```

```python
# Chạy agent với truy vấn kompleks
agent.run(
    "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?"
)
```

**Chuỗi thực thi (trích từ output)**

```
> Entering new AgentExecutor chain...
 I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.
Action: Search
Action Input: "Olivia Wilde boyfriend"
Observation: Olivia Wilde started dating Harry Styles after ending her years-long engagement to Jason Sudeikis — see their relationship timeline.
Thought: I need to find out Harry Styles' age.
Action: Search
Action Input: "Harry Styles age"
Observation: 29 years
Thought: I need to calculate 29 raised to the 0.23 power.
Action: Calculator
Action Input: 29^0.23
Observation: Answer: 2.169459462491557

Thought: I now know the final answer.
Final Answer: Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557.
> Finished chain.
```

**Kết quả trả về**

```
"Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557."
```

Trong ví dụ trên, agent đã:
1. Sử dụng **Search** để lấy thông tin về boyfriend.
2. Sử dụng **Search** nữa để lấy tuổi.
3. Sử dụng **Calculator** (llm‑math) để tính lũy thừa.
4. Kết hợp suy luận và hành động để tạo ra câu trả lời cuối cùng.

## 5. Tổng kết
- ReAct là một phương pháp prompting mạnh mẽ vì nó **kết hợp reasoning và acting**, cho phép LLM truy cập và sử dụng kiến thức ngoài để cải thiện độ chính xác và giảm hallucination.
- Quy trình hoạt động qua các bước lặp: **Thought → Action → Observation**, cho phép mô hình duy trì và cập nhật kế hoạch hành động dựa trên thông tin mới thu được.
- Khi so sánh với Act‑only và CoT, ReAct đạt hiệu quả tốt hơn trên nhiều bài toán biết thức và quyết định, mặc dù vẫn phụ thuộc fortemente vào chất lượng của công cụ ngoài (công cụ tìm kiếm, API,…).
- Trong thực tiễn, việc xây dựng một ReAct agent với framework như LangChain rất đơn giản: chỉ cần cung cấp LLM, một tập công cụ (search, calculator,…) và khởi tạo agent với loại `zero-shot-react-description`.
- Để nâng cao độ ổn định, các nhà nghiên cứu thường kết hợp ReAct với CoT và Self‑Consistency (take majority vote từ nhiều samples), giúp giảm lỗi do kết quả tìm kiếm kém hoặc suy luận không chắc chắn.

Với những hiểu biết trên, bạn có thể bắt đầu áp dụng ReAct để xây dựng các hệ thống AI có khả năng **tương tác linh hoạt với môi trường ngoài**, từ trả lời câu hỏi phức tạp cho đến tự động hóa quy trình làm việc trên web và game dựa trên văn bản. Hãy thử nghiệm với các công cụ và tập dữ liệu khác nhau để感受 mức độ tăng cường mà ReAct mang lại.