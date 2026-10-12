Mục tiêu: Sửa các script để đọc nội dung bài học từ `data/processed/` thay vì từ `content/`

Mô tả công việc:
- Theo yêu cầu issue: "Đảm bảo các script đọc nội dung bài học từ `data/processed/` thay vì thư mục `content/` cũ ở mọi nơi thích hợp"
- Cần tìm và sửa tất cả các script که hiện đang đọc từ `content/` để thay bằng việc đọc từ `data/processed/`
- Phải đảm bảo việc thay đổi này không làm vỡ chức năng và rằng dữ liệu được đọc đúng đạng

Các bước:
1. Đọc và hiểu kế hoạch cấu trúc lại từ issue spec của Kiến trúc sư (issue #ROAD-69)
2. Tìm kiếm trong toàn bộ repository để tìm các tham chiếu đến `content/` trongscripts và file cấu hình
   - Tìm kiếm pattern như `content/`, `content\\`, hoặc các đường dẫn cụ thể đến file trong `content/`
3. Đối với mỗi tham chiếu tìm thấy:
   - Xác định xem đây là một script cần sửa hay là phần của tài liệu/documentation
   - Nếu là script, thay đổi đường dẫn để trỏ đến đường dẫn tương ứng trong `data/processed/`
   - Ví dụ: thay `content/ai-agents/agents-usecases.md` bằng `data/processed/ai-agents/agents-usecases.md`
4. Đặc biệt chú ý đến script `generate_roadmap_json.py` và bất kỳ script nào khác tạo ra dữ liệu cho frontend
5. Kiểm tra sau khi thay đổi để đảm bảo:
   - Tất cả các script vẫn hoạt động đúng
   - Dữ liệu được đọc là đầy đủ và chính xác
   - Không còn أي tham chiếu lỗi thời đến `content/` trong code

Files/PR dự kiến:
- Thay đổi trong các script như `generate_roadmap_json.py` và có thể là các script xử lý khác
- Thay đổi trong các file cấu hình nếu có

Cách kiểm tra:
- Chạy các script để确保他们工作正常
- Kiểm tra đầu ra của chúng (ví dụ: file `frontend/src/roadmap-data.json`) để xác nhận họ đang đọc dữ liệu đúng
- Tìm kiếm trong toàn bộ repository tham chiếu đến `content/` trong các file không phải là tài liệu hoặc commentary và xác nhận không còn lại nào

Lưu ý: Công việc này nên được thực hiện SAU_KHI `data/processed/` đã được phục hồi đúng và có thể cần thực hiện TRƯỚC_KHI chạy các script tạo ra đầu ra.