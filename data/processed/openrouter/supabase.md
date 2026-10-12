# Bài học: Khái niệm cơ bản về Machine Learning trong AI Engineering  

## 1. Mục tiêu học tập  
- Hiểu rõ khái niệm **Artificial Intelligence (AI)**, **Machine Learning (ML)** và **Deep Learning (DL)**.  
- Nắm bắt quy trình **training** và **evaluation** của một model ML.  
- Khả năng thực hiện **pre‑processing** dữ liệu và **evaluate** kết quả sử dụng các công cụ phổ biến (Python + scikit‑learn).  

## 2. Tổng quan  
AI Engineering là lĩnh vực thiết kế, triển khai và duy trì các hệ thống trí tuệ nhân tạo. Trong đó Machine Learning là nền tảng quan trọng để cho máy tính “học” từ dữ liệu而不需要 được lập trình thủ công. Bài học này sẽ cung cấp cái nhìn tổng quan về các khái niệm cơ bản, giúp người học nắm bắt được cách xây dựng và đánh giá một model ML thực tế.  

## 3. Kiến thức cốt lõi  

| Thuật ngữ | Ý nghĩa (tiếng Việt) | Ghi chú |
|-----------|----------------------|----------|
| **Artificial Intelligence (AI)** | trí tuệ nhân tạo, khả năng mô phỏng hành vi thông minh của con người. | bao gồm ML, DL, rule‑based systems, v.v. |
| **Machine Learning (ML)** | học máy, một nhánh của AI cho phép hệ thống tự học từ dữ liệu. |chia thành supervised, unsupervised, reinforcement learning. |
| **Deep Learning (DL)** | học sâu, sử dụng neural network много层 để học đặc trưng phức tạp. | áp dụng rộng rãi trong picture, speech, language. |
| **Model** | mô hình học, là hàm số (function) được huấn luyện để dự đoán. | ví dụ: Linear Regression, Decision Tree, Neural Network. |
| **Training** | giai đoạn huấn luyện, dùng dữ liệu có nhãn (label) để điều chỉnh trọng số. | split dữ liệu thành train / validation / test. |
| **Feature** | đặc trưng, biến đầu vào được dùng để mô tả dữ liệu. | có thể là số, categorical, image pixel, v.v. |
| **Label** | nhãn, kết quả cần dự đoán (classification) hoặc giá trị tiếp tục (regression). | |
| **Evaluation metric** | chỉ số đánh giá, ví dụ: Accuracy, Precision, Recall, F1, MSE, RMSE. | lựa chọn tùy thuộc vào bài toán. |
| **Overfitting** | quá tinh xảo, model nhớ dữ liệu training而 không generalise. | kiểm soát bằng regularization, early stopping, dữ liệu augmentation. |

### Quy trình cơ bản của một dự án ML  
1. **Thu thập & làm sạch dữ liệu** – xử lý missing value, outlier, chuẩn hoá.  
2. **Phân chia dữ liệu** – train / validation / test (thường 70/15/15%).  
3. **Chọn mô hình** – dựa vào bài toán (classification, regression, clustering…).  
4. **Huấn luyện (training)** – tối ưu các trọng số để giảm lỗi.  
5. **Đánh giá (evaluation)** – dùng các metric trên tập validation/test.  
6. **Tối ưu** – thay đổi hyperparameter, thử model khác, hoặc cải thiện dữ liệu.  
7. **Triển khai** – lưu model (pickle, joblib), tích hợp vào ứng dụng.  

## 4. Ví dụ minh họa  

### Ví dụ 1: Linear Regression đơn giản  

```python
# Import thư viện
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Tạo dữ liệu giả lập (1000 mẫu, 1 feature)
X, y = make_regression(n_samples=1000, n_features=1, noise=10, random_state=42)

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Khởi tạo và huấn luyện model
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán và đánh giá
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
```

**Giải thích**  
- `make_regression` tạo bộ dữ liệu có mối quan hệ tuyến tính, noise là sai số.  
- `train_test_split` chia dữ liệu để có tập validation (test).  
- `LinearRegression` là một model **supervised** cho bài toán regression.  
- `mean_squared_error` là **evaluation metric** thường dùng cho regression.  

### Ví dụ 2: Classification với Decision Tree  

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Tải dữ liệu Iris (3 lớp, 4 feature)
iris = load_iris()
X, y = iris.data, iris.target

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y)

# Model
clf = DecisionTreeClassifier(max_depth=3, random_state=0)
clf.fit(X_train, y_train)

# Dự đoán
y_pred = clf.predict(X_test)

# Đánh giá
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
```

**Giải thích**  
- `DecisionTreeClassifier` là một model **supervised** cho **classification**.  
- `max_depth` giới hạn độ sâu cây để tránh **overfitting**.  
- `classification_report` cung cấp chi tiết về **Precision, Recall, F1** cho từng lớp.  

## 5. Tổng kết  

- **AI Engineering** xây dựng hệ thống thông minh; **Machine Learning** là công cụ chính để “học” từ dữ liệu.  
- Quy trình **training** – **evaluation** – **optimization** là trọng tâm; hiểu rõ các **metric** và cách phòng ngừa **overfitting** là yếu tố thành công.  
- Ví dụ Python với **scikit‑learn** cho thấy cách nhanh chóng triển khai một model **Linear Regression** và **Decision Tree** để giải quyết bài toán **regression** và **classification**.  

> **Lưu ý quan trọng:** Khi triển khai thực tế, luôn xác thực lại mô hình trên dữ liệu **test** độc lập và cân nhắc các yếu tố như cân bằng lớp (class imbalance), scaling dữ liệu, và lựa chọn hyperparameter hợp lý.  

---  

*Bài học này cung cấp nền tảng vững chắc để người học tiếp tục khám phá các kỹ thuật nâng cao trong AI Engineering.*