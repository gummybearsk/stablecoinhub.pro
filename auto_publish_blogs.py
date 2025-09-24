#!/usr/bin/env python3
"""
Automated blog publishing system for StableCoin Hub.
Reads blog schedule and publishes blogs automatically.
"""

import os
import re
import json
from datetime import datetime, timezone
from pathlib import Path

def read_blog_schedule():
    """Read and parse the blog schedule from markdown file"""
    schedule_file = Path("../blog-schedule.md")

    if not schedule_file.exists():
        print(f"Warning: blog-schedule.md not found at {schedule_file}")
        # Use fallback schedule
        return get_fallback_schedule()

    with open(schedule_file, 'r') as f:
        content = f.read()

    # Parse the markdown to extract blog schedule
    schedule = {}
    current_month = None

    lines = content.split('\n')
    for line in lines:
        # Check for month headers
        if line.startswith('## '):
            month_match = re.search(r'## (\w+ \d{4})', line)
            if month_match:
                current_month = month_match.group(1)

        # Check for blog entries
        if line.startswith('- **'):
            date_match = re.search(r'\*\*(\w+ \d+)\*\*: (.+)', line)
            if date_match and current_month:
                day = date_match.group(1)
                title = date_match.group(2)

                # Convert to full date
                full_date = f"{current_month} {day.split()[-1]}"
                try:
                    date_obj = datetime.strptime(full_date, "%B %Y %d")
                    date_key = date_obj.strftime("%Y-%m-%d")

                    # Generate URL from title
                    url = generate_url_from_title(title)

                    if date_key not in schedule:
                        schedule[date_key] = []

                    schedule[date_key].append({
                        "title": title,
                        "url": url,
                        "category": determine_category(title),
                        "description": generate_description(title)
                    })
                except ValueError:
                    continue

    return schedule

def get_fallback_schedule():
    """Fallback schedule if blog-schedule.md is not available"""
    return {
        "2025-09-24": [
            {
                "url": "best-altcoins-to-buy",
                "title": "Best Altcoins to Buy Right Now: Top Picks, Examples, and Alternatives",
                "category": "Investment",
                "description": "Discover the best alternative cryptocurrencies to invest in, including analysis of top performers and emerging projects with potential for growth."
            }
        ],
        "2025-09-25": [
            {
                "url": "usdt-vs-usdc",
                "title": "USDT vs USDC: Key Differences, Safety, and Which Stablecoin to Choose",
                "category": "Comparison",
                "description": "Comprehensive comparison of Tether (USDT) and USD Coin (USDC), analyzing safety, transparency, regulatory compliance, and ideal use cases."
            }
        ]
    }

def generate_url_from_title(title):
    """Generate URL-friendly slug from title"""
    # Remove special characters and convert to lowercase
    url = re.sub(r'[^\w\s-]', '', title.lower())
    # Replace spaces with hyphens
    url = re.sub(r'[-\s]+', '-', url)
    # Remove trailing hyphens
    url = url.strip('-')
    # Limit length
    if len(url) > 50:
        url = url[:50].rsplit('-', 1)[0]
    return url

def determine_category(title):
    """Determine category based on title keywords"""
    title_lower = title.lower()

    if any(word in title_lower for word in ['how to', 'guide', 'what is', 'explained']):
        return "Education"
    elif any(word in title_lower for word in ['vs', 'versus', 'comparison', 'difference']):
        return "Comparison"
    elif any(word in title_lower for word in ['best', 'top', 'invest', 'buy']):
        return "Investment"
    elif any(word in title_lower for word in ['earn', 'yield', 'apy', 'interest', 'staking']):
        return "Yield"
    elif any(word in title_lower for word in ['bitcoin', 'btc', 'ethereum', 'eth']):
        return "Crypto"
    elif any(word in title_lower for word in ['coin', 'dollar', 'cent', 'penny']):
        return "Currency"
    elif any(word in title_lower for word in ['trade', 'trading', 'support', 'resistance']):
        return "Trading"
    else:
        return "General"

def generate_description(title):
    """Generate a description based on the title"""
    descriptions = {
        "stablecoin": "Comprehensive guide to stablecoins, their mechanisms, and practical applications in the cryptocurrency ecosystem.",
        "bitcoin": "In-depth analysis of Bitcoin, including market trends, valuation, and investment strategies.",
        "earn": "Discover strategies to generate passive income through cryptocurrency investments and DeFi protocols.",
        "coin": "Essential information about coins, their value, history, and collection potential.",
        "invest": "Expert insights on cryptocurrency investments, market analysis, and portfolio strategies.",
        "usdt": "Complete guide to Tether (USDT), the world's largest stablecoin by market capitalization.",
        "usdc": "Detailed overview of USD Coin (USDC), focusing on safety, transparency, and use cases."
    }

    title_lower = title.lower()
    for keyword, desc_template in descriptions.items():
        if keyword in title_lower:
            return desc_template

    return "Comprehensive guide providing essential insights and practical information for cryptocurrency and stablecoin users."

def create_blog_html(blog_data):
    """Create HTML content for a blog post"""
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - StableCoin Hub</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.stablecoinhub.pro/blog/{url}/">
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
        <nav class="text-sm mb-6" aria-label="Breadcrumb">
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
                <time datetime="{iso_date}">{date}</time>
                <span class="mx-2">•</span>
                <span>8 min read</span>
            </div>
            <div class="mt-4">
                <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm">{category}</span>
            </div>
        </header>

        <!-- Article Content -->
        <div class="prose prose-lg max-w-none">
            <p class="text-lg text-gray-700 mb-6 leading-relaxed">
                {description}
            </p>

            <h2 class="text-2xl font-bold mb-4 mt-8">Overview</h2>

            <p class="mb-4">
                Understanding the fundamentals of {topic} is essential for anyone navigating the modern financial landscape. This comprehensive guide breaks down complex concepts into actionable insights that you can apply immediately.
            </p>

            <h2 class="text-2xl font-bold mb-4 mt-8">Key Points to Consider</h2>

            <ul class="list-disc pl-6 space-y-2 mb-6">
                <li>Market dynamics and current trends</li>
                <li>Risk factors and mitigation strategies</li>
                <li>Regulatory considerations and compliance</li>
                <li>Technical implementation details</li>
                <li>Future outlook and emerging opportunities</li>
            </ul>

            <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8">
                <p class="font-semibold mb-2">📊 Discover More Resources</p>
                <p>
                    Explore our comprehensive directory of 95+ stablecoin platforms, exchanges, and DeFi protocols at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Find the perfect tools for your financial strategy.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Practical Applications</h2>

            <p class="mb-4">
                The insights from this guide can be applied in various scenarios:
            </p>

            <ol class="list-decimal pl-6 space-y-2 mb-6">
                <li><strong>Investment Planning:</strong> Make informed decisions based on comprehensive market analysis</li>
                <li><strong>Risk Management:</strong> Identify and mitigate potential risks in your portfolio</li>
                <li><strong>Strategic Positioning:</strong> Align your approach with market trends and opportunities</li>
                <li><strong>Operational Efficiency:</strong> Implement best practices for optimal results</li>
                <li><strong>Compliance:</strong> Navigate regulatory requirements with confidence</li>
            </ol>

            <div class="bg-yellow-50 border-l-4 border-yellow-600 p-6 my-8">
                <p class="font-semibold mb-2">⚠️ Important Reminder</p>
                <p>
                    Always conduct thorough research and consider consulting with financial advisors before making investment decisions. The cryptocurrency market is volatile and past performance doesn't guarantee future results.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Getting Started</h2>

            <p class="mb-4">
                Ready to take action? Here's how to get started:
            </p>

            <div class="bg-gray-100 rounded-lg p-6 mb-6">
                <ol class="list-decimal pl-6 space-y-3">
                    <li>Review your current portfolio and risk tolerance</li>
                    <li>Research available platforms and tools</li>
                    <li>Start with small amounts to gain experience</li>
                    <li>Monitor performance and adjust strategies</li>
                    <li>Stay informed about market developments</li>
                </ol>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Expert Tips</h2>

            <div class="space-y-4 mb-6">
                <div class="flex items-start">
                    <span class="text-2xl mr-3">💡</span>
                    <p><strong>Diversification:</strong> Don't put all your eggs in one basket. Spread risk across different assets and strategies.</p>
                </div>
                <div class="flex items-start">
                    <span class="text-2xl mr-3">📈</span>
                    <p><strong>Market Timing:</strong> While perfect timing is impossible, understanding market cycles can improve decision-making.</p>
                </div>
                <div class="flex items-start">
                    <span class="text-2xl mr-3">🔒</span>
                    <p><strong>Security First:</strong> Always prioritize security measures to protect your assets.</p>
                </div>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Conclusion</h2>

            <p class="mb-4">
                The landscape of digital finance continues to evolve rapidly, presenting both opportunities and challenges. By staying informed and applying the insights from this guide, you're better positioned to navigate this dynamic environment successfully.
            </p>

            <p class="mb-4">
                Remember that continuous learning and adaptation are key to long-term success. Visit <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a> regularly for the latest updates, tools, and analysis in the stablecoin ecosystem.
            </p>

            <div class="bg-green-50 border-l-4 border-green-600 p-6 my-8">
                <p class="font-semibold mb-2">✅ Key Takeaways</p>
                <ul class="list-disc pl-6 space-y-1">
                    <li>Understanding fundamentals is crucial for success</li>
                    <li>Risk management should always be a priority</li>
                    <li>Stay informed about regulatory developments</li>
                    <li>Use reliable platforms and tools</li>
                    <li>Continuous learning leads to better outcomes</li>
                </ul>
            </div>
        </div>

        <!-- Author Box -->
        <div class="bg-gray-100 rounded-lg p-6 mt-12">
            <h3 class="font-semibold mb-2 text-lg">About StableCoin Hub</h3>
            <p class="text-gray-600 mb-3">
                StableCoin Hub is your premier destination for discovering and comparing stablecoin tools, platforms, and resources. Our mission is to make the stablecoin ecosystem accessible to everyone through comprehensive directories, expert analysis, and educational content.
            </p>
            <p class="text-gray-600">
                Explore our directory of 95+ verified platforms at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline font-medium">StableCoinHub.pro</a> and join thousands of users making informed decisions in the stablecoin space.
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

    # Extract topic from title
    topic = blog_data['title'].split(':')[0] if ':' in blog_data['title'] else blog_data['title'].split(' ')[0]

    # Get current date
    now = datetime.now(timezone.utc)
    date = now.strftime("%B %d, %Y")
    iso_date = now.isoformat()

    return template.format(
        title=blog_data['title'],
        description=blog_data['description'],
        url=blog_data['url'],
        date=date,
        iso_date=iso_date,
        category=blog_data['category'],
        breadcrumb_title=breadcrumb,
        topic=topic.lower()
    )

def publish_blogs_for_date(target_date=None):
    """Publish blogs for a specific date or today"""
    if target_date is None:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"Checking blogs for {target_date}...")

    # Read schedule
    schedule = read_blog_schedule()

    if target_date not in schedule:
        print(f"No blogs scheduled for {target_date}")
        return 0

    blogs = schedule[target_date]
    print(f"Found {len(blogs)} blog(s) to publish")

    published_count = 0
    for blog in blogs:
        # Check if blog already exists
        blog_dir = Path(f"blog/{blog['url']}")
        blog_file = blog_dir / "index.html"

        if blog_file.exists():
            print(f"⏭️  Blog already exists: {blog['title']}")
            continue

        # Create blog directory
        blog_dir.mkdir(parents=True, exist_ok=True)

        # Create blog HTML
        html_content = create_blog_html(blog)

        # Write blog file
        with open(blog_file, 'w') as f:
            f.write(html_content)

        print(f"✅ Published: {blog['title']}")
        print(f"   URL: /blog/{blog['url']}/")
        published_count += 1

    return published_count

def main():
    """Main function for manual execution"""
    import sys

    # Check for date argument
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
        print(f"Publishing blogs for specific date: {target_date}")
    else:
        target_date = None
        print("Publishing blogs for today")

    published = publish_blogs_for_date(target_date)

    if published > 0:
        print(f"\n🎉 Successfully published {published} new blog(s)")
        print("Remember to commit and push the changes to GitHub!")
    else:
        print("\n✨ No new blogs to publish")

if __name__ == "__main__":
    main()