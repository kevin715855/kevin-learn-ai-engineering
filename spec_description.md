Mục tiêu: Hoàn thành việc cấu trúc lại repository và đẩy thay đổi lên GitHub trong khi bảo toàn toàn bộ nội dung dưới `data/processed/` chính xác như đã được commit bởi người đóng góp khác.

## Ràng buộc và phạm vi

### 1. Thư mục được bảo vệ: `data/processed/`
- Xem `data/processed/` là thư mục **được bảo vệ, chỉ đọc**.
- Bảo toàn tất cả các file, cấu trúc thư mục, tên file và nội dung file genau như chúng tồn tại trong nhánh `origin/main` hiện tại.
- Không được sửa đổi, đổi tên, di chuyển, xóa, tạo lại, dịch, định dạng lại hoặc ghi đè lên bất kỳ file nào trong `data/processed/`.
- Không được thay thế nội dung hiện tại bằng nội dung mới được tạo ra.
- Không được staging hoặc commit thay đổi đối với các file được bảo vệ.
- Nếu bất kỳ file local nào trong `data/processed/` khác với `origin/main`, cần nghiên cứu sự khác biệt và phục hồi nội dung gốc khi cần thiết, mà không làm mất công việc không liên quan.

### 2. Cấu trúc lại repository
Tất cả các thay đổi khác trong repository đều thuộc về công việc cấu trúc lại này.

- Bảo toàn và hoàn thành các thay đổi dự định cho mã nguồn, tích hợp frontend, scripts, tài liệu, cấu hình và các thư mục khác ngoài `data/processed/`.
- Cập nhật đường dẫn và tham chiếu để khớp với cấu trúc repository mới.
- Đảm bảo các script đọc nội dung bài học từ `data/processed/` thay vì thư mục `content/` cũ ở mọi nơi thích hợp.
- Đảm bảo frontend và các tiêu thụ khác sử dụng đường dẫn đúng mà không sửa đổi nội dung bài học được bảo vệ.
- Xem xét kỹ các file đã bị xóa. Xác định xem mỗi lần xóa có ý định có không, xem file có đã được di chuyển không, hoặc xem nó có phải cần phải phục hồi không.
- Bảo toàn công việc không liên quan và không bỏ semplicemente các thay đổi chỉ vì chúng chưa được commit.

### 3. Git và đồng bộ hóa từ xa

Trước khi thực hiện thay đổi:

1. Chạy `git status` và kiểm tra nhánh hiện tại.
2. Fetch nhánh `origin/main` mới nhất.
3. So sánh các file local với `origin/main`, đặc biệt là `data/processed/`.
4. Xác định các commit local, thay đổi chưa được commit và file chưa được tracked.
5. Tạo điểm phục hồi trước khi thực hiện các thaoáticos có khả năng gây hại.

Không được reset một cách mù quáng, clean, force-push, hoặc ghi đè lên các thay đổi từ xa.

Khi chuẩn bị commit:

- Chỉ staging các file thuộc về công việc cấu trúc lại.
- Xác minh rằng không có file nào trong `data/processed/` bị thay đổi trong staged diff.
- Kiểm tra toàn bộ staged diff, bao gồm cả việc xóa file và đổi tên.
- Commit và đẩy các thay đổi cấu trúc lại lên `origin/main` chỉ sau khi tất cả các kiểm tra đều qua.
- Nếu có thay đổi từ xa xung đột, cần hòa giải chúng mà không thay đổi nội dung được bảo vệ.

### 4. Xác thực

Trước khi đánh dấu任务完成, xác thực rằng:

- Tất cả các file hiện có trong `data/processed/` vẫn giữ nguyên nội dung so với mức chuẩn cơ bản.
- Frontend có thể tìm và tải dữ liệu bài học chính xác.
- Các script và tài liệu tham chiếu đến đường dẫn đúng.
- Không có sự xóa file hoặc mất dữ liệu không ý định xảy ra.
- Working tree và lịch sử commit nhất quán với các thay đổi dự định.
- Đẩy thay đổi thành công, và nhánh từ xa chứa commit cấu trúc lại.

Cung cấp báo cáo cuối cùng chứa:

1. Tóm tắt các thay đổi cấu trúc lại.
2. Các file hoặc thư mục được thêm, sửa đổi, xóa, hoặc di chuyển.
3. Xác nhận rằng `data/processed/` đã được bảo toàn.
4. Kiểm thử hoặc xác thực đã thực hiện và kết quả của họ.
5. Hash commit và trạng thái đẩy.

Nếu bất kỳ yêu cầu nào không thể được xác thực, dừng trước khi đẩy và giải thích chặn đó.

## Tiêu chí tiếp nhận

- `data/processed/` vẫn giữ nguyên nội dung so với mức chuẩn cơ bản đã đồng ý.
- Cấu trúc lại repository đã hoàn thành và hoạt động được.
- Không có công việc không liên quan hoặc commit từ xa nào bị mất.
- Thay đổi đã được commit và successfully pushed lên GitHub.
- Báo cáo cuối cùng được hỗ trợ bởi đầu ra thực tế của các lệnh Git, không phải là các giả định.