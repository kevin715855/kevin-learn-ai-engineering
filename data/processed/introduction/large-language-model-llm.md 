# lớn ngôn ngữ mô hình (LLM)

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ có thể:

- Định nghĩa Large Language Model (LLM) và nêu đặc điểm chính của nó.  
- Giải thích cách LLM hoạt động dựa trên machine learning, deep learning và kiến trúc transformer.  
- Liệt kê các ứng dụng phổ biến của LLM trong thực tiễn.  
- Nhận biết ưu điểm cũng như hạn chế và rủi ro khi sử dụng LLM.  
- Hiểu cách các nhà phát triển có thể bắt đầu nhanh chóng xây dựng ứng dụng LLM bằng các dịch vụ đám mây hiện có.

## 2. Tổng quan

Large Language Model (LLM) là một loại mô hình trí tuệ nhân tạo (AI) được huấn luyện trên lượng dữ liệu ngôn ngữ khổng lồ (thường là hàng tỷ token) để có khả năng **nhận biết**, **hiểu** và **tạo ra** văn bản (hoặc mã) theo cách gần giống con người. Với khả năng xử lý ngôn ngữ tự nhiên, LLM đã trở thành nền tảng cho nhiều ứng dụnggenerative AI, chatbot, hỗ trợ lập trình, phân tích cảm xúc và nhiều lĩnh vực khác.

Bài học sẽ đưa bạn qua khái niệm cơ bản, nguyên lý hoạt động, ví dụ thực tiễn, ưu điểm – nhược điểm, và hướng dẫn khởi đầu cho nhà phát triển.

## 3. Kiến thức cốt lõi

### 3.1 Đặc điểm của LLM
- **Huấn luyện trên dữ liệu lớn**: Tên “large” xuất phát từ việc sử dụng bộ dữ liệu textoscaled tới hàng tá–tỷ token, thường lấy từ internet, sách, bài báo, mã nguồn…
- **Cơ sở là machine learning**: LLM là một ứng dụng của machine learning, cụ thể là deep learning (học sâu).
- **Kiến trúc neural network – transformer**: Các LLM hiện đại được xây dựng trên mạng nơ-ron nhân tạo (neural network) loại transformer, który cho phép mô hình nắm bắt **ngữ cảnh** (context) thông qua cơ chế self‑attention.
- **Fine‑tuning / Prompt‑tuning**: Sau quá trình huấn luyện chung, mô hình có thể được tinh chỉnh (fine‑tuning) cho một nhiệm vụ cụ thể hoặc được dẫn dắt bằng prompt (prompt‑tuning) để tạo ra đầu mong muốn.

### 3.2 Nguyên lý hoạt động
1. **Machine learning & deep learning**  
   - Machine learning: cho mô hình học từ dữ liệu mà không cần lập trình規則 rõ ràng.  
   - Deep learning: sử dụng nhiều lớp neuron để trích xuất đặc điểm phức tạp; học dựa trên xác suất (probabilistic analysis) của dữ liệu không có cấu trúc.

2. **Mạng nơ-ron và lớp (layers)**  
   - Mỗi lớp gồm nhiều nút (node); tín hiệu chỉ được truyền qua khi đầu ra của lớp vượt qua một ngưỡng nhất định.  
   - Cấu trúc bao gồm: input layer → một hoặc nhiều hidden layers → output layer.

3. **Transformer & self‑attention**  
   - Self‑attention cho phép mỗi từ trong một chuỗi quan hệ với tất cả các từ khác, tính toán mức độ quan tâm (attention score) để hiểu **mối liên hệ ngữ cảnh** (ví dụ: từ “it” trong câu tham chiếu đến danh từ trước đó).  
   - Nhờ đó, LLM có thể xử lý câu dài, phụ thuộc ngữ cảnh và tạo ra văn bản cohärent mà không cần quy tắc cú phápStrict.

4. **Huấn luyện và tinh chỉnh**  
   - **Pre‑training**: mô hình xem lại lượng lớn văn bản để học thống kê ngôn ngữ.  
   - **Fine‑tuning**: huấn luyện thêm trên tập dữ liệu nh mał specialized (ví dụ: bộ câu hỏi‑trả lời y tế) để nâng thành výkon trên một domaine cụ thể.  
   - **Prompt‑tuning**: điều chỉnh chỉ bằng cách thiết kế prompt (câu hỏi hoặc instruc­tion) mà không thay đổi trọng số mô hình.

### 3.3 Ứng dụng thực tiễn
| Loại ứng dụng | Mô tả | Ví dụ cụ thể |
|---------------|-------|--------------|
| Generative AI | Sinh văn bản từ prompt (bài viết, thơ, email, code…) | ChatGPT, Gemini, Llama |
| Hỗ trợ lập trình | Gợi ý, hoàn thành hoặc tạo hàm/code từ mô tả tự nhiên | GitHub Copilot, Tabnine |
| Phân tích cảm xúc | Xác định tiêu cực/trung bình/tích cảm trong bình luận,review | Công cụ monitoring thương hiệu |
| Ứng vụ khách hàng | Trả lời tự động, hướng dẫn giải quyết vấn đề | Chatbot ngân hàng, trợ giúp technischen |
| Nghiên cứu sinh học | Đánh giá chuỗi DNA, dự đoán cấu trúc protein | Mô hình chuyên dụng trong genomics |
| Tìm kiếm trực tuyến | Hiểu ý định truy vấn và trả về kết quả liên quan | Bing Chat, Google’s Search Generative Experience |
| Dịch vụ tài chính, pháp lý | Tóm tắt hợp đồng, tạo báo cáo | Các công cụ AI trong luật và kế toán |

### 3.4 Ưu điểm
- **Xử lý câu hỏi phi cấu trúc**: Không cần cú pháp lệnh cố định; có thể trả lời câu hỏi mở, mơ hồ hoặc chưa từng thấy.
- **T linh hoạt**: Một mô hình có thể được áp dụng cho nhiều nhiệm vụ chỉ qua thay đổi prompt hoặc fine‑tuning nhẹ.
- **Tốc độ sinh ra**: Đưa ra phản hồi trong giây sau khi nhận prompt.

### 3.5 Hạn chế và rủi ro
- **Phụ thuộc vào chất lượng dữ liệu huấn luyện**: Nếu dữ liệu chứa sai lệch, thông tin sai hoặc nội dung độc hại, mô hình sẽ lặp lại chúng.
- **Hallucination**: Trong trường hợp không đủ thông tin, LLM có thể “ba 꾸” (trò chơi) – tạo ra thông tin vô cơ nhưng được trình bày một cách thuyết phục.
- **Rủi ro bảo mật**:  
  - Mô hình có thể bị manipulat qua **prompt injection** để tạo ra输出 không mong muốn.  
  - Dữ liệu bí mật được đưa vào prompt có thể được lưu và sau đó tiết lộ trong các phản hồi khác (mô hình không được thiết kế như một “vault” bảo mật).
- **Tốn tài nguyên**: Huấn luyện và lưu trữ mô hình đòi hỏi bộ nhớ, GPU và chi phí điện năng lớn.

## 4. Ví dụ minh họa

### Ví dụ 1: Sử dụng LLM để viết một đoạn mã Python
**Prompt**:  
```
Viết một hàm Python tính giai thừa của một số nguyên không âm.
```

**Kết quả có thể nhận được từ Copilot/Code LLM**:  
```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n phải là số nguyên không âm")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```
*Giải thích*: Mô hình đã nắm được cấu trúc lógica của vòng lặp và xử lý trường hợp lỗi dựa trên các mẫu mã đã thấy trong bộ dữ liệu huấn luyện.

### Ví dụ 2: Trả lời câu hỏi mở về âm nhạc
**Prompt**:  
```
Các ban funk nổi tiếng nhất trong lịch sử là gì và tại sao chúng được coi là tuyệt vời?
```

**Kết quả có thể thấy** (từ một LLM như ChatGPT):  
1. **Parliament-Funkadelic** – dẫn dắt bởi George Clinton, kết hợp rock, soul và âm thanh психоделик, tạo ra groove đặc trưng.  
2. **James Brown** – thường được称为 “Cha của funk”, với nhấn mạnh mạnh mẽ vào hit và rythmic punchy.  
3. **Earth, Wind & Fire** – sebbene hơn về R&B/funk, họ mang arrival của hợp声 đẹp và phần thức của phong cách disco-funk.  
4. **The Meters** – yhtye New Orleans nổi tiếng với các riff guitarraSiнгт Thức và groove quá dễ nhịp.  

*Giải thích*: LLM đã tổng hợp kiến thức từ nhiều nguồn văn bản, tạo ra một danh sách có ý nghĩa và đưa ra lý do dựa trên đặc điểm âm nhạc và ảnh hưởng văn hóa.

### Ví dụ 3: Rủi ro rò rỉ dữ liệu qua prompt
Giả sử một người dùng dán vào chatbot một đoạn mã chứa **API key** cá nhân:  
```
sk_live_abcdef1234567890
```
Nếu mô hình được huấn luyện lại bằng cách lưu lại các đầu vào (một số dịch vụ có thể làm điều này để cải thiện chất lượng), thì key này có thể xuất hiện trong phản hồi của một người dùng khác khi họ hỏi: “Hãy cho tôi một ví dụ về key API Stripe”. Đây là một hình thức rủi ro bảo mật được nêu trong phần hạn chế.

## 5. Tổng kết

- **LLM** là mô hình AI deep learning dựa trên kiến trúc transformer, được huấn luyện trên lượng dữ liệu ngôn ngữ khổng lồ để hiểu và sinh ra văn bản hoặc mã.  
- Hoạt động nhờ **self‑attention** cho phép mô hình nắm bắt ngữ cảnh, sau đó có thể được **fine‑tuning** hoặc **prompt‑tuning** cho các tác vụ cụ thể.  
- Ứng dụng rất đa dạng: từ sinh văn bản sáng tạo (ChatGPT, Gemini), hỗ trợ lập trình (Copilot), phân tích cảm xúc, dịch vụ khách hàng, đến nghiên cứu sinh học và tìm kiếm thông tin.  
- Ưu điểm lớn nhất là khả năng trả lời câu hỏi tự nhiên, phi cấu trúc mà không cần lập trình cú pháp cứng.  
- Tuy nhiên, mô hình cũng có hạn chế: phụ thuộc vào chất lượng dữ liệu huấn luyện, dễ **hallucinate**, và có rủi ro bảo mật khi dữ liệu bí mật bị lộ qua prompt.  
- Để nhà phát triển bắt đầu, cần có **kho lưu trữ vector** (ví dụ: Cloudflare Vectorize + R2) và **nền tảng chạy mô hình** (Cloudflare Workers AI), giúp giảm chi phí egress và cho phép thử nghiệm nhanh chóng.  

Với những kiến thức trên, bạn có thể đánh giá xem LLM có phù hợp với nhu cầu dự án của mình không và biết cách tiếp cận một cách an toàn và hiệu quả.