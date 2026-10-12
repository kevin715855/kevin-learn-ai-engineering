Mục tiêu: Phục hồi tất cả các file trong thư mục `data/processed/` để khớp exatamente với `origin/main`

Mô tả công việc:
- Các file trong `data/processed/` hiện tại có nội dung không đúng (nh resemblance đến phiên bản ngắn của `content/` thay vì nội dung đầy đủ, chi tiết như trong `origin/main`)
- Cần sao chép nội dung từ `origin/main:data/processed/` để thay thế nội dung local sai
- Phải đảm bảo không làm mất bất kỳ công việc không liên quan nào (kéo xuống từ `origin/main` và thay thế nội dung-local)

Các bước:
1. Xác nhận danh sách tất cả các file trong `data/processed/` mà cần được phục hồi
2. Với mỗi file, thay thế nội dung-local bằng nội dung từ `origin/main`
   - Sử dụng: `git show origin/main:<file-path> > <file-path>` hoặc sao chép trực tiếp
3. Xác minh rằng sau khi phục hồi, `git diff origin/main -- data/processed/` khôngแสดง bất kỳ sự khác biệt nào
4. Đảm bảo không có file nào trong `data/processed/` được staging để commit (vì chúng là protected)

Files/PR yang dự kiến:
- Các file trong thư mục `data/processed/` sẽ được thay đổi để khớp với `origin/main`

Cách kiểm tra:
- Chạy `git diff origin/main -- data/processed/` và xác nhận không có output
- Kiểm tra một vài file để đảm bảo chúng có nội dung đầy đủ, chi tiết (không phải chỉ frontmatter)

Lưu ý: Đây là công việc phục hồi, không phải là phần của việc cấu trúc lại - mục tiêu là đưa `data/processed/` về trạng thái đúng như trong `origin/main` trước khi bắt đầu cấu trúc lại.