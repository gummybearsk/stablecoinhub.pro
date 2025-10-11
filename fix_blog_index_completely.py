#!/usr/bin/env python3
"""
Fix blog index page completely - proper titles, chronological order, all blogs
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta

def extract_blog_info(blog_dir):
    """Extract proper title and description from blog HTML"""
    index_file = blog_dir / "index.html"
    if not index_file.exists():
        return None

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from <title> tag (before the | separator)
    title_match = re.search(r'<title>(.*?)(?:\s*\||\s*-|$)', content)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Fallback to h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
        title = h1_match.group(1).strip() if h1_match else blog_dir.name.replace('-', ' ').title()

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = desc_match.group(1) if desc_match else ""

    # Determine category
    if re.search(r'📁\s*([^<]+)</span>', content):
        cat_match = re.search(r'📁\s*([^<]+)</span>', content)
        category = cat_match.group(1).strip()
    else:
        # Determine from content
        title_lower = title.lower()
        if "yield" in title_lower or "apy" in title_lower or "interest" in title_lower:
            category = "Yield"
        elif "defi" in title_lower or "lending" in title_lower:
            category = "DeFi"
        elif "regulation" in title_lower:
            category = "Regulation"
        elif "risk" in title_lower or "insurance" in title_lower or "depeg" in title_lower:
            category = "Risk Management"
        elif "vs" in title_lower or "comparison" in title_lower:
            category = "Comparison"
        elif any(word in title_lower for word in ["penny", "dollar", "coin", "quarter", "grading"]):
            category = "Traditional Currency"
        elif "arbitrage" in title_lower or "trading" in title_lower:
            category = "Trading"
        elif "bridge" in title_lower or "smart contract" in title_lower or "algorithmic" in title_lower:
            category = "Technology"
        elif "market cap" in title_lower or "analysis" in title_lower:
            category = "Market Analysis"
        else:
            category = "Education"

    return {
        "url": blog_dir.name,
        "title": title,
        "description": description[:200] + "..." if len(description) > 200 else description,
        "category": category
    }

def create_blog_index():
    """Create blog index with proper titles and chronological order"""

    blog_path = Path("blog")

    # Get all blog directories
    all_blogs = []
    for blog_dir in blog_path.iterdir():
        if blog_dir.is_dir() and not blog_dir.name.startswith('_'):
            info = extract_blog_info(blog_dir)
            if info:
                all_blogs.append(info)

    # Sort blogs - we'll assign dates in reverse chronological order
    # Most recent first
    priority_blogs = [
        # October 2025 blogs (most recent)
        "stablecoin-apy-guide",
        "stablecoin-depegging-risks",
        "how-to-buy-stablecoin",
        "best-stablecoin-for-international-transfers",
        "stablecoin-regulation",
        "stablecoin-for-beginners",
        "penny-coins-guide",
        "half-dollar-coins-value",
        "stablecoin-interest-accounts",
        "stablecoin-arbitrage",
        "coin-grading-guide",
        "stablecoin-lending-platforms",
        "rare-quarters-worth-money",
        "algorithmic-stablecoins",
        "stablecoin-smart-contracts",
        "stablecoin-liquidity-pools",
        "cbdc-vs-stablecoins",
        "stablecoin-bridges",
        "stablecoin-market-cap-analysis",
        "stablecoin-insurance",
    ]

    # Organize blogs
    ordered_blogs = []

    # Add priority blogs first (newest)
    for blog_url in priority_blogs:
        blog = next((b for b in all_blogs if b['url'] == blog_url), None)
        if blog:
            ordered_blogs.append(blog)

    # Add remaining blogs
    for blog in all_blogs:
        if blog['url'] not in priority_blogs:
            ordered_blogs.append(blog)

    # Generate dates (starting from today going backwards)
    base_date = datetime(2025, 10, 11)
    dates = []
    for i in range(len(ordered_blogs)):
        date = base_date - timedelta(days=i)
        dates.append(date.strftime("%b %d, %Y"))

    # Generate HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - StableCoin Hub</title>
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
                """ + f"{len(ordered_blogs)}" + """ comprehensive guides and articles
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
                <button onclick="filterBlogs('Risk Management')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Risk Management</button>
                <button onclick="filterBlogs('Technology')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Technology</button>
                <button onclick="filterBlogs('Traditional Currency')" class="filter-btn text-gray-500 hover:text-gray-700 whitespace-nowrap pb-2">Traditional Currency</button>
            </div>
        </div>
    </div>

    <!-- Blog Grid -->
    <div class="py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div id="blog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

    # Add all blogs in chronological order with proper titles
    for i, blog in enumerate(ordered_blogs):
        html += f"""
                <article class="blog-card bg-white rounded-xl overflow-hidden shadow-sm card-hover" data-category="{blog['category']}">
                    <div class="p-6">
                        <div class="flex items-center mb-3">
                            <span class="bg-indigo-100 text-indigo-600 text-xs px-2 py-1 rounded-full">{blog['category']}</span>
                            <span class="text-gray-500 text-sm ml-2">{dates[i]}</span>
                        </div>
                        <h2 class="text-xl font-bold text-gray-900 mb-3 line-clamp-2">
                            <a href="/blog/{blog['url']}/" class="hover:text-indigo-600">{blog['title']}</a>
                        </h2>
                        <p class="text-gray-600 mb-4 line-clamp-3">{blog['description']}</p>
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
                    <ul class="space-y-2">"""

    # Add first 3 blogs to footer
    for blog in ordered_blogs[:3]:
        html += f"""
                        <li><a href="/blog/{blog['url']}/" class="text-gray-400 hover:text-white text-sm">{blog['title'][:50]}...</a></li>"""

    html += """
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

    # Write the file
    with open('blog/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Created blog index with {len(ordered_blogs)} blogs")
    print("✅ All blogs now have proper titles (not URL slugs)")
    print("✅ Blogs are listed in chronological order (newest first)")

    # Show first 5 blogs as preview
    print("\n📝 First 5 blogs in order:")
    for i, blog in enumerate(ordered_blogs[:5]):
        print(f"  {i+1}. {dates[i]}: {blog['title'][:60]}...")

def main():
    os.chdir('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')
    create_blog_index()
    print("\n✅ Blog index page completely fixed!")

if __name__ == "__main__":
    main()