# Remote MCP Servers – Truy cập dịch vụ qua mô hình MCP mà không cần cài đặt local

## 1. Mục tiêu học tập
Sau khi hoàn thành bài học, người học sẽ:
- Hiểu nguyên lý cơ bản của **Model Context Protocol (MCP)** và cách các máy chủ remote MCP hoạt động.
- Biết cách kết nối một AI assistant (Claude, Codex, Cursor, v.v.) với các dịch vụ bên thứ ba thông qua remote MCP server.
- Recognize một vài ví dụ phổ biến (Notion, Linear, Stripe, Ahrefs, v.v.) và lợi ích cụ thể khi sử dụng chúng trong quy trình làm việc của AI.
- Đánh giá khi nào nên sử dụng remote MCP thay vì cài đặt SDK hoặc API riêng.

## 2. Tổng quan
Model Context Protocol (MCP) là một giao thức mở chuẩn hoá cách AI assistants trao đổi ngữ cảnh (tools, data, prompts) với các dịch vụ bên ngoài. Thay vì phải cài đặt từng thư viện SDK hoặc quản lý API key từng dịch vụ, nhà phát triển có thể triển khai một **MCP server** remote (được lưu trữ trên internet) và AI assistant chỉ cần trỏ tới endpoint đó qua HTTP (thường là Streamable HTTP) với OAuth hoặc API‑key. Khi kết nối, assistant sẽ nhận được danh sách các **tools** (functions) mà server cung cấp và có thể gọi chúng như thể chúng là hàm nội bộ.

Trang **mcpservers.org** tổng hợp danh sách các remote MCP server “one‑click” từ các nhà cung cấp uy tín (Notion, Linear, Stripe, Ahrefs, Atlassian, v.v.) và cho phép AI assistant truy cập chúng ngay lập tức mà không cần cài đặt phần mềm phụ trợ locally. Các server này thường:
- Được offizielle hoặc cộng đồng duy trì.
- Hỗ trợ OAuth 2.0 (hoặc PKCE) để ủy quyền an toàn.
- Trả về danh sách tools có thể được gọi trực tiếp từ assistant.
- Hoạt động với bất kỳ MCP‑compatible client nào (Claude, Codex, Cursor, v.v.).

## 3. Kiến thức cốt lõi
### 3.1. Thành phần chính của một remote MCP server
| Thành phần | Mô tả |
|-----------|-------|
| **Endpoint** | URL `https://<domain>/mcp` (thường là Streamable HTTP) mà client kết nối tới. |
| **OAuth / API‑key** | Mekanism cấp phép để client truy cập; nhiều server cho phép “no‑auth” cho công cụ công khairead‑only. |
| **Tool schema** | Khi kết nối, server trả về JSON mô tả từng tool: tên, mô tả, tham số đầu vào, kiểu trả về. |
| **Execution** | Khi client gọi một tool, server thực thi logic phía_server (ví dụ: truy vấn API Notion, tạo issue Linear) và trả kết quả về cho client. |
| **Stateless / Stateful** | Hầu hết là stateless; một số lưu trữ session ngắn hạn (ví dụ: lưu trữ token OAuth). |

### 3.2. Luồng làm việc típico
1. **AI assistant** ( Claude, Codex, … ) khởi tạo kết nối tới `https://example.com/mcp` với OAuth token hoặc API‑key đã được cấu hình.
2. Assistant gửi yêu cầu `tools/list` để nhận danh sách các công cụ khả dụng.
3. Người dùng (hoặc agent) mô tả nhu cầu bằng ngôn ngữ tự nhiên; assistant suy ra quale tool cần gọi và truyền tham số phù hợp.
4. Server thực thi tool (gọi API bên thứBA, truy vấn DB, v.v.) và trả về kết quả (thường là JSON hoặc văn bản).
5. Assistant tích hợp kết quả vào cuộc hội thoại hoặc thực hiện hành động tiếp theo (ví dụ: ghi vào Notion, cập nhật Linear issue).

### 3.3. Lợi ích chính
- **Không cần cài đặt local** – giảm摩擦 cho nhà phát triển và người dùng cuối.
- **Quản lý tập trung** – cập nhật tool chỉ cần thực hiện trên server; tất cả client sẽ nhận được phiên bản mới ngay lập tức.
- **Bảo mật** – OAuth cho phép granular scopes; không cần lưu trữ API key trên máy local.
- **Đa nền tảng** – Hoạt động với bất kỳ MCP‑compatible client nào, không phụ thuộc vào ngôn ngữ hoặc framework cụ thể.
- **Mở rộng dễ dàng** – Nhiều nhà cung cấp đã publicar официаль remote MCP server; chỉ cần thêm endpoint mới vào danh sách cấu hình của assistant.

## 4. Ví dụ minh họa
### 4.1. Kết nối với Notion MCP server
Giả sử chúng ta có một Claude Desktop đã được cấu hình để sử dụng remote MCP server của Notion (endpoint: `https://mcpservers.org/servers/notion-mcp-server`).  

**Bước 1 – Xác thực**  
Trong cấu hình Claude, chúng ta thêm OAuth client ID/secret được cung cấp bởi Notion MCP server (hoặc sử dụng “no‑auth” nếu server cho phép công khai đọc).  

**Bước 2 – Lấy danh sách tools**  
Claude gửi request:  
```json
{ "type": "tools/list", "id": 1 }
```
Phản hồi (rút gọn):
```json
{
  "type": "tools/list",
  "id": 1,
  "result": {
    "tools": [
      { "name": "search_pages", "description": "Tìm kiếm trang Notion theo từ khóa", "inputSchema": { ... } },
      { "name": "create_page", "description": "Tạo một trang mới trong workspace", "inputSchema": { ... } },
      { "name": "update_page", "description": "Cập nhật nội dung trang hiện có", "inputSchema": { ... } }
    ]
  }
}
```

**Bước 3 – Gọi tool**  
Người dùng nói: “Tạo một trang mới có tiêu đề ‘Kế hoạch sprint 23’ và nội dung là danh sách công việc.” Claude xác định tool `create_page`, xây dựng payload:
```json
{
  "type": "tools/call",
  "id": 2,
  "name": "create_page",
  "arguments": {
    "title": "Kế hoạch sprint 23",
    "content": "- Định nghĩa mục tiêu\n- Phân công nhiệm vụ\n- Đánh giá rủi ro"
  }
}
```
Server Notion thực hiện lệnh tạo trang qua API Notion và trả về ID của trang mới.

**Bước 4 – Nhận kết quả**  
Claude nhận phản hồi:
```json
{
  "type": "tools/call",
  "id": 2,
  "result": { "pageId": "abc123", "url": "https://www.notion.so/abc123" }
}
```
Sau đó Claude có thể thông báo cho người dùng: “Đã tạo trang Kế hoạch sprint 23 tại https://www.notion.so/abc123”.

### 4.2. Sử dụng Linear MCP server để quản lý issue
Tương tự, endpoint `https://mcpservers.org/servers/linear-mcp` cung cấp tools như `list_issues`, `create_issue`, `update_issue`. Khi một agente cần báo lỗi, nó chỉ cần gọi:
```json
{
  "type": "tools/call",
  "name": "create_issue",
  "arguments": {
    "title": "Lỗi hiển thị trên màn hình điện thoại",
    "description": "Các nút không phản hồi khi thiết bị ở chế độ chế độ màn hình tối",
    "teamId": "TEAM_123",
    "priority": "high"
  }
}
```
Linear MCP server sẽ tạo issue trong workspace Linear và trả về URLissue, cho phép agente theo dõi hoặc cập nhật sau này.

### 4.3. Truy cập dữ liệu tài chính qua Alpha Vantage MCP server
Endpoint `https://mcp.alphavantage.co` cho phép lấy giá chứng khoán realtime. Một ví dụ gọi:
```json
{
  "type": "tools/call",
  "name": "get_quote",
  "arguments": { "symbol": "AAPL" }
}
```
Trả về JSON chứa `price`, `volume`, `timestamp`, v.v., cho agent sử dụng trong quyết định giao dịch hoặc báo cáo.

### 4.4. Kết hợp nhiều server trong một workflow
Một agente có thể:
1. Tìm kiếm xu hướng thị trường qua **Alpha Vantage** (stock quote).
2. Tạoissue trên **Linear** để theo dõi cơ hội đầu tư.
3. Ghi chú chiến lược vào **Notion** để team tham khảo.
Tất cả những thao tác này đều thực hiện qua các remote MCP server khác nhau mà không cần cài đặt SDK riêng cho mỗi dịch vụ.

## 5. Tổng kết
- Remote MCP server cho phép AI assistants truy cập các dịch vụ bên thứBA qua một giao thức thống一 (MCP) mà không cần cài đặt thư viện hoặc quản lý API key từng dịch vụ một cách thủ công.
- Các server được lưu trữ trên internet, thường bảo vệ bằng OAuth và cung cấp danh sách các tools rõ ràng, chi tiết.
- Một loạt các dịch vụ phổ biến (Notion, Linear, Stripe, Ahrefs, Atlassian, v.v.) đã có官方 remote MCP server trên `mcpservers.org`, giúp các nhà phát triển và người dùng nhanh chóng tích hợp chúng vào quy trình làm việc của AI.
- Khi xây dựng quy trình AI, người ta nên ưu tiên sử dụng remote MCP khi:
  - Cần truy cập nhanh vào một dịch vụ đã có server công khai.
  - Muốn giảmภาระ quản lý phụ thuộc và bảo mật API key.
  - Cần tương tác với nhiều dịch vụ khác nhau trong một đơn vị làm việc đồng thời.
- Trong trường hợp cần tính năng đặc thù hoặc không có server remote disponibile, vẫn có thể tự triển khai một MCP server riêng hoặc sử dụng SDK местная. 

Với hiểu biết này, bạn có thể bắt đầu kết nối các AI assistant như Claude, Codex, Cursor với hàng chục remote MCP server có sẵn và mở rộng khả năng tự động hóa, truy xuất dữ liệu và quản lý công việc mà không cần viết mã kết nối phức tạp.