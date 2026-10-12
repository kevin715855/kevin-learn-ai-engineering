# @huggingface/inference – Thư viện TypeScript để gọi mô hình Hugging Face

## 1. Mục tiêu học tập

Sau khi đọc bài học này, bạn sẽ biết:

* Cài đặt và khởi tạo `InferenceClient` để truy cập các dịch vụ Hugging Face.
* Sử dụng Inference Providers (các nhà cung cấp bên thứ ba) để chạy inference mà không cần tự quản lý máy chủ.
* Xử lý lỗi bằng các lớp lỗi đặc biệt của gói.
* Gọi các tác vụ phổ biến: sinh văn bản, chat completion, trích xuất đặc trưng, dịch, OCR, … và các tác vụ âm thanh, hình ảnh, đa phương tiện, bảng.
* Kết nối tới Inference Endpoints (dịch vụ sản xuất) và tới các máy chủ inference cục bộ (llama.cpp, Ollama, vLLM, TGI …).
* Áp dụng tree‑shaking để giảm kích thước bundle.
* Chạy test và tìm mô hình phù hợp trên Hugging Face Hub.

## 2. Tổng quan

`@huggingface/inference` là một wrapper TypeScript cung cấp một giao diện thống nhất để thực hiện inference trên nhiều dịch vụ khác nhau:

1. **Inference Providers** – kết nối tới các nhà cung cấp máy chủ không quản lý (Fal.ai, Replicate, Together, Groq …) qua Hugging Face Hub.
2. **Inference Endpoints** – triển khai mô hình riêng trên hạ tầng完全 quản lý của Hugging Face.
3. **Local endpoints** – kết nối tới máy chủ inference chạy trên máy local nếu chúng tuân thủ API tương thích OpenAI.

Gói này hỗ trợ cả API đồng bộ và streaming, cung cấp các lớp lỗi chi tiết để giúp debug, và cho phép tree‑shaking khi chỉ cần một số hàm cụ thể.

## 3. Kiến thức cốt lõi

### 3.1 Cài đặt

```bash
# npm
npm install @huggingface/inference
# pnpm
pnpm add @huggingface/inference
# yarn
yarn add @huggingface/inference
```

### 3.2 Khởi tạo client

```ts
import { InferenceClient } from '@huggingface/inference';

const hf = new InferenceClient('your access token');
```

> **Lưu ý quan trọng:** Token truy cập phải được giữ bí mật. Nếu dùng trong frontend, hãy đặt token trên một proxy/server riêng để tránh lộ mã thông báo.

### 3.3 Sử dụng Inference Providers

Khi tạo yêu cầu, truyền tham số `provider` để chỉ định nhà cung cấp. Giá trị mặc định là `"auto"` – hệ thống sẽ chọn nhà cung cấp đầu tiên trong danh sách ưu tiên của bạn (cấu hình tại https://hf.co/settings/inference-providers).

```ts
const client = new InferenceClient('hf_...'); // hoặc API key của provider (ví dụ: Replicate)

await client.textToImage({
  provider: 'replicate',
  model: 'black-forest-labs/Flux.1-dev',
  inputs: 'A black forest cake'
});
```

Chỉ một subset của các model được hỗ trợ bởi mỗi provider. Danh sách model tương thích có thể tra cứu qua các endpoint như:

```
https://huggingface.co/api/partners/<provider-id>/models
```

### 3.4 Xử lý lỗi

Gói định nghĩa các lớp lỗi kế thừa từ `Error`:

| Lỗi | Khi nào xảy ra | Thuộc tính quan trọng |
|-----|----------------|----------------------|
| `InferenceClientError` | Lỗi cơ bản | `message` |
| `InferenceClientInputError` | Tham số đầu vào không hợp lệ | `message` |
| `InferenceClientProviderApiError` | Lỗi API từ provider (rate limit, auth…) | `message`, `request`, `response` |
| `InferenceClientHubApiError` | Lỗi API từ Hugging Face Hub | `message`, `request`, `response` |
| `InferenceClientProviderOutputError` | Phản hồi từ provider không đúng định dạng mong đợi | `message` |

Ví dụ bắt lỗi chi tiết:

```ts
import {
  InferenceClientError,
  InferenceClientProviderApiError,
  InferenceClientHubApiError,
  InferenceClientProviderOutputError,
  InferenceClientInputError,
} from '@huggingface/inference';

try {
  const result = await hf.textGeneration({
    model: 'gpt2',
    inputs: 'Hello, I am a language model',
  });
} catch (err) {
  if (err instanceof InferenceClientProviderApiError) {
    console.error('Provider API Error:', err.message);
    console.error('Request:', err.request);
    console.error('Response:', err.response);
  } else if (err instanceof InferenceClientHubApiError) {
    console.error('Hub API Error:', err.message);
    console.error('Request:', err.request);
    console.error('Response:', err.response);
  } else if (err instanceof InferenceClientProviderOutputError) {
    console.error('Provider Output Error:', err.message);
  } else if (err instanceof InferenceClientInputError) {
    console.error('Input Error:', err.message);
  } else {
    console.error('Unexpected error:', err);
  }
}
```

### 3.5 Tree‑shaking

Nếu chỉ cần một số hàm, import trực tiếp từ module để công cụ đóng gói (webpack, esbuild, Rollup…) có thể loại bỏ code không dùng:

```ts
import { textGeneration } from '@huggingface/inference';

await textGeneration({
  accessToken: 'hf_...',
  model: 'mistralai/Mixtral-8x7B-v0.1',
  inputs: 'The answer to the universe is',
  parameters: { max_new_tokens: 50 }
});
```

### 3.6 Các tác vụ chính

#### Xử lý ngôn ngữ tự nhiên (NLP)

* **Text generation** – `textGeneration`, `textGenerationStream`.
* **Chat completion** – `chatCompletion`, `chatCompletionStream`.
* **Feature extraction** – `featureExtraction`.
* **Fill‑mask** – `fillMask`.
* **Summarization** – `summarization`.
* **Question answering** – `questionAnswering`.
* **Table question answering** – `tableQuestionAnswering`.
* **Text classification** – `textClassification`.
* **Token classification** – `tokenClassification`.
* **Translation** – `translation` (có thể chỉ định `src_lang`, `tgt_lang`).
* **Zero‑shot classification** – `zeroShotClassification`.
* **Sentence similarity** – `sentenceSimilarity`.
* **Text ranking** – `textRanking`.

#### Âm thanh (Audio)

* **Automatic speech recognition** – `automaticSpeechRecognition`.
* **Audio classification** – `audioClassification`.
* **Text‑to‑speech** – `textToSpeech`.
* **Audio‑to‑audio** – `audioToAudio`.

#### Thị giác (Computer Vision)

* **Image classification** – `imageClassification`.
* **Object detection** – `objectDetection`.
* **Image segmentation** – `imageSegmentation`.
* **Image‑to‑text** – `imageToText` (OCR, captioning).
* **Text‑to‑image** – `textToImage`.
* **Image‑to‑image** – `imageToImage`.
* **Zero‑shot image classification** – `zeroShotImageClassification`.

#### Đa phương tiện (Multimodal)

* **Visual question answering** – `visualQuestionAnswering`.
* **Document question answering** – `documentQuestionAnswering`.

#### Bảng (Tabular)

* **Tabular regression** – `tabularRegression`.
* **Tabular classification** – `tabularClassification`.

Mỗi hàm nhận đối số đầu vào tương ứng (ví dụ: `inputs` là chuỗi, blob, hoặc đối tượng có cấu trúc) và tùy chọn `parameters` để điều chỉnh hành vi mô hình (temperature, max_tokens, …).

### 3.7 Kết nối tới Inference Endpoints (sản xuất)

Sau khi triển khai mô hình trên Hugging Face Inference Endpoints, bạn nhận được một URL privado. Ví dụ:

```ts
import { InferenceClient } from '@huggingface/inference';

const hf = new InferenceClient('hf_xxxxxxxxxxxxxx', {
  endpointUrl:
    'https://j3z5luu0ooo76jnl.us-east-1.aws.endpoints.huggingface.cloud/v1/',
});

const response = await hf.chatCompletion({
  messages: [{ role: 'user', content: 'What is the capital of France?' }],
});

console.log(response.choices[0].message.content);
```

Nếu endpoint được cấu hình **scale‑to‑0**, yêu cầu đầu tiên có thể phải chờ tải mô hình. Để tắt hành vi chờ và xử lý lỗi 500 tự thân, truyền `{ retry_on_error: false }` vào hàm gọi.

### 3.8 Sử dụng local endpoints (llama.cpp, Ollama, vLLM, TGI …)

Nếu bạn chạy một máy chủ inference cục bộ tuân thủ API OpenAI, chỉ cần truyền `endpointUrl` và không cần access token:

```ts
import { InferenceClient } from '@huggingface/inference';

const hf = new InferenceClient(undefined, {
  endpointUrl: 'http://localhost:8080', // ví dụ: server llama.cpp
});

const response = await hf.chatCompletion({
  messages: [{ role: 'user', content: 'What is the capital of France?' }],
});

console.log(response.choices[0].message.content);
```

### 3.9 Chạy test

Để chạy bộ test của gói (yêu cầu có token Hugging Face):

```bash
HF_TOKEN="your access token" pnpm run test
```

### 3.10 Tìm modèles phù hợp

Trang https://huggingface.co/tasks liệt kê các tác vụ, kèm mô hình mẫu, demo và giải thích chi tiết. Bạn có thể lọc theo thư viện, độ lớn, mức độ tài nguyên … để chọn mô hình tốt nhất cho use‑case của mình.

### 3.11 Dependencies

* `@huggingface/tasks` – chỉ cung cấp các kiểu TypeScript cho các tác vụ, không có runtime dependency lớn.

## 4. Ví dụ minh họa

### 4.1 Tạo ảnh từ prompt sử dụng provider Replicate

```ts
import { InferenceClient } from '@huggingface/inference';

const client = new InferenceClient('hf_your_token'); // hoặc API key Replicate
await client.textToImage({
  provider: 'replicate',
  model: 'black-forest-labs/Flux.1-dev',
  inputs: 'a picture of a green bird',
});
```

### 4.2 Streaming chat completion với mô hình Cerebras

```ts
import { InferenceClient } from '@huggingface/inference';

const hf = new InferenceClient('hf_your_token');

let answer = '';
for await (const chunk of hf.chatCompletionStream({
  model: 'Qwen/Qwen3-32B',
  provider: 'cerebras',
  messages: [{ role: 'user', content: 'Can you help me solve an equation?' }],
  max_tokens: 512,
  temperature: 0.1,
})) {
  if (chunk.choices?.[0]?.delta?.content) {
    answer += chunk.choices[0].delta.content;
    process.stdout.write(chunk.choices[0].delta.content); // hiển thị real‑time
  }
}
console.log('\nĐã hoàn thành:', answer);
```

### 4.3 Xử lý lỗi khi gọi API Hugging Face Hub

```ts
import { InferenceClient, InferenceClientHubApiError } from '@huggingface/inference';

const hf = new InferenceClient('hf_your_token');

try {
  await hf.textGeneration({ model: 'non-existent-model', inputs: 'test' });
} catch (e) {
  if (e instanceof InferenceClientHubApiError) {
    console.error('Lỗi Hub:', e.message);
    console.error('Status:', e.response?.status);
  } else {
    console.error('Lỗi khác:', e);
  }
}
```

## 5. Tổng kết

* `@huggingface/inference` cung cấp một giao diện thống nhất,Type‑safe để gọi mô hình trên Hugging Face Hub, các nhà cung cấp bên thứ ba, Inference Endpoints và các máy chủ local.
* Việc khởi tạo đơn giản: `new InferenceClient(token)`; cần luôn bảo vệ token truy cập.
* Các tham số quan trọng (`provider`, `model`, `inputs`, `parameters`) cho phép linh hoạt chọn dịch vụ và tinh chỉnh đầu ra.
* Gói cung cấp hệ thống lỗi chi tiết giúp debug nhanh chóng, và hỗ trợ tree‑shaking để tối ưu bundle size.
* Nhiều tác vụ NLP, âm thanh, eyesight, đa phương tiện và bảng đều có sẵn; bạn chỉ cần gọi hàm tương ứng.
* Khi chuyển từ môi trường prototype sang production, hãy chuyển sang Inference Endpoints hoặc tự-hosted local server và cấu hình `endpointUrl` cho client.
* Để test và tìm mô hình, sử dụng biến môi trường `HF_TOKEN` và trang Tasks trên Hugging Face.

Với những kiến thức trên, bạn có thể tích hợp nhanh chóng các mô hình AI tiên tiến vào ứng dụng JavaScript/TypeScript của mình, từ prototypes nhanh chóng cho tới dịch vụ sản xuất vững chắc. Happy coding!