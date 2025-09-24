#!/usr/bin/env python3
import os
import re
from pathlib import Path

def add_canonical_tag(file_path):
    """Add canonical tag to HTML file if not present"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if canonical tag already exists
    if 'rel="canonical"' in content or "rel='canonical'" in content:
        print(f"✓ Canonical tag already exists in {file_path}")
        return False

    # Determine the canonical URL based on the file path
    rel_path = os.path.relpath(file_path, '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')

    # Special handling for index.html files
    if rel_path == 'index.html':
        canonical_url = 'https://stablecoinhub.pro/'
    elif rel_path.endswith('/index.html'):
        # For directory index files, use the directory path
        dir_path = rel_path.replace('/index.html', '')
        canonical_url = f'https://stablecoinhub.pro/{dir_path}/'
    else:
        # For other HTML files
        canonical_url = f'https://stablecoinhub.pro/{rel_path}'

    # Find the </head> tag and insert canonical tag before it
    head_pattern = re.compile(r'(</head>)', re.IGNORECASE)

    if head_pattern.search(content):
        # Create the canonical tag with proper indentation
        canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'

        # Insert the canonical tag before </head>
        new_content = head_pattern.sub(canonical_tag + r'\1', content, count=1)

        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Added canonical tag to {file_path}: {canonical_url}")
        return True
    else:
        print(f"⚠️  No </head> tag found in {file_path}")
        return False

def process_all_html_files():
    """Process all HTML files in the repository"""
    repo_dir = '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo'
    updated_count = 0
    processed_count = 0

    # Find all HTML files
    for root, dirs, files in os.walk(repo_dir):
        # Skip .git directory
        if '.git' in root:
            continue

        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                processed_count += 1

                if add_canonical_tag(file_path):
                    updated_count += 1

    print(f"\n📊 Summary:")
    print(f"   Total HTML files processed: {processed_count}")
    print(f"   Files updated with canonical tags: {updated_count}")
    print(f"   Files already had canonical tags: {processed_count - updated_count}")

if __name__ == "__main__":
    print("🔧 Adding canonical tags to all HTML files...")
    print("=" * 50)
    process_all_html_files()
    print("=" * 50)
    print("✅ Process complete!")