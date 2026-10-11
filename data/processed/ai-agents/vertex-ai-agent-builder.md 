# Giới thiệu Vertex AI – Nền tảng Machine Learning của Google Cloud  

## 1. Mục tiêu học tập  

Sau bài học bạn sẽ:  

- Nắm được khái niệm tổng quát về Vertex AI và vai trò của nó trong chu trình vidạt học máy (ML life‑cycle).  
- Hiểu cách cấu hình một dự án Google Cloud, tạo tài khoản thanh toán và bucket Cloud Storage để lưu trữ dữ liệu.  
- Tạo một Vertex AI Workbench (JupyterLab) và khởi tạo SDK `google-cloud‑aiplatform`.  
- Tải một tập dữ liệu từ local lên Cloud Storage, sau đó đọc trực tiếp từ bucket trong Workbench.  
- Huấn luyện một mô hình AutoML cho bài toán phân lớp, xem chỉ số hiệu quả và triển khai mô hình thành endpoint để thực hiện dự đoán.  
- Nắm được quy trình tổng quát để huấn luyện và triển khai mô hình tùy chỉnh (custom training) bằng Docker và XGBoost.  

## 2. Tổng quan  

Vertex AI là sản phẩm của Google Cloud (ra mắt 2021) mà thống nhất toàn bộ quy trình ML – từ chuẩn bị dữ liệu, huấn luyện, tối ưu siêu tham số, triển khai đến giám sát mô hình – vào một nền tảng duy nhất. Nó hỗ trợ hai cách tiếp cận chính:  

- **AutoML** – phù hợp với người mới hoặc những ai muốn giảm thiểu công việc viết code; nền tảng tự động thực hiện tiền xử lý, chọn thuật toán và tuning siêu tham số.  
- **Huấn luyện mô hình tùy chỉnh** – cho phép các nhà khoa học dữ liệu và engineer sử dụng framework họ喜欢 (TensorFlow, PyTorch, XGBoost…) và đóng gói thành Docker container để chạy trên Vertex AI.  

Trong bài học này chúng ta sẽ thực hành toàn bộ quy trình trên một tập dữ liệu thực (UCI Dry Bean) để thấy rõ từng bước: tạo project → billing → bucket → upload dữ liệu → Workbench → AutoML → triển khai → (tùy chọn) custom training.  

## 3. Kiến thức cốt lõi  

### 3.1. Cấu trúc dự án Google Cloud  

| Thành phần | Mô tả |  
|------------|-------|  
| **Project** | Đơn vị quản lý cấp cao nhất cho mọi tài nguyên (bucket, workbench, model…). |  
| **Billing account** | Cung cấp thông tin thanh toán; Vertex AI chỉ bắt đầu tính phí khi bạn sử dụng tài nguyên trả phí (ví dụ: máy ảo, giờ huấn luyện). |  
| **Cloud Storage bucket** | Kho chứa đối tượng (objects) dùng để lưu trữ dữ liệu thô (CSV, Parquet…) và artefacts mô hình. Mỗi bucket cần tên toàn cục duy nhất. |  
| **Vertex AI Workbench** | Môi trường phát triển dựa trên JupyterLab 3, đã được cài đặt sẵn SDK `google-cloud‑aiplatform` và các công cụ `gcloud`, `gsutil`. Bạn chọn cấu hình máy (CPU, RAM) tùy theo ngân sách và nhu cầu. |  

### 3.2. Luồng làm việc típico trong Vertex AI  

1. **Chuẩn bị dữ liệu** – tải tập dữ liệu lên bucket (hoặc sử dụng BigQuery).  
2. **Khởi tạo Workbench** – mở notebook, cài đặt/upgrade SDK, khai báo `PROJECT_ID`, `BUCKET_URI`, `REGION`.  
3. **Huấn luyện mô hình** –  
   - *AutoML*: tạo `TabularDataset` từ đường dẫn GCS, sau đó gọi `ai.AutoMLTabularTrainingJob.run(...)`.  
   - *Custom training*: viết script huấn luyện, đóng gói vào Dockerfile, xây dựng image, push lên Container Registry, sau đó tạo job training qua console hoặc SDK.  
4. **Đánh giá** – sau khi training xong, console hiển thị metrics (accuracy, precision, f1 …).  
5. **Triển khai** – gọi `model.deploy(machine_type="…")` để nhận được đối tượng `Endpoint`. Gửi dữ liệu JSON tới `endpoint.predict([...])` để nhận dự đoán.  
6. **Giám sát & dừng** – sau khi kiểm tra xong, nhớ dừng Workbench để tránh phí không cần thiết.  

### 3.3. Điểm khác biệt giữa AutoML và Custom training  

| Tiêu chí | AutoML | Custom training |  
|----------|--------|----------------|  
| **Yêu cầu code** | Rất ít (chỉ cần chỉ định target và phần split). | Cần viết script huấn luyện và Dockerfile. |  
| **Linh hoạt framework** | Giới hạn ở các thuật toán được nền tảng hỗ trợ nội bộ. | Bất kỳ framework nào có thể chạy trong container (TF, PyTorch, XGBoost, Scikit‑learn…). |  
| **Chi phí** | Thường thấp hơn vì chỉ dùng tài nguyên cần thiết cho quá trình AutoML. | Có thể cao hơn do cần chạy container và có thể lưu trữ image. |  
| **Thời gian thiết lập** | Nhanh (nhiều bước được tự động hoá). | Longe hơn (xây dựng image, push, cấu hình job). |  

## 4. Ví dụ minh họa  

Dưới đây là các đoạn code quan trọng được trích từ tutorial, cùng với giải thích ngắn gọn để bạn có thể thực hành ngay trong Vertex AI Workbench.  

### 4.1. Thiết lập project và SDK  

```python
from google.cloud import aiplatform as ai

PROJECT_ID = 'vertexai-tutorial-423010'          # <-- thay bằng ID dự án của bạn
BUCKET_URI = 'gs://vetex-tutorial-bucket-bex'   # <-- thay bằng tên bucket của bạn
REGION = 'us-central1'

ai.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)
```

*Giải thích*: `ai.init` kết nối SDK với dự án, khu vực và bucket lưu trữ tạm (staging bucket) mà Vertex AI sẽ dùng để lưu artefacts trong quá trình training.  

### 4.2. Tải dataset từ local lên Cloud Storage (thực hiện ngoài Workbench)  

1. Tải file **Dry Bean Dataset** từ UCI, lưu dưới dạng Excel.  
2. Chuyển sang CSV và lưu vào thư mục `data/` của bạn:  

```python
from pathlib import Path
import pandas as pd

cwd = Path.cwd()
data_path = cwd / "data" / "Dry_Bean_Dataset.xlsx"
beans = pd.read_excel(data_path)                 # yêu cầu cài openpyxl
beans.to_csv(cwd / "data" / "dry_bean.csv", index=False)
```

3. Tạo bucket trong Cloud Storage (qua console hoặc `gsutil mb gs://<tên-bucket>`) và upload file CSV:  

```bash
gsutil cp ./data/dry_bean.csv gs://vetex-tutorial-bucket-bex/
```

### 4.3. Đọc dữ liệu trực tiếp từ GCS trong Workbench  

```python
import pandas as pd

gcs_path = "gs://vetex-tutorial-bucket-bex/dry_bean.csv"
beans = pd.read_csv(gcs_path)        # hoạt động vì Workbench đã được xác thực
beans.head()
```

### 4.4. Khám phá nhanh dữ liệu (tùy chọn)  

```python
beans.info()
# вывод: 17 cột (15 numeric + 1 object target 'Class'), 13 611 bản ghi, không missing.

feature_names = beans.columns.tolist()
```

### 4.5. Huấn luyện mô hình AutoML  

```python
# 1. Tạo đối tượng TabularDataset từ CSV trên GCS
ds = ai.TabularDataset.create(
    display_name="dry_bean_dataset",
    gcs_source=gcs_path
)

# 2. Định nghĩa job huấn luyện AutoML (phân lớp)
job = ai.AutoMLTabularTrainingJob(
    display_name="dry-bean-classification",
    optimization_prediction_type="classification",
)

# 3. Chạy job – chia train/validation/test 80/10/10
model = job.run(
    dataset=ds,
    target_column="Class",
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
    model_display_name="baseline-classification-model",
    disable_early_stopping=False,
)
```

Sau khi job hoàn thành, bạn có thể xem metrics trên tab **MODEL DEVELOPMENT > TRAINING** của console – trong ví dụ này mọi chỉ số đều > 0.90.  

### 4.6. Triển khai mô hình và thực hiện dự đoán  

```python
# Triển khai (comment out nếu không muốn tốn phí)
# endpoint = model.deploy(machine_type="n1-standard-4")

# Nếu đã có endpoint, ví dụ thực hiện dự đoán cho một mẫu:
prediction = endpoint.predict(
    [{
        "Area": "30099",
        "Perimeter": "638.8209999999999",
        "MajorAxisLength": "237.14191130827916",
        "MinorAxisLength": "162.3034300714102",
        "AspectRation": "1.4611022774068396",
        "Eccentricity": "0.7290928631259719",
        "ConvexArea": "30477",
        "EquivDiameter": "195.76321681302556",
        "Extent": "0.8036043251902283",
        "Solidity": "0.9875972044492568",
        "roundness": "0.9268374259664279",
        "Compactness": "0.8255108332939839",
        "ShapeFactor1": "0.007878730566074592",
        "ShapeFactor2": "0.002256976927384019",
        "ShapeFactor3": "0.6814681358857279",
        "ShapeFactor4": "0.9956946453228307",
    }]
)

print(prediction)
```

*Giải thích*: Mỗi mẫu phải được biểu diễn dưới dạng dict (JSON) với các trường trùng tên cột. `endpoint.predict` trả về danh sách các dự đoán (nhãn lớp và xác suất).  

### 4.7. Huấn luyện mô hình tùy chỉnh (XGBoost) – tổng quan các bước  

1. **Cấu trúc thư mục**  

```
dry-beans/
 └─ trainer/
      └─ train.py
 └─ Dockerfile
```

2. **Nội dung Dockerfile** (được lưu trong `dry-beans/Dockerfile`)  

```dockerfile
FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-6
WORKDIR /

# Copy trainer code
COPY trainer /trainer

# Install XGBoost
RUN pip install xgboost==1.6.2

# Entry point
ENTRYPOINT ["python", "-m", "trainer.train"]
```

3. **Script huấn luyện (`trainer/train.py`) – chỉ mang tính chất minh hoá**  

```python
import pandas as pd
from google.cloud import storage
from xgboost import XGBClassifier
import joblib

# ---- cấu hình ----
BUCKET_NAME = "vetex-tutorial-bucket-bex"
CSV_BLOB = "dry_bean.csv"
MODEL_BLOB = "model/xgboost_dry_bean.joblib"

# ---- tải dữ liệu từ GCS ----
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)
blob = bucket.blob(CSV_BLOB)
blob.download_to_filename("/tmp/dry_bean.csv")
df = pd.read_csv("/tmp/dry_bean.csv")

X = df.drop(columns="Class")
y = df["Class"]

# ---- huấn luyện ----
clf = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    objective="multi:softprob",
    num_class=7,
    eval_metric="mlogloss",
    n_jobs=4,
)
clf.fit(X, y)

# ---- lưu model trở lại GCS ----
joblib.dump(clf, "/tmp/model.joblib")
blob_out = bucket.blob(MODEL_BLOB)
blob_out.upload_from_filename("/tmp/model.joblib")
print("Model trained and uploaded!")
```

4. **Xây dựng và push image**  

```bash
# Thay đổi các biến này cho phù hợp
PROJECT_ID=vertexai-tutorial-423010
IMAGE_URI=gcr.io/$PROJECT_ID/dry-beans:v1

docker build ./ -t $IMAGE_URI          # từ thư mục dry-beans/
docker run $IMAGE_URI                  # kiểm tra local
docker push $IMAGE_URI                 # gửi lên Container Registry
```

5. **Tạo Custom Training Job qua console**  

- Chọn **No managed dataset** → **Custom training**.  
- Đặt tên model (ví dụ: `dry-beans-classifier`).  
- Trong phần **Training container**, chọn hình ảnh vừa push (`IMAGE_URI`) và chỉ định bucket đầu ra cho artefact mô hình.  
- Chọn loại máy (ví dụ: n1-standard-4, 4 vCPU) → **START TRAINING**.  

Sau khi job hoàn thành (hoặc gặp lỗi quota CPU như trong bài gốc), bạn có thể triển khai model tương tự như phần AutoML bằng `model.deploy(...)`.  

## 5. Tổng kết  

- Vertex AI cung cấp một nền tảng thống nhất để thực hiện toàn bộ chu trình ML, từ lưu trữ dữ liệu, huấn luyện (AutoML hoặc custom) tới triển khai và giám sát.  
- Với AutoML, bạn chỉ cần cung cấp dữ liệu và chỉ định cột target; nền tảng lo phần còn lại (tiền xử lý, chọn mô hình, tuning).  
- Đối với những người có kinh nghiệm và cần kiểm soát chi tiết, custom training cho phép sử dụng bất kỳ framework nào, đóng gói vào Docker và chạy trên hạ tầng compute của Google Cloud.  
- Quy trình thực hành bao gồm: tạo project & billing → bucket → upload dữ liệu → Workbench → khởi tạo SDK → tải dữ liệu từ GCS → (AutoML) tạo `TabularDataset` và chạy `AutoMLTabularTrainingJob.run` → triển khai mô hình → thực hiện dự đoán → (tùy chọn) xây dựng Docker image, push và tạo custom training job.  
- Luôn nhớ dừng Workbench sau khi hoàn thành để tránh phát sinh chi phí không cần thiết.  

Bài học này đã cung cấp đủ cơ bản để bạn bắt đầu khám phá sâu hơn các tính năng nâng cao của Vertex AI như pipeline,Batch prediction, monitoring, hoặc tích hợp với các dịch vụ khác của Google Cloud (BigQuery, AI Platform Pipelines…). Hãy tiếp tục khám phá và áp dụng vào các bài toán thực tế của mình!