# Lỗi trong quản lý context của mô hình LLM và tác động đến AI Agents  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ:  

- Hiểu tại sao việc tăng kích thước context window không tự động nâng cao chất lượng phản hồi của mô hình.  
- Nhận diện bốn dạng lỗi context phổ biến: **Context Poisoning**, **Context Distraction**, **Context Confusion**, **Context Clash**.  
- Giải thích nguyên nhân và manifesta­tion cụ thể của từng loại lỗi qua các nghiên cứu và ví dụ thực tế.  
- Nhận ra tại sao AI agents (đặc biệt là những agents thực hiện luồng trabalho đa bước) dễ bị ảnh hưởng bởi các lỗi này.  

## 2. Tổng quan  

Các mô hình LLM hiện đại (ví dụ: Gemini 2.5, GPT‑4.1) đã mở rộng context window lên tới 1 triệu token, khiến nhiều người nghĩ rằng cukup “ném vào prompt” mọi thứ cần thiết – công cụ, tài liệu, hướng dẫn – và mô hình sẽ tự xử lý. Tuy nhiên, context quá lớn không chỉ không giúp mà còn tạo ra cácfailure mode mới. Khi context được “ngập” bằng thông tin không liên quan, sai lệch hoặc противореч información, mô hình có thể:  

- Nhận lầm thông tin sai (hallucination) như là thật và lặp lại nó (context poisoning).  
- Tập trung quá mức vào lịch sử context thay vì sử dụng kiến thức từ pretraining (context distraction).  
- Sử dụng thông tin thừa để sinh phản hồi kém chất lượng (context confusion).  
- Xử lý những phần context mâu thuẫn với nhau, dẫn đến suy luận sai lầm (context clash).  

Các hiện tượng này đặc biệt nguy hiểm đối với AI agents vì chúng thường thu thập context từ nhiều nguồn, thực hiện nhiều lượt gọi công cụ và duy trì lịch sử tương tác dài.  

## 3. Kiến thức cốt lõi  

### 3.1 Context Poisoning (Nhiễm context)  
- **Định nghĩa**: Một hallucination hoặc lỗi nào đó đi vào context và được trích dẫn lại nhiều lần.  
- **Tác động**: Mô hình có thể “bị stał” trên mục tiêu không thể đạt được hoặc không liên quan, lặp lại hành động sai.  
- **Ví dụ**: Trong nghiên cứu Gemini 2.5 playing Pokémon, agent thường hallucinate về trạng thái trò chơi; thông tin sai này đi vào phần “goals” của context, khiến agent phát triển chiến lược vô nghĩa và không thể hồi phục.  

### 3.2 Context Distraction (Phân tâm context)  
- **Định nghĩa**: Khi context tăng dài, mô hình thay vì sử dụng kiến thức từ pretraining, lại 집중 quá nhiều vào lịch sử context đã tích lũy.  
- **Tác động**: Mô hình tendencia lặp lại các hành động trước đó thay vì sinh ra kế hoạch mới.  
- **Cú pháp**: Đối với Gemini 2.5 Pro (context > 1 triệu token), hiện tượng nổi bật sau khoảng 100 k token; mô hình bevorzugt cácaction lặp lại từ lịch sử.  
- **Mô hình nhỏ**: Nghiên cứu Databricks cho thấy mức độ suy giảm độ chính xác bắt đầu khoảng 32 k token cho Llama 3.1 405B và còn thấp hơn đối với các model nhỏ hơn.  

### 3.3 Context Confusion (Nhầm lẫn context)  
- **Định nghĩa**: Nội dung thừa (ví dụ: danh sách công cụ không liên quan) được mô hình lấy vào account và làm giảm chất lượng phản hồi.  
- **Tác động**: Mô hình có thể gọi công cụ không phù hợp hoặc sinh ra đáp án không liên quan vì phải “lưu ý” tới mọi thứ trong context.  
- **Chứng minh**: Berkeley Function‑Calling Leaderboard cho thấy mọi model giảm hiệu suất khi được cung cấp hơn một công cụ; khi số công cụ tăng (ví dụ: 46 công cụ trên GeoEngine benchmark), model Llama 3.1 8b (quantized) thất bại, nhưng thành công khi chỉ có 19 công cụ.  

### 3.4 Context Clash (Xung đột context)  
- **Định nghĩa**: Hai hoặc nhiều phần trong context chứa thông tin mâu thuẫn với nhau.  
- **Tác động**: Mô hình dựa vào các giả thiết sớm (sai) và không thể chỉnh sửa khi позже nhận được thông tin đúng.  
- **Ví dụ**: Nghiên cứu Microsoft/Salesforce sử dụng “sharded prompts” – chia thông tin ban đầu thành nhiều tin nhắn연속. Khi mô hình phải tổng hợp từ các turn eerder, nó giữ lại các đáp án sai lầm từ turn đầu và chúng ảnh hưởng đến câu trả lời cuối cùng, provocando giảm trung bình 39 % điểm số (o3 từ 98,1 xuống 64,1).  

### 3.5 Tác động tổng thể lên AI Agents  
- Agents thường **thu thập context** từ: tài liệu, kết quả công cụ, phản hồi của sub‑agents, và lịch sử trò chuyện.  
- Mỗi nguồn tiềm tàng có thể giới thiệu một trong các lỗi trên.  
- Khi context “ngập”, agents có thể:  
  - Lặp lại hành động cũ (distraction).  
  - Tiêu diệt mục tiêu do hallucination (poisoning).  
  - Gọi công cụ không cần thiết (confusion).  
  - Ra quyết định dựa trên giả thiết mâu thuẫn (clash).  

## 4. Ví dụ minh họa  

### 4.1 Context Poisoning – Agent Pokémon  
```text
Context (rút gọn):
- Goal: Defeat Gym Leader Brock using Water‑type Pokémon.
- Summary: Agent believes it already has a Squirtle (hallucination).
- Observation: Enemy Brock uses Geodude.
```
Khi agent suy luận dựa trên mục tiêu “poisoned”, nó liên tục chọn Squirtle (which it doesn’t have) và thất bại lặp đi lặp lại.  

### 4.2 Context Distraction – Gemini 2.5 Pro  
- Khi chat quá 100 k token, agent bắt đầu **lặp lại** hành động cuối cùng trong lịch sử (ví dụ: continuamente “look around”) thay vì tạo ra kế hoạch mới để vượt qua thử thách.  

### 4.3 Context Confusion – Công cụ dư thừa  
- Prompt chứa mô tả của 46 công cụ khác nhau (file‑search, calculator, email‑sender, …).  
- Model Llama 3.1 8b (quantized) khi được hỏi “What is the capital of France?” trả về một lời gọi công cụ **email‑sender** với nội dung không liên quan, làm giảm độ chính xác.  
- Khi giảm số công cụ xuống 19, model trả về đúng “Paris” mà không gọi bất kỳ công cụ nào.  

### 4.4 Context Clash – Sharded Prompt  
- Turn 1: “What is 2+2?” → Agent trả lời “4”.  
- Turn 2: “Now multiply the result by 3.” → Agent (dựa trên context đã có “4”) trả lời “12”.  
- Tuy nhiên, vì context còn chứa câu trả lời sai từ một phiên bản trước (ví dụ: agent曾 hallucinate “5” ở turn 0), sau khi tổng hợp, cuối cùng agent cho ra “15” thay vì “12”.  

## 5. Tổng kết  

- Mở rộng context window mang lại khả năng lưu trữ nhiều thông tin, nhưng không bảo证 chất lượng suy luận tốt hơn.  
- Ba lỗi chính – **poisoning**, **distraction**, **confusion** – xuất hiện khi context chứa thông tin sai, thừa hoặc khiến mô hình tập trung quá mức vào lịch sử thay vào kiến thức từ pretraining.  
- **Context clash** là dạng lỗi nghiêm trọng hơn khi các phần trong context mâu thuẫn, gây ra giả thiết sai lầm khó khắc phục.  
- AI Agents đặc biệt dễffected vì họ tự động xây dựng context đa nguồn và đa luồng.  
- Các biện pháp giảm thiểu (dynamic tool loading, context quarantine, summarization selective, …) sẽ được đề cập trong bài viết tiếp theo “How to Fix Your Context”.  

**Lưu ý quan trọng**: Khi xây dựng hoặc sử dụng LLM‑based agents, luôn kiểm soát kích thước và chất lượng nội dung được umieszczeno vào context; việc “thêm tất cả” không phải là giải pháp tối ưu.