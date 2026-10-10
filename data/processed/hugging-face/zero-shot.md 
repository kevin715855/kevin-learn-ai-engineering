# Zero‑shot Prompting: Nguyên lý và ứng dụng trong Prompt Engineering  

## 1. Mục tiêu học tập  
Sau bài học này, người học sẽ能够:  

- Giải thích **zero‑shot prompting** là gì và cách nó hoạt động.  
- Phân biệt zero‑shot prompting với few‑shot prompting (bao gồm one‑shot).  
- Liệt kê các thành phần chính của một prompt trong zero‑shot.  
- Nhận biết ưu điểm và hạn chế của zero‑shot prompting.  
- Mô tả các kỹ thuật cải thiện hiệu suất zero‑shot (instruction tuning, RLHF).  
- Áp dụng zero‑shot prompting vào một số trường hợp thường见: phân loại văn bản, trích xuất thông tin, trả lời câu hỏi, tóm tắt, sinh dữ liệu, trò chuyện.  
- Giới thiệu brevemente các phương pháp nâng cao như Chain‑of‑Thought và Tree‑of‑Thought.  

## 2. Tổng quan  
Zero‑shot prompting là một kỹ thuật trong **prompt engineering** mà mô hình ngôn ngữ lớn (LLM) được yêu cầu tạo ra câu trả lời chỉ dựa trên kiến thức mà nó đã học trong giai đoạn **pre‑training**, không cần cung cấp bất kỳ ví dụ đầu vào‑đầu ra nào cho nhiệm vụ cụ thể. Khi tác vụ mới xuất hiện, chúng ta chỉ cần đưa ra một **prompt** mô tả nhiệm vụ và mong đợi mô hình suy luận (infer) câu trả lời thích hợp.  

Cách tiếp cận này tận dụng khả năng **zero‑shot learning** của các foundation model: chúng có thể áp dụng kiến thức đã học để giải quyết vấn đề mới mà không cần huấn luyện thêm.  

## 3. Kiến thức cốt lõi  

### 3.1 Định nghĩa và cách hoạt động  
- **Zero‑shot prompting**: prompt không chứa bất kỳ ví dụ输出 nào; mô hình dựa vào kiến thức pretrain để suy ra output.  
- Quy trình:  
  1. **Instruction** – chỉ dẫn mô hình làm gì (ví dụ: “Đặt tên lớp cho vấn đề đã mô tả…”).  
  2. **Context** – mô tả các lớp/nhãn có thể chọn (High, Medium, Low …).  
  3. **Input data** – конкретный объект cần xử lý (ví dụ: “Issue: Users are reporting that they are unable to upload files.”).  
  4. **Output indicator** (tùy chọn) – từ hoặc ký hiệu báo hiệu loại output mong đợi (ví dụ: “Class:”).  

Khi đầy đủ 4 thành phần trên, mô hình sẽ tạo ra câu trả lời phù hợp, mặc dù chưa từng thấy bất kỳ ví dụ nào về cách gán nhãn cho trường hợp cụ thể đó.  

### 3.2 So sánh với Few‑shot prompting  
|                     | Zero‑shot                              | Few‑shot (ví dụ: 2‑shot)                     |
|---------------------|----------------------------------------|----------------------------------------------|
| Ví dụ đầu ra        | Không có                               | Cung cấp một vài cặp input‑output mẫu        |
| Độ phức tạp prompt  | Đơn giản (chỉ instruction + context)   | Dài hơn vì phải nhúng ví dụ                  |
| Khi nào dùng        | Khi không có dữ liệu labeled hoặc muốn thử nhanh | Khi mô hình cần hướng dẫn cụ thể để cải thiện độ chính xác |
| Hiệu suất           | Phù hợp với задачи mà kiến thức pretrain đã покрывает | Tốt hơn khi task đòi hỏi sự tinh chỉnh nhẹ dựa trên mẫu |

Trong tài nguyên nguồn, ví dụ few‑shot cho cùng mô hình **IBM granite‑3‑8b‑instruct** cung cấp ba cặp (issue → class) và mô hình dự đoán lớp “Medium” cho issue cuối cùng.  

### 3.3 Ưu điểm  
1. **Đơn giản** – prompt ngắn, dễ tạo và hiểu.  
2. **Không cần data phụ trợ** – hữu ích khi dữ liệu label稀缺 hoặc không thể thu thập.  
3. **Linh hoạt** – dễ chỉnh sửa prompt khi yêu cầu thay đổi.  

### 3.4 Hạn chế  
1. **Biến động hiệu suất** – trên các nhiệm vụ phức tạp, đòi hỏi kiến thức chuyên sâu hoặc output rất cụ thể, mô hình có thể đưa ra kết quả kurang ổn định.  
2. **Phụ thuộc vào chất lượng pretrain** – nếu mô hình chưa được tiếp cận đủ với một chủ đề, ngôn ngữ hoặc bối cảnh cụ thể, hiệu suất zero‑shot sẽ giảm.  

### 3.5 Cải thiện hiệu suất  
- **Instruction tuning**: fine‑tune mô hình trên bộ dữ liệu bao gồm các instruction và output mong đợi (tóm tắt, перевод, đọc hiểu …). Kết quả là mô hình hiểu và thực hiện tốt hơn các instruction mới mà không cần few‑shot examples.  
- **Reinforcement Learning with Human Feedback (RLHF)**:  
  1. Fine‑tune trên dataset có human‑provided target responses.  
  2. Thu thập output từ mô hình cho nhiều prompt, có người xếp hạng.  
  3. Huấn luyện một mô hình 강화学习 để học policy chọn output tốt nhất dựa trên xếp hạng.  
Cả hai kỹ thuật này đã được chứng minh nâng cao độ chính xác zero‑shot trên nhiều tác vụ NLP.  

### 3.6 Ứng dụng thực tiễn  
Zero‑shot prompt có thể áp dụng cho nhiều trường hợp NLP mà không cần training data bổ sung:  

- **Phân loại văn bản** (ví dụ: xác định mức độ ưu tiên của lỗi IT).  
- **Trích xuất thông tin** –Given a passage and a question, model returns the requested span.  
- **Trả lời câu hỏi** – sử dụng kiến thức pretrain để tạo câu trả lời.  
- **Tóm tắt văn bản** – instruction “Summarize the following text…”.  
- **Sinh dữ liệu** – tạo mã, văn bản, hình ảnh theo mô tả.  
- **Trò chuyện** – sử dụng mô hình đã được fine‑tune cho chat (chat‑GPT‑like) để duy trì cuộc hội thoại.  

### 3.7 Các phương pháp nâng cao (khi zero‑shot/few‑shot không đủ)  
- **Chain‑of‑Thought (CoT) prompting** – chia nhiệm vụ thành chuỗi các bước reasoning trung gian; mô hình phải sinh ra mỗi bước trước khi đưa ra kết luận cuối cùng. Cung cầu reasoning trong suốt và cải thiện hiệu suất trên các bài toán cần suy luận đa bước (Toán học, lógica).  
- **Tree‑of‑Thought (ToT) prompting** – mở rộng CoT bằng việc tạo một cây các khả năng tiếp theo; mô hình có thể khám phá nhiều đường đi, lui lại khi cần, và tìm giải pháp tối ưu. Thích hợp cho bài toán tìm kiếm không gian lớn (Sudoku, Game of 24).  

## 4. Ví dụ minh họa  

### 4.1 Zero‑shot example (phân loại mức độ ưu tiên)  
**Prompt** (được chạy trong IBM watsonx.ai Prompt Lab – chế độ *Freeform*):  

```
Set the Class name for the issue described to either High, Medium or Low. 
Predict only the Class name for the last issue. 
Give a short description for why that Class name was chosen.

Class name: High
Description: An issue that has a high business cost, impacts many users or both.

Class name: Medium
Description: An issue that falls somewhere in between high and low.

Class name: Low
Description: An issue that has an impact on a few users, does not have a high business cost or both.

Issue: Users are reporting that they are unable to upload files.
```

**Output** (đ wyróżнен жирным в оригинале):  

```
Class: High
Description: This issue is considered high because it impacts many users and has a high business cost. The inability to upload files can prevent users from completing their tasks, which can lead to delays and decreased productivity. Additionally, this issue may impact multiple departments or teams, further increasing the business cost.
```

**Giải thích:** Mô hình chưa từng thấy bất kỳ ví dụ nào về cách gán nhãn “High/Medium/Low” cho một trường hợp cụ thể, nhưng dựa trên mô tả các lớp và kiến thức pretrain về tác động của lỗi không thể tải file, nó suy ra rằng đây là vấn đề mức độ **High**.  

### 4.2 Few‑shot example (cùng mô hình, cùng nhiệm vụ)  
**Prompt** (thêm ba ví dụ):  

```
Set the Class name for the issue described to either High, Medium or Low. 
I've provided a few examples of issues and their corresponding Class names. 
Predict only the Class name for the last issue. 
Give a short description for why that Class name was chosen.

Class name: High
Description: An issue that has a high business cost, impacts many users or both.

Class name: Medium
Description: An issue that falls somewhere in between high and low.

Class name: Low
Description: An issue that has an impact on a few users, does not have a high business cost or both.

Issue: New users report that they cannot create accounts.
Class: High

Issue: A user reports that labels are rendering overlapping in the app's analytics function.
Class: Low

Issue: Users in the United States are reporting that the app is crashing when trying to make a purchase.
Class: High

Issue: Users report that images are not loading in the app.
```

**Output:**  

```
Class: **Medium**
Explanation: The issue of images not loading in the app impacts users' experience and might cause frustration, but it does not have a high business cost or impact many users. Therefore, it is classified as a medium-level issue.
```

**Giải thích:** Khi được cung cấp ba cặp ví dụ input‑output, mô hình học được النمط и dự đoán nhãn **Medium** cho issue cuối cùng, minh họa cách few‑shot có thể cải thiện độ chính xác khi prompt cần sự hướng dẫn cụ thể.  

## 5. Tổng kết  
- Zero‑shot prompting là phương pháp prompt engineering đơn giản, tận dụng kiến thức pretrain của LLM để suy luận output mà không cần ví dụ huấn luyện.  
- Nó bao gồm **instruction**, **context**, **input data**, và tùy chọn **output indicator**.  
- So với few‑shot, zero‑shot không yêu cầu dữ liệu mẫu nhưng có thể gặp dificulty trên nhiệm vụ phức tạp hoặc đòi hỏi kiến thức chuyên sâu sâu.  
- Hiệu suất zero‑shot có thể được nâng cao qua **instruction tuning** và **RLHF**.  
- Ứng dụng rộng: phân loại văn bản, trích xuất thông tin, trả lời câu hỏi, tóm tắt, sinh dữ liệu, trò chuyện.  
- Khi zero‑shot/few‑shot không đủ, các kỹ thuật nâng cao như **Chain‑of‑Thought** và **Tree‑of‑Thought** cung cấp cách suy luận có cấu trúc tốt hơn.  

Với những hiểu biết trên, bạn có thể tự thiết kế và tối ưu hoá prompt cho các nhiệm vụ AI thực tế dựa trên mô hình ngôn ngữ lớn.