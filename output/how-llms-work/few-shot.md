# Few-shot Prompting

## 1. Mục tiêu học tập

- Giải thích khái niệm few-shot prompting và cách nó cho phép mô hình học bối cảnh (in‑context learning).  
- Xây dựng prompt chứa một vài demonstrations (1‑shot, 3‑shot, …) và dự đoán kết quả mong đợi.  
- Nhậnทรôle của định dạng prompt và phân phối nhãn trong few‑shot, ngay cả khi nhãn được random.  
- Nhận biết giới hạn của few‑shot khi confronting tasks requiring deeper reasoning và biết khi nào nên cân nhắc các kỹ thuật nâng cao như chain‑of‑thought hoặc fine‑tuning.

## 2. Tổng quan

Các mô hình ngôn ngữ lớn (LLM) đã thể hiện khả năng Zero‑shot впечатляюще, nhưng đối với một số nhiệm vụ phức tạp, chúng vẫn thất bại khi chỉ nhận được mô tả nhiệm vụ mà không có bất kỳ ví dụ nào. Few‑shot prompting là một kỹ thuật cung cấp một số demonstrations (ví dụ) ngay trong prompt để “điều kiện” mô hình, từ đó giúp mô hình suy ra đúng định dạng hoặc nhãn cho các ví dụ mới. Khi mô hình đạt đủ quy mô (theo các nghiên cứu của Kaplan et al., 2020 và Touvron et al., 2023), khả năng few‑shot bắt đầu xuất hiện và có thể được nâng cao bằng cách tăng số lượng demonstrations.

## 3. Kiến thức cốt lõi

### 3.1 Few‑shot là gì?  
Few‑shot prompting là việc đưa vào prompt một vài cặp **input–output** (demonstrations) mà mô hình sẽ dùng như bối cảnh để suy ra output cho một input mới mà không có demonstration cụ thể. Số demonstrations thường gọi là *k‑shot* (ví dụ: 1‑shot, 3‑shot, 5‑shot).

### 3.2 Tại sao few‑shot hoạt động?  
Khi mô hình đủ lớn, nó có khả năng học trong‑bối‑cảnh (in‑context learning): các demonstrations hoạt động như một dạng “conditioning” giúp mô hìnhinternalize pattern của nhiệm vụ (label space, định dạng, mối quan hệ giữa input và output).Các nghiên cứu cho thấy:

- **Label space và distribución của input text** trong demonstrations đều quan trọng, dù các label đó có đúng hay không đối với mỗi input riêng.  
- **Định dạng** (ví dụ: cách ngăn cách bằng `//`, xuống dòng, dấu hai chấm) cũng góp phần vào hiệu suất; thậm chí khi dùng random labels, giữ định dạng đã tốt hơn việc không có label nào.  
- Chọn ngẫu nhiên label từ **phân phối thực** của các label (thay vì phân phối đồng đều) còn cải thiện kết quả hơn.

### 3.3 Giới hạn của few‑shot  
Few‑shot hoạt động tốt với nhiều tasks đơn giản (ví dụ: classification, sử dụng từ mới trong câu). Tuy nhiên, đối với các nhiệm vụ đòi hỏi **suy luận đa bước** (arithmetic, commonsense, symbolic reasoning), chỉ提供几个例子 thường不足以获得可靠的答案。 trong phần “Limitations of Few-shot Prompting” của nguồn, ví dụ về việc xác định xem tổng của các số lẻ có chẵn không cho thấy mô hình vẫn trả lời sai ngay cả khi đã cung cấp một số demonstrations. Điều này cho thấy khi task đòi hỏi **bước reasoning sâu**, chúng ta có thể cần:

- Bài toán được chia thành các bước nhỏ và demonstrat mỗi bước (giống như chain‑of‑thought prompting).  
- Tham khảo các kỹ thuật nâng cao hơn hoặc fine‑tune mô hình trên dữ liệu nhiệm vụ cụ thể.

### 3.4 Mối quan hệ với Chain‑of‑Thought (CoT)  
Khi few‑shot không đủ,Chain‑of‑Thought prompting được提出 để nudging mô hình sinh ra một chuỗi reasoning trung gian trước khi đưa ra câu trả lời cuối cùng. Đây là bước tiến logic sau khi nhận ra hạn chế của few‑shot trên các tasks reasoning phức tạp.

## 4. Ví dụ minh họa

### 4.1 Ví dụ đơn giản – học sử dụng từ mới  
**Prompt**

```
A "whatpu" is a small, furry animal native to Tanzania. An example of a sentence that uses the word whatpu is:
We were traveling in Africa and we saw these very cute whatpus.

To do a "farduddle" means to jump up and down really fast. An example of a sentence that uses the word farduddle is:
```

**Output (mô hình sinh ra)**

```
When we won the game, we all started to farduddle in celebration.
```

*Giải thích:* Chỉ với một demonstration (1‑shot) cho cách dùng từ “farduddle”, mô hình đã học cách tạo một câu hợp lệ chứa từ đó.

### 4.2 Ví dụ random labels – định dạng vẫn quan trọng  
**Prompt**

```
This is awesome! // Negative
This is bad! // Positive
Wow that movie was rad! // Positive
What a horrible show! //
```

**Output**

```
Negative
```

*Giải thích:* Dù các label (Negative/Positive) đã được gán ngẫu nhiên, mô hình vẫn dự đoán nhãn đúng cho câu cuối cùng vì nó đã học được định dạng `//` và dựa vào sự xuất hiện của các từ cảm xúc trong các demonstration trước.

### 4.3 Ví dụ不同格式 – mô hình bền vững hơn  
**Prompt**

```
Positive This is awesome!
This is bad! Negative
Wow that movie was rad!
Positive
What a horrible show! --
```

**Output**

```
Negative
```

*Giải thích:* Định dạng không nhất quán (một số dòng không có `//`, có dấu `--`), nhưng mô hình vẫn cho ra nhãn đúng, cho thấy các mô hình GPT mới đang trở nên ít phụ thuộc vào định dạng cứng nhắc.

### 4.4 Giới hạn trên bài toán reasoning – few‑shot không đủ  
**Prompt (các demonstrations + test case)**

```
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.
A: The answer is False.

The odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24.
A: The answer is True.

The odd numbers in this group add up to an even number: 16,  11, 14, 4, 8, 13, 24.
A: The answer is True.

The odd numbers in this group add up to an even number: 17,  9, 10, 12, 13, 4, 2.
A: The answer is False.

The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1.
A:
```

**Output**

```
The answer is True.
```

*Giải thích:* Tổng các số lẻ trong nhóm cuối cùng là \(15+5+13+7+1 = 41\) (lẻ) → đáp án đúng là **False**, nhưng mô hình trả về **True**. Đây là biểu hiện rõ ràng của giới hạn few‑shot khi confronting tasks requiring multi‑step reasoning (cần tính tổng, kiểm tra chẵn/lẻ). Để cải thiện, ta có thể:

- Thêm demonstrations mỗi bước (tính tổng lẻ rồi kiểm tra chẵn/lẻ) – giống như chain‑of‑thought.  
- Hoặc fine‑tune mô hình trên bộ dữ liệu tương tự.

## 5. Tổng kết

- Few‑shot prompting cho phép mô hình học bối cảnh bằng cách đưa một vài demonstrations vào prompt; hiệu quả tăng khi mô hình đủ lớn và khi label space, input distribution, và định dạng được giữ nhất quán.  
- Ngay cả khi labels được random, việc giữ định dạng có thể vẫn dẫn tới dự đoán đúng, cho thấy định dạng đóng vai trò then chốt.  
- Tuy nhiên, few‑shot không đủ cho các nhiệm vụ đòi hỏi reasoning sâu (ví dụ: kiểm tra tổng số lẻ có chẵn không). Trong các trường hợp này, cần suy nghĩ tới chain‑of‑thought prompting hoặc fine‑tuning.  
- Việc hiểu rõ khi nào và cách áp dụng few‑shot sẽ giúp bạn xây dựng prompt hiệu quả cho nhiều ứng dụng LLM trước khi cânถึง các kỹ thuật nâng cao.