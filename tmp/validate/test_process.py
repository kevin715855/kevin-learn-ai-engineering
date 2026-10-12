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

def build_frontmatter(fm):
    lines = ['---']
    for key in sorted(fm.keys()):
        lines.append(f'{key}: {fm[key]}')
    lines.append('---')
    return '\n'.join(lines) + '\n'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm, body = parse_frontmatter(content)

    # Determine module: parent directory name relative to output root? We'll assume we know.
    # For test, we'll set module to "introduction"
    module = "introduction"
    # order: we'll set to 1 for test
    order = 1
    # status
    status = fm.get('source_status', 'completed')
    if status == '':
        status = 'completed'

    # Build new frontmatter
    new_fm = fm.copy()
    changed = False
    if 'id' not in new_fm:
        new_fm['id'] = os.path.splitext(os.path.basename(filepath))[0]
        changed = True
    if 'title' not in new_fm:
        new_fm['title'] = os.path.splitext(os.path.basename(filepath))[0].replace('-', ' ').title()
        changed = True
    if 'module' not in new_fm:
        new_fm['module'] = module
        changed = True
    if 'order' not in new_fm:
        new_fm['order'] = order
        changed = True
    if 'status' not in new_fm:
        new_fm['status'] = status
        changed = True

    if changed:
        new_fm_content = build_frontmatter(new_fm)
        new_content = new_fm_content + body
        return new_content, changed
    else:
        return content, False

if __name__ == '__main__':
    filepath = sys.argv[1]
    new_content, changed = process_file(filepath)
    if changed:
        print("--- NEW CONTENT ---")
        print(new_content)
        print("--- END ---")
    else:
        print("No changes needed.")