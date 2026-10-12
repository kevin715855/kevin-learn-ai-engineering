# Retrieval-Augmented Generation (RAG) – Cải thiện mô hình ngôn ngữ lớn bằng truy xuất dữ liệu

## 1. Mục tiêu học tập
Sau bài học này, bạn sẽ có thể:
- Giải thích概念 Retrieval-Augmented Generation (RAG) và tại sao nó được phát triển.
- Liệt kê các thách thức phổ biến của Large Language Model (LLM) mà RAG giải quyết.
- Nêu بوضوح lợi ích của RAG về chi phí, tính cập nhật, độ tin cậy và khả năng kiểm soát của nhà phát triển.
- Mô tả quy trình làm việc của RAG từ tạo dữ liệu ngoại vi đến việc cập nhật dữ liệu.
- Phân biệt RAG với semantic search và nêu情况 nào nên dùng từng phương pháp.
- Liệt kê các dịch vụ AWS hỗ trợ xây dựng hệ thống RAG (Amazon Bedrock, Amazon Kendra, Amazon SageMaker JumpStart).

## 2. Tổng quan
Large Language Models (LLM) được huấn luyện trên bộ dữ liệu tĩnh và có thể sinh ra câu trả lời chưa chính xác, lỗi thời hoặc dựa trên nguồn không uy tín khi được đặt câu hỏi trong bối cảnh cụ thể. Điều này làm giảm độ tin cậy của các ứng dụng AI sinh tạo như chatbot. Retrieval-Augmented Generation (RAG) ra đời để mở rộng khả năng của LLM bằng cách cho phép mô hình truy xuất thông tin từ một kiến thức bên ngoài (external knowledge base) trước khi sinh ra câu trả lời. Vì không cần huấn luyện lại mô hình, RAG là giải pháp tiết kiệm chi phí và linh hoạt cho việc đưa kiến thức tổ chức hoặc trường dữ liệu mới vào LLM.

## 3. Kiến thức cốt lõi

### 3.1 Định nghĩa RAG
RAG là quá trình tối ưu đầu ra của một LLM bằng cách **truy xuất** (retrieve) thông tin từ một nguồn kiến thức bên ngoài trước khi mô hình sinh ra câu trả lời. Kết quả là LLM sinh ra phản hồi dựa trên cả kiến thức đã học trong quá trình huấn luyện và kiến thức mới được cung cấp qua truy xuất.

### 3.2 Tại sao LLM cần được補強?
LLM có một số hạn chế phổ biến:
- **Thông tin sai** khi mô hình không biết câu trả lời nhưng vẫn tự tin đưa ra một câu trả lời.
- **Thông tin lỗi thời** vì dữ liệu huấn luyện là tĩnh và có một ngày cắt-off.
- **Nguồn không uy tín** khi mô hình lấy thông tin từ tài liệu không được kiểm chứng.
- **Nhầm lẫn về thuật ngữ** khi cùng một từ có nghĩa khác nhau trong các nguồn dữ liệu huấn luyện khác nhau.

RAG giải quyết những vấn đề trên bằng cách đưa LLM đến một **kho tri thức xác thực** (authoritative knowledge base) mà tổ chức kiểm soát.

### 3.3 Quy trình làm việc của RAG
1. **Tạo dữ liệu bên ngoài (External data)**  
   - Dữ liệu này không thuộc bộ dữ liệu huấn luyện ban đầu của LLM.  
   - Có thể lấy từ API, cơ sở dữ liệu, kho tài liệu, v.v.  
   - Định dạng có thể là file, bản ghi CSDL, văn bản dài.  
   - Dữ liệu thường được **vector hoá** bằng embedding language model và lưu trữ trong **vector database** để dễ dàng tìm kiếm tương tự.

2. **Truy xuất thông tin liên quan (Retrieve relevant information)**  
   - Câu hỏi của người dùng cũng được chuyển thành vector (embedding).  
   - Thực hiện phépso sánh vector trong vector database để tìm các đoạn văn bản có độ tương đồng cao nhất.  
   - Ví dụ: trong một chatbot HR, câu hỏi “How much annual leave do I have?” sẽ dẫn đến việc truy xuất tài liệu chính sách nghỉ phép và bản ghi nghỉ phép cá nhân của nhân viên.

3. **Cải thiện prompt (Augment the LLM prompt)**  
   - Đoạn văn bản được truy xuất được chèn vào prompt gốc (user query) bằng kỹ thuật prompt engineering.  
   - Prompt mới chứa cả câu hỏi và bối cảnh znalice, cho phép LLM sinh ra câu trả lời chính xác và có thể trích dẫn nguồn.

4. **Cập nhật dữ liệu bên ngoài (Update external data)**  
   - Để kiến thức luôn mới, dữ liệu bên ngoài cần được cập nhật định kỳ (batch) hoặc gần thực thời (real‑time).  
   - Mỗi lần cập nhật, embedding được tạo lại và lưu trữ trong vector database.

### 3.4 Ưu điểm của RAG
| Lợi ích | Mô tả |
|---------|-------|
| **Triển khai hiệu quả về chi phí** | Không cần huấn luyện lại foundation model; chỉ cần kết nối với nguồn kiến thức bên ngoài. |
| **Thông tin cập nhật** | Datasource có thể là feed tin tức, mạng xã hội, hoặc hệ thống nội bộ thường xuyên được làm mới. |
| **Tăng độ tin cậy của người dùng** | Kết quả có thể đi kèm trích dẫn hoặc link tới nguồn gốc, người dùng có thể tự kiểm tra. |
| **Kiểm soát tốt hơn cho nhà phát triển** | Được quyền chọn nguồn dữ liệu, giới hạn truy cập theo quyền限, sửa sai nguồn khi phát hiện lỗi. |

### 3.5 RAG vs Semantic Search
- **Semantic search** là một công cụ tìm kiếm dựa trên ý nghĩa (vector similarity) mà không sinh ra văn bản mới. Nó thích hợp khi cần truy xuất các đoạn văn bản liên quan nhất từ một kho kiến thức lớn.  
- Trong RAG, semantic search thường được dùng ở bước **Retrieve relevant information** để lấy các đoạn văn bản có liên quan cao nhất.  
- Khi muốn **chỉ lấy đoạn văn bản** (không sinh trả lời), dùng semantic search đơn lẻ; khi cần **sinh trả lời dựa trên nguồn đã truy xuất**, dùng RAG.  
- Semantic search cũng giúp giảmภาร chuẩn bị dữ liệu (chunking, embedding) vì nhiều dịch vụ đã cung cấp pipeline hoàn chỉnh.

### 3.6 Hỗ trợ từ AWS
- **Amazon Bedrock** – dịch vụ toàn quản lý cung cấp các foundation model và **Knowledge Bases** để kết nối FM với nguồn dữ liệu của bạn. Quy trình vector hoá, truy xuất và sinh phản hồi được tự động hoá.  
- **Amazon Kendra** – công cụ tìm kiếm doanh nghiệp cao độ chính xác, cung cấp **Retrieve API** có thể trả về tới 100 đoạn semantic‑relevant (mỗi đoạn ≤200 token) và hỗ trợ nhiều định dạng tài liệu (HTML, Word, PDF, Excel, …).  
- **Amazon SageMaker JumpStart** – kho chứa các notebook và ví dụ mã giúp triển khai RAG nhanh chóng bằng cách dùng các model đã được training sẵn.  

## 4. Ví dụ minh họa

### 4.1 Trường hợp sử dụng: Chatbot hỗ trợ chính sách nhân sự
**Yêu cầu:** Nhân viên hỏi “How many days of annual leave do I have left for this year?”

**Các bước thực hiện RAG:**
1. **Tạo dữ liệu bên ngoài:**  
   - Kho tài liệu bao gồm:  
     - `annual_leave_policy.pdf` (chính sách nghỉ phép năm)  
     - `employee_leave_records.csv` (bản ghi nghỉ phép cá nhân)  
   - Mỗi tài liệu được biến thành vector bằng mô hình embedding (ví dụ: Titan Embeddings) và lưu trong Amazon Kendra vector index.

2. **Truy xuất thông tin liên quan:**  
   - Câu hỏi được chuyển thành vector → truy xuất Kendra → trả về 2 đoạn:  
     - Đoạn 1: “Mỗi nhân viên có rätt 20 ngày nghỉ phép mỗi năm, được cộng dồn từ ngày 1/1.”  
     - Đoạn 2: “Mã nhân viên 12345 đã sử dụng 8 ngày nghỉ phép tới nay.”

3. **Cải thiện prompt:**  
   ```text
   Bạn là một trợ lý HR. Dựa vào thông tin sau:
   - Mỗi nhân viên có 20 ngày nghỉ phép mỗi năm.
   - Nhân viên mã 12345 đã sử dụng 8 ngày nghỉ phép.
   
   Hãy trả lời: Nhân viên 12345 còn bao ngày nghỉ phép năm nay?
   ```
   LLM (ví dụ: Claude 2 trên Bedrock) sinh ra:  
   > “Nhân viên mã 12345 còn 12 ngày nghỉ phép cho năm này.”  
   Kèm theo, hệ thống có thể đính kèm link tới `annual_leave_policy.pdf` và `employee_leave_records.csv` để người dùng xác thực.

4. **Cập nhật dữ liệu bên ngoài:**  
   - Mỗi tối, hệ thống ETL tự động lấy file `employee_leave_records.csv` mới nhất từ HRIS, tạo embedding mới và cập nhật chỉ mục Kendra.  
   - Chính sách nghỉ phép nếu thay đổi cũng được tải lên và re‑embed.

### 4.2 So sánh với Semantic Search chỉ
Nếu chỉ dùng semantic search và không có bước sinh trả lời, hệ thống sẽ trả về hai đoạn văn trên mà không tổng hợp chúng thành một câu trả lời tự nhiên. Người dùng sẽ phải đọc và tự tính số ngày còn lại. RAG giảm thiểu tác động này bằng việc cho LLM thực hiện việc tổng hợp và sinh câu trả lời cuối cùng.

## 5. Tổng kết
- RAG cho phép LLM truy xuất kiến thức bên ngoài đáng tin cậy trước khi sinh ra câu trả lời, тем самым khắc phục các lỗi của LLM như thông tin sai, lỗi thời và thiếu nguồn.  
- Quy trình gồm 4 bước chính: tạo dữ liệu ngoài, truy xuất sémantic, tăng cường prompt, và cập nhật dữ liệu định kỳ.  
- Lợi ích nổi bật là chi phí triển khai thấp, thông tin luôn mới, tăng độ tin cậy của người dùng và cho nhà phát triển kiểm soát linh hoạt nguồn dữ liệu.  
- Semantic search thường được sử dụng như một thành phần trong bước truy xuất của RAG; khi chỉ cần lấy tài liệu mà không cần sinh trả lời, dùng semantic search đơn lẻ.  
- AWS cung cấp đầy đủ các công cụ cần thiết: Amazon Bedrock (Knowledge Bases), Amazon Kendra (tìm kiếm sémantic cấp doanh nghiệp), và Amazon SageMaker JumpStart (mẫu code và notebook) để triển khai RAG một cách nhanh chóng và bảo mật.  

Những điểm trên là nền tảng để bạn bắt đầu xây dựng các ứng dụng AI sinh tạo đáng tin cậy và chuyên nghiệp trên nền tảng AWS. Hãy áp dụng quy trình RAG vào dự án chatbot, trợ lý ảo hoặc hệ thống hỗ trợ quyết định của organização để đạt được chất lượng phản hồi tốt nhất.