import os
import json
import re

OUTPUT_DIR = r"E:\PROJECT\roadmap-ai-engineer\output"
FRONTEND_SRC_DIR = r"E:\PROJECT\roadmap-ai-engineer\frontend\src"

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_raw = parts[1].strip()
    body = parts[2].strip()
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

def main():
    modules = []
    
    # Read output directory entries
    if not os.path.exists(OUTPUT_DIR):
        print("Output dir not found:", OUTPUT_DIR)
        return

    # List subdirectories (modules)
    # We can rely on the order in output/README.md or sorted/discovered order
    # Let's read output/README.md to get module order if possible, or directory scan.
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    module_dirs = []
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r'### \[(.*?)\]\(\.\/(.*?)\/README\.md\)', line)
                if match:
                    m_slug = match.group(2)
                    if os.path.isdir(os.path.join(OUTPUT_DIR, m_slug)):
                        module_dirs.append(m_slug)
                        
    # Add any missing module dirs
    for entry in sorted(os.listdir(OUTPUT_DIR)):
        full_path = os.path.join(OUTPUT_DIR, entry)
        if os.path.isdir(full_path) and entry not in module_dirs:
            module_dirs.append(entry)

    for m_slug in module_dirs:
        m_path = os.path.join(OUTPUT_DIR, m_slug)
        mod_readme = os.path.join(m_path, "README.md")
        mod_title = m_slug.replace("-", " ").title()
        mod_id = m_slug
        
        lessons = []
        # Find all .md files except README.md
        for file_name in sorted(os.listdir(m_path)):
            if file_name == "README.md" or not file_name.endswith(".md"):
                continue
            lesson_path = os.path.join(m_path, file_name)
            with open(lesson_path, "r", encoding="utf-8", errors="ignore") as lf:
                raw_text = lf.read()
            fm, body = parse_frontmatter(raw_text)
            
            l_slug = fm.get("slug", file_name[:-3])
            l_title = fm.get("title", l_slug.replace("-", " ").title())
            l_id = fm.get("id", l_slug)
            
            lessons.append({
                "id": l_id,
                "slug": l_slug,
                "title": l_title,
                "original_title": fm.get("original_title", l_title),
                "content": raw_text, # keep full text or body
                "filename": file_name
            })
            
        modules.append({
            "id": mod_id,
            "slug": m_slug,
            "title": mod_title,
            "lessons": lessons
        })

    data = {
        "total_modules": len(modules),
        "total_lessons": sum(len(m["lessons"]) for m in modules),
        "modules": modules
    }

    os.makedirs(FRONTEND_SRC_DIR, exist_ok=True)
    out_json_path = os.path.join(FRONTEND_SRC_DIR, "roadmap-data.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {out_json_path} with {len(modules)} modules and {data['total_lessons']} lessons.")

if __name__ == "__main__":
    main()
