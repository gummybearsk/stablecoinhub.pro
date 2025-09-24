#!/usr/bin/env python3
"""
Update all canonical URLs to use https://www.stablecoinhub.pro format
"""

import os
import re
from pathlib import Path

def update_canonical_url(file_path):
    """Update canonical URL in an HTML file to use www prefix"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find canonical tags without www
    pattern = r'<link rel="canonical" href="https://stablecoinhub\.pro([^"]*)"'
    replacement = r'<link rel="canonical" href="https://www.stablecoinhub.pro\1"'

    # Count matches before replacement
    matches = len(re.findall(pattern, content))

    if matches > 0:
        # Replace canonical URLs
        content = re.sub(pattern, replacement, content)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    return False

def main():
    """Main function to update all canonical URLs"""
    print("🔧 Updating all canonical URLs to use https://www. format...")

    fixed_count = 0
    already_correct = 0
    total_count = 0

    # Find all HTML files
    for html_file in Path('.').rglob('*.html'):
        total_count += 1

        # Check if file has canonical tag
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<link rel="canonical"' in content:
            if 'href="https://www.stablecoinhub.pro' in content:
                already_correct += 1
            elif update_canonical_url(html_file):
                fixed_count += 1
                print(f"✅ Updated: {html_file}")

    print(f"\n📊 Summary:")
    print(f"   Total HTML files scanned: {total_count}")
    print(f"   Files updated: {fixed_count}")
    print(f"   Files already correct: {already_correct}")

    if fixed_count > 0:
        print("\n✨ Canonical URLs updated successfully!")
        print("All pages now use https://www.stablecoinhub.pro format")
    else:
        print("\n✓ All canonical URLs are already using the correct format.")

if __name__ == "__main__":
    main()