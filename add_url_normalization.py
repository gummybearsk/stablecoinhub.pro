#!/usr/bin/env python3
"""
Add URL normalization script to all HTML files to handle query parameters and redirects properly
"""

import os
import re
from pathlib import Path

def add_url_normalization(file_path):
    """Add URL normalization script to HTML file if not already present"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if normalization script already exists
    if 'Clean URL and remove query parameters' in content:
        return False

    # Check if file already has canonical tag
    has_canonical = 'rel="canonical"' in content

    # Determine the canonical URL based on file path
    if file_path.name == 'index.html':
        if 'blog' in str(file_path):
            if file_path.parent.name != 'blog':
                # This is a blog post
                canonical_url = f"https://www.stablecoinhub.pro/blog/{file_path.parent.name}/"
            else:
                # This is the blog index
                canonical_url = "https://www.stablecoinhub.pro/blog/"
        elif file_path.parent.name in ['about', 'submit']:
            canonical_url = f"https://www.stablecoinhub.pro/{file_path.parent.name}/"
        else:
            canonical_url = "https://www.stablecoinhub.pro/"
    else:
        # For non-index files like privacy.html, terms.html
        canonical_url = f"https://www.stablecoinhub.pro/{file_path.name}"

    # Script to add
    normalization_script = f'''    <link rel="canonical" href="{canonical_url}">
    <script>
        // Clean URL and remove query parameters while preserving tracking
        (function() {{
            // Check if URL has query parameters
            if (window.location.search) {{
                // Extract any tracking parameters we want to preserve
                const urlParams = new URLSearchParams(window.location.search);
                const ref = urlParams.get('ref');
                const utm_source = urlParams.get('utm_source');
                const utm_campaign = urlParams.get('utm_campaign');

                // Store tracking info in sessionStorage
                if (ref) sessionStorage.setItem('ref_source', ref);
                if (utm_source) sessionStorage.setItem('utm_source', utm_source);
                if (utm_campaign) sessionStorage.setItem('utm_campaign', utm_campaign);

                // Clean URL without reload - just update the address bar
                const cleanUrl = window.location.protocol + '//' + window.location.host + window.location.pathname;
                window.history.replaceState({{}}, document.title, cleanUrl);
            }}

            // Ensure we're on www subdomain
            if (window.location.hostname === 'stablecoinhub.pro') {{
                window.location.href = 'https://www.stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
            }}
        }})();
    </script>'''

    # Find where to insert the script (after <title> tag)
    title_pattern = r'(</title>)'

    if re.search(title_pattern, content):
        # If canonical already exists, just add the script
        if has_canonical:
            script_only = normalization_script.split('</script>')[0].split('<script>')[1] + '</script>'
            script_tag = '\n    <script>' + script_only
            content = re.sub(title_pattern, r'\1' + script_tag, content)
        else:
            # Add both canonical and script
            content = re.sub(title_pattern, r'\1\n' + normalization_script, content)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    return False

def main():
    """Main function to add URL normalization to key pages"""
    print("🔧 Adding URL normalization to handle query parameters...")

    updated_count = 0

    # Key pages to update
    key_pages = [
        Path("index.html"),
        Path("about/index.html"),
        Path("submit/index.html"),
        Path("blog/index.html"),
        Path("privacy.html"),
        Path("terms.html"),
        Path("disclaimer.html")
    ]

    for page_path in key_pages:
        if page_path.exists():
            if add_url_normalization(page_path):
                updated_count += 1
                print(f"✅ Updated: {page_path}")
            else:
                print(f"⏭️  Already has normalization: {page_path}")
        else:
            print(f"❌ Not found: {page_path}")

    print(f"\n📊 Summary:")
    print(f"   Files updated: {updated_count}")
    print("\n✨ URL normalization added successfully!")
    print("URLs with query parameters (like ?ref=producthunt) will now be handled properly.")

if __name__ == "__main__":
    main()