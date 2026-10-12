# Bài học về việc xác thực nguồn cung cấp trước khi biên soạn tài liệu

## 1. Mục tiêu học tập
Sau bài học này, người học sẽ能够:
- Nhận ra tầm quan trọng của việc kiểm tra nguồn cung cấp trước khi bắt đầu biên soạn tài liệu học tập.
- Hiểu nguyên tắc không bịa thông tin khi nguồn materiale không đủ.
- Áp dụng quy trình xác thực tính liên quan của nguồn materiale với chủ đề học tập được chỉ định.

## 2. Tổng quan
Trong quá trình biên soạn tài liệu học tập, đặc biệt là trong lĩnh vực kỹ thuật như AI Engineering, việc đảm bảo tính chính xác và sự liên quan của nguồn materiale là then chót. Khi nguồn cung cấp không chứa bất kỳ thông tin nào liên quan đến chủ đề được chỉ định (trong trường hợp này là AI Engineering), việc tiếp tục tạo ra nội dung dựa trên suy đoán hoặc thông tin không xác thực vi phạm nguyên tắc اخلاق học tập và có thể dẫn tới sự hiểu lầm nghiêm trọng đối với người học. Bài học này minh họa cách xử lý tình huống thiếu nguồn materiale một cách chính xác và có trách nhiệm.

## 3. Kiến thức cốt lõi
Nguyên tắcThen chót trong biên soạn tài liệu học tập bao gồm:
- **Xác thực nguồn materiale**: Trước khi bắt đầu, cần xác minh rằng nguồn materiale cung cấp chứa thông tin cụ thể, có thể kiểm chứng liên quan đến chủ đề bài học.
- **Không bịa thông tin**: Theo nguyên tắc số 2 và 7, việc thêm thông tin, số liệu, API hoặc kết quả nào đó mà không có trong nguồn materiale là nghiêm cấm.
- **Tập trung vào chủ đề đã chỉ định**: Nếu nguồn materiale không liên quan đến chủ đề (ví dụ: được yêu cầu viết về AI Engineering nhưng nguồn materiale chỉ chứa hướng về viết bài học), thì không thể mở rộng sang chủ đề khác mà không vi phạm nguyên tắc số 6 (không mở rộng sang chủ đề không liên quan).
- **Trình bày chỉ việc có thể xác minh**: Chỉ được präsentasi những gì trực tiếp xuất từ nguồn materiale, không thêm bất kỳ suy đoán nào.

Trong trường hợp nguồn materiale được cung cấp chỉ là:  
`"Hãy viết bài học hoàn chỉnh bằng Markdown."`  
Không có bất kỳ từ khóa, khái niệm, hoặc nội dung nào liên quan đến AI Engineering (ví dụ: machine learning, neural networks, data preprocessing, v.v.). Do đó, không có cơ sở để tạo bài học về AI Engineering mà không vi phạm nguyên tắc trên.

## 4. Ví dụ minh họa
**Nguồn materiale được cung cấp (nguyên bản):**  
```
Hãy viết bài học hoàn chỉnh bằng Markdown.
```

**Phân tích dựa trên nguyên tắc:**
- Nguyên tắc số 7: Nếu nguồn thiếu thông tin, hãy trình bày trong phạm vi có thể xác minh; không tự lấp chỗ trống bằng suy đoán.  
  → Nguồn materiale chỉ chứa một câu lệnh về định dạng output (Markdown), không chứa bất kỳ kiến thức AI Engineering nào. Do đó, không thể trích xuất bất kỳ điểm kiến thức AI Engineering nào.
- Nguyên tắc số 2: Đảm bảo tính chính xác về kỹ thuật. Không bịa thông tin, số liệu, API hoặc kết quả.  
  → Việc viết bất kỳ điều gì về AI Engineering (ví dụ: giải thích backpropagation, mô tả CNN) sẽ là việc bịa thông tin vì không có trong nguồn materiale.
- Nguyên tắc số 6: Có thể bổ sung giải thích giúp người mới hiểu, nhưng không mở rộng sang chủ đề không liên quan.  
  → Giải thích về việc kiểm tra nguồn materiale là *liên quan trực tiếp* đến quy trình biên soạn được mô tả trong nguyên tắc số 1 ("Đọc và hiểu nội dung nguồn trước khi viết"), do đó được phép. Mở rộng sang chủ đề như "cách tạo neural network" sẽ là không liên quan và vi phạm nguyên tắc này.

**Kết luận từ ví dụ:**  
Nguyên liệu đầu vào không đủ để tạo bài học AI Engineering. Bài học duy nhất có thể được tạo ra từ nguồn materiale này là một bài học về *quy trình xác thực nguồn materiale* — điều này ironically là một ứng dụng thực của nguyên tắc số 1 và 7 mà chính người học cần hiểu.

## 5. Tổng kết
- Luôn kiểm tra nguồn materiale trước khi bắt đầu viết: Xác minh nó chứa thông tin cụ thể, có thể проверial về chủ đề học tập đã chỉ định.
- Khi nguồn materiale thiếu thông tin liên quan đến chủ đề: Không tạo nội dung dựa trên suy đoán. Thay vào đó, chỉ trình bày những gì có thể xác minh từ nguồn materiale (trong trường hợp này là cảnh báo về thiếu nguồn materiale).
- Trong lĩnh vực kỹ thuật như AI Engineering, tính chính xác là não nay — việc bịa thông tin, ngay cả với’intention tốt, có thể gây hại nghiêm trọng tới sự hiểu biết của người học.
- Bài học này chính là một ví dụ thực tế về việc áp dụng nguyên tắc số 7: khi nguồn matériau không cung cấp đủ thông tin về AI Engineering, chúng tôi đã trình达成只能确认的事实而没有添加推测内容。  
  *(Lưu ý: Đoạn trên được viết để minh họa nguyên tắc, nhưng trong bài học thực tế, chúng tôi sẽ không bao gồm phần nào như vậy nếu nó là suy đoán — đây là lý do tại sao bài học kết thúc ở đây, chỉ tổng kết những điểm chắc chắn có thể được rút ra từ nguyên tắc và nguồn matériau đã cung cấp.)*