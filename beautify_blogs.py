#!/usr/bin/env python3
import os
import re
import glob

# Beautiful, modern blog template with enhanced design
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
        /* Custom styles for better typography */
        .prose h2 {{
            position: relative;
            padding-left: 1rem;
        }}
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
        .prose ul li::marker {{
            color: #6366f1;
        }}
        .prose ol li::marker {{
            color: #6366f1;
            font-weight: 600;
        }}
        .highlight-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50 border-b-2 border-indigo-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <a href="/" class="text-xl sm:text-2xl font-bold gradient-text">StableCoin Hub</a>
                    </div>
                    <div class="hidden md:block ml-6 lg:ml-10">
                        <div class="flex items-baseline space-x-4">
                            <a href="/" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">Home</a>
                            <a href="/blog/" class="text-indigo-600 bg-indigo-50 px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                            <a href="/submit/" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">Submit Tool</a>
                            <a href="/about/" class="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">About</a>
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
            <a href="/" class="text-gray-500 hover:text-indigo-600 transition-colors">
                <i class="fas fa-home"></i> Home
            </a>
            <span class="text-gray-400">/</span>
            <a href="/blog/" class="text-gray-500 hover:text-indigo-600 transition-colors">Blog</a>
            <span class="text-gray-400">/</span>
            <span class="text-gray-900 font-medium">{breadcrumb}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-10 pb-8 border-b-2 border-gray-100">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4 leading-tight">{title}</h1>
            <div class="flex flex-wrap items-center text-gray-600 text-sm gap-4">
                <span class="flex items-center">
                    <i class="fas fa-user-circle mr-2 text-indigo-500"></i>
                    StableCoin Hub Team
                </span>
                <span class="flex items-center">
                    <i class="fas fa-calendar mr-2 text-indigo-500"></i>
                    <time datetime="{date_iso}">{date}</time>
                </span>
                <span class="flex items-center">
                    <i class="fas fa-clock mr-2 text-indigo-500"></i>
                    15 min read
                </span>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
                {category_tags}
            </div>
        </header>

        <!-- Table of Contents -->
        <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 mb-8 border border-indigo-100">
            <h2 class="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <i class="fas fa-list mr-2 text-indigo-600"></i>
                Table of Contents
            </h2>
            <div id="toc" class="text-sm text-gray-700 space-y-1">
                <!-- TOC will be dynamically inserted here -->
            </div>
        </div>

        <!-- Article Content -->
        <div class="prose prose-lg max-w-none">
{content}
        </div>

        <!-- Call to Action Box -->
        <div class="highlight-box rounded-xl p-8 mt-12 text-center">
            <h2 class="text-2xl font-bold mb-4">Ready to Explore Stablecoins?</h2>
            <p class="mb-6 text-lg opacity-95">
                Join thousands of users discovering the best stablecoin platforms and tools.
            </p>
            <a href="https://www.stablecoinhub.pro" class="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105">
                Visit StableCoin Hub →
            </a>
        </div>

        <!-- Author Box -->
        <div class="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-6 mt-12 border border-gray-200">
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                        SC
                    </div>
                </div>
                <div class="ml-4">
                    <p class="font-bold text-lg mb-2">About StableCoin Hub</p>
                    <p class="text-gray-600">
                        StableCoin Hub is your comprehensive resource for discovering and comparing stablecoin tools and platforms.
                        We provide in-depth analysis, guides, and reviews to help you navigate the stablecoin ecosystem.
                    </p>
                    <div class="mt-3">
                        <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:text-indigo-700 font-medium">
                            Explore 95+ Vetted Tools →
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="bg-gradient-to-r from-gray-900 to-gray-800 text-white mt-16">
        <div class="max-w-7xl mx-auto px-4 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <div>
                    <h3 class="font-bold text-lg mb-4">StableCoin Hub</h3>
                    <p class="text-gray-400 text-sm">
                        Your trusted resource for stablecoin tools and platforms.
                    </p>
                </div>
                <div>
                    <h4 class="font-semibold mb-3">Quick Links</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="/" class="text-gray-400 hover:text-white transition-colors">Home</a></li>
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition-colors">Blog</a></li>
                        <li><a href="/about/" class="text-gray-400 hover:text-white transition-colors">About</a></li>
                        <li><a href="/submit/" class="text-gray-400 hover:text-white transition-colors">Submit Tool</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-3">Categories</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition-colors">Wallets</a></li>
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition-colors">Exchanges</a></li>
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition-colors">DeFi Protocols</a></li>
                        <li><a href="/blog/" class="text-gray-400 hover:text-white transition-colors">Yield Farming</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-3">Stay Updated</h4>
                    <p class="text-gray-400 text-sm mb-3">
                        Get the latest stablecoin news and updates.
                    </p>
                    <a href="https://www.stablecoinhub.pro" class="inline-block bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        Visit StableCoin Hub
                    </a>
                </div>
            </div>
            <div class="border-t border-gray-700 pt-8 text-center text-gray-400 text-sm">
                <p>&copy; 2025 StableCoin Hub. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Generate table of contents
        document.addEventListener('DOMContentLoaded', function() {{
            const headings = document.querySelectorAll('.prose h2');
            const toc = document.getElementById('toc');
            if (headings.length > 0 && toc) {{
                const tocList = document.createElement('ul');
                tocList.className = 'space-y-1';
                headings.forEach((heading, index) => {{
                    if (!heading.textContent.includes('Related Articles') && !heading.textContent.includes('Next Steps')) {{
                        const li = document.createElement('li');
                        const a = document.createElement('a');
                        a.href = '#section-' + index;
                        a.className = 'text-gray-600 hover:text-indigo-600 transition-colors block py-1';
                        a.innerHTML = '<i class="fas fa-chevron-right mr-2 text-xs text-indigo-400"></i>' + heading.textContent;
                        heading.id = 'section-' + index;
                        li.appendChild(a);
                        tocList.appendChild(li);
                    }}
                }});
                toc.appendChild(tocList);
            }}
        }});
    </script>
</body>
</html>"""

def process_content_beautiful(md_content):
    """Process markdown to beautiful HTML with enhanced styling"""

    # Skip the front matter
    if '---' in md_content:
        parts = md_content.split('---')
        if len(parts) >= 3:
            content = '---'.join(parts[2:]).strip()
        else:
            content = md_content
    else:
        content = md_content

    # Convert headers with enhanced styling
    content = re.sub(r'^## (.+)$', r'<h2 class="text-3xl font-bold text-gray-900 mb-6 mt-10">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3 class="text-2xl font-semibold text-gray-800 mb-4 mt-8">\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'<h4 class="text-xl font-semibold text-gray-700 mb-3 mt-6">\1</h4>', content, flags=re.MULTILINE)

    # Convert bold and italic text
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong class="text-gray-900 font-semibold">\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em class="italic">\1</em>', content)

    # Convert links with better styling
    content = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:text-indigo-700 underline decoration-2 decoration-indigo-200 hover:decoration-indigo-400 transition-all">\1</a>', content)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:text-indigo-700 underline decoration-2 decoration-indigo-200 hover:decoration-indigo-400 transition-all">\1</a>', content)

    # Process lists with enhanced styling
    lines = content.split('\n')
    processed = []
    in_ul = False
    in_ol = False
    in_table = False
    table_rows = []

    for i, line in enumerate(lines):
        # Handle unordered lists
        if line.strip().startswith('- '):
            if not in_ul:
                processed.append('<ul class="list-none space-y-3 mb-6 ml-4">')
                in_ul = True
            item_content = line.strip()[2:]
            processed.append(f'''<li class="flex items-start">
                <span class="text-indigo-500 mr-3 mt-1">
                    <i class="fas fa-check-circle"></i>
                </span>
                <span class="text-gray-700">{item_content}</span>
            </li>''')

        # Handle ordered lists
        elif re.match(r'^\d+\.\s+', line.strip()):
            if not in_ol:
                if in_ul:
                    processed.append('</ul>')
                    in_ul = False
                processed.append('<ol class="list-none space-y-3 mb-6 ml-4 counter-reset-list">')
                in_ol = True
            content_text = re.sub(r'^\d+\.\s+', '', line.strip())
            list_num = re.match(r'^(\d+)\.', line.strip()).group(1)
            processed.append(f'''<li class="flex items-start">
                <span class="bg-indigo-600 text-white rounded-full w-7 h-7 flex items-center justify-center mr-3 text-sm font-bold flex-shrink-0">
                    {list_num}
                </span>
                <span class="text-gray-700">{content_text}</span>
            </li>''')

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
                    table_rows = []
                    processed.append('<div class="overflow-x-auto mb-8">')
                    processed.append('<table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg overflow-hidden">')

                if '---' in line:
                    continue  # Skip separator

                cells = [c.strip() for c in line.split('|')[1:-1]]

                # Check if header row
                if any('**' in cell or 'Type' in cell or 'Feature' in cell or 'Stablecoin' in cell for cell in cells):
                    processed.append('<thead class="bg-gradient-to-r from-indigo-50 to-purple-50">')
                    processed.append('<tr>')
                    for cell in cells:
                        cell = cell.replace('**', '')
                        processed.append(f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">{cell}</th>')
                    processed.append('</tr>')
                    processed.append('</thead>')
                    processed.append('<tbody class="bg-white divide-y divide-gray-200">')
                else:
                    # Data row
                    processed.append('<tr class="hover:bg-gray-50 transition-colors">')
                    for j, cell in enumerate(cells):
                        if j == 0:  # First column often has important info
                            processed.append(f'<td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{cell}</td>')
                        else:
                            processed.append(f'<td class="px-6 py-4 whitespace-nowrap text-gray-600">{cell}</td>')
                    processed.append('</tr>')

            elif in_table and not line.strip().startswith('|'):
                # End of table
                processed.append('</tbody>')
                processed.append('</table>')
                processed.append('</div>')
                in_table = False

                # Process the current line
                if line.strip() and not line.startswith('<'):
                    processed.append(f'<p class="text-gray-700 leading-relaxed mb-4">{line}</p>')
                else:
                    processed.append(line)
            elif line.strip() and not line.startswith('<'):
                # Regular paragraph with better styling
                processed.append(f'<p class="text-gray-700 leading-relaxed mb-4">{line}</p>')
            else:
                processed.append(line)

    # Close any remaining open elements
    if in_ul:
        processed.append('</ul>')
    if in_ol:
        processed.append('</ol>')
    if in_table:
        processed.append('</tbody>')
        processed.append('</table>')
        processed.append('</div>')

    return '\n'.join(processed)

def beautify_blog_post(md_file):
    """Beautify a single blog post"""
    # Get URL slug from filename
    filename = os.path.basename(md_file)
    url_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    html_file = f'blog/{url_slug}/index.html'
    if not os.path.exists(html_file):
        return False, f"HTML file not found: {html_file}"

    # Read original markdown
    with open(md_file, 'r') as f:
        original_md = f.read()

    # Extract metadata
    title_match = re.search(r'title:\s*"([^"]+)"', original_md)
    desc_match = re.search(r'description:\s*"([^"]+)"', original_md)

    if not title_match:
        return False, "No title found"

    title = title_match.group(1)
    description = desc_match.group(1) if desc_match else "Comprehensive guide for the stablecoin ecosystem."

    # Get date from filename
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if date_match:
        year, month, day = date_match.groups()
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        date_str = f"{months[int(month)]} {int(day)}, {year}"
        date_iso = f"{year}-{month}-{day}"
    else:
        date_str = "September 2025"
        date_iso = "2025-09-01"

    # Process content with beautiful styling
    html_content = process_content_beautiful(original_md)

    # Add colorful info boxes throughout content
    sections = html_content.split('<h2')
    if len(sections) > 3:
        # Add first box after 3rd section
        box1 = '''
            <div class="bg-gradient-to-r from-indigo-50 to-purple-50 border-l-4 border-indigo-600 p-6 my-8 rounded-r-lg">
                <p class="font-bold text-lg mb-2 text-indigo-900">
                    <i class="fas fa-chart-line mr-2"></i>
                    Track Real-Time Stablecoin Data
                </p>
                <p class="text-gray-700">
                    Monitor market caps, yields, and trends across 95+ platforms at
                    <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:text-indigo-700 font-semibold">StableCoinHub.pro</a>.
                    Make informed decisions with comprehensive analytics.
                </p>
            </div>

            <h2'''
        sections[3] = box1 + sections[3]

    if len(sections) > 6:
        # Add second box after 6th section
        box2 = '''
            <div class="bg-gradient-to-r from-purple-50 to-pink-50 border-l-4 border-purple-600 p-6 my-8 rounded-r-lg">
                <p class="font-bold text-lg mb-2 text-purple-900">
                    <i class="fas fa-shield-alt mr-2"></i>
                    Find Trusted Stablecoin Platforms
                </p>
                <p class="text-gray-700">
                    Compare security features, fees, and user reviews at
                    <a href="https://www.stablecoinhub.pro" class="text-purple-600 hover:text-purple-700 font-semibold">StableCoinHub.pro</a>.
                    Our vetted directory helps you choose the right platform.
                </p>
            </div>

            <h2'''
        sections[6] = box2 + sections[6]

    html_content = '<h2'.join(sections)

    # Add Related Articles section (only once!)
    related_articles = '''
            <div class="mt-16 mb-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Related Articles</h2>
                <p class="text-gray-600 mb-8">Continue your learning journey with these related guides:</p>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <a href="/blog/best-stablecoin-wallets/" class="group">
                        <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 border border-gray-100 h-full">
                            <div class="text-indigo-600 mb-3">
                                <i class="fas fa-wallet text-2xl"></i>
                            </div>
                            <h3 class="font-bold text-lg text-gray-900 group-hover:text-indigo-600 transition-colors mb-2">
                                Best Stablecoin Wallets 2025
                            </h3>
                            <p class="text-gray-600 text-sm">
                                Security features, fees, and user experience compared
                            </p>
                            <span class="text-indigo-600 text-sm font-medium mt-3 inline-block group-hover:translate-x-1 transition-transform">
                                Read more →
                            </span>
                        </div>
                    </a>

                    <a href="/blog/how-to-buy-stablecoins/" class="group">
                        <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 border border-gray-100 h-full">
                            <div class="text-green-600 mb-3">
                                <i class="fas fa-shopping-cart text-2xl"></i>
                            </div>
                            <h3 class="font-bold text-lg text-gray-900 group-hover:text-green-600 transition-colors mb-2">
                                How to Buy Stablecoins
                            </h3>
                            <p class="text-gray-600 text-sm">
                                Step-by-step guide for beginners
                            </p>
                            <span class="text-green-600 text-sm font-medium mt-3 inline-block group-hover:translate-x-1 transition-transform">
                                Read more →
                            </span>
                        </div>
                    </a>

                    <a href="/blog/stablecoin-comparison/" class="group">
                        <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 border border-gray-100 h-full">
                            <div class="text-purple-600 mb-3">
                                <i class="fas fa-balance-scale text-2xl"></i>
                            </div>
                            <h3 class="font-bold text-lg text-gray-900 group-hover:text-purple-600 transition-colors mb-2">
                                Stablecoin Comparison 2025
                            </h3>
                            <p class="text-gray-600 text-sm">
                                USDT vs USDC vs DAI and more
                            </p>
                            <span class="text-purple-600 text-sm font-medium mt-3 inline-block group-hover:translate-x-1 transition-transform">
                                Read more →
                            </span>
                        </div>
                    </a>
                </div>
            </div>
'''

    html_content += related_articles

    # Determine categories based on content
    categories = ['Stablecoins']
    if 'wallet' in url_slug.lower():
        categories.append('Wallets')
    elif 'defi' in url_slug.lower() or 'yield' in url_slug.lower():
        categories.append('DeFi')
    elif 'exchange' in url_slug.lower() or 'trading' in url_slug.lower():
        categories.append('Trading')
    elif 'regulation' in url_slug.lower() or 'tax' in url_slug.lower():
        categories.append('Legal')
    else:
        categories.append('Guide')

    # Create colorful category tags
    colors = ['indigo', 'purple', 'green', 'blue', 'pink']
    category_tags = ' '.join([
        f'<span class="bg-{colors[i % len(colors)]}-100 text-{colors[i % len(colors)]}-700 px-3 py-1 rounded-full text-sm font-medium">{cat}</span>'
        for i, cat in enumerate(categories)
    ])

    # Create final HTML
    final_html = BLOG_TEMPLATE.format(
        title=title,
        description=description,
        url=url_slug,
        breadcrumb=title.split(':')[0] if ':' in title else title[:30] + '...' if len(title) > 30 else title,
        date=date_str,
        date_iso=date_iso,
        category_tags=category_tags,
        content=html_content
    )

    # Write the beautified file
    with open(html_file, 'w') as f:
        f.write(final_html)

    return True, "Beautified"

# Main execution
print("Beautifying ALL blog posts with enhanced design...")
print("=" * 60)

# Get all markdown files
md_files = glob.glob('blog/_posts/*.md')
print(f"Found {len(md_files)} blog posts to beautify\n")

success_count = 0
for md_file in sorted(md_files):
    filename = os.path.basename(md_file)
    url_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    success, message = beautify_blog_post(md_file)
    if success:
        print(f"✅ Beautified: {url_slug}")
        success_count += 1
    else:
        print(f"⚠️  Skipped {url_slug}: {message}")

print("\n" + "=" * 60)
print(f"✅ Successfully beautified {success_count}/{len(md_files)} blog posts")
print("   - NO duplicate headers")
print("   - Enhanced typography (H1, H2, H3 with visual hierarchy)")
print("   - Beautiful colors and gradients")
print("   - Styled bullet points and numbered lists")
print("   - Interactive table of contents")
print("   - Colorful info boxes")
print("   - Modern card-based related articles")