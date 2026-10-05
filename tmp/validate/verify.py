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
    root_dir = sys.argv[1] if len(sys.argv) > 1 else 'output'
    required = {'id', 'title', 'module', 'order', 'status'}
    missing_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith('.md') and f != 'README.md':
                filepath = os.path.join(dirpath, f)
                with open(filepath, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                fm, _ = parse_frontmatter(content)
                missing = required - set(fm.keys())
                if missing:
                    missing_files.append((filepath, missing))
    if missing_files:
        print("Files missing required frontmatter fields:")
        for filepath, missing in missing_files:
            print(f"  {filepath}: {missing}")
        sys.exit(1)
    else:
        print("All files have required frontmatter fields: id, title, module, order, status")
        sys.exit(0)

if __name__ == '__main__':
    main()