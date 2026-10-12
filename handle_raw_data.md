Mục tiêu: Xác định và xử lý thư mục `raw_data/lessons/` dựa trên nhu cầu của hệ thống

Mô tả công việc:
- Thư mục `raw_data/lessons/` có vẻ chứa dữ liệu bài học thô (file JSON và MD) mà có thể được sử dụng để tạo ra nội dung
- Trong trạng thái hiện tại, thư mục này trống nhưng `git status` показывает многие файлы как удаленные (D),意味着它们曾经存在但现在被删除了
- 需要确定这些文件是否是系统所必需的，以及它们与data/processed/和content/的关系

步骤：
1. 阅读和理解架构师的规格说明 issue（issue #ROAD-69）
2. 调查 raw_data/lessons/ 文件如何被系统使用（如果有的话）
   - 检查脚本是否从这里读取
   - 检查这些文件是否与 data/processed/ 中的 ID 对应
3. 确定这些文件是否应该：
   a) 被恢复（如果它们是必要的）
   b) 保持删除状态（如果它们被 data/processed/ 替代）
   c) 被用于其他目的
4. 如果需要恢复：
   - 从 origin/main:raw_data/lessons/ 恢复文件
   - 验证它们是否与 data/processed/ 文件通过 ID 匹配
5. 更新任何仍然引用 raw_data/lessons/ 的脚本或配置

Files/PR 预期：
- 可能更改 raw_data/lessons/ 目录的状态（恢复或保持删除）
- 可能更改脚本以正确引用数据来源

检查方式：
- 验证 raw_data/lessons/ 文件（如果存在）是否正确且完整
- 确认数据流：从何处读取 lesson content
- 检查 git status 以确保没有意外更改

注意：此工作应在 data/processed/ 被正确恢复之后进行，并且在确定这些文件在系统中的实际作用之后。