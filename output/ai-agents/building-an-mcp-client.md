# Xây dựng MCP Client tùy chỉnh bằng Langchain và Gemini  

## 1. Mục tiêu học tập  

- Hiểu mô hình **Model Context Protocol (MCP)** và quy trình làm việc của client.  
- Xây dựng một MCP client kết nối tới server local qua **STDIO** và thực hiện các thao tác qua công cụ (tool).  
- Tích hợp MCP client với máy chủ **SSE** (Server‑Sent Events) của Composio để tương tác với dịch vụ ngoài như Slack.  
- Sử dụng **Langchain**, **LangGraph** và **Gemini** để tạo agent có khả năng gọi tool và duy trì cuộc trò chuyện.  

## 2. Tổng quan  

MCP là một giao thức chuẩn hoá phát triển bởi Anthropic cho phép mô hình ngôn ngữ lớn (LLM) truy cập công cụ, tài nguyên, cơ sở dữ liệu và dịch vụ ngoài qua kiến trúc client‑server. Khi muốn kết nối với công cụ nội bộ hoặc dịch vụ không được hỗ trợ sẵn, việc phát triển **MCP client tùy chỉnh** cho phép:  

- Kết nối tới công cụ nội bộ hoặc tùy chỉnh.  
- Cung cấp dữ liệu thời gian thực cho LLM để tăng độ chính xác câu trả lời.  
- Giữ tính trung lập với nhà cung cấp, dễ dàng thay đổi hoặc mở rộng tích hợp sau này.  

Bài học này sẽ hướng dẫn bạn tạo hai loại client:  

1. **STDIO client** – kết nối tới một server local (ví dụ: server chạy lệnh terminal).  
2. **SSE client** – kết nối tới một server hosted trên Composio (ví dụ: Slack MCP server).  

## 3. Kiến thức cốt lõi  

### 3.1. MCP và vòng đời client  

MCP hoạt động theo mô hình **client‑server**. Vòng đời của một MCP client bao gồm các bước:  

1. **Connect** – client gửi phiên bản giao thức và khả năng của mình tới server.  
2. **Handshake** – server phản hồi, thiết lập kết nối.  
3. **Exchange** – client và server trao đổi tin nhắn (request‑response hoặc one‑way notification).  
4. **Terminate** – kết nối bị chius khi có lỗi, mất mạng hoặc một bên đóng kết nối.  

### 3.2. Tại sao cần MCP client tùy chỉnh?  

- **Công cụ nội bộ**: Các công cụ riêng tư hoặc legacy không có trong danh sách MCP server công khai.  
- **Dữ liệu thực thời**: Cung cấp context mới nhất cho LLM khi làm việc với hệ thống nội bộ.  
- **Tránh vendor lock‑in**: Dễ dàng chuyển đổi giữa nhiều server mà không thay đổi mã client.  

### 3.3. Thành phần技术栈  

| Thành phần | Vai trò |  
|------------|---------|  
| **StdioServerParameters** | Định nghĩa lệnh và tham số để khởi động MCP server qua stdio. |  
| **ClientSession** (từ `mcp`) | Quản lý kết nối stdio hoặc SSE với server. |  
| **load_mcp_tools** (từ `langchain_mcp_adapters`) | Tải danh sách công cụ có sẵn từ MCP server và chuyển đổi sang định dạng tool của Langchain. |  
| **create_react_agent** (từ `langgraph.prebuilt`) | Tạo agent typu ReAct kết hợp LLM và danh sách tool. |  
| **ChatGoogleGenerativeAI** | LLM Gemini (phiên bản 1.5‑pro) cung cấp khả năng suy luận và gọi tool. |  
| **sse_client** (từ `mcp.client.sse`) | Thiết lập kết nối Server‑Sent Events tới MCP server hosted. |  
| **CustomEncoder** | Encoder JSON tùy chỉnh để serialize các đối tượng có thuộc tính `content` (được dùng bởi các đối tượng trả về từ tool). |  

### 3.4. Quy trình mã hóa client  

1. **Đọc biến môi trường** (`GOOGLE_API_KEY` hoặc `GEMINI_API_KEY`) để khởi tạo LLM.  
2. **Xác nhận đối số dòng lệnh** – đường dẫn tới script server (STDIO) hoặc URL server (SSE).  
3. **Khởi tạo kết nối** (`stdio_client` hoặc `sse_client`) và bọc trong `ClientSession`.  
4. **Tải công cụ** qua `load_mcp_tools`.  
5. **Tạo agent** bằng `create_react_agent`.  
6. **Vòng lặp trò chuyện**: nhận đầu vào từ terminal, gửi tới agent, định dạng và in phản hồi.  

## 4. Ví dụ minh họa  

### 4.1. Cấu trúc dự án  

```
mcp/
├─ servers/          # chứa mã MCP server
│   └─ terminal_server.py
├─ clients/          # chứa mã MCP client
│   ├─ client.py        # STDIO client
│   └─ sse_client.py    # SSE client
└─ workspace/        # thư mục lưu kết quả hoạt động của terminal
```

### 4.2. STDIO client – `client.py`  

```python
#!/usr/bin/env python
"""
MCP client that connects to an MCP server via stdio, loads tools,
and runs a chat loop using Google Gemini LLM.
"""

import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Optional, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()  # Load GOOGLE_API_KEY from .env

# Custom JSON encoder for objects with 'content' attribute
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)

# Instantiate Gemini LLM (deterministic, retry)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Require server script path as command‑line argument
if len(sys.argv) < 2:
    print("Usage: python client.py <path_to_server_script>")
    sys.exit(1)
server_script = sys.argv[1]

# Configure MCP server startup parameters
server_params = StdioServerParameters(
    command="python" if server_script.endswith(".py") else "node",
    args=[server_script],
)

# Global holder for the active MCP session (used by tool adapter)
mcp_client = None

# Main async function: connect, load tools, create agent, run chat loop
async def run_agent():
    global mcp_client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_client = type("MCPClientHolder", (), {"session": session})()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            print("MCP Client Started! Type 'quit' to exit.")
            while True:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                # Send user query to agent and print formatted response
                response = await agent.ainvoke({"messages": query})
                try:
                    formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                except Exception:
                    formatted = str(response)
                print("\nResponse:")
                print(formatted)
    return

# Entry point
if __name__ == "__main__":
    asyncio.run(run_agent())
```

**Giải thích:**  
- Kết nối tới server qua `stdio_client`.  
- Tải công cụ từ server, tạo agent ReAct với Gemini.  
- Vòng lặp nhập lệnh, in phản hồi dưới dạng JSON đẹp (nhờ `CustomEncoder`).  

### 4.3. MCP server terminal – `servers/terminal_server.py`  

```python
# imports
import os
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("terminal")

DEFAULT_WORKSPACE = os.path.join(os.getcwd(), "workspace")

# define tool - llm will create code/ command and pass to this fn
@mcp.tool()
async def run_server_command(command: str) -> str:
    """
    Run a terminal command in workspace.
    Args:
        command: The shell command to run on windows

    Returns:
        The command output or an error message.
    """
    # try catch to handle exception
    try:
        result = subprocess.run(command, cwd=DEFAULT_WORKSPACE, shell=True, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Cách chạy:**  

```bash
# từ thư mục gốc mcp
python "clients/client.py" "servers/terminal_server.py"
```

Sau khi thấy prompt `Query:` bạn có thể thực hiện các lệnh terminal như:  

```
Create a folder called test, and inside it, create a file named file.txt. In the file, write "MCP Building Is Fun"
```

Client sẽ gửi yêu cầu tới server, server thực thi lệnh trong thư mục `workspace`, và trả về kết quả (thông thường là chuỗi rỗng nếu thành công). Kiểm tra thư mục `workspace` để xác nhận file đã được tạo.  

Lệnh `Delete the test folder.` sẽ được nhớ nhờ lịch sử cuộc trò chuyện và xóa thư mục vừa tạo.  

### 4.4. SSE client – `sse_client.py`  

```python
#!/usr/bin/env python
"""
client_sse.py

MCP client that connects to an SSE-based MCP server, loads tools,
and runs a chat loop using Google Gemini LLM.
"""

import os
import sys
import json
import warnings
import logging
import asyncio
from typing import Optional, List

from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()  # Load GEMINI_API_KEY from .env

# Suppress specific warnings
warnings.filterwarnings('ignore')

# Custom JSON encoder for objects with 'content' attribute
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)

# Instantiate Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Require MCP server URL as command‑line argument
if len(sys.argv) < 2:
    print("Usage: python sse_client.py <mcp_server_url>")
    sys.exit(1)
server_url = sys.argv[1]

# Global holder for the active MCP session (used by tool adapter)
mcp_client = None

# Main async function: connect, load tools, create agent, run chat loop
async def run_agent():
    global mcp_client
    async with sse_client(url=server_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            mcp_client = type("MCPClientHolder", (), {"session": session})()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            print("MCP Client Started! Type 'quit' to exit.")
            while True:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                # Send user query to agent and print formatted response
                response = await agent.ainvoke({"messages": query})
                try:
                    formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                except Exception:
                    formatted = str(response)
                print("\nResponse:")
                print(formatted)
    return

# Entry point
if __name__ == "__main__":
    asyncio.run(run_agent())
```

**Cách kết nối tới Composio SSE server (ví dụ Slack):**  

1. Truy cập [Composio MCP Directory](https://mcp.composio.dev/), tìm **Slack**, tạo URL riêng và sao chép.  
2. Đảm bảo  môi trường ảo đã được kích hoạt và file `.env` chứa `GEMINI_API_KEY`.  
3. Chạy:  

```bash
python "clients/sse_client.py" "<your‑composio‑slack‑sse‑url>"
```

Sau khi thấy prompt `Query:` bạn có thể gửi tin nhắn tới Slack, ví dụ:  

```
Query: send a message 'hii' to social channel
```

Client sẽ gọi tool `send_message` (hoặc tương đương) của Slack MCP server, tin nhắn sẽ xuất hiện trong kênh đã chỉ định.  

## 5. Tổng kết  

- MCP cung cấp một giao thức thống nhất để LLM tương tác với công cụ và dịch vụ qua mô hình client‑server.  
- Xây dựng **MCP client tùy chỉnh** cho phép kết nối tới công cụ nội bộ, dịch vụ không được hỗ trợ sẵn và duy trì sự trung lập với nhà cung cấp.  
-Trong bài học chúng ta đã:  
  - Thiết lập môi trường và cấu trúc dự án.  
  - Viết client STDIO kết nối tới server terminal và thực hiện lệnh shell.  
  - Viết client SSE kết nối tới máy chủ hosted (Composio‑Slack) và gửi tin nhắn.  
  - Sử dụng `langchain_mcp_adapters`, `langgraph.prebuilt.create_react_agent` và `ChatGoogleGenerativeAI` để tạo agent có khả năng gọi tool và duy trì cuộc trò chuyện.  

Khi áp dụng vào thực tế, cần lưu ý về **bảo mật** (quyền truy cập API key), **xử lý lỗi** (timeout, mạng đứt) và **quyền công cụ** (RBAC) nếu triển khai trong môi trường doanh nghiệp. Các nền tảng như **MCP gateway** của Composio cung cấp những tính năng này để mở rộng khả năng sử dụng MCP trong quy mô lớn.  

Bạn đã có thể tự siebie phát triển các MCP client phù hợp với nhu cầu tích hợp cá nhân hoặc tổ chức. Hãy thử mở rộng với các công cụ khác (GitHub, Firebase, cơ sở dữ liệu) hoặc triển khai kết hợp nhiều server trong một hệ thống phức tạp. Chúc bạn thành công!