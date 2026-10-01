---
id: WZVW8FQu6LyspSKm1C_sl
slug: using-sdks-directly
title: "Using SDKs Directly"
original_title: "Using SDKs Directly"
module_id: 4_ap0rD9Gl6Ep_4jMfPpG
module_title: "AI Agents"
language: vi
source_status: completed
---

# Using SDKs Directly

While tools like Langchain and LlamaIndex make it easy to implement RAG, you don't have to necessarily learn and use them. If you know about the different steps of implementing RAG, you can simply do it all yourself e.g., do the chunking using `@langchain/textsplitters` package, create Biểu diễn nhúng (Embeddings) using any LLM e.g., use OpenAI Biểu diễn nhúng (Embedding) API through their SDK, save the Biểu diễn nhúng (Embeddings) to any Cơ sở dữ liệu Vector e.g. if you are using Supabase Vector DB, you can use their SDK, and similarly, you can use the relevant SDKs for the rest of the steps as well.

Visit the following resources to learn more:

- [@official@Langchain Text Splitter Package](https://www.npmjs.com/package/@langchain/textsplitters)
- [@official@OpenAI Biểu diễn nhúng (Embedding) API](https://platform.openai.com/docs/guides/Biểu diễn nhúng (Embeddings))
- [@official@Supabase AI & Vector Documentation](https://supabase.com/docs/guides/ai)