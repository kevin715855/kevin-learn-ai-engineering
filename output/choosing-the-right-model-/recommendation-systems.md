# Recommendation Engine – Hệ thống đề xuất

## 1. Mục tiêu học tập

Sau khi học bài này, người học sẽ:
- Nắm được khái niệm và vai trò của recommendation engine trong các ứng dụng thương mại điện tử, phương tiện truyền thông, du lịch…  
- Hiểu quy trình hoạt động của hệ thống đề xuất từ thu thập dữ liệu đến tối ưu hóa mô hình.  
- Phân biệt ba loại chính của recommendation engine: collaborative filtering (memory‑based, model‑based), content‑based filtering và hybrid system.  
- Đánh giá lợi ích và thách thức khi triển khai hệ thống đề xuất trong doanh nghiệp.  
- Áp dụng kiến thức để đề xuất giải pháp phù hợp với một số use case thực tế.

## 2. Tổng quan

Recommendation engine (hay recommender) là một hệ thống AI sử dụng big data analytics và machine learning để đề xuất các mục nội dung, sản phẩm hoặc dịch vụ phù hợp với sở thích và hành vi của người dùng. Hệ thống này giúp người dùng khám phá nội dung mà họ có thể không tự tìm thấy, đồng thời nâng trải nghiệm cá nhân hóa, tăng tỷ lệ chuyển đổi và doanh thu cho các nền tảng thương mại, truyền thông, du lịch vàmarketing.

Theo số liệu từ IBM Think (2024), thị trường recommendation engine ước tính khoảng **6,88 tỷ USD** và dự kiến tăng gấp ba trong vòng 5 năm tới. Các nghiên cứu của McKinsey cho thấy việc cá nhân hóa có thể tăng doanh thu **5%–15%**, trong khi **76%** khách hàng cảm thấy bực bội khi không nhận được trải nghiệm cá nhân hóa.

## 3. Kiến thức cốt lõi

### 3.1 Quy trình hoạt động (5 giai đoạn)

| Giai đoạn | Mô tả chi tiết |
|-----------|----------------|
| **1. Thu thập dữ liệu** | Thu thập **d dữ liệu rõ ràng** (explicit) như đánh giá, bình luận, like, review và **dữ liệu ngầm** (implicit) bao gồm lịch sử duyệt, click, giỏ hàng, lịch sử mua sọ, tìm kiếm. Ngoài ra còn thu thập thông tin khách hàng (tuổi, giới tính, sở thích, lối sống) và đặc điểm mục (giá, loại, thẻTag). |
| **2. Lưu trữ** | Dữ liệu được đưa vào kho chứa phù hợp: <br>• **Data warehouse** – tổng hợp dữ liệu có cấu trúc từ nhiều nguồn.<br>• **Data lake** – lưu trữ cả dữ liệu có cấu trúc và phi cấu trúc.<br>• **Data lakehouse** – kết hợp lợi thế của cả hai. |
| **3. Phân tích** | Áp dụng các thuật toán machine learning để tìm mẫu, mối quan hệ và đo lường sức mạnh của chúng. Mô hình được huấn luyện trên tập dữ liệu lớn để đưa ra đề xuất phù hợp. |
| **4. Lọc (Filtering)** | Áp dụng quy tắc/toán học cụ thể tùy thuộc vào loại recommendation engine để đưa ra danh sách mục наиболее liên quan từ kết quả phân tích. |
| **5. Tinh chỉnh (tùy chọn)** | Đánh giá định kỳ đầu ra của hệ thống, điều chỉnh siêu tham số hoặc thêm dữ liệu mới để nâng cao độ chính xác và chất lượng đề xuất qua thời gian. |

### 3.2 Các loại recommendation engine

#### 3.2.1 Collaborative Filtering (Lọc cộng tác)

- **Nguyên lý**: Đề xuất dựa trên sự tương đồng giữa người dùng hoặc giữa các mục. Giả sử: người dùng có sở thích gần giống sẽ thích những mục tương tự.
- **Hai phân支 chính**:
  1. **Memory‑based**  
     - *User‑based*: tính độ similarity giữa người dùng hiện tại và tất cả người dùng khác (theo hàng trong ma trận user‑item).  
     - *Item‑based*: tính similarity giữa mục qua cách người dùng tương tác với chúng (theo cột trong ma trận).  
     - Cách triển khai thường dựa trên **k‑nearest neighbors (KNN)**.  
  2. **Model‑based**  
     - Xây dựng mô hình dự đoán (ví dụ: ma trận phân giải **matrix factorization**) từ ma trận user‑item làm dữ liệu huấn luyện.  
     - Ma trận lớn được phân tách thành hai ma trận nhỏ (user‑factor, item‑factor) rồi nhân lại để dự đoán giá trị thiếu (đề xuất).  
     - Các cải tiến: kết hợp **deep learning** (neural network), **Naive Bayes**, clustering, decision trees.  
- **Ư điểm**: Không cần mô tả chi tiết của mục; hiệu quả khi có đủ dữ liệu lịch sử.  
- **Nhược điểm**: **Cold start** – khó xử lý người dùng mới hoặc mục mới do thiếu dữ liệu lịch sử.

#### 3.2.2 Content‑Based Filtering (Lọc dựa trên nội dung)

- **Nguyên lý**: Đề xuất mục có đặc điểm tương tự với những mục mà người dùng đã thích.  
- **Quá trình**:  
  - Mỗi mục và người dùng được biểu diễn dưới dạng **vector** trong không gian đặc trưng (vector space).  
  - Độ similarity đo bằng khoảng cách (ví dụ: cosine similarity) giữa vector người dùng và vector mục.  
  - Mô hình thường là **classifier hoặc hồi quy** dựa trên các đặc trưng của mục (màu sắc, danh mục, giá, thẻTag) và dữ liệu hành vi của người dùng.  
- **Ư điểm**: Giảm thiểu vấn đề cold start vì dựa trên metadata thay vì lịch sử tương tác.  
- **Nhược điểm**: Thérèse khám phá mới (exploration) – xu hướng đề xuất những mục tương tự với những gì đã được thích, gây hạn chế trong việc tìm ra xu hướng mới.

#### 3.2.3 Hybrid Recommendation System

- **Nguyên lý**: Kết hợp cả collaborative filtering và content‑based filtering để استغلال lợi điểm của mỗi phương pháp và giảm nhược điểm của từng phương pháp.  
- **Triển khai thường见**:  
  - Trọng số kết hợp hai điểm số từ hai mô hình.  
  - Sử dụng collaborative filtering để tạo lô kandidat, sau đó lọc lại bằng content‑based filtering.  
  - Hoặc xây dựng mô hình chung (ví dụ: Factorization Machine) nhận cả đặc trưng người dùng và đặc trưng mục.  
- **Ví dụ thực tế**: Netflix sử dụng hệ thống hybrid để đề xuất phim vàรายการ TV, đạt hiệu suất cao hơn so với mỗi phương pháp riêng lẻ.

### 3.3 Lợi ích của recommendation engine

| Lợi ích | Mô tả / Số liệu hỗ trợ |
|--------|------------------------|
| **Cải thiện trải nghiệm người dùng** | Người dùng tiết kiệm thời gian tìm kiếm; 80% nội dung mà người xem trên Netflix đến từ đề xuất. |
| **Tăng độ giữ chân khách hàng** | Theo McKinsey, trải nghiệm tốt hơn → hài lòng khách hàng tăng 20% → khách hàng trung thành hơn. |
| **Nâng tỷ lệ chuyển đổi** | Khuyến mãi cá nhân hóa làm tăng taux chuyển đổi 10%–15%. |
| **Tăng doanh thu** | 35% của doanh số mua sắm trên Amazon đến từ đề xuất; Netflix ước lượng tiết kiệm > 1 triệu USD nhờ hệ thống đề xuất. |
| **Cá nhân hóa sâu** | Đề xuất phù hợp với sở thích cá nhân tạo cảm giác được “hiểu”. |

### 3.4 Thách thức và hạn chế

| Thách thức | Mô tả |
|------------|-------|
| **Chi phí và độ phức tạp** | Cần kiến trúc quy mô lớn để xử lý và lọc khối lượng dữ liệu khổng lồ; đầu tư phần cứng, GPU, hệ thống phân tán. |
| **Tốc độ và mở rộng** | Yêu cầu phản hồi thời gian thực cho hàng nghìn,甚至 triệu người dùng đồng thời. |
| **Đề xuất không liên quan** | Nếu hàmloss tập trung vào chỉ số sai (ví dụ: maximizing clicks mà không quan tâm tới satisfaction) có thể lặp đi lặp lại những mục phổ biến, bỏ qua mục mới hoặc ít người biết. |
| **Bias (side effect)** | Mô hình có thể học các bias xã hội từ dữ liệu (giới tính, chủng tộc…) hoặc từ con người gán nhãn, dẫn tới đề xuất sai lệch. |
| **Bảo mật và tuân thủ** | Một số người dùng không muốn chia sẻ dữ liệu cá nhân; doanh nghiệp phải tuân thủ GDPR, CCPA và các quy định về bảo mật dữ liệu khi thu thập và lưu trữ. |

### 3.5 Use case thực tế

| Ngành | Ứng dụng recommendation engine |
|------|------------------------------|
| **E‑commerce & Retail** | Đề xuất sản phẩm “khách hàng cũng mua”, sản phẩm phụ hợp, combo đề especiais, khuyến mãi theo mùa. *Ví dụ*: Amazon. |
| **Media & Entertainment** | Đề xuất phim, bài hát, ebook, trò chơi dựa trên lịch sử xem/nghe. *Ví dụ*: Netflix, Spotify, YouTube. |
| **Travel & Hospitality** | Đề xuất khách sạn, nhà hàng, hoạt động du lịch dựa trên ngân sách và lịch sử 여행. |
| **Marketing** | Đề xuất nội dung (blog, case study, webinar) để nuôi dưỡng leads và đưa vào chiến dịch email/targeted ads. |
| **AIOps** | Đề xuất các biện pháp khắc phục sự cố IT dựa trên dữ liệu log, metrics và historiques sự cố, giúp 팀 vận hành реагировать nhanh hơn. |

## 4. Ví dụ minh họa

### 4.1 Minh họa quá trình collaborative filtering (user‑based)

Giả sử chúng ta có ma trận rating (người dùng × phim) như sau (0 = chưa đánh giá):

| Người dùng \ Phim | Phim A | Phim B | Phim C | Phim D |
|-------------------|--------|--------|--------|--------|
| Alice             | 5      | 0      | 3      | 4      |
| Bob               | 4      | 0      | 0      | 5      |
| Carol             | 0      | 5      | 4      | 0      |
| Dave              | 3      | 4      | 0      | 0      |

**Bước 1 – Tính similarity** (ví dụ: cosine similarity) giữa Alice và các user khác.  
- Similarity(Alice, Bob) ≈ 0.86  
- Similarity(Alice, Carol) ≈ 0.30  
- Similarity(Alice, Dave) ≈ 0.71  

**Bước 2 – Dự đoán rating của Alice cho Phim B** (mà Alice chưarating)  

\[
\hat{r}_{Alice, B} = \frac{\sum_{u \neq Alice} sim(Alice,u) \cdot r_{u,B}}{\sum_{u \neq Alice} |sim(Alice,u)|}
= \frac{0.86 \cdot 0 + 0.30 \cdot 5 + 0.71 \cdot 4}{0.86 + 0.30 + 0.71}
\approx \frac{0 + 1.5 + 2.84}{1.87}
\approx 2.32
\]

Vì dự đoán không cao, hệ thống có thể không đề xuất Phim B cho Alice, mà thay vào đó sẽ xem các phim có dự đoán rating cao hơn (ví dụ: Phim C, D).

### 4.2 Minh họa content‑based filtering

Giả sử mỗi phim được mô tả bằng vector đặc trưng: **[action, comedy, rating]**.  

- Phim X = [1, 0, 4.5] (action cao, không comédie, rating 4.5)  
- Phim Y = [0, 1, 4.0] (comedy, không action)  

Người dùng đã thích Phim X → vector người dùng ≈ [1, 0, 4.5] (trung bình các phim đã thích).  

Tính cosine similarity:  

- sim(user, X) ≈ 1 (trùng khớp)  
- sim(user, Y) ≈ 0 (không có chung thành phần)  

→ Hệ thống sẽ đề xuất các phim có thành phần action cao, tương tự Phim X.

### 4.3 Minh họa hybrid (giả lập đơn giản)

1. **Bước collaborative** – Tìm top‑5 phim dựa trên similarity người dùng.  
2. **Bước content‑based** – Trong 5 phim đó, lọc ra những phim có đặc trưng giống với sở thích đã biết (thể loại, đạo diễn).  
3. **Kết quả** – Danh sách cuối cùng là intersection của 2 bộ lọc, thường mang lại độ chính xác cao hơn khi dữ liệu lịch sử sparse.

## 5. Tổng kết

- Recommendation engine là hệ thống AI dựa trên **big data analytics** và **machine learning**, đóng vai trò then chốt trong việc cá nhân hoá trải nghiệm người dùng và tăng doanh thu cho doanh nghiệp.  
- Quy trình hoạt động bao gồm **5 giai đoạn**: thu thập dữ liệu → lưu trữ → phân tích → lọc → (tùy chọn) tinh chỉnh.  
- Ba phương pháp chính:  
  - **Collaborative filtering** (memory‑based & model‑based) – dựa trên sự tương đồng giữa người dùng/mục.  
  - **Content‑based filtering** – dựa trên đặc trưng mục và vector hóa.  
  - **Hybrid** – kết hợp cả hai để vượt qua hạn chế của mỗi phương pháp.  
- Lợi ích rõ ràng: cải thiện UX, tăng retention, nâng chuyển đổi và doanh thu; thách thức bao gồm chi phí infrastrukture, độ trễ thực‑time, bias, và vấn đề bảo mật.  
- Các ngành kinh doanh như thương mại điện tử, truyền médias, du lịch, marketing và AIOps đều có ứng dụng thực tiễn của recommendation engine, với ví dụ điển hình như Amazon, Netflix, Spotify.

Với những kiến thức trên, người học có thể phân tích nhu cầu đề xuất của một dự án cụ thể, chọn loại recommendation engine phù hợp và thiết kế hệ thống cân bằng giữa độ chính xác, tốc độ và chi phí triển khai.