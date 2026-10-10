# Data Classification – Nguyên tắc và ứng dụng trong bảo mật dữ liệu  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ có thể:  

- Giải thích **Data Classification** là gì và tại sao nó là bước đầu tiên trong việc bảo mật dữ liệu.  
- Mô tả quy trình thực hiện data classification (xây dựng schema, phân loại tự động & thủ công).  
- Liệt kê các cấp độ phân loại phổ biến (public, internal use, restricted, confidential, archived) và ví dụ dữ liệu thuộc từng cấp độ.  
- Nêu rõ vai trò của data classification trong việc **đánh giá rủi ro, kiểm soát truy cập, mã hoá, sao lưu&phục hồi và tuân thủ** các quy định (GDPR, HIPAA, PCI DSS, v.v.).  
- Áp dụng kiến thức vào một tình huống thực tế để đưa ra biện pháp bảo mật phù hợp với mỗi loại dữ liệu.  

## 2. Tổng quan  

Data classification (phân loại dữ liệu) là việc sắp xếp và gán nhãn dữ liệu dựa trên mức độ nhạy cảm, mức độ quan trọng và các tiêu chuẩn được xác định trước. Khi dữ liệu được phân loại, tổ chức có thể:

- Tập trung nguồn lực vào những assets nhạy cảm nhất.  
- Áp dụng biện pháp bảo mật (mã hoá, kiểm soát truy cập, sao lưu…) phù hợp với mỗi nhóm dữ liệu.  
- Đảm bảo tuân thủ các quy định về bảo mật và quyền riêng tư.  

Trong bối cảnh bảo mật hiện đại, data classification thường được tích hợp vào các giải pháp **Data Security Posture Management (DSPM)** để tự động quét, phân loại và giám sát liên tục dữ liệu trên môi trường đám mây.  

## 3. Kiến thức cốt lõi  

### 3.1. Định nghĩa và cách hoạt động  

1. **Xây dựng schema phân loại** – xác định các danh mục (ví dụ: public, internal use, restricted, confidential) và tiêu chí cho mỗi danh mục (nhạy cảm, pháp lý, giá trị kinh doanh…).  
2. **Khám phá dữ liệu** – quét các tài sản dữ liệu có cấu trúc và không cấu trúc (cơ sở dữ liệu, file share, storage đám mây…).  
3. **Gán nhãn** – dựa trên nội dung, siêu dữ liệu hoặc quy tắc xác định trước, mỗi đối tượng dữ liệu nhận được một mức độ phân loại. Quy trình có thể tự động (bằng giải pháp DSPM sử dụng AI/ML) hoặc thủ công (chuyên gia đánh giá khi cần chuyên môn sâu).  
4. **Áp dụng biện pháp bảo mật** – sau khi gán nhãn, tổ chức triển khai các biện pháp tương ứng (mã hoá, kiểm soát truy cập, chính sách sao lưu…) cho mỗi mức độ.  

> **Lưu ý**: Các thuật ngữ quan trọng như **PII** (Personally Identifiable Information), **PHI** (Protected Health Information), **PCI DSS** (Payment Card Industry Data Security Standard), **GDPR**, **HIPAA** đều được nhắcถึง trong phần “Tại sao data classification quan trọng” vì chúng là các loại dữ liệu hoặc tiêu chuẩn thường bị yêu cầu bảo mật đặc biệt.  

### 3.2. Tại sao data classification quan trọng?  

- **Bảo vệ thông tin nhạy cảm** – PII, PHI, dữ liệu tài chính,secret thương mại… dễ bị l용 dụng nếu không được bảo vệ đúng cách.  
- **Hỗ trợ tuân thủ pháp luật** – Quy định như GDPR (phạt до 4 % doanh số toàn cầu), HIPAA, PCI DSS yêu cầu tổ chức phải biết nơi dữ liệu cá nhân/ sức khỏe/ thanh toán được lưu trữ và áp dụng biện pháp bảo mật thích hợp.  
- **Tối ưu hoá nguồn lực** – Tập trung chi phí bảo mật vào dữ liệu có mức độ rủi ro cao, tránh lãng phí trên dữ liệu công khai ít nguy hiểm.  
- **Cơ sở cho các quy trình bảo mật khác** – Dễ dàng建立 chính sách access control, mã hoá, sao lưu và phản hồi sự kiện khi biết claramente mức độ nhạy cảm của mỗi tài sản.  

### 3.3. Các cấp độ phân loại phổ biến  

| Cấp độ | Mô tả | Ví dụ dữ liệu |
|--------|-------|---------------|
| **Public** | Dữ liệu không nhạy cảm, có thể chia sẻ tự do. | Bản tin báo chí, tài liệu marketing công khai. |
| **Internal Use Only** | Dữ liệu nội bộ, không công khai nhưng không ảnh hưởng nghiêm trọng nếu rò rỉ. | Bản ghi lương, ghi chú họp nội bộ, kế hoạch dự án nội bộ. |
| **Restricted** | Dữ liệu có mức độ nhạy cảm trung bình; cần kiểm soát truy cập. | Thông tin khách hàng (không chứa PII), kế hoạch marketing, bảng giá nội bộ. |
| **Confidential** | Dữ liệu rất nhạy cảm, phải được bảo vệ ở mức cao nhất. | PII, PHI, thông tin thẻ thanh toán, secret thương mại, tài liệu tài chính chi tiết. |
| **Archived** | Dữ liệu không còn được sử dụng thường xuyên nhưng phải giữ lại vì lý do pháp lý, lịch sử hoặc व्यवसाय. | Báo cáo tài tính cũ, hồ sơ nhân viên đã nghỉ việc. |

> Các cấp độ có thể được tùy chỉnh tuỳ theo ngành (ví dụ: trong y tế có thể thêm “PHI‑Restricted”, trong tài chính có thêm “PCI‑DSS‑Confidential”).  

### 3.4. Các trường hợp sử dụng (Use Cases) thường gặp  

- **Personally Identifiable Information (PII)** – họ tên, số CMND/CCCD, số tài khoản ngân hàng, email, số điện thoại.  
- **Protected Health Information (PHI)** – bản ghi y tế, kết quả chẩn đoán, předpis thuốc, thông tin bảo hiểm y tế.  
- **Financial Data** – số thẻ tín dụng, số tài khoản, lịch sử giaoənd Dich, dữ liệu đầu tư.  
- **Confidential Business Information** – bí mật thương mại, kế hoạch kinh tranh, nghiên cứu thị trường.  
- **Intellectual Property** – bản quyền, sáng chế, thương hiệu, secret thuật toán.  
- **Government/Regulated Data** – thông tin an toàn quốc gia, bản ghi các cơ quan thực thi pháp luật.  
- **Employee Data** – hồ sơ 업무, đánh giá hiệu suất, kỷ luật.  

### 3.5. Cách data classification nâng cao bảo mật dữ liệu  

| Khía cạnh bảo mật | Vai trò của data classification |
|-------------------|---------------------------------|
| **Risk Assessment** | Xác định哪些資產屬於高風險，幫助優先分配資源。 |
| **Access Control** | 依據分類結果定義誰可以訪問哪些數據（例如：僅限高級管理人員訪問機密財務數據）。 |
| **Data Encryption** | 決定哪些數據需要加密（靜態/傳輸）以及加密強度（例如：PII 必須同時加密靜態與傳輸）。 |
| **Backup & Recovery** | 根據分類制定備份頻率和存儲位置（例如：機密數據每日備份並存儲於異地加密存儲）。 |
| **Compliance** | 為符合 GDPR、HIPAA、PCI DSS 等法規提供證據：組織能展示其已知哪些數據受規範約束並已實施對應控制措施。 |

Các giải pháp **DSPM** thường tự動化上述步驟：掃描雲端資產、根據預先定義的規則或模型自動打標籤、持續監控變化並觸發告警當數據被錯誤分類或存放在不符合政策的位置。  

## 4. Ví dụ minh họa  

### Tình huống  

Một công ty công nghệ lưu trữ các loại dữ liệu sau trong môi trường AWS S3:  

| Loại dữ liệu | Mô tả | Nhạy cảm |
|--------------|-------|----------|
| Email khách hàng (name, email, phone) | Thông tin liên hệ để gửi newsletter | PII (nhạy cảm) |
| Báo cáo tài chính quý | Số liệu doanh lợi, chi phí | Confidential (nhạy cảm cao) |
| Tài liệu marketing công khai | Banner, video quảng bá sản phẩm | Public (không nhạy cảm) |
| Bản ghi nội bộ về roadmap sản phẩm | Kế hoạch tính năng 6‑12 tháng tới | Internal Use Only (trung bình) |
| Hồ sơ nhân viên (lương, ID, 성과 đánh giá) | Thông tin lương và đánh giá | Confidential (PII + lương) |
| Bản sao lưu cũ của hệ thống CRM (6 tháng trước) | Dữ liệu lịch sử không còn dùng ngày hôm nay | Archived (cần giữ vì luật lưu trữ) |

### Quy trình phân loại & ứng dụng biện pháp bảo mật  

1. **Xây dựng schema** – public, internal use, restricted, confidential, archived.  
2. **Quét & gán nhãn** (có thể dùng DSPM):  
   - Email khách hàng → **confidential** (PII)  
   - Báo cáo tài chính → **confidential**  
   - Tài liệu marketing → **public**  
   - Roadmap nội bộ → **internal use**  
   - Hồ sơ nhân viên → **confidential** (PII+lương)  
   - Bản sao lưu CRM → **archived**  
3. **Áp dụng biện pháp**:  

| Mức độ phân loại | Biên pháp bảo mật được áp dụng |
|------------------|--------------------------------|
| **Public** | Không cần mã hoá; cho phép truy cập công khai; lưu trữ ở S3 bucket có quyền `public-read`. |
| **Internal Use Only** | Mã hoá ở resting (S3 SSE‑S3); kiểm soát truy cập qua IAM roles chỉ cho nội bộ; sao lưu tuần 1 lần. |
| **Confidential** | Mã hoá cả ở resting và trong truyền输 (S3 SSE‑KMS + TLS); IAM policy chỉ cho nhóm cụ thể (예: tài chính, HR); sao lưu ngày 1 lần và sao lưu ở vùng địa lý khác, lưu trữ lâu dài với lock (Object Lock). |
| **Archived** | Mã hoá resting; giữ trong bucket có chế độ retense compliance; truy cập chỉ qua yêu cầu đặc biệt; sao lưu không cần thường xuyên. |

### Kết quả  

- Dữ liệu PII được bảo vệ bởi mã hoá KMS và kiểm soát truy cập chặt chẽ → giảm rủi ro theft hoặc niew意暴露.  
- Báo cáo tài chính chỉ cho bộ tài chính truy cập → ngăn ngừa rò rỉ thông tin chiến lược.  
- Dữ liệu công khai vẫn có thể truy cập dễ dàng cho khách hàng và đối tác.  
- Dữ liệu lưu trữ đáp ứng yêu cầu pháp lý về thời gian lưu giữ mà không gây tốn tài nguyên lưu trữ unnecessarily.  

> Ví dụ trên minh họa cách **data classification** trực tiếp dẫn đến việc chọn đúng công cụ bảo mật (mã hoá, IAM, sao lưu) và đáp ứng các yêu cầu tuân thủ (GDPR cho PII, HIPAA nếu có dữ liệu y tế, PCI DSS cho thẻ thanh toán).  

## 5. Tổng kết  

- **Data classification** là quá trình gán nhãn dữ liệu dựa trên mức độ nhạy cảm và các tiêu chuẩn xác định trước; đây là nền tảng cho mọi chính sách bảo mật dữ liệu.  
- Quy trình bao gồm: định nghĩa schema, khám phá dữ liệu, tự động/hand‑on gán nhãn, sau đó áp dụng biện pháp bảo mật phù hợp.  
- Các cấp độ phổ biến (public, internal use, restricted, confidential, archived) giúp tổ chức sắp xếp và ưulice bảo mật.  
- Dzięki data classification, các活动 như **risk assessment**, **access control**, **encryption**, **backup/recovery** và **compliance** trở nên có mục tiêu và hiệu quả hơn.  
- Trong môi trường đám mây hiện đại, các giải pháp **DSPM** thường được dùng để tự動化 và liên tục giám sát quá trình phân loại, giúp組織 szybko reagować na zmiany i zapewniać ciągłość ochrony.  
- Áp dụng đúng cách data classification không chỉ giảm nguy cơ rò rỉ dữ liệu mà còn giúp tổ chức đáp ứng các quy định pháp lý (GDPR, HIPAA, PCI DSS) và tối ưu hoá chi phí bảo mật.  

---  

*Lưu ý: Các thuật ngữ tiếng Anh như **PII**, **PHI**, **PCI DSS**, **GDPR**, **HIPAA**, **DSPM** đã được giữ nguyên vì chúng là tên chuẩn trong lĩnh vực bảo mật và quyền riêng tư.*