#!/usr/bin/env python3
"""
Automatic SEO Monitor and Fixer
Continuously ensures all HTML pages have proper canonical tags and redirect scripts.
Can be run as a pre-commit hook or scheduled task.
"""

import os
import re
from pathlib import Path
from datetime import datetime

class SEOMonitor:
    def __init__(self):
        self.repo_dir = '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo'
        self.domain = 'stablecoinhub.pro'
        self.issues_found = []
        self.fixes_applied = []

    def get_canonical_url(self, file_path):
        """Determine the correct canonical URL for a file"""
        rel_path = os.path.relpath(file_path, self.repo_dir)

        if rel_path == 'index.html':
            return f'https://{self.domain}/'
        elif rel_path.endswith('/index.html'):
            dir_path = rel_path.replace('/index.html', '')
            return f'https://{self.domain}/{dir_path}/'
        elif rel_path.endswith('.html'):
            # For non-index HTML files (like privacy.html, terms.html)
            return f'https://{self.domain}/{rel_path}'
        else:
            return None

    def get_redirect_script(self):
        """Get the standard redirect and query parameter removal script"""
        return '''<script>
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
</script>'''

    def check_canonical_tag(self, content, file_path):
        """Check if canonical tag exists and is correct"""
        canonical_url = self.get_canonical_url(file_path)
        if not canonical_url:
            return True  # Skip non-HTML files

        # Check for any canonical tag
        canonical_pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']'
        match = re.search(canonical_pattern, content, re.IGNORECASE)

        if not match:
            return False, "missing", canonical_url

        existing_url = match.group(1)

        # Check if URL is correct (should not have www and should be https)
        if 'www.' in existing_url or existing_url.startswith('http://'):
            return False, "incorrect", canonical_url

        if existing_url != canonical_url:
            return False, "incorrect", canonical_url

        return True, None, None

    def check_redirect_script(self, content):
        """Check if redirect script exists"""
        if 'window.location.hostname === \'www.stablecoinhub.pro\'' in content or \
           'window.location.hostname === "www.stablecoinhub.pro"' in content:
            return True
        return False

    def fix_html_file(self, file_path):
        """Fix any SEO issues in an HTML file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        fixes = []

        # Check and fix canonical tag
        canonical_check = self.check_canonical_tag(content, file_path)
        if canonical_check[0] is not True:
            status, issue_type, correct_url = canonical_check

            if issue_type == "missing":
                # Add canonical tag before </head>
                if '</head>' in content:
                    canonical_tag = f'    <link rel="canonical" href="{correct_url}">\n'
                    content = content.replace('</head>', canonical_tag + '</head>')
                    fixes.append(f"Added canonical tag: {correct_url}")

            elif issue_type == "incorrect":
                # Fix incorrect canonical URL
                canonical_pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']'
                new_canonical = f'<link rel="canonical" href="{correct_url}"'
                content = re.sub(canonical_pattern, new_canonical, content, flags=re.IGNORECASE)
                fixes.append(f"Fixed canonical URL: {correct_url}")

        # Check and add redirect script if missing
        if not self.check_redirect_script(content):
            redirect_script = self.get_redirect_script()
            if '</head>' in content:
                content = content.replace('</head>', redirect_script + '\n</head>')
                fixes.append("Added redirect script")

        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            rel_path = os.path.relpath(file_path, self.repo_dir)
            self.fixes_applied.append({
                'file': rel_path,
                'fixes': fixes
            })
            return True

        return False

    def scan_all_files(self, fix=True):
        """Scan all HTML files in the repository"""
        total_files = 0
        files_with_issues = 0
        files_fixed = 0

        for root, dirs, files in os.walk(self.repo_dir):
            # Skip .git directory
            if '.git' in root:
                continue

            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    total_files += 1

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for issues
                    has_issues = False
                    rel_path = os.path.relpath(file_path, self.repo_dir)

                    canonical_check = self.check_canonical_tag(content, file_path)
                    if canonical_check[0] is not True:
                        has_issues = True
                        self.issues_found.append(f"{rel_path}: Canonical tag {canonical_check[1]}")

                    if not self.check_redirect_script(content):
                        has_issues = True
                        self.issues_found.append(f"{rel_path}: Redirect script missing")

                    if has_issues:
                        files_with_issues += 1
                        if fix:
                            if self.fix_html_file(file_path):
                                files_fixed += 1

        return total_files, files_with_issues, files_fixed

    def generate_report(self):
        """Generate a report of the scan"""
        print("=" * 60)
        print("🔍 SEO MONITOR REPORT")
        print("=" * 60)
        print(f"📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        if self.issues_found:
            print("⚠️  Issues Found:")
            for issue in self.issues_found[:10]:  # Show first 10 issues
                print(f"   - {issue}")
            if len(self.issues_found) > 10:
                print(f"   ... and {len(self.issues_found) - 10} more")
            print()

        if self.fixes_applied:
            print("✅ Fixes Applied:")
            for fix_info in self.fixes_applied[:10]:  # Show first 10 fixes
                print(f"   📄 {fix_info['file']}:")
                for fix in fix_info['fixes']:
                    print(f"      - {fix}")
            if len(self.fixes_applied) > 10:
                print(f"   ... and {len(self.fixes_applied) - 10} more files fixed")
            print()

        print("=" * 60)

def main():
    import sys

    print("🤖 Automatic SEO Monitor & Fixer")
    print("=" * 60)

    monitor = SEOMonitor()

    # Check if we should just scan or also fix
    fix_mode = True
    if len(sys.argv) > 1 and sys.argv[1] == '--check-only':
        fix_mode = False
        print("📊 Running in CHECK-ONLY mode (no fixes will be applied)")
    else:
        print("🔧 Running in FIX mode (issues will be automatically fixed)")

    print("🔍 Scanning all HTML files...")
    print()

    total, issues, fixed = monitor.scan_all_files(fix=fix_mode)

    monitor.generate_report()

    print(f"📊 Summary:")
    print(f"   Total HTML files scanned: {total}")
    print(f"   Files with issues: {issues}")
    if fix_mode:
        print(f"   Files fixed: {fixed}")
        if fixed > 0:
            print(f"\n✅ All SEO issues have been automatically fixed!")
            print("📝 Remember to commit and push these changes.")
    else:
        if issues > 0:
            print(f"\n⚠️  Found {issues} files with SEO issues.")
            print("Run without --check-only flag to automatically fix them.")

    # Return exit code based on whether issues were found
    sys.exit(0 if issues == 0 else 1)

if __name__ == "__main__":
    main()