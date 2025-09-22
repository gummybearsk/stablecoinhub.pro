#!/usr/bin/env python3
import os
import re

def fix_blog_links():
    """Fix all incorrect blog links to use relative paths"""

    blog_dir = 'blog'
    files_fixed = 0

    # Patterns to replace
    replacements = [
        # External blog subdomain to relative path
        (r'https://www\.blog\.stablecoinhub\.pro/?', '/blog/'),
        (r'https://blog\.stablecoinhub\.pro/?', '/blog/'),
        # Ensure main site links are consistent
        (r'https://stablecoinhub\.pro', 'https://www.stablecoinhub.pro'),
    ]

    # Process all HTML files in blog directory
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content

                    # Apply all replacements
                    for pattern, replacement in replacements:
                        # Special handling for blog links - don't replace if it's already a proper link to another blog post
                        if 'blog.stablecoinhub.pro' in pattern:
                            # Replace standalone blog site references
                            content = re.sub(pattern + r'(?!")', replacement, content)
                        else:
                            content = re.sub(pattern, replacement, content)

                    # Write back if changed
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_fixed += 1
                        print(f"Fixed: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"\nTotal files fixed: {files_fixed}")

    # Also fix the main index.html
    index_file = 'index.html'
    if os.path.exists(index_file):
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Already fixed blog links, but ensure main site links are consistent
            content = re.sub(r'https://stablecoinhub\.pro', 'https://www.stablecoinhub.pro', content)

            if content != original_content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {index_file}")

        except Exception as e:
            print(f"Error processing {index_file}: {e}")

if __name__ == "__main__":
    fix_blog_links()