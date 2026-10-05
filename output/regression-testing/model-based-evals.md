---
id: LJ6_U5lOdc0uRngutj7Ro
slug: model-based-evals
title: "Đánh giá dựa trên mô hình"
original_title: "Model-Based Evals"
module_id: Bkzi3QyzKyHxcHE7sodRZ
module_title: "Regression Testing"
language: vi
source_status: completed
---
# Đánh giá dựa trên mô hình

Đánh giá dựa trên mô hình sử dụng một mô hình AI riêng để tự động chấm điểm hoặc đánh giá đầu ra của ứng dụng LLM của bạn. Thay vì viết các quy tắc thủ công hoặc dựa trên con người đánh giá, bạn chuyển giao việc phán xét cho một mô hình khác, một kỹ thuật thường được gọi là LLM-as-a-Judge. Bạn viết một prompt mô tả tiêu chí đánh giá, và mô hình judge sẽ xếp hạng phản hồi. Phương pháp này có thể xử lý các khía cạnh chất lượng chủ quan, mở rộng mà các quy tắc không thể nắm bắt được, đồng thời mở rộng quy mô với chi phí thấp hơn rất nhiều so với đánh giá của con người, mặc dù đòi hỏi phải thiết kế prompt kỹ lưỡng để tránh thiên lệch và mâu thuẫn trong chính các mô hình judge.

Truy cập các tài nguyên sau đây để tìm hiểu thêm:

- [@article@A pragmatic guide to LLM evals for devs](https://newsletter.pragmaticengineer.com/p/evals)
- [@article@LLM-as-a-judge: một hướng dẫn đầy đủ về việc sử dụng LLMs để đánh giá]
- [@video@LLM as a Judge: Scaling AI Evaluation Strategies](https://www.youtube.com/watch?v=trfUBIDeI1Y)