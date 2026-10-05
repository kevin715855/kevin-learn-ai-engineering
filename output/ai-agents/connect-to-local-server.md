---
id: H-G93SsEgsA_NGL_v4hPv
slug: connect-to-local-server
title: "Kết nối tới máy chủ địa phương"
original_title: "Connect to Local Server"
module_id: 4_ap0rD9Gl6Ep_4jMfPpG
module_title: "AI Agents"
language: vi
source_status: completed
---
# Kết nối tới Máy chủ cục bộ

Triển khai Local Desktop có nghĩa là chạy máy chủ MCP trực tiếp trên máy tính của bạn thay vì trên một đám mây hoặc máy chủ từ xa. Bạn cài đặt phần mềm MCP, các runtime cần thiết và các file model lên desktop hoặc laptop của bạn. Sau đó máy chủ sẽ lắng nghe trên địa chỉ cục bộ như `127.0.0.1:8000`, chỉ có thể truy cập từ cùng một máy trừ khi bạn mở cổng một cách thủ công. Cài đặt này rất hữu ích cho các thử nghiệm nhanh, demonstration cá nhân hoặc thí nghiệm riêng vì bạn giữ toàn quyền kiểm soát và tránh chi phí đám mây. Tuy nhiên, nó bị giới hạn bởi tốc độ và bộ nhớ phần cứng của bạn, và người khác không thể truy cập vào nó mà không dùng các công cụ tạo tunnel như ngrok hoặc chuyển cổng cục bộ.

Truy cập các nguồn tài nguyên sau để tìm hiểu thêm:

- [@official@Kết nối đến máy chủ MCP địa phương](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
- [@article@Hướng dẫn Xây dựng và Lưu trữ Máy chủ MCP Của Bạn trong Các Bước Đơn giản](ttps://collabnix.com/how-to-build-and-host-your-own-mcp-servers-in-easy-steps/)
- [@video@Máy chủ MCP địa phương cho Cursor (Bước từng bước)](https://www.youtube.com/watch?v=_Qr0WTgR5EM)