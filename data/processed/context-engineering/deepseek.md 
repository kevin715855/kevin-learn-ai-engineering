# DeepSeek – Công ty AI Trung Quốc và ảnh hưởng toàn cầu

## 1. Mục tiêu học tập

Sau khi hoàn thành bài học, người học sẽ có thể:
- Giải thích DeepSeek là gì, thời điểm ra đời và bối cảnh phát triển.
- So sánh DeepSeek với OpenAI về mô hình, giá cả, chính sách mã nguồn mở và cách huấn luyện.
- Mô tả các đổi mới trong quá trình huấn luyện mô hình R1 của DeepSeek (reinforcement learning, reward engineering, distillation, emergent behavior network, hybrid architecture training).
- Liệt kê các phiên bản mô hình chính của DeepSeek từ DeepSeek Coder tới DeepSeek‑V3.1 và đặc điểm nổi bật của mỗi phiên bản.
- Phân tích lý do DeepSeek gây ra “cảnh báo” tại Mỹ và các quốc gia khác, bao gồm rủi ro chi phí, hạn chế về phần cứng, mối đe doạ mô hình kinh doanh và lo ngại về an ninh, quyền riêng tư.
- Nêu các biện pháp cấm hoặc kiểm traDeepSeek mà một số quốc gia và tổ chức đã áp dụng.
- Tóm tắt sự kiện tấn công mạng và rò rỉ dữ liệu mà DeepSeek đã trải qua.

## 2. Tổng quan

DeepSeek là một công ty phát triển AI có trụ sở ở Hangzhou, Trung Quốc, thành lập vào tháng 5 2023 bởi Liang Wenfeng (cũng là đồng sáng lập của quỹ lực lượng mật độ cao High‑Flyer). Mặc dù chưa công bố mức vốn và оценка, DeepSeek nhanh chóng trở thành đối thủ đáng gờm của OpenAI nhờ việc phát hành các mô hình LLM nguồn mở có chi phí phát triển thấp nhưng hiệu suất cao. Mô hình R1, ra đời vào tháng 1 2025, đã khiến DeepSeek vượt过 ChatGPT trong bảng xếp hạng ứng dụng trên Apple App Store và dẫn đến một loạt phản ứng trong thị trường chứng khoán, các lệnh cấm sử dụng tại các cơ quan 정부 và doanh nghiệp, cũng như các sự cố bảo mật.

## 3. Kiến thức cốt lõi

### 3.1. Tổng quan về DeepSeek
- **Thành lập:** 5/2023, Hangzhou, Trung Quốc.  
- **Chủ Liang Wenfeng**, đồng sáng lập quỹ High‑Flyer.  
- **Hoạt động:** Là phòng nghiên cứu AI độc lập dưới hauts của High‑Flyer.  
- **Nhiệm vụ:** Phát triển các LLM nguồn mở, tập trung vào hiệu suất cao với chi phí thấp.

### 3.2. So sánh DeepSeek vs OpenAI

| Tiêu chí | OpenAI | DeepSeek |
|---|---|---|
| **Năm thành lập** | 2015 | 2023 |
| **Trụ sở** | San Francisco, CA, USA | Hangzhou, Trung Quốc |
| **Tập trung phát triển** | Năng lực AI rộng | Mô hình hiệu quả, hầu hết mã nguồn mở |
| **Mô hình nổi bật** | GPT‑4o, o1, GPT‑5 | DeepSeek‑V3, DeepSeek‑R1, DeepSeek‑V3.1 |
| **Mô hình chuyên dụng** | Dall‑E (ảnh), Whisper (giọng) | DeepSeek‑Coder (code), Janus‑Pro (thị giác) |
| **Giá API** (triệu token) | GPT‑5: $1.25 (input), $10 (output) | DeepSeek‑V3.1: $0.56 (input), $1.68 (output) |
| **Chính sách mã nguồn mở** | Hạn chế | Hầu hết mã nguồn mở |
| **Cách huấn luyện** | Giám sát + fine‑tuning dựa trên hướng dẫn | Reinforcement learning (RL) lớn |
| **Chi phí phát triển (ước lượng)** | Trăm triệu USD cho o1 | Dưới $6 triệu cho R1 (theo заявление công ty) |

### 3.3. Các đổi mới trong huấn luyện mô hình R1
1. **Reinforcement learning (RL) lớn** – tập trung vào các tác vụ suy luận, giảm thời gian và số accelerator cần thiết.  
2. **Reward engineering** – xây dựng hệ thống phần thưởng dựa trên quy tắc, outperforms các mô hình phần thưởng neural thông thường.  
3. **Distillation** – nén kiến thức từ mô hình lớn sang các bản nhỏ (1.5 tỷ tham số) mà vẫn giữ được khả năng suy luận.  
4. **Emergent behavior network** – phát hiện ra các mẫu suy luận phức tạp xuất현 tự nhiên qua RL mà không cần lập trình cụ thể.  
5. **Hybrid architecture training (DeepSeek‑V3.1)** – huấn luyện một model đơn để hỗ trợ cả **fast inference** (mode không suy nghĩ) và **deep reasoning** (mode suy nghĩ) thông qua việc đưa *thinking tokens* (∧ và ∨) vào chuỗi token.

### 3.4. Các phiên bản mô hình chính
- **DeepSeek Coder (11/2023)** – mô hình open source đầu tiên, tập trung vào lập trình.  
- **DeepSeek LLM (12/2023)** – phiên bản đầu tiên của mô hình chung.  
- **DeepSeek‑V2 (05/2024)** – cải tiến hiệu suất, giảm chi phí huấn luyện.  
- **DeepSeek‑Coder‑V2 (07/2024)** – 236 tỷ tham số, cửa sổ context 128 K token, dành cho thách thức code phức tạp.  
- **DeepSeek‑V3 (12/2024)** – kiến trúc MoE, 671 tỷ tham số, context 128 K token.  
- **DeepSeek‑R1 (01/2025)** – dựa trên V3, tập trung vào reasoning cao, chi phí thấp.  
- **DeepSeek‑R1‑0528 (05/2025)** – bản cập nhật R1, hỗ trợ system prompt, JSON output, function calling; giảm hallucination, tăng trung bình token mỗi câu hỏi từ 12 K → 23 K.  
- **DeepSeek‑R1‑0528‑Qwen3‑8B** – bản distilled 8 tỷ tham số dựa trên Qwen3, nhằm thiết bị có tài nguyên hạn chế.  
- **Janus‑Pro‑7B (01/2025)** – mô hình visão, hiểu và sinh ảnh.  
- **DeepSeek‑V3.1 (08/2025)** – hybrid model 840 tỷ tham số, hỗ trợ cả thinking và non‑thinking mode, Context 128 K, cải tiến tool calling & agent capabilities.

### 3.5. Lý do DeepSeek gây “cảnh báo” tại Mỹ
- **Gây xáo tron chi phí:** Đ tvr đề phát triển R1 chỉ < $6 triệu, khiến các công ty US đã đầu tư hàng trăm tỷ USD cảm thấy áp lực.  
- **Thành công dù bị hạn chế chip:** Mặc dù cřaus xuất khẩu chip AI cấp cao sang Trung Quốc, DeepSeek vẫn đạt được hiệu suất hàng đầu.  
- ** Đe doạ mô hình kinh doanh:** DeepSeek cung cấp mô hình mở source và miễn phí, trái ngược với mô hình thuê bao trả phí của OpenAI.  
- **Lo ngại địa chính trị:** Vụ rzecz được coi là “Sputnik moment” của AI – sự đột phá của Trung Quốc thách thức dominio công nghệ của Mỹ.  
- **Rủi ro bảo mật & riêng phục:** Dữ liệu người dùng được lưu trữ tại Trung Quốc, tăng nguy cơ rò rỉ đến chính phủ; также mô hình được huấn luyện với góc nhìn Trung Quốc có thể mang thiên trướng.

### 3.6. Các lệnh cấm hoặc kiểm tra DeepSeek
- Cơ quan nước Úc, Chính phủ Trung ́ın Độ (Ấn Độ), Ý, NASA, Bộ Công nghiệp Hàn Quốc, Cơ quan politiche Đài Loan, Chính phủ bang Texas (Mỹ), Hội đồng Congresso Mỹ, Hải quân Mỹ, Bộ quốc phòng Mỹ.  
- EU: Ý (cấm Jan 2025 vì lo ngại GDPR), Đức (cơ quan bảo vệ dữ liệu đề nghị chặn App trên cửa hàng của Apple/Google tại Đức).  
- Nguy cơ cấm rộng khắp EU do vi phạm GDPR & EU AI Act.

### 3.7. Sự cố bảo mật
- **Tấn công mạng (27/01/2025):** Đ 공격을 DDoS lớn nhằm vào API và web chat; DeepSeek giới hạn đăng ký mới nhưng duy trì dịch vụ cho người dùng hiện có; lỗi được sửa vào ngày 28/01.  
- **Rò rỉ dữ liệu (29/01/2025):** Wiz Research phát hiện một cơ sở dữ liệu backend công khai chứa lịch sử chat, khóa API, log streams; DeepSeek lấy dữ liệu offline sau khi được thông báo.  

## 4. Ví dụ minh họa

**Ví dụ 1 – So sánh chi phí API**  
Giả sử một ứng dụng cần xử lý 1 triệu token input và 1 triệu token output.

| Nhà cung cấp | Chi phí input | Chi phí output | Tổng chi phí |
|---|---|---|---|
| OpenAI GPT‑5 | 1 × $1.25 = $1.25 | 1 × $10 = $10 | **$11.25** |
| DeepSeek‑V3.1 | 1 × $0.56 = $0.56 | 1 × $1.68 = $1.68 | **$2.24** |

→ DeepSeek rẻ hơn khoảng **5 lần** cho cùng mức sử dụng.

**Ví dụ 2 – Sử dụng thinking token trong DeepSeek‑V3.1**  
Khi muốn model vào *deep reasoning mode*, chúng ta chèn token `∧` trước câu hỏi và token `∨` sau câu trả lời. Ví dụ:

```
User: ∧ Giải thích nguyên nhân của hiện tượng effet de serre ∨
Model: (trả lời trong режим suy luận sâu, sử dụng nhiều bước reasoning)
```

Nếu không muốn sử dụng chế độ suy luận sâu, đơn giản bỏ qua hai token này → model hoạt động ở *fast inference mode* (trả lời nhanh hơn, ít chi phí tính toán).

## 5. Tổng kết

- DeepSeek là công ty AI Trung Quốc nổi bật với chiến lược phát triển các LLM nguồn mở có chi phí thấp nhưng hiệu suất cao, đặc biệt là mô hình reasoning R1.  
- So với OpenAI, DeepSeek tập trung vào hiệu năng, chi phí phát triển thấp (< $6 triệu), và chính sách mã nguồn mở gần như toàn bộ, trong khi OpenAI nadal đi theo mô hình proprietary và chi phí cao.  
- Các đổi mới trong huấn luyện (reinforcement learning, reward engineering, distillation, emergent behavior network, hybrid architecture) đã giúp DeepSeek đạt được hiệu suất đáng ngờ với ít tài nguyên hơn.  
- Sự thành công của DeepSeek đã làm biến động thị trường, gây ra lo ngại về chi phí, an ninh dữ liệu và địa chính trị tại Mỹ và nhiều nước khác, dẫn tới lệnh cấm hoặc kiểm tra tại nhiều cơ quan pemerintah và doanh nghiệp.  
- Tuy nhiên, DeepSeek cũng đối mặt với những thách thức bảo mật như tấn công DDoS và rò rỉ cơ sở dữ liệu, nhấn mạnh tầm quan trọng của việc bảo vệ hạ tầng và dữ liệu khi triển khai mô hình AI ở quy mô lớn.  

Việc hiểu sâu về DeepSeek giúp người học nắm được xu hướng mới trong ngành AI: sự cạnh tranh giữa các mô hình proprietary và open source, tác động của chi phí phát triển đến mô hình kinh doanh, và những 고려an ninh, pháp lý khi đưa AI vào sử dụng rộng范.