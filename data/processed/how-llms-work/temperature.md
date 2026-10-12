# Nhiệt độ (Temperature) trong Xử lý Ngôn ngữ Tự nhiên và AI  

## 1. Mục tiêu học tập  
Sau bài học người học sẽ:  
- Hiểu khái niệm **temperature** trong mô hình ngôn ngữ lớn (LLM) và tác động của nó đến phân phối xác suất của các token.  
- Giải thích việc tăng nhiệt độ làm “phẳng hoá” đường cong xác suất và vì sao điều này có thể dẫn đến phản hồi sáng tạo hơn nhưng cũng dễ xuất hiện **hallucination** (giả ảo).  
- Xác định cách chọn giá trị temperature phù hợp cho các tác vụ **sách fact‑based** (thật) và **creative** (sáng tạo).  
- Viết một yêu cầu API đơn giản với tham số `temperature` và mô phỏng cách lấy mẫu token dựa trên nhiệt độ bằng Python.  

## 2. Tổng quan  
Khi làm việc với các mô hình sinh văn bản như GPT‑3.5/4, Claude, LLaMA… người dùng thường gặp tham số **temperature** trong body request. Tham số này không đơn giản là “độ sáng tạo” mà có gốc gốc từ lý thuyết thống kê: nó thay đổi **entropy** (độ bất ngờ) của phân phối xác suất mà mô hình dùng để chọn token tiếp theo.  

Bài học này sẽ giải thích:  
- Nhiệt độ hoạt động như thế nào trên phân phối xác suất (ví dụ: làm phẳng đường cong).  
- Ảnh hưởng của nhiệt độ đến chất lượng output (chính xác vs. đa dạng).  
- Nguyên tắc chọn temperature cho các trường hợp sử dụng khác nhau.  

## 3. Kiến thức cốt lõi  

### 3.1. Định dạng probabilístico của LLM  
Khi một LLM đã được huấn luyện, ở mỗi bước sinh nó tính toán một **vector logits** (giá trị thô) cho toàn bộ từ vựng. Sau đó áp dụng hàm **softmax** để chuyển logits thành một phân phối xác suất \(P(token_i) = \frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}}\) trong đó:  
- \(z_i\) là logit của token \(i\).  
- \(\tau\) (tau) là **temperature**.  

Khi \(\tau = 1\) ta получаем phân phối gốc (softmax chuẩn).  

### 3.2. Ảnh hưởng của temperature  
| Giá trị τ | Hiệu ứng trên phân phối | Ý nghĩa thực tiễn |
|----------|------------------------|-------------------|
| τ → 0    | Phân phối tập trung trọng vào token có logit cao nhất (argmax). | Output deterministic, cực kỳ bảo guard, ít đa dạng. |
| τ = 1    | Phân phối như sau khi huấn luyện. | Mức độ “bình thường”. |
| τ > 1    | Phân phối được **làm phẳng** (entropy tăng): các token ít احتمال hơn có cơ hội lớn hơn được chọn. | Output sáng tạo, đa dạng, nhưng có nguy cơ sinh ra token không liên quan → hallucination. |
| τ < 1    | Phân phối **nét nhọn** hơn (entropy giảm): tập trung hơn vào token có xác suất cao. | Output lebih chính xác, ít ng Ngủ, nhưng có thể trở nên lặp đi lặp lại (repetition). |

> **Hallucination** xuất hiện khi mô hình, vì đã “phẳng hoá” phân phối, chọn một token ít khả năng nhưng mà trong ngữ cảnh thực tế là sai.  

### 3.3. Nguyên tắc chọn temperature  
- **Tác vụ fact‑based** (trả lời câu hỏi conocimiento, tóm tắt tài liệu, lấy dữ liệu): dùng **τ thấp** (0.2‑0.5).  
- **Tác vụ creative** (viết truyện, tạo bài thơ, brainstorming ý tưởng): dùng **τ cao** (0.7‑1.0, đôi khi lên tới 1.2 nếu model cho phép).  
- Khi cần **cân bằng**, nhiều người chọn τ ≈ 0.7 làm giá trị mặc định (正如 OpenAI documentation gợi ý).  

### 3.4. Lưu ý về giới hạn  
- Không phải mọi model đều chấp nhận τ > 2; một số model sẽ clip hoặc báo lỗi.  
- Temperature **không** thay đổi kiến thức nội tại của model; nó chỉ ảnh hưởng đến cách chọn từ các khả năng đã có.  

## 4. Ví dụ minh họa  

### 4.1. Gọi API OpenAI với temperature  

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk‑xxxxxxxxxxxxxxxxx" \
  -d '{
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "What is TheNewStack?"}],
        "temperature": 0.7
      }'
```

- Khi `temperature = 0.7` mô hình sẽ tạo ra một câu trả lời có sự cân bằng giữa chính xác và sự tự nhiên.  
- Nếu thay `"temperature": 0.0` → câu trả lời sẽ luôn là token có xác suất cao nhất (thường là câu trả lời ngắn gọn, haìn định).  
- Nếu thay `"temperature": 1.2` → mô hình có thể tạo ra các từ ít thường见 hơn, tăng khả năng sáng tạo nhưng cũng tăng nguy cơ trả lời zawierające bład (hallucination).  

### 4.2. Mô phỏng lấy mẫu token với Python  

```python
import numpy as np

def sample_token(logits, temperature=1.0):
    """
    logits: 1‑d array of raw scores for each token in the vocabulary
    temperature: τ (>0)
    Returns index of the sampled token.
    """
    # Apply temperature scaling
    scaled = logits / temperature
    # Convert to probabilities via softmax (with stability)
    exp_shifted = np.exp(scaled - np.max(scaled))
    probs = exp_shifted / exp_shifted.sum()
    # Sample according to the probability distribution
    return np.random.choice(len(logits), p=probs)

# Example logits for a tiny vocabulary of 5 tokens
logits = np.array([2.0, 0.5, 1.0, 0.2, 0.1])

print("Temperature 0.2 (deterministic-leaning):", sample_token(logits, 0.2))
print("Temperature 1.0 (original distribution):", sample_token(logits, 1.0))
print("Temperature 2.0 (flatter, more random):", sample_token(logits, 2.0))
```

**Giải thích:**  
- Khi τ = 0.2, hàm `sample_token` sẽ rất hay chọn token có logit lớn nhất (index 0).  
- Khi τ = 2.0, phân phối được làm phẳng; các token có logit nhỏ (index 3,4) có xác suất tăng đáng kể, do đó có thể được chọn.  

## 5. Tổng kết  
- **Temperature** là tham số điều chỉnh entropy của phân suất token trong LLMs; giá trị thấp làm nhọn phân phối (deterministic), giá trị cao làm phẳng phân phối (creative).  
- Việc tăng temperature zwiększa szanse na wybór mniej prawdopodobnych tokenów, co może prowadzić do **hallucinations** gdy model generuje faktualną zawartość.  
- Dựa trên mục tiêu bài toán, chọn temperature phù hợp:  
  - **Fact‑based / chính xác:** τ ≈ 0.2‑0.5  
  - **Sáng tạo / đa dạng:** τ ≈ 0.7‑1.0 (có thể lên tới 1.2 nếu model cho phép).  
- Hiểu cơ chế này giúp lập trình viên điều chỉnh output của LLM một cách có chủ đích, giảm thiểu lỗi không mong muốn và tận dụng sức mạnh sinh văn bản của mô hình.