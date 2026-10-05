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
    # rel_path is like "introduction\ai-vs-agi.md"
    parent_dir = os.path.dirname(rel_path)
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
    else:
        module = ''

    # Determine order: we need to know all files in the same module directory
    # We'll compute order later in a separate pass.
    # For now, we'll compute order by sorting files in the same directory.
    # We'll do this outside this function.

    # Determine status
    status = fm.get('source_status', 'completed')
    if status == '':
        status = 'completed'

    # Ensure required fields
    changed = False
    if 'id' not in fm:
        # Generate id from filename? But we expect it to be present.
        # If missing, we can set to slug or filename.
        fm['id'] = os.path.splitext(os.path.basename(filepath))[0]
        changed = True
    if 'title' not in fm:
        fm['title'] = os.path.splitext(os.path.basename(filepath))[0].replace('-', ' ').title()
        changed = True
    if 'module' not in fm:
        fm['module'] = module
        changed = True
    # order will be added later
    if 'status' not in fm:
        fm['status'] = status
        changed = True

    # If any changes, reconstruct content
    if changed:
        new_fm = build_frontmatter(fm)
        new_content = new_fm + body
        return new_content
    else:
        return None  # no change

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else 'output'
    print(f"Processing markdown files in {root_dir}")

    # First, gather all markdown files per directory to compute order
    file_info = {}  # dirpath -> list of (filename, order)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        md_files = [f for f in filenames if f.lower().endswith('.md') and f != 'README.md']
        if md_files:
            # Sort by filename (case-insensitive)
            sorted_files = sorted(md_files, key=lambda x: x.lower())
            file_info[dirpath] = [(f, i+1) for i, f in enumerate(sorted_files)]

    # Process each file
    for dirpath, files in file_info.items():
        for filename, order in files:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            fm, body = parse_frontmatter(content)

            # Determine module
            rel_path = os.path.relpath(filepath, root_dir)
            parent_dir = os.path.dirname(rel_path)
            if parent_dir:
                module = parent_dir.replace('\\', '/')
            else:
                module = ''

            # Determine status
            status = fm.get('source_status', 'completed')
            if status == '':
                status = 'completed'

            # Build new frontmatter
            new_fm = fm.copy()
            changed = False
            if 'id' not in new_fm:
                new_fm['id'] = os.path.splitext(filename)[0]
                changed = True
            if 'title' not in new_fm:
                new_fm['title'] = os.path.splitext(filename)[0].replace('-', ' ').title()
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
                # Build frontmatter lines
                lines = ['---']
                for key in sorted(new_fm.keys()):
                    lines.append(f'{key}: {new_fm[key]}')
                lines.append('---')
                new_content = '\n'.join(lines) + '\n' + body
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")
            else:
                print(f"No change: {filepath}")

if __name__ == '__main__':
    main()