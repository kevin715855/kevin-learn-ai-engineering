---
id: WZVW8FQu6LyspSKm1C_sl
slug: using-sdks-directly
title: "Sử dụng SDKs trực tiếp"
original_title: "Using SDKs Directly"
module_id: 4_ap0rD9Gl6Ep_4jMfPpG
module_title: "AI Agents"
language: vi
source_status: completed
---
# Sử dụng SDKs trực tiếp

Mặc dù các công cụ như Langchain và LlamaIndex giúp việc triển khai RAG trở nên dễ dàng, bạn không nhất thiết phải học và sử dụng chúng. Nếu bạn biết các bước khác nhau trong việc triển khai RAG, bạn có thể tự thực hiện toàn bộ quy trình, ví dụ: thực hiện chunking bằng gói `@langchain/textsplitters`, tạo embedding bằng bất kỳ mô hình LLM nào, ví dụ: sử dụng API Embedding của OpenAI qua SDK của họ, lưu embedding vào bất kỳ cơ sở dữ liệu vector nào, ví dụ: nếu bạn đang sử dụng Supabase Vector DB, bạn có thể dùng SDK của họ, và tương tự, bạn cũng có thể dùng các SDK phù hợp cho các bước còn lại.

Truy cập các nguồn lực sau đây để tìm hiểu thêm:

- [@official@Langchain Gói tách văn bản](https://www.npmjs.com/package/@langchain/textsplitters)
- [@official@API Nhúng OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [@official@Tài liệu Supabase AI & Vector](https://supabase.com/docs/guides/ai)