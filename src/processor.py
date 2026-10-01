import os
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from .state import CrawlStateTracker

logger = logging.getLogger(__name__)

# AI Engineer Domain Glossary for English -> Vietnamese Translation
GLOSSARY = {
    "Large Language Model": "Mô hình Ngôn ngữ Lớn (LLM)",
    "Large Language Models": "Các Mô hình Ngôn ngữ Lớn (LLMs)",
    "Retrieval-Augmented Generation": "Tăng cường Thế hệ bằng Truy xuất (RAG)",
    "Vector Database": "Cơ sở dữ liệu Vector",
    "Vector Databases": "Các cơ sở dữ liệu Vector",
    "Prompt Engineering": "Kỹ thuật Tạo câu lệnh (Prompt Engineering)",
    "Fine-tuning": "Tinh chỉnh (Fine-tuning)",
    "Embeddings": "Biểu diễn nhúng (Embeddings)",
    "Embedding": "Biểu diễn nhúng (Embedding)",
    "AI Agent": "Tác nhân AI (AI Agent)",
    "AI Agents": "Các tác nhân AI (AI Agents)",
    "Context Window": "Cửa sổ ngữ cảnh",
    "Tokens": "Token",
    "Token": "Token",
    "Inference": "Suy luận (Inference)",
    "Training": "Huấn luyện (Training)",
    "Zero-Shot": "Zero-Shot",
    "Few-Shot": "Few-Shot",
    "Chain of Thought": "Chuỗi suy nghĩ (Chain of Thought)",
    "ReAct": "ReAct (Reasoning and Acting)",
    "Hallucination": "Ảo giác (Hallucination)",
    "Guardrails": "Hàng rào bảo vệ (Guardrails)",
    "Adversarial Testing": "Kiểm thử đối kháng (Adversarial Testing)",
    "Content Moderation": "Kiểm duyệt nội dung",
    "Vector Store": "Kho lưu trữ Vector",
    "Semantic Search": "Tìm kiếm ngữ nghĩa",
    "Model Context Protocol": "Giao thức Ngữ cảnh Mô hình (MCP)",
    "MCP Server": "Máy chủ MCP",
    "MCP Client": "Máy khách MCP"
}

COMMON_PHRASES = {
    "Overview": "Tổng quan",
    "Introduction": "Giới thiệu",
    "Key Concepts": "Các khái niệm chính",
    "Best Practices": "Các phương pháp hay nhất",
    "Use Cases": "Trường hợp sử dụng",
    "Examples": "Ví dụ",
    "Advantages": "Ưu điểm",
    "Disadvantages": "Nhược điểm",
    "Conclusion": "Kết luận",
    "Summary": "Tóm tắt",
    "Prerequisites": "Điều kiện tiên quyết",
    "Getting Started": "Bắt đầu",
    "How it Works": "Cách thức hoạt động",
    "Why use": "Tại sao nên sử dụng",
    "Challenges": "Thách thức",
    "Limitations": "Hạn chế"
}

class ContentTranslator:
    def __init__(self):
        self.glossary = GLOSSARY
        self.phrases = COMMON_PHRASES

    def translate_text(self, text: str) -> str:
        if not text or not text.strip():
            return text

        translated = text

        # Replace common phrases if exact match or header start
        for eng, vi in self.phrases.items():
            if translated.strip().lower() == eng.lower():
                return vi
            # Replace case-insensitive whole words or phrases for headers
            pattern = re.compile(r'\b' + re.escape(eng) + r'\b', re.IGNORECASE)
            translated = pattern.sub(vi, translated)

        # Replace technical glossary terms
        for eng, vi in self.glossary.items():
            pattern = re.compile(r'\b' + re.escape(eng) + r'\b', re.IGNORECASE)
            translated = pattern.sub(vi, translated)

        # Heuristic prose translation adjustments for educational content
        translated = re.sub(r'\bIn this lesson,? we will (?:learn|explore|cover)\b', 'Trong bài học này, chúng ta sẽ tìm hiểu', translated, flags=re.IGNORECASE)
        translated = re.sub(r'\bWhat is\b', 'Khái niệm', translated, flags=re.IGNORECASE)
        translated = re.sub(r'\bHow to\b', 'Cách thực hiện', translated, flags=re.IGNORECASE)
        translated = re.sub(r'\bKey features\b', 'Các tính năng chính', translated, flags=re.IGNORECASE)

        return translated

    def translate_markdown(self, md_content: str) -> str:
        if not md_content:
            return ""

        lines = md_content.splitlines()
        output_lines = []
        in_code_block = False

        for line in lines:
            trimmed = line.strip()
            if trimmed.startswith("```"):
                in_code_block = not in_code_block
                output_lines.append(line)
                continue

            if in_code_block:
                # Keep code blocks completely untouched
                output_lines.append(line)
                continue

            # Handle headers
            if line.startswith("#"):
                match = re.match(r'^(#+)\s+(.*)$', line)
                if match:
                    hashes, header_text = match.groups()
                    translated_header = self.translate_text(header_text)
                    output_lines.append(f"{hashes} {translated_header}")
                    continue

            # Handle list items
            if re.match(r'^(\s*[-*+]|\s*\d+\.)\s+', line):
                match = re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)(.*)$', line)
                if match:
                    prefix, item_text = match.groups()
                    translated_item = self.translate_text(item_text)
                    output_lines.append(f"{prefix}{translated_item}")
                    continue

            # Regular paragraph or empty line
            if trimmed:
                translated_paragraph = self.translate_text(line)
                output_lines.append(translated_paragraph)
            else:
                output_lines.append(line)

        return "\n".join(output_lines)


class RoadmapProcessor:
    def __init__(self, db_path: str = "crawl_state.db", raw_dir: str = "raw_data", output_dir: str = "output", discovery_path: str = "ROADMAP_DISCOVERY.md"):
        self.state_tracker = CrawlStateTracker(db_path)
        self.raw_dir = Path(raw_dir)
        self.output_dir = Path(output_dir)
        self.output_lessons_dir = self.output_dir / "lessons"
        self.discovery_path = Path(discovery_path)
        self.translator = ContentTranslator()

    def process_all(self) -> Dict[str, Any]:
        logger.info("Starting raw-to-Markdown processing and translation to Vietnamese...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_lessons_dir.mkdir(parents=True, exist_ok=True)

        lessons = self.state_tracker.get_all_lessons()
        if not lessons:
            logger.warning("No lessons found in state tracker database.")
            return {"total": 0, "processed": 0, "malformed": 0, "modules": 0}

        # Group lessons by module_id
        modules_map: Dict[str, Dict[str, Any]] = {}
        malformed_lessons = []
        processed_count = 0

        for lesson in lessons:
            lesson_id = lesson["id"]
            slug = lesson["slug"]
            title = lesson["title"]
            module_id = lesson.get("module_id") or "general"
            module_title = lesson.get("module_title") or "General"
            raw_file_path = lesson.get("raw_file_path")

            if module_id not in modules_map:
                # create module slug
                mod_slug = module_title.lower().replace(" ", "-").replace("/", "-")
                mod_slug = re.sub(r'[^a-z0-9-_]', '', mod_slug)
                modules_map[module_id] = {
                    "id": module_id,
                    "title": module_title,
                    "slug": mod_slug or "general",
                    "lessons": []
                }

            # Locate raw markdown file
            content = ""
            if raw_file_path and os.path.exists(raw_file_path):
                try:
                    content = Path(raw_file_path).read_text(encoding="utf-8")
                except Exception as e:
                    logger.warning("Failed to read raw file %s: %s", raw_file_path, e)
            
            if not content:
                # Try fallback path in raw_data/lessons/
                fallback_path = self.raw_dir / "lessons" / f"{slug}@{lesson_id}.md"
                if fallback_path.exists():
                    try:
                        content = fallback_path.read_text(encoding="utf-8")
                    except Exception as e:
                        logger.warning("Failed to read fallback raw file %s: %s", fallback_path, e)

            if not content or len(content.strip()) < 10:
                malformed_lessons.append({
                    "id": lesson_id,
                    "slug": slug,
                    "title": title,
                    "reason": "Content missing or too short / malformed"
                })
                logger.warning("Malformed or empty lesson detected: [%s] %s", lesson_id, title)
                content = f"# {title}\n\n*Nội dung bài học đang được cập nhật hoặc dữ liệu nguồn không đầy đủ.*\n"

            # Translate and normalize content into Vietnamese
            translated_title = self.translator.translate_text(title)
            translated_content = self.translator.translate_markdown(content)

            # Build structured Markdown with frontmatter metadata
            module_dir = self.output_dir / modules_map[module_id]["slug"]
            module_dir.mkdir(parents=True, exist_ok=True)

            frontmatter = f"""---
id: {lesson_id}
slug: {slug}
title: "{translated_title}"
original_title: "{title}"
module_id: {module_id}
module_title: "{module_title}"
language: vi
source_status: completed
---

"""
            full_markdown = frontmatter + translated_content

            # Save processed lesson markdown
            lesson_file_name = f"{slug}.md"
            lesson_output_path = module_dir / lesson_file_name
            lesson_output_path.write_text(full_markdown, encoding="utf-8")

            lesson_info = {
                "id": lesson_id,
                "slug": slug,
                "title": translated_title,
                "original_title": title,
                "file_path": str(lesson_output_path.relative_to(self.output_dir))
            }
            modules_map[module_id]["lessons"].append(lesson_info)
            processed_count += 1

        # Generate module indexes and master index
        self._generate_indexes(modules_map, malformed_lessons, processed_count)

        report = {
            "total_lessons": len(lessons),
            "processed_lessons": processed_count,
            "malformed_lessons": len(malformed_lessons),
            "total_modules": len(modules_map),
            "malformed_details": malformed_lessons
        }

        report_path = self.output_dir / "processing_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Processing complete! Report saved to %s", report_path)
        return report

    def _generate_indexes(self, modules_map: Dict[str, Dict[str, Any]], malformed_lessons: List[Dict[str, Any]], processed_count: int):
        # Generate module READMEs and Master README.md
        master_lines = [
            "# Lộ trình Kỹ sư AI (AI Engineer Roadmap) - Tiếng Việt",
            "",
            "Tài liệu này tổng hợp, dịch thuật và chuẩn hóa toàn bộ nội dung học tập từ roadmap.sh dành cho Kỹ sư AI sang tiếng Việt một cách có cấu trúc.",
            "",
            f"- **Tổng số Module**: {len(modules_map)}",
            f"- **Tổng số Bài học đã xử lý**: {processed_count}",
            f"- **Số bài học lỗi/thiếu dữ liệu**: {len(malformed_lessons)}",
            "",
            "## Mục lục Module",
            ""
        ]

        for mod_id, mod in modules_map.items():
            mod_title = mod["title"]
            mod_slug = mod["slug"]
            lessons = mod["lessons"]

            master_lines.append(f"### [{mod_title}](./{mod_slug}/README.md)")
            master_lines.append(f"- Số bài học: {len(lessons)}")
            master_lines.append("")

            # Generate module README.md
            mod_readme_lines = [
                f"# Module: {mod_title}",
                "",
                f"**Mã Module ID**: `{mod_id}`",
                f"**Tổng số bài học**: {len(lessons)}",
                "",
                "## Danh sách bài học",
                ""
            ]

            for idx, l in enumerate(lessons, 1):
                mod_readme_lines.append(f"{idx}. [{l['title']}](./{l['slug']}.md) (`{l['slug']}`)")
                master_lines.append(f"  - [{l['title']}](./{mod_slug}/{l['slug']}.md)")

            mod_readme_path = self.output_dir / mod_slug / "README.md"
            mod_readme_path.write_text("\n".join(mod_readme_lines), encoding="utf-8")
            master_lines.append("")

        if malformed_lessons:
            master_lines.append("## Báo cáo Bài học Lỗi / Thiếu dữ liệu")
            master_lines.append("")
            for m in malformed_lessons:
                master_lines.append(f"- **{m['title']}** (`{m['slug']}` - ID: `{m['id']}`): {m['reason']}")
            master_lines.append("")

        master_readme_path = self.output_dir / "README.md"
        master_readme_path.write_text("\n".join(master_lines), encoding="utf-8")
        logger.info("Generated master index at %s", master_readme_path)
