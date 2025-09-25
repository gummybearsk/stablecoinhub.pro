#!/usr/bin/env python3
"""
Auto-publish scheduled blog posts based on the publishing schedule.
This script runs daily via GitHub Actions and publishes blogs for the current date.
"""

import os
from datetime import datetime, timezone
from pathlib import Path

# Blog publishing schedule
BLOG_SCHEDULE = {
    "2025-09-25": [
        {
            "url": "usdt-vs-usdc",
            "title": "USDT vs USDC: Key Differences, Safety, and Which Stablecoin to Choose",
            "category": "Comparison",
            "description": "Comprehensive comparison of Tether (USDT) and USD Coin (USDC), analyzing safety, transparency, and use cases."
        }
    ],
    "2025-09-26": [
        {
            "url": "are-circulated-coins-worth-money",
            "title": "Are Circulated Coins Worth Money? How to Identify Rare and Valuable Coins",
            "category": "Collecting",
            "description": "Learn how to identify valuable circulated coins and understand what makes certain coins worth more than face value."
        }
    ]
}

def get_today_blogs():
    """Get blogs scheduled for today"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return BLOG_SCHEDULE.get(today, [])

def create_blog_html(blog_data):
    """Create HTML content for a blog post"""
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - StableCoin Hub</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="https://www.stablecoinhub.pro/blog/{url}/">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="text-2xl font-bold text-indigo-600">StableCoin Hub</a>
                <div class="flex space-x-4">
                    <a href="/" class="hover:text-indigo-600">Home</a>
                    <a href="/blog/" class="hover:text-indigo-600">Blog</a>
                </div>
            </div>
        </div>
    </nav>
    <article class="max-w-4xl mx-auto px-4 py-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">{title}</h1>
        <p class="text-lg text-gray-700 mb-6">{description}</p>
        <div class="prose prose-lg max-w-none">
            <p>Content will be added here.</p>
        </div>
    </article>
</body>
</html>"""

    return template.format(
        title=blog_data['title'],
        description=blog_data['description'],
        url=blog_data['url']
    )

def main():
    """Main function to publish scheduled blogs"""
    today_blogs = get_today_blogs()

    if not today_blogs:
        print(f"No blogs scheduled for today ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})")
        return

    print(f"Publishing {len(today_blogs)} blog(s) for today:")

    for blog in today_blogs:
        # Create blog directory
        blog_dir = Path(f"blog/{blog['url']}")
        blog_dir.mkdir(parents=True, exist_ok=True)

        # Create blog HTML
        html_content = create_blog_html(blog)

        # Write blog file
        blog_file = blog_dir / "index.html"
        with open(blog_file, 'w') as f:
            f.write(html_content)

        print(f"✅ Published: {blog['title']}")
        print(f"   URL: /blog/{blog['url']}/")

    print(f"\nSuccessfully published {len(today_blogs)} blog(s)")

if __name__ == "__main__":
    main()
