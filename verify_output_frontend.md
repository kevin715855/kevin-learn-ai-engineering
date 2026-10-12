Mục tiêu: Xác minh rằng output/ và frontend/src/roadmap-data.json được tạo ra chính xác từ data/processed/

Mô tả công việc:
- Sau khi data/processed/ đã được phục hồi đúng và các script đã được sửa để đọc từ data/processed/, cần xác minh rằng:
  1. Thư mục output/ chứa các file đã được xử lý đúng (có thể là bản dịch hoặc định dạng lại)
  2. File frontend/src/roadmap-data.json chứa đầy đủ dữ liệu bài học đúng định dạng
- Đây là bước quan trọng để đảm bảo rằng frontend và các tiêu thụ khác có thể truy cập đúng nội dung bài học

Các bước:
1. Đọc và hiểu kế hoạch cấu trúc lại từ issue spec của Kiến trúc sư (issue #ROAD-69)
2. Xác định quy trình tạo ra output/ và roadmap-data.json:
   - Tìm các script chịu trách nhiệm cho việc này
   - Hiểu họ đọc từ đâu và ghi ra đâu
3. Chạy quy trình tạo ra output/ (nếu có)
   - Xác minh rằng các file trong output/ có nội dung đúng (không phải chỉ là placeholder)
   - Kiểm tra xem họ có đang đọc từ data/processed/ không
4. Chạy quy trình tạo ra frontend/src/roadmap-data.json (nếu có script riêng)
   - Hoặc xác minh rằng generate_roadmap_json.py đã được sửa để đọc từ data/processed/ và output/ như 적절
   - Kiểm tra file JSON để đảm bảo:
     * Nó chứa đủ modules và bài học
     * Nội dung bài học là đầy đủ và chính xác (không phải chỉ frontmatter)
     * Định dạng đúng cho frontend sử dụng
5. Xác minh rằng frontend có thể đọc và sử dụng dữ liệu này đúng (nếu có thể kiểm tra)

Files/PR dự kiến:
- Thay đổi trong các script tạo ra output/ và roadmap-data.json (nếu cần)
- Có thể có thay đổi trong output/ nếu chúng được tái tạo đúng

Cách kiểm tra:
- Kiểm tra một vài file trong output/ để xác nhận họ có nội dung đầy đủ (so sánh với data/processed/ hoặc mong đợi)
- Kiểm tra frontend/src/roadmap-data.json để xác nhận nó chứa đầy đủ nội dung bài học
- Chạy bất kỳ test nào có sẵn để xác minh frontend hoạt động đúng
- Đảm bảo git status khôngแสดง bất kỳ thay đổi không mong muốn nào trong data/processed/ (vì chúng là protected)

Lưu ý: Đây là một trong những bước xác thực cuối cùng trước khi push các thay đổi lên GitHub.