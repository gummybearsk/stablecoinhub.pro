#!/usr/bin/env python3
"""
Update blog index page to include newly published blog posts
"""

import os
import re
from pathlib import Path
from datetime import datetime

def create_blog_card_html(url, title, category, date, description):
    """Create HTML for a blog card"""
    # Format date as "Sep 25, 2025"
    if isinstance(date, str):
        date_str = date
    else:
        date_str = date.strftime("%b %d, %Y")

    return f"""            <article class="bg-white rounded-xl shadow-sm hover:shadow-md transition">
                <div class="p-6">
                    <div class="flex items-center gap-3 mb-3">
                        <span class="bg-indigo-100 text-indigo-600 text-xs px-3 py-1 rounded-full font-medium">{category}</span>
                        <span class="text-gray-500 text-sm">{date_str}</span>
                    </div>
                    <h2 class="text-xl font-bold text-gray-900 mb-3">
                        <a href="/blog/{url}/" class="hover:text-indigo-600">{title}</a>
                    </h2>
                    <p class="text-gray-600 mb-4 line-clamp-3">{description[:150]}...</p>
                    <a href="/blog/{url}/" class="text-indigo-600 font-medium hover:text-indigo-800">
                        Read More →
                    </a>
                </div>
            </article>"""

def add_new_blog_to_index(blog_data):
    """Add a new blog to the blog index page"""
    index_path = Path("blog/index.html")

    if not index_path.exists():
        print(f"Blog index not found at {index_path}")
        return False

    # Read the current index
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create the new blog card HTML
    new_card = create_blog_card_html(
        blog_data['url'],
        blog_data['title'],
        blog_data.get('category', 'Guides'),
        blog_data.get('date', datetime.now().strftime("%b %d, %Y")),
        blog_data.get('description', 'Read our latest insights on stablecoins and cryptocurrency.')
    )

    # Find the blog grid container
    # Look for the opening of the blog grid and insert the new card at the beginning
    pattern = r'(<div id="blog-grid" class="grid[^>]*>)'

    if re.search(pattern, content):
        # Insert the new card after the grid opening
        content = re.sub(pattern, r'\1\n' + new_card, content)

        # Write back the updated content
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Added '{blog_data['title']}' to blog index")
        return True
    else:
        print("Could not find blog grid in index.html")
        return False

def update_homepage_latest_blogs(blog_data):
    """Update the homepage with the latest blog"""
    homepage_path = Path("index.html")

    if not homepage_path.exists():
        print(f"Homepage not found at {homepage_path}")
        return False

    # Read the current homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there's a latest blogs section
    if 'Latest Blog Posts' in content or 'Recent Articles' in content:
        # This would need to be customized based on the actual homepage structure
        print("Homepage has a blog section that needs updating")
        # Implementation would go here based on the actual structure

    return True

def main():
    """Main function to update blog index with today's published blog"""
    # Today's blog data (Sept 25, 2025)
    todays_blog = {
        "url": "usdt-vs-usdc",
        "title": "USDT vs USDC: Key Differences, Safety, and Which Stablecoin to Choose",
        "category": "Comparison",
        "date": "Sep 25, 2025",
        "description": "Comprehensive comparison of Tether (USDT) and USD Coin (USDC), analyzing safety, transparency, regulatory compliance, and ideal use cases for each stablecoin."
    }

    # Update blog index
    add_new_blog_to_index(todays_blog)

    # Update homepage (if applicable)
    update_homepage_latest_blogs(todays_blog)

    print("\n📝 Blog index updated successfully!")
    print("Remember to commit and push these changes.")

if __name__ == "__main__":
    main()