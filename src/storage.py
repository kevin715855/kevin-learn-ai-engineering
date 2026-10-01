import json
from pathlib import Path
import datetime

class RawStorage:
    def __init__(self, base_dir: str = "raw_data"):
        self.base_dir = Path(base_dir)
        self.lessons_dir = self.base_dir / "lessons"
        self.lessons_dir.mkdir(parents=True, exist_ok=True)

    def save_lesson_raw(self, lesson_id: str, slug: str, content: str, status_code: int, headers: dict, download_url: str) -> str:
        filename = f"{slug}@{lesson_id}.md"
        file_path = self.lessons_dir / filename

        raw_package = {
            "lesson_id": lesson_id,
            "slug": slug,
            "download_url": download_url,
            "status_code": status_code,
            "headers": headers,
            "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "content": content
        }

        # Save as json metadata package or direct markdown with frontmatter/metadata sidecar
        # Saving both raw markdown content and json metadata container ensures zero loss of source information
        file_path.write_text(content, encoding="utf-8")
        
        meta_path = self.lessons_dir / f"{slug}@{lesson_id}.json"
        meta_path.write_text(json.dumps(raw_package, indent=2), encoding="utf-8")

        return str(file_path.resolve())
