---
id: 2t4uINxmzfx8FUF-_i_2B
slug: connect-to-remote-server
title: "Kết nối tới máy chủ từ xa"
original_title: "Connect to Remote Server"
module_id: 4_ap0rD9Gl6Ep_4jMfPpG
module_title: "AI Agents"
language: vi
source_status: completed
---
# Kết nối tới Máy chủ Từ xa

Triển khai từ xa hoặc trên đám mây đặt máy chủ MCP trên nhà cung cấp đám mây thay vì trên máy local. Bạn đóng gói máy chủ dưới dạng container hoặc máy ảo, chọn dịch vụ như AWS, Azure hoặc GCP, và cung cấp cho nó tài nguyên tính toán, lưu trữ và một địa chỉ HTTPS công khai. Cân bằng tải (load balancer) phân bổ lưu lượng, trong khi tự động mở rộng (auto-scaling) thêm hoặc xóa các bản sao của máy chủ khi nhu cầu thay đổi. Bạn bảo mật điểm cuối bằng TLS, khóa API và tường lửa, và gửi log và chỉ số đến công cụ giám sát của nhà cung cấp. Cấu hình này cho phép máy chủ phục vụ nhiều người dùng, việc cập nhật trở nên dễ dàng hơn và bạn tránh được giới hạn phần cứng local, tuy nhiên bạn phải theo dõi chi phí và bảo vệ dữ liệu nhạy cảm.

Hãy truy cập các nguồn lực sau đây để biết thêm chi tiết:

- [@official@Kết nối với các Máy chủ MCP từ xa](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)
- [@article@Máy chủ MCP từ xa](https://mcpservers.org/remote-mcp-servers)
- [@video@Triển khai MCP Server từ xa bằng Python (Bước từng bước)](https://www.youtube.com/watch?v=wXAqv8uvY0M)