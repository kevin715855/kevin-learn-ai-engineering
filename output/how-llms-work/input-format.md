# Học cách xây dựng ứng dụng với Claude Code: Thành phần của một Prompt

## 1. Mục tiêu học tập

Sau khi hoàn thành bài học này, người học sẽ:
- Hiểu ba–bốn thành phần cơ bản của một prompt trong prompt engineering.
- Phân biệt vai trò của **Instruction**, **Context**, **Input Data** và **Output Indicator**.
- Xây dựng một prompt đơn giản để thực hiện một tác vụ cụ thể (ví dụ: phân loại cảm xúc văn bản).
- Áp dụng kiến thức này để thiết kế các prompt hiệu quả cho các mô hình ngôn ngữ lớn (LLM).

## 2. Tổng quan

Prompt engineering là kỹ thuật thiết kế các đoạn văn bản (prompt) để hướng dẫn mô hình ngôn ngữ lớn tạo ra phản hồi mong muốn. Một prompt không chỉ là câu hỏi; nó có thể chứa các thành phần khác nhau để cải thiện chất lượng và độ chính xác của đầu ra. Bài học này sẽ giải thích từng thành phần thường gặp trong một prompt và minh họa bằng ví dụ thực tế.

## 3. Kiến thức cốt lõi

### 3.1 Instruction (Hướng dẫn)

- **Định dạng**: Mô tả rõ ràng tác vụ mà bạn muốn mô hình thực hiện.
- **Ví dụ**: “Classify the text into neutral, negative, or positive” (Phân loại văn bản thành trung bình, tiêu cực hoặc tích cực).
- **Lưu ý**: Càng cụ thể và không mơ hồ, mô hình càng dễ hiểu yêu cầu.

### 3.2 Context (Ngữ cảnh)

- **Định dạng**: Thông tin bổ sung hoặc ví dụ giúp mô hình hiểu tốt hơn về nhiệm vụ và mong muốn về định dạng đầu ra.
- **Ví dụ**: Cung cấp một vài câu đã được gán nhãn cảm xúc trước khi yêu cầu phân loại câu mới.
- **Lưu ý**: Context là thành phần tùy chọn; nó được dùng khi nhiệm vụ phức tạp hoặc cần hướng dẫn thêm.

### 3.3 Input Data (Dữ liệu đầu vào)

- **Định dạng**: Cụm từ, câu hỏi, hoặc dữ liệu mà bạn muốn mô hình xử lý.
- **Ví dụ**: “I think the food was okay.” (Tôi думаю ăn được quite bình thường).
- **Lưu ý**: Đây là phần mà mô hình sẽ sinh ra phản hồi dựa trên Instruction và Context (nếu có).

### 3.4 Output Indicator (Chỉ báo đầu ra)

- **Định dạng**: Đại chỉ dạng hoặc cấu trúc mà bạn mong đợi trong kết quả, thường là một từ khóa hoặc dấu phân cách.
- **Ví dụ**: “Sentiment:” (Cảm xúc:), sau đó mô hình sẽ điền giá trị như “positive”, “negative” hoặc “neutral”.
- **Lưu ý**: Output Indicator giúp tách phần trả lời ra khỏi phầnrompt và dễ pós‑process.

> **Lưu ý tổng hợp**: Một prompt không nhất thiết phải chứa đầy đủ bốn thành phần. Tùy thuộc vào tác vụ, bạn có thể chỉ cần Instruction + Input Data, hoặc bổ sung Context và Output Indicator để đạt hiệu quả tốt hơn.

## 4. Ví dụ minh họa

### 4.1 Prompt phân loại cảm xúc (không có Context)

```
Classify the text into neutral, negative, or positive

Text: I think the food was okay.

Sentiment:
```

- **Instruction**: “Classify the text into neutral, negative, or positive”
- **Input Data**: “I think the food was okay.”
- **Output Indicator**: “Sentiment:”
- **Context**: Không có.

Khi mô hình nhận được prompt này, nó sẽ suy ra rằng câu “I think the food was okay.” mang cảm xúc trung bình và sinh ra:

```
Sentiment: neutral
```

### 4.2 Prompt phân loại cảm xúc (có Context)

```
Classify the text into neutral, negative, or positive

Examples:
- "I love this movie!" -> positive
- "The service was terrible." -> negative
- "It was okay, nothing special." -> neutral

Text: I think the food was okay.

Sentiment:
```

- **Instruction**:同上
- **Context**: Ba ví dụ đã được gán nhãn để giúp mô hình hiểu cách phân loại.
- **Input Data**: “I think the food was okay.”
- **Output Indicator**: “Sentiment:”

Các ví dụ trong Context cung cấp thêm견 giải về cách biểu diễn từng lớp, giúp mô hình đưa ra quyết định chính xác hơn, đặc biệt khi biên giới giữa các lớp mơ hồ.

## 5. Tổng kết

- Một prompt gồm có thể bao gồm **Instruction**, **Context**, **Input Data** và **Output Indicator**.
- **Instruction** xác định nhiệm vụ; **Input Data** là đối tượng cần xử lý; **Output Indicator** chỉ định định dạng đầu ra; **Context** cung cấp thông tin bổ sung để cải thiện hiệu suất.
- Không phải mọi prompt đều cần tất cả bốn thành phần; việc chọn thành phần phù hợp phụ thuộc vào độ phức tạp của tác vụ và mức độ hướng dẫn mà mô hình cần.
- Thực hành xây dựng prompt với các thành phần trên sẽ giúp bạn khai thác tốt hơn khả năng của các mô hình như Claude, GPT‑4, hoặc các LLM khác khi xây dựng ứng dụng AI.