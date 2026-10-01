import json
import urllib.request
import urllib.error
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

ROADMAP_JSON_URL = "https://roadmap.sh/ai-engineer.json"
GITHUB_CONTENTS_URL = "https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/roadmaps/ai-engineer/content"

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

class DiscoveryEngine:
    def __init__(self, output_discovery_path: str = "ROADMAP_DISCOVERY.md"):
        self.output_discovery_path = Path(output_discovery_path)

    def discover(self):
        logger.info("Fetching roadmap structure from %s", ROADMAP_JSON_URL)
        roadmap_data = fetch_json(ROADMAP_JSON_URL)
        nodes = roadmap_data.get("nodes", [])
        edges = roadmap_data.get("edges", [])

        topics = [n for n in nodes if n.get("type") == "topic"]
        subtopics = [n for n in nodes if n.get("type") == "subtopic"]

        logger.info("Fetched %d topics (modules) and %d subtopics (lessons)", len(topics), len(subtopics))

        # Fetch GitHub contents for raw markdown URLs and slugs
        logger.info("Fetching GitHub content directory listing from %s", GITHUB_CONTENTS_URL)
        try:
            gh_files = fetch_json(GITHUB_CONTENTS_URL)
        except Exception as e:
            logger.warning("Failed to fetch GitHub contents list: %s. Falling back to constructed URLs.", e)
            gh_files = []

        # Build map from node_id to github info
        node_to_gh = {}
        for f in gh_files:
            name = f.get("name", "")
            download_url = f.get("download_url")
            if "@" in name and name.endswith(".md"):
                slug_part, rest = name.rsplit("@", 1)
                node_id = rest[:-3] # remove .md
                node_to_gh[node_id] = {
                    "slug": slug_part,
                    "filename": name,
                    "download_url": download_url
                }

        # Build adjacency for modules and lessons using edges
        import math
        parent_map = {}
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            parent_map[target] = source

        # Group lessons by topic
        module_dict = {}
        for t in topics:
            t_id = t.get("id")
            t_label = t.get("data", {}).get("label", "Unnamed Topic")
            module_dict[t_id] = {
                "id": t_id,
                "title": t_label,
                "lessons": []
            }

        lessons_list = []
        for s in subtopics:
            s_id = s.get("id")
            s_label = s.get("data", {}).get("label", "Unnamed Lesson")
            
            # Find parent topic
            curr = s_id
            topic_id = None
            while curr in parent_map:
                parent = parent_map[curr]
                if parent in module_dict:
                    topic_id = parent
                    break
                curr = parent

            if not topic_id:
                sp = s.get("positionAbsolute") or s.get("position") or {"x": 0, "y": 0}
                sx, sy = sp.get("x", 0), sp.get("y", 0)
                min_dist = float("inf")
                for t in topics:
                    tp = t.get("positionAbsolute") or t.get("position") or {"x": 0, "y": 0}
                    tx, ty = tp.get("x", 0), tp.get("y", 0)
                    dist = math.hypot(sx - tx, sy - ty)
                    if dist < min_dist:
                        min_dist = dist
                        topic_id = t["id"]

            gh_info = node_to_gh.get(s_id, {})
            slug = gh_info.get("slug", s_label.lower().replace(" ", "-").replace("/", "-"))
            download_url = gh_info.get("download_url") or f"https://raw.githubusercontent.com/nilbuild/developer-roadmap/master/roadmaps/ai-engineer/content/{slug}@{s_id}.md"

            sp_abs = s.get("positionAbsolute") or s.get("position") or {"y": 0}
            y_pos = sp_abs.get("y", 0)

            lesson_obj = {
                "id": s_id,
                "title": s_label,
                "slug": slug,
                "module_id": topic_id,
                "module_title": module_dict.get(topic_id, {}).get("title", "General"),
                "download_url": download_url,
                "y_pos": y_pos
            }
            lessons_list.append(lesson_obj)

            if topic_id in module_dict:
                module_dict[topic_id]["lessons"].append(lesson_obj)

        for mod in module_dict.values():
            mod["lessons"].sort(key=lambda l: l.get("y_pos", 0))

        modules_list = [m for m in module_dict.values() if m["lessons"]]

        discovery_report = {
            "total_modules": len(modules_list),
            "total_lessons": len(lessons_list),
            "modules": modules_list,
            "lessons": lessons_list
        }

        # Generate ROADMAP_DISCOVERY.md
        self.generate_discovery_markdown(discovery_report)

        return discovery_report

    def generate_discovery_markdown(self, report: dict):
        lines = [
            "# Roadmap.sh AI Engineer Course Structure Discovery",
            "",
            f"- **Total Modules (Topics)**: {report['total_modules']}",
            f"- **Total Lessons (Subtopics)**: {report['total_lessons']}",
            "- **Source Roadmap API**: https://roadmap.sh/ai-engineer.json",
            "",
            "## Modules and Lessons Inventory",
            ""
        ]

        for mod_idx, mod in enumerate(report["modules"], 1):
            lines.append(f"### {mod_idx}. {mod['title']}")
            lines.append(f"- **Module ID**: `{mod['id']}`")
            lines.append(f"- **Lessons Count**: {len(mod['lessons'])}")
            lines.append("")
            for lesson_idx, lesson in enumerate(mod["lessons"], 1):
                lines.append(f"  - {lesson_idx}. **{lesson['title']}** (`{lesson['slug']}`)")
                lines.append(f"    - ID: `{lesson['id']}`")
                lines.append(f"    - URL: `{lesson['download_url']}`")
            lines.append("")

        content = "\n".join(lines)
        self.output_discovery_path.write_text(content, encoding="utf-8")
        logger.info("Saved discovery report to %s", self.output_discovery_path)
