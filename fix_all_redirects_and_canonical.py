#!/usr/bin/env python3
"""
Comprehensive script to fix all redirect and canonical URL issues
"""

import os
import re
import json
from pathlib import Path

def fix_vercel_json():
    """Update vercel.json with comprehensive redirect rules"""
    vercel_config = {
        "redirects": [
            # Non-www to www redirects
            {
                "source": "/(.*)",
                "has": [{"type": "host", "value": "stablecoinhub.pro"}],
                "destination": "https://www.stablecoinhub.pro/$1",
                "permanent": True
            },
            # Blog subdomain redirects
            {
                "source": "/(.*)",
                "has": [{"type": "host", "value": "blog.stablecoinhub.pro"}],
                "destination": "https://www.stablecoinhub.pro/blog/$1",
                "permanent": True
            },
            # Handle common index patterns
            {
                "source": "/index.html",
                "destination": "/",
                "permanent": True
            },
            {
                "source": "/:path*/index.html",
                "destination": "/:path*/",
                "permanent": True
            }
        ],
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {
                        "key": "Link",
                        "value": "<https://www.stablecoinhub.pro/$1>; rel=\"canonical\""
                    }
                ]
            }
        ]
    }

    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    print("✅ Updated vercel.json with comprehensive redirect rules")

def fix_netlify_toml():
    """Create comprehensive netlify.toml configuration"""
    netlify_config = """[[redirects]]
  from = "https://stablecoinhub.pro/*"
  to = "https://www.stablecoinhub.pro/:splat"
  status = 301
  force = true

[[redirects]]
  from = "http://stablecoinhub.pro/*"
  to = "https://www.stablecoinhub.pro/:splat"
  status = 301
  force = true

[[redirects]]
  from = "https://blog.stablecoinhub.pro/*"
  to = "https://www.stablecoinhub.pro/blog/:splat"
  status = 301
  force = true

[[redirects]]
  from = "http://blog.stablecoinhub.pro/*"
  to = "https://www.stablecoinhub.pro/blog/:splat"
  status = 301
  force = true

# Handle index.html
[[redirects]]
  from = "/index.html"
  to = "/"
  status = 301
  force = true

[[redirects]]
  from = "/*/index.html"
  to = "/*/"
  status = 301
  force = true

[build]
  publish = "."

[build.processing]
  skip_processing = false

[build.processing.html]
  pretty_urls = true
"""

    with open('netlify.toml', 'w') as f:
        f.write(netlify_config)
    print("✅ Updated netlify.toml with comprehensive redirect rules")

def fix_htaccess():
    """Update .htaccess with comprehensive redirect and parameter handling"""
    htaccess_content = """# Enable Rewrite Engine
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://www.stablecoinhub.pro/$1 [R=301,L]

# Redirect non-www to www
RewriteCond %{HTTP_HOST} ^stablecoinhub\.pro$ [NC]
RewriteRule ^(.*)$ https://www.stablecoinhub.pro/$1 [R=301,L]

# Redirect blog subdomain to main domain blog folder
RewriteCond %{HTTP_HOST} ^blog\.stablecoinhub\.pro$ [NC]
RewriteRule ^(.*)$ https://www.stablecoinhub.pro/blog/$1 [R=301,L]

# Remove index.html
RewriteCond %{THE_REQUEST} ^[A-Z]{3,9}\ /([^/]+/)*index\.html\ HTTP/
RewriteRule ^(([^/]+/)*)index\.html$ https://www.stablecoinhub.pro/$1 [R=301,L]

# Remove query parameters from URLs (but preserve them internally)
RewriteCond %{QUERY_STRING} ^utm_source=.*$ [OR]
RewriteCond %{QUERY_STRING} ^utm_medium=.*$ [OR]
RewriteCond %{QUERY_STRING} ^utm_campaign=.*$ [OR]
RewriteCond %{QUERY_STRING} ^utm_term=.*$ [OR]
RewriteCond %{QUERY_STRING} ^utm_content=.*$ [OR]
RewriteCond %{QUERY_STRING} ^ref=.*$ [OR]
RewriteCond %{QUERY_STRING} ^gclid=.*$ [OR]
RewriteCond %{QUERY_STRING} ^fbclid=.*$
RewriteRule ^(.*)$ /$1? [R=301,L]

# Add trailing slash to directories
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_URI} !(.*)/$
RewriteRule ^(.*)$ /$1/ [L,R=301]
"""

    with open('.htaccess', 'w') as f:
        f.write(htaccess_content)
    print("✅ Updated .htaccess with comprehensive redirect and parameter handling")

def fix_redirects_file():
    """Update _redirects file for Netlify"""
    redirects_content = """# Force www subdomain
https://stablecoinhub.pro/* https://www.stablecoinhub.pro/:splat 301!
http://stablecoinhub.pro/* https://www.stablecoinhub.pro/:splat 301!

# Redirect blog subdomain to main domain blog folder
https://blog.stablecoinhub.pro/* https://www.stablecoinhub.pro/blog/:splat 301!
http://blog.stablecoinhub.pro/* https://www.stablecoinhub.pro/blog/:splat 301!

# Handle common paths
/index.html / 301!
/blog/index.html /blog/ 301!
/*/index.html /*/ 301!

# Common redirects for SEO
/blog https://www.stablecoinhub.pro/blog/ 301!
/about https://www.stablecoinhub.pro/about/ 301!
/submit https://www.stablecoinhub.pro/submit/ 301!
"""

    with open('_redirects', 'w') as f:
        f.write(redirects_content)
    print("✅ Updated _redirects file with comprehensive rules")

def add_canonical_script():
    """Create a JavaScript file for dynamic canonical URL handling"""
    canonical_script = """// Canonical URL and Query Parameter Handler
(function() {
    'use strict';

    // Function to get clean URL without parameters
    function getCleanUrl() {
        var url = window.location.protocol + '//' + 'www.stablecoinhub.pro' + window.location.pathname;

        // Remove index.html from URL
        url = url.replace(/\/index\.html$/, '/');

        // Ensure trailing slash for directories
        if (!url.match(/\.[a-z]{2,4}$/i) && !url.endsWith('/')) {
            url += '/';
        }

        return url;
    }

    // Function to handle query parameters
    function handleQueryParameters() {
        if (window.location.search) {
            // Extract tracking parameters
            var urlParams = new URLSearchParams(window.location.search);
            var trackingParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref', 'gclid', 'fbclid'];

            // Store tracking info in sessionStorage
            trackingParams.forEach(function(param) {
                var value = urlParams.get(param);
                if (value) {
                    sessionStorage.setItem(param, value);

                    // Send to analytics if available
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'page_view', {
                            [param]: value
                        });
                    }
                }
            });

            // Clean URL in address bar
            var cleanUrl = getCleanUrl();
            window.history.replaceState({}, document.title, cleanUrl);
        }
    }

    // Function to update or create canonical tag
    function updateCanonicalTag() {
        var canonicalTag = document.querySelector('link[rel="canonical"]');
        var cleanUrl = getCleanUrl();

        if (canonicalTag) {
            canonicalTag.setAttribute('href', cleanUrl);
        } else {
            canonicalTag = document.createElement('link');
            canonicalTag.rel = 'canonical';
            canonicalTag.href = cleanUrl;
            document.head.appendChild(canonicalTag);
        }
    }

    // Function to ensure www subdomain
    function ensureWwwSubdomain() {
        if (window.location.hostname === 'stablecoinhub.pro') {
            var newUrl = 'https://www.stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
            window.location.replace(newUrl);
            return true; // Redirecting, stop further execution
        }
        return false;
    }

    // Execute functions
    if (!ensureWwwSubdomain()) {
        handleQueryParameters();
        updateCanonicalTag();
    }
})();
"""

    with open('canonical-handler.js', 'w') as f:
        f.write(canonical_script)
    print("✅ Created canonical-handler.js for dynamic URL handling")

def fix_html_files():
    """Update all HTML files with proper canonical tags and scripts"""
    html_files = []

    # Find all HTML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Calculate canonical URL
            rel_path = os.path.relpath(file_path, '.')
            if rel_path.endswith('index.html'):
                canonical_path = os.path.dirname(rel_path)
                if canonical_path == '.':
                    canonical_path = ''
            else:
                canonical_path = rel_path.replace('.html', '/')

            canonical_url = f"https://www.stablecoinhub.pro/{canonical_path}".rstrip('/') + '/'
            if canonical_url == "https://www.stablecoinhub.pro/":
                pass  # Keep as is for homepage

            # Update or add canonical tag
            if '<link rel="canonical"' in content:
                content = re.sub(
                    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
                    f'<link rel="canonical" href="{canonical_url}">',
                    content
                )
            else:
                # Add canonical tag after <title> or charset
                if '</title>' in content:
                    content = content.replace('</title>', f'</title>\n    <link rel="canonical" href="{canonical_url}">')
                elif '<meta charset' in content:
                    content = re.sub(
                        r'(<meta charset[^>]*>)',
                        f'\\1\n    <link rel="canonical" href="{canonical_url}">',
                        content
                    )

            # Add canonical handler script if not present
            if 'canonical-handler.js' not in content and '</head>' in content:
                script_tag = '    <script src="/canonical-handler.js"></script>\n</head>'
                content = content.replace('</head>', script_tag)

            # Update meta og:url tags
            if 'property="og:url"' in content:
                content = re.sub(
                    r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>',
                    f'<meta property="og:url" content="{canonical_url}">',
                    content
                )

            # Update twitter:url tags
            if 'name="twitter:url"' in content:
                content = re.sub(
                    r'<meta\s+name="twitter:url"\s+content="[^"]*"\s*/?>',
                    f'<meta name="twitter:url" content="{canonical_url}">',
                    content
                )

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✓ Fixed {file_path}")

        except Exception as e:
            print(f"  ✗ Error fixing {file_path}: {e}")

    print(f"✅ Updated {len(html_files)} HTML files with proper canonical tags")

def create_sitemap():
    """Create an updated sitemap with proper canonical URLs"""
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://www.stablecoinhub.pro/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://www.stablecoinhub.pro/blog/</loc>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://www.stablecoinhub.pro/about/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://www.stablecoinhub.pro/submit/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""

    # Add blog posts to sitemap
    blog_dir = Path('blog')
    if blog_dir.exists():
        for blog_path in blog_dir.iterdir():
            if blog_path.is_dir() and not blog_path.name.startswith('_'):
                blog_url = f"https://www.stablecoinhub.pro/blog/{blog_path.name}/"
                sitemap_content += f"""    <url>
        <loc>{blog_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""

    sitemap_content += "</urlset>"

    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    print("✅ Created updated sitemap.xml with canonical URLs")

def create_robots_txt():
    """Create robots.txt with proper sitemap reference"""
    robots_content = """User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /*.json$
Disallow: /*?utm_*
Disallow: /*?ref=*
Disallow: /*?gclid=*
Disallow: /*?fbclid=*

Sitemap: https://www.stablecoinhub.pro/sitemap.xml

# Canonical URL preference
Host: www.stablecoinhub.pro
"""

    with open('robots.txt', 'w') as f:
        f.write(robots_content)
    print("✅ Created robots.txt with proper canonical host preference")

def main():
    """Run all fixes"""
    print("🚀 Starting comprehensive redirect and canonical URL fixes...\n")

    # Change to repo directory
    os.chdir('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')

    # Run all fixes
    fix_vercel_json()
    fix_netlify_toml()
    fix_htaccess()
    fix_redirects_file()
    add_canonical_script()
    fix_html_files()
    create_sitemap()
    create_robots_txt()

    print("\n✅ All redirect and canonical URL issues have been fixed!")
    print("\n📝 Next steps:")
    print("1. Review the changes")
    print("2. Test locally if needed")
    print("3. Deploy to production")
    print("4. Verify in Google Search Console after deployment")

if __name__ == "__main__":
    main()