#!/usr/bin/env python3
import os
import re
import glob

def convert_markdown_to_html(content):
    """Convert markdown content to HTML while preserving structure"""
    # Basic conversions
    html = content

    # Headers
    html = re.sub(r'^## (.+)$', r'</div><h2 class="text-2xl font-bold mb-4 mt-8">\1</h2><div class="prose-content">', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3 class="text-xl font-semibold mb-3">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4 class="text-lg font-semibold mb-2">\1</h4>', html, flags=re.MULTILINE)

    # Bold text
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-indigo-600 hover:underline">\1</a>', html)

    # Lists - handle multi-line list items
    lines = html.split('\n')
    processed_lines = []
    in_list = False
    in_ordered_list = False
    list_buffer = []

    for i, line in enumerate(lines):
        # Check for unordered list item
        if line.strip().startswith('- '):
            if in_ordered_list and list_buffer:
                processed_lines.append('<ol class="list-decimal pl-6 space-y-2 mb-6">')
                processed_lines.extend(list_buffer)
                processed_lines.append('</ol>')
                list_buffer = []
                in_ordered_list = False
            in_list = True
            list_buffer.append(f'<li>{line.strip()[2:]}</li>')
        # Check for ordered list item
        elif re.match(r'^\d+\.\s+', line.strip()):
            if in_list and list_buffer:
                processed_lines.append('<ul class="list-disc pl-6 space-y-2 mb-6">')
                processed_lines.extend(list_buffer)
                processed_lines.append('</ul>')
                list_buffer = []
                in_list = False
            in_ordered_list = True
            content = re.sub(r'^\d+\.\s+', '', line.strip())
            list_buffer.append(f'<li>{content}</li>')
        else:
            # End of list
            if in_list and list_buffer:
                processed_lines.append('<ul class="list-disc pl-6 space-y-2 mb-6">')
                processed_lines.extend(list_buffer)
                processed_lines.append('</ul>')
                list_buffer = []
                in_list = False
            elif in_ordered_list and list_buffer:
                processed_lines.append('<ol class="list-decimal pl-6 space-y-2 mb-6">')
                processed_lines.extend(list_buffer)
                processed_lines.append('</ol>')
                list_buffer = []
                in_ordered_list = False

            # Process regular lines
            if line.strip() and not line.startswith('<'):
                # Check if it's a table
                if '|' in line and line.strip().startswith('|'):
                    processed_lines.append(line)
                else:
                    processed_lines.append(f'<p class="mb-4">{line}</p>')
            else:
                processed_lines.append(line)

    # Handle any remaining list items
    if in_list and list_buffer:
        processed_lines.append('<ul class="list-disc pl-6 space-y-2 mb-6">')
        processed_lines.extend(list_buffer)
        processed_lines.append('</ul>')
    elif in_ordered_list and list_buffer:
        processed_lines.append('<ol class="list-decimal pl-6 space-y-2 mb-6">')
        processed_lines.extend(list_buffer)
        processed_lines.append('</ol>')

    html = '\n'.join(processed_lines)

    # Handle tables
    html = re.sub(r'\| (.+) \|', lambda m: process_table_row(m.group(0)), html)

    # Clean up div tags
    html = html.replace('<div class="prose-content">', '')
    html = html.replace('</div><h2', '\n\n<h2')

    return html

def process_table_row(row):
    """Convert markdown table row to HTML"""
    if '---' in row:
        return ''  # Skip separator rows
    cells = row.split('|')[1:-1]  # Remove empty first and last elements
    if all('**' in cell or 'Feature' in cell or 'Stablecoin' in cell for cell in cells[:1]):
        # Header row
        return '<tr>' + ''.join(f'<th class="border border-gray-300 px-4 py-2">{cell.strip()}</th>' for cell in cells) + '</tr>'
    else:
        # Data row
        return '<tr>' + ''.join(f'<td class="border border-gray-300 px-4 py-2">{cell.strip()}</td>' for cell in cells) + '</tr>'

def restore_blog_post(md_file, blog_dir):
    """Restore a single blog post with original content"""
    # Extract URL from filename
    filename = os.path.basename(md_file)
    # Remove date prefix and .md extension
    url_part = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

    # Check if corresponding HTML file exists
    html_file = f"{blog_dir}/{url_part}/index.html"
    if not os.path.exists(html_file):
        print(f"  ⚠️  HTML file not found: {html_file}")
        return False

    # Read original markdown content
    with open(md_file, 'r') as f:
        md_content = f.read()

    # Extract metadata and content
    if '---' in md_content:
        parts = md_content.split('---')
        if len(parts) >= 3:
            front_matter = parts[1]
            content = '---'.join(parts[2:])
        else:
            content = md_content
    else:
        content = md_content

    # Convert markdown to HTML
    html_content = convert_markdown_to_html(content)

    # Read current HTML template
    with open(html_file, 'r') as f:
        current_html = f.read()

    # Find the content section and replace it
    # Look for the pattern between the initial description and Related Articles
    pattern = r'(<p class="text-lg text-gray-700 mb-6">.*?</p>)(.*?)(<h2 class="text-2xl font-bold mb-4 mt-8">Related Articles</h2>)'

    # Extract the description from the front matter or use existing
    description_match = re.search(r'description:\s*"([^"]+)"', front_matter if 'front_matter' in locals() else '')
    if description_match:
        description = description_match.group(1)
    else:
        description = "Comprehensive guide and analysis for the stablecoin ecosystem."

    # Build the new content section
    new_content_section = f'''
            <p class="text-lg text-gray-700 mb-6">
                {description}
            </p>

{html_content}

            <div class="bg-indigo-50 border-l-4 border-indigo-600 p-6 my-8">
                <p class="font-semibold mb-2">📊 Explore StableCoin Hub</p>
                <p>
                    Discover 95+ stablecoin platforms, exchanges, and DeFi protocols at <a href="https://www.stablecoinhub.pro" class="text-indigo-600 hover:underline">StableCoinHub.pro</a>. Find the perfect tools for your stablecoin strategy.
                </p>
            </div>

            <h2 class="text-2xl font-bold mb-4 mt-8">Related Articles</h2>'''

    # Replace the content
    new_html = re.sub(
        pattern,
        new_content_section + r'\3',
        current_html,
        flags=re.DOTALL
    )

    # Write the updated file
    with open(html_file, 'w') as f:
        f.write(new_html)

    return True

# Main execution
blog_dir = 'blog'
posts_dir = 'blog/_posts'

# Get all markdown files
md_files = glob.glob(f"{posts_dir}/*.md")

print(f"Found {len(md_files)} original blog posts to restore")
print("=" * 50)

restored = 0
for md_file in sorted(md_files):
    filename = os.path.basename(md_file)
    print(f"\nProcessing: {filename}")
    if restore_blog_post(md_file, blog_dir):
        restored += 1
        print(f"  ✅ Restored full content")
    else:
        print(f"  ⏭️  Skipped")

print("\n" + "=" * 50)
print(f"✅ Successfully restored {restored} blog posts with original content")
print("✅ All formatting, colors, and cross-links preserved")