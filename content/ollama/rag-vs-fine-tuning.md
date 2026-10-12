# RAG vs Fine‑tuning: Khi nào nên dùng mỗi phương pháp?

## 1. Mục tiêu học tập
Sau bài học này, bạn sẽ able to:
- Giải thích nguyên lý cơ bản của Retrieval‑Augmented Generation (RAG) và fine‑tuning.
- Liệt kê lợi ích và thách thức chính của mỗi cách tiếp cận.
- So sánh RAG và fine‑tuning theo tiêu chí như độ mới dữ liệu, độ phức tạp triển khai, hiệu suất, khả năng mở rộng và bảo mật.
- Xác định trường hợp sử dụng thích hợp cho RAG, fine‑tuning hoặc kết hợp hai phương pháp (hybrid).
- Áp dụng những yếu tố quyết định (chi phí, tần suất thay đổi dữ liệu, yêu cầu bảo mật, nguồn lực kỹ thuật) để chọn phương pháp phù hợp với dự án AI của mình.

## 2. Tổng quan
Các mô hình ngôn ngữ lớn (LLM) được huấn luyện trước trên bộ dữ liệuทั่วไป và có kiến thức “đóng băng” tại thời điểm huấn luyện. Khi cần trả lời câu hỏi về thông tin mới hoặc chuyên sâu, hai chiến lược phổ biến được ra mắt:
- **RAG (Retrieval‑Augmented Generation)**: kết nối LLM với một nguồn kiến thức ngoài (cơ sở dữ liệu, kho tài liệu) để truy xuất dữ liệu liên quan tại thời điểm truy vấn và cung cấp nó làm bối cảnh cho mô hình.
- **Fine‑tuning**: tiếp tục huấn luyện LLM trên một bộ dữ liệu đặc thù để điều chỉnh trọng số nội bộ,ทำให้ mô hình “nhớ” kiến thức chuyên ngành.

Cả hai đều có mục tiêu nâng cao chất lượng đầu ra, nhưng cách đạt được khác nhau và dẫn đến các trade‑off khác nhau. Bài học này sẽ giúp bạn hiểu khi nào nên ưu tiên mỗi phương pháp và khi nào kết hợp chúng sẽ mang lại kết quả tốt nhất.

## 3. Kiến thức cốt lõi

### 3.1 Retrieval‑Augmented Generation (RAG)

**Cơ chế hoạt động**
1. Nhận truy vấn từ người dùng.  
2. Tìm kiếm trong kho kiến thức (document store, vector database) các đoạn văn bản có độ tương đồng cao với truy vấn (thường qua embedding + similarity search).  
3. Ghép các đoạn được truy xuất với truy vấn gốc thành một “augmented prompt”.  
4. Đaugmented prompt được đưa vào LLM để sinh câu trả lời.

**Lợi ích**
- Truy cập thông tin mới nhất mà không cần huấn luyện lại mô hình.  
- Giảm hallucinations vì câu trả lời được căn cứ vào dữ liệu thực tế.  
- Bảo mật và kiểm soát truy cập tốt hơn vì dữ liệu riêng vẫn còn trong kho dưới quy định của tổ chức.  
- Khả năng truy vet (traceability): mỗi câu trả lời có thể liên kết lại với tài liệu nguồn.

**Thách thức**
- Xây dựng và bảo trì cơ sở hạ tầng truy xuất (pipeline ingest, embedding, indexing, vector search).  
- Cần cân bằng giữa độ chính xác truy xuất và độ trễ (latency).  
- Giới hạn kích thước prompt (context window) của LLM buộc phải chọn lọc và chunk thông tin liên quan.

**Ví dụ minh họa**
- Chatbot nội bộ trả lời câu hỏi về chính sách HR: khi người dùng hỏi “Cách đặt lại mật khẩu VPN?”, RAG tìm trong wiki nội bộ đoạn hướng dẫn cụ thể, ghép vào prompt và LLM trả lời bước‑by‑step phù hợp với công ty.

### 3.2 Fine‑tuning

**Cơ chế hoạt động**
- Chuẩn bị bộ dữ liệu có nhãn (prompt‑response) thuộc lĩnh vực mục tiêu.  
- Huấn luyện lại (continue training) LLM trên bộ dữ liệu này, điều chỉnh trọng số (hoặc một phần trọng số qua técnicas PEFT như LoRA).  
- Mô hình sau fine‑tuning có thể tạo ra đầu tuân theo phong cách, thuật ngữ và định dạng của domain.

**Lợi ích**
- Độ chínhสูca và sự phù hợp ngữ cảnh cao vì kiến thức đã được “nhúng” vào trọng số.  
- Tiết kiệm tài nguyên khi một mô hình nhỏ sau fine‑tuning có thể cạnh tranh với mô hình lớn hơn về hiệu suất trên nhiệm vụ chuyên biệt.  
- Kiểm soát phong cách, tone và định dạng đầu ra (quan trọng cho ứng dụng như soạn thảo pháp lý, báo cáo y tế).

**Thách thức**
- Cần dữ liệu có nhãn chất lượng lớn và lực lượng tính toán (GPU/TPU) để huấn luyện.  
- Nguy cơ over‑fit: mô hình quá chuyên biệt và kém hiệu lực trên các nhiệm vụ ngoài domain.  
- Khó cập nhật kiến thức mới: phải thu thập dữ liệu mới và huấn luyện lại.  
- Không có nguồn gốc minh bạch (không thể trace lại câu trả lời tới tài liệu cụ thể).

**Ví dụ minh họa**
- Mô hình trả lời y tế được fine‑tuning trên bản ghi bệnh án và sách giáo khoa y. Khi bác sĩ hỏi “Triệu chứng đau đầu bắt đầu đột ngột, buồn nén và giảm lực một bên?”, mô hình sinh ra gợi ý chẩn đoán „cơ ممن tăng huyết áp” bằng ngôn ngữ y và định dạng ghi chú lâm sàng.

### 3.3 So sánh nhanh RAG vs fine‑tuning

| Tiêu chí | RAG | Fine‑tuning |
|----------|-----|--------------|
| **Độ mới dữ liệu** | Lấy từ nguồn ngoài lúc truy vấn → luôn cập nhật | Giới hạn đến bộ dữ liệu huấn luyện lần cuối |
| **Phức tạp triển khai** | Xây dựng pipeline ingest, vector DB, retrieval | Thu thập & gán nhãn dữ liệu, huấn luyện mô hình (cần GPU) |
| **Chi phí** | Chi phí đầu tư thấp, chi phí liên tục cho retrieval | Chi phí đầu tư cao (huấn luyện), chi phí phục vụ thấp |
| **Hiệu suất** | Cải thiện độ trung thực (giảm hallucination) | Độ chính xác và phong cách chuyên biệt cao hơn trên nhiệm vụ hẹp |
| **Khả mở rộng** | Dễ dàng thêm tài nguyên mới mà không retrain | Cần retrain khi thay đổi kiến thức hoặc mở rộng domain |
| **Bảo mật & tư liệu** | Dữ liệu riêng vẫn ở trong hệ thống kiểm soát | Dữ liệu nhạy cảm có thể “bám” vào trọng số mô hình (rủi ro rò rỉ) |
| **Traceability** | Có thể truy ngược về tài liệu nguồn | Khó kiểm tra nguồn gốc thông tin |

### 3.4 Khi nào dùng RAG?
- Thông tin thay đổi thường xuyên (giá chứng khoán, tin tức, tài liệu nội bộ cập nhật hàng ngày).  
- Yêu cầu truy vet nguồn hoặc tuân thủ các quy định bảo mật (GDPR, HIPAA).  
- Hạn chế về dữ liệu có nhãn hoặc nguồn lực tính toán để fine‑tuning.  
- Ứng dụng cần truy cập vào kho tài liệu lớn mà không thể embed vào mô hình (ví dụ: trợ lý hỗ trợ khách hàng dựa trên kiến thức nội bộ).

### 3.5 Khi nào dùng fine‑tuning?
- Nhiệm vụ đòi hỏi định dạng, phong cách hoặc thuật ngữ rất cụ thể (soạn thảo hợp đồng pháp lý, báo cáo y tế, tạo mã theo chuẩn công ty).  
- Môi trường triển khai bị hạn chế (offline, thiết bị nhẹ) không thể truy xuất CSDL bên ngoài.  
- Có sẵn bộ dữ liệu có nhãn chất lượng và muốn tối ưu chi phí phục vụ (mô hình nhỏ nhưng hiệu suất cao).  
- Ứng dụng cần kiểm soát chặt chẽ về đầu ra (ví dụ: chatbot theo phong cách thương hiệu).

### 3.6 Cách kết hợp (Hybrid)
- **Idea**: fine‑tuning LLM để đạt được chuyên môn sâu, đồng thời dùng RAG để cung cấp thông tin mới nhất hoặc nhữngGap không được bao phủ trong bộ huấn luyện.  
- **Lợi ích**: Kész combines sự đồng nhất phong cách + khả năng truy cập dữ liệu thời gian thực.  
- **Thực tế**: Một hệ thống phân tích tài liệu pháp lý có thể fine‑tuning trên bộ luật và sự kiện để hiểu ngữ pháp pháp lý, rồi dùng RAG để truy xuất أحدث bản sửa đổi luật hoặc precedents mới nhất khi trả lời.  
- **Lưu ý**: Phương pháp này cần đầu vào từ cả hai 분야 (ML engineering + data engineering) và chi phí tương ứng tăng lên.

### 3.7 Hướng dẫn quyết định
1. **Xác định ưu tiên chính**: Dữ liệu mới nhất → RAG; Định dạng / phong cách chuyên biệt → fine‑tuning.  
2. **Đánh giá tần suất thay đổi dữ liệu**: Nếu cập nhật hàng ngày/tuần → RAG; Thay đổi hàng năm hoặc ít hơn → fine‑tuning có thể khả thi.  
3. **Kiểm tra nguồn lực**:  
   - Có đủ dữ liệu có nhãn và GPU? → cân nhắc fine‑tuning.  
   - Chỉ có tài liệu nguyên bản và ít chuyên gia ML? → RAG dễ triển khai hơn.  
4. **Xem xét bảo mật & traceability**: Nếu cần kiểm soát truy xuất dữ liệu và khả năng audit → RAG ưu tiên.  
5. **Thử nghiệm bắt đầu bằng phương pháp đơn giản hơn**, sau đó mở rộng theo nhu cầu (ví dụ: bắt đầu với RAG, sau khi thu thập đủ dữ liệu có nhãn thì thêm fine‑tuning).  

## 4. Ví dụ minh họa (pseudo‑code)

### RAG bằng LangChain (Python)
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 1. Tải và embedding tài liệu
docs = load_my_documents()                     # hàm tự viết đọc file/pdf
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# 2. Xây dựng chain truy xuất + LLM
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 3. Trả lời
answer = qa.run("Cách đặt lại mật khẩu VPN của công ty?")
print(answer)
```
- Đoạn này minh họa các bước: ingest → embedding → lưu trong FAISS → truy xuất → tạo prompt augmented → LLM trả lời.

### Fine‑tuning bằng Hugging Face Transformers (PyTorch)
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import load_dataset

model_name = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tập dữ liệu có các cặp (prompt, response) về y tế
dataset = load_dataset("csv", data_files="medical_qa.csv")
def preprocess(example):
    inputs = tokenizer(example["question"], truncation=True, max_length=128)
    targets = tokenizer(example["answer"], truncation=True, max_length=128)
    return {"input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
            "labels": targets["input_ids"]}

tokenized_ds = dataset.map(preprocess, batched=True)

training_args = TrainingArguments(
    output_dir="./t5-medical",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    learning_rate=5e-5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds["train"],
)

trainer.train()
```
- Minh họa quá trình chuẩn bị dữ liệu, tokenization, huấn luyện và lưu mô hình đã fine‑tuning.

## 5. Tổng kết
- **RAG** cho phép mô hình truy cập kiến thức bên ngoài ngay lúc truy vấn, thích hợp cho trường hợp cần thông tin mới nhất, tính minh bạch và bảo mật cao.  
- **Fine‑tuning** đưa kiến thức chuyên ngành vào trọng số mô hình, giúp raggiungere độ chính xác, phong cách và định dạng ổn định trên nhiệm vụ hẹp, nhưng đòi hỏi dữ liệu có nhãn, lực lượng tính toán và khó cập nhật.  
- **Lựa chọn** phụ thuộc vào tần suất thay đổi dữ liệu, yêu cầu bảo mật, nguồn lực có sẵn và mức độ kiểm soát đầu ra mong muốn.  
- **Hybrid** (fine‑tuning + RAG) có thể mang lại cả chuyên môn sâu và khả năng truy cập dữ liệu thời gian thực, nhưng đòi hỏi đầu tư hơn về cả ML và data engineering.  

Bằng cách đánh giá những yếu tố trên và bắt đầu với phương pháp đơn giản nhất phù hợp với nhu cầu hiện tại, bạn có thể dần phát triển hệ thống AI trở nên mạnh mẽ, linh hoạt và đáng tin cậy hơn theo thời gian.