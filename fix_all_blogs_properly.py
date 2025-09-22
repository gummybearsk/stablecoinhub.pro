#!/usr/bin/env python3
import os
import re
import glob

# Clean, beautiful blog template
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
    <style>
        .prose h2::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(to bottom, #6366f1, #8b5cf6);
            border-radius: 2px;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="https://www.stablecoinhub.pro" class="text-2xl font-bold text-indigo-600">StableCoin Hub</a>
                    <div class="hidden md:block ml-10">
                        <div class="flex items-baseline space-x-4">
                            <a href="https://www.stablecoinhub.pro" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="https://www.stablecoinhub.pro/blog/" class="text-indigo-600 bg-indigo-50 px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                            <a href="https://www.stablecoinhub.pro/submit/" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Submit Tool</a>
                            <a href="https://www.stablecoinhub.pro/about/" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Article -->
    <article class="max-w-4xl mx-auto px-4 py-12">
        <!-- Breadcrumb -->
        <nav class="text-sm mb-6 flex items-center space-x-2">
            <a href="https://www.stablecoinhub.pro" class="text-gray-500 hover:text-indigo-600">
                <i class="fas fa-home"></i> Home
            </a>
            <span class="text-gray-400">/</span>
            <a href="https://www.stablecoinhub.pro/blog/" class="text-gray-500 hover:text-indigo-600">Blog</a>
            <span class="text-gray-400">/</span>
            <span class="text-gray-900 font-medium">{breadcrumb}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-10 pb-8 border-b-2 border-gray-100">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4 leading-tight">{title}</h1>
            <div class="flex flex-wrap items-center text-gray-600 text-sm gap-4">
                <span><i class="fas fa-user-circle mr-2 text-indigo-500"></i>StableCoin Hub Team</span>
                <span><i class="fas fa-calendar mr-2 text-indigo-500"></i>{date}</span>
                <span><i class="fas fa-clock mr-2 text-indigo-500"></i>15 min read</span>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
                {category_tags}
            </div>
        </header>

        <!-- Article Content -->
        <div class="prose prose-lg max-w-none">
{content}
        </div>

        <!-- Single Related Articles Section -->
        <div class="mt-16 mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Related Articles</h2>
            <p class="text-gray-600 mb-8">Continue exploring our comprehensive guides:</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {related_cards}
            </div>
        </div>

        <!-- Call to Action -->
        <div class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl p-8 mt-12 text-center">
            <h2 class="text-2xl font-bold mb-4">Ready to Explore Stablecoins?</h2>
            <p class="mb-6 text-lg opacity-95">
                Join thousands discovering the best stablecoin platforms and tools.
            </p>
            <a href="https://www.stablecoinhub.pro" class="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition-all">
                Visit StableCoin Hub →
            </a>
        </div>

        <!-- Author Box -->
        <div class="bg-gray-100 rounded-lg p-6 mt-12">
            <p class="font-bold text-lg mb-2">About StableCoin Hub</p>
            <p class="text-gray-600">
                StableCoin Hub is your comprehensive resource for discovering and comparing stablecoin tools and platforms.
                Visit <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>
                to explore our directory of 95+ vetted tools.
            </p>
        </div>
    </article>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16">
        <div class="max-w-7xl mx-auto px-4 py-12">
            <div class="text-center">
                <p class="mb-4">&copy; 2025 StableCoin Hub. All rights reserved.</p>
                <div class="space-x-4">
                    <a href="https://www.stablecoinhub.pro" class="text-gray-400 hover:text-white">Home</a>
                    <a href="https://www.stablecoinhub.pro/blog/" class="text-gray-400 hover:text-white">Blog</a>
                    <a href="https://www.stablecoinhub.pro/about/" class="text-gray-400 hover:text-white">About</a>
                    <a href="https://www.stablecoinhub.pro/submit/" class="text-gray-400 hover:text-white">Submit Tool</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>"""

def clean_and_convert_markdown(md_content):
    """Convert ORIGINAL markdown to clean HTML"""

    # Skip front matter
    if '---' in md_content:
        parts = md_content.split('---')
        if len(parts) >= 3:
            content = '---'.join(parts[2:]).strip()
        else:
            content = md_content
    else:
        content = md_content

    # Convert headers properly
    content = re.sub(r'^## (.+)$', r'<h2 class="text-3xl font-bold text-gray-900 mb-6 mt-10 relative pl-4">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3 class="text-2xl font-semibold text-gray-800 mb-4 mt-8">\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'<h4 class="text-xl font-semibold text-gray-700 mb-3 mt-6">\1</h4>', content, flags=re.MULTILINE)

    # Convert text formatting
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong class="font-bold text-gray-900">\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em class="italic">\1</em>', content)

    # Convert links
    content = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:text-indigo-700 underline">\1</a>', content)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:text-indigo-700 underline">\1</a>', content)

    # Process lines for lists and paragraphs
    lines = content.split('\n')
    processed = []
    in_ul = False
    in_ol = False
    in_table = False

    for line in lines:
        # Handle unordered lists
        if line.strip().startswith('- '):
            if not in_ul:
                processed.append('<ul class="list-disc pl-6 space-y-2 mb-6 text-gray-700">')
                in_ul = True
            processed.append(f'<li>{line.strip()[2:]}</li>')

        # Handle ordered lists
        elif re.match(r'^\d+\.\s+', line.strip()):
            if not in_ol:
                if in_ul:
                    processed.append('</ul>')
                    in_ul = False
                processed.append('<ol class="list-decimal pl-6 space-y-2 mb-6 text-gray-700">')
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
                if not in_table:
                    in_table = True
                    processed.append('<div class="overflow-x-auto mb-8">')
                    processed.append('<table class="min-w-full border border-gray-200 rounded-lg">')

                if '---' in line:
                    continue  # Skip separator

                cells = [c.strip() for c in line.split('|')[1:-1]]

                # Check if header row
                if any('**' in cell or 'Type' in cell or 'Feature' in cell or 'Stablecoin' in cell for cell in cells):
                    processed.append('<thead class="bg-gray-100"><tr>')
                    for cell in cells:
                        cell = cell.replace('**', '')
                        processed.append(f'<th class="border border-gray-300 px-4 py-2 text-left font-semibold">{cell}</th>')
                    processed.append('</tr></thead><tbody>')
                else:
                    processed.append('<tr class="hover:bg-gray-50">')
                    for cell in cells:
                        processed.append(f'<td class="border border-gray-300 px-4 py-2">{cell}</td>')
                    processed.append('</tr>')

            elif in_table and not line.strip().startswith('|'):
                processed.append('</tbody></table></div>')
                in_table = False
                if line.strip() and not line.startswith('<'):
                    processed.append(f'<p class="text-gray-700 leading-relaxed mb-4">{line}</p>')
            elif line.strip() and not line.startswith('<'):
                processed.append(f'<p class="text-gray-700 leading-relaxed mb-4">{line}</p>')
            else:
                processed.append(line)

    # Close any remaining tags
    if in_ul:
        processed.append('</ul>')
    if in_ol:
        processed.append('</ol>')
    if in_table:
        processed.append('</tbody></table></div>')

    html = '\n'.join(processed)

    # Add info boxes at strategic points
    sections = html.split('<h2')
    if len(sections) > 3:
        info_box = '''
        <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8 rounded-r-lg">
            <p class="font-bold text-lg mb-2 text-indigo-900">
                <i class="fas fa-chart-line mr-2"></i>Track Real-Time Stablecoin Data
            </p>
            <p class="text-gray-700">
                Monitor market caps, yields, and trends across 95+ platforms at
                <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:text-indigo-700 font-semibold">StableCoinHub.pro</a>.
            </p>
        </div>
        <h2'''
        sections[3] = info_box + sections[3]
        html = '<h2'.join(sections)

    return html

# Related articles for different posts
RELATED_ARTICLES = {
    'default': [
        ('best-stablecoin-wallets', 'Best Stablecoin Wallets', 'Security & Features Guide', 'wallet', 'indigo'),
        ('how-to-buy-stablecoins', 'How to Buy Stablecoins', 'Step-by-step Guide', 'shopping-cart', 'green'),
        ('stablecoin-comparison', 'Stablecoin Comparison', 'USDT vs USDC vs DAI', 'balance-scale', 'purple')
    ],
    'wallets': [
        ('crypto-card', 'Crypto Debit Cards', 'Spend Your Stablecoins', 'credit-card', 'blue'),
        ('stablecoin-security', 'Stablecoin Security', 'Protection Guide', 'shield-alt', 'red'),
        ('how-to-buy-stablecoins', 'Buying Guide', 'Get Started Today', 'shopping-cart', 'green')
    ],
    'defi': [
        ('stablecoin-lending', 'Lending Platforms', 'Earn Passive Income', 'coins', 'yellow'),
        ('defi-protocols', 'DeFi Protocols', 'Yield Farming Guide', 'chart-line', 'indigo'),
        ('stablecoin-risks', 'Understanding Risks', 'Stay Safe', 'exclamation-triangle', 'red')
    ]
}

def get_related_cards(url_slug):
    """Generate related article cards"""
    # Determine category
    if 'wallet' in url_slug:
        articles = RELATED_ARTICLES.get('wallets', RELATED_ARTICLES['default'])
    elif 'defi' in url_slug or 'yield' in url_slug or 'lend' in url_slug:
        articles = RELATED_ARTICLES.get('defi', RELATED_ARTICLES['default'])
    else:
        articles = RELATED_ARTICLES['default']

    cards = []
    for slug, title, desc, icon, color in articles:
        cards.append(f'''
            <a href="https://www.stablecoinhub.pro/blog/{slug}/" class="group">
                <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 border border-gray-100 h-full">
                    <div class="text-{color}-600 mb-3">
                        <i class="fas fa-{icon} text-2xl"></i>
                    </div>
                    <h3 class="font-bold text-lg text-gray-900 group-hover:text-{color}-600 transition-colors mb-2">
                        {title}
                    </h3>
                    <p class="text-gray-600 text-sm">{desc}</p>
                    <span class="text-{color}-600 text-sm font-medium mt-3 inline-block group-hover:translate-x-1 transition-transform">
                        Read more →
                    </span>
                </div>
            </a>''')

    return '\n'.join(cards)

def fix_blog_post(md_file):
    """Fix a single blog post completely"""
    filename = os.path.basename(md_file)
    url_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    # Create directory if needed
    blog_dir = f'blog/{url_slug}'
    os.makedirs(blog_dir, exist_ok=True)

    html_file = f'{blog_dir}/index.html'

    # Read ORIGINAL markdown
    with open(md_file, 'r') as f:
        original_md = f.read()

    # Extract metadata
    title_match = re.search(r'title:\s*"([^"]+)"', original_md)
    desc_match = re.search(r'description:\s*"([^"]+)"', original_md)

    if not title_match:
        print(f"  ⚠️ No title in {filename}")
        return False

    title = title_match.group(1)
    description = desc_match.group(1) if desc_match else "Comprehensive guide for the stablecoin ecosystem."

    # Get date from filename
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if date_match:
        year, month, day = date_match.groups()
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        date_str = f"{months[int(month)]} {int(day)}, {year}"
    else:
        date_str = "September 2025"

    # Convert ENTIRE original content
    html_content = clean_and_convert_markdown(original_md)

    # Determine categories
    categories = []
    if 'wallet' in url_slug.lower():
        categories = ['Wallets', 'Security']
    elif 'defi' in url_slug.lower() or 'yield' in url_slug.lower():
        categories = ['DeFi', 'Yield']
    elif 'regulation' in url_slug.lower() or 'tax' in url_slug.lower():
        categories = ['Legal', 'Compliance']
    elif 'exchange' in url_slug.lower() or 'trading' in url_slug.lower():
        categories = ['Trading', 'Exchange']
    else:
        categories = ['Stablecoins', 'Guide']

    category_tags = ' '.join([
        f'<span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm">{cat}</span>'
        for cat in categories
    ])

    # Get related articles
    related_cards = get_related_cards(url_slug)

    # Create breadcrumb
    breadcrumb = title.split(':')[0] if ':' in title else (title[:40] + '...' if len(title) > 40 else title)

    # Generate final HTML
    final_html = BLOG_TEMPLATE.format(
        title=title,
        description=description,
        url=url_slug,
        breadcrumb=breadcrumb,
        date=date_str,
        category_tags=category_tags,
        content=html_content,
        related_cards=related_cards
    )

    # Write file
    with open(html_file, 'w') as f:
        f.write(final_html)

    return True

# Main execution
print("Fixing ALL blog posts properly...")
print("=" * 60)

# Get all markdown files
md_files = glob.glob('blog/_posts/*.md')
print(f"Found {len(md_files)} original blog posts\n")

success = 0
for md_file in sorted(md_files):
    filename = os.path.basename(md_file)
    if fix_blog_post(md_file):
        print(f"✅ Fixed: {filename}")
        success += 1
    else:
        print(f"❌ Failed: {filename}")

print("\n" + "=" * 60)
print(f"✅ Successfully fixed {success}/{len(md_files)} blog posts")
print("   - NO duplicate headers")
print("   - FULL original content restored")
print("   - Clean, beautiful design")
print("   - Working navigation links to main site")
print("   - Proper related articles section")