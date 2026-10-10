# Beyond Basics: Contextual & Role Prompting That Actually Works

## 1. Mục tiêu học tập
- Hiểu nguyên tắc và lợi ích của **system prompting**, **role prompting** và **contextual prompting**.  
- Biết cách tạo các prompt hệ thống, vai trò và bối cảnh hiệu quả cho các nhiệm vụ cụ thể.  
- Kỹ năng kết hợp ba kỹ thuật này để kiểm soát đầu ra của LLM một cách chính xác và nhất quán.  
- Áp dụng các mẫu prompt thực tế vào các tình huống như phân tích phản hồi khách hàng, viết tài liệu kỹ thuật, tạo nội dung marketing.  
- Thực hành проверка và cải tiến prompt qua thử nghiệm có hệ thống.

## 2. Tổng quan
Sau khi thành thaoat với các kỹ thuật prompting cơ bản (zero‑shot, few‑shot), nhiều người gặp “tường” khi cần kiểm soát hơn về giọng điệu, độ sâu kiến thức và tính nhất quán của đầu ra. **System prompting**, **role prompting** và **contextual prompting** cung cấp ba chiều mới để định hình cách mô hình hiểu và phản hồi. Chúng cho phép đặt quy tắc hoạt động, gán vai trò chuyên môn và cung cấp bối cảnh situational, từ đó giảm lượng “guesswork” và tăng mức độ liên quan, độ tin catty của nội dung sinh ra.

## 3. Kiến thức cốt lõi

### 3.1 System Prompting: Quy tắc nền tảng
System prompt đặt các quy tắc cơ bản trước khi bắt đầu cuộc trò chuyện, giống như việc cấu hình tham số hệ thống.

**Lợi ích chính**
- Đảm bảo định dạng đầu ra nhất quán (bảng, JSON, bullet points …).  
- Áp dụng ràng buộc cụ thể (không speculation, chỉ dùng الأدلة …).  
- Định hướng mô hình نحو kiến thức chuyên môn qua việc khai báo “bạn là chuyên gia …”.  
- Xác định tiêu chí đánh giá (low‑cost, high‑impact …).  
- Xác định mô hình tương tác (hỏi làm rõ trước khi đưa ra khuyến nghị).

**Các mẹo强大**
1. **Rõ ràng về định dạng** – nêu chính xác cách bạn muốn dữ liệu được trình bày.  
2. **Xác định lĩnh vực kiến thức** – cho mô hình biết nó là chuyên gia trong một domaine để kích hoạt知识相关.  
3. **Đặt ràng buộc** – chỉ ra những gì **không** được làm.  
4. **Xác định tiêu chí đánh giá** – hướng ưu tiên các giải pháp.  
5. **Xây dựng mô hình tương tác** – yêu cầu mô hình hỏi trước khi kết luận.

**Lỗi thường gặp**  
Viết system prompt quá dài và phức tạp. Một câu hoặc hai câu tập trung vào các tham số cần thiết thường hiệu quả hơn một đoạn văn dài.

### 3.2 Role Prompting: Biến đổi nhân cách
Role prompting gán một danh tính hoặc nhân vật cụ thể để AI “trở thành” người đó khi trả lời.

**Khi mang lại breakthrough**
- Cần kiến thức chuyên môn hoặc góc nhìn đặc biệt.  
- Yêu cầu một phong cách truyền达 nhất quán.  
- Muốn truy cập vào knowledge domain cụ thể.  
- Muốn giảm lượng câu trả lời chung chung, “safe”.

**Kỹ thuật bí mật**
1. **Chi tiết về cấp độ chuyên môn** – “entry‑level” vs. “world‑class expert with 20 years of experience” tạo ra khác biệt rõ rệt.  
2. **Thêm nềnbanh 관련** – ví dụ: “Bạn là nhà tài chính phân tích thị trường mới phát triển, trước đây làm việc ở Goldman Sachs”.  
3. **Áp dụng phương pháp論解** – “Bạn giải quyết vấn đề bằng suy nghĩ nguyên lý và phân tích hệ thống”.  
4. **Xác định phong cách giao tiếp** – “Bạn giải thích概念 phức tạp bằng analogy đơn giản, không dùng thuật ngữ chuyên môn”.  
5. **Thêm tính cách khi cần** – “Bạn là người細致 và thận trọng, luôn chỉ ra các rủi ro tiềm ẩn”.

**Phong cách hiệu quả cho các mục đích khác nhau**
- **Giải thích kỹ thuật** – “Giải thích như thể bạn đang nói với một chuyên gia đồng cấp, nhưng phải chính xác và chi tiết”.  
- **Nội dung sáng tạo** – “Viết bằng hình ảnh sống động và shared cảm xúc”.  
- **Nội dung thuyết phục** – “Viết theo phong cách tự tin, dựa trên chứng據, sẵn sàng預測 và trả lời các ý kiến phản對”.  
- **Giảm độ phức tạp** – “Giải thích như thể bạn đang dạy một học sinh trung học tài năng”.  
- **Tiếp thị và kinh doanh** – “Viết theo phong cách chuyên nghiệp, ngắn gọn và hướng tới hành động”.

### 3.3 Contextual Prompting: Bí mật của sự liên quan
Contextual prompt cung cấp thông tin nền để mô hình hiểu情境 của yêu cầu.

**Khi không thể thiếu**
- Yêu cầu cần background cụ thể.  
- Đang làm việc trên chủ đề đục chéo hoặc ngành chuyên môn.  
- Cần đầu ra phù hợp với một đối tượng hoặc hoàn cảnh nhất định.  
- Xây dựng dựa trên thông tin trước đó trong một cuộc hội thoại.

**Mẹo профессионал**
1. **Thông tin về đối tượng** – Ai sẽ đọc? Họ biết gì? Họ quan tâm gì?  
2. **Ràng buộc liên quan** – ngân sách, yêu cầu kỹ thuật, khung thời gian …  
3. **Mục tiêu và mục đích** – “Đây là bài trình bán hàng nhằm convencer leadership tăng ngân sách bộ phận”.  
4. **Yếu tố situação** – “Email này cần phục hồi niềm tin sau khi chúng ta hết hạn tuần qua”.  
5. **Điểm dữ liệu cụ thể** – “Cơ sở người dùng đã tăng 23% MoM và đa phần là mobile‑first”.

**Mẫu Contextual Prompt hoạt động mọi lúc**
```
Context: [Bạn là 누구 + thông tin nền liên quan]
Audience: [Đối tượng sẽ nhận + điều họ quan tâm]
Purpose: [Bạn đang cố gắng đạt được gì]
Constraints: [Các hạn chế hoặc yêu cầu]
Tone: [Cảm giác mà người đọc sẽ có]

[Yêu cầu cụ thể của bạn]
```

### 3.4 Kết hợp System, Role, Context
Khi được kết hợp, ba lớp này tạo ra một lớp kiểm soát “đa chiều” giúp mô hình tạo ra đáp ứng vừa chính xác, vừa phù hợp, vừa liên quan.

**Ví dụ thực tế chuyển đổi công việc với khách hàng**
- **System**: Định hình vai trò là chuyên gia trực quan hoá dữ liệu, lưu ý nền tảng kỹ thuật của đối tượng, đòi hỏi khuyến nghị cụ thể dựa trên số liệu.  
- **Role**: Đặt mình làm tư vấn tài chính truyền thông, chuyên giúp startup chỉ ra chỉ số cho nhà đầu tư.  
- **Context**: Miêu tả chính xác hoàn cảnhStartup (SaaS cho công trường, tăng trưởng 15%/ tháng, chi phí获客 tăng).  
- **Yêu cầu cuối**: Cho ba insight quan trọng nhất và hình ảnh minh hoạ phù hợp cho bản trình投資人.

Kết quả thường:
1. **Độ chính xác kỹ thuật** (từ system).  
2. **Phù hợp với trường hợp sử dụng** (từ role).  
3. **Liên quan tới hoàn cảnh cụ thể** (từ context).

### 3.5 Thử nghiệm và cải tiến hệ thống
1. **Kiểm tra từng thành phần riêng** – Xem system, role, context mỗi cái ra sao trước khi ghép.  
2. **Ghi lại mẫu hiệu quả** – Xây dựng thư viện cá nhân các prompt system/role/context cho các loại tác vụ khác nhau.  
3. **Lặp lại dựa trên phản hồi cụ thể** – Điều chỉnh một thành phần mỗi lần để phân biệt tác động.  
4. **Chia sẻ với người khác** – Thử nghiệm hợp tác là cách tốt nhất để tinh tế các kỹ thuật này.

## 4. Ví dụ minh họa

### 4.1 Ví dụ System Prompting – Phản hồi khách hàng
```
You are a product analytics expert who identifies actionable insights from customer feedback. Always categorize issues by severity (Critical, Major, Minor) and by type (UI/UX, Performance, Feature Request, Bug). Be concise and specific.

Analyze this customer feedback:
"I've been using your app for about 3 weeks now. The UI is clean but finding features is confusing. Also crashed twice when uploading photos."
```

### 4.2 Ví dụ Role Prompting – Kỹ sư hiệu suất web
```
I want you to act as a senior web performance engineer with 15 years of experience optimizing high-traffic websites. Explain why my website might be loading slowly and suggest the most likely fixes, prioritized by impact vs. effort.
```

### 4.3 Ví dụ Contextual Prompting – Bài viết trò chơi arcade
```
Context: I run a blog focused on 1980s arcade games. My audience consists mainly of collectors and enthusiasts in their 40s-50s who played these games when they were originally released. They're knowledgeable about the classics but enjoy discovering obscure games they might have missed.

Write a blog post about underappreciated arcade games from 1983-1985 that hardcore collectors should seek out today.
```

### 4.4 Ví dụ Kết hợp – Chuyên gia trực quan hoá dữ liệu + Tư vấn tài chính + Bối cảnh startup
```
System: You are a data visualization expert who transforms complex data into clear, actionable insights. You always consider the target audience's technical background when explaining concepts. Your recommendations should be concrete, specific, and justified by data.

Role: Act as a financial communications consultant who specializes in helping startups explain their business metrics to potential investors.

Context: I'm the founder of a SaaS startup preparing for our Series A funding round. Our product is a project management tool for construction companies. We've been growing 15% month-over-month for the past year, but our customer acquisition cost has been rising. Our investors will be fairly technical but not experts in construction software.

Given these monthly metrics: [metrics data]

What are the 3 most important insights I should highlight in my investor presentation, and what visualization would best represent each one?
```

### 4.5 Ứng dụng thực tế

#### 4.5.1 Trình tạo phản hồi dịch vụ khách hàng
```
System: You generate customer service responses that are empathetic, solution-focused, and align with our brand voice. Always prioritize customer satisfaction while following company policies.

Role: You are a senior customer service representative at a premium outdoor gear company known for exceptional customer relationships. You have 10+ years of experience handling complex customer issues.

Context: Our brand voice is friendly yet professional. We have a generous return policy (90 days, no questions asked), but items must be unused with tags attached. For used items, we offer a 50% store credit.

Customer message: "I bought a jacket from you guys 3 months ago, and the zipper just broke. Can I return it?"
```

#### 4.5.2 Nhà viết tài liệu kỹ thuật
```
System: You create technical documentation that is accurate, concise, and follows a consistent structure. Use clear explanations with examples. Format with markdown.

Role: You are a technical writer with expertise in cloud computing technologies, particularly AWS services. You specialize in writing for technically proficient users who are new to specific services.

Context: This documentation is for a section in our company developer portal explaining how to use our custom logging framework with AWS CloudWatch. Most readers are familiar with CloudWatch but not our proprietary logging tools.

Write a guide on how to set up error alerting using our LogManager class with CloudWatch. Include code examples in Python.
```

#### 4.5.3 Trình tạo nội dung marketing
```
System: You generate marketing content that is engaging, benefit-focused, and tailored to specific audience segments. Always include a clear call to action.

Role: You are a digital marketing specialist who excels at creating content that converts browsers to buyers. You have particular expertise in writing for e-commerce platforms.

Context: Our company sells premium home office furniture. This email campaign targets professionals who have been working from home for 1+ years and have browsed our ergonomic chairs category but haven't purchased. Our primary competitive advantage is our 15-year warranty and free ergonomic consultation.

Write a follow-up email highlighting the long-term health benefits of our ergonomic chairs, addressing common hesitations about price.
```

## 5. Tổng kết
- **System prompting** quy định cách AI hoạt động (định dạng, ràng buộc, tiêu chí).  
- **Role prompting** thay đổi “ai” mà AI tưởng себя là,從而激活领域知识和特定的表达方式。  
- **Contextual prompting** cung cấp thông tin nền, đối tượng, mục tiêu và ràng buộc để làm cho câu trả lời liên quan và có giá trị thực tế.  
- Khi **kết hợp** ba lớp này, bạn có thể tạo ra các prompt mang lại độ chính xác kỹ thuật, độ phù hợp vai trò và mức độ liên quan bối cảnh tối đa.  
- **Thử nghiệm có hệ thống** (kiểm tra riêng, ghi lại mẫu hiệu quả, lặp lại dựa trên phản hồi, chia sẻ với đồng nghiệp) là chìa khóa để thành thạo这些技巧.  

Áp dụng những nguyên tắc trên sẽ giúp bạn chuyển đổi từ “nhiều khi çalış” sang “luôn cung cấp đúng những gì bạn cần” khi làm việc với LLM. Chúc bạn thành công trong hành trình prompt engineering!