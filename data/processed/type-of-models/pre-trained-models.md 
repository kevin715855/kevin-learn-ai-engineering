# Pre-trained Models: Quá khứ, Hiện tại và Tương lai

## 1. Mục tiêu học tập

Sau khi học bài này, người học sẽ able to:

- Giải thích ý tưởng cơ bản và vai trò của các **pre‑trained model (PTM)** trong AI hiện nay.  
- Nêu rõ mối quan hệ giữa PTM, **transfer learning** và **self‑supervised learning**.  
- Liệt kê bốn hướng phát triển chính của PTM được đề cập trong bài survey.  
- Minh họa cách sử dụng một PTM (ví dụ: BERT) để fine‑tune trên một task cụ thể.  
- Nhận ra những thách thức mở còn lại trong nghiên cứu PTM.

## 2. Tổng quan

Các mô hình được **pre‑train** trên dữ liệu lớn (có hoặc không có nhãn) trước khi được áp dụng vào các bài toán cụ thể. Nhờ mục tiêu pre‑training phức tạp và số lượng tham số enormes, chúng có thể “lưu trữ” kiến thức từ massa dữ liệu và sau đó được **fine‑tune** để giải quyết các downstream task khác nhau. Điều này đã thay đổi cách tiếp cận trong AI: thay vì xây dựng mô hình từ đầu cho mỗi bài toán, cộng đồng如今 tende to sử dụng PTM như một **backbone** chung và chỉ cần điều chỉnh nhẹ cho từng ứng dụng.

Bài survey được trích dẫn (2021) cung cấp một cái nhìn tổng quan về lịch sử, những breakthroughs gần đây và những hướng nghiên cứu mở của PTM, đặc biệt trong lĩnh vực **natural language processing (NLP)** và **multimodal processing**.

## 3. Kiến thức cốt lõi

### 3.1. Lịch sử và quan hệ với Transfer learning & Self‑supervised learning  

- **Transfer learning**: ý tưởng sử dụng kiến thức đã học từ một domain để cải thiện hiệu suất trên domain khác. PTM là một hình thức đặc biệt của transfer learning nơi kiến thức được thu thập trong giai đoạn pre‑training trên dữ liệu rất lớn và không có nhãn (hoặc có nhãn rộng).  
- **Self‑supervised learning**: trong pre‑training, mô hình tự tạo ra các señal supervisión từ chính dữ liệu đầu vào (ví dụ: masked language model trong BERT, next‑token prediction trong GPT). Đây là nguồn động lực chính cho việc học biểu diễn mà không cần dữ liệu có nhãn thủ công.

### 3.2. Tại sao PTM hoạt động tốt  

1. **Kiến trúc sâu và tham số lớn** (trăm triệu đến hàng tỷ) cho khả năng biểu diễn phong phú.  
2. **Mục tiêu pre‑training** (masked language modeling, autoregressive language modeling, contrastive loss …) buộc mô hình học mối quan hệ ngữ cảnh và kiến thức về thế giới.  
3. **Lưu trữ kiến thức trong tham số** → khi fine‑tune trên một task nhỏ, chỉ cần điều chỉnh vài lớp cuối (hoặc các adaptor) để'exploitation kiến thức đã học.

### 3.3. Những breakthroughs gần đây (theo bài survey)

Nhờ sự tăng công suất tính toán và khả năng truy cập dữ liệu, PTM phát triển theo bốn hướng chính:

| Hướng rozwoj | Mô tả ngắn gọn |
|--------------|----------------|
| **Thiết kế kiến trúc hiệu quả** |Các biến thể như **Transformer‑based** (BERT, GPT, T5), **sparse attention**, **mixture‑of‑experts** để mở rộng mô hình mà không tăng tuyến tính chi phí tính toán. |
| **Sử dụng bối cảnh phong phú** |Kết hợp dữ liệu đa modal (text‑image, audio‑video) hoặc sử dụng kiến thức bên ngoài (knowledge graph, retrieval‑augmented). |
| **Nâng cao hiệu suất tính toán** |Kỹ thuật quantization, pruning, distillation, và các thuật toán huấn luyện hiệu quả (mixed‑precision, sharding). |
| **Giải thích và phân tích lý thuyết** |Nghiên cứu về biểu diễnภายใน, probing, và các công cụ trực quan hóa để hiểu vì sao PTM hoạt động; cũng như phân tích tổng quat của các giới hạn generalization. |

### 3.4. Những vấn đề mở và hướng nghiên cứu trong tương lai  

- **Effectiveness vs. efficiency**: Cân bằng giữa mô hình lớn và tài nguyên hạn chế.  
- **Bias và fairness**: Hiểu và giảm thiểu các biểu現 xã hội không mong muốn vốn có trong dữ liệu pre‑train.  
- **Generalization ra ngoài distribución**: Độ bền vững khi gặp dữ liệu ngoại répartition (OOD).  
- **Đa modal và đa nhiệm**: Xây dựng một mô hình duy nhất có thể xử lý đồng thời text, hình ảnh, âm thanh và video một cách thống nhất.  
- **Lý thuyết dự đoán scaling laws**: Phát triển mô hình lý thuyết để dự đoán lợi nhuận khi tăng dữ liệu, tham số và compute.

## 4. Ví dụ minh họa

### 4.1. Minh họa kiến trúc và cách thức pre‑training (BERT)

BERT sử dụng **masked language model (MLM)**: trong mỗi câu, một phần các token được thay đổi bằng `[MASK]` và mô hình phải dự đoán chúng dựa trên bối cảnh xung quanh.

```python
# Pseudocode for BERT MLM objective (simplified)
for batch in data_loader:
    input_ids, attention_mask = batch
    # Randomly mask 15% tokens
    masked_input, labels = mask_tokens(input_ids)
    # Forward pass
    logits = bert_model(masked_input, attention_mask=attention_mask)
    # Compute cross‑entropy loss only on masked positions
    loss = loss_fct(logits.view(-1, vocab_size), labels.view(-1))
    loss.backward()
    optimizer.step()
```

Kết quả: sau pre‑training trên bộ dữ liệu lớn (BookCorpus + Wikipedia), BERT học được biểu diễn ngữ cảnh phong phú mà có thể được tái sử dụng cho nhiều task như phân loại cảm xúc, trả lời câu hỏi, v.v.

### 4.2. Fine‑tuning BERT cho phân loại cảm xúc (SST‑2)

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from datasets import load_dataset

# Load dataset
dataset = load_dataset("glue", "sst2")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def preprocess(example):
    return tokenizer(example["sentence"], truncation=True, padding="max_length", max_length=128)

encoded = dataset.map(preprocess, batched=True)

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded["train"],
    eval_dataset=encoded["validation"],
)

trainer.train()
```

**Giải thích**:  
- `BertForSequenceClassification` thêm một lớp dense trên top của BERT để đưa ra 확률 cho hai lớp (tích cực / tiêu cực).  
- Chỉ cần huấn luyện vài epoch trên bộ dữ liệu nhỏ (SST‑2) là mô hình đã đạt độ chính xác > 90 %, thể hiện sức mạnh của kiến thức đã được lưu trữ trong BERT qua pre‑training.

### 4.3. Minh họa một hướng “sử dụng bối cảnh phong phú”: модель **CLIP** (Contrastive Language‑Image Pre‑training)

CLIP pre‑train trên cặp (ảnh, mô tả text) bằng contrastive loss, cho phép mô hình học mối quan hệ giữa hình ảnh và ngôn ngữ. Sau pre‑training, CLIP có thể thực hiện zero‑shot image classification mà không cần fine‑tune trên bất kỳ label ảnh nào.

## 5. Tổng kết

- Các **pre‑trained model** như BERT, GPT đã trở thành “backbone” tiêu chuẩn trong AI nhờ khả năng học biểu diễn phong phú từ dữ liệu lớn qua self‑supervised objectives.  
- Chúng nằm ở giao điểm giữa **transfer learning** và **self‑supervised learning**, cho phép áp dụng nhanh chóng vào nhiều downstream task chỉ bằng việc fine‑tune nhẹ.  
- Các breakthroughs gần đây tập trung vào: (i) thiết kế kiến trúc hiệu quả, (ii) khai báo bối cảnh đa dạng và phong phú, (iii) nâng cao hiệu suất tính toán, và (iv)深化解释与理论分析。  
- Tuy nhiên, còn nhiều thách thức mở như cân bằng hiệu quả‑tính toán, xử lý bias, tăng cường generalization OOD và phát triển lý thuyết dự đoán scaling. Những hướng này sẽ định hình nghiên cứu PTM trong những năm tới.  

Việc nắm vững những khái niệm trên sẽ giúp người học không chỉ hiểu tại sao PTM mạnh mà còn biết cách áp dụng và tiếp tục khám phá nhữngfrontier nghiên cứu trong lĩnh vực này.