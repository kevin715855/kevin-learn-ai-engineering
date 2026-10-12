# Phát hiện bất thường (Anomaly Detection) bằng Embeddings từ Gemini API  

## 1. Mục tiêu học tập  

Sau bài học này, bạn sẽ能够:  

- Tạo embeddings cho văn bản bằng mô hình **embedding-001** của Gemini API.  
- Áp dụng giảm chiều (t‑SNE) để trực quan hóa embedding trong không gian 2D.  
- Tính centroid của mỗi nhóm và xác định điểm ngoại lai dựa trên khoảng cách Euclidean.  
- Vẽ biểu đồ.scatter để quan sát nhóm và điểm ngoại lai.  
- Đánh giá nhạy感 của bộ phát hiện qua việc thay đổi bán kính (radius).  

## 2. Tổng quan  

Bài hướng dẫn minh hoá cách sử dụng embeddings từ Gemini API để phát hiện các bản ghi “lạ” (outlier) trong bộ dữ liệu **20 Newsgroups**. Quy trình bao gồm:  

1. Chuẩn bị và làm sạch dữ liệu văn bản (loại bỏ email, tên, tiêu đề …).  
2. Lấy mẫu 150 bản ghi từ mỗi chủ đề thuộc nhóm **sci** (sci.crypt, sci.electronics, sci.med, sci.space).  
3. Sinh vector embedding độ dài 768 cho mỗi bản ghi với task type **CLUSTERING**.  
4. Giảm chiều bằng t‑SNE xuống 2 dimensiones để vẽ biểu đồ散布図.  
5. Tính centroid (trung bình vector) của mỗi lớp trong không gian embedding gốc.  
6. Xác định điểm nào có khoảng cách từ centroid lớn hơn một ngưỡng **radius** được coi là outlier.  
7. Trực quan hóa outlier trên biểu đồ t‑SNE và in một vài ví dụ văn bản ngoại lai.  

## 3. Kiến thức cốt lõi  

### 3.1 Embeddings và task type  

- Mô hình **embedding-001** trả về vector 768‑dimension.  
- Khi gọi `genai.embed_content`, tham số `task_type` chỉ định mục đích sử dụng.  
  - `CLUSTERING` (phụ hợp cho việc phát hiện outlier) cho vector embedding tối ưu để giữ các điểm cùng nhóm gần nhau.  

### 3.2 Chuẩn bị dữ liệu  

- Bộ dữ liệu **20 Newsgroups** chứa khoảng 18.000 bài viết trên 20 chủ đề.  
- Trong hướng dẫn chúng ta chỉ dùng tập **train** và lọc ra 4 chủ đề liên quan đến khoa học (`sci.*`).  
- Các bước tiền xử lý bao gồm:  
  - Loại bỏ địa chỉ email (`re.sub(r'[\\w\\.-]+@[\\w\\.-]+', '', text)`).  
  - Loại bỏ tên người gửi và các từ loại như `"From: "` , `"\\nSubject: "` .  
  - Cắt mỗi đoạn văn tối đa 5000 ký tự để tránh độ dài過大.  

### 3.3 Tạo embedding  

```python
def make_embed_text_fn(model):
    @retry.Retry(timeout=300.0)
    def embed_fn(text: str) -> list[float]:
        embedding = genai.embed_content(
            model=model,
            content=text,
            task_type="clustering"
        )["embedding"]
        return np.array(embedding)
    return embed_fn

def create_embeddings(df):
    model = 'models/embedding-001'
    df['Embeddings'] = df['Text'].progress_apply(make_embed_text_fn(model))
    return df
```

- Kết quả: cột **Embeddings** chứa list 768 số thực (`float32`).  

### 3.4 Giảm chiều với t‑SNE  

- Không thể trực quan hóa 768‑dimension trực tiếp → dùng **t‑Distributed Stochastic Neighbor Embedding (t‑SNE)**.  
- Tham số quan trọng: `random_state=0` (để kết quả tái tạo), `n_iter=1000`.  
- Sau giảm chiều ta得到 DataFrame `df_tsne` với các cột `TSNE1`, `TSNE2` và `Class Name`.  

### 3.5 Tính centroid và phát hiện outlier  

- **Centroid** của một lớp là trung bình các vector embedding thuộc lớp đó (trong không gian gốc 768‑d).  
- Khoảng cách Euclidean giữa một điểm và centroid của lớp tính bằng:  

```python
def calculate_euclidean_distance(p1, p2):
    return np.sqrt(np.sum(np.square(p1 - p2)))
```

- Một điểm được đánh dấu **outlier** nếu `distance > radius`.  
- Hàm `detect_outlier` lặp qua toàn bộ DataFrame, thêm cột boolean `Outlier` và trả về số lượng outlier cho mỗi giá trị `radius`.  

### 3.6 Trực quan hoá  

- Vẽ biểu đồ scatter của t‑SNE, tô màu theo `Class Name`.  
- Đánh dấu centroid bằng dấu `X` đen.  
- Vẽ các điểm outlier bằng vòng tròn màu đỏ trong suốt (`alpha=0.5`).  

## 4. Ví dụ minh họa  

Dưới đây là các đoạn code trích từ notebook, được giữ nguyên để bạn có thể chạy lại.  

### 4.1 Cài đặt và cấu hình API Key  

```bash
!pip install -U -q google-generativeai
```

```python
import re, tqdm, numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
import google.generativeai as genai
from google.colab import userdata
from sklearn.datasets import fetch_20newsgroups
from sklearn.manifold import TSNE

API_KEY = userdata.get('API_KEY')
genai.configure(api_key=API_KEY)
```

### 4.2 Kiểm tra các model hỗ trợ embeddings  

```python
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(m.name)
# Output: models/embedding-001 (duplicated)
```

### 4.3 Chuẩn bị và lấy mẫu dữ liệu  

```python
newsgroups_train = fetch_20newsgroups(subset='train')
# Xóa email, tên, tiêu đề …
newsgroups_train.data = [re.sub(r'[\\w\\.-]+@[\\w\\.-]+', '', d) for d in newsgroups_train.data]
newsgroups_train.data = [re.sub(r"[()]*", "", d) for d in newsgroups_train.data]
newsgroups_train.data = [d.replace("From: ", "") for d in newsgroups_train.data]
newsgroups_train.data = [d.replace("\\nSubject: ", "") for d in newsgroups_train.data]
newsgroups_train.data = [d[:5000] if len(d) > 5000 else d for d in newsgroups_train.data]

df_train = pd.DataFrame(newsgroups_train.data, columns=['Text'])
df_train['Label'] = newsgroups_train.target
df_train['Class Name'] = df_train['Label'].map(newsgroups_train.target_names.__getitem__)

# Lấy 150 mẫu mỗi label
SAMPLE_SIZE = 150
df_train = (df_train.groupby('Label', as_index=False)
            .apply(lambda x: x.sample(SAMPLE_SIZE))
            .reset_index(drop=True))

# Chỉ giữ các nhóm science
df_train = df_train[df_train['Class Name'].str.contains('sci')]
df_train = df_train.reset_index(drop=True)
```

### 4.4 Tạo embeddings  

```python
from tqdm.auto import tqdm
tqdm.pandas()
from google.api_core import retry

def make_embed_text_fn(model):
    @retry.Retry(timeout=300.0)
    def embed_fn(text: str) -> list[float]:
        embedding = genai.embed_content(model=model,
                                        content=text,
                                        task_type="clustering")['embedding']
        return np.array(embedding)
    return embed_fn

def create_embeddings(df):
    model = 'models/embedding-001'
    df['Embeddings'] = df['Text'].progress_apply(make_embed_text_fn(model))
    return df

df_train = create_embeddings(df_train)
df_train.drop('index', axis=1, inplace=True)
```

### 4.5 Giảm chiều bằng t‑SNE  

```python
X = np.array(df_train['Embeddings'].tolist(), dtype=np.float32)   # shape (600, 768)

tsne = TSNE(random_state=0, n_iter=1000)
tsne_results = tsne.fit_transform(X)

df_tsne = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
df_tsne['Class Name'] = df_train['Class Name']
```

### 4.6 Vẽ scatter ban đầu  

```python
plt.figure(figsize=(8,6))
sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":"})
sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='Class Name', palette='Set2')
plt.title('Scatter plot of news using t-SNE')
plt.xlabel('TSNE1')
plt.ylabel('TSNE2')
plt.show()
```

### 4.7 Tính centroid (trong không gian embedding gốc)  

```python
def get_embedding_centroids(df):
    emb_centroids = {}
    grouped = df.groupby('Class Name')
    for c in grouped.groups:
        sub_df = grouped.get_group(c)
        emb_centroids[c] = np.mean(sub_df['Embeddings'].tolist(), axis=0)
    return emb_centroids

emb_c = get_embedding_centroids(df_train)
```

### 4.8 Vẽ centroid trên biểu đồ t‑SNE  

```python
centroids_df = pd.DataFrame([
    {'TSNE1': np.mean(df_tsne[df_tsne['Class Name']==c]['TSNE1']),
     'TSNE2': np.mean(df_tsne[df_tsne['Class Name']==c]['TSNE2']),
     'Class Name': c}
    for c in emb_c.keys()
])

plt.figure(figsize=(8,6))
sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":"})
sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='Class Name', palette='Set2')
sns.scatterplot(data=centroids_df, x='TSNE1', y='TSNE2',
                color="black", marker='X', s=100, label='Centroids')
plt.title('Scatter plot of news using t-SNE with centroids')
plt.xlabel('TSNE1')
plt.ylabel('TSNE2')
plt.legend(bbox_to_anchor=(1,1), loc='upper left')
plt.show()
```

### 4.9 Hàm detect outlier và tìm bán kính phù hợp  

```python
def detect_outlier(df, emb_centroids, radius):
    for idx, row in df.iterrows():
        class_name = row['Class Name']
        dist = np.sqrt(np.sum((row['Embeddings'] - emb_centroids[class_name])**2))
        df.at[idx, 'Outlier'] = dist > radius
    return df['Outlier'].sum()

# Thử các bán kính khác nhau
radius_list = np.arange(0.3, 0.75, 0.02).round(2).tolist()
outlier_counts = [detect_outlier(df_train.copy(), emb_c, r) for r in radius_list]

plt.figure(figsize=(14,8))
plt.bar(list(map(str, radius_list)), outlier_counts)
plt.title("Number of outliers vs. distance of points from centroid")
plt.xlabel("Distance (radius)")
plt.ylabel("Number of outliers")
for i, v in enumerate(outlier_counts):
    plt.text(i, v, str(v), ha='center')
plt.show()
```

### 4.10 Áp dụng bán kính chọn (ví dụ 0.62) và 시각 hoá outlier  

```python
RADIUS = 0.62
detect_outlier(df_train, emb_c, RADIUS)   # thêm cột Outlier vào df_train
df_outliers = df_train[df_train['Outlier'] == True]

# Lấy chỉ số của outlier để bản đồ trên t‑SNE
outliers_projected = df_tsne.loc[df_outliers.index]

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 10})
sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":"})
sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='Class Name', palette='Set2')
sns.scatterplot(data=centroids_df, x='TSNE1', y='TSNE2',
                color="black", marker='X', s=100, label='Centroids')
sns.scatterplot(data=outliers_projected, x='TSNE1', y='TSNE2',
                color='red', marker='o', alpha=0.5, s=90, label='Outliers')
plt.title('Scatter plot of news with outliers projected with t-SNE')
plt.xlabel('TSNE1')
plt.ylabel('TSNE2')
plt.legend(bbox_to_anchor=(1,1), loc='upper left')
plt.show()
```

### 4.11 In một vài ví dụ văn bản ngoại lai  

```python
for category in ['sci.crypt', 'sci.electronics', 'sci.med', 'sci.space']:
    cat_out = df_outliers[df_outliers['Class Name'] == category]
    if not cat_out.empty:
        print(f"\n--- {category} ---")
        print(cat_out['Text'].iloc[0])
```

## 5. Tổng kết  

- **Embedding** từ Gemini API (model `embedding-001`) cung cấp biểu diễn số học 768‑dimension cho văn bản, phù hợp với задача clustering khi thiết lập `task_type="clustering"`.  
- Quy trình phát hiện outlier gồm: (i) tạo embedding, (ii) tính centroid của mỗi lớp trong không gian embedding, (iii) đo khoảng cách Euclidean từ mỗi điểm tới centroid của lớp, (iv) coi điểm có khoảng cách vượt quá ngưỡng radius là outlier.  
- Giảm chiều bằng **t‑SNE** cho phép trực quan hóa phân bố và xác định trực quan các điểm lạ. Tuy nhiên t‑SNE có thể tốn thời gian收敛 và dễ rơi vào local minima; trong thực tế có thể cân nhắc **PCA** hoặc **UMAP** nếu cần tốc độ hoặc ổn định hơn.  
- Bán kính `radius` là siêu tham số điều chỉnh độ nhạy cảm của bộ detector; việc thử các giá trị khác nhau và quan sát số lượng outlier giúp chọn giá trị phù hợp với bài toán cụ thể.  
- Các bước trên có thể áp dụng cho bất kỳ bộ dữ liệu văn bản nào (tin tức, tài liệu pháp lý, phản hồi khách hàng …) để phát hiện các bản ghi không đuan với phân phối chính,從而 hỗ trợ chất lượng dữ liệu, giám sát truyException, hoặc phát hiện hội chứng lỗi.  

---  

*Hướng dẫn này được trích và biến đổi từ notebook ufficiali của Google Gemini API về **Anomaly detection with embeddings**. Todos mã code được giữ nguyên để đảm bảo tính chính xác khi thực thi.*