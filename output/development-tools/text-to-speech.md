# Amazon Polly – Dịch vụ AI Text‑to‑Speech

## 1. Mục tiêu học tập

- Mô tả Amazon Polly là gì và cách hoạt động của nó.  
- Liệt kê các tính năng chính: giọng sống động, tùy chỉnh đầu ra (SSML & lexicon), sức mạnh Gen AI, bảo mật và kiểm soát.  
- Nêu các trường hợp sử dụng thực tế phổ biến.  
- Giải thích mô hình giá và các ưu đãmi miễn phí / free tier hiện tại.  
- Thực hiện một ví dụ đơn giản gọi API Polly để tạo file âm thanh bằng Python (boto3).  

## 2. Tổng quan

Amazon Polly là dịch vụ hoàn toàn quản lý của Amazon Web Services (AWS) chuyển đổi bất kỳ chuỗi văn bản nào thành luồng âm thanh bằng cách dùng các mô hình học sâu (neural network) và voice engine hiện đại. Dịch vụ cung cấp hàng chục ngôn ngữ, nhiều giọng nam/nữ, cho phép nhà phát triển tích hợp khả năng “nói” vào ứng dụng web, mobile, thiết bị IoT hoặc hệ thống IVR mà không cần quản lý cơ sở hạ tầng phức tạp.

## 3. Kiến thức cốt lõi

### 3.1 Nguyên lý hoạt động

1. **Nhập dữ liệu** – Văn bản dưới dạng plain text hoặc SSML (Speech Synthesis Markup Language) được gửi tới Polly qua API `synthesize_speech`.  
2. **Xử lý** – Polly chạy một voice engine (chuẩn hoặc neural) dựa trên transformer billions‑parameter để tạo ra sóng âm thanh từ đầu vào.  
3. **Đầu ra** – Kết quả là một luồng âm thanh trong các định dạng chuẩn: **MP3**, **OGG**, hoặc **PCM** (tần số mẫu 8 kHz, 16 kHz, 22.05 kHz).  

### 3.2 Thành phần quan trọng

| Thành phần | Mô tả |
|-----------|-------|
| **Voice (giọng nói)** | Được ghi lại từ người bản địa, có nhiều lựa chọn nam/nữ và các biến thể ngôn ngữ ( >100 giọng, >40 ngôn ngữ). |
| **SSML** | Ngôn ngữ đánh dấu cho phép thay đổi **pause**, **emphasis**, **pitch**, **rate**, và **pronunciation** bằng các thẻ như `<break>`, `<emphasis>`, `<prosody>`, `<say-as>`. |
| **Custom Lexicon** | Từ điển tuỳ chỉnh để thay đổi cách phát âm của viết tắt, tên thương hiệu, thuật ngữ chuyên ngành. |
| **Voice Engine** | - **Standard**: giọng truyền thống.<br>- **Neural (Gen‑AI)**: sử dụng mô hình transformer lớn để tạo ra giọng nói cảm xúc, Coloquial và streamable. |
| **Bảo mật & kiểm soát** | Polly không lưu trữ nội dung văn bản sau khi xử lý. Đầu ra âm thanh có thể lưu trữ, cache, hoặc phát lại mà không tốn phí extra. Định dạng chuẩn giúp tích hợp dễ dàng vào S3, CloudFront, hoặc các hệ thống phát stream. |

### 3.3 Mô hình giá

- **Free tier 12 tháng** – Mỗi tài khoản mới nhận được lượng ký tự miễn phí tùy theo voice engine (từ 100 000 đến 5 000 000 kýтри).  
- **Sau free tier** – Tính phí theo số ký tự xử lý (giá różn theo engine và định dạng xuất).  
- **Free Tier crédits từ 15/07/2025** – Khách AWS mới có thể nhận được tới **$200** crédit áp dụng cho dịch vụ như Amazon Polly, có hiệu lực 12 tháng kể từ ngày tạo tài khoản.  

### 3.4 Trường hợp sử dụng tiêu biểu

- **Đọc bài báo, e‑learning, audiobook** – chuyển văn bản thành audio để người dùng “nghe” thay vì đọc.  
- **Hệ thống IVR & hotline** – tạo phản hồi thoại động cho cuộc gọi khách hàng.  
- **Dubbing & trò chơi** – tạo voice‑over cho animation, video game, hoặc video quảng cáo.  
- **Ứng dụng IoT** – cung cấp phản hồi voix cho thiết bị智能家居, wearable, hoặc robot.  
- **Truy cập & hỗ trợ người khuyết tật** – tạo phiên bản audio của nội dung web để hỗ trợ người với проблемы зрения hoặc dyslexia.  

## 4. Ví dụ minh họa

### 4.1 Chuẩn bị

- Tài khoản AWS có quyền truy cập Amazon Polly.  
- Cài đặt AWS CLI hoặc SDK; ở đây dùng **boto3** (Python).  
- Cấu hình credentials: `aws configure` (Access Key, Secret Key, region – ví dụ `us-east-1`).  

### 4.2 Mã Python – synthesize speech thành file MP3

```python
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def synthesize_polly(text: str,
                    voice_id: str = 'Joanna',
                    output_format: str = 'mp3') -> str | None:
    """
    Gọi Amazon Polly để chuyển văn bản thành file âm thanh.
    Trả về đường dẫn file nếu thành công, ngược lại trả về None.
    """
    polly = boto3.client('polly', region_name='us-east-1')
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
            # Nếu dùng SSML: thay Text bằng chuỗi SSML và thêm TextType='ssml'
        )
    except (BotoCoreError, ClientError) as err:
        print(f"Lỗi khi gọi Polly: {err}")
        return None

    if "AudioStream" in response:
        out_file = "output.mp3"
        with open(out_file, "wb") as f:
            f.write(response["AudioStream"].read())
        print(f"Đã tạo file âm thanh: {out_file}")
        return out_file
    else:
        print("Không nhận được AudioStream từ Polly")
        return None

if __name__ == "__main__":
    sample = ("Chào buổi sáng! Đây là ví dụ sử dụng Amazon Polly "
              "để tạo ra giọng nói tự nhiên bằng Python.")
    synthesize_polly(sample, voice_id='Joanna')
```

**Giải thích nhanh:**

- `synthesize_speech` là API chính của Polly.  
- `VoiceId` chọn giọng (ví dụ: Joanna – giọng nữ Mỹ).  
- `OutputFormat` xác định định dạng file (mp3, ogg, pcm).  
- Để dùng SSML, thay `Text` bằng chuỗi SSML và thêm tham số `TextType='ssml'`.  

### 4.3 Ví dụ sử dụng SSML để tinh chỉnh

```xml
<speak>
    Xin chào <break time="300ms"/> các bạn.
    <emphasis level="moderate">Amazon Polly</emphasis> có thể tạo ra
    <prosody rate="slow" pitch="+2st">giọng nói</prosody> tự nhiên.
</speak>
```

Khi truyền chuỗi trên với `TextType='ssml'`, Polly sẽ:

- Thêm một **pause** 300 ms sau “Xin chào”.  
- Đánh dấu mạnh *Amazon Polly*.  
- Giảm tốc độ đọc và nâng cao pitch 2 semitone cho cụm từ “giọng nói”.  

## 5. Tổng kết

- **Amazon Polly** là dịch vụ TTS hoàn toàn quản lý của AWS, dựa trên mạng neural để tạo ra giọng nói gần giống người thật.  
- Hỗ trợ **nhiều ngôn ngữ và giọng nói**, cho phép **tùy chỉnh** qua SSML và lexicon tuỳ chỉnh.  
- **Voice engine neural (Gen‑AI)** cung cấp chất lượng cao, cảm xúc và khả năng stream.  
- **Bảo mật**: không lưu trữ văn bản đầu ra, chỉ giữ âm thanh dưới dạng các định dạng chuẩn (MP3/OGG/PCM).  
- **Mô hình giá**: free tier 12 tháng (hoặc up to $200 crédito từ 07/2025), sau đó tính phí theo ký tự.  
- **Triển khai đơn giản** qua AWS SDK (boto3, AWS CLI, etc.) – ví dụ trên cho thấy chỉ cần vài dòng mã để tạo file âm thanh.  

Với những kiến thức trên, bạn đã có thể bắt đầu tích hợp Amazon Polly vào các ứng dụng AI‑engineering như hệ thống IVR, audio‑content, trò chơi, hoặc thiết bị IoT để mang lại trải nghiệm tương tác bằng giọng nói tự nhiên và hiệu quả.