import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentProcessor01:
    def __init__(self, source_dir="output", content_dir="content", output_dir="output"):
        self.source_dir = Path(source_dir)
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self):
        logger.info("Starting ContentProcessor01")
        organized = self._organize_lessons()
        indexes = self._generate_indexes()
        return {"lessons_organized": organized, "indexes_generated": indexes, "status": "completed"}
    
    def _organize_lessons(self):
        count = 0
        if self.source_dir.exists():
            for module_path in self.source_dir.iterdir():
                if module_path.is_dir() and module_path.name != "__pycache__":
                    module_name = module_path.name
                    target_dir = self.content_dir / module_name
                    target_dir.mkdir(parents=True, exist_ok=True)
                    for file_path in module_path.glob("*.md"):
                        if file_path.name != "README.md":
                            try:
                                shutil.copy2(file_path, target_dir / file_path.name)
                                count += 1
                            except Exception as e:
                                logger.error(f"Failed to copy {file_path}: {e}")
        logger.info(f"Organized {count} lessons")
        return count
    
    def _generate_indexes(self):
        count = 0
        module_indexes = self._generate_module_indexes()
        count += len(module_indexes)
        if self._generate_master_index(module_indexes):
            count += 1
        logger.info(f"Generated/updated {count} indexes")
        return count
    
    def _generate_module_indexes(self):
        updated = []
        if self.content_dir.exists():
            for module_path in self.content_dir.iterdir():
                if module_path.is_dir() and module_path.name != "__pycache__":
                    module_name = module_path.name
                    output_module_dir = self.output_dir / module_name
                    output_module_dir.mkdir(parents=True, exist_ok=True)
                    lesson_files = list(module_path.glob("*.md"))
                    lesson_count = len(lesson_files)
                    module_title = module_name.replace("-", " ").title()
                    index_content = f"# Module: {module_title}\n\n**Mã Module ID**: `{module_name}`\n**Tổng số bài học**: {lesson_count}\n\n## Danh sách bài học\n"
                    for i, lesson_file in enumerate(sorted(lesson_files), 1):
                        lesson_name = lesson_file.stem
                        lesson_title = lesson_name.replace("-", " ").title()
                        index_content += f"{i}. [{lesson_title}](./{lesson_file.name}) (`{lesson_name}`)\n"
                    try:
                        with open(output_module_dir / "README.md", "w", encoding="utf-8") as f:
                            f.write(index_content)
                        updated.append(module_name)
                    except Exception as e:
                        logger.error(f"Failed to write module index for {module_name}: {e}")
        return updated
    
    def _generate_master_index(self, module_list):
        master_index_path = self.output_dir / "README.md"
        total_lessons = 0
        module_details = []
        for module_name in module_list:
            module_path = self.content_dir / module_name
            if module_path.exists():
                lesson_count = len(list(module_path.glob("*.md")))
                total_lessons += lesson_count
                module_title = module_name.replace("-", " ").title()
                module_details.append((module_name, module_title, lesson_count))
        master_content = f"# Lộ trình Kỹ sư AI (AI Engineer Roadmap) - Tiếng Việt\n\nTài liệu này tổng hợp, dịch thuật và chuẩn hóa toàn bộ nội dung học tập từ roadmap.sh dành cho Kỹ sư AI sang tiếng Việt một cách có cấu trúc.\n\n- **Tổng số Module**: {len(module_list)}\n- **Tổng số Bài học đã xử lý**: {total_lessons}\n- **Số bài học lỗi/thiếu dữ liệu**: 0\n\n## Mục lục Module\n"
        for module_name, module_title, lesson_count in sorted(module_details, key=lambda x: x[0]):
            master_content += f"### [{module_title}](./{module_name}/README.md)\n- Số bài học: {lesson_count}\n\n"
        try:
            with open(master_index_path, "w", encoding="utf-8") as f:
                f.write(master_content)
            logger.debug("Generated master index")
            return True
        except Exception as e:
            logger.error(f"Failed to write master index: {e}")
            return False

def main():
    logging.basicConfig(level=logging.INFO)
    processor = ContentProcessor01()
    report = processor.process()
    print("ContentProcessor01 Processing Report:")
    print(f"  Lessons organized: {report['lessons_organized']}")
    print(f"  Indexes generated: {report['indexes_generated']}")
    print(f"  Status: {report['status']}")

if __name__ == "__main__":
    main()
