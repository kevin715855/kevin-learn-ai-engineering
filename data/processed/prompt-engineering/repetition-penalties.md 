# Giảm sự lặp lại của LLM bằng các tham số penalty

## 1. Mục tiêu học tập

- Hiểu nguyên nhân khiến mô hình ngôn ngữ lớn (LLM) tạo ra văn bản lặp lại.  
- Nắm ba loại penalty thường dùng: `frequency_penalty`, `presence_penalty` và `repetition_penalty`.  
- Biết cách áp dụng penalty phù hợp với từng tình huống (bài báo dài, bản quảng cáo, hỗ trợ khách hàng, mô hình open‑source).  
- Thực hành tweak các giá trị penalty theo quy trình từng bước và kiểm tra kết quả.  
- Tránh các lỗi phổ biến khi sử dụng penalty và kiểm tra chất lượng đầu ra trước khi triển khai.

## 2. Tổng quan

Khi yêu cầu LLM đưa ra một “giải giải rõ ràng”, ta đôi khi nhận được cùng một câu được diễn đạt theo ba cách khác nhau – μο hình chỉ đơn giản đi theo đường có xác suất cao nhất trong quá trình giải mã (decoding). Sự lặp lại này thường không phải do lỗi ý định mà là do:

1. **Đường giải mã follows the highest‑probability trail** – một khi một cụm từ trở nên có xác suất cao, nó có xu hướng tiếp tục được chọn.  
2. **Dữ liệu huấn luyện chứa rất nhiều mẫu (templates)** – các từ khóa như “therefore”, “in conclusion” xuất hiện thường xuyên và được mô hình học vì chúng “hoạt động” từ góc độ thống kê.  
3. **Prompt không đủ ràng buộc** – khi không xác định định dạng, độ dài hoặc quy tắc trùng lặp, mô hình sẽ “đệm” bằng cách diễn đạt lại chính nó.

Các tham số **penalty** hoạt động như những nút điều chỉnh xác suất: chúng làm giảm xác suất của các token đã xuất hiện, giúp mô hình thoát ra khỏi vòng lặp an toàn và sinh ra ngôn ngữ đa dạng hơn.

## 3. Kiến thức cốt lõi

### 3.1 Frequency penalty  
- **Công thức (OpenAI‑style)**: giảm xác suất của token theo tỷ lệ với số lần token đã xuất hiện.  
- **Ứng dụng**: giảm việc dùng lại cùng một tính từ hoặc cụm từ (“powerful”, “efficient”, “seamless”).  
- **Bắt đầu**:  
  - Văn bản dài: **0.3 – 0.8**  
  - Bản quảng cáo: **0.8 – 1.2** (cẩn thận: giá trị quá cao có thể tạo ra từ lạ).  

### 3.2 Presence penalty  
- **Công thức**:罚对已经出现至少一次的 token（无论出现多少次），鼓励引入新 token /主题。  
- **Ứng dụng**: khi mô hình quay quanh một ý tưởng mà không mở rộng, hoặc khi cần nhiều góc độ khác nhau.  
- **Bắt đầu**: **0.2 – 0.7**.  

### 3.3 Repetition penalty (open‑source)  
- **Công thức (Hugging Face/Transformers)**: nhân hệ số > 1.0 với xác suất của mọi token đã sinh ra; 1.0 = không penalize.  
- **Ứng dụng**: khi chạy các mô hình như LLaMA, Mistral, Qwen ở мест và thấy cụm từ lặp lại literally hoặc “stutter” cho đến giới hạn token.  
- **Bắt đầu**: **1.1 – 1.3**; trên **1.5** có thể gây ra đầu saída “funky” vì là công cụ assez blunt.  

### 3.4 Quy trình tuning thực tiễn  

1. **Sửa prompt trước** (free wins): định dạng đầu ra (bullet list, bảng, bước đánh số), giới hạn từ/số mục, quy tắc “no‑dup”, liền từ không cần thiết (“overall”, “in conclusion”).  
2. **Thêm penalty dần**: tăng mỗi tham số 0.1 mỗi lần và quan sát.  
   - Phrase loops → tăng `frequency_penalty`.  
   - One‑idea spirals → tăng `presence_penalty`.  
   - Open‑source inference → thử `repetition_penalty` trước khi viết lại prompt.  
3. **Đo lường, không chỉ cảm nhận**:  
   - Nếu một câu có thể hoán đổi với câu trước và vẫn có nghĩa →Probably redundant.  
   - Nếu tính từเดียว xuất hiện ≥5 lần trong 300 từ → `frequency_penalty` quá thấp.  

### 3.5 Cài đặt đã được thử nghiệm theo kịch bản  

| Kịch bản | Mục tiêu | `frequency_penalty` | `presence_penalty` | Ghi chú prompt |
|----------|----------|----------------------|--------------------|----------------|
| Báo cáo dài (UK fintech 2026) | Tránh lặp lại cùng một luận điểm | 0.5 – 0.8 | 0.2 – 0.5 | Mỗi phần phải có ít nhất một ví dụ mới; không dùng từ kết nối lặp lại |
| Bản quảng cáo ngắn | Ngắn gọn, không đầy buzzword | 0.9 – 1.2 | 0.1 – 0.4 | Danh sách từ cấm (innovative, cutting‑edge, next‑gen) |
| Hỗ trợ khách hàng (multi‑turn) | Tránh copy/paste instructions | 0.3 – 0.6 | 0.2 – 0.5 | Không lặp lại hướng dẫn đã đưa; chỉ thêm bước còn thiếu; chào hỏi một cụm ngắn mỗi trả lời |
| Mô hình open‑source (stutter) | Khắc phục việc lặp lại literal | `repetition_penalty` 1.15 – 1.30 | – | Kết hợp với temperature/top‑p khi cần |

### 3.6 Ví dụ mã (Node.js)  

```javascript
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const prompt = `
Write a concise UK-focused explanation (max 180 words) of why a council tax account balance
can look higher than expected. Use 4 bullet points. Avoid filler phrases like "overall" or
"in conclusion". Each bullet must introduce a distinct reason.
`;

const res = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: prompt }],
  temperature: 0.6,
  frequency_penalty: 0.7,
  presence_penalty: 0.3
});

console.log(res.choices[0].message.content);
```

**Điều chỉnh**  
- Nếu vẫn thấy cụm từ lặp lại → tăng `frequency_penalty` lên **0.8**.  
- Nếu đầu ra nhảy từ chủ đề này sang chủ đề khác quá nhiều → giảm `presence_penalty` xuống **0.2**.  
- Nếu ngôn ngữ nghe không tự nhiên → giảm cả hai paramètres xuống **0.1**.  

*(Các tham số này thuộc bề mặt API `chat/completions` của OpenAI.)*

### 3.7 Những lỗi thường gặp và cách tránh  

| Lỗi | Mô tả | Cách khắc phục |
|-----|-------|----------------|
| 1. Mục tiêu “không повторений” (zero repetition) | Penalty quá cao khiến mô hình phải tìm từ đồng nghĩa lạ (ex: “this caffeinated beverage” thay vì “coffee”). | Giữ các параметра ở mức trung bình và dựa vào prompt để ràng buộc cấu trúc. |
| 2. Dùng penalty bù đắp cho prompt mơ hồ | Penalty không thay thế được các ràng buộc rõ ràng về định dạng, độ dài, quy tắc. | Đầu tiên làm rõ prompt; sau đó mới áp dụng penalty như “bảo flavor”. |
| 3. Sao chép cài đặt giữa các nhiệm vụ | Cài đặt quảng cáo sẽ làm hỏng bài viết học术 vì cần từ vựng nhất quán. | Tùy chỉnh parameters theo mục tiêu cụ thể của từng tác vụ. |
| 4. Bỏ qua sự khác biệt giữa các mô hình | Mô hình open‑source thường nhạy cảm hơn với repetition control. | Tăng dần và luôn kiểm tra tính liênFisher của văn bản. |

### 3.8 Checklist trước khi triển khai  

- [ ] Prompt có **định dạng** và **giới hạn độ dài** rõ ràng.  
- [ ] Prompt chứa quy tắc **no‑dup** (mỗi điểm phải mang thông tin mới).  
- [ ] Penalty bắt đầu trong **khoảng bảo guard** (conservative range).  
- [ ] Bạn điều chỉnh mỗi tham số theo **bước 0.1**, không nhảy lớn.  
- [ ] Đọc lại output: nó phải **nghe tự nhiên** cho con người, không giống như “từ điển đồng nghĩa” quá度.  

## 4. Ví dụ minh họa (từ mã trên)

Giả sử ta chạy đoạn mã với `frequency_penalty = 0.7` và `presence_penalty = 0.3`. Kết quả có thể trông như sau (dạng bullet points, mỗi пункт ≈ 40‑45 từ, tổng < 180 từ):

- Giá thuế cơ sở của bất động sản có thể đã được tăng nhờ vào việc tái оценка hàng năm do المجلس tempatية thực hiện.  
- Các khoản phí phụ như phí xử lý rác thải, phí bảo vệ môi trường được cộng vào tổng số thanh toán hàng năm.  
- Nếu bạn đã giảm免税额 (ví dụ: đăng ký giảm thuế cho người lớn tuổi) nhưng hồ sơ chưa được cập nhật, số dư sẽ hiển thị cao hơn mức thực tế.  
- Các khoản nợ còn lại từ kỳ thanh toán trước (do thanh toán trễ hoặc lỗi tính费) được tác động lên số dư hiện tại.

Nếu sau khi chạy lại ta thấy cụm từ “cộng vào tổng số thanh toán hàng năm” xuất hiện hai lần, chúng ta tăng `frequency_penalty` lên 0.8 và chạy lại – lần này các câu sẽ được diễn đạt bằng cách khác nhau trong khi vẫn giữ nguyên ý nghĩa.

## 5. Tổng kết

- Sự lặp lại của LLM là hiện tượng tự nhiên do quá trình giải mã xác suất và sự phong phú của mẫu trong dữ liệu huấn luyện.  
- Các tham số penalty (`frequency_penalty`, `presence_penalty`, `repetition_penalty`) là công cụ điều chỉnh xác suất để giảm тенденци лặp lại mà không làm mất đi chất lượng.  
- Hiệu quả nhất khi kết hợp với **prompt có ràng buộc rõ ràng** và thực hiện **bước chỉnh tuning nhỏ bé** (0.1 mỗi lần).  
- Mỗi loại nhiệm vụ (bài báo, bản quảng cáo, hỗ trợ khách hàng, mô hình open‑source) có một khoảng tham số gợi ý; tuy nhiên, luôn cần kiểm tra lại đầu ra bằng mắt người.  
- Tránh các sai lầm thường: không đặt mục tiêu “không có bất kỳ từ lặp nào”, không dùng penalty thay cho prompt tốt, không sao chép cài đặt giữa các nhiệm vụ, và luôn huom着 model‑specific sensitivities.  

Áp dụng những nguyên tắc trên sẽ giúp bạn khiến LNG “ngừng nói nhảm” và bắt đầu tạo ra nội dung **ngắn gọn, đa dạng và hữu ích** cho ứng dụng thực tiễn của mình.