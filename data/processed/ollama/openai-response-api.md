# Viết bài học kỹ thuật bằng Markdown

## 1. Mục tiêu học tập

Sau khi hoàn thành bài học này, người học sẽ能够:

- Nêu được các thành phần cơ bản của một bài học kỹ thuật theo định dạng Markdown.  
- Áp dụng các cú pháp Markdown phổ biến (tiêu đề, danh sách, mã, bảng, liên kết, hình ảnh) để tạo tài liệu có cấu trúc rõ ràng.  
- Viết một ví dụ minh họa ngắn gọn trong Markdown, bao gồm mã nguồn và giải thích.  
- Tổng kết lại những điểm cần lưu ý để tài liệu dễ đọc, dễ bảo trì và phù hợp với mục đích giảng dạy.

## 2. Tổng quan

Markdown là ngôn ngữ đánh dấu nhẹ, dễ học và được hỗ trợ rộng rãi trong các nền tảng ghi chú, hệ thống quản lý tài liệu (GitHub, GitLab, Notion…) và công cụ tạo trang web static. Khi viết bài học kỹ thuật, sử dụng Markdown giúp:

- Tập trung vào nội dung thay vì lo lắng về định dạng phức tạp.  
- Dễ dàng phiên bản và cộng tác qua hệ thống kiểm soát phiên bản (Git).  
- Xuất ra nhiều định dạng khác nhau (HTML, PDF, slide) bằng công cụ như Pandoc hoặc MkDocs.  

Bài học này sẽ hướng dẫn bạn xây dựng một bài học Markdown có cấu trúc chuẩn: **Mục tiêu → Tổng quan → Kiến thức cốt lõi → Ví dụ minh họa → Tổng kết**.

## 3. Kiến thức cốt lõi

### 3.1 Cấu trúc cơ bản của bài học

```markdown
# Tên bài học

## 1. Mục tiêu học tập
...

## 2. Tổng quan
...

## 3. Kiến thức cốt lõi
...

## 4. Ví dụ minh họa
...

## 5. Tổng kết
...
```

### 3.2 Các thành phần Markdown thường dùng

| Thành phần | Cú pháp | Mô tả |
|------------|---------|-------|
| Tiêu đề cấp 1 | `# Tiêu đề` | Tên bài học |
| Tiêu đề cấp 2 | `## Tiêu đề` | Các phần chính |
| In đậm | `**văn bản**` | Nhấn mạnh khái niệm quan trọng |
| In nghiêng | `*văn bản*` | Nhấn mạnh nhẹ hoặc định danh |
| Mã nguồn nội dòng | `` `code` `` | Đánh dấu từ khóa, tên hàm |
| Khối mã | ``` ```python\ncode\n``` ``` | Hiển thị đoạn mã với syntax highlight (nếu công cụ hỗ trợ) |
| Danh sách không thứ tự | `- mục` | Liệt kê ý tưởng |
| Danh sách có thứ tự | `1. mục` | Các bước thực hiện theo thứ tự |
| Bảng | `| Header | Header |\n|---|---|\n| cell | cell |` | Trình bày thông tin có cấu trúc |
| Liên kết | `[texto](URL)` | Tham chiếu tới tài nguyên ngoài |
| Hình ảnh | `![alt text](path/to/image.png)` | Chèn minh họa visual |
| Trích dẫn | `> nội dung` | Nhấn mạnh lời dẫn hoặc ghi chú |

### 3.3 Lưu ý khi viết bài học kỹ thuật

- **Nhất quán kiểu dấu**: dùng cùng một kiểu tiêu đề, danh sách và dấu cách trong toàn bộ tài liệu.  
- **Tránh mã hóa HTML không cần thiết** nếu mục tiêu là giữ tài liệu độc lập với nền tảng.  
- **Đóng gói mã nguồn** trong các block có chỉ định ngôn ngữ (ví dụ: ```python) để công cụHighlight hiển thị đúng.  
- **Sử dụng liên kết tương đối** khi tài liệu sẽ được chia sẻ trong cùng một kho chứa (repo).  
- **Kiểm tra độ dài dòng**: để đọc dễ, cố gắng giữ mỗi dòng dưới 100 ký tự (không tính mã).  

## 4. Ví dụ minh họa

Dưới đây là một bài học ngắn về **Xây dựng hàm tính giai thừa trong Python** viết bằng Markdown.

```markdown
# Tính giai thừa trong Python

## 1. Mục tiêu học tập
- Hiểu مفهوم giai thừa (n!).  
- Viết hàm tính giai thừa bằng cách lặp và bằng đệ quy.  
- Phân tích độ thời gian và không gian của hai giải pháp.

## 2. Tổng quan
Giai thừa của một số nguyên không âm `n` là tích của tất cả các số nguyên từ 1 đến `n`.  
Đây là một bài toán典型 để giới thiệu conceptos lặp và đệ quy.

## 3. Kiến thức cốt lõi
### 3.1 Công thức
$$ n! = 1 \times 2 \times 3 \times \dots \times n $$
### 3.2 Edge cases
- `0! = 1` (định nghĩa).  
- Đối với `n < 0`, hàm sẽ raise `ValueError`.

## 4. Ví dụ minh họa

### 4.1 Giải pháp lặp
```python
def factorial_iterative(n: int) -> int:
    """Tính n! bằng vòng lặp for."""
    if n < 0:
        raise ValueError("n must be non‑negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

### 4.2 Giải pháp đệ quy
```python
def factorial_recursive(n: int) -> int:
    """Tính n! bằng đệ quy."""
    if n < 0:
        raise ValueError("n must be non‑negative")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)
```

### 4.3 Kiểm thử nhanh
```python
assert factorial_iterative(5) == 120
assert factorial_recursive(5) == 120
```

## 5. Tổng kết
- Giai thừa có thể tính bằng lặp (O(n) thời gian, O(1) bộ nhớ) hoặc đệ quy (O(n) thời gian, O(n) bộ nhớ vì call stack).  
- Trong Python, đệ quy có giới hạn depth (~1000), vì vậy với n lớn nên dùng phiên bản lặp.  
- Luôn kiểm tra đầu vào để tránh lỗi logic.
```
**Kết quả hiển thị (trong một trình preview Markdown):**  

![Preview của ví dụ](https://via.placeholder.com/600x400?text=Markdown+Preview+Example)  

*(Trong tài liệu thực tế, bạn thay đường link hình ảnh bằng ảnh minh họa thực tế hoặc bỏ phần này nếu không cần.)*

## 5. Tổng kết

- Một bài học kỹ thuật tốt trong Markdown cần có **cấu trúc rõ ràng** (mục tiêu → tổng quan → kiến thức → ví dụ → tổng kết).  
- Sử dụng **các thành phần Markdown** tiêu đề, danh sách, mã, bảng, liên kết và hình ảnh để tăng tính可读性 và互動性.  
- Giữ **nhất quán phong cách** và **tránh markup không cần thiết** để tài liệu dễ bảo trì và chuyển đổi sang các định dạng khác.  
- Luôn **kiểm tra mã nguồn** trong các block có chỉ định ngôn ngữ để đảm bảo chúng được highlight đúng và có thể chạy được khi sao chép.  

Bằng cách áp dụng những quy tắc trên, bạn sẽ có thể tạo ra các bài học kỹ thuật chuyên nghiệp, dễ đọc và hữu ích cho cộng đồng học tập.