#!/usr/bin/env python3
import os
import re

# Read the original what-is-stablecoin content
with open('blog/_posts/2025-09-21-what-is-stablecoin.md', 'r') as f:
    original = f.read()

# Extract just the content part (after the front matter)
content_start = original.find('## Quick Answer')
original_content = original[content_start:] if content_start != -1 else original

# Read the current HTML template
with open('blog/what-is-stablecoin/index.html', 'r') as f:
    html_template = f.read()

# Find where to insert the content (replace the short placeholder)
# We'll replace everything between the description paragraph and Related Articles section
pattern = r'(<p class="text-lg text-gray-700 mb-6">.*?</p>)(.*?)(<h2 class="text-2xl font-bold mb-4 mt-8">Related Articles</h2>)'

# Convert markdown to HTML-ish format (keeping the original content structure)
html_content = original_content

# Basic markdown to HTML conversions while preserving content
html_content = re.sub(r'^## (.+)$', r'<h2 class="text-2xl font-bold mb-4 mt-8">\1</h2>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^### (.+)$', r'<h3 class="text-xl font-semibold mb-3">\1</h3>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:underline">\1</a>', html_content)

# Wrap lists properly
html_content = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ul class="list-disc pl-6 space-y-2 mb-6">\n' + m.group(0) + '</ul>\n', html_content)

# Add paragraph tags to standalone text
lines = html_content.split('\n')
processed_lines = []
in_list = False
for line in lines:
    if line.strip():
        if line.startswith('<h') or line.startswith('<ul') or line.startswith('</ul') or line.startswith('<li'):
            processed_lines.append(line)
            in_list = '<li' in line or '<ul' in line
        elif not in_list and not line.startswith('<'):
            processed_lines.append(f'<p class="mb-4">{line}</p>')
        else:
            processed_lines.append(line)
    else:
        processed_lines.append('')

html_content = '\n'.join(processed_lines)

# Create the new full content section
full_content_section = f'''
            <p class="text-lg text-gray-700 mb-6">
                Learn what stablecoins are, how they work, and why they're essential in crypto. Comprehensive guide covering types, examples, and real-world applications.
            </p>

{html_content}

            <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8">
                <p class="font-semibold mb-2">📊 Track Stablecoin Markets</p>
                <p>
                    Stay updated with real-time stablecoin data, yield rates, and market analysis at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Our tools help you make informed decisions in the stablecoin ecosystem.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Related Articles</h2>'''

# Replace content in the HTML
new_html = re.sub(
    r'(<p class="text-lg text-gray-700 mb-6">.*?</p>)(.*?)(<h2 class="text-2xl font-bold mb-4 mt-8">Related Articles</h2>)',
    full_content_section + r'\3',
    html_template,
    flags=re.DOTALL
)

# Write the updated file
with open('blog/what-is-stablecoin/index.html', 'w') as f:
    f.write(new_html)

print("✅ Restored full content for: What Is a Stablecoin")
print(f"   Original word count: ~{len(original_content.split())} words")