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

def process_file(filepath, root_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm, body = parse_frontmatter(content)

    # Determine module: parent directory name relative to root_dir
    rel_path = os.path.relpath(filepath, root_dir)
    print(f"  rel_path: {rel_path!r}")
    parent_dir = os.path.dirname(rel_path)
    print(f"  parent_dir: {parent_dir!r}")
    if parent_dir:
        module = parent_dir
        # Normalize path separators to forward slash? Keep as is for now.
        # But we want module as a string like "introduction"
        # On Windows, parent_dir might be "introduction" (single level) or nested?
        # In our structure, files are directly under module directories, no deeper.
        # So parent_dir should be just the module name.
        # However, if there are subdirectories, we might need to adjust.
        # We'll assume no subdirectories beyond module.
        # Convert backslashes to forward slash for consistency.
        module = module.replace('\\', '/')
        print(f"  module (after replace): {module!r}")
    else:
        module = ''
        print(f"  module empty")

    # Determine order: we need to know all files in the same module directory
    # We'll compute order later in a separate pass.
    # For now, we'll compute order by sorting files in the same directory.
    # We'll do this outside this function.

    # Determine status
    status = fm.get('source_status', 'completed')
    if status == '':
        status = 'completed'
    print(f"  status: {status!r}")

    # Ensure required fields
    changed = False
    if 'id' not in fm:
        fm['id'] = os.path.splitext(os.path.basename(filepath))[0]
        changed = True
        print("  added id")
    if 'title' not in fm:
        fm['title'] = os.path.splitext(os.path.basename(filepath))[0].replace('-', ' ').title()
        changed = True
        print("  added title")
    if 'module' not in fm:
        fm['module'] = module
        changed = True
        print("  added module")
    # order will be added later
    if 'status' not in fm:
        fm['status'] = status
        changed = True
        print("  added status")

    # If any changes, reconstruct content
    if changed:
        new_fm = build_frontmatter(fm)
        new_content = new_fm + body
        return new_content, changed
    else:
        return None, False

if __name__ == '__main__':
    root_dir = sys.argv[1] if len(sys.argv) > 1 else 'output'
    filepath = sys.argv[2]
    print(f"Processing {filepath}")
    new_content, changed = process_file(filepath, root_dir)
    if changed:
        print("Changed!")
        # Write to a temp file to see
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            tmp.write(new_content)
            print(f"Written to: {tmp.name}")
    else:
        print("No change.")