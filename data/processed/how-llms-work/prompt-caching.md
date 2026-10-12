# Prompt Caching – Cơ chế tối ưu chi phí và độ trễ cho mô hình ngôn ngữ lớn

## 1. Mục tiêu học tập
Sau bài học này, bạn sẽ:
- Hiểu bản chất của **prompt caching** và tại sao nó lại hữu ích cho các ứng dụng AI.
- Nêu được điểm khác biệt giữa prompt caching và cách cache thông thường (conventional caching).
- Giải thích cách hoạt động của prompt caching, bao gồm việc tạo key, tra cứu cache, lưu kết quả và việc hủy bỏ (invalidation).
- Nhận diện các trường hợp sử dụng thực tiễn (ví dụ: portail tài liệu nội bộ, chatbot hỗ trợ khách hàng, chiến dịch marketing) mà prompt caching mang lại lợi ích.
- Đánh giá lợi ích và những lưu ý khi triển khai prompt caching trong hệ thống LLM.

## 2. Tổng quan
Các mô hình ngôn ngữ lớn (LLM) mạnh mẽ nhưng đắt đỏ về chi phí và có thể gây trễ khi xử lý nhiều yêu cầu trùng lặp. Mỗi token mà mô hình đọc và sinh ra đều tạo ra chi phí API và tiêu tốn thời gian tính toán. Khi người dùng gửi lại cùng một prompt (hoặc một phần lớn của prompt không thay đổi), mô hình sẽ thực hiện lại toàn bộ quy trình đó – tốn kém và giảm trải nghiệm người dùng.

**Prompt caching** là một kỹ thuật lưu trữ các phần prompt không thay đổi (hoặc toàn bộ prompt) để sau này có thể tái sử dụng kết quả thay vì phải tính toán lại từ đầu. Khi được áp dụng đúng cách, nó giúp giảm chi phí API, giảm độ trễ và tăng độ nhất quán của phản hồi trong các ứng dụng như chatbot, trợ lý ảo, hệ thống hỗ trợ khách hàng, hoặc các cổng tài liệu nội bộ.

## 3. Kiến thức cốt lõi

### 3.1 Định nghĩa
Prompt caching là quá trình **lưu trữ (cache)** kết quả hoặc trạng thái trung gian của một prompt đã được LLM xử lý, sau đó tái sử dụng khi cùng một prompt (hoặc một phần giống hệt) được gửi lại. Mục tiêu chính là tránh việc LLM phải **lặp lại** các bước mã hóa và sinh token cho những nội dung đã biết.

### 3.2 So sánh với cache thông thường (conventional caching)

| Tiêu chí | Prompt caching | Conventional caching |
|---|---|---|
| **Mục tiêu** | Tránh recomputation của LLM cho các prompt giống hệt. | Tăng tốc truy cập dữ liệu tĩnh (HTML, ảnh, kết quả DB, API). |
| **Độ tin cậy của output** | Chỉ hoạt động khi **prompt và mọi tham số** (temperature, top‑p, system prompt …) **hết sức giống**. | Deterministic: cùng input → cùng output (ví dụ: truy vấn CSDL). |
| **Hiệu năng** | Giảm số token gửi tới LLM → giảm chi phí API và latency end‑to‑end. | Giảm tải backend, giảm latency mạng. |
| **Quản lý thời gian sống** | Thông thường gắn liền với phiên bản mô hình (nếu mô hình được cập nhật hoặc huấn luyện lại, cache cần được làm mới). | Dựa trên TTL (time‑to‑live), phiên bản, hoặc invalidation thủ công khi dữ liệu gốc thay đổi. |

### 3.3 Nguyên lý hoạt động
1. **Tạo key**  
   - Khi nhận được prompt, hệ thống sinh một *cache key*.  
   - Có hai chiến lược chính:  
     - **Exact‑match caching**: key = hash của chuỗi prompt (có thể bao gồm model name, temperature, system prompt). Chỉ trùng khi mọi thành phần giống hệt.  
     - **Semantic caching**: tạo embedding vector của prompt và tìm kiếm trong vector database những prompt có nghĩa gần似. Cho phép tái sử dụng dù diễn đạt khác nhau nhưng ý nghĩa tương đồng.  
2. **Tra cứu cache**  
   - Kiểm tra xem key (hoặc embedding) đã tồn tại trong kho lưu trữ (key‑value store hoặc vector DB) chưa.  
3. **Cache hit / miss**  
   - **Hit**: trả về kết quả đã lưu ngay, không cần gọi LLM.  
   - **Miss**: gửi prompt tới LLM, nhận output, rồi lưu output (kèm embedding hoặc metadata) dưới key vừa tạo để sử dụng lần sau.  
4. **Lưu kết quả**  
   - Lưu trữ output (và tùy chọn embedding) cùng với key để các request tiếp theo có thể truy xuất nhanh.  
5. **Hủy bỏ (invalidation)**  
   - Các mục cache có thể hết hạn dựa trên TTL do máy chủ xác định, hoặc khi mô hình được cập nhật lại, hoặc khi phát hiện “content drift” (ngữ cảnh đã thay đổi gây ra kết quả cũ không còn chính xác).

### 3.4 Triển khai trong hệ thống LLM (ví dụ với LangChain)
LangChain cung cấp một lớp trung gian để tích hợp prompt caching vào chuỗi xử lý LLM mà không cần xây dựng từ zero. Quy trình chung:

```python
from langchain.cache import InMemoryCache
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI

# Bật cache bộ nhớ (có thể thay bằng Redis, SQLite, v.v.)
llm = OpenAI(temperature=0)
llm.cache = InMemoryCache()

prompt = PromptTemplate(
    input_variables=["question"],
    template="Trả lời ngắn gọn câu hỏi sau: {question}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# Lần đầu tiên – gọi LLM và lưu kết quả vào cache
answer1 = chain.run({"question": "What is artificial intelligence?"})
# Lần thứ hai – trả về từ cache, không gọi LLM nữa
answer2 = chain.run({"question": "What is artificial intelligence?"})
```

- **InMemoryCache** là một triển khai đơn giản; trong production thường thay bằng **Redis**, **Memcached**, hoặc **vector database** (đối với semantic caching).  
- LangChain cũng cho phép bật/tắt cache qua `llm.cache = False` khi cần kiểm tra hoặc debug.

### 3.5 Trường hợp sử dụng típ
| Trường hợp | Vì sao prompt caching hiệu quả |
|---|---|
| **Cổng tài liệu nội bộ** | Nhân viên thường hỏi về cùng một quy trình, chính sách. Cache trả lời ngay lập tức, giảm lượng truy vấn LLM. |
| **Chatbot hỗ trợ khách hàng** | Câu hỏi thường gặp (giá trịDiscount, trạng thái đơn hàng) được trả lời từ cache → phản hồi nhanh, chi phí thấp. |
| **Chiến dịch marketing tự động** | Nhiều người dùng hỏi cùng thông tin sản phẩm; cache giảm số lượng API call trong giờ cao điểm. |
| **Hệ thống RAG (Retrieval‑Augmented Generation)** | Phần “context” được truy xuất từ vector store thường không thay đổi trong một phiên làm việc; caching phần context + prompt giúp sinh câu trả lời nhanh hơn. |
| **Công cụ hỗ trợ viết code** | Prompt chứa hướng dẫn_style hoặc thư viện thường dùng được lưu lại, giúp đề xuất code nhanh hơn. |

### 3.6 Lợi ích nổi bật
- **Tiết kiệm chi phí API** – mỗi cache hit意味着 không cần gửi token tới LLM, giảm trực tiếp chi phí sử dụng.  
- **Giảm độ trễ** – trả về từ cache thường trong vòng vài miligiây, trong khi gọi LLM có thể mất vài trăm miligiây tới vài giây.  
- **Tái sử dụng tài nguyên** – bộ tính toán được dành cho các prompt mới, phức tạp thay vì lãng phí cho những nội dung lặp lại.  
- **Khả năng mở rộng** – khi lưu lượng tăng, tỷ lệ cache hit thường tăng, giúp hệ thống ổn định mà không cần tăng cấp thêm phần cứng đáng kể.  
- **Đáp ứng nhất quán** – cùng prompt → cùng output, nâng cao độ tin cậy và trải nghiệm người dùng.  
- **Giảm tải máy chủ** – ít request đến LLM 의미 có ít hơn các tính toán nặng trên GPU/CPU.  

### 3.7 Lưu ý và thách thức
- **Yêu cầu độ đồng nhất** – chỉ hoạt động khi prompt và toàn bộ bộ tham số (temperature, top‑p, seed…) **hết sức giống**; bất kỳ thay đổi nào đều gây miss.  
- **Dữ liệu động / ngữ cảnh thay đổi** – nếu prompt phụ thuộc vào thông tin thời gian thực (ví dụ: giá cổ phiếu, thời tiết), cache dễ trở nên **lỗi thời** và cung cấp thông tin không chính xác.  
- **Quản lý cache** – cần thiết lập chính sách TTL, giới hạn bộ nhớ, và chiến lược invalidation để tránh tràn bộ nhớ hoặc cung cấp kết quả cũ.  
- **Trường hợp edge** – попыт việc cache một phần prompt (prefix caching) hoặc sử dụng semantic caching tăng độ phức tạp của hệ thống và có thể dẫn đến lỗi nếu không được kiểm soát kỹ.  
- **Riêng tư và bảo mật** – lưu trữ prompt hoặc output có thể chứa thông tin nhạy cảm; cần mã hóa và kiểm soát truy cập vào bộ cache.  

### 3.8 Tóm tắt
Prompt caching là một kỹ thuật **lưu trữ kết quả hoặc trạng thái trung gian của prompt** để tránh phải xử lý lại những phần không thay đổi khi gọi LLM lặp lại. Nó khác với cache thông thường ở mục tiêu (tránh recomputation LLM thay vì truy xuất dữ liệu tĩnh), đòi hỏi độ đồng nhất Strict, và thường được gán liền với phiên bản mô hình. Khi triển khai đúng cách – thông qua exact‑match hoặc semantic caching, kết hợp với các kho lưu trữ như Redis hoặc vector database – prompt caching giúp giảm đáng kể chi phí API, giảm độ trải, tăng đáp ứng nhất quán, và mở rộng khả năng chịu tải của các ứng dụng AI như chatbot, cổng tài liệu, hệ thống hỗ trợ khách hàng. Tuy nhiên, cần quản lý kỹ lưỡng các vấn đề về dữ liệu động, invalidation cache, và bảo mật để tránh những phản hồi lỗi thời hoặc rò rò rủi ro.

--- 

**Tài liệu tham khảo** (trích từ bài gốc):
- Scaling Laws for Neural Language Models (Kaplan et al., 2020)  
- Prompt Cache: Modular Attention Reuse for Low‑Latency Inference (Gim et al., 2024)  
- OpenAI Prompt Caching documentation  
- Các nghiên cứu gần đây về auditing, leakage và продвинутых кеширований prompt.