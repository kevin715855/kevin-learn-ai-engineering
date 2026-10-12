import os
import sys

def parse_frontmatter(content):
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    fm_raw = parts[1].strip()
    body = parts[2].strip()
    fm = {}
    for line in fm_raw.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

def main():
    filepath = sys.argv[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm, body = parse_frontmatter(content)
    print(f"File: {filepath}")
    print(f"Frontmatter keys: {list(fm.keys())}")
    print(f"Has id: {'id' in fm}")
    print(f"Has title: {'title' in fm}")
    print(f"Has module: {'module' in fm}")
    print(f"Has order: {'order' in fm}")
    print(f"Has status: {'status' in fm}")
    print(f"Has source_status: {'source_status' in fm}")
    print("---")

if __name__ == '__main__':
    main()