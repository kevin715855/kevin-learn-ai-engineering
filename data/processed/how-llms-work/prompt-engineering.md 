# Prompt Engineering: Nguyên tắc và ứng dụng trong Generative AI  

## 1. Mục tiêu học tập  

Sau khi đọc bài học này, bạn sẽ能够:  

- Giải thích **prompt engineering** là gì và vai trò của nó trong các hệ thống AI sinh tạo.  
- Định nghĩa **prompt** và nêu điểm khác biệt giữa prompt tự nhiên và prompt được thiết kế kỹ lưỡng.  
- Nêu tại sao prompt engineering quan trọng đối với nhà phát triển, trải nghiệm người dùng và khả năng mở rộng của ứng dụng AI.  
- Liệt kê một số **use case** tiêu biểu (chuyên môn, suy nghĩ phản biện, sáng tạo).  
- mô tả các **kỹ thuật** phổ biến của prompt engineering (chain‑of‑thought, tree‑of‑thought, maieutic, complexity‑based, generated knowledge, least‑to‑most, self‑refine, directional‑stimulus).  
- Áp dụng các **best practice** khi viết prompt (mô tả rõ ràng, cung cấp bối cảnh đủ, cân bằng độ phức tạp, thử nghiệm và cải tiến).  
- Nhận biết cách AWS hỗ trợ việc xây dựng và triển khai các mô hình generative AI (Amazon CodeWhisperer, Bedrock, SageMaker JumpStart, SageMaker).  

## 2. Tổng quan  

Prompt engineering là quá trình thiết kế và điều chỉnh các đoạn văn bản tự nhiên (prompt) để hướng dẫn mô hình ngôn ngữ lớn (LLM) – thành phần lõi của generative AI – tạo ra đầu ra mong muốn. Mặc dù LLM có khả năng tổng quát cao, chúng vẫn cần hướng dẫn cụ thể để tạo ra nội dung chính xác, liên quan và phù hợp với mục đích ứng dụng. Việc thiết kế prompt hiệu quả giúp kiểm soát hành vi AI, cải thiện trải nghiệm người dùng và mở rộng khả năng tái sử dụng trên nhiều nghiệp vụ.  

Bài học này tổng hợp các khái niệm cơ bản, lợi ích, trường hợp ứng dụng, kỹ thuật chính và thực tiễn tốt nhất mà AWS đề cập trong trang “What is Prompt Engineering?”.  

## 3. Kiến thức cốt lõi  

### 3.1 Prompt là gì?  

- **Prompt** là một chuỗi ký tự bằng ngôn ngữ tự nhiên (ví dụ: câu hoặc đoạn văn) được gửi tới mô hình generative AI để yêu cầu thực hiện một nhiệm vụ cụ thể.  
- Mô hình dựa trên kiến thức đã được huấn luyện trước trên lượng dữ liệu khổng lồ để **dự đoán** đầu ra tốt nhất phù hợp với prompt đó.  
- Một prompt đơn giản (một từ) vẫn có thể kích hoạt mô hình tạo ra phản hồi chi tiết, nhưng chất lượng của đầu ra phụ thuộc sterk vào mức độ rõ ràng và bối cảnh mà prompt cung cấp.  

### 3.2 Prompt engineering là gì?  

- Quá trình **lựa chọn, kết hợp và tinh chỉnh** các định dạng, từ ngữ, biểu tượng và cấu trúc trong prompt để hướng dẫn AI sinh ra output mong muốn.  
- Yêu cầu sự sáng tạo và thử nghiệm lặp đi lặp lại (trial‑and‑error) để xây dựng một “thư viện prompt” mà ứng dụng có thể tái sử dụng.  
- Kết quả là: AI hiểu rõ ý định của người dùng, tạo ra câu trả lời chính xác và phù hợp với định dạng mong đợi.  

### 3.3 Tại sao prompt engineering quan trọng?  

| Lợi ích | Mô tả chi tiết |
|--------|----------------|
| **Kiểm soát tốt hơn cho nhà phát triển** | Prompt thiết lập bối cảnh và ý định, giúp AI tập trung vào yêu cầu, tránh sinh ra nội dung không mong muốn hoặcoutside domain. |
| **Cải thiện trải nghiệm người dùng** | Người dùng nhận được câu trả lời coherent và liên quan ngay từ lần thử đầu, giảm nhu cầu thử nghiệmMultiple attempts. Giảm tác động của bias trong dữ liệu huấn luyện. |
| **Tăng tính linh hoạt và mở rộng** | Các prompt có thể được trừu tượng hóa (domain‑neutral) và tái sử dụng trong nhiều bộ phận, quy trình hoặc sản phẩm, giúp mở rộng đầu tư AI mà không cần xây dựng mô hình mới từ đầu. |

### 3.4 Use case tiêu biểu  

1. **Chuyên môn (Subject‑matter expertise)** – Yêu cầu AI trích dẫn nguồn chính xác và đưa ra câu trả lời phù hợp với lĩnh vực (y học, pháp luật, kỹ thuật).  
2. **Suy nghĩ phản biện (Critical thinking)** – AI liệt kê các lựa chọn, đánh giá tiêu chí và đưa ra đề xuất lý luận.  
3. **Sáng tạo (Creativity)** – AI giúp sinh ra ý tưởng nhân vật, bối cảnh, bản phối màu, hoặc đoạn nhạc dựa trên hướng dẫn ngắn gọn.  

### 3.5 Kỹ thuật prompt engineering phổ biến  

| Kỹ thuật | Nguyên tắc chính | Ví dụ ngắn |
|----------|------------------|------------|
| **Chain‑of‑thought (CoT)** | Chia vấn đề thành các bước logic liên tiếp, mô hình suy nghĩ từng bước trước khi đưa ra câu trả lời cuối. | Giải phương trình 2x + 3 = 11 → “Trừ 3 từ hai vế” → “Chia cho 2”. |
| **Tree‑of‑thought (ToT)** | Mở rộng CoT bằng việc sinh ra nhiều bước tiếp theo có thể, sau đó thực hiện tìm kiếm trên cây để chọn nghiệm tốt nhất. | Ảnh hưởng của biến khí hậu → liệt kê tác động môi trường và xã hội, sau đó chi tiết từng nhánh. |
| **Maieutic prompting** | Mô hình сначала trả lời câu hỏi, sau đó được yêu cầu giải thích từng phần của câu trả lời; các giải thích mâu thuẫn được cắt bớt. | “Tại sao trời xanh?” → mô tả tán cực của ánh sáng xanh → giải thích tại sao xanh tán cực hơn. |
| **Complexity‑based prompting** | Thực hiện nhiều lần CoT, chọn những chuỗi suy nghĩ dài nhất, rồi lấy kết quả phổ biến nhất. | Giải bài toán phức tạp với nhiều bước tính toán. |
| **Generated knowledge prompting** | Mô hình trước tiên sinh ra các사실 liên quan cần biết, sau đó sử dụng chúng để hoàn thành yêu cầu chính. | Viết bài về Auswirkungen của deforestation → trước tiên liệtizzare “giảm sinh học”, “gây thay đổi khí hậu”. |
| **Least‑to‑most prompting** | Mô hình liệt kê các sub‑problem từ dễ tới khó, sau đó giải quyết chúng theo thứ tự, dùng kết quả của sub‑problem trước để hỗ trợ sub‑problem sau. | Giải phương trình bậc nhất bằng cách chia thành “trừ hằng số”, “chia cho hệ số”. |
| **Self‑refine prompting** | Mô hình sinh ra câu trả lời, tự đánh giá (critique) và cải thiện dựa trên phản hồi của mình, lặp lại cho tới khi đạt tiêu chí dừng. | Viết một bài ngắn, phát hiện thiếu ví dụ, bổ sung ví dụ, lặp lại. |
| **Directional‑stimulus prompting** | Thêm từ khóa hoặc cues cụ thể vào prompt để hướng модель về输出 mong muốn. | “Viết một bài thơ về tình yêu chứa từ ‘heart’, ‘passion’, ‘eternal’.” |

### 3.6 Best practice khi thiết kế prompt  

1. **Unambiguous prompts** – Mô tả rõ ràng output mong muốn (tóm tắt, danh sách, bảng, …). Tránh двусмысленность như “mô tả” khi thực sự cần “tóm tắt”.  
2. **Adequate context** – Cung cấp đủ thông tin về vai trò, đối tượng, định dạng đầu ra (số lượng mục, kiểu bảng, …). Ví dụ: “Cho tôi bảng top 10 phim của thập niên 1990, gồm cột Ten phim, Năm phát hành, Doanh thu”.  
3. **Balance between targeted information and desired output** – Không quá ngắn (thiếu bối cảnh) và không quá dài (làm nhầm lẫn model). Sử dụng ngôn ngữ đơn giản, loại bỏ từ thừa.  
4. **Experiment and refine** – Thử nghiệm nhiều biến體prompt, đo lường chất lượng output (độ chính xác, liên quan, định dạng), lặp lại cho tới khi ổn định. Không có quy tắc cứng, vì vậy linh hoạt và khả năng thích ứng là then chốt.  

### 3.7 Hỗ trợ của AWS cho Generative AI và Prompt Engineering  

- **Amazon CodeWhisperer** – Gợi ý mã nguồn real‑time dựa trên bình luận và code hiện có, giúp developer viết prompt hoặc tích hợp model vào ứng dụng.  
- **Amazon Bedrock** – Truy cập các mô hình ngôn ngữ lớn qua API mà không cần quản lý hạ tầng; thích hợp để triển khai các prompt engineering pipeline.  
- **Amazon SageMaker JumpStart** – Kho chứa mô hình nguồn mở (OpenLLaMA, RedPajama, MPT‑7B, FLAN‑T5, GPT‑NeoX‑20B, BLOOM…) để试验 và so sánh hiệu quả của các kỹ thuật prompt.  
- **Amazon SageMaker** – Cung cấp môi trường quản lý để huấn luyện, tinh chỉnh và triển khai mô hình tự construir nếu cần tự đào tạo model riêng cho domain cụ thể.  

Bằng cách kết hợp các dịch vụ trên, các团队 có thể nhanh chóng dựng dựng, kiểm tra và mở rộng các ứng dụng generative AI dựa trên nền tảng prompt engineering vững chắc.  

## 4. Ví dụ minh họa  

### Ví dụ 1: Prompt được thiết kế cho chatbot bán hàng  

**Yêu cầu của người dùng (raw):**  
> “Where to purchase a shirt.”  

**Prompt được kỹ sư thiết kế (engineered prompt):**  
> “Bạn là một trợ lý bán hàng cho một công ty may mặc. Một người dùng đang sống ở Alabama, Hoa Kỳ đang hỏi bạn nơi mua áo sơ mi. Hãy trả lời bằng ba vị trí cửa hàng gần nhất hiện có hàng áo sơ mi trong kho.”  

**Kết quả mong muốn từ mô hình:**  
- Danh sách ba cửa hàng (tên, địa chỉ, khoảng cách) hiện có áo sơ mi, mỗi mục được định dạng ngắn gọn, dễ đọc.  

**Lý do úč dụng:**  
- Prompt cung cấp **vai trò** (tư vấn bán hàng), **bối cảnh địa lý** (Alabama, Mỹ) và **định dạng output** (danh sách ba cửa hàng gần nhất). Điều này giúp model tập trung vào việc truy xuất thông tin cửa hàng thay vì trả lời chung chung về “áo sơ mi”.  

### Ví dụ 2: Ứng dụng Chain‑of‑thought để giải toán  

**Prompt:**  
> “Giải phương trình 3x − 7 = 20. Hãy montrant mỗi bước suy nghĩ rõ ràng.”  

**Quy trình suy nghích của mô hình (CoT):**  
1. Cộng 7 vào cả hai vế → 3x = 27  
2. Chia cả hai vế cho 3 → x = 9  

**Output cuối:**  
> x = 9  

**Lý do:** Bằng cách buộc model suy nghĩ từng bước, ta giảm khả năng mắc lỗi cálculo và có thể kiểm tra từng bước trung gian.  

## 5. Tổng kết  

- **Prompt engineering** là phương pháp thiết kế và tinh chỉnh đoạn văn bản tự nhiên để hướng dẫn mô hình generative AI tạo ra đầu ra phù hợp, chính xác và có định dạng mong muốn.  
- **Prompt** là câu lệnh gửi tới AI; chất lượng của output phụ thuộc mức độ rõ ràng, bối cảnh và cấu trúc của prompt.  
- Việc áp dụng prompt engineering mang lại **kiểm soát tốt hơn** cho nhà phát triển, **cải thiện trải nghiệm người dùng** và **tăng tính linh hoạt** cho hệ thống AI.  
- Các **use case** chính bao gồm hỗ trợ chuyên môn, suy nghĩ phản biện và tạo ra ý tưởng sáng tạo.  
- Các **kỹ thuật** phổ biến (chain‑of‑thought, tree‑of‑thought, maieutic, complexity‑based, generated knowledge, least‑to‑most, self‑refine, directional‑stimulus) cung cấp các công cụ để phân tích vấn đề, sinh kiến thức trung gian và tối ưu kết quả đầu ra.  
- **Best practice** bao gồm việc viết prompt không mâu thuẫn, cung cấp đủ bối cảnh, cân bằng độ ngắn‑dài, và thực hiện thử nghiệm lặp lại để tối ưu.  
- **AWS** cung cấp một bộ công cụ toàn diện (CodeWhisperer, Bedrock, SageMaker JumpStart, SageMaker) để phát triển, thử nghiệm và triển khai các mô hình generative AI kèm theo các chiến lược prompt engineering hiệu quả.  

Với những kiến thức trên, bạn có thể bắt đầu xây dựng các prompt mạnh mẽ, tối ưu hoá tương tác giữa người dùng và AI, và khai thác tối đa tiềm năng của generative AI trên nền tảng AWS.