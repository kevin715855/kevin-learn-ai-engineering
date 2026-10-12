---
id: mX987wiZF7p3V_gExrPeX
language: vi
module: hugging-face
module_id: v99C5Bml2a6148LCJ9gy9
module_title: Hugging Face
order: 13
original_title: Chunking
slug: chunking
source_status: completed
status: completed
title: Chunking
---
# Chunking

The chunking step in Tăng cường Thế hệ bằng Truy xuất (RAG) (RAG) involves breaking down large documents or data sources into smaller, manageable chunks. This is done to ensure that the retriever can efficiently search through large volumes of data while staying within the Token or input limits of the model. Each chunk, typically a paragraph or section, is converted into an Biểu diễn nhúng (Embedding), and these Biểu diễn nhúng (Embeddings) are stored in a Cơ sở dữ liệu Vector. When a query is made, the retriever searches for the most relevant chunks rather than the entire document, enabling faster and more accurate retrieval.

Visit the following resources to learn more:

- [@article@Understanding LangChain's RecursiveCharacterTextSplitter](https://dev.to/eteimz/understanding-langchains-recursivecharactertextsplitter-2846)
- [@article@Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
- [@article@A Guide to Chunking Strategies for Retrieval Augmented Generation](https://zilliz.com/learn/guide-to-chunking-strategies-for-rag)