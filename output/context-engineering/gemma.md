# Bài học: Xác nhận tính đủ của nguyên liệu nguồn

## 1. Mục tiêu học tập
- Nhận biết khi nguyên liệu nguồn thiếu thông tin kỹ thuật cần thiết
- Áp dụng nguyên tắc không bịa thông tin trong việc biên soạn tài liệu học tập
- Hiểu tầm quan trọng của việc kiểm tra tính xác thực trước khi tạo bài học

## 2. Tổng quan
Trong quá trình biên soạn tài liệu học tập về AI Engineering, bước đầu tiên và quan trọng nhất là xác nhận rằng nguyên liệu nguồn chứa đủ thông tin kỹ thuật có thể xác minh. Bài học này minh họa quy trình xử lý khi nguyên liệu nguồn không cung cấp nội dung cụ thể cần thiết để tạo ra bài học có giá trị, đồng thời tuân thủ nghiêm ngặt các nguyên tắc biên soạn được cung cấp.

## 3. Kiến thức cốt lõi

### Nguyên tắc không lấp chỗ trống bằng suy đoán
Theo nguyên tắc số 7 trong hướng dẫn biên soạn:  
> "Nếu nguồn thiếu thông tin, hãy trình bày trong phạm vi có thể xác minh; không tự lấp chỗ trống bằng suy đoán."  

Nguyên tắc này có nghĩa là khi materiale sources không chứa các chi tiết kỹ thuật cụ thể (ví dụ: API, mô hình, số liệu, thuật toán), **không được phép** tạo ra thông tin假想 để điền vào những chỗ trống. Ví dụ:
- ❌ Sai: "Nguyên liệu nguồn không nói về TensorFlow, vì vậy tôi sẽ giảng giải về TensorFlow 2.0..."
- ✅ Đúng: "Nguyên liệu nguồn không cung cấp bất kỳ thông tin cụ thể nào về framework hoặc công cụ AI nào."

### Yêu cầu về tính xác thực técnica
Mỗi bài học kỹ thuật phải đáp ứng:
- **Gán mác với nguồn gốc**: Mọi khái niệm, thuật ngữ, ví dụ code phải trực tiếp traceable về nguyên liệu nguồn.
- **Không mở rộng chủ đề**: Nguyên tắc #6 cấm mở rộng sang chủ đề không liên quan, ngay cả khi mục tiêu là giúp người mới hiểu hơn.
- **Trân trọng định dạng mà không thay thế nội dung**: Yêu cầu "viết bằng Markdown" chỉ là chỉ định định dạng, không thể được xem là nội dung học tập.

### Quy trình xử lý khi thiếu thông tin
1. **Đọc và hiểu nguyên liệu nguồn**: Xác định chính xác những gì được cung cấp và ciò che manca.
2. **Kiểm tra tính đủ**: Đặt câu hỏi: "Nguyên liệu nguồn có chứa đủ thông tin kỹ thuật để giải thích một khái niệm AI Engineering cụ thể không?"
3. **Hành động соответствующий**: 
   - Nếu đủ: Tiến hành biên soạn theo cấu trúc bài học.
   - Nếu không đủ: Trình bày rõ ràng tình trạng thiếu hụt thay vì tạo ra nội dung giả.

## 4. Ví dụ minh họa

### Nguyên liệu nguồn được cung cấp:
```
Hãy viết bài học hoàn chỉnh bằng Markdown.
```

### Phân tích nội dung nguồn
- **Yêu cầu định dạng**: Rõ ràng là "viết bằng Markdown" (chỉ định cách trình bày).
- **Thiếu nội dung học tập**: 
  - Không có bất kỳ khái niệm AI Engineering nào được đề cập (ví dụ: mô hình, thuật toán, ứng dụng).
  - Không có số liệu, API, hoặc kết quả 실험 nào để giải thích.
  - Không có bối cảnh hoặc mục tiêu học tập cụ thể nào được mô tả.

### Phản hồi適当 theo nguyên tắc
> "Nguyên liệu nguồn chỉ cung cấp yêu cầu về định dạng output (Markdown) mà không chứa bất kỳ nội dung kỹ thuật cụ thể nào liên quan đến AI Engineering. Do đó, không thể tạo ra bài học kỹ thuật có giá trị vì việc làm như vậy sẽ vi phạm nguyên tắc #7 (Không được lấp chỗ trống bằng suy đoán). Nội dung học tập phải xuất trực tiếp từ nguyên liệu nguồn, và trong trường hợp này, nguyên liệu nguồn không chứa thành phần nào để formando thành bài học về AI Engineering."

### Giải thích tại sao đây là phản hồi đúng
- **Tuân thủ nguyên tắc #7**: Không bịa ra một chủ đề như "Giới thiệu về Rückpropagation" hoặc "Ứng dụng của CNN trong xử lý ảnh" vì nguyên liệu nguồn không đề cập đến chúng.
- **Giữ nguyên yêu cầu định dạng**: Văn bản phản hồi vẫn được viết bằng Markdown như được yêu cầu.
- **Không vi phạm nguyên tắc #6**: Không mở rộng sang chủ đề ngoài zakres (ví dụ: không giải thích tại sao Markdown quan trọng hoặc cách viết bài học tốt).
- **Chính xác về tính disponibile**: Đúngly afirmar que a fonte não contém conteúdo técnico.

## 5. Tổng kết
- **Nội dung precedes format**: Yêu cầu về định dạng (Markdown) là thứ hai; nội dung kỹ thuật có thể xác minh từ nguồn là điều precede và bắt buộc.
- **Integritas over completion**:Một bài học ngắn nhưng accurato là luôn preferable to một bài học dài piena di contenuti inventati.
- **Kiểm tra trước khi viết**: Luôn bắt đầu bằng bước xác thực: "Nguyên liệu nguồn này cho tôi gì để explicar về AI Engineering?"
- **Nguyên tắc là bản hướng dẫn**: Khi nguồn thiếu thông tin, việc áp dụng đúng nguyên tắc #7 là dấu hiệu của chuyên môn, không phải sự bất ngờ.