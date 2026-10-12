---
id: H-G93SsEgsA_NGL_v4hPv
slug: connect-to-local-server
title: "Kết nối tới Máy chủ cục bộ"
original_title: "Connect to Local Server"
module_id: 4_ap0rD9Gl6Ep_4jMfPpG
module_title: "AI Agents"
language: vi
source_status: completed
---
# Kết Nối Đến Máy Chủ Cục Bộ

Triển khai trên Desktop cục bộ có nghĩa là chạy máy chủ MCP trực tiếp trên máy tính cá nhân của bạn thay vì trên một đám mây hoặc máy chủ từ xa. Bạn cài đặt phần mềm MCP, các thời gian chạy cần thiết và các tệp mô hình lên desktop hoặc laptop của bạn. Máy chủ sau đó sẽ lắng nghe trên địa chỉ cục bộ như `127.0.0.1:8000`, chỉ có thể truy cập từ cùng một máy trừ khi bạn mở cổng thủ công. Cài đặt này rất thích hợp cho các bài kiểm tra nhanh, demonstration cá nhân hoặc các thử nghiệm riêng tư vì bạn giữ toàn quyền kiểm soát và tránh được chi phí đám mây. Tuy nhiên, nó bị giới hạn bởi tốc độ và bộ nhớ của phần cứng bạn, và người khác không thể truy cập vào nó mà không cần sử dụng công cụ tạo Tunnel như ngrok hoặc chuyển cổng cục bộ.

Truy cập các nguồn lực sau để tìm hiểu thêm:

- [@official@Kết nối với máy chủ MCP địa phương](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
- [@article@Cách Xây Dựng và Lưu Trữ MCP Server Của Bạn Trong Các Bước Dễ Dàng](ttps://collabnix.com/how-to-build-and-host-your-own-mcp-servers-in-easy-steps/)
- [@video@Máy chủ MCP địa phương cho Cursor (bước theo bước)](https://www.youtube.com/watch?v=_Qr0WTgR5EM)