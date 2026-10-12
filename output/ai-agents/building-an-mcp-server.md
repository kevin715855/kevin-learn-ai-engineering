# MCP (Model Context Protocol) – Kết nối AI agent với công cụ và dữ liệu

## 1. Mục tiêu học tập

- Hiểu được MCP là gì và vì sao nó trở thành chuẩn chung để kết nối AI agent với các công cụ bên ngoài.  
- Biết được ba thành phần chính của MCP: **tools**, **resources**, **prompts** và cách chúng hoạt động trong kiến trúc host‑client‑server.  
- Có thể xây dựng một MCP server đơn giản bằng Python + FastMCP, chạy qua stdio và kiểm tra bằng MCP Inspector.  
- Học cách chuyển server sang chế độ **streamable‑HTTP** để triển khai như một dịch vụ web và kết nối với máy khách như Claude Desktop hoặc Cursor.  
- Nắm được quy trình kết nối tới nhà cung cấp MCP được quản lý (Composio) để truy cập hơn 1.000 công cụ đã được xác thực sẵn.  
- Áp dụng một số nguyên tắc triển khai production (logging, validation, bảo mật, health check, versioning…) để MCP server ổn định trong môi trường thực tế.  

## 2. Tổng quan

Khi làm việc với các mô hình ngôn ngữ lớn (LLM), mỗi nhà cung cấp thường có định dạng gọi hàm riêng, mỗi tích hợp cần mã “dán” riêng và mỗi bản nâng cấp mô hình có thể gây hại cho các thành phần downstream.  

**Model Context Protocol (MCP)** ra đời để giải quyết vấn đề này bằng cách cung cấp một giao diện chuẩn cho **công cụ**, **nguồn dữ liệu** và **AI client**. Thay vì phải xây dựng lại tích hợp cho mỗi mô hình hoặc ứng dụng, ta chỉ cần展示 khả năng một lần qua một **MCP server**; các client MCP tương thích sẽ kết nối tới server đó và sử dụng các công‑cụ, tài nguyên và prompt mà server cung cấp.

MCP được ra mắt bởi Anthropic vào tháng 11/2024 và nhanh chóng được przyję bởi OpenAI, Microsoft, Google vào mùa xuân 2025, trở thành chuẩn de facto để kết nối hệ thống AI với các công cụ bên ngoài.

Bài học này sẽ hướng dẫn bạn:

- Xây dựng MCP server local (stdio) bằng Python + FastMCP.  
- Kiểm tra server với **MCP Inspector** (giao diện web).  
- Expose server qua **streamable‑HTTP** để chạy như dịch vụ web.  
- Kết nối tới **Composio MCP** – dịch vụ quản lý cung cấp hơn 1.000 công cụ đã được xác thực.  
- Áp dụng một use‑case nâng cao (phiên bản tài chính analyst) để thấy MCP hoạt động trong thực tế.  
- Điểm checklist trước khi triển khai production.

## 3. Kiến thức cốt lõi

### 3.1 MCP là gì?

- MCP server là một tiến trình **JSON‑RPC 2.0** exposed ba nguyên语 (primitives) tới mọi MCP client qua **stdio** hoặc **streamable HTTP**:
  - **Tools** – hàm mà mô hình có thể gọi (side‑effecting).  
  - **Resources** – dữ liệu chỉ‑read mà mô hình có thể đọc (ví dụ: nội dung file, thông tin hệ thống).  
  - **Prompts** – mẫuprompt có thể tái sử dụng để hướng dẫn mô hình thực hiện tác vụ.  

MCP không quy định chi tiết về cách triển khai các công cụ; đó là “implementation detail”. Điểm mạnh chính là **một lần học giao thức**, sau đó agent có thể nói chuyện với bất kỳ máy chủ MCP nào tuân thủ.

### 3.2 So sánh với API truyền thống

| Tiêu chí | MCP | REST / GraphQL / gRPC |
|----------|-----|-----------------------|
| Mục đích chính | Cung cấp một cách duy nhất cho LLM lấy context **và** gọi công cụ có side‑effect | Trao đổi dữ liệu máquina‑máquina chung, logic kinh doanh |
| Công sức tích hợp | Khi agent biết MCP, nó có thể giao tiếp với mọi máy chủ MCP‑compatible; chỉ cần một SDK/wire‑spec | Mỗi API có spec/SDK riêng → tích hợp từng cái một |
| Mô hình tương tác | Phiên trạng + tin nhắn双向; hỗ trợ tác vụ dài và callback tiến độ | Yêu cầu/phản hồi vô trạng; thường là một chiều |
| Hỗ trợ streaming | Chuẩn hoá qua “Streamable HTTP” (SSE/WebSocket) | Không phải phần của REST; dev thường tự thêm WebSocket/SSE |
| Mở rộng (thêm khả năng mới) | Server có thể thêm tool/resource mà không làm hỏng client; client khám phá tại thời gian chạy | Cần versioning hoặc client phải cập nhật endpoint/types mới |
| Chuẩn hoá wire format | Một JSON‑Schema cho input/output + transport được định nghĩa | Nhiều phong cách (REST, GraphQL, gRPC) với header/auth/error/media types khác nhau |
| 성숙도 & công cụ | Đang phát triển nhanh; nhiều server mã nguồn mở và hỗ trợ thương mại frü | thập kỷ các hướng dẫn best‑practice, gateway, SDK, APM, monitoring |
| Độ trễ đường đi | Thêm một hop (agent → MCP → API); streaming giảm thời gian chờ cho payload lớn | Gọi trực tiếp; thường thấp hơn cho tải‑lượng cao, xác định |
| Use case típico | Autonomous agents chaining nhiều công cụ, workflow động, user‑in‑the‑loop | Dịch vụ CRUD, tích hợp ổn định, micro‑service cao lưu lượng |

### 3.3 Kiến trúc MCP

```
MCP Host (ví dụ: Claude Desktop, Cursor) 
      ↓ (tạo) 
MCP Client (một‑mot kết nối tới một MCP Server) 
      ↓ 
MCP Server (công cụ, resources, prompts) 
      ↓ 
Nguồn dữ liệu địa phương hoặc dịch vụ xa (file, DB, API…)
```

- **MCP Host**: ứng dụng muốn sử dụng công cụ/dữ liệu qua MCP.  
- **MCP Client**: instance do host tạo ra, duy trì kết nối một‑mot tới một MCP Server.  
- **MCP Server**: chương trình nhẹ công开开具 tools/resources/prompts qua giao thức MCP.  
- **Local Data Sources**: file, database, codebase, dịch vụ local mà server có thể truy cập.  
- **Remote Services**: API/cloud externe (Google Sheets, GitHub, Slack, Postgres…) mà server có thể gọi.

Với cách phân lớp này, host không cần biết chi tiết về cách thức xác thực, gọi API, truy cập file – mọi thứ được ẩn sau interface MCP sạch.

### 3.4 Xây dựng MCP server local (Python + FastMCP)

**Yêu cầu**  
- Python 3.10+  
- Claude Desktop hoặc Cursor (để test)  
- (Tùy chọn) Node.js 18+ nếu muốn dùng TypeScript.

**Các bước**  

1. Tạo thư mục và môi trường ảo  

```bash
mkdir mcp_servers && cd mcp_servers
python3 -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install FastMCP
```

2. Tạo file `server.py` (ví dụ dưới đây chứa ba tool, một resource và hai prompt):

```python
# server.py
import base64, os, uuid
from typing import List
from fastmcp import FastMCP

mcp = FastMCP("Utility MCP Server")

@mcp.tool()
def generate_password() -> str:
    """Tạo mật khẩu ngược từ UUID4 (dev‑only)."""
    uuid_bytes = str(uuid.uuid4()).encode()
    b64 = base64.b64encode(uuid_bytes).decode()
    return b64[::-1]

@mcp.tool()
def list_files(directory: str = ".") -> List[str]:
    """Liệt kê tên file/thư mục trong `directory`."""
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def read_file(filename: str) -> str:
    """Đọc toàn bộ nội dung file (UTF‑8)."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.resource("data://sys-info")
def get_system_info() -> str:
    """Trả về snapshot phần cứng & tài nguyên hệ thống."""
    import platform, psutil, subprocess
    from datetime import datetime
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    day = now.strftime("%A")
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime = str(now - boot).split(".")[0]
    sys_t = platform.system()
    mach = platform.machine()
    cpu = psutil.cpu_count(logical=False)
    try:
        gpu = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=gpu_name", "--format=csv,noheader"],
            encoding="utf-8"
        ).strip()
    except Exception:
        gpu = "N/A (NVIDIA‑SMI not found)"
    cpu_usage = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    return f"""
             --- Hardware Specs ---
            OS:        {sys_t} ({mach})
            CPU:       {cpu} Physical Cores
            GPU:       {gpu}

            --- Temporal Context ---
            Date/Time: {ts}
            Day:       {day}
            Uptime:    {uptime}

            --- Resource Utilization ---
            CPU Load:  {cpu_usage}%
            RAM Usage: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)
            Disk (C:): {disk.percent}% Used ({disk.free // (1024**3)}GB Free)
            """

@mcp.prompt()
def helper_prompt(task: str, context: str = "") -> str:
    """Prompt chung cho bất kỳ tâche nào."""
    base = f"""
Task: {task}
Please approach this systematically:
1. Break down the problem
2. Consider multiple solutions
3. Explain your reasoning
4. Provide clear, actionable steps
"""
    if context:
        base += f"\n\nAdditional context: {context}"
    return base

@mcp.prompt()
def api_endpoint_design_prompt(endpoint_name: str, purpose: str) -> str:
    """Prompt thiết kế endpoint RESTful."""
    return f"""
Design a RESTful API endpoint: {endpoint_name}
Purpose: {purpose}
Please provide:
1. HTTP method and URL pattern
2. Request/response schemas with examples
3. Status codes and error handling
4. Authentication requirements
5. Rate limiting considerations
6. OpenAPI/Swagger documentation snippet
Follow REST conventions and include proper validation.
Use JSON for data exchange and meaningful HTTP status codes.
"""

if __name__ == "__main__":
    # Chạy qua stdio (local)
    mcp.run()
    # Để chạy qua streamable‑HTTP, thay dòng trên bằng:
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

**Giải thích các decorator quan trọng**  

- `@mcp.tool()` – bọc hàm và đăng ký nó như một **tool** có thể được LLM gọi. Docstring của hàm rất quan trọng vì nó giúp mô hình hiểu mục đích và đối số.  
- `@mcp.resource("uri")` – đăng ký hàm như một **resource**; client có thể đọc dữ liệu từ URI này (ví dụ: `data://sys-info`).  
- `@mcp.prompt()` – đăng ký hàm như một **prompt template**; client có thể gọi để lấy chuỗi prompt đã được parameters.  
- `mcp.run()` – khởi động server. Để chạy qua HTTP streamable, thay transport và chỉ định host/port như示范 ở trên.

3.5 Kiểm thử local bằng **MCP Inspector**

```bash
npx @modelcontextprotocol/inspector python server.py
```

Lệnh trên sẽ khởi động một trình inspect web tại `http://localhost:xxxx`. Nhấn **Connect**, sau đó bạn có thể gọi trực tiếp mỗi tool/resource/prompt và xem phản hồi JSON‑RPC. Điều này rất hữu ích để xác minh schema và xử lý lỗi trước khi kết nối với LLM thực.

3.6 Kết nối tới máy khách (Cursor / Claude Desktop)

Trong thư mục dự án của Cursor, tạo file `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "utility_server": {
      "type": "stdio",
      "command": "/full/path/to/.venv/bin/python",
      "args": ["/full/path/to/mcp_servers/server.py"]
    }
  }
}
```

Mở **Cursor Settings → Tools & MCPs**, tìm `utility_server` và bật **Enable**. Khi mở chat/agents, bạn có thể gọi các tool như `generate_password`, `list_files`… và server sẽ hỏi quyền trước khi thực hiện thao tác trên hệ thống (để tránh việc agent thay đổi files mà không đồng ý).

3.7 Expose server qua **streamable‑HTTP** (triển khai web)

Thay phần `if __name__ == "__main__":` trong `server.py` bằng:

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

Sau khi chạy, server sẽ lắng nghe tại `http://<host>:8000/mcp`. Cấu hình MCP client (ví dụ trong Cursor) sẽ trở thành:

```json
{
  "mcpServers": {
    "composio_http": {
      "type": "http",
      "url": "http://<host>:8000/mcp",
      "headers": {}
    }
  }
}
```

Với chế độ này, server hoạt động như một dịch vụ web có thể được đặt đằng sau reverse proxy, cân bằng tải, hoặc chạy trên các plataforma như Cloudflare Workers, Vercel Edge (nếu viết bằng TypeScript).

3.8 Kết nối tới **Composio MCP** (dịch vụ quản lý)

Thay vì tự host rất nhiều server, bạn có thể dùng **Composio MCP** – một nền tảng cung cấp hơn 1.000 công cụ đã được xác thực trước (Google Sheets, Slack, GitHub, …) qua một URL duy nhất.

Các bước cơ bản:

1. Truy cập https://dashboard.composio.dev/, đăng nhập hoặc tạo tài khoản.  
2. Ở phần **Install**, chọn MCP client bạn dùng (Claude, Cursor, VS Code…) và sao chép lệnh cài đặt.  
3. Ví dụ cho Claude:  

```bash
claude mcp add --scope user --transport http composio https://connect.composio.dev/mcp
```

4. Sau khi chạy lệnh, mở Claude và xác thực các ứng dụng cần thiết (Gmail, Google Drive,…) qua trang **Connect Apps** nếu muốn.  
5. Bây giờ agent có thể gọi bất kỳ công cụ nào trong kho Composio mà không cần quản lý từng API key riêng.

3.9 Use‑case nâng cao: **Financial Analyst Agent** (minh họa)

- Mục tiêu: Tự động thu thập dữ liệu tài chính (Yahoo Finance, SEC filings, Google Sheets), phân tích bằng Claude, tạo báo cáo trong Google Docs, lưu trữ và gửi email tóm tắtExecutive.  
- Thành phần chính:  
  - **Composio MCP** cung cấp công cụ kết nối tới các dịch vụ trên.  
  - Agent là một prompt (hoặc luồng pracy) chạy trong Claude/Cursor, lấy parameters như ID của Google Sheet, Google Doc template, folder Drive, địa chỉ GMAIL.  
  - Khi agent thực hiện, nó sẽ song song gọi nhiều công cụ qua MCP (ví dụ: `google_sheets.read`, `yahoo_finance.get_price`, `gmail.send_email`) và tổng hợp kết quả.  

Chi tiết cài đặt và prompt mẫu có sẵn trong repository của Composio; việc quan trọng nhất là agent chỉ cần biết **URL** của Composio MCP và các ID cần thiết – mọi xử lý xác thực, request rate‑limit, refresh token được Composio quản lý.

3.10 Checklist triển khai production

Trước khi đưa MCP server vào môi trường thực tế, hãy kiểm tra các mục sau:

| Mục | Mô tả |
|-----|-------|
| **Logging** | Ghi log vào `stderr` hoặc file; **không** ghi vào `stdout` khi chạy qua stdio (để không làm mất kết nối JSON‑RPC). |
| **Error handling** | Bọc mỗi tool/resource bằng `try/except`; trả về thông báo lỗi rõ ràng thay vì để exception nuốt kết nối. |
| **Input validation** | Sử dụng type hint (Python) hoặc Zod (TypeScript); thêm kiểm tra cụ thể (SQL injection, path traversal) khi làm việc với DB hoặc file hệ thống. |
| **Rate‑limit external API** | Để MCP quản lý tần suất gọi (Composio đã làm điều này) hoặc tự áp dụng limiter (ví dụ: `tenacity`, `aiolimiter`). |
| **Secrets** | Lưu API key, token trong biến môi trường; **không** hard‑code và **không** commit vào repo. |
| **Tool design** | Mỗi tool nên có một mục đích單一; tránh tạo tool “toàn năng” quá lớn. |
| **Schema versioning** | Khi thay đổi signature của tool/resource, tăng phiên bản server (ví dụ: `v1`, `v2`) để client có thể thích nghi. |
| **Health check** | Đối với server HTTP, exposición endpoint `/health` trả về `200 OK` khi mọi thứ ổn định. |
| **Authentication** | - Untuk nội部: dùng Bearer token. <br> - Untuk công khai: dùng OAuth 2.0. <br> - Không kết hợp cả hai trên cùng một endpoint công khai/riêng. |

Sau khi đáp ứng checklist, MCP server sẽ sẵn sàng để phục vụ nhiều client đồng thời mà vẫn giữ được độ tin cậy và bảo mật.

## 4. Ví dụ minh họa

### 4.1 Chạy local server và kiểm tra bằng MCP Inspector

```bash
# 1. Khởi động server (stdio)
python server.py
# Terminal sẽ không xuất ra gì trừ khi có log error.

# 2.Trong một terminal khác, chạy Inspector
npx @modelcontextprotocol/inspector python server.py
```

Mở trình duyệt tới URL mà Inspector in ra (thường là `http://127.0.0.1:xxxx`). Nhấn **Connect**, bạn sẽ thấy danh sách các tool: `generate_password`, `list_files`, `read_file`; resource: `data://sys-info`; prompt: `helper_prompt`, `api_endpoint_design_prompt`. Nhấn vào bất kỳ tool nào, nhập đối số (nếu có) và xem phản hồi JSON‑RPC. Kết quả cho `generate_password` sẽ là một chuỗi base64‑được‑đảo‑ngược như:

```
==dGM0ZTcwLTI0ZTUtNDJlZC05Y2I1LTk3OGJjODAxMDAwNw==
```

### 4.2 Kết nối tới Cursor (local stdio)

Trong dự án Cursor, tạo `.cursor/mcp.json` như trong phần 3.6, sau đó:

1. Mở **Settings → Tools & MCPs**.  
2. Tìm `utility_server`, bật **Enable**.  
3. Mở chat agents, gõ:  

```
Generate password
```

Cursor sẽ hiển thị dialog xin quyền; sau khi bạn đồng ý, nó sẽ gọi tool `generate_password` và trả về chuỗi password như trên.

### 4.3 Chuyển sang streamable‑HTTP và kết nối từ bên ngoài

Sửa `server.py` như phần 3.7, chạy:

```bash
python server.py   # now listens on 0.0.0.0:8000
```

Trong một máy khác (hoặc trong Docker), cấu hình MCP client:

```json
{
  "mcpServers": {
    "my_http_server": {
      "type": "http",
      "url": "http://<your-server-ip>:8000/mcp",
      "headers": {}
    }
  }
}
```

Bây giờ bất kỳ MCP client nào (Claude, Cursor, hoặc một script tự viết) có thể gửi yêu cầu JSON‑RPC tới `http://<your-server-ip>:8000/mcp` và nhận được kết quả như khi chạy qua stdio.

### 4.4 Sử dụng Composio MCP (không cần tự host)

Sau khi chạy lệnh cài đặt Composio (xem 3.8), trong Claude bạn có thể hỏi:

```
Tạo một báo cáo tài chính cho công ty AAPL bằng Google Sheets và gửi qua Gmail.
```

Claude sẽ tự động:

1. Gọi công cụ `google_sheets.read` để lấy bảng giá.  
2. Gọi `yahoo_finance.get_price` để lấy giá hiện tại.  
3. Gọi `google_docs.create_from_template` để điền báo cáo.  
4. Gọi `gmail.send_email` để gửi bản tóm tắt tới địa chỉ bạn cung cấp.  

Tất cả các bước này diễn ra qua một **unique URL** `https://connect.composio.dev/mcp` mà bạn không cần quản lý từng API key riêng.

## 5. Tổng kết

- **MCP** cung cấp một giao diện thống一 (JSON‑RPC) để AI agent gọi **tools**, đọc **resources** và sử dụng **prompts**, giúp loại bỏ việc phải viết mã “dán” riêng cho mỗi dịch vụ.  
- Xây dựng MCP server thật nhanh với **FastMCP** trong Python chỉ cần vài chục dòng code; các decorator `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` tự động đăng ký khả năng của bạn lên giao thức.  
- Kiểm thử local bằng **MCP Inspector** trước khi kết nối tới LLM giúp sớm phát hiện lỗi schema hoặc xử lý ngoại lệ.  
- Để triển khai thực tế, chuyển sang **streamable‑HTTP** cho phép server chạy như một dịch vụ web và được đặt đằng sau cân bằng tải hoặc các nền tảng serverless.  
- Khi muốn truy cập hàng nghìn công cụ mà không phải tự host, **Composio MCP** cung cấp một điểm cuối duy nhất với hơn 1.000 công cụ đã được xác thực sẵn dùng.  
- Những best practice về logging, validation, bảo mật, rate‑limit, versioning và health check là yếu tố then chốt để MCP server ổn định và an toàn trong môi trường production.  

Bằng cách nắm vững kiến thức trên, bạn có thể tạo ra các kết nối mạnh mẽ giữa AI agent và thế giới công cụ bên ngoài, mở ra khả năng xây dựng các agent tự động và thông minh hơn bao giờ hết. Chúc bạn học tập và triển khai thành công!