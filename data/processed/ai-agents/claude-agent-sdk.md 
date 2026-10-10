# Getting Started with the Claude Agent SDK

## 1. Mục tiêu học tập

- Hiểu Claude Agent SDK là gì và cách nó mở rộng khả năng của Claude Code.  
- Cài đặt Claude Code CLI và Claude Agent SDK trên máy local.  
- Xây dựng một ứng dụng CLI đa công cụ (TrendSmith) bằng Python, sử dụng SDK để lên kế hoạch, thực thi và xác thực các công việc.  
- Kiểm tra ứng dụng bằng các lệnh `/trend` và `/scan`, xem báo cáo tự động lưu và tóm tắt tài nguyên sử dụng.  
- Đánh giá lợi ích của SDK trong việc tự động hoá quy trình phát triển và tạo agentic CLI có thể tái sử dụng.

## 2. Tổng quan

Claude Agent SDK cho phép nhà phát triển biến quy trình “plan → build → run” của Claude Code thành các ứng dụng có thể lập trình được. Thay vì ghép nối nhiều script, công cụ và prompt một cách thủ công, SDK cung cấp một cấu trúc có trạng thái, mở rộng và tích hợp sâu với môi trường local (hệ thống tệp, công cụ tìm kiếm web, v.v.). Bài học này hướng dẫn bạn cài đặt SDK, tạo một ứng dụng theo dõi xu hướng thị trường (TrendSmith) và thử nghiệm nó qua giao diện dòng lệnh.

## 3. Kiến thức cốt lõi

### 3.1 Claude Agent SDK là gì?

- SDK được xây dựng trên nền tảng **Claude Code** và được cung cấp bởi Anthropic.  
- Nó cho phép kết nối Claude với các công cụ locais (WebSearch, WebFetch, hệ thống tệp…) và orchestrates các workflow phức tạp như nghiên cứu, tạo mã, tự động hoá triển khai.  
- Thành phần chính:  
  - `ClaudeAgentOptions` – cấu hình mô hình, prompt hệ thống, danh sách công cụ cho phép.  
  - `ClaudeSDKClient` – client không đồng bộ chịu trách nhiệm gửi truy vấn và nhận luồng phản hồi.  
  - Các loại block trong phản hồi: `AssistantMessage` (văn bản), `ToolUseBlock` (sử dụng công cụ), `ToolResultBlock` (kết quả công cụ), `ResultMessage` (thống kê token, chi phí).  

### 3.2 Yêu cầu trước khi cài đặt

| Yêu cầu | Chi tiết |
|---------|----------|
| Python | >= 3.10 |
| Node.js | >= 18 (để cài Claude Code CLI qua npm) |
| Claude API Key | Hoặc tài khoản Anthropic để xác thực |

### 3.3 Cài đặt Claude Code CLI

- Trên Windows (PowerShell):  

  ```powershell
  irm https://claude.ai/install.ps1 | iex
  ```

- Thêm thư mục `C:\Users\<user>\.local\bin` vào biến môi trường PATH, khởi động lại PowerShell và kiểm tra:

  ```powershell
  claude --version
  ```

- Trên các nền tảng khác, có thể dùng npm:

  ```bash
  npm i -g @anthropic-ai/claude-code
  ```

Sau khi cài, chạy `claude` trong terminal để đăng nhập.

### 3.4 Cài đặt Claude Agent SDK (Python)

```bash
pip install claude-agent-sdk
```

Nếu gặp lỗi `CLINotFoundError`, kiểm tra lại việc cài Claude Code CLI và biến PATH.

### 3.5 Xây dựng ứng dụng đa công cụ – TrendSmith

#### 3.5.1 Import và cài đặt cơ bản

```python
import asyncio
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
)

HELP = """Commands:
/trend   Quick multi-source scan (auto-saves markdown)
/scan    Short one-page scan
/help /exit     Help / Quit
"""

MODEL = os.getenv("CLAUDE_MODEL", "sonnet")  # e.g. "sonnet-4.5"
GRAY = "\033[90m"
RESET = "\033[0m"
```

#### 3.5.2 Prompt hệ thống và vị trí lưu báo cáo

```python
SYS = """You are TrendSmith, a fast, concise trend researcher.
- Finish quickly (~20 s).
- For /trend: ≤1 WebSearch + ≤2 WebFetch from distinct domains.
- For /scan: ≤1 WebFetch only.
Return for /trend:
 TL;DR (1 line)
 3-5 Signals (short bullets)
 Key Players, Risks, 30/90-day Watchlist
 Sources (markdown: **Title** -- URL)
Return for /scan: 5 bullets + TL;DR + Sources.
After finishing /trend, the client will auto-save your full brief.
"""

BASE = Path(__file__).parent
REPORTS = BASE / "reports"
```

#### 3.5.3 Hàm tiện ích để lưu file an toàn

```python
def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M")

def _sanitize(s: str):
    return re.sub(r"[^\w\-.]+", "_", s).strip("_") or "untitled"

def _ensure_dir(p: Path):
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def _safe_write(path: Path, text: str) -> Path:
    """Write text to path; if directory/permission fails, fall back to ~/TrendSmith/reports."""
    try:
        _ensure_dir(path.parent)
        path.write_text(text, encoding="utf-8")
        return path
    except Exception:
        home_reports = Path.home() / "TrendSmith" / "reports"
        _ensure_dir(home_reports)
        fb = home_reports / path.name
        fb.write_text(text, encoding="utf-8")
        return fb

def save_report(topic: str, text: str) -> Path:
    filename = f"{_sanitize(topic)}_{_ts()}.md"
    target = REPORTS / filename
    return _safe_write(target, text.strip() + "\n")
```

#### 3.5.4 Theo dõi trạng thái mỗi lần chạy

```python
class State:
    def __init__(self):
        self.brief = ""
        self.model_raw = None
        self.usage = {}
        self.cost = None
        self.last_cmd = None
        self.last_topic = None
        self.tools = {}
        self.t0 = 0.0
        self.t1 = 0.0

    def reset(self):
        self.brief = ""
        self.model_raw = None
        self.usage = {}
        self.cost = None
        self.tools = {}
        self.t0 = time.perf_counter()
        self.t1 = 0.0

def friendly_model(name: str | None) -> str:
    if not name:
        return MODEL
    n = (name or "").lower()
    if "sonnet-4-5" in n or "sonnet_4_5" in n:
        return "Claude 4.5 Sonnet"
    if "sonnet" in n:
        return "Claude Sonnet"
    if "haiku" in n:
        return "Claude Haiku"
    if "opus" in n:
        return "Claude Opus"
    return name or "Unknown"
```

#### 3.5.5 Hiển thị tóm tắt việc sử dụng

```python
def usage_footer(st: State, opts_model: str):
    st.t1 = st.t1 or time.perf_counter()
    dur = st.t1 - st.t0
    usage = st.usage or {}
    it = usage.get("input_tokens")
    ot = usage.get("output_tokens")
    total = usage.get("total_tokens")
    if total is None and (it is not None or ot is not None):
        total = (it or 0) + (ot or 0)
    tools_used = ", ".join(f"{k}×{v}" for k, v in st.tools.items()) or "--"
    model_label = friendly_model(st.model_raw or opts_model)

    box = [
        "┌─ Run Summary ─────────────────────────────────────────────",
        f"│ Model: {model_label}",
        f"│ Tokens: {total if total is not None else '?'}"
        + (f" (in={it if it is not None else '?'} | out={ot if ot is not None else '?'})"
            if (it is not None or ot is not None) else ""),
        f"│ Tools: {tools_used}",
        f"│ Duration: {dur:.1f}s",
        "└───────────────────────────────────────────────────────────",
    ]
    print(GRAY + "\n".join(box) + RESET, file=sys.stderr)
```

#### 3.5.6 Vòng lặp chính (REPL)

```python
async def main():
    """Setup → REPL → parse → query/stream → auto-save → summary."""
    st = State()
    _ensure_dir(REPORTS)

    opts = ClaudeAgentOptions(
        model=MODEL,
        system_prompt=SYS,
        allowed_tools=["WebFetch", "WebSearch"],
    )

    print("📈 TrendSmith \n\n" + HELP)

    async with ClaudeSDKClient(options=opts) as client:
        while True:
            # Read input
            try:
                user = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break

            if not user:
                continue
            low = user.lower()

            # Basic commands
            if low in {"/exit", "exit", "quit"}:
                print("Bye!")
                break
            if low in {"/help", "help"}:
                print(HELP)
                continue

            # Parse into a prompt
            if low.startswith("/trend "):
                topic = user.split(" ", 1)[1].strip().strip('"')
                if not topic:
                    print('e.g. /trend "AI chip startups"')
                    continue
                st.last_cmd, st.last_topic = "trend", topic
                prompt = f"Run a fast trend scan for '{topic}' following the output spec."
            elif low.startswith("/scan "):
                q = user.split(" ", 1)[1].strip()
                if not q:
                    print('e.g. /scan "AI hardware news"')
                    continue
                st.last_cmd, st.last_topic = "scan", q
                prompt = f"Quick scan for '{q}' in under 10s (≤1 WebFetch). Return 5 bullets + TL;DR + sources."
            else:
                st.last_cmd, st.last_topic = "free", None
                prompt = user

            # Execute request and stream results
            st.reset()
            print(f"{GRAY}▶ Working...{RESET}")
            try:
                await client.query(prompt)
            except Exception as e:
                print(f"{GRAY}❌ Query error: {e}{RESET}")
                continue

            try:
                async for m in client.receive_response():
                    if isinstance(m, AssistantMessage):
                        st.model_raw = st.model_raw or m.model
                        for b in m.content:
                            if isinstance(b, TextBlock):
                                st.brief += b.text or ""
                                print(b.text or "", end="")
                            elif isinstance(b, ToolUseBlock):
                                name = b.name or "Tool"
                                st.tools[name] = st.tools.get(name, 0) + 1
                                print(f"{GRAY}\n🛠 Tool: {name}{RESET}")
                            elif isinstance(b, ToolResultBlock):
                                pass  # quiet tool payloads
                    elif isinstance(m, ResultMessage):
                        st.usage = m.usage or {}
                        st.cost = m.total_cost_usd
            except Exception as e:
                print(f"{GRAY}\n⚠ Stream error: {e}{RESET}")

            # Auto-save trend briefs and show the summary
            if st.last_cmd == "trend" and st.brief.strip():
                try:
                    saved_path = save_report(st.last_topic or "trend", st.brief)
                    print(f"\n{GRAY}✅ Auto-saved → {saved_path}{RESET}")
                except Exception as e:
                    print(f"{GRAY}⚠ Save error: {e}{RESET}")

            st.t1 = time.perf_counter()
            usage_footer(st, opts.model)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.6 Kiểm tra ứng dụng TrendSmith

- Chạy script:  

  ```bash
  python .\trend_smith.py
  ```

- Lệnh `/trend "<topic>"` thực hiện quét đa nguồn, tự động lưu báo cáo Markdown vào thư mục `reports/`.  
- Lệnh `/scan "<query>"` thực hiện quét ngắn (≤1 WebFetch) và in kết quả ra terminal.  
- Các lệnh `/help` và `/exit` tương ứng hiển thị trợ giúp và thoát.  

Trong ví dụ bài viết, lệnh  

```
/trend "AI chip startups"
```  

đã sử dụng các công cụ WebSearch và WebFetch để thu thập thông tin từ nhiều trang web, tạo ra báo cáo chi tiết, tự động lưu vào file như `AI_chip_startups_20251128_1430.md` và hiển thị tóm tắt tài nguyên (token, chi phí khoảng $0.136, thời gian thực thi).  

Lệnh  

```
/scan Code CLI tools
```  

sử dụng một lần WebFetch để tạo bản tóm tắt ngắn gồm 5 bullet points, TL;DR và danh sách nguồn.

## 4. Tổng kết

- Claude Agent SDK biến Claude Code thành một nền tảng lập trình agent có thể tích hợp công cụ local và lưu trạng thái.  
- Quy trình cài đặt bao gồm Claude Code CLI (Node.js) và gói Python `claude-agent-sdk`.  
- Ứng dụng mẫu TrendSmith minh họa cách định nghĩa prompt hệ thống, đăng ký công cụ (`WebFetch`, `WebSearch`), xử lý luồng phản hồiStream và tự động lưu kết quả.  
- Thông qua các lệnh `/trend` và `/scan`, bạn có thể trải nghiệm quy trình “plan → act → verify” trong một CLI giao tiếp tự nhiên.  
- SDK mang lại ổn định, khả năng tái tạo và giảm thiểu mã bộ ghép (glue code), phù hợp để tự động hoá các tác vụ phát triển, phân tích hoặc triển khai, đồng thời cho phép mở rộng bằng cách viết các agent mới dựa trên cùng SDK.