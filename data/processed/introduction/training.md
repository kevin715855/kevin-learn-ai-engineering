# Model Training trong Machine Learning

## 1. Mục tiêu học tập  
Sau bài học này, người học sẽ:  
- Nắm rõ khái niệm *model training* và vai trò của nó trong quy trình học máy.  
- Phân biệt giữa học có giám sát (supervised learning) và học không giám sát (unsupervised learning).  
- Hiểu được 7 bước chính để xây dựng một mô hình ML.  
- Đánh giá các yếu tố ảnh hưởng đến thời gian huấn luyện mô hình.  
- Áp dụng kiến thức vào bối cảnh sản xuất Industry 4.0 (ví dụ: bảo trì dự đoán, phát hiện bất thường).

## 2. Tổng quan  
Model training là quá trình đưa dữ liệu huấn luyện vào một thuật toán học máy để thuật toán học được mối quan hệ giữa biến đầu vào (features) và biến mục tiêu (target). Khi mô hình đã “hiểu” được quan hệ này, nó có thể đưa ra dự đoán hoặc xác định pattern trên dữ liệu mới. Trong sản xuất, việc huấn luyện mô hình cho phép nhà máy phát hiện sớm sự hỏng hóc, tối ưu hiệu suất thiết bị (OEE) và giảm downtime.

## 3. Kiến thức cốt lõi  

### 3.1 Định nghĩa cơ bản  
- **Training dataset**: Bộ dữ liệu gồm cặp (input, output) dùng để huấn luyện.  
- **Model fitting**: Vòng lặpiterate trong đó mô hình điều chỉnh các tham số (weights) để giảm sai số giữa output dự đoán và output thực tế.  

### 3.2 Hai loại học chính  

| Loại | Tính năng | Ví dụ ứng dụng |
|------|-----------|----------------|
| **Supervised learning** | Cần dữ liệu có nhãn (input + output mong muốn). Mô hình học từ sai số giữa dự đoán và nhãn thực tế. | Dự đoán số lượng sản phẩm lỗi dựa trên cảm biến nhiệt độ, áp lực. |
| **Unsupervised learning** | Chỉ có input, không có output. Mô hình tự tìm cấu trúc, cụm hoặc pattern trong dữ liệu. | Phân cụm các máy semelhante dựa trên đặc hiệu rung để lên lịch bảo trì. |

### 3.3 7 bước xây dựng mô hình ML  

1. **Định nghĩa vấn đề** – Xác định mục tiêu (dự đoán, phân loại, clustering…), đưa ra câu hỏi: input là gì, output mong đợi là gì.  
2. **Thu thập dữ liệu** – Lấy dữ liệu từ cơ sở dữ liệu existentes hoặc thu thập mới; chất lượng và khối lượng dữ liệu quyết định hiệu suất mô hình.  
3. **Chuẩn bị dữ liệu** – Làm sạch (loại bỏ trùng lặp, sửa lỗi), chuẩn hoá (normalization), chọn thuộc tính liên quan; chia dữ liệu thành tập huấn luyện và tập validation.  
4. **Chọn mô hình / protocol** – Áp dụng thuật toán phù hợp với loại dữ liệu và mục tiêu (ví dụ: linear regression cho regression, k‑means cho clustering, CNN cho ảnh).  
5. **Huấn luyện mô hình** – Đưa tập huấn luyện vào algorithm, khởi tạo weights ngẫu nhiên, lan truyền ngược để cập nhật weights.  
6. **Đánh giá và xác định tiêu chuẩn thành công** – Kiểm tra trên tập validation, tính các chỉ số (accuracy, precision, recall, F1, MSE…) để đo lường hiệu quả.  
7. **Điều chỉnh siêu‑tham số (parameter tuning)** – Tối ưu các siêu‑tham số (learning rate, số lớp, số cụm…) để mô hình đạt độ chính xác cao nhất trên validation trước khi達到 điểm sinh lợi giảm (diminishing return).  

### 3.4 Thời gian huấn luyện  
Không có thời gian cố định. Các yếu tố ảnh hưởng:  
- Chất lượng và lượng dữ liệu huấn luyện.  
- Độ phức tạp của mô hình (số tham số, kiến trúc).  
- Phương pháp huấn luyện (batch, mini‑batch, online).  
- Tài nguyên tính toán (CPU, GPU, RAM).  
- Kỹ năng của đội ngũ thực hiện.  
Việc tối ưu hoá bất kỳ yếu tố nào cũng có thể rút ngắn thời gian huấn luyện.

### 3.5 Ứng dụng trong sản xuất (Industry 4.0)  
- **Bảo trì dự đoán (Predictive Maintenance)**: Huấn luyện mô hình trên dữ liệu cảm biến (giật, nhiệt độ, dòng điện) để dự đoán thời điểm hỏng hóc, giảm downtime.  
- **Phát hiện bất thường (Anomaly Detection)**: Mô hình unsupervised học pattern bình thường; khi dữ liệu mới lệchpattern fortemente → cảnh báo.  
- **Optimization of OEE**: Dự đoán sản lượng, chất lượng, thời gian cycle dựa trên dữ liệu quy trình → đưa ra quyết định điều chỉnh thông số máy móc.  

## 4. Ví dụ minh họa  

**Bài toán**: Dự đoán taux lỗi sản phẩm dựa trên hai cảm biến: nhiệt độ (°C) và áp suất (bar).  

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Dữ liệu giả (n=100)
np.random.seed(42)
temp = np.random.normal(80, 5, 100)          # nhiệt độ
pressure = np.random.normal(2.0, 0.2, 100)   # áp suất
error_rate = 0.01*temp + 0.05*pressure + np.random.normal(0, 0.5, 100)  # công thức thực + noise

X = np.column_stack((temp, pressure))
y = error_rate

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1)

# Huấn luyện hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán và đánh giá
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error trên validation: {mse:.4f}")
```

**Giải thích**:  
1. Bước 1‑2: Định nghĩa vấn đề (dự đoán lỗi) và tạo dữ liệu.  
2. Bước 3: Chuẩn bị – tạo mảng features `X`, chia train/val.  
3. Bước 4: Chọn mô hình – `LinearRegression` phù hợp với bài toán regression.  
4. Bước 5: Huấn luyện – `model.fit`.  
5. Bước 6: Đánh giá – tính MSE trên tập validation.  
6. Bước 7 (tùy chọn): Có thể điều chỉnh siêu‑tham số (ví dụ: thêm regularization) để giảm MSE hơn.

## 5. Tổng kết  
- Model training là bước Core trong pipeline học máy, nơi thuật toán học từ dữ liệu để xây dựng khả năng dự đoán hoặc khám phá pattern.  
- Học có giám sát và học không giám sát là hai hướng chính, tùy thuộc vào sự có mặt của nhãn output.  
- Xây dựng mô hình thành công cần atravers 7 bước: định nghĩa問題 → thu thập → chuẩn bị → chọn mô hình → huấn luyện → đánh giá → tune siêu‑tham số.  
- Thời gian huấn luyện phụ thuộc vào nhiều yếu tố; việc tối ưu hoá dữ liệu, mô hình và tài nguyên tính toán giúp giảm thời gian.  
- Trong môi trường sản xuất Industry 4.0, mô hình đã được huấn luyện có thể mang lại lợi ích thực tế như bảo trì dự đoán, phát hiện bất thường và nâng cao OEE.  

Những điểm trên cung cấp nền tảng lý tưởng để bạn bắt đầu áp dụng machine learning vào các bài toán thực tế trong ngành công nghiệp.