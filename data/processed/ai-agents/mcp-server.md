# Giới thiệu về Remote MCP Servers và cách khai thác chúng trong AI Engineering  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ có thể:  

- **Giảiyfik** khái niệm Model Context Protocol (MCP) và vai trò của MCP server trong việc mở rộng khả năng của các mô hình AI.  
- **Phân biệt** các loại MCP server theo mục đích (Development, Productivity, Database, …) và biết nơi tìm kiếm chúng.  
- **Mô tả** cách kết nối và sử dụng một MCP server từ các công cụ AI phổ biến như Claude, Cursor hoặc Codex.  
- **Đánh giá** lợi ích và注意事项 khi sử dụng remote MCP server trong quy trình làm việc thực tế.  

## 2. Tổng quan  

Model Context Protocol (MCP) là một chuẩn mở cho phép các **AI agent** (ví dụ: Claude, Cursor, Codex) trao đổi thông tin và thực hiện hành động qua các **server** cung cấp công cụ (tools) cụ thể. Thay vì phải embed mọi khả năng trực tiếp vào mô hình, các nhà phát triển có thể triển khai một **MCP server** nào đó – từ dịch vụ tài chính, hệ thống quản lý dự án, đến công cụ爬取 web – và exposes chúng qua MCP. Khi một AI agent kết nối tới server này,它能够以统一的格式调用这些工具，从而在不重新训练模型的情况下获得最新、领域特定的数据或功能。

Trang **mcpservers.org** (Remote MCP Servers) là một thư viện công khai tập hợp và phân loại các MCP server đã được triển khai veřejně. Trang cung cấp:

- **Danh sách featured** (được highlight) và **latest** (mới nhất).  
- **Phân loại theo chủ đề** như Development, Productivity, Database, Web Scraping, Cloud Service, v.v.  
- **Các chủ đề phổ biến** (Browser Automation, RAG, OpenAPI, …) giúp người dùng nhanh chóng tìm server phù hợp với nhu cầu cụ thể.  
- **FAQ** trả lời các câu hỏi cơ bản về MCP và cách sử dụng.  

Nhờ vậy, các nhà phát triển và nhà nghiên cứu AI có thể nhanh速发现并集成所需的功能，而无需自行构建和维护后端服务。  

## 3. Kiến thức cốt lõi  

### 3.1. MCP là gì?  

- **Model Context Protocol** định nghĩa một giao tiếp tiêu chuẩn (thường dựa trên JSON‑RPC qua stdio hoặc HTTP) giữa **AI client** và **MCP server**.  
- Server khai báo một tập hợp **tools** (công cụ) mà client có thể gọi, kèm theo mô tả tham số và kiểu trả về.  
- Client (ví dụ: Claude Desktop) đọc qua khai báo này, tạo ra các lệnh gọi phù hợp, và trả kết quả lại cho mô hình AI để nó tiếp tục suy luận hoặc thực hiện hành động.  

### 3.2. Phân loại MCP server trên mcpservers.org  

| Danh mục | Mô tả ngắn gọn | Ví dụ nổi bật (trang featured) |
|----------|----------------|--------------------------------|
| **Development** | Các server hỗ trợ công cụ phát triển, debugging, dokumentation, CI/CD. | Chrome DevOps MCP, Context7 MCP, Supabase MCP, Railway MCP |
| **Productivity** | Tích hợp với ứng dụng học việc, lập lịch, quản lý nhiệm vụ. | Atlassian MCP (Jira/Confluence), Cal.com MCP, NotebookLM MCP |
| **Database** | Truy vấn và quản lý cơ sở dữ liệu. | Supabase MCP (Postgres, Auth, Storage) |
| **Web Scraping** | Tự động hoá tương tác với trang web, lấy dữ liệu có cấu trúc. | Firecrawl MCP, Playwright MCP, Browserbase |
| **Cloud Service / Cloud Storage** | Làm việc với hạ tầng đám mây (functions, kv, object storage). | Cloudflare MCP, MiniMax MCP |
| **Finance** | Cung cấp dữ liệu thị trường, công cụ phân tích tài chính. | Alpha Vantage MCP, WickedAPI (DeFi) |
| **Search** | Truy vấn cơ sở kiến thức, pháp lý, công cụ recruitment. | Exa MCP, Fermat 360, Work Insiders |
| **Version Control** | Tương tác với Git, PR, issues. | GitHub MCP |
| **Communication** | Kết nối với nền tảng họp, ghi chú meeting. | Granola MCP |
| **Memory** | Lưu trữ và truy xuất ngữ cảnh dài hạn. | (khác nhỏ) |
| **Design** | Truy cập API phần mềm thiết kế. | Blender MCP |
| **Other** | Các server không thuộc nhóm trên. | – |

Mỗi mục trong danh sách trên mcpservers.org cung cấp:  

- **Tên server**  
- **Logo** (nếu có)  
- **Mô tả ngắn** về chức năng chính  
- **Link đến trang chi tiết** (thường bao gồm hướng dẫn cài đặt, ví dụ sử dụng, và licensing)  

### 3.3. Cách khai thác một MCP server  

1. **Tìm server phù hợp** – truy cập mcpservers.org, lọc theo danh mục hoặc từ khóa (ví dụ: “Jira”, “Postgres”, “web‑scraping”).  
2. **Xác định phương thức kết nối** – hầu hết các server cung cấp hai lựa chọn:  
   - **stdio** (chạy local process và trao đổi qua stdin/stdout) – phù hợp khi muốn chạy server trên máy phát triển.  
   - **HTTP/WebSocket** (endpoint công khai) – thích hợp cho việc triển khai trên cloud và cho nhiều client cùng kết nối.  
3. **Cài đặt MCP client** – hầu hết các IDE AI (Claude Desktop, Cursor, Codex) đã tích hợp sẵn khả năng kết nối tới MCP server qua cấu hình (file `mcp.json` hoặc biến môi trường).  
4. **Xác thực (nếu cần)** – một số server yêu cầu API key, token OAuth, hoặc chỉ cho phép kết nối từ địa chỉ IP đã đăng ký. Thông tin này được nêu rõ trong trang chi tiết của server.  
5. **Gọi công cụ** – sau khi kết nối thành công, client sẽ nhận danh sách `tools` từ server. Khi AI muốn thực hiện một hành động (ví dụ: “lấy 5 issue mới nhất từ dự án ABC”), nó sẽ gửi một request JSON‑RPC đến server với tên công cụ và tham số tương ứng. Server xử lý và trả về kết quả (thường là văn bản hoặc JSON) mà AI tiếp tục sử dụng trong luồng suy luận.  

### 3.4. Lưu ý khi sử dụng remote MCP server  

- **An toàn** – chỉ kết nối tới server từ nguồn đáng tin cậy; kiểm tra chính sách bảo mật và giới hạn tốc độ (rate limit).  
- **Chi phí** – một số server cung cấp gói free tier有限度， vượt qua mức đó sẽ phải trả phí.  
- **Phiên bản** – vì MCP đang phát triển, client và server cần sử dụng phiên bản giao thức tươngpatible (thường được ghi trong README).  
- **Độ trễ** – khi gọi qua internet, thời gian phản hồi có thể thêm vài chục đến vài trăm ms; cần cân nhắc trong các workflow thời gian thực.  

## 4. Ví dụ minh họa  

### Tình huống  
Bạn là nhà phát triển phần mềm và muốn cho AI agent (Claude) có thể **liệt kê các issue mở** từ một dự án Jira mà팀 của bạn đang quản lý, mà không cần rời khỏi môi trường coding.

### Các bước thực hiện (giả sử bạn đã có Atlassian MCP server – một trong các *official* server trên mcpservers.org)

1. **Xác định endpoint**  
   Trang chi tiết của *Atlassian MCP Server* cung cấp URL công khai: `https://mcp.atlassian.com` (giao thức HTTP).  
2. **Cấu hình Claude Desktop**  
   Thêm vào file `claude_desktop/mcp.json`:

   ```json
   {
     "servers": [
       {
         "name": "atlassian-jira",
         "url": "https://mcp.atlassian.com",
         "type": "http",
         "auth": {
           "apiKey": "YOUR_ATLASSIAN_API_KEY"
         }
       }
     ]
   }
   ```

   (API key được tạo từ tài khoản Atlassian và có quyền truy cập Jira Cloud.)  

3. **Khởi động Claude** – sau khi load cấu hình, Claude sẽ tự động kết nối tới server và lấy danh sách `tools`. Bạn sẽ thấy một công cụ tên `jira.list_open_issues` trong danh sách.  

4. **Yêu cầu từ AI**  
   Trong giao diện chat, bạn gõ:  

   ```
   Hãy liệt kê 5 issue mở hiện tại của dự án PROJ.
   ```

   Claude sẽ:  
   - Xác định tool `jira.list_open_issues` phù hợp.  
   - Gửi request JSON‑RPC tới `https://mcp.atlassian.com` với payload:  

     ```json
     {
       "tool": "jira.list_open_issues",
       "arguments": {
         "projectKey": "PROJ",
         "maxResults": 5
       }
     }
     ```

   - Nhận kết quả (thường là mảng JSON chứa key, tóm tắt, trạng thái, …) và trình bày dưới dạng danh sách易读.  

5. **Kết quả** (ví dụ giả định)  

   ```
   1. PROJ-123 – Linh tính xác thực sai – Mở  
   2. PROJ-124 – Giao diện nút Submit không phản hồi – Mở  
   3. PROJ-125 – Thiếu log khi lỗi kết nối DB – Mở  
   4. PROJ-126 – Cải thiện thời gian tải trang danh sách sản phẩm – Mở  
   5. PROJ-127 – Thêm kiểm tra quyền truy cập cho API /admin – Mở  
   ```

### Giải thích  
- Ví dụ trên **không** là mã code thực tế từ tài nguyên nguồn (trang mcpservers.org chỉ cung cấp danh sách và mô tả).  
- Tuy nhiên, nó minh hoá **quy trình chung** được mô tả trong FAQ và trong phần “How do I use an MCP server with Claude or Cursor?” –即: tìm server → cấu hình kết nối → AI agent gọi tool qua chuẩn MCP.  
- Nếu bạn muốn thử thực tế, hãy truy cập https://mcpservers.org/servers/atlassian-mcp-server, đọc phần “Usage” và sao chép cấu hình mẫu mà họ cung cấp.  

## 5. Tổng kết  

- **MCP** cung cấp một chuẩn mở để **AI agent** truy cập tới các **công cụ chuyên biệt** mà không cần embed chúng vào mô hình.  
- Trang **mcpservers.org** là một kho **remote MCP server** giàu chất lượng, được phân loại rõ ràng theo mục đích (Development, Productivity, Database, Web Scraping, Cloud Service, …) và constantly updated với featured và latest servers.  
- Việc sử dụng một MCP server bao gồm: tìm server phù hợp, xác định cách kết nối (stdio hoặc HTTP), cung cấp thông tin xác thực nếu cần, cấu hình trong client AI (Claude, Cursor, Codex) và sau đó cho AI gọi các công cụ qua JSON‑RPC.  
- Lợi ích rõ rệt: giảm thời gian phát triển, luôn có dữ liệu hoặc功能 mới nhất mà không cần retrain mô hình, và mở rộng khả năng của AI agent một cách modules.  
- Khi triển khai, cần lưu ý về **bảo mật**, **giới hạn mức sử dụng**, và **phiên bản giao thức** để tránh gián đoạn hoặc rò rỉ thông tin.  

Bằng cách nắm vững những khái niệm trên, bạn có thể bắt đầu tích hợp các MCP server vào dự án AI của mình và khai thác tối đa sức mạnh của các công cụ bên ngoài mà không phải rời khỏi môi trường làm việc của các trợ lý AI mình đang sử dụng.