#!/usr/bin/env python3
"""
Auto-publish scheduled blog posts based on the publishing schedule.
This script runs daily via GitHub Actions and publishes blogs for the current date.
"""

import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
import json

# Import blog schedule from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Dynamic blog schedule - will be updated as needed
BLOG_SCHEDULE = {
    "2025-09-30": [
        {
            "url": "stablecoin-defi-lending",
            "title": "Stablecoin DeFi Lending: Complete Guide to Earning Passive Income",
            "category": "DeFi",
            "description": "Learn how to earn passive income through stablecoin lending in DeFi. Compare top platforms, understand risks, and maximize your yields."
        }
    ],
    "2025-09-30": [
        {
            "url": "stablecoin-defi-lending",
            "title": "Stablecoin DeFi Lending: Complete Guide to Earning Passive Income",
            "category": "DeFi",
            "description": "Learn how to earn passive income through stablecoin lending in DeFi. Compare top platforms, understand risks, and maximize your yields."
        },
        {
            "url": "stablecoin-yield-farming-guide",
            "title": "Stablecoin Yield Farming: Ultimate Guide to Maximizing Returns",
            "category": "DeFi",
            "description": "Master yield farming with stablecoins. Learn strategies, compare platforms, and understand the risks and rewards of DeFi yield farming."
        }
    ],
    "2025-10-01": [
        {
            "url": "best-stablecoin-exchanges-2025",
            "title": "Best Stablecoin Exchanges 2025: Top Platforms for Trading & Earning",
            "category": "Exchanges",
            "description": "Compare the best cryptocurrency exchanges for stablecoin trading in 2025. Find low fees, high liquidity, and earning opportunities."
        }
    ],
    "2025-10-02": [
        {
            "url": "stablecoin-regulation-guide",
            "title": "Stablecoin Regulation Guide: Global Rules and Compliance in 2025",
            "category": "Regulation",
            "description": "Navigate the evolving stablecoin regulatory landscape. Understand global rules, compliance requirements, and what's coming next."
        }
    ]
}

def get_today_blogs():
    """Get blogs scheduled for today"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Checking for blogs scheduled on {today}")
    return BLOG_SCHEDULE.get(today, [])

def check_blog_exists(url):
    """Check if a blog already exists"""
    blog_path = Path(f"blog/{url}/index.html")
    return blog_path.exists()

def create_blog_html(blog_data):
    """Create comprehensive HTML content for a blog post"""
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - StableCoin Hub</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="https://www.stablecoinhub.pro/blog/{url}/">

    <!-- Open Graph Meta Tags -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.stablecoinhub.pro/blog/{url}/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">

    <!-- Twitter Meta Tags -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://www.stablecoinhub.pro/blog/{url}/">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">

    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <!-- Script to handle query parameters -->
    <script>
    (function() {{
        // Handle URL query parameters for proper canonical
        if (window.location.search) {{
            var canonicalTag = document.querySelector('link[rel="canonical"]');
            if (canonicalTag) {{
                // Keep the canonical URL clean without query parameters
                var cleanUrl = 'https://www.stablecoinhub.pro' + window.location.pathname;
                if (cleanUrl.endsWith('/index.html')) {{
                    cleanUrl = cleanUrl.replace('/index.html', '/');
                }}
                canonicalTag.setAttribute('href', cleanUrl);
            }}
        }}
    }})();
    </script>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="text-2xl font-bold text-indigo-600">StableCoin Hub</a>
                <div class="hidden md:flex space-x-6">
                    <a href="/" class="text-gray-700 hover:text-indigo-600 transition">Home</a>
                    <a href="/blog/" class="text-gray-700 hover:text-indigo-600 transition">Blog</a>
                    <a href="/about/" class="text-gray-700 hover:text-indigo-600 transition">About</a>
                    <a href="/submit/" class="text-gray-700 hover:text-indigo-600 transition">Submit Tool</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <article class="max-w-4xl mx-auto px-4 py-12">
        <div class="bg-white rounded-lg shadow-md p-8">
            <!-- Article Header -->
            <div class="mb-8">
                <div class="flex items-center gap-3 mb-4">
                    <span class="bg-indigo-100 text-indigo-600 text-xs px-3 py-1 rounded-full font-medium">{category}</span>
                    <span class="text-gray-500 text-sm">{date}</span>
                </div>
                <h1 class="text-4xl font-bold text-gray-900 mb-4">{title}</h1>
                <p class="text-lg text-gray-700">{description}</p>
            </div>

            <!-- Article Content -->
            <div class="prose prose-lg max-w-none">
                <p class="mb-6">
                    Welcome to our comprehensive guide on {topic}. This article provides expert insights,
                    practical strategies, and the latest developments in the stablecoin ecosystem.
                </p>

                <h2 class="text-2xl font-bold mt-8 mb-4">Key Highlights</h2>
                <ul class="list-disc pl-6 mb-6">
                    <li>In-depth analysis and expert insights</li>
                    <li>Practical implementation strategies</li>
                    <li>Latest market trends and developments</li>
                    <li>Risk management and best practices</li>
                </ul>

                <p class="mb-6">
                    The stablecoin ecosystem continues to evolve rapidly, offering new opportunities and challenges
                    for investors, traders, and developers. Understanding these dynamics is crucial for success.
                </p>

                <div class="bg-blue-50 border-l-4 border-blue-600 p-6 my-8">
                    <p class="font-semibold mb-2">💡 Pro Tip</p>
                    <p>
                        Always conduct thorough research and consider your risk tolerance before making any
                        investment decisions in the stablecoin space.
                    </p>
                </div>

                <p class="mb-6">
                    For more comprehensive stablecoin resources, tools, and analysis, visit
                    <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>.
                </p>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="bg-white border-t mt-12">
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="text-center text-gray-500">
                <p>&copy; 2025 StableCoin Hub. All rights reserved.</p>
                <div class="mt-4 space-x-4">
                    <a href="/" class="hover:text-indigo-600">Home</a>
                    <a href="/blog/" class="hover:text-indigo-600">Blog</a>
                    <a href="/about/" class="hover:text-indigo-600">About</a>
                    <a href="/submit/" class="hover:text-indigo-600">Submit Tool</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>"""

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    topic = blog_data['title'].split(':')[0] if ':' in blog_data['title'] else blog_data['title'].split()[0]

    return template.format(
        title=blog_data['title'],
        description=blog_data['description'],
        url=blog_data['url'],
        category=blog_data.get('category', 'Guides'),
        date=date_str,
        topic=topic.lower()
    )

def update_blog_index(blog_data):
    """Update the main blog index page with the new blog post"""
    index_path = Path("blog/index.html")

    if not index_path.exists():
        print(f"Warning: Blog index not found at {index_path}")
        return False

    # Read the current index
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create the new blog card HTML
    date_str = datetime.now(timezone.utc).strftime("%b %d, %Y")
    new_card = f'''            <article class="bg-white rounded-xl shadow-sm hover:shadow-md transition">
                <div class="p-6">
                    <div class="flex items-center gap-3 mb-3">
                        <span class="bg-indigo-100 text-indigo-600 text-xs px-3 py-1 rounded-full font-medium">{blog_data.get('category', 'Guides')}</span>
                        <span class="text-gray-500 text-sm">{date_str}</span>
                    </div>
                    <h2 class="text-xl font-bold text-gray-900 mb-3">
                        <a href="/blog/{blog_data['url']}/" class="hover:text-indigo-600">{blog_data['title']}</a>
                    </h2>
                    <p class="text-gray-600 mb-4 line-clamp-3">{blog_data['description']}</p>
                    <a href="/blog/{blog_data['url']}/" class="text-indigo-600 font-medium hover:text-indigo-800">
                        Read more →
                    </a>
                </div>
            </article>'''

    # Find the blog grid section and add the new card at the beginning
    grid_pattern = r'(<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">)'

    if re.search(grid_pattern, content):
        # Insert the new card after the grid opening tag
        content = re.sub(
            grid_pattern,
            r'\1\n' + new_card,
            content,
            count=1
        )

        # Save the updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated blog index with: {blog_data['title']}")
        return True
    else:
        print("Warning: Could not find blog grid section in index.html")
        return False

def update_homepage_blog_section(blog_data):
    """Update the homepage with the latest blog post"""
    homepage_path = Path("index.html")

    if not homepage_path.exists():
        print("Warning: Homepage not found")
        return False

    # Read the current homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create the new blog entry for homepage
    date_str = datetime.now(timezone.utc).strftime("%b %d, %Y")
    new_blog_entry = f'''                <article class="bg-white rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="p-6">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="bg-indigo-100 text-indigo-600 text-xs px-2 py-1 rounded-full">{blog_data.get('category', 'Guides')}</span>
                            <span class="text-gray-500 text-sm">{date_str}</span>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-2">
                            <a href="/blog/{blog_data['url']}/" class="hover:text-indigo-600 transition">{blog_data['title']}</a>
                        </h3>
                        <p class="text-gray-600 text-sm mb-3">{blog_data['description'][:100]}...</p>
                        <a href="/blog/{blog_data['url']}/" class="text-indigo-600 text-sm font-medium hover:text-indigo-800">
                            Read more →
                        </a>
                    </div>
                </article>'''

    # Find the "Latest Blog Posts" section and update it
    if 'Latest Blog Posts' in content:
        # Pattern to find the blog posts grid
        pattern = r'(<h2[^>]*>Latest Blog Posts</h2>.*?<div class="grid[^>]*>)(.*?)(</div>\s*</section>)'

        def replace_blogs(match):
            before = match.group(1)
            blogs = match.group(2)
            after = match.group(3)

            # Keep only the 3 most recent blogs
            existing_articles = re.findall(r'<article[^>]*>.*?</article>', blogs, re.DOTALL)

            # Add the new blog at the beginning and keep only 3 total
            updated_blogs = new_blog_entry
            if existing_articles:
                # Keep up to 2 more existing blogs
                for i, article in enumerate(existing_articles[:2]):
                    updated_blogs += '\n' + article

            return before + '\n' + updated_blogs + '\n            ' + after

        content = re.sub(pattern, replace_blogs, content, flags=re.DOTALL)

        # Save the updated homepage
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated homepage with latest blog: {blog_data['title']}")
        return True
    else:
        print("Warning: Could not find 'Latest Blog Posts' section on homepage")
        return False

def main():
    """Main function to publish blogs for today"""
    blogs = get_today_blogs()

    if not blogs:
        print("No blogs scheduled for today")
        return 0

    print(f"Found {len(blogs)} blog(s) to publish today")
    published_count = 0

    for blog in blogs:
        # Check if blog already exists
        if check_blog_exists(blog['url']):
            print(f"⏭️  Blog already exists: {blog['title']}")
            continue

        # Create blog directory
        blog_dir = Path(f"blog/{blog['url']}")
        blog_dir.mkdir(parents=True, exist_ok=True)

        # Create blog HTML
        html_content = create_blog_html(blog)

        # Write blog file
        blog_file = blog_dir / "index.html"
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Published: {blog['title']}")
        print(f"   URL: /blog/{blog['url']}/")

        # Update blog index
        update_blog_index(blog)

        # Update homepage
        update_homepage_blog_section(blog)

        published_count += 1

    if published_count > 0:
        print(f"\n🎉 Successfully published {published_count} new blog(s)")
    else:
        print("\n✨ No new blogs to publish")

    return published_count

if __name__ == "__main__":
    main()
    exit(0)
