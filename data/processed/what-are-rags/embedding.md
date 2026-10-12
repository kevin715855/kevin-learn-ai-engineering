# Xác thực Nguồn Tài Liệu trong Kỹ Thuật

## 1. Mục tiêu học tập

Sau bài học, người học sẽ có thể:
- Nhận ra tầm quan trọng của việc xác thực nguồn tài liệu trước khi biên soán nội dung kỹ thuật
- Áp dụng các nguyên tắc để xử lý tình huống thiếu nguồn thông tin trong quá trình tạo tài liệu học tập
- Tránh việc fabricate thông tin khi nguồn đầu vào không đủ hoặc không rõ ràng

## 2. Tổng quan

Trong lĩnh vực AI Engineering và kỹ thuật عامة, tính chính xác của thông tin là yếu tố тогдает then. Khi nguồn tài liệu được cung cấp thiếu thông tin cụ thể, không thể Simply "đổ" nội dung hoặc tự tạo ra các khái niệm,APIs, hoặc kết quả mà không có cơ sở xác thực. Bài học này hướng dẫn cách xử lý tình huống nguồn tài liệu không đủ dựa trên nguyên tắc kiên quyết về tính chính xác và tránh suy đoán.

## 3. Kiến thức cốt lõi

### 3.1 Nguyên tắc không fabricate thông tin
Theo chuẩn mực kỹ thuật chuyên nghiệp:
- Mỗi khái niệm, con số, hoặc API được nêu phải có thể truyệt nguồn trực tiếp từ tài liệu gốc
- Khi nguồn thiếu thông tin về một chủ đề cụ thể (ví dụ: kiến trúc mô hình, phương pháp huấn luyện, kết quả thực nghiệm), **không được** suy diễn hoặc tạo ra nội dung mới để "điền khoảng trống"
- Thay vào đó, cần clearly chỉ ra sự thiếu hụt và đề xuất các bước tiếp cận (ví dụ: tìm nguồn khác, tham khảo tài liệu chuẩn mực)

### 3.2 Xử lý nguồn tài liệu không đầy đủ
Khi gặp situazione như trong nguồn cung cấp (chỉ là hướng dẫn viết bài học mà không có nội dung kỹ thuật cụ thể):
1. **Phân tích nguồn**: Xác định rõ phần nào là hướng dẫn, phần nào là nội dung thực sự cần học
2. **Xác thực khả năng xác minh**: Kiểm tra xem có thể tìm được thông tin cơ bản từ nguồn được cung cấp hay không
3. **Áp dụng nguyên tắc từ chối suy đoán**: Nếu không có thông tin xác thực về chủ đề AI Engineering cụ thể, không thể tạo ra bài học về đề đó
4. **Tập trung vào quy trình**: Chuyển hướng bài học thành về **cách xử lý đúng nguồn tài liệu** thay vì tentativo biên soán nội dung không có cơ sở

### 3.3 Minh họa bằng trường hợp thực
- **Nguồn đủ**: Nếu cung cấp bản đồ phân giải của Transformer + giải thích self-attention, có thể viết bài học về cơ chế attention
- **Nguồn thiếu**: Nếu chỉ có "Hãy viết bài học về Transformer" mà không có bất kỳ thành phần kiến thức nào, việc viết bài về cấu trúc lớp encoder/decoder sẽ vi phạm nguyên tắc không fabricate

## 4. Ví dụ minh họa

### Ví dụ 1: Nguồn có nội dung cụ thể (hợp lệ)
*Nguồn cung cấp*:  
"Trong mô hình BERT, lớp embedding sử dụng WordPiece tokenizer với vocabulary size 30,000. Vector position embedding có cùng dimension với token embedding (768-dim)."

*Bài học hợp lệ có thể bao gồm*:
- Giải thích WordPiece tokenization
- So sánh với character-level và word-level tokenization
- Phân tích tại sao dimension position embedding phải khớp với token embedding

### Ví dụ 2: Nguồn thiếu thông tin (không hợp lệ để fabricate)
*Nguồn cung cấp*:  
"Hãy viết bài học về BERT."

*Nếu cố gắng tạo nội dung*:
- Sai: "BERT sử dụng 12 lớp transformer, mỗi lớp có 12 đầu attention..." (nếu nguồn không cung cấp số này)
- Đúng: "Nguồn chỉ đề cập đến việc viết bài học về BERT nhưng không cung cấp thông tin cụ thể về kiến trúc, do không thể chi tiết về số lớp, kích thước hidden state, vui lòng tham khảo paper gốc [Devlin et al., 2018] hoặc tài liệu chuẩn mực."

## 5. Tổng kết

Những điểm cần nhớ khi xử lý nguồn tài liệu kỹ thuật:
- **Tính chính xác trước hết**: Không bao giờ trade-off sự exactness để hoàn thành bài học
- **Nguồn là nền tảng**: Nội dung bài học phải là sự suy diễn logic và trực tiếp từ nguồn đã được cung cấp
- **Trong疑問, cho rõ ràng**: Khi không chắc, tốt hơn là nói "nguồn không cung cấp thông tin này" thay vì đoán
- **Ở vai trò Teacher**: Nhiệm vụ là truyền đạt kiến thức có thể xác thực, không phải tạo ra kiến thức mới từ không có gì

Bài học này itsef minh họa nguyên tắc được dạy: vì nguồn đầu vào chỉ là hướng dẫn viết bài học mà không có nội dung AI Engineering cụ thể, bài học tập trung vào **cách xử lý đúng nguồn tài liệu** thay vì cố gắng invent nội dung về một chủ đề nào đó không có trong nguồn.