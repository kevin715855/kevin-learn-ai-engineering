import unittest
import tempfile
import pathlib
import os
import shutil

from src.processor import ContentTranslator, RoadmapProcessor
from src.state import CrawlStateTracker

class TestContentTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ContentTranslator()

    def test_translate_text(self):
        text = "Introduction to Large Language Model and Prompt Engineering."
        translated = self.translator.translate_text(text)
        self.assertIn("Mô hình Ngôn ngữ Lớn (LLM)", translated)
        self.assertIn("Kỹ thuật Tạo câu lệnh (Prompt Engineering)", translated)

    def test_translate_markdown(self):
        md = "# Overview\n\nHere is a python code block:\n\n```python\nprint('Large Language Model')\n```\n\n- Key concepts"
        translated = self.translator.translate_markdown(md)
        self.assertIn("# Tổng quan", translated)
        # Code block content should remain untranslated
        self.assertIn("print('Large Language Model')", translated)
        self.assertIn("- Các khái niệm chính", translated)

class TestRoadmapProcessor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.raw_dir = os.path.join(self.temp_dir, "raw_data")
        self.output_dir = os.path.join(self.temp_dir, "output")

        os.makedirs(os.path.join(self.raw_dir, "lessons"), exist_ok=True)
        self.tracker = CrawlStateTracker(self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_process_all(self):
        # Register test lesson
        lesson_id = "test-123"
        slug = "test-lesson"
        title = "Large Language Model"
        module_id = "mod-1"
        module_title = "Hugging Face"

        self.tracker.upsert_lesson(lesson_id, slug, title, module_id, module_title)
        raw_file = pathlib.Path(self.raw_dir) / "lessons" / f"{slug}@{lesson_id}.md"
        raw_file.write_text("# Overview\n\nIntroduction to Large Language Model.", encoding="utf-8")
        self.tracker.set_status(lesson_id, "COMPLETED", raw_file_path=str(raw_file.resolve()))

        processor = RoadmapProcessor(
            db_path=self.db_path,
            raw_dir=self.raw_dir,
            output_dir=self.output_dir,
            discovery_path=os.path.join(self.temp_dir, "disc.md")
        )

        report = processor.process_all()
        self.assertEqual(report["total_lessons"], 1)
        self.assertEqual(report["processed_lessons"], 1)
        self.assertEqual(report["malformed_lessons"], 0)

        # Verify output file exists
        output_lesson_path = pathlib.Path(self.output_dir) / "hugging-face" / f"{slug}.md"
        self.assertTrue(output_lesson_path.exists())
        content = output_lesson_path.read_text(encoding="utf-8")
        self.assertIn("Mô hình Ngôn ngữ Lớn (LLM)", content)

        master_readme = pathlib.Path(self.output_dir) / "README.md"
        self.assertTrue(master_readme.exists())

if __name__ == "__main__":
    unittest.main()
