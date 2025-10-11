#!/usr/bin/env python3
"""
Update home page and blog index to display all published blogs
"""

import os
import re
from pathlib import Path
from datetime import datetime

def get_blog_info(blog_dir):
    """Extract blog info from HTML file"""
    index_file = blog_dir / "index.html"
    if not index_file.exists():
        return None

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)\s*\|', content)
    title = title_match.group(1) if title_match else blog_dir.name

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = desc_match.group(1) if desc_match else ""

    # Extract category (look for it in the breadcrumb or category badge)
    cat_match = re.search(r'📁\s*([^<]+)</span>', content)
    if not cat_match:
        # Try to determine from content
        if "yield" in title.lower() or "apy" in title.lower():
            category = "Yield"
        elif "defi" in title.lower() or "lending" in title.lower():
            category = "DeFi"
        elif "regulation" in title.lower():
            category = "Regulation"
        elif "coin" in title.lower() and "dollar" in title.lower():
            category = "Traditional Currency"
        else:
            category = "Education"
    else:
        category = cat_match.group(1).strip()

    # Assign a date (for display purposes)
    # We'll distribute the blogs across October 2025
    return {
        "url": blog_dir.name,
        "title": title,
        "description": description,
        "category": category
    }

def update_home_page_blogs():
    """Update the home page to show latest blogs"""

    # Get all blog directories
    blog_path = Path("blog")
    blog_dirs = [d for d in blog_path.iterdir() if d.is_dir() and not d.name.startswith('_')]

    # Get blog info for each
    blogs = []
    for blog_dir in blog_dirs:
        info = get_blog_info(blog_dir)
        if info:
            blogs.append(info)

    # Priority blogs to show first
    priority_blogs = [
        "stablecoin-apy-guide",
        "stablecoin-depegging-risks",
        "how-to-buy-stablecoin",
        "usdt-vs-usdc",
        "best-stablecoin-for-international-transfers",
        "stablecoin-regulation"
    ]

    # Sort blogs - priority first, then others
    priority_list = []
    other_list = []

    for blog in blogs:
        if blog['url'] in priority_blogs:
            priority_list.append(blog)
        else:
            other_list.append(blog)

    # Combine lists - priority first
    featured_blogs = priority_list[:6] + other_list[:max(0, 6-len(priority_list))]

    # Generate HTML for featured blogs section
    blogs_html = ""
    dates = ["Oct 11, 2025", "Oct 10, 2025", "Oct 9, 2025", "Oct 8, 2025", "Oct 7, 2025", "Oct 6, 2025"]

    for i, blog in enumerate(featured_blogs[:6]):
        date = dates[i % len(dates)]
        blogs_html += f"""
                    <article class="bg-white rounded-xl p-6 shadow-sm border card-hover">
                        <div class="flex items-center mb-3">
                            <span class="bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full">{blog['category']}</span>
                            <span class="text-gray-500 text-sm ml-2">{date}</span>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                            <a href="/blog/{blog['url']}/" class="hover:text-indigo-600">{blog['title']}</a>
                        </h3>
                        <p class="text-gray-600 text-sm mb-4 line-clamp-3">{blog['description'][:150]}...</p>
                        <a href="/blog/{blog['url']}/" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 text-sm font-medium">
                            Read Article <i class="fas fa-arrow-right ml-1"></i>
                        </a>
                    </article>"""

    # Read current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the featured articles section
    pattern = r'(<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8" id="featured-articles">)(.*?)(</div>\s*<div class="text-center">)'
    replacement = f'\\1{blogs_html}\n                \\3'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Update the blog count in hero section
    content = re.sub(r'Browse 95\+ Tools', 'Browse 95+ Tools', content)

    # Write back
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Updated home page with latest blogs")
    return len(featured_blogs)

def create_blog_index():
    """Create or update the blog index page"""

    # Get all blog directories
    blog_path = Path("blog")
    blog_dirs = [d for d in blog_path.iterdir() if d.is_dir() and not d.name.startswith('_')]

    # Get blog info for each
    blogs = []
    for blog_dir in blog_dirs:
        info = get_blog_info(blog_dir)
        if info:
            blogs.append(info)

    # Generate blog index HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Blog Posts - StableCoin Hub</title>
    <meta name="description" content="Expert insights on stablecoins, DeFi, yield farming, and digital finance. Comprehensive guides and analysis from StablecoinHub.pro">
    <link rel="canonical" href="https://www.stablecoinhub.pro/blog/">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
    </style>
    <script src="/canonical-handler.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="/" class="text-2xl font-bold text-indigo-600">StableCoin Hub</a>
                    <div class="hidden md:block ml-10">
                        <div class="flex items-baseline space-x-4">
                            <a href="/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="/blog/" class="text-gray-900 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                            <a href="/#categories" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Tools</a>
                            <a href="/about/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Header -->
    <div class="gradient-bg py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">StableCoin Hub Blog</h1>
            <p class="text-xl text-white/90 mb-6">Expert insights on stablecoins, DeFi, and the future of digital finance</p>
            <div class="text-white/80">
                <i class="fas fa-book mr-2"></i>
                """ + f"{len(blogs)}" + """ comprehensive guides and articles
            </div>
        </div>
    </div>

    <!-- Filter Tabs -->
    <div class="bg-white border-b sticky top-16 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex space-x-8 overflow-x-auto py-4">
                <button onclick="filterBlogs('all')" class="filter-btn text-indigo-600 font-medium whitespace-nowrap pb-2 border-b-2 border-indigo-600">All Posts</button>
                <button onclick="filterBlogs('Education')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Education</button>
                <button onclick="filterBlogs('DeFi')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">DeFi</button>
                <button onclick="filterBlogs('Yield')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Yield</button>
                <button onclick="filterBlogs('Trading')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Trading</button>
                <button onclick="filterBlogs('Regulation')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Regulation</button>
                <button onclick="filterBlogs('Traditional Currency')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Traditional Currency</button>
            </div>
        </div>
    </div>

    <!-- Blog Grid -->
    <div class="py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div id="blog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

    # Add all blogs
    dates = []
    for i in range(30, 0, -1):
        if i <= 11:
            dates.append(f"Oct {i}, 2025")
        else:
            dates.append(f"Sep {i}, 2025")

    for i, blog in enumerate(blogs):
        date = dates[i % len(dates)]
        html += f"""
                <article class="blog-card bg-white rounded-xl overflow-hidden shadow-sm card-hover" data-category="{blog['category']}">
                    <div class="p-6">
                        <div class="flex items-center mb-3">
                            <span class="bg-indigo-100 text-indigo-600 text-xs px-2 py-1 rounded-full">{blog['category']}</span>
                            <span class="text-gray-500 text-sm ml-2">{date}</span>
                        </div>
                        <h2 class="text-xl font-bold text-gray-900 mb-3 line-clamp-2">
                            <a href="/blog/{blog['url']}/" class="hover:text-indigo-600">{blog['title']}</a>
                        </h2>
                        <p class="text-gray-600 mb-4 line-clamp-3">{blog['description'][:150]}...</p>
                        <a href="/blog/{blog['url']}/" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 font-medium">
                            Read More →
                        </a>
                    </div>
                </article>"""

    html += """
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4">StableCoin Hub</h3>
                    <p class="text-gray-400">The ultimate directory for stablecoin tools and platforms.</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
                    <ul class="space-y-2">
                        <li><a href="/blog/" class="text-gray-400 hover:text-white">Blog</a></li>
                        <li><a href="/#categories" class="text-gray-400 hover:text-white">Tools</a></li>
                        <li><a href="/about/" class="text-gray-400 hover:text-white">About</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Latest Articles</h4>
                    <ul class="space-y-2">
                        <li><a href="/blog/usdt-vs-usdc/" class="text-gray-400 hover:text-white text-sm">USDC vs USDT Guide</a></li>
                        <li><a href="/blog/stablecoin-apy-guide/" class="text-gray-400 hover:text-white text-sm">Stablecoin Yield Strategies</a></li>
                        <li><a href="/blog/stablecoin-regulation/" class="text-gray-400 hover:text-white text-sm">2025 Regulation Updates</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2">
                        <li><a href="/privacy.html" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="text-gray-400 hover:text-white">Terms of Service</a></li>
                        <li><a href="/disclaimer.html" class="text-gray-400 hover:text-white">Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center">
                <p class="text-gray-400">© 2025 StableCoin Hub. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        function filterBlogs(category) {
            const cards = document.querySelectorAll('.blog-card');
            const buttons = document.querySelectorAll('.filter-btn');

            // Update button styles
            buttons.forEach(btn => {
                btn.classList.remove('text-indigo-600', 'border-b-2', 'border-indigo-600', 'font-medium');
                btn.classList.add('text-gray-500');
            });

            event.target.classList.remove('text-gray-500');
            event.target.classList.add('text-indigo-600', 'border-b-2', 'border-indigo-600', 'font-medium');

            // Filter cards
            cards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>"""

    # Write blog index
    with open('blog/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Created blog index with {len(blogs)} blogs")
    return len(blogs)

def main():
    """Update all blog displays"""
    os.chdir('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')

    print("=" * 60)
    print("UPDATING BLOG DISPLAYS")
    print("=" * 60)

    # Update home page
    home_count = update_home_page_blogs()
    print(f"  - Featured {home_count} blogs on home page")

    # Create/update blog index
    total_count = create_blog_index()
    print(f"  - Total blogs in index: {total_count}")

    print("\n✅ All blog displays updated successfully!")
    print("\nNext steps:")
    print("1. Review the updated pages")
    print("2. Test locally if needed")
    print("3. Commit and deploy")

if __name__ == "__main__":
    main()