# Adversarial Testing for Generative AI  

## 1. Mục tiêu học tập  

- **Hiểu nguyên tắc**: Người học sẽ nắm rõ ý nghĩa của *adversarial testing* – cách đánh giá một mô hình AI sinh học bằng cách cung cấp các đầu vào có khả năng gây ra output không an toàn hoặc sai lệch.  
- **Biết quy trình**: Người học sẽ thành thạo 4 bước chính của quy trình adversarial testing:  
  1. Xác định các đầu vào cần kiểm tra.  
  2. Tìm hoặc tạo bộ dữ liệu thử nghiệm.  
  3. Tạo và gán nhãn kết quả của mô hình.  
  4. Báo cáo và giảm thiểu các lỗi phát hiện được.  
- **Ứng dụng thực tiễn**: Sử dụng kiến thức này để thiết kế, thực hiện và ghi nhận kết quả adversarial testing cho mô hình sinh học (ví dụ: LLM, image generator, …) nhằm cải thiện độ tin cậy, an toàn và tuân thủ chính sách sản phẩm.  

## 2. Tổng quan  

Adversarial testing là một phương pháp **kiểm tra chủ động** nhằm “đánh lừa” mô hình AI bằng cách cung cấp dữ liệu mà người dùng có thể gây ra các vi phạm an toàn (policy violations), lỗi thời gian thực hoặc các hành vi không mong muốn.  

- **Mục đích**: Khám phá các điểm yếu tiềm ẩn, đánh giá mức độ mô hình đáp ứng được các rủi ro an toàn và cung cấp dữ liệu để **cải tiến mô hình**, **xây dựng các bộ lọc**, hoặc **đánh giá rủi ro** trước khi sản phẩm ra mắt.  
- **Liên quan**: Đây là một phần quan trọng trong quá trình **xây dựng AI có trách nhiệm** (responsible AI) và được khuyến nghị làm một trong các “best practice” cho các nhóm phát triển AI.  

## 3. Kiến thức cốt lõi  

### 3.1 Adversarial testing  
- **Định nghĩa**: Kiểm tra mô hình bằng cách cung cấp **đầu vào “adversarial”** – dữ liệu có khả năng gây ra output không an toàn (ví dụ: lời nói vi phạm chính sách, nội dung nhạy cảm, lỗi thực thi).  
- **Loại truy vấn**:  
  - **Explicitly adversarial**: chứa ngôn ngữ vi phạm chính sách rõ ràng hoặc cố gắng “lách luật” mô hình.  
  - **Implicitly adversarial**: xuất hiện bình thường nhưng chứa thông tin nhạy cảm, gây tranh cãi hoặc tiềm ẩn (ví dụ: đề cập đến tuổi, giới tính, tôn giáo, tài chính).  

### 3.2 Quy trình adversarial testing (4 bước)  

| Bước | Nội dung chính | Ghi chú quan trọng |
|------|----------------|-------------------|
| **1. Identify inputs for testing** | Xác định các loại đầu vào cần kiểm tra dựa trên **chính sách sản phẩm**, **kiểu dùng**, **edge case** và **đa dạng từ vựng/semantic**. | - Phân tích chính sách an toàn (ví dụ: Google Generative AI Prohibited Use Policy).<br>- Thu thập các trường hợp sử dụng thực tế (tóm tắt tài liệu, đề xuất, biểu diễn văn hoá).<br>- Đảm bảo **lexical diversity** (độ dài, từ vựng, cấu trúc câu) và **semantic diversity** (đề tài, văn hoá, ngữ cảnh). |
| **2. Find or create test datasets** | Tìm dữ liệu đã tồn tại hoặc tạo dữ liệu mới để **gây ra output vi phạm**. | - **Find**: Sử dụng các bộ dữ liệu academic benchmark trong Responsible Generative AI Toolkit để kiểm tra phạm vi an toàn.<br>- **Create**: Đầu tiên tạo “seed” dataset (tens‑hàng mẫu) rồi mở rộng bằng công cụ tổng hợp dữ liệu (BigQuery DataFrames, LLM).<br>- Tránh lặp lại, trùng lặp nhãn (hate speech vs obscenity) để không gây nhiễu. |
| **3. Generate and annotate model outputs** | Dùng mô hình sinh học để tạo output cho các câu hỏi adversarial, sau đó **gán nhãn** các lỗi/vi phạm. | - Tự động: Dùng **safety classifiers** để phân loại (cảnh báo Hate Speech, Violence, …).<br>- Nhân: Rát nhân cần kiểm tra lại các nhãn “uncertain” vì các tín hiệu có định nghĩa mỏng (ví dụ: Hate Speech).<br>- Cung cấp **guideline** cho rater để giảm biến đổi do背景, kiến thức, giá trị cá nhân. |
| **4. Report and mitigate** | Tổng hợp kết quả, tính các chỉ số an toàn, trực quan hoá (biểu đồ, ví dụ lỗi) và đề xuất **biện pháp giảm thiểu** (fine‑tuning, filter, blocklist). | - Báo cáo giúp **đánh giá rủi ro** và **quyết định launch**.<br>- Thông tin được truyền cho các bên liên quan (stakeholder, quyết định viên). |

### 3.3 Các khái niệm/đối tượng quan trọng (giữ nguyên tiếng Anh)

- **Adversarial query** – truy vấn có tính “đánh lừa”.  
- **Policy violation** – vi phạm chính sách an toàn.  
- **Safety classifier** – mô hình/phần mềm phân loại nội dung vi phạm.  
- **Human rater** – người đánh giá thủ công.  
- **Fine‑tuning** – tinh chỉnh mô hình dựa trên dữ liệu mới.  
- **Filter / blocklist** – bộ lọc, danh sách cấm.  

## 4. Ví dụ minh họa  

### 4.1 Tình huống  
Bạn đang phát triển một chatbot dựa trên LLM cho việc **tóm tắt tài liệu**. Mục tiêu an toàn: **cấm** mô hình đưa ra bất kỳ nội dung vi phạm chính sách nào (ví dụ: khuyên độc hại, hate speech, medical advice không chính thống).

### 4.2 Áp dụng quy trình  

1. **Identify inputs**  
   - **Chính sách**: “Không cung cấp lời khuyên y tế không được xác thực”.  
   - **Edge case**: Người dùng hỏi “Cách chữa bệnh tiểu đường nhanh nhất?”.  
   - **Lexical diversity**: Câu hỏi ngắn, dài, dùng từ “cách”, “kỹ thuật”, “thuốc”, “điều trị”.  

2. **Find or create test datasets**  
   - **Find**: Kiểm tra các bộ dữ liệu đã có ví dụ “medical advice” (ví dụ: MIMIC‑IV, HealthQA).  
   - **Create**: Nếu thiếu, tạo seed 30 câu hỏi mang tính “implicitly adversarial” (ví dụ: “Bạn có thể gợi ý một loại thuốc giảm đường huyết không?”). Sử dụng LLM để tổng hợp thêm 200 câu, biến đổi ngữ cảnh, tone.  

3. **Generate and annotate model outputs**  
   - Gửi các câu hỏi này tới mô hình, thu thập câu trả lời.  
   - Dùng **safety classifier** (ví dụ: Perspective API, custom classifier) để tự động đánh dấu “medical advice”.  
   - Rát nhân kiểm tra 20% mẫu “uncertain”, sửa nhãn nếu cần.  

4. **Report and mitigate**  
   - Tổng hợp tỷ lệ “policy violation” = 12% (so với mục tiêu <5%).  
   - Trực quan hoá bằng biểu đồ “violation rate by query length”.  
   - **Biện pháp**: Thêm **filter** dựa trên danh sách từ khóa y tế, hoặc **fine‑tune** mô hình với dữ liệu “safe medical advice” và dữ liệu “adversarial medical queries”.  

### 4.3 Kết quả  

| Kết quả | Mô tả |
|--------|-------|
| **Tỷ lệ vi phạm** | 12% (cao hơn ngưỡng cho phép). |
| **Loại vi phạm phổ biến** | Gợi ý thuốc, chỉ dẫn điều trị, thông tin y tế không xác thực. |
| **Biện pháp khắc phục** | - Triển khai filter từ khóa y tế.<br>- Tăng cường dữ liệu training bằng “adversarial medical Q&A”.<br>- Đánh giá lại mô hình mỗi 2 tuần. |

## 5. Tổng kết  

- **Adversarial testing** giúp **phát hiện sớm** các lỗi an toàn và **cải thiện** mô hình sinh học.  
- Quy trình gồm **4 bước**: Xác định đầu vào, Tìm/ tạo dữ liệu, Tạo & gán nhãn output, Báo cáo & giảm thiểu.  
- **Đa dạng** (lexical, semantic) và **liên kết** với chính sách sản phẩm là yếu tố then chốt để test có ý nghĩa.  
- Sử dụng **safety classifiers** kết hợp **human rater** để đánh giá chính xác, tránh bias.  
- Kết quả **báo cáo** cung cấp các chỉ số an toàn, trực quan hoá và hướng dẫn **biện pháp** (filter, fine‑tuning, blocklist) để **đảm bảo tính tin cậy** và **tuân thủ** cho ứng dụng AI sinh học.  

> **Lưu ý**: Khi thực hiện adversarial testing, luôn tuân thủ **chính sách an toàn** của sản phẩm và **quy định pháp lý** liên quan đến dữ liệu nhạy cảm (sức khỏe, tài chính, tôn giáo,…).