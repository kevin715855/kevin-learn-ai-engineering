# ReAct Prompting: Kết hợp Reasoning và Acting trong LLM  

## 1. Mục tiêu học tập  

Sau bài học này, bạn sẽ able to:  

- Giải thích ý tưởng cốt lõi của framework **ReAct** và cách nó kết hợp *reasoning traces* (chuỗi suy luận) và *task‑specific actions* (hành động).  
- Mô tả luồng hoạt động của ReAct: Thought → Action → Observation và vai trò của mỗi thành phần.  
- So sánh ReAct với phương pháp Chain‑of‑Thought (CoT) và nêu điểm mạnh, điểm yếu của từng phương pháp.  
- Áp dụng ReAct để xây dựng một AI agent đơn giản bằng LangChain, sử dụng công cụ tra cứu và máy tính.  
- Đánh giá kết quả của ReAct trên các nhiệm vụ biết thức (knowledge‑intensive) và quyết định (decision‑making).  

## 2. Tổng quan  

ReAct (Reason+Act) được提出 bởi Yao et al., 2022 để khắc phục hạn chế của các mô hình ngôn ngữ lớn (LLM) khi chỉ dựa trên kiến thức nội bộ: chúng dễ sinh ra *fact hallucination* và không thể cập nhật thông tin mới từ môi trường bên ngoài.  

ReAct khuyến khích LLM tạo ra **reasoning traces** (chuỗi suy luận) và **actions** (hành động) xen kẽ, cho phép mô hình:  

- **Induce, track, update** kế hoạch hành động và xử lý ngoại lệ.  
- **Interface** với nguồn bên ngoài (knowledge base, công cụ tìm kiếm, môi trường mô phỏng) để thu thập thông tin mới.  
- **Improve** độ tin cậy và sự пояснюю interpretable của câu trả lời.  

Kết quả thử nghiệm cho thấy ReAct thường vượt qua các baseline mạnh trên các tác vụ hỏi đáp المعرفة (HotPotQA, Fever) và các trò chơi quyết định (ALFWorld, WebShop). Khi kết hợp với Chain‑of‑Thought (CoT) hoặc Self‑Consistency, ReAct cho hiệu suất tốt nhất.

## 3. Kiến thức cốt lõi  

### 3.1 Thành phần chính của ReAct  

| Thành phần | Mô tả | Ví dụ |
|-----------|-------|-------|
| **Thought (Suy luận)** | Văn bản tự do mô tả Reasoning: phân tích câu hỏi, lập kế hoạch, kết hợp thông tin đã biết. | “I need to search Colorado orogeny, find the area that the eastern sector extends into, then find the elevation range.” |
| **Action (Hành động)** | Lệnh gọi công cụ bên ngoài (tìm kiếm, tra cứu, máy tính, …). Định dạng thường là `ToolName[input]`. | `Action 1 Search[Colorado orogeny]` |
| **Observation (Quả 관찰)** | Kết quả trả về từ công cụ, được feeding lại vào prompt để tiếp tục suy luận. | `Observation 1 The Colorado orogeny was an episode of mountain building …` |

Quá trình lặp lại **Thought → Action → Observation** tạo ra một *trajectory* (quỹ đạo)Solution cho nhiệm vụ.

### 3.2 Khi nào dùng ReAct?  

- **Nhiệm vụ biết thức (knowledge‑intense)** – cần truy xuất thông tin外部 để trả lời câu hỏi (HotPotQA, fact‑checking).  
- **Nhiệm vụ quyết định (decision‑making)** – môi trường phức tạp yêu cầu lập kế hoạch và thực hiện hành động tuần tự (ALFWorld – trò chơi văn bản, WebShop – mua sắm trực tuyến).  

### 3.3 Ưu điểm và hạn chế  

| Ưu điểm | Hạn chế |
|--------|---------|
| Giảm fact hallucination bằng cách kiểm tra lại thông tin bên ngoài. | Cấu trúc suy luận–hành động có thể làm giảm sự linh hoạt trong việc tạo ra các bước suy luận phức tạp. |
| Tăng khả năng giải thích (interpretability) vì mỗi bước hành động có lý do rõ ràng. | Hiệu suất phụ thuộc fortemente vào chất lượng của kết quả tìm kiếm; kết quả không liên quan có thể làm lạc hướng suy luận. |
| Dễ kết hợp với CoT hoặc Self‑Consistency để wykorzysta cả kiến thức nội bộ và thông tin bên ngoài. | Vẫn chưa đạt được mức效率 của con người trên các tác vụ quyết định khó. |

## 4. Ví dụ minh họa  

### 4.1 Ví dụ suy luận trên HotPotQA (trích từ bài báo)

> **Question**: Aside from the Apple Remote, what other devices can control the program Apple Remote was originally designed to interact with?  

Quá trình ReAct (được rút gọn):

```
Thought 1: I need to find what program Apple Remote was originally designed to interact with.
Action 1: Search[Apple Remote original program]
Observation 1: Apple Remote was designed to control Front Row.

Thought 2: Now I need to find devices that can control Front Row.
Action 2: Search[Front Row control devices]
Observation 2: Devices include infrared receivers, Bluetooth adapters, and certain keyboards.

Thought 3: The answer is infrared receivers, Bluetooth adapters, and certain keyboards.
Action 3: Finish[infrared receivers, Bluetooth adapters, and certain keyboards]
```

### 4.2 Triển khai ReAct agent bằng LangChain (Python)

```python
%%capture
# Cài đặt các thư viện cần thiết
!pip install --upgrade openai
!pip install --upgrade langchain
!pip install --upgrade python-dotenv
!pip install google-search-results

# Import libs
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

# Cấu hình LLM và công cụ
llm = OpenAI(model_name="text-davinci-003", temperature=0)
tools = load_tools(["google-serper", "llm-math"], llm=llm)
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Chạy agent với một truy vấn phức hợp
result = agent.run(
    "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?"
)
print(result)
```

**Kết quả mong đợi** (tuỳ thuộc vào thời điểm truy vấn):

```
Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557.
```

**Giải thích ngắn gọn**  

1. **Thought** → xác định cần tìm bạn gái của Olivia Wilde.  
2. **Action** → sử dụng công cụ `google-serper` để tra cứu “Olivia Wilde boyfriend”.  
3. **Observation** → trả về “Harry Styles”.  
4. **Thought** → cần biết tuổi của Harry Styles.  
5. **Action** → tra cứu “Harry Styles age” → Observation: 29 years.  
6. **Thought** → cần tính 29^0.23.  
7. **Action** → sử dụng công cụ `llm-math` (máy tính) → Observation: 2.169459462491557.  
8. **Thought** → đã có câu trả lời cuối cùng.  
9. **Action** → `Finish` và in ra kết quả.

### 4.3 So sánh hiệu quả (trích từ bài báo)

| Phương pháp | HotPotQA (EM) | Fever (Acc) |
|------------|--------------|------------|
| Act only   | thấp          | thấp        |
| CoT        | cao          | trung bình |
| ReAct      | trung bình    | cao        |
| ReAct + CoT/ Self‑Consistency | **cao nhất** | **cao nhất** |

*Chú ý:* Các con số trên chỉ mang tính minh hoá; giá trị thực phụ thuộc vào bản thiết đặt và mô hình आधार.

## 5. Tổng kết  

- ReAct là một frameworkPrompting cho phép LLM tạo ra **reasoning traces** và **actions** xen kẽ, giúp mô hình truy xuất và sử dụng thông tin bên ngoài một cách có hệ thống.  
- Qua vòng lặp **Thought → Action → Observation**, ReAct có thể lập kế hoạch, sửa lỗi và đưa ra câu trả lời chính xác hơn so với chỉ dùng suy luận nội bộ (CoT) hoặc chỉ thực hiện hành động (Act).  
- Mặc dù ReAct giảm nguy cơ fact hallucination và tăng khả năng giải thích, hiệu suất của nó vẫn phụ thuộc vào chất lượng của công cụ tìm kiếm và có thể bị hạn chế bởi cấu trúc cứng của suy luận–hành động.  
- Kết hợp ReAct với CoT hoặc Self‑Consistency thường cho kết quả tốt nhất trên cả nhiệm vụ biết thức và quyết định.  
- Thực hành với LangChain cho thấy cách nhanh chóng xây dựng một **ReAct agent** sử dụng công cụ tìm kiếm (Google‑Serper) và máy tính (llm‑math) để xử lý các truy vấn đa bước.  

Bằng cách nắm vững nguyên lý và cách triển khai ReAct, bạn sẽ có thể thiết kế các hệ thống AI mạnh mẽ hơn, capazes của tương tác linh hoạt với thế giới thực và cung cấp đáp án được căn cứ bằng chứng.