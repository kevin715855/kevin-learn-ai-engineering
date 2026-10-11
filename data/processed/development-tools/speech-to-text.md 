# Speech to Text – Chuyển đổi giọng nói thành văn bản

## 1. Mục tiêu học tập
Sau bài học này, bạn sẽ能够:
- Giải thích **speech to text** (STT) là gì và nguyên lý hoạt động cơ bản của nó.
- Nêu được hai loại chính của công nghệ STT và sự khác biệt giữa chúng.
- Liệt kê các ứng dụng thực tiễn phổ biến của STT trong các ngành như Marketing, Ngân hàng, Y tế.
- Đánh giá lợi ích và hạn chế của STT trong thực tế.
- Áp dụng các tiêu chí để lựa chọn phần mềm STT miễn phí hay trả phí phù hợp với nhu cầu.
- Thực hiện một quy trình đơn giản để chuyển đổi audio thành text bằng **Amazon Transcribe** (AWS).

## 2. Tổng quan
Speech to text (STT), còn được gọi là *speech recognition* hoặc *computer speech recognition*, là công nghệ sử dụng mô hình học máy để biến tín hiệu âm thanh (giọng nói) thành chuỗi ký tự Unicode có thể đọc được. STT đang được triển khai rộng rãi từ các tính năng dictation trên điện thoại thông minh đến các giải pháp chuyên ngành như phân tích cuộc gọi, phụ đề video và ghi âm y khoa. Bài học sẽ cung cấp kiến thức nền tảng về cách STT hoạt động, những loại công nghệ chính, ứng dụng thực tế, và cách bắt đầu sử dụng dịch vụ Amazon Transcribe trên nền tảng AWS.

## 3. Kiến thức cốt lõi

### 3.1 Định nghĩa và nguyên lý hoạt động
- **Speech to text** là phần mềm nhận dạng giọng nói, chuyển đổi tín hiệu âm thanh thành văn bản có thể chỉnh sửa.
- Quy trình cơ bản bao gồm:
  1. **Thu thập tín hiệu âm thanh** → rung động từ nguồn phát âm.
  2. **Analog‑to‑Digital Converter (ADC)** chuyển đổi tín hiệu liên tục thành mẫu số离散.
  3. **Lọc và phân đoạn** âm thanh thành các khung thời gian ngắn (hh/millisec).
  4. **Trích xuất phoneme** – đơn vị âm thanh phân biệt các từ trong ngôn ngữ.
  5. **So sánh phoneme** với mô hình ngôn ngữ (thông thường là mạng neural hoặc HMM) để dự đoán chuỗi từ nhất có khả năng.
  6. **Đưa ra đầu ra** dưới dạng văn bản Unicode.

### 3.2 Hai loại chính của STT
| Loại | Đặc điểm | Ứng dụng thường gặp |
|------|----------|----------------------|
| **Speaker‑dependent** | Huấn luyện trên giọng nói của một người cụ thể → độ Accuracy cao khi người dùng đã training. | Phần mềm dictation cá nhân (Dragon NaturallySpeaking,Built‑in dictation trên Windows/macOS). |
| **Speaker‑independent** | Không phụ thuộc vào người nói → được xây dựng trên dữ liệu đa dạng. | Ứng dụng điện thoại, dịch vụ đám mày (Amazon Transcribe, Google Speech‑to‑Text). |

### 3.3 Ứng dụng thực tiễn
- **Call analytics & agent assist**: Trích xuất insights từ cuộc gọi khách hàng (Amazon Transcribe Call Analytics).
- **Media content search & subtitling**: Chuyển đổi audio/video thành text để tạo phụ đề, tìm kiếm nội dung (kết hợp với Amazon Translate).
- **Clinical documentation**: Amazon Transcribe Medical ghi âm cuộc trò chuyện y khoa vào EHR.
- **Ngân hàng & dịch vụ khách hàng**: Voice‑activated IVR, xác thực bằng giọng nói.
- **Marketing**: Phân tích accent, từ vựng để hiểu hành vi người tiêu dùng.

### 3.4 Lợi ích
- **Tiết kiệm thời gian**: Bản ghi âm được transcript ngay lập tức.
- **Hiệu quả chi phí**: Giá thuê dịch vụ STT thường thấp hơn thuê người biên dịch rę.
- **Nâng cao truy cập**: Phụ đề, transcript giúp người khiếm thính và tìm kiếm nội dung dễ dàng.
- **Cải thiện trải nghiệm khách hàng**: Tích hợp NLU để hiểu ý định và cung cấp phản hồi nhanh.

### 3.5 Hạn chế
- **Không hoàn hảo**: Độ lỗi phụ thuộc vào chất lượng âm thanh, accent, tiếng nền.
- **Cần can thiệp con người**: Đôi khi cần chỉnh sửa sau khi transcript để đạt độ chính xác mong muốn.
- **Yêu cầu bản ghi sạch**: âm thanh phải rõ ràng, một người nói mỗi lúc, ít tiếng background, phát âm chuẩn.

### 3.6 Tiêu chí lựa chọn phần mềm STT
1. **Không cần phần mềm phụ thuộc** – giải pháp dựa trên web/API chỉ cần kết nối internet.
2. **Mức độ Accuracy được cam kết** – nhà cung cấp thường công bố WORD ERROR RATE (WER).
3. **Hỗ trợ đa ngôn ngữ** – quan trọng nếu xử lý âm thanh đa ngữ.
4. **Tương thích với ứng dụng** – SDK hoặc API có thể tích hợp vào mobile/web app.
5. **Chi phí & hỗ trợ** – so sánh gói miễn phí (giới hạn lượng audio, ít hỗ trợ) với gói trả phí (độ chính xác cao, SLA).

### 3.7 Sử dụng Amazon Transcribe để chuyển đổi giọng nói thành văn bản
**Quy trình cơ bản:**
1. **Tạo tài khoản AWS** (nếu chưa có) và mở dịch vụ **Transcribe** trong AWS Management Console.
2. **Upload file audio** lên Amazon S3 (định dạng được hỗ trợ: wav, mp3, flac, …).
3. **Tạo một transcription job** (có thể qua Console, AWS CLI hoặc SDK).
4. **Chờ job hoàn thành**, sau đó tải kết quả transcript (định dạng JSON) từ S3.

**Ví dụ sử dụng AWS CLI** (giả sử bucket `my‑audio‑bucket` và file `speech.wav`):
```bash
aws transcribe start-transcription-job \
    --transcription-job-name my-speech-job \
    --media MediaFileUri=s3://my-audio-bucket/speech.wav \
    --output-key my-speech-job/ \
    --language-code en-US
```
- `transcription-job-name`: tên eindeutigung của job.
- `MediaFileUri`: đường dẫn tới file audio trên S3.
- `output-key`: nơi lưu file kết quả (JSON) sau khi xử lý.
- `language-code`: mã ngôn ngữ (ví dụ `en-US`, `vi-VN`).

Kết quả JSON chứa trường `Transcript` với văn bản đã được chuyển đổi, đồng thời metadata như thời gian bắt đầu/kết thúc của từng từ (nếu bậtEnable speaker diarization).

**Lưu ý:** Để miễn phí trong tier free, AWS cung cấp 60 phút audio transcription miễn phí mỗi tháng trong 12 tháng đầu. Vượt mức này sẽ được tính phí theo lượng audio thực tế.

## 4. Ví dụ minh họa
**Trong phần này, chúng ta minh họa cách sử dụng Amazon Transcribe để chuyển đổi một đoạn ghi âm cuộc gọi khách hàng thành text và sau đó trích xuất từ khóa liên quan tới “giá cả”.**

1. Chuẩn bị file audio `call-record.mp3` và upload lên S3.
2. Chạy lệnh CLI như trên với `--language-code vi-VN` (giả sử Gespräch bằng tiếng Việt).
3. Khi job hoàn thành, tải file `my-speech-job.json` về và truy cập:
   ```json
   {
     "results": {
       "transcripts": [{"transcript": "Xin chào, bạn có thể cho tôi biết giá của sản phẩm này không?"}],
       ...
     }
   }
   ```
4. Văn bản được trích xuất (`"transcript"`) hiện có thể dùng cho các bước tiếp theo như tìm kiếm từ khóa, phân tích cảm xúc, hoặc tạo báo cáo cho trung tâm gọi.

**Kết quả minh họa** cho thấy STT không chỉ tạo ra bản ghi chữ mà còn làm nền tảng để thực hiện các tác vụ phân tích nâng cao mà không cần nhập tay.

## 5. Tổng kết
- Speech to text là công nghệ chuyển đổi âm thanh thành văn bản dựa trên mô hình học máy và xử lý tín hiệu.
- Nó gồm hai loại chính: *speaker‑dependent* (độ cao cá nhân) và *speaker‑independent* (đa dụng, thường dùng trên đám mây).
- Ứng dụng rộng范围 từ trung tâm gọi, nội dung media, tới y tế và ngân hàng.
- Lợi ích chính là tiết kiệm thời gian, giảm chi phí, tăng khả năng truy cập và cải thiện trải nghiệm người dùng; hạn chế bao gồm phụ thuộc vào chất lượng âm thanh và cần can thiệp con người.
- Khi chọn phần mềm STT, cần xem xét độ chính xác, hỗ trợ ngôn ngữ, sự không cần phần mềm phụ đề, và chi phí/hỗ trợ.
- Amazon Transcribe cung cấp một cách dễ dàng và có thể mở rộng để triển khai STT trên AWS; một đơn giản lệnh CLI hoặc gọi API đủ để bắt đầu một transcription job và nhận kết quả JSON để xử lý tiếp.

Những điểm trên sẽ giúp bạn nắm vững cơ bản về speech to text và biết cách áp dụng chúng vào dự án thực tế của mình. Hãy tiếp tục khám phá các tính năng nâng cao của Amazon Transcribe như **Call Analytics**, **Medical Transcription**, hoặc **speaker diarization** để tối ưu hoá giải pháp của bạn.