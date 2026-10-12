# Giới thiệu về Model Context Protocol (MCP)

## 1. Mục tiêu học tập

Sau bài học này, bạn sẽ có thể:
- Giải thích được MCP là gì và vai trò của nó trong hệ sinh thái AI.
- Liệt kê những khả năng mà MCP mở ra cho các ứng dụng AI.
- Hiểu tại sao MCP quan trọng đối với nhà phát triển, ứng dụng AI và người dùng cuối.
- Nêu tên một số công cụ và nền tảng phổ biến đã hỗ trợ MCP.
- Bắt đầu tìm hiểu cách xây dựng máy chủ (server), khách hàng (client) hoặc ứng dụng MCP.

## 2. Tổng quan

Model Context Protocol (MCP) là một chuẩn mã nguồn mở để kết nối các ứng dụng AI (ví dụ: Claude, ChatGPT) với các hệ thống bên ngoài như nguồn dữ liệu, công cụ và quy trình làm việc. MCP hoạt động như một “cổng USB‑C” cho AI: nó cung cấp một giao diện thống nhất, giúp các ứng dụng AI truy cập thông tin và thực hiện tác vụ mà không cần phải tích hợp từng kết nối một cách riêng lẻ.

## 3. Kiến thức cốt lõi

### 3.1 MCP là gì?

- Chuẩn mở, không thuộc về bất kỳ công ty nào.
- Định nghĩa cách các ứng dụng AI (client) trao đổi dữ liệu và lệnh với các máy chủ (server) cung cấp tài nguyên bên ngoài.
- Cho phép AI truy cập nguồn dữ liệu (file local, database), công cụ (công cụ tìm kiếm, máy tính) và quy trình (prompt chuyên biệt).

### 3.2 Những gì MCP có thểEnable

| Trường hợp sử dụng | Mô tả |
|--------------------|-------|
| **Trợ lý AI cá nhân** | Truy cập Google Calendar, Notion để lên lịch, ghi chú, trả lời câu hỏi dựa trên dữ liệu cá nhân. |
| **Sinh mã từ thiết kế** | Claude Code có thể tạo toàn bộ ứng dụng web từ một thiết kế Figma. |
| **Chatbot doanh nghiệp** | Kết nối với nhiều cơ sở dữ liệu wewn组织, cho phép người dùng phân tích dữ liệu qua giao diện trò chuyện. |
| **Thiết kế và in 3D** | Mô hình AI tạo ra mô hình 3D trên Blender và gửi trực tiếp tới máy in 3D để sản xuất. |

### 3.3 Tại sao MCP quan trọng?

- **Cho nhà phát triển**: Giảm thời gian và phức tạp khi xây dựng hoặc tích hợp ứng dụng AI vì không cần viết adapter riêng cho mỗi nguồn dữ liệu/công cụ.
- **Cho ứng dụng AI hoặc аген**: Mở rộng khả năng bằng cách kết nối với một hệ sinh thái phong phú của dữ liệu, công cụ và ứng dụng, từ đó cải thiện trải nghiệm người dùng cuối.
- **Cho người dùng cuối**: Nhận được các trợ lý AI mạnh mẽ hơn, có thể thực hiện hành động thay người dùng khi cần (ví dụ: đặt lịch, truy xuất tài liệu).

### 3.4 Hỗ trợ hệ sinh thái rộng

MCP được triển khai trên nhiều khách hàng và máy chủ phổ biến:
- **Trợ lý AI**: Claude, ChatGPT.
- **Công cụ phát triển**: Visual Studio Code (qua Copilot), Cursor, MCPJam.
- **Các nền tảng khác**: Nhiều dự án cộng đồng cũng đã tích hợp MCP, cho phép “xây dựng một lần, kết nối everywhere”.

### 3.5 Bắt đầu xây dựng

- **Xây dựng máy chủ (server)**: Tạo MCP server để công khai dữ liệu và công cụ của bạn.  
  → Xem hướng dẫn: *Build servers* (tại `/docs/2026-07-28/develop/build-server`).
- **Xây dựng khách hàng (client)**: Phát triển ứng dụng kết nối tới các MCP server.  
  → Xem hướng dẫn: *Build clients* (tại `/docs/2026-07-28/develop/build-client`).
- **Xây dựng MCP Apps**: Tạo ứng dụng tương tác chạy bên trong khách hàng AI.  
  → Xem hướng dẫn: *Build MCP Apps* (tại `/extensions/apps/overview`).

### 3.6 Nâng cao kiến thức

- **Kiến trúc**: Nắm vững khái niệm cơ bản và cấu trúc của MCP.  
  → Xem: *Architecture* (tại `/docs/2026-07-28/learn/architecture`).
- **Bảo mật**: Hiểu các cân nhắc và thực hành tốt nhất về bảo mật khi sử dụng MCP.  
  → Xem: *Security best practices* (tại `/docs/2026-07-28/tutorials/security/security_best_practices`).
- **Cộng đồng**: Hướng dẫn cách đóng góp và tham gia vào phát triển MCP.  
  → Xem: *Contributing* (tại `/community/contributing`).

## 4. Ví dụ minh họa

**Scenario**: Một trợ lý AI dựa trên Claude muốn giúp người dùng xem lịchretta ngày hôm nay từ Google Calendar.

1. **Máy chủ MCP** được triển khai để bọc Google Calendar API và cung cấp một endpoint `GET /events/today`.
2. **Khách hàng Claude** (ứng dụng AI) được cấu hình để kết nối tới MCP server này qua chuẩn MCP.
3. Khi người dùng hỏi: “Hôm nay tôi có cuộc họp gì?”, Claude gửi yêu cầu tới MCP server, nhận về danh sách sự kiện và trả lời bằng ngôn ngữ tự nhiên.

*Mã mẫu giả định (pseudocode) để minh họa việc gọi MCP client:*

```python
# Giả sử chúng ta có thư viện mcp_client đã được cung cấp
from mcp_client import MCPClient

# Khởi tạo kết nối tới MCP server running locally tại cổng 8080
client = MCPClient(host="localhost", port=8080)

# Gọi hàm đã đượcExpose bởi server: get_today_events
events = client.call("get_today_events", {})

# Trình bày kết quả cho người dùng
if events:
    print("Hôm nay bạn có các cuộc họp sau:")
    for ev in events:
        print(f"- {ev['time']}: {ev['title']}")
else:
    print("Hôm nay không có cuộc họp nào.")
```

> **Lưu ý**: Đoạn mã trên chỉ là minh họa logic gọi MCP; chi tiết triển khai thực tế phụ thuộc vào thư viện MCP cụ thể và định nghĩa của server.

## 5. Tổng kết

- MCP cung cấp một chuẩn thống nhất để kết nối AI với dữ liệu, công cụ và quy trình bên ngoài, hoạt động như một “cổng USB‑C” cho trí tuệ nhân tạo.
- Nó mở ra nhiều khả năng thực tiễn: trợ lý cá nhân mạnh mẽ, sinh mã từ thiết kế, chatbot phân tích dữ liệu, và thậm chí thiết kế+in 3D.
- Với lợi thế về giảm độ phức tạp cho nhà phát triển, mở rộng khả năng cho ứng dụng AI và cải thiện trải nghiệm người dùng, MCP đang nhận được hỗ trợ rộng rãi từ nhiều công cụ và nền tảng phổ biến.
- Để bắt đầu, bạn có thể Xây dựng máy chủ, khách hàng hoặc ứng dụng MCP theo các hướng dẫn官方, sau đó tìm hiểu sâu hơn về kiến trúc và bảo mật.
- Cộng đồng MCP đang phát triển; việc tham gia đóng góp sẽ giúp tiêu chuẩn ngày càng hoàn thiện và phong phú hơn.