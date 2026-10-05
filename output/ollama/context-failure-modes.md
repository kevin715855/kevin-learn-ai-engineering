---
id: mfiiWDVZEeUGFa6KKUGLB
slug: context-failure-modes
title: "Bối cảnh các chế độ lỗi"
original_title: "Context Failure Modes"
module_id: rTT2UnvqFO3GH6ThPLEjO
module_title: "Ollama"
language: vi
source_status: completed
---
# các chế độ lỗi trong bối cảnh

Các trạng thái lỗi của ngữ cảnh là những cách phổ biến mà một context pipeline có thể xảy ra lỗi và làm giảm hiệu suất của một agent. Các trường hợp này bao gồm context poisoning, khi thông tin sai được đưa vào và được coi là sự thật; context distraction, khi quá nhiều nội dung không liên quan làm mất tập trung của mô hình từ những điều quan trọng; và context rot, khi độ chính xác giảm khi lượng nội dung tăng lên ngay cả trong phạm vi đã khai báo của mô hình. Các lỗi khác bao gồm stale data không còn phản ánh thực tế và thông tin mâu thuẫn từ các nguồn khác nhau mà mô hình không thể hòa giải.

Hãy truy cập các nguồn sau để tìm hiểu thêm.

- [@article@How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)
- [@article@Hiểu các chế độ thất bại của LLM (Và tại sao chúng quan trọng hơn chính mô hình)](https://medium.com/@RamPrakashD/understanding-llm-failure-modes-and-why-they-matter-more-than-the-model-itself-2104edccf3cd)
- [@article@Các Đồi Trình Code Không Cần Cửa Sổ Bối Cảnh Lớn — Họ Cần Một Trình Biên Dịch Bối Cảnh](https://towardsdatascience.com/coding-agents-dont-need-bigger-context-windows-they-need-a-context-compiler/)
- [@video@Các Mẫu Lỗi RAG, Giải Thích](https://www.youtube.com/watch?v=1nI0hX9dvD4&t=32s)