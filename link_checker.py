#!/usr/bin/env python3
"""
Link checker for StableCoin Hub website
Checks all HTML files for links and verifies if target files exist
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

def extract_links_from_html(file_path):
    """Extract all href links from an HTML file"""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all href attributes
        href_pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(href_pattern, content)

        for match in matches:
            # Skip external links, anchors, and javascript
            if (not match.startswith('http') and
                not match.startswith('//') and
                not match.startswith('mailto:') and
                not match.startswith('tel:') and
                not match.startswith('#') and
                not match.startswith('javascript:')):
                links.append(match)

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return links

def normalize_path(link, base_dir):
    """Convert a relative link to an absolute path"""
    if link.startswith('/'):
        # Absolute path from root
        path = os.path.join(base_dir, link.lstrip('/'))
    else:
        # Relative path
        path = os.path.join(base_dir, link)

    # Handle trailing slashes and index.html
    if path.endswith('/'):
        path = os.path.join(path, 'index.html')
    elif not path.endswith('.html') and not '.' in os.path.basename(path):
        # If no extension and no dot, assume directory with index.html
        path = os.path.join(path, 'index.html')

    return os.path.normpath(path)

def check_file_exists(file_path):
    """Check if a file exists, handling common variations"""
    if os.path.exists(file_path):
        return True

    # If it's a directory path, check for index.html
    if os.path.isdir(file_path):
        index_path = os.path.join(file_path, 'index.html')
        return os.path.exists(index_path)

    # If it doesn't end in .html, try adding it
    if not file_path.endswith('.html'):
        html_path = file_path + '.html'
        if os.path.exists(html_path):
            return True

        # Try as directory with index.html
        index_path = os.path.join(file_path, 'index.html')
        if os.path.exists(index_path):
            return True

    return False

def main():
    repo_dir = '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo'
    os.chdir(repo_dir)

    broken_links = defaultdict(list)
    all_links = defaultdict(list)

    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files to check\n")

    # Check links in each file
    for html_file in html_files:
        print(f"Checking: {html_file}")
        links = extract_links_from_html(html_file)

        for link in links:
            all_links[html_file].append(link)

            # Convert to absolute path
            target_path = normalize_path(link, repo_dir)

            # Check if target exists
            if not check_file_exists(target_path):
                broken_links[html_file].append({
                    'link': link,
                    'target_path': target_path,
                    'reason': 'File not found'
                })

    # Report results
    print("\n" + "="*80)
    print("LINK CHECK RESULTS")
    print("="*80)

    if broken_links:
        print(f"\nBROKEN LINKS FOUND: {sum(len(links) for links in broken_links.values())}")
        print("-" * 50)

        for file, links in broken_links.items():
            print(f"\nFile: {file}")
            for link_info in links:
                print(f"  ❌ Link: {link_info['link']}")
                print(f"     Expected: {link_info['target_path']}")
                print(f"     Reason: {link_info['reason']}")
    else:
        print("\n✅ No broken internal links found!")

    # Summary statistics
    total_links = sum(len(links) for links in all_links.values())
    total_broken = sum(len(links) for links in broken_links.values())

    print(f"\nSUMMARY:")
    print(f"Total HTML files checked: {len(html_files)}")
    print(f"Total internal links found: {total_links}")
    print(f"Broken links: {total_broken}")
    print(f"Success rate: {((total_links - total_broken) / total_links * 100):.1f}%" if total_links > 0 else "N/A")

if __name__ == "__main__":
    main()