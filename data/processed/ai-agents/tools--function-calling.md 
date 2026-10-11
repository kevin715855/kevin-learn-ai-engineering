# AI Agent Tools: So sánh 15+ Nền tảng Phổ biến

## 1. Mục tiêu học tập
Sau bài học này, người học sẽ:
- Hiểu bản chất của **AI agent** và cách nó khác với chatbot.
- Nắm được bốn nhóm chính của công cụ agent hiện nay và ví dụ代表 của mỗi nhóm.
- Giải thích các tiêu chí chọn lựa agent (tự chủ‑kiểm soát, độ tin cậy‑độ chuẩn, khả năng tích hợp, bảo mật‑tuân thủ, chi phí‑mô hình giá).
- Hiểu vai trò của hai tiêu chuẩn mở **MCP** (Model Context Protocol) và **A2A** (Agent‑to‑Agent) trong hệ sinh thái agent.
- Nhận biết những thách thức còn tồn tại về độ tin cậy, quyết định phức tạp và quản trị (governance) của agent.

## 2. Tổng quan
AI agent là một hệ thống thực hiện một **vòng lặp** (loop): đọc ngữ cảnh → chọn công cụ → thực hiện hành động → kiểm tra kết quả → quyết định bước tiếp theo cho tới khi nhiệm vụ kết thúc hoặc đạt một giới hạn nào đó. Vòng lặp này giúp agent không chỉ trả lời (như chatbot) mà còn **lập kế hoạch, thực hiện và điều chỉnh** dựa trên phản hồi từ môi trường.

Bài viết nguồn so sánh hơn 15 nền tảng agent được phân loại vào bốn danh mục:
1. **AI coding agents** – hỗ trợ phát triển mã nguồn.
2. **Enterprise agent platforms** – nền tảng quản lý và điều phối agent trong doanh nghiệp.
3. **Customer service and conversational agents** – agent tương tác với khách hàng.
4. **Agent development and automation frameworks** – công cụ để xây dựng agent tự do.

Ngoài ra, bài viết còn trình bày các cấp độ tự chủ của agentic AI, các yếu tố ảnh hưởng tới quyết định mua sắm, và thách thức quản trị mà ngành vẫn chưa giải quyết hoàn toàn.

## 3. Kiến thức cốt lõi

### 3.1 AI agent vs. chatbot
- **Chatbot**: chỉ sinh ra câu trả lời dựa trên prompt hiện tại.
- **Agent**: thực hiện một chuỗi hành động có thể thay đổi trạng thái bên ngoài (ví dụ: sửa file, gọi API, tạo tickets) và chỉ tiếp tục sau khi kiểm tra kết quả của mỗi bước.

### 3.2 Quatre nhóm công cụ agent

| Nhóm | Mục đích chính | Ví dụ đại diện |
|------|----------------|----------------|
| **AI coding agents** | Hỗ trợ viết, sửa, kiểm tra mã trong IDE hoặc terminal. | Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Kiro (AWS) |
| **Enterprise agent platforms** | Cung cấpcontrol plane, quản lý identidad, audit trail, và kết nối với hệ thống nội bộ. | OpenAI Frontier, Microsoft Agent 365, Gemini Enterprise Agent Platform, IBM watsonx Orchestrate, Creatio AI Studio |
| **Customer service & conversational agents** | Tự động hóa phản hồi khách hàng qua chat, voice hoặc SMS. | Salesforce Agentforce, OpenAI Presence, Tidio Lyro |
| **Agent development & automation frameworks** | Cung cấp runtime hoặc workflow để các đội tự-built agent. | LangGraph, CrewAI, n8n |

### 3.3 Các cấp độ tự chủ (Levels of Agentic AI)
| Mô tả | Thành phần chính |
|-------|------------------|
| **Level 4 – Highly autonomous, adaptive** | LLM + tools + intent, actions, reasoning/decision‑making, memory/reflection, autonomous learning, generalization |
| **Level 3 – Context‑aware & reflective** | LLM + tools + intent, actions, reasoning/decision‑making, memory/reflection, context awareness |
| **Level 2 – Strategic task automation** | RL‑based AI + tools + intent, actions, reasoning/decision‑making |
| **Level 1 – Rule‑based (deterministic)** | Rule‑based AI + tools + intent, actions (simple step sequences) |

### 3.4 Tiêu chí chọn lựa agent

1. **Autonomy vs. Control** – Mức độ agent có thể hành động mà không cần sự đồng ý con người. Các công cụ như Cursor, Claude Code giữ con người tại điểm quyết định (copilot), trong khi nền tảng hoàn toàn tự động cần có guardrails mạnh.
2. **Reliability vs. Accuracy** – Nghiên cứu Princeton (2024‑2026) cho thấy độaccuracy tăng đều nhưng độtin cậy (consistency across runs) cải thiện chậm. Một agent có thể giải quyết một nhiệm vụ thường xuyên nhưng lại thất bại trong một số lần lặp → rủi ro về liability.
3. **Integration depth** – Hai tiêu chuẩn mở hiện nay:
   - **MCP (Model Context Protocol)**: kết nối agent với công cụ (tools). Phiên bản 2026‑07‑28 chuyển thành stateless request/response, sử dụng header‑based routing (`Mcp-Method`, `Mcp-Name`), cache‑able list results, và cứng hơn về authorization.
   - **A2A (Agent‑to‑Agent protocol)**: cho phép agent trao đổi thẻ danh tính (Agent Cards) và làm việc cùng nhau. Được quỹ Linux Foundation� vært, đã có hơn 150 tổ chức hỗ trợ và triển khai trong供应链, tài chính, bảo hiểm, IT ops.
4. **Security, identity, compliance** – Mỗi agent nên có:
   - Một **identity** riêng ràng với quyền truy cập được scoped到 một công việc cụ thể.
   - Nhật ký audit và một **kill switch** có thể dừng thực hiện giữa chừng.
   - Tuân thủ OWASP Top 10 for Agentic Applications (ASI01‑ASI10) và các quy định EU AI Act (transparentiy obligations, machine‑readable markings).
5. **Cost & pricing model** – Các mô hình phổ biến:
   - Per‑seat / per‑agent‑instance (flat fee).
   - Consumption (per task, API call, voice minute).
   - Outcome (per resolved ticket, booked meeting, collected invoice).
   - Hybrid (platform fee + usage/outcome tier) – đang trở thành chuẩn mã vì mang lại mức chi phí dự đoán được và phần thưởng cho nhà cung cấp.

### 3.5 Governance – Vấn đề chưa được giải quyết hoàn toàn
- Các công cụ mới như **Cisco AI Agent Monitor**, **OpenAI Frontier**, **Agentic AI Foundation (AAIF)**, và **Creatio AI Studio** đã cung cấp giám sát thực thời, danh tính agent, và bảng điều khiển gouvernance.
- Tuy nhiên, vấn đề **error propagation** trong hệ thống multi‑agent (một lỗi được chấp nhận làm tiền đề cho các agent sau) và **khả năng xử lý tình huống phức tạp** (cần shared understanding, empathy, hoặc Talking‑through) vẫn còn là bài toán nghiên cứu mở.

### 3.6 Những gì hoạt động tốt hôm nay
- **Coding assistance** với con người làm reviewer (fast IDE agent + slower reasoning agent).
- **High‑volume repetitive support** – agent giải quyết các truy vấn thường xuyên, cải thiện thời gian trả lời dù tỷ lệ hoàn thành chưa cao.
- **Research synthesis** – agent quét tài liệu mới, trích dẫn và lưu reference list.
- **Governed agent inventories** – các nền tảng mới giúp đếm, cấp quyền và theo dõi agent từ nhiều nguồn khác nhau.

### 3.7 Những gì còn chưa дося được
- Triển khai tự động hoàn toàn (ví dụ: deploy code hoặc chuyển tiền) mà không có sự phê duyệt do độtin cậy thấp.
- Xử lý tình huống khách hàng đòi hỏi **empathy, judgement** hoặc **unstated context**.
- Quyết định đa‑phía liên quan đến **organizational politics** hoặc **unspoken constraints**.
- Phát triển **chiến lược mới** – agent chỉ tối ưu trong các ràng buộc đã cho, không thắc mắc đối với các ràng buộc đó.
- **Quản lý lỗi đa‑agent** – việc một agent truyền sai sót làm nguyên nhân cho agent khác cần nhiều nghiên cứu hơn.

## 4. Ví dụ minh họa

### 4.1 Vòng lặp hoạt động của một agent (mô tả)
> 1. **Đọc ngữ cảnh** – agent lấy nội dung ticket hỗ trợ khách hàng hoặc yêu cầu lập kế hoạch từ bộ nhớ chung.  
> 2. **Chọn công cụ** – dựa trên mục tiêu, agent tra cứu danh sách công cụ có sẵn qua MCP (ví dụ: công cụ kiểm tra mã, công cụ tạo pull request).  
> 3. **Thực hiện** – gọi công cụ, chờ kết quả (ví dụ: chạy unit test).  
> 4. **Kiểm tra kết quả** – nếu test fail, agent ghi lại lỗi và quyết định sửa code; nếu pass, chuyển sang bước tiếp theo (ví dụ: tạo commit).  
> 5. **Lặp hoặc dừng** – agent lặp lại cho tới khi đạt mục tiêu (pull request ready) hoặc đạt giới hạn số lần thử, sau đóawait human approval trước khi merge.

### 4.2 So sánh ngắn gọn hai công cụ coding
| Công cụ | Điểm mạnh | Giới hạn chính |
|---------|-----------|----------------|
| **Claude Code** | Hoạt động trong terminal, có khả năng review mã và đưa phản hồi nội dòng mà không tự merge. | Cần thiết lập môi trường local; phụ thuộc vào khả năng truy cập repo. |
| **OpenAI Codex** |Có sẵn qua CLI, desktop app, IDE và ChatGPT; hỗ trợ import session từ Claude Code / Cursor. | Mặc định model thay đổi thường xuyên → các benchmark nhanh lỗi thời. |

### 4.3 Minh họa việc sử dụng MCP
Một request MCP stateless có thể trông như sau (giả sử JSON trong body):
```json
{
  "method": "tools/list",
  "params": {}
}
```
- Header `Mcp-Method: tools/list` và `Mcp-Name: <tool‑name>` cho phép gateway định tuyến mà không cần phân tích body.
- Phảpplication trả về kèm `cache-control` và thứ tự định danh xác định để upstream prompt cache ổn định khi kết nối lại.

### 4.4 Ví dụ mô hình giá hybride (Creatio AI Studio)
- **Platform fee**: trả hằng tháng cố định, không giới hạn số lượng agent hoặc workflow.
- **Model consumption**: mỗi lần gọi LLM trừ credits từ tài khoản; credits có thể mua thêm tùy sử dụng.
Mô hình này giúp doanh nghiệp chi phí dự đoán được phần nền tảng, đồng thời trả theo mức sử dụng thực tế của mô hình AI.

## 5. Tổng kết
- AI agent được định nghĩa bằng **vòng lặp percep‑act‑observe** cho phép nó thực hiện những hành động có hậu quả trong thế giới thực, khác biệt根本 với chatbot chỉ trả lời.
- Thị trường hiện nay chia thành bốn nhóm chính: công cụ hỗ trợ coding, nền tảng enterprise, agent chăm sóc khách hàng, và framework để tự‑built agent.
- Khi chọn agent, đội needs to cân bằng **tự chủ‑kiểm soát**, **tin cậy‑chuẩn**, **khả năng tích hợp** (thông qua MCP và A2A), **bảo mật‑tuân thủ**, và **mô hình giá** phù hợp với quy mô và mục tiêu sử dụng.
- Mặc dù nhiều giải pháp đã xử lý tốt các trường hợp lặp lại và hỗ trợ phát triển, các thách thức về **độ tin cậy lâu dài**, **quyết định phức tạp**, và **lỗi lan truyền trong hệ thống multi‑agent** vẫn cần nghiên cứu và cải tiến thêm.
- Việc nắm vững những khái niệm trên sẽ giúp bạn đánh giá, triển khai và quản lý agent một cách có trách nhiệm và hiệu quả trong dự án AI của mình.