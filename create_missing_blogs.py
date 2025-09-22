#!/usr/bin/env python3
import os
import re
import glob

# The beautiful template with all the nice design elements
BLOG_TEMPLATE = """<!DOCTYPE html>
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
            <span class="text-gray-900">{breadcrumb}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">{title}</h1>
            <div class="flex items-center text-gray-600 text-sm">
                <span>By StableCoin Hub Team</span>
                <span class="mx-2">•</span>
                <time datetime="{date_iso}">{date}</time>
                <span class="mx-2">•</span>
                <span>15 min read</span>
            </div>
            <div class="mt-4 flex gap-2">
                {category_tags}
            </div>
        </header>

        <!-- Article Content -->
        <div class="prose prose-lg max-w-none">
{content}
        </div>

        <!-- Author Box -->
        <div class="bg-gray-100 rounded-lg p-6 mt-12">
            <p class="font-semibold mb-2">About StableCoin Hub</p>
            <p class="text-gray-600">
                StableCoin Hub is your comprehensive resource for discovering and comparing stablecoin tools and platforms. Visit <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a> to explore our directory of 95+ vetted tools.
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

def process_original_content(md_content):
    """Process the EXACT original markdown content to HTML, preserving everything"""

    # Skip the front matter
    if '---' in md_content:
        parts = md_content.split('---')
        if len(parts) >= 3:
            content = '---'.join(parts[2:]).strip()
        else:
            content = md_content
    else:
        content = md_content

    # Convert headers
    content = re.sub(r'^## (.+)$', r'<h2 class="text-2xl font-bold mb-4 mt-8">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3 class="text-xl font-semibold mb-3">\1</h3>', content, flags=re.MULTILINE)

    # Convert bold text
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Convert links - handle both blog links and external links
    content = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:underline">\1</a>', content)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:underline">\1</a>', content)

    # Process lists properly
    lines = content.split('\n')
    processed = []
    in_ul = False
    in_ol = False

    for line in lines:
        # Handle unordered lists
        if line.strip().startswith('- '):
            if not in_ul:
                processed.append('<ul class="list-disc pl-6 space-y-2 mb-6">')
                in_ul = True
            processed.append(f'<li>{line.strip()[2:]}</li>')
        # Handle ordered lists
        elif re.match(r'^\d+\.\s+', line.strip()):
            if not in_ol:
                if in_ul:
                    processed.append('</ul>')
                    in_ul = False
                processed.append('<ol class="list-decimal pl-6 space-y-2 mb-6">')
                in_ol = True
            content_text = re.sub(r'^\d+\.\s+', '', line.strip())
            processed.append(f'<li>{content_text}</li>')
        else:
            # Close open lists
            if in_ul:
                processed.append('</ul>')
                in_ul = False
            if in_ol:
                processed.append('</ol>')
                in_ol = False

            # Handle tables
            if '|' in line and line.strip().startswith('|'):
                if '---' in line:
                    continue  # Skip separator
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if any('**' in cell or 'Stablecoin' in cell or 'Type' in cell for cell in cells):
                    # Header row
                    processed.append('<div class="overflow-x-auto mb-6"><table class="min-w-full border-collapse border border-gray-300"><thead class="bg-gray-100"><tr>')
                    for cell in cells:
                        processed.append(f'<th class="border border-gray-300 px-4 py-2">{cell}</th>')
                    processed.append('</tr></thead><tbody>')
                else:
                    # Data row
                    processed.append('<tr>')
                    for cell in cells:
                        processed.append(f'<td class="border border-gray-300 px-4 py-2">{cell}</td>')
                    processed.append('</tr>')
            elif line.strip() and not line.startswith('<'):
                # Regular paragraph
                processed.append(f'<p class="mb-4">{line}</p>')
            else:
                processed.append(line)

    # Close any open lists
    if in_ul:
        processed.append('</ul>')
    if in_ol:
        processed.append('</ol>')

    return '\n'.join(processed)

# Blog post metadata
BLOG_METADATA = {
    'usdc-vs-usdt-complete-guide': {'date': 'September 11, 2025', 'date_iso': '2025-09-11', 'categories': ['Comparison', 'Analysis']},
    'are-stablecoins-good-investment': {'date': 'September 11, 2025', 'date_iso': '2025-09-11', 'categories': ['Investment', 'Guide']},
    'euro-stablecoins': {'date': 'September 10, 2025', 'date_iso': '2025-09-10', 'categories': ['Regional', 'Euro']},
    'commodity-backed-stablecoins': {'date': 'September 10, 2025', 'date_iso': '2025-09-10', 'categories': ['Types', 'Commodities']},
    'stablecoin-bridges': {'date': 'September 9, 2025', 'date_iso': '2025-09-09', 'categories': ['DeFi', 'Infrastructure']},
    'stablecoin-insurance': {'date': 'September 9, 2025', 'date_iso': '2025-09-09', 'categories': ['Risk', 'Protection']},
    'stablecoin-statistics': {'date': 'September 8, 2025', 'date_iso': '2025-09-08', 'categories': ['Data', 'Analytics']},
    'stablecoin-debit-cards': {'date': 'September 8, 2025', 'date_iso': '2025-09-08', 'categories': ['Payment', 'Cards']},
    'stablecoin-remittances': {'date': 'September 7, 2025', 'date_iso': '2025-09-07', 'categories': ['Payment', 'Transfer']},
    'stablecoin-oracles': {'date': 'September 7, 2025', 'date_iso': '2025-09-07', 'categories': ['Technology', 'DeFi']},
    'stablecoin-treasury': {'date': 'September 6, 2025', 'date_iso': '2025-09-06', 'categories': ['Finance', 'Management']},
    'stablecoin-adoption': {'date': 'September 6, 2025', 'date_iso': '2025-09-06', 'categories': ['Market', 'Trends']},
    'asian-stablecoins': {'date': 'September 5, 2025', 'date_iso': '2025-09-05', 'categories': ['Regional', 'Asia']},
    'stablecoin-derivatives': {'date': 'September 5, 2025', 'date_iso': '2025-09-05', 'categories': ['Trading', 'Advanced']},
    'inflation-hedge-stablecoins': {'date': 'September 4, 2025', 'date_iso': '2025-09-04', 'categories': ['Investment', 'Protection']},
    'stablecoin-scalability': {'date': 'September 4, 2025', 'date_iso': '2025-09-04', 'categories': ['Technology', 'Performance']},
    'stablecoin-governance': {'date': 'September 3, 2025', 'date_iso': '2025-09-03', 'categories': ['DAO', 'Governance']},
    'stablecoin-privacy': {'date': 'September 3, 2025', 'date_iso': '2025-09-03', 'categories': ['Privacy', 'Security']},
    'stablecoin-etf': {'date': 'September 2, 2025', 'date_iso': '2025-09-02', 'categories': ['Investment', 'ETF']},
    'stablecoin-smart-contracts': {'date': 'September 2, 2025', 'date_iso': '2025-09-02', 'categories': ['Technology', 'Smart Contracts']},
    'stablecoin-compliance': {'date': 'September 1, 2025', 'date_iso': '2025-09-01', 'categories': ['Legal', 'Compliance']},
    'stablecoin-gaming': {'date': 'September 1, 2025', 'date_iso': '2025-09-01', 'categories': ['Gaming', 'Use Cases']},
    'stablecoin-education': {'date': 'August 31, 2025', 'date_iso': '2025-08-31', 'categories': ['Education', 'Learning']},
    'stablecoin-future': {'date': 'August 31, 2025', 'date_iso': '2025-08-31', 'categories': ['Future', 'Trends']},
    'stablecoin-networks': {'date': 'August 30, 2025', 'date_iso': '2025-08-30', 'categories': ['Blockchain', 'Networks']},
    'stablecoin-use-cases': {'date': 'August 30, 2025', 'date_iso': '2025-08-30', 'categories': ['Use Cases', 'Applications']},
    'stablecoin-volatility': {'date': 'August 29, 2025', 'date_iso': '2025-08-29', 'categories': ['Risk', 'Analysis']},
    'stablecoin-apis': {'date': 'August 29, 2025', 'date_iso': '2025-08-29', 'categories': ['Technology', 'Development']},
    'stablecoin-accounting': {'date': 'August 28, 2025', 'date_iso': '2025-08-28', 'categories': ['Finance', 'Accounting']},
    'stablecoin-mining': {'date': 'August 28, 2025', 'date_iso': '2025-08-28', 'categories': ['Mining', 'Yield']},
    'stablecoin-news': {'date': 'August 27, 2025', 'date_iso': '2025-08-27', 'categories': ['News', 'Updates']},
    'stablecoin-portfolio': {'date': 'August 27, 2025', 'date_iso': '2025-08-27', 'categories': ['Investment', 'Portfolio']},
    'stablecoin-partnerships': {'date': 'August 26, 2025', 'date_iso': '2025-08-26', 'categories': ['Business', 'Partnerships']},
    'stablecoin-trading-strategies': {'date': 'August 26, 2025', 'date_iso': '2025-08-26', 'categories': ['Trading', 'Strategies']},
    'stablecoin-glossary': {'date': 'August 25, 2025', 'date_iso': '2025-08-25', 'categories': ['Education', 'Reference']},
    'stablecoin-research': {'date': 'August 25, 2025', 'date_iso': '2025-08-25', 'categories': ['Research', 'Analysis']},
    'stablecoin-calculator': {'date': 'August 24, 2025', 'date_iso': '2025-08-24', 'categories': ['Tools', 'Calculator']},
    'stablecoin-community': {'date': 'August 24, 2025', 'date_iso': '2025-08-24', 'categories': ['Community', 'Social']},
    'stablecoin-beginners-guide': {'date': 'August 23, 2025', 'date_iso': '2025-08-23', 'categories': ['Education', 'Beginner']},
    'stablecoin-monthly-recap': {'date': 'August 23, 2025', 'date_iso': '2025-08-23', 'categories': ['News', 'Recap']}
}

# Related articles mapping
RELATED_ARTICLES = {
    'default': [
        {'url': '/blog/what-is-stablecoin/', 'title': 'What Is a Stablecoin?', 'desc': 'Complete Beginner Guide'},
        {'url': '/blog/best-stablecoin-wallets/', 'title': 'Best Wallets', 'desc': 'Store Safely'},
        {'url': '/blog/earn-interest-on-crypto/', 'title': 'Earn Yield', 'desc': 'Passive Income'}
    ]
}

def get_related_articles(url_slug):
    """Get related articles for a blog post"""
    # Return default for now - can be customized per post
    return RELATED_ARTICLES['default']

def create_blog_post(md_file):
    """Create HTML for a blog post"""
    # Get URL slug from filename
    filename = os.path.basename(md_file)
    url_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    # Create directory if needed
    blog_dir = f'blog/{url_slug}'
    os.makedirs(blog_dir, exist_ok=True)

    html_file = f'{blog_dir}/index.html'

    # Check if already exists
    if os.path.exists(html_file):
        return False, f"Already exists: {html_file}"

    # Read original markdown
    with open(md_file, 'r') as f:
        original_md = f.read()

    # Extract metadata
    title_match = re.search(r'title:\s*"([^"]+)"', original_md)
    desc_match = re.search(r'description:\s*"([^"]+)"', original_md)

    if not title_match:
        return False, "No title found in markdown"

    title = title_match.group(1)
    description = desc_match.group(1) if desc_match else "Comprehensive guide for the stablecoin ecosystem."

    # Get metadata
    metadata = BLOG_METADATA.get(url_slug, {
        'date': 'September 2025',
        'date_iso': '2025-09-01',
        'categories': ['Stablecoins', 'Guide']
    })

    # Process content
    html_content = process_original_content(original_md)

    # Add beautiful info box mid-content
    sections = html_content.split('<h2')
    if len(sections) > 3:
        box_messages = [
            ('🏦 Visit StableCoin Hub for More', 'Explore our comprehensive directory at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a> to discover 95+ stablecoin tools, exchanges, and DeFi protocols.'),
            ('📊 Track Stablecoin Markets', 'Stay updated with real-time data at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Find the best yields and trading opportunities.'),
            ('🔍 Discover More Tools', 'Browse vetted platforms at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Compare features, fees, and security.'),
        ]
        import random
        box_title, box_text = random.choice(box_messages)

        sections[3] = f'''
            <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8">
                <p class="font-semibold mb-2">{box_title}</p>
                <p>{box_text}</p>
            </div>

            <h2''' + sections[3]
        html_content = '<h2'.join(sections)

    # Get related articles
    related = get_related_articles(url_slug)
    related_html = '\n'.join([
        f'''<a href="{art['url']}" class="block bg-white rounded-lg p-4 border hover:shadow-md transition">
                    <h3 class="font-semibold text-gray-900 mb-1 text-sm hover:text-indigo-600">
                        {art['title']}
                    </h3>
                    <p class="text-gray-600 text-xs">{art['desc']}</p>
                </a>''' for art in related
    ])

    # Add Next Steps section
    next_steps = f'''
            <h2 class="text-2xl font-bold mb-4 mt-8">Next Steps</h2>

            <p class="mb-4">Continue exploring the stablecoin ecosystem:</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                {related_html}
            </div>
'''

    html_content += next_steps

    # Create category tags
    category_tags = ' '.join([
        f'<span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm">{cat}</span>'
        for cat in metadata['categories']
    ])

    # Create final HTML
    final_html = BLOG_TEMPLATE.format(
        title=title,
        description=description,
        url=url_slug,
        breadcrumb=title.split(':')[0] if ':' in title else title,
        date=metadata['date'],
        date_iso=metadata['date_iso'],
        category_tags=category_tags,
        content=html_content
    )

    # Write the file
    with open(html_file, 'w') as f:
        f.write(final_html)

    return True, "Created"

# Main execution
print("Creating missing blog HTML files with EXACT original content...")
print("=" * 60)

# Get all markdown files
md_files = glob.glob('blog/_posts/*.md')

# List of blog posts to create
missing_posts = [
    'usdc-vs-usdt-complete-guide',
    'are-stablecoins-good-investment',
    'euro-stablecoins',
    'commodity-backed-stablecoins',
    'stablecoin-bridges',
    'stablecoin-insurance',
    'stablecoin-statistics',
    'stablecoin-debit-cards',
    'stablecoin-remittances',
    'stablecoin-oracles',
    'stablecoin-treasury',
    'stablecoin-adoption',
    'asian-stablecoins',
    'stablecoin-derivatives',
    'inflation-hedge-stablecoins',
    'stablecoin-scalability',
    'stablecoin-governance',
    'stablecoin-privacy',
    'stablecoin-etf',
    'stablecoin-smart-contracts',
    'stablecoin-compliance',
    'stablecoin-gaming',
    'stablecoin-education',
    'stablecoin-future',
    'stablecoin-networks',
    'stablecoin-use-cases',
    'stablecoin-volatility',
    'stablecoin-apis',
    'stablecoin-accounting',
    'stablecoin-mining',
    'stablecoin-news',
    'stablecoin-portfolio',
    'stablecoin-partnerships',
    'stablecoin-trading-strategies',
    'stablecoin-glossary',
    'stablecoin-research',
    'stablecoin-calculator',
    'stablecoin-community',
    'stablecoin-beginners-guide',
    'stablecoin-monthly-recap'
]

created_count = 0
for md_file in sorted(md_files):
    filename = os.path.basename(md_file)
    url_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    if url_slug in missing_posts:
        success, message = create_blog_post(md_file)
        if success:
            print(f"✅ Created: {url_slug}")
            created_count += 1
        else:
            print(f"⚠️  Skipped {url_slug}: {message}")

print("\n" + "=" * 60)
print(f"✅ Successfully created {created_count} missing blog posts")
print("   - EXACT original content preserved")
print("   - Beautiful design elements included")
print("   - Proper URLs and navigation")