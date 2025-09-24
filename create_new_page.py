#!/usr/bin/env python3
"""
Automatic HTML page creator with SEO-optimized canonical tags and redirect scripts.
Usage: python3 create_new_page.py <page_path> <title> <description>
Example: python3 create_new_page.py "products/new-tool" "New Tool - StableCoin Hub" "Description of the new tool"
"""

import os
import sys
from pathlib import Path

def create_html_template(page_path, title, description):
    """Generate HTML template with all SEO optimizations"""

    # Clean up the page path
    if page_path.endswith('.html'):
        page_path = page_path[:-5]
    if page_path.endswith('/'):
        page_path = page_path[:-1]

    # Determine canonical URL
    if page_path in ['', 'index', 'home']:
        canonical_url = 'https://stablecoinhub.pro/'
        file_path = 'index.html'
    else:
        # For directory-based pages
        canonical_url = f'https://stablecoinhub.pro/{page_path}/'
        file_path = f'{page_path}/index.html'

    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GX6EB7DSFL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-GX6EB7DSFL');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">

    <!-- Canonical URL for SEO -->
    <link rel="canonical" href="{canonical_url}">

    <!-- Stylesheets -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

    <!-- SEO & Redirect Script -->
    <script>
    // Redirect from www to non-www
    if (window.location.hostname === 'www.stablecoinhub.pro') {{
        window.location.href = 'https://stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
    }}

    // Remove query parameters from canonical URL dynamically
    if (window.location.search) {{
        var canonicalTag = document.querySelector('link[rel="canonical"]');
        if (canonicalTag) {{
            var cleanUrl = window.location.origin + window.location.pathname;
            if (window.location.pathname.endsWith('/index.html')) {{
                cleanUrl = cleanUrl.replace('/index.html', '/');
            }}
            canonicalTag.setAttribute('href', cleanUrl);
        }}
    }}
    </script>

    <!-- Open Graph tags for social sharing -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="StableCoin Hub">
    <meta property="og:type" content="website">

    <!-- Twitter Card tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <a href="/" class="text-xl sm:text-2xl font-bold text-indigo-600">StableCoin Hub</a>
                    </div>
                    <div class="hidden md:block ml-6 lg:ml-10">
                        <div class="flex items-baseline space-x-4">
                            <a href="/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="/blog/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                            <a href="/submit/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Submit Tool</a>
                            <a href="/about/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                        </div>
                    </div>
                </div>
                <div class="md:hidden">
                    <button onclick="toggleMobileMenu()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
        </div>
        <!-- Mobile menu -->
        <div id="mobile-menu" class="md:hidden hidden bg-white border-t">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                <a href="/" class="block px-3 py-2 text-gray-500 hover:text-indigo-600">Home</a>
                <a href="/blog/" class="block px-3 py-2 text-gray-500 hover:text-indigo-600">Blog</a>
                <a href="/submit/" class="block px-3 py-2 text-gray-500 hover:text-indigo-600">Submit Tool</a>
                <a href="/about/" class="block px-3 py-2 text-gray-500 hover:text-indigo-600">About</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="py-12 sm:py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">{title.replace(" - StableCoin Hub", "")}</h1>

            <!-- Add your content here -->
            <div class="bg-white rounded-lg shadow-sm p-6">
                <p class="text-gray-600">Page content goes here...</p>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-8 sm:py-12 mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-lg sm:text-xl font-bold mb-4">StableCoin Hub</h3>
                    <p class="text-gray-400 text-sm">The ultimate directory for stablecoin tools and platforms.</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="/" class="text-gray-400 hover:text-white transition">Home</a></li>
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition">Blog</a></li>
                        <li><a href="/submit/" class="text-gray-400 hover:text-white transition">Submit Tool</a></li>
                        <li><a href="/about/" class="text-gray-400 hover:text-white transition">About</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Resources</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition">Latest Articles</a></li>
                        <li><a href="/#categories" class="text-gray-400 hover:text-white transition">Tool Categories</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="/privacy.html" class="text-gray-400 hover:text-white transition">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="text-gray-400 hover:text-white transition">Terms of Service</a></li>
                        <li><a href="/disclaimer.html" class="text-gray-400 hover:text-white transition">Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center">
                <p class="text-gray-400 text-sm">&copy; 2025 StableCoin Hub. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        function toggleMobileMenu() {{
            document.getElementById('mobile-menu').classList.toggle('hidden');
        }}
    </script>
</body>
</html>'''

    return template, file_path

def create_page(page_path, title, description):
    """Create the HTML page with proper directory structure"""
    repo_dir = '/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo'

    template, file_path = create_html_template(page_path, title, description)

    # Full file path
    full_path = os.path.join(repo_dir, file_path)

    # Create directory if needed
    dir_path = os.path.dirname(full_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"✅ Created directory: {dir_path}")

    # Check if file already exists
    if os.path.exists(full_path):
        response = input(f"⚠️  File {file_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled.")
            return

    # Write the file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"✅ Created page: {file_path}")
    print(f"📍 Canonical URL: {template.split('rel="canonical" href="')[1].split('"')[0]}")
    print(f"✅ SEO optimizations included:")
    print("   - Canonical tag for duplicate content prevention")
    print("   - WWW to non-www redirect")
    print("   - Query parameter stripping")
    print("   - Open Graph tags for social sharing")
    print("   - Google Analytics tracking")

def main():
    if len(sys.argv) < 2:
        print("📝 HTML Page Creator with Automatic SEO Setup")
        print("=" * 50)
        print("\nUsage:")
        print("  python3 create_new_page.py <page_path> [title] [description]")
        print("\nExamples:")
        print('  python3 create_new_page.py "tools"')
        print('  python3 create_new_page.py "tools" "Stablecoin Tools - StableCoin Hub"')
        print('  python3 create_new_page.py "products/defi" "DeFi Products" "Best DeFi products for stablecoins"')
        print("\nNote: page_path should not include .html extension")
        return

    page_path = sys.argv[1]

    # Default title and description if not provided
    if len(sys.argv) > 2:
        title = sys.argv[2]
    else:
        page_name = page_path.split('/')[-1].replace('-', ' ').title()
        title = f"{page_name} - StableCoin Hub"

    if len(sys.argv) > 3:
        description = sys.argv[3]
    else:
        description = f"Explore {title.replace(' - StableCoin Hub', '')} on StableCoin Hub - Your comprehensive stablecoin resource."

    create_page(page_path, title, description)

if __name__ == "__main__":
    main()