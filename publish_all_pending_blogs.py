#!/usr/bin/env python3
"""
Script to check and publish all pending blog posts
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

def read_blog_schedule():
    """Read and parse the blog schedule from markdown file"""
    schedule_file = Path("../blog-schedule.md")

    if not schedule_file.exists():
        print(f"Error: blog-schedule.md not found at {schedule_file}")
        return {}

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
                        "date": date_key,
                        "category": determine_category(title)
                    })
                except ValueError:
                    continue

    return schedule

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

def check_blog_exists(url):
    """Check if blog already exists"""
    blog_dir = Path(f"blog/{url}")
    blog_file = blog_dir / "index.html"
    return blog_file.exists()

def analyze_blogs():
    """Analyze blog publishing status"""
    schedule = read_blog_schedule()

    if not schedule:
        print("No blog schedule found!")
        return

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Categorize blogs
    published = []
    should_be_published = []
    future = []

    for date_str, blogs in sorted(schedule.items()):
        for blog in blogs:
            blog_info = {
                "date": date_str,
                "title": blog['title'],
                "url": blog['url'],
                "exists": check_blog_exists(blog['url'])
            }

            if date_str <= today:
                if blog_info['exists']:
                    published.append(blog_info)
                else:
                    should_be_published.append(blog_info)
            else:
                future.append(blog_info)

    # Print analysis
    print("=" * 80)
    print("BLOG PUBLISHING STATUS REPORT")
    print("=" * 80)
    print(f"Today's Date: {today}")
    print(f"Total Scheduled Blogs: {sum(len(blogs) for blogs in schedule.values())}")
    print()

    print(f"✅ PUBLISHED BLOGS: {len(published)}")
    if published:
        for blog in published[:5]:
            print(f"   • {blog['date']}: {blog['title'][:50]}...")
        if len(published) > 5:
            print(f"   ... and {len(published) - 5} more")
    print()

    print(f"⚠️  SHOULD BE PUBLISHED (MISSING): {len(should_be_published)}")
    if should_be_published:
        for blog in should_be_published:
            print(f"   • {blog['date']}: {blog['title']}")
            print(f"     URL: /blog/{blog['url']}/")
    print()

    print(f"📅 FUTURE BLOGS: {len(future)}")
    if future:
        for blog in future[:5]:
            print(f"   • {blog['date']}: {blog['title'][:50]}...")
        if len(future) > 5:
            print(f"   ... and {len(future) - 5} more")
    print()

    return should_be_published

def main():
    """Main function"""
    os.chdir('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')

    # Analyze blog status
    missing_blogs = analyze_blogs()

    if missing_blogs:
        print("=" * 80)
        print("PUBLISHING MISSING BLOGS")
        print("=" * 80)

        # Ask for confirmation
        response = input(f"\nDo you want to publish all {len(missing_blogs)} missing blogs? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            # Import and use the auto_publish_blogs module
            import sys
            sys.path.append('.')
            from auto_publish_blogs import publish_blogs_for_date

            published_count = 0
            for blog in missing_blogs:
                print(f"\nPublishing blogs for {blog['date']}...")
                count = publish_blogs_for_date(blog['date'])
                published_count += count

            print(f"\n✅ Successfully published {published_count} blogs!")
            print("\n📝 Next steps:")
            print("1. Review the published blogs")
            print("2. Update the blog index if needed")
            print("3. Deploy to production")
        else:
            print("Publishing cancelled.")
    else:
        print("✨ All blogs are up to date! No missing blogs found.")

if __name__ == "__main__":
    main()