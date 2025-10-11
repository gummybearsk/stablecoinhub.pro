#!/usr/bin/env python3
"""
Script to automatically publish all missing blog posts
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')
os.chdir('/Users/raymond/Desktop/Stablecoinhub.pro/stablecoinhub-repo')

# Import the auto_publish_blogs module
from auto_publish_blogs import publish_blogs_for_date

def publish_all_missing():
    """Publish all missing blogs up to today"""

    # List of dates with missing blogs (from the analysis)
    missing_dates = [
        "2025-09-21", "2025-09-22", "2025-09-23", "2025-09-25",
        "2025-09-26", "2025-09-27", "2025-09-28", "2025-09-29", "2025-09-30",
        "2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05",
        "2025-10-06", "2025-10-07", "2025-10-08", "2025-10-09", "2025-10-10", "2025-10-11"
    ]

    print("=" * 80)
    print("AUTOMATICALLY PUBLISHING ALL MISSING BLOGS")
    print("=" * 80)
    print(f"Total dates to process: {len(missing_dates)}")
    print()

    total_published = 0

    for date in missing_dates:
        print(f"\n📝 Processing date: {date}")
        print("-" * 40)
        count = publish_blogs_for_date(date)
        total_published += count

        if count > 0:
            print(f"✅ Published {count} blog(s) for {date}")
        else:
            print(f"⏭️  No new blogs to publish for {date}")

    print("\n" + "=" * 80)
    print(f"🎉 PUBLISHING COMPLETE!")
    print(f"Total blogs published: {total_published}")
    print("=" * 80)

    return total_published

if __name__ == "__main__":
    published = publish_all_missing()

    if published > 0:
        print("\n📋 Next steps:")
        print("1. Review the published blogs")
        print("2. Update the blog index page")
        print("3. Deploy to production")
        print("4. Verify in Google Search Console")
    else:
        print("\n✨ All blogs are already published!")