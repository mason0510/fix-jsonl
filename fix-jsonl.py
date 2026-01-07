#!/usr/bin/env python3
"""
Claude Code JSONL Repair Tool v2.0

Features:
  1. Remove thinking / redacted_thinking content
  2. Auto-fix corrupted JSON format
  3. Fix truncated JSON lines
  4. Remove empty and invalid lines

Usage:
  fix-jsonl <keyword>       # Fuzzy match project directory
  fix-jsonl <full-path>     # Specify directory or file
  fix-jsonl --all           # Fix all projects
  fix-jsonl                 # Show help

Examples:
  fix-jsonl wechat
  fix-jsonl custom-skills
  fix-jsonl --all
"""

import json
import os
import sys
import glob
import re

# Default Claude Code projects directory
PROJECTS_DIR = os.path.expanduser("~/.claude/projects")


def try_fix_json(line):
    """Try to fix corrupted JSON"""
    line = line.strip()
    if not line:
        return None, "empty"

    # 1. Direct parse
    try:
        return json.loads(line), None
    except json.JSONDecodeError:
        pass

    # 2. Try common fixes
    fixes = [
        # Truncated JSON - try to close
        (lambda s: s + '"}' if s.count('"') % 2 == 1 else s),
        (lambda s: s + '}' if s.count('{') > s.count('}') else s),
        (lambda s: s + ']}' if s.count('[') > s.count(']') else s),
        (lambda s: s + ']"}' if s.count('[') > s.count(']') and s.count('"') % 2 == 1 else s),
        # Trailing comma
        (lambda s: re.sub(r',\s*}', '}', s)),
        (lambda s: re.sub(r',\s*]', ']', s)),
        # Control characters
        (lambda s: re.sub(r'[\x00-\x1f]', '', s)),
    ]

    test_line = line
    for fix in fixes:
        test_line = fix(test_line)
        try:
            return json.loads(test_line), "fixed"
        except json.JSONDecodeError:
            continue

    # 3. Try to extract valid JSON portion
    match = re.search(r'^(\{.*\})', line)
    if match:
        try:
            return json.loads(match.group(1)), "truncated"
        except json.JSONDecodeError:
            pass

    return None, "unfixable"


def remove_thinking(data):
    """Remove thinking content"""
    modified = False

    # Remove top-level thinking
    if 'thinking' in data:
        del data['thinking']
        modified = True

    # Remove thinking from message.content
    if 'message' in data and isinstance(data['message'], dict):
        content = data['message'].get('content')
        if isinstance(content, list):
            original_len = len(content)
            data['message']['content'] = [
                c for c in content
                if not (isinstance(c, dict) and c.get('type') in ('thinking', 'redacted_thinking'))
            ]
            if len(data['message']['content']) != original_len:
                modified = True

    return modified


def fix_jsonl_file(filepath, verbose=True):
    """Fix a single JSONL file"""
    if not os.path.exists(filepath):
        return 0, 0, "not found"

    original_size = os.path.getsize(filepath)
    if original_size == 0:
        return 0, 0, "empty file"

    new_lines = []
    fixed_lines = 0
    removed_lines = 0
    thinking_removed = 0

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            data, fix_status = try_fix_json(line)

            if data is None:
                removed_lines += 1
                continue

            if fix_status:
                fixed_lines += 1

            if remove_thinking(data):
                thinking_removed += 1

            new_lines.append(json.dumps(data, ensure_ascii=False) + '\n')

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    new_size = os.path.getsize(filepath)
    saved = original_size - new_size

    status_parts = []
    if thinking_removed:
        status_parts.append(f"thinking:{thinking_removed}")
    if fixed_lines:
        status_parts.append(f"fixed:{fixed_lines}")
    if removed_lines:
        status_parts.append(f"removed:{removed_lines}")

    return saved, len(status_parts) > 0, ", ".join(status_parts) if status_parts else "no change"


def find_project_dirs(keyword):
    """Find project directories by keyword"""
    if keyword == "--all":
        return [os.path.join(PROJECTS_DIR, d) for d in os.listdir(PROJECTS_DIR)
                if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    pattern = os.path.join(PROJECTS_DIR, f"*{keyword}*")
    return glob.glob(pattern)


def fix_project(keyword):
    """Fix project"""
    # Full path
    if keyword.startswith('/') or keyword.startswith('~'):
        keyword = os.path.expanduser(keyword)
        if os.path.isfile(keyword):
            saved, changed, status = fix_jsonl_file(keyword)
            icon = "✓" if changed else "·"
            print(f"{icon} {os.path.basename(keyword)}: {status} ({saved/1024:.1f}KB)")
            return
        dirs = [keyword] if os.path.isdir(keyword) else []
    else:
        dirs = find_project_dirs(keyword)

    if not dirs:
        print(f"Not found: {keyword}")
        return

    total_saved = 0
    total_fixed = 0

    for dir_path in sorted(dirs):
        if not os.path.isdir(dir_path):
            continue

        files = glob.glob(os.path.join(dir_path, "*.jsonl"))
        if not files:
            continue

        dir_saved = 0
        dir_fixed = 0
        dir_name = os.path.basename(dir_path)

        # Truncate long directory names
        if len(dir_name) > 60:
            dir_name = "..." + dir_name[-57:]

        file_results = []
        for filepath in files:
            saved, changed, status = fix_jsonl_file(filepath)
            if changed:
                dir_saved += saved
                dir_fixed += 1
                file_results.append(f"  ✓ {os.path.basename(filepath)}: {status} ({saved/1024:.1f}KB)")

        if dir_fixed > 0:
            print(f"\n📁 {dir_name}")
            for r in file_results:
                print(r)
            total_saved += dir_saved
            total_fixed += dir_fixed

    if total_fixed > 0:
        print(f"\n{'='*50}")
        print(f"Fixed: {total_fixed} files | Saved: {total_saved/1024/1024:.2f} MB")
    else:
        print("Nothing to fix")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Recent projects:")
        try:
            dirs = sorted(os.listdir(PROJECTS_DIR),
                         key=lambda d: os.path.getmtime(os.path.join(PROJECTS_DIR, d)),
                         reverse=True)[:10]
            for d in dirs:
                short = d if len(d) <= 50 else "..." + d[-47:]
                print(f"  {short}")
        except:
            pass
        return

    fix_project(sys.argv[1])


if __name__ == "__main__":
    main()
