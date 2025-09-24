#!/usr/bin/env python3
import os
import re
from pathlib import Path

def update_canonical_urls(file_path):
    """Update canonical URLs to use apex domain (without www)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if canonical tag exists
    if 'rel="canonical"' not in content and "rel='canonical'" not in content:
        print(f"⚠️  No canonical tag in {file_path}")
        return False

    # Pattern to match canonical tags with www
    patterns = [
        (r'<link\s+rel="canonical"\s+href="https://www\.stablecoinhub\.pro([^"]*)"',
         r'<link rel="canonical" href="https://stablecoinhub.pro\1"'),
        (r"<link\s+rel='canonical'\s+href='https://www\.stablecoinhub\.pro([^']*)'",
         r"<link rel='canonical' href='https://stablecoinhub.pro\1'"),
        (r'<link\s+rel="canonical"\s+href="http://stablecoinhub\.pro([^"]*)"',
         r'<link rel="canonical" href="https://stablecoinhub.pro\1"'),
        (r"<link\s+rel='canonical'\s+href='http://stablecoinhub\.pro([^']*)'",
         r"<link rel='canonical' href='https://stablecoinhub.pro\1'"),
        (r'<link\s+rel="canonical"\s+href="http://www\.stablecoinhub\.pro([^"]*)"',
         r'<link rel="canonical" href="https://stablecoinhub.pro\1"'),
        (r"<link\s+rel='canonical'\s+href='http://www\.stablecoinhub\.pro([^']*)'",
         r"<link rel='canonical' href='https://stablecoinhub.pro\1'"),
    ]

    updated = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            updated = True
            print(f"✅ Updated canonical URL in {file_path}")

    # Also update any internal links that use www
    internal_patterns = [
        (r'href="https://www\.stablecoinhub\.pro([^"]*)"', r'href="https://stablecoinhub.pro\1"'),
        (r"href='https://www\.stablecoinhub\.pro([^']*)'", r"href='https://stablecoinhub.pro\1'"),
        (r'href="http://www\.stablecoinhub\.pro([^"]*)"', r'href="https://stablecoinhub.pro\1"'),
        (r"href='http://www\.stablecoinhub\.pro([^']*)'", r"href='https://stablecoinhub.pro\1'"),
        (r'href="http://stablecoinhub\.pro([^"]*)"', r'href="https://stablecoinhub.pro\1"'),
        (r"href='http://stablecoinhub\.pro([^']*)'", r"href='https://stablecoinhub.pro\1'"),
    ]

    for pattern, replacement in internal_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            updated = True

    if updated:
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    # Check if canonical already uses apex domain (correct format)
    if re.search(r'rel="canonical".*href="https://stablecoinhub\.pro', content) or \
       re.search(r"rel='canonical'.*href='https://stablecoinhub\.pro", content):
        print(f"✓ Canonical URL already correct in {file_path}")
        return False

    return False

def add_redirect_script():
    """Add JavaScript redirect from www to non-www for client-side handling"""
    redirect_script = '''<script>
    // Redirect from www to non-www
    if (window.location.hostname === 'www.stablecoinhub.pro') {
        window.location.href = 'https://stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
    }
    // Remove query parameters from canonical URL dynamically
    if (window.location.search) {
        var canonicalTag = document.querySelector('link[rel="canonical"]');
        if (canonicalTag) {
            var cleanUrl = window.location.origin + window.location.pathname;
            if (window.location.pathname.endsWith('/index.html')) {
                cleanUrl = cleanUrl.replace('/index.html', '/');
            }
            canonicalTag.setAttribute('href', cleanUrl);
        }
    }
</script>
'''
    return redirect_script

def process_all_html_files():
    """Process all HTML files in the repository"""
    repo_dir = '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo'
    updated_count = 0
    processed_count = 0
    needs_redirect_script = []

    # Find all HTML files
    for root, dirs, files in os.walk(repo_dir):
        # Skip .git directory
        if '.git' in root:
            continue

        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                processed_count += 1

                if update_canonical_urls(file_path):
                    updated_count += 1

                # Check if we should add redirect script to main pages
                rel_path = os.path.relpath(file_path, repo_dir)
                if rel_path in ['index.html', 'privacy.html', 'terms.html', 'disclaimer.html'] or \
                   rel_path.startswith('blog/') or rel_path.startswith('about/') or rel_path.startswith('submit/'):
                    needs_redirect_script.append(file_path)

    # Add redirect script to main pages
    print("\n🔧 Adding redirect scripts to main pages...")
    redirect_script = add_redirect_script()
    script_added_count = 0

    for file_path in needs_redirect_script:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if redirect script already exists
        if 'Redirect from www to non-www' not in content:
            # Add script before </head>
            if '</head>' in content:
                content = content.replace('</head>', redirect_script + '\n</head>')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                script_added_count += 1
                print(f"✅ Added redirect script to {os.path.relpath(file_path, repo_dir)}")

    print(f"\n📊 Summary:")
    print(f"   Total HTML files processed: {processed_count}")
    print(f"   Files with URLs updated: {updated_count}")
    print(f"   Redirect scripts added: {script_added_count}")

if __name__ == "__main__":
    print("🔧 Fixing canonical URLs and adding redirect scripts...")
    print("=" * 50)
    process_all_html_files()
    print("=" * 50)
    print("✅ Process complete!")
    print("\n📝 Additional steps needed:")
    print("1. Commit and push these changes to GitHub")
    print("2. GitHub Pages will handle HTTP to HTTPS redirect automatically")
    print("3. The apex domain (stablecoinhub.pro) will be the primary URL")
    print("4. JavaScript will redirect www to non-www for better SEO")