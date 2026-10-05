# Báo cáo Đánh giá và Xác minh Nguồn Dữ liệu Roadmap.sh (AI Engineer)

Báo cáo này thực hiện khảo sát, xác minh các nguồn dữ liệu cho lộ trình AI Engineer trên `roadmap.sh`, đánh giá giấy phép bản quyền, cấu trúc nội dung và đề xuất chiến lược xử lý cho công cụ trích xuất (Extractor).

---

## 1. Kiểm tra URL `https://roadmap.sh/ai-engineer.json`

- **Trạng thái**: Tồn tại và hoạt động ổn định (**HTTP 200 OK**).
- **Cấu trúc dữ liệu trả về**:
  - Dạng JSON object chứa toàn bộ cấu trúc sơ đồ của lộ trình AI Engineer.
  - Các trường chính bao gồm: `_id`, `title`, `description`, `slug`, `nodes` (danh sách các topic/node trên bản đồ), `edges` (quan hệ kết nối giữa các node), `courses`, `seo`, v.v.
- **Đánh giá**: Endpoint này rất thích hợp để trích xuất cấu trúc tổng quan (roadmap discovery, topology, grouping, categories), nhưng có thể thay đổi hoặc gặp giới hạn (rate limit) nếu gọi trực tiếp liên tục.

---

## 2. Khảo sát Nguồn Thay thế ổn định hơn: Kho lưu trữ GitHub `developer-roadmap`

- **Nguồn GitHub chính thức**: `https://github.com/kamranahmedse/developer-roadmap`
- **Đường dẫn dữ liệu AI Engineer**:
  - Metadata sơ đồ: Có thể lấy từ API hoặc file cấu hình trong repo.
  - Nội dung bài học (lessons/topics): Thư mục `roadmaps/ai-engineer/content/` chứa hàng loạt tệp Markdown (`*.md`) tương ứng với từng node/topic trên roadmap (ví dụ: `ai-agents@Uffu609uQbIzDl88Ddccv.md`, `anthropic-claude@hy6EyKiNxk1x84J63dhez.md`, v.v.).
- **Đề xuất nguồn nên dùng (Hybrid / Combined Source)**:
  - Sử dụng **file JSON từ `roadmap.sh`** (hoặc bản sao đã chuẩn hóa) để nắm bắt cấu trúc cây/đồ thị lộ trình (nodes, edges, groups).
  - Sử dụng **kho lưu trữ GitHub `kamranahmedse/developer-roadmap`** (tải trực tiếp raw files từ `roadmaps/ai-engineer/content/`) làm nguồn nội dung Markdown chính cho từng bài học.
  - **Lý do**: Kho GitHub cực kỳ ổn định, có thể clone/submodule hoặc fetch qua raw URL, tránh phụ thuộc hoàn toàn vào API web của roadmap.sh và dễ dàng quản lý version control.

---

## 3. Kiểm tra Giấy phép và Điều khoản Bản quyền (License)

- **Nguồn kiểm tra**: Tệp `license` trong kho `kamranahmedse/developer-roadmap`.
- **Nội dung điều khoản**:
  - Toàn bộ nội dung, văn bản và hình ảnh trong dự án được bảo hộ bởi luật bản quyền (Copyright © Kamran Ahmed).
  - **Quy định sử dụng**: Cho phép sử dụng cho mục đích cá nhân (personal use). **Không cho phép** tái xuất bản (publish), đăng lại nội dung, hình ảnh hoặc tệp dự án lên bất kỳ phương tiện nào khác (blog posts, articles, newsletters, v.v.) mà không có sự đồng ý trước bằng văn bản từ tác giả.
  - **Ngoại lệ**: Các bản fork read-only trên GitHub phục vụ mục đích đóng góp cho dự án (`contributing`).
- **Ý nghĩa đối với dự án**:
  - Công cụ trích xuất, dịch và chuẩn hóa (`roadmap-ai-engineer`) phục vụ mục đích nghiên cứu, học tập cá nhân/nội bộ.
  - Nếu muốn phân phối hoặc công khai thương mại/cộng đồng, cần xin phép tác giả hoặc giữ nguyên thông tin ghi nguồn, tuân thủ giới hạn sử dụng công hợp lý (fair use / educational reference).

---

## 4. Đánh giá Độ dày Nội dung Mỗi Topic & Chiến lược Chống Bịa đặt (Hallucination) của LLM

### 4.1. Độ dày nội dung
- Hầu hết các tệp Markdown (`content/*.md`) của mỗi topic có dung lượng vừa phải (thường từ vài đoạn văn bản ngắn, định nghĩa cốt lõi, danh sách gầu đầu dòng, và các liên kết tham khảo đến tài liệu chính thức, bài viết, video).
- Không phải topic nào cũng có nội dung dài; nhiều topic chỉ là tóm tắt ngắn gọn kèm links.

### 4.2. Nguy cơ LLM Hallucination
- Khi sử dụng LLM để dịch sang tiếng Việt hoặc chuẩn hóa, LLM có xu hướng tự ý thêm thắt nội dung, mở rộng dài dòng hoặc bịa đặt các khái niệm kỹ thuật/ví dụ code không có trong bản gốc (`source`).

### 4.3. Đề xuất Chiến lược Chống Bịa đặt (Hallucination Prevention Strategy)
1. **Strict Source Grounding (Ràng buộc nguồn nghiêm ngặt)**:
   - System prompt cho LLM phải quy định rõ: *Chỉ dịch và cấu trúc lại đúng nội dung có sẵn trong tệp Markdown gốc. Không tự thêm thông tin kỹ thuật, không bịa thêm ví dụ code hoặc số liệu không xuất hiện trong nguồn.*
2. **Key Takeaways & References Preservation**:
   - Giữ nguyên các đường dẫn (URLs) và tài liệu tham khảo gốc từ tác giả.
   - Phân tách rõ phần "Nội dung gốc dịch chuẩn" và phần "Ghi chú/Mở rộng tùy chọn" (nếu có yêu cầu mở rộng phải đánh dấu rõ ràng).
3. **Contract & Schema Validation**:
   - Áp dụng các schema validation (như Contract C, D, E trong dự án) để kiểm tra các trường bắt buộc (`title`, `summary`, `body`, `references`), đảm bảo không có trường dữ liệu rỗng hoặc sinh ra sai lệch cấu trúc.
4. **Deterministic Processing & Temperature = 0**:
   - Sử dụng nhiệt độ thấp (temperature = 0 hoặc 0.2) khi gọi API LLM để giảm thiểu tính ngẫu nhiên và sáng tạo ngoài mong đợi.

---

## 5. Kết luận & Đề xuất Tiếp theo
- Nguồn dữ liệu kết hợp (JSON API từ `roadmap.sh` + Markdown content từ repo GitHub `developer-roadmap`) là khả thi và tối ưu nhất.
- Đã hoàn tất đánh giá nguồn và sẵn sàng chờ phê duyệt trước khi chuyển sang **Task 1.1** (Xây dựng module discovery và crawl dữ liệu thô).
