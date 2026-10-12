---
id: mX987wiZF7p3V_gExrPeX
slug: chunking
title: "Chunking"
original_title: "Chunking"
module_id: lVhWhZGR558O-ljHobxIi
module_title: "What are RAGs?"
language: vi
source_status: completed
---
# Chunking

Bước chia thành các đoạn (chunking) trong Retrieval-Augmented Generation (RAG) liên quan đến việc chia các tài liệu hoặc nguồn dữ liệu lớn thành các phần nhỏ, dễ quản lý. Điều này được thực hiện để đảm bảo rằng hệ thống truy xuất (retriever) có thể tìm kiếm hiệu quả trong khối lượng dữ liệu lớn mà vẫn nằm trong giới hạn token hoặc đầu vào của mô hình. Mỗi đoạn (thường là một đoạn văn hoặc một mục) được chuyển thành vector embedding, và các vector này được lưu trữ trong cơ sở dữ liệu vector. Khi có một truy vấn được đưa ra, hệ thống truy xuất sẽ tìm các đoạn có mức độ liên quan cao nhất thay vì toàn bộ tài liệu, từ đó giúp quá trình truy xuất nhanh chóng và chính xác hơn.

Tham khảo các nguồn tài nguyên sau để tìm hiểu thêm:

- [@article@Hiểu về RecursiveCharacterTextSplitter của LangChain](https://dev.to/eteimz/understanding-langchains-recursivecharactertextsplitter-2846)
- [@article@Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
- [@article@Hướng dẫn về các chiến lược chunking cho Retrieval Augmented Generation](https://zilliz.com/learn/guide-to-chunking-strategies-for-rag)