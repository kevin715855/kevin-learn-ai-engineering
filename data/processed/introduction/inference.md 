# AI Inference và AI Training: Khái niệm và Ứng dụng thực tiễn  

## 1. Mục tiêu học tập  
Sau khi hoàn thành bài học, người học sẽ có thể:  

- Giải thích sự khác biệt giữa **AI inference** (suy luận) và **AI training** (huấn luyện).  
- Mô tả cách một mô hình học máy chuyển từ giai đoạn huấn luyện sang giai đoạn suy luận.  
- Liệt kê một số trường hợp sử dụng phổ biến của AI inference trong thực tế.  
- So sánh mức độ tiêu thụ tài nguyên tính toán của hai giai đoạn training và inference.  
- Nêu cách các nền tảng đám mây (ví dụ: Cloudflare Workers AI) hỗ trợ chạy AI inference ở edge.  

## 2. Tổng quan  
Trong quá trình phát triển một mô hình trí tuệ nhân tạo, ta thường chia làm hai giai đoạn chính:  

1. **Training (huấn luyện)** – Mô hình tiếp nhận và học từ một tập dữ liệu lớn để phát hiện ra các mẫu, mối quan hệ hoặc規律 (pattern).  
2. **Inference (suy luận)** – Sau khi đã được huấn luyện, mô hình áp dụng kiến thức đã học để đưa ra dự đoán hoặc kết luận trên dữ liệu mới, chưa từng thấy.  

AI inference là “hành động” của mô hình: nó lấy đầu vào mới và tạo ra đầu ra (dự đoán, phân loại, tạo văn bản, …) mà không cần thấy các ví dụ về kết quả mong muốn trước đó.  

## 3. Kiến thức cốt lõi  

### 3.1. Định nghĩa AI Inference  
- **AI inference** là quá trình mà một mô hình máy học đã được huấn luyện sử dụng để suy ra kết quả từ dữ liệu đầu vào mới.  
- Mô hình không cần được展示 lại các cặp вход‑выход (input‑output) để thực hiện việc này; nó dựa trên kiến thức đã internalize trong quá trình training.  

### 3.2. Quy trình AI Training  
- **Đầu vào**: Tập dữ liệu có thể là có cấu trúc (structured) hoặc không cấu trúc (unstructured), có nhãn (labeled) hoặc không có nhãn (unlabeled).  
- **Hoạt động**: Mô hình được cung cấp với dữ liệu và điều chỉnh các tham số nội bộ (trong mạng neural) để giảm thiểu lỗi giữa dự đoán và nhãn thực tế (hoặc để tìm cấu trúc ẩn trong dữ liệu không có nhãn).  
- **Fine‑tuning**: Sau một vòng huấn luyện ban đầu, nhà phát triển có thể kiểm tra mô hình trên một tập validation, sửa lỗi và huấn luyện lại để cải thiện hiệu suất.  
- **Kết thúc**: Khi mô hình đạt đủ độ chính xác trên tập validation/test, huấn luyện dừng (hoặc chỉ tiếp tục khi có nhu cầu thay đổi use case).  

### 3.3. Tính toán tài nguyên (Compute Power)  
| Giai đoạn | Tính toán cần thiết | Tính chất chi phí |
|-----------|-------------------|-------------------|
| **Training** | Cực lớn – thường cần GPU/TPU chạy trong giờ, ngày,甚至 أسابيع để xử lý ملايين‑tỷ ví dụ. | Chi phí chủ yếu là một‑lần (one‑time) vì sau khi mô hình đạt độ dok desired, thường không cần huấn luyện lại trừ khi thay đổi dữ liệu hoặc mục tiêu. |
| **Inference** | Tính toán liên tục – mỗi request mới đều khiến mô hình thực hiện các phép toán forward pass. | Chi phí là **ongoing**; nếu mô hình phục vụ lượng lớn truy cập (api, ứng dụng thời gian thực) thì tổng tiêu thụ có thể vượt qua chi phí training trong dài hạn. |

> **Lưu ý**: Các kỹ thuật như Low‑Rank Adaptation (LoRA) cho phép điều chỉnh mô hình cho use case mới với chi phí tính toán thấp hơn so với huấn luyện từ đầu.  

### 3.4. Trường hợp sử dụng phổ biến của AI Inference  
- **Large Language Models (LLMs)** – Đọc và tạo ra văn bản mới dựa trên prompt chưa từng thấy.  
- **Predictive analytics** – Dự đoán xu hướng, doanh số, hoặc hiệu suất thể thao từ dữ liệu lịch sử.  
- **Email security** – Phát hiện spam, business email compromise (BEC) bằng cách phân tích nội dung và đặc điểm của thư mới.  
- **Xe tự lái** – Nhận dạng biển báo, người đi bộ, xe khác trong môi trường chưa từng встретиться.  
- **Nghiên cứu khoa học & y tế** – Trích xuất kết luận từ bộ dữ liệu genom, hình ảnh y tế, hoặc thí nghiệm.  
- **Tài chính** – Dự đoán xu hướng thị trường, rủi ro crédit, hoặc phát hiện gian lận dựa trên dữ liệu lịch sử giao dịch.  

### 3.5. Hỗ trợ chạy AI Inference ở Edge (ví dụ: Cloudflare)  
- **Cloudflare Workers AI** – Cung cấp accès đến GPU phân tánทั่ว thế giới, cho phép chạy mô hình gần với người dùng (low latency).  
- **Vectorize** – Dịch vụ tạo và lưu trữ embeddings (vector biểu diễn) dùng cho retrieval‑augmented generation hoặc tìm kiếm similarity.  
- **R2 (Object Storage)** – Lưu trữ dữ liệu training với mức phí egress = 0, giúp giảm chi phí khi cần truy cập lại tập dữ liệu để fine‑tune hoặc đánh giá.  

## 4. Ví dụ minh họa  

### Ví dụ 1: Xe tự lái nhận diện biển báo dừng  
1. **Huấn luyện**: Nhà phát triển cung cấp vài triệu hình ảnh biển báo dừng dưới nhiều góc, độ sáng, và thời tiết. Mô hình học sẽ nhận ra đặc điểm hình d팔, màu đỏ, và chữ “STOP”.  
2. **Suy luận**: Khi xe chạy trên một con đường mới mà chưa từng thấy, camera truyền frame hiện tại vào mô hình. Mô hình thực hiện forward pass và xuất ra nhãn “stop sign” với độ tin cậy cao → hệ thống phanh xe.  

### Ví dụ 2: Mô hình ngôn ngữ lớn trả lời câu hỏi  
- **Huấn luyện**: Mô hình được train trên bộ dữ liệu văn bản phong phú (sách, bài viết, code) để学习统计语言规律.  
- **Suy luận**: Người dùng đưa prompt: “Vì sao trời opět mืt vào ban đêm?”. Mô hình không cần thấy câu hỏi này trong tập huấn luyện; dựa trên cácpattern đã học, nó tạo ra câu trả lời hợp lý về việc mặt Trời điaway và rotation của Trái Đất.  

### Ví dụ 3: Phát hiện email spam  
- **Huấn luyện**: Tập dữ liệu gồm hàng ngàn email được nhãn “spam” và “not spam”. Mô hình học các từ, cấu trúc header, và đường link đặc trùng của spam.  
- **Suy luận**: Khi một email mới vào hộp thư, mô hình đưa ra xác suất spam; nếu vượt ngưỡng (ví dụ >0.9), hệ thống đưa email vào thư rác.  

## 5. Tổng kết  
- **AI inference** là giai đoạn thực thi của một mô hình đã được huấn luyện, nơi mà mô hình áp dụng kiến thức đã học để đưa ra dự đoán hoặc kết luận trên dữ liệu mới.  
- **AI training** là giai đoạn chuẩn bị, tốn lớn tài nguyên tính toán nhưng thường là một‑lần; inference là quá trình tiêu thụ tài nguyên liên tục khi mô hình được triển khai trong sản xuất.  
- Các ứng dụng thực tiễn của AI inference rất đa dạng: từ xe tự lái, LLMs, bảo mật email, tới dự đoán tài chính và nghiên cứu khoa học.  
- Các nền tảng đám mây hiện đại (ví dụ: Cloudflare Workers AI, Vectorize, R2) cung cấp hạ tầng để chạy inference ở edge, giảm latency và tối ưu chi phí.  

Nhận thức rõ ràng về hai giai đoạn này giúp nhà phát triển lựa chọn đúng chiến lược training/fine‑tuning và tối ưu hóa việc triển khai mô hình trong môi trường production.