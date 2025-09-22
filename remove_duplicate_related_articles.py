#!/usr/bin/env python3
import os
import re

def fix_duplicate_related_articles(file_path):
    """Remove duplicate Related Articles sections from HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Related Articles sections
    pattern = r'<!-- Single Related Articles Section -->.*?(?=<!-- Footer|</body>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    if len(matches) > 1:
        # Keep only the first Related Articles section
        # Remove all others
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]

    # Also check for any other pattern of Related Articles
    # Count how many h2 tags contain "Related Articles"
    h2_pattern = r'<h2[^>]*>Related Articles</h2>'
    h2_matches = list(re.finditer(h2_pattern, content))

    if len(h2_matches) > 1:
        # Find the complete section for each h2 (from h2 to next major section or footer)
        sections_to_remove = []
        for i, match in enumerate(h2_matches[1:], 1):  # Skip the first one
            start = match.start()
            # Find the parent div that contains this h2
            # Look backwards for opening div
            div_start = content.rfind('<div', 0, start)
            # Find the matching closing div
            div_count = 1
            pos = content.find('>', div_start) + 1
            while div_count > 0 and pos < len(content):
                if content[pos:pos+4] == '<div':
                    div_count += 1
                    pos = content.find('>', pos) + 1
                elif content[pos:pos+6] == '</div>':
                    div_count -= 1
                    pos += 6
                else:
                    pos += 1

            if div_count == 0:
                sections_to_remove.append((div_start, pos))

        # Remove sections in reverse order to maintain indices
        for start, end in reversed(sections_to_remove):
            content = content[:start] + content[end:]

    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return len(h2_matches) if h2_matches else 0

def main():
    blog_dir = 'blog'
    fixed_count = 0
    total_count = 0

    for folder in os.listdir(blog_dir):
        folder_path = os.path.join(blog_dir, folder)
        if os.path.isdir(folder_path):
            index_file = os.path.join(folder_path, 'index.html')
            if os.path.exists(index_file):
                total_count += 1
                original_count = fix_duplicate_related_articles(index_file)
                if original_count > 1:
                    fixed_count += 1
                    print(f"Fixed {folder}: had {original_count} Related Articles sections")

    print(f"\nFixed {fixed_count}/{total_count} blog posts with duplicate Related Articles")

if __name__ == "__main__":
    main()