# Kỹ thuật vai trò trong Prompt Engineering (Role Prompting)

## 1. Mục tiêu học tập
- Nắm được khái niệm **role prompting** và cách nó ảnh hưởng đến đầu ra của mô hình ngôn ngữ lớn (LLM).  
- Biết cách áp dụng vai trò để thay đổi phong cách, giọng độ và độ sâu của văn bản được sinh ra.  
- Hiểu vai trò có thể cải thiện độ chính xác trong một số bài toán (ví dụ: toán học).  
- Thực hành viết prompt với vai trò cụ thể và đánh giá kết quảso với prompt không có vai trò.

## 2. Tổng quan
Role prompting (gán vai trò) là một kỹ thuật trong prompt engineering cho phép người dùng chỉ định một “persona” hoặc vai trò cho mô hình AI (ví dụ: nhà phê bình ẩm thực, chuyên gia tiếp thị, nhà toán học). Khi mô hình nhận vai trò đó, nó sẽ điều chỉnh cách xử lý và trình bày thông tin để phù hợp với đặc điểm của vai trò đã được chỉ định. Kỹ thuật này được sử dụng rộng rãi trong việc tạo nội dung sáng tạo, soạn thảo email, viết đánh giá, cũng như nâng cao độ chính xác trong các bài toán logic và toán học.

## 3. Kiến thức cốt lõi

### 3.1. Định dạng cơ bản của role prompt
```
Bạn là <vai trò>. <yêu cầu cụ thể>
```
- `<vai trò>`: mô tảPersona (nhà phê bình, chuyên gia marketing, nhân viên chăm sóc khách hàng, v.v.).  
- `<yêu cầu cụ thể>`: nhiệm vụ mà bạn muốn mô hình thực hiện (viết đánh giá, soạn email, giải toán,…).

### 3.2. Ảnh hưởng của vai trò
| Yếu tố | Khi không có vai trò | Khi có vai trò |
|--------|----------------------|----------------|
| Phong cách | Trung tính, có thể chung chung | Theo đặc điểm của vai trò (professional, say mê, giải quyết vấn đề,…) |
| Giọng độ | Trung lập | Chính xác, thuyết phục, đồng cảm… tùy vai trò |
| Độ chi tiết | Ít chi tiết | Thêm thông tin, ví dụ, ngôn ngữ chuyên môn |
| Độ chính xác (đặc biệt trong toán) | Có thể sai do mô hình không “tập trung” | Có khả năng cao hơn khi vai trò đòi hỏi suy luận logic (ví dụ: nhà toán học) |

### 3.3. Ứng dụng chính
1. **Thay đổi phong cách văn bản** – phù hợp cho bài đánh giá, bài viết, email, nội dung marketing.  
2. **Nâng cao độ chính xác** – đặc biệt hữu ích trong các bài toán cần suy luận từng bước (math, logic).

### 3.4. Lưu ý
- Vai trò cần được mô tả rõ ràng và cụ thể để mô hình có “hình dung” vềPersona.  
- Khi sử dụng với các mô hình mới (GPT‑4, Claude …), tác động của vai trò tới độ chính xác có thể giảm nhẹ; cần kiểm tra kết quả thực nghiệm.  
- Kết hợp role prompting với các kỹ thuật khác (instructions, few‑shot examples) để tối ưu kết quả.

## 4. Ví dụ minh họa

### 4.1. Thay đổi phong cách đánh giá pizza  
**Prompt không có vai trò**
```
Write a review of [pizza place].
```
**Kết quả AI (tóm tắt)**
> I recently had the pleasure of trying [random pizza place] and I must say that I was thoroughly impressed. The pizza was cooked to perfection and the toppings were fresh and flavorful…

**Prompt với vai trò “food critic”**
```
You are a food critic. Write a review of [pizza place].
```
**Kết quả AI**
> I recently had the pleasure of dining at [Pizza Place], a cozy pizzeria located in the heart of the city. Despite its small size, the restaurant packs a huge punch when it comes to flavor. … (mô tả chi tiết hơn về bánh, sốt, phô mai, phục vụ)

**Prompt với vai trò “Michelin Guide reviewer”**
```
You are a food critic writing for the Michelin Guide. Write a review of [pizza place].
```
**Kết quả AI**
> Located in the heart of [random city], [random pizza place] is a popular spot for pizza lovers. Upon entering, the warm, inviting atmosphere and the smell of freshly baked pizza will make you feel right at home. … (miêu lucht phong cách chính thức, đề cập đến menu, giá cả, không gian)

### 4.2. Soạn email thông báo sự trễ giao hàng  
**Vai trò: Communications Specialist**
```
You are a communications specialist. Draft an email to your client advising them about a delay in the delivery schedule due to logistical problems.
```
**Kết quả AI**
> Subject: Important Update Regarding Your Order  
> Dear [Client's Name],  
> I hope this email finds you well. I'm reaching out to notify you of a delay in the delivery of your order… (ngắn gọn, trang trọng, giải quyết vấn đề)

**Vai trò: Marketing Expert**
```
You are a marketing expert. Draft an email to a client advising them about a delay in the delivery schedule due to logistical problems.
```
**Kết quả AI**
> Subject: A Little More Wait for Your Wonderful Products  
> Dear [Client's Name],  
> We hope this message finds you buzzing with excitement for your upcoming order! … (ngôn ngữ khích lệ, tích cực, nhấn mạnh sự kiên nhẫn)

**Vai trò: Customer Service Representative**
```
You are a customer service representative. Draft an email to a client advising them about a delay in the delivery schedule due to logistical problems.
```
**Kết quả AI**
> Subject: Attention Required: Update on Your Order Status  
> Dear [Client's Name],  
> Greetings from [Your Company Name].  
> We wanted to inform you that, due to unforeseen logistical challenges, there might be a delay in the delivery of your order… (thông cảm, giải pháp, hỗ trợ)

### 4.3. Nâng cao độ chính xác trong bài toán Toán  
**Prompt không có vai trò**
```
What is 100*100/400*56?
```
**Kết quả AI (sai)**
> 280  

**Prompt với vai trò “brilliant mathematician”**
```
You are a brilliant mathematician who can solve any problem in the world.
Attempt to solve the following problem:
What is 100*100/400*56?
```
**Kết quả AI (đúng)**
> The answer is 1400.

*Giải thích:* Khi được đặt vai trò nhà toán học, mô hình tập trung vào quy tắc 우선 tiên của phép nhân và chia (từ trái sang phải) và cho ra kết quả chính xác.

## 5. Tổng kết
- **Role prompting** là kỹ thuật gán một vai trò hoặc persona cụ thể cho LLM để kiểm soát phong cách, giọng độ và đôi khi là độ chính xác của đầu ra.  
- Khi áp dụng, chúng ta có thể dễ dàng tạo ra văn bản phù hợp với nhu cầu (đánh giá ẩm thực, email zawod, bài viết marketing…) bằng cách chỉ cần thay đổi mô tả vai trò.  
- Ngoài ra, trong một số trường hợp như bài toán toán học hoặc logic, việc đặt vai trò chuyên gia có thể giúp mô hình tập trung vào suy luận logic và giảm lỗi.  
- Để đạt hiệu quả tốt nhất, nên mô tả vai trò một cách rõ ràng, cụ thể và có thể kết hợp với các kỹ thuật khác như hướng dẫn chi tiết (instructions) hoặc few‑shot examples.  

Bằng cách luyện tập viết prompt với các vai trò khác nhau, bạn sẽ nhanh chóng thành thạo khả năng kiểm soát đầu ra của mô hình AI và áp dụng linh hoạt trong nhiều bài toán thực tiễn.