#!/usr/bin/env python3
"""
Auto-publish scheduled blog posts based on the publishing schedule.
This script runs daily via GitHub Actions and publishes blogs for the current date.
"""

import os
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Blog publishing schedule
BLOG_SCHEDULE = {
    "2025-09-21": [
        {
            "url": "what-is-stablecoin",
            "title": "What Is a Stablecoin? Types, Examples, and How They Work",
            "category": "Education",
            "description": "Complete guide to understanding stablecoins, their mechanisms, types (fiat-backed, crypto-backed, algorithmic), and role in the cryptocurrency ecosystem."
        }
    ],
    "2025-09-22": [
        {
            "url": "earn-interest-on-crypto",
            "title": "How to Earn Interest on Crypto: Accounts, APY Rates, and Yield Strategies",
            "category": "Yield",
            "description": "Discover the best platforms and strategies to earn 5-12% APY on your stablecoins safely through lending, staking, and DeFi protocols."
        }
    ],
    "2025-09-23": [
        {
            "url": "who-is-on-us-coins",
            "title": "Who Is on US Coins? Complete Guide to Presidents and Historical Figures",
            "category": "Education",
            "description": "Learn about the presidents and historical figures featured on US coins, from Lincoln pennies to Sacagawea dollars."
        }
    ],
    "2025-09-24": [
        {
            "url": "best-altcoins-to-buy",
            "title": "Best Altcoins to Buy Right Now: Top Picks, Examples, and Alternatives",
            "category": "Investment",
            "description": "Discover the best alternative cryptocurrencies to invest in, including analysis of top performers and emerging projects."
        }
    ],
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
    ],
    "2025-09-27": [
        {
            "url": "how-much-is-10000-bitcoin-worth",
            "title": "How Much Is 10,000 Bitcoin Worth? USD Value Today and in History",
            "category": "Crypto",
            "description": "Calculate the current value of 10,000 Bitcoin and explore its historical significance, including the famous pizza purchase."
        }
    ],
    "2025-09-28": [
        {
            "url": "where-can-i-get-dollar-coins",
            "title": "Where Can I Get Dollar Coins? Buying, Collecting, and Using Them Today",
            "category": "Practical",
            "description": "Complete guide on where to obtain dollar coins for spending or collecting, including banks, online dealers, and the US Mint."
        }
    ],
    "2025-09-29": [
        {
            "url": "bitcoin-support-resistance-levels",
            "title": "Bitcoin Support and Resistance Levels: Key Price Zones to Watch",
            "category": "Trading",
            "description": "Learn how to identify and trade Bitcoin support and resistance levels for better entry and exit points."
        }
    ],
    "2025-09-30": [
        {
            "url": "do-stablecoins-go-up-in-value",
            "title": "Do Stablecoins Go Up in Value? Understanding Types, Risks, and Why People Invest",
            "category": "Education",
            "description": "Explore whether stablecoins can increase in value, their investment potential, and earning strategies."
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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GX6EB7DSFL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-GX6EB7DSFL');
    </script>
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
                            <a href="/blog/" class="text-gray-900 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                            <a href="/submit/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Submit Tool</a>
                            <a href="/about/" class="text-gray-500 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Article -->
    <article class="max-w-4xl mx-auto px-4 py-12">
        <!-- Breadcrumb -->
        <nav class="text-sm mb-6">
            <a href="/" class="text-gray-500 hover:text-indigo-600">Home</a>
            <span class="mx-2 text-gray-400">/</span>
            <a href="/blog/" class="text-gray-500 hover:text-indigo-600">Blog</a>
            <span class="mx-2 text-gray-400">/</span>
            <span class="text-gray-900">{breadcrumb_title}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">{title}</h1>
            <div class="flex items-center text-gray-600 text-sm">
                <span>By StableCoin Hub Team</span>
                <span class="mx-2">•</span>
                <time>{date}</time>
                <span class="mx-2">•</span>
                <span>10 min read</span>
            </div>
            <div class="mt-4">
                <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm">{category}</span>
            </div>
        </header>

        <!-- Article Content -->
        <div class="prose prose-lg max-w-none">
            <p class="text-lg text-gray-700 mb-6">
                {description}
            </p>

            <h2 class="text-2xl font-bold mb-4 mt-8">Key Insights</h2>

            <p class="mb-4">
                This comprehensive guide provides essential information for anyone interested in understanding this topic. Whether you're a beginner or an experienced user, these insights will help you make informed decisions.
            </p>

            <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8">
                <p class="font-semibold mb-2">📊 Explore More Tools</p>
                <p>
                    Discover 95+ stablecoin platforms, exchanges, and DeFi protocols at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Find the perfect tools for your strategy.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Why This Matters</h2>

            <p class="mb-4">
                The cryptocurrency and stablecoin ecosystem is rapidly evolving. Staying informed through trusted resources helps you navigate this complex landscape effectively.
            </p>

            <h2 class="text-2xl font-bold mb-4 mt-8">Practical Applications</h2>

            <ul class="list-disc pl-6 space-y-2 mb-6">
                <li>Portfolio management and diversification</li>
                <li>Risk assessment and mitigation</li>
                <li>Strategic planning for investments</li>
                <li>Understanding market dynamics</li>
                <li>Making informed financial decisions</li>
            </ul>

            <div class="bg-yellow-50 border-l-4 border-yellow-600 p-6 my-8">
                <p class="font-semibold mb-2">💡 Pro Tip</p>
                <p>
                    Always do your own research (DYOR) and never invest more than you can afford to lose. The cryptocurrency market carries inherent risks.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Stay Updated</h2>

            <p class="mb-4">
                Visit <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a> regularly for the latest tools, news, and analysis. Our team continuously updates our directory with new platforms and features.
            </p>

            <div class="bg-green-50 border-l-4 border-green-600 p-6 my-8">
                <p class="font-semibold mb-2">✅ Key Takeaways</p>
                <ul class="list-disc pl-6 space-y-1">
                    <li>Understanding the fundamentals is crucial for success</li>
                    <li>Different strategies serve different goals and risk profiles</li>
                    <li>Proper research and risk management are essential</li>
                    <li>The ecosystem continues to evolve with new innovations</li>
                </ul>
            </div>
        </div>

        <!-- Author Box -->
        <div class="bg-gray-100 rounded-lg p-6 mt-12">
            <p class="font-semibold mb-2">About StableCoin Hub</p>
            <p class="text-gray-600">
                StableCoin Hub is your comprehensive resource for discovering and comparing stablecoin tools and platforms. Visit <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a> to explore our full directory.
            </p>
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

    breadcrumb = blog_data['title'].split(':')[0] if ':' in blog_data['title'] else blog_data['title'][:30] + "..."
    date = datetime.now(timezone.utc).strftime("%B %d, %Y")

    return template.format(
        title=blog_data['title'],
        description=blog_data['description'],
        url=blog_data['url'],
        date=date,
        category=blog_data['category'],
        breadcrumb_title=breadcrumb
    )

def update_blog_index(new_blogs):
    """Update the main blog index page with new posts"""
    index_path = Path("blog/index.html")

    if not index_path.exists():
        print(f"Blog index not found at {index_path}")
        return

    # Read current index
    with open(index_path, 'r') as f:
        content = f.read()

    # Find the blog posts section
    # This is a simplified version - you'd need to parse the actual HTML structure
    # For now, we'll just log that the index should be updated
    print(f"Blog index should be updated with {len(new_blogs)} new posts")

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

    # Update blog index
    update_blog_index(today_blogs)

    print(f"\nSuccessfully published {len(today_blogs)} blog(s)")

if __name__ == "__main__":
    main()