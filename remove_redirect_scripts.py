#!/usr/bin/env python3
"""
Remove the problematic redirect scripts that are causing infinite loops
"""

import os
import re
from pathlib import Path

def remove_redirect_script(file_path):
    """Remove the redirect script from an HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find and remove the redirect script
    # This matches the entire script block that contains the redirect
    pattern = r'<script>\s*\(function\(\)\s*\{[^}]*// Redirect from www to non-www[^}]*window\.location\.href = \'https://stablecoinhub\.pro\'[^}]*\}\)\(\);\s*</script>'

    # Also check for a simpler pattern
    pattern2 = r'// Redirect from www to non-www\s*if \(window\.location\.hostname === \'www\.stablecoinhub\.pro\'\) \{\s*window\.location\.href = \'https://stablecoinhub\.pro\' \+ window\.location\.pathname \+ window\.location\.search \+ window\.location\.hash;\s*\}'

    # Count matches before removal
    matches = len(re.findall(pattern, content)) + len(re.findall(pattern2, content))

    if matches > 0:
        # Remove the redirect scripts
        content = re.sub(pattern, '', content)
        content = re.sub(pattern2, '', content)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    return False

def main():
    """Main function to remove redirect scripts from all HTML files"""
    print("🔧 Removing problematic redirect scripts...")

    fixed_count = 0
    total_count = 0

    # Find all HTML files
    for html_file in Path('.').rglob('*.html'):
        total_count += 1
        if remove_redirect_script(html_file):
            fixed_count += 1
            print(f"✅ Fixed: {html_file}")

    print(f"\n📊 Summary:")
    print(f"   Total HTML files scanned: {total_count}")
    print(f"   Files fixed: {fixed_count}")

    if fixed_count > 0:
        print("\n✨ Redirect scripts removed successfully!")
        print("The website should no longer have infinite refresh loops.")
    else:
        print("\n✓ No redirect scripts found to remove.")

if __name__ == "__main__":
    main()