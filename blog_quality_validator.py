#!/usr/bin/env python3
"""
Blog Quality Validator - Ensures all blog posts meet minimum quality standards.
This prevents short, duplicate, or low-quality content from being published.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Quality Standards
MIN_WORD_COUNT = 2500  # Minimum words per blog
MIN_LINE_COUNT = 300   # Minimum lines of HTML
MIN_PARAGRAPHS = 15    # Minimum content paragraphs
MIN_HEADERS = 5        # Minimum section headers (h2, h3, h4)
MAX_DUPLICATE_CONTENT = 0.15  # Maximum 15% duplicate content between blogs

class BlogQualityValidator:
    def __init__(self, blog_dir: str = "blog"):
        self.blog_dir = Path(blog_dir)
        self.errors = []
        self.warnings = []
        self.blog_contents = {}

    def validate_all_blogs(self) -> bool:
        """Validate all blog posts in the directory."""
        print("🔍 Starting Blog Quality Validation...")
        print("=" * 60)

        all_valid = True
        blog_dirs = [d for d in self.blog_dir.iterdir() if d.is_dir()]

        # First, load all blog contents for duplicate checking
        for blog_dir in blog_dirs:
            index_file = blog_dir / "index.html"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.blog_contents[blog_dir.name] = f.read()

        # Now validate each blog
        for blog_dir in sorted(blog_dirs):
            index_file = blog_dir / "index.html"
            if index_file.exists():
                print(f"\n📝 Validating: {blog_dir.name}")
                if not self.validate_single_blog(index_file, blog_dir.name):
                    all_valid = False

        # Check for duplicate content across blogs
        print(f"\n🔄 Checking for duplicate content across {len(self.blog_contents)} blogs...")
        self.check_duplicate_content()

        # Summary
        print("\n" + "=" * 60)
        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} errors found")
            for error in self.errors:
                print(f"   • {error}")
        else:
            print("✅ All blogs pass quality validation!")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")

        return all_valid and len(self.errors) == 0

    def validate_single_blog(self, file_path: Path, blog_name: str) -> bool:
        """Validate a single blog post."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract text content (remove HTML tags for word count)
        text_content = self.extract_text(content)

        # Check word count
        word_count = len(text_content.split())
        line_count = len(content.splitlines())

        # Count content elements
        paragraphs = len(re.findall(r'<p[^>]*>.*?</p>', content, re.DOTALL))
        headers = len(re.findall(r'<h[234][^>]*>.*?</h[234]>', content, re.DOTALL))

        # Validation checks
        is_valid = True

        if word_count < MIN_WORD_COUNT:
            self.errors.append(f"{blog_name}: Only {word_count} words (minimum: {MIN_WORD_COUNT})")
            is_valid = False

        if line_count < MIN_LINE_COUNT:
            self.errors.append(f"{blog_name}: Only {line_count} lines (minimum: {MIN_LINE_COUNT})")
            is_valid = False

        if paragraphs < MIN_PARAGRAPHS:
            self.warnings.append(f"{blog_name}: Only {paragraphs} paragraphs (recommended: {MIN_PARAGRAPHS}+)")

        if headers < MIN_HEADERS:
            self.warnings.append(f"{blog_name}: Only {headers} section headers (recommended: {MIN_HEADERS}+)")

        # Check for placeholder content
        if "Content will be added here" in content or "This article provides expert insights" in content:
            self.errors.append(f"{blog_name}: Contains placeholder content!")
            is_valid = False

        # Check for proper meta tags
        if not re.search(r'<meta name="description"[^>]*content="[^"]{50,}"', content):
            self.warnings.append(f"{blog_name}: Meta description too short or missing")

        if not re.search(r'<link rel="canonical"', content):
            self.errors.append(f"{blog_name}: Missing canonical URL")
            is_valid = False

        # Display stats
        status = "✅" if is_valid else "❌"
        print(f"   {status} Words: {word_count:,} | Lines: {line_count} | Paragraphs: {paragraphs} | Headers: {headers}")

        return is_valid

    def extract_text(self, html: str) -> str:
        """Extract text content from HTML."""
        # Remove script and style elements
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        # Remove HTML tags
        html = re.sub(r'<[^>]+>', ' ', html)
        # Remove extra whitespace
        html = ' '.join(html.split())
        return html

    def check_duplicate_content(self):
        """Check for duplicate content between blogs."""
        blog_names = list(self.blog_contents.keys())

        for i, blog1 in enumerate(blog_names):
            for blog2 in blog_names[i+1:]:
                similarity = self.calculate_similarity(
                    self.blog_contents[blog1],
                    self.blog_contents[blog2]
                )

                if similarity > MAX_DUPLICATE_CONTENT:
                    self.errors.append(
                        f"High duplicate content ({similarity:.1%}) between {blog1} and {blog2}"
                    )

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        # Extract meaningful content blocks
        blocks1 = set(re.findall(r'<p[^>]*>(.*?)</p>', text1, re.DOTALL))
        blocks2 = set(re.findall(r'<p[^>]*>(.*?)</p>', text2, re.DOTALL))

        if not blocks1 or not blocks2:
            return 0.0

        # Calculate Jaccard similarity
        intersection = blocks1.intersection(blocks2)
        union = blocks1.union(blocks2)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def fix_short_blogs(self) -> List[str]:
        """Return list of blogs that need fixing."""
        short_blogs = []

        for blog_dir in self.blog_dir.iterdir():
            if blog_dir.is_dir():
                index_file = blog_dir / "index.html"
                if index_file.exists():
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    text_content = self.extract_text(content)
                    word_count = len(text_content.split())

                    if word_count < MIN_WORD_COUNT:
                        short_blogs.append(blog_dir.name)

        return short_blogs


def create_blog_validator_hook():
    """Create a pre-commit hook to validate blogs before committing."""

    hook_content = '''#!/bin/bash
# Pre-commit hook to validate blog quality

echo "🔍 Running blog quality validation..."

# Run the validator
python blog_quality_validator.py

# Check exit code
if [ $? -ne 0 ]; then
    echo "❌ Blog validation failed! Fix the issues before committing."
    exit 1
fi

echo "✅ Blog validation passed!"
exit 0
'''

    # Create .git/hooks directory if it doesn't exist
    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Write pre-commit hook
    hook_file = hooks_dir / "pre-commit"
    with open(hook_file, 'w') as f:
        f.write(hook_content)

    # Make it executable
    os.chmod(hook_file, 0o755)
    print("✅ Created pre-commit hook for blog validation")


def integrate_with_auto_publish():
    """Update the auto-publish script to include quality checks."""

    publish_script = Path(".github/scripts/publish_scheduled_blogs.py")

    if publish_script.exists():
        with open(publish_script, 'r') as f:
            content = f.read()

        # Add quality validation import and check
        if "BlogQualityValidator" not in content:
            validation_code = '''
# Import blog quality validator
sys.path.insert(0, str(Path(__file__).parent.parent))
from blog_quality_validator import BlogQualityValidator

def validate_blog_quality(blog_path):
    """Validate blog quality before publishing."""
    validator = BlogQualityValidator()
    blog_name = Path(blog_path).parent.name

    if not validator.validate_single_blog(Path(blog_path), blog_name):
        print(f"❌ Blog {blog_name} failed quality validation!")
        print(f"   Errors: {validator.errors}")
        return False
    return True
'''

            # Insert after imports
            lines = content.splitlines()
            import_end = 0
            for i, line in enumerate(lines):
                if line.startswith("import") or line.startswith("from"):
                    import_end = i + 1

            lines.insert(import_end, validation_code)

            # Also add validation check before publishing
            publish_check = '''
                # Validate blog quality before publishing
                blog_path = f"blog/{blog['url']}/index.html"
                if not validate_blog_quality(blog_path):
                    print(f"⚠️  Skipping {blog['url']} due to quality issues")
                    continue
'''

            # Find where blogs are published and add check
            for i, line in enumerate(lines):
                if "update_blog_index" in line or "publish" in line.lower():
                    lines.insert(i, publish_check)
                    break

            # Write updated script
            with open(publish_script, 'w') as f:
                f.write('\n'.join(lines))

            print("✅ Updated auto-publish script with quality validation")


def main():
    """Main function to run validation and setup."""
    validator = BlogQualityValidator()

    # Run validation
    is_valid = validator.validate_all_blogs()

    # Get list of short blogs
    short_blogs = validator.fix_short_blogs()

    if short_blogs:
        print(f"\n⚠️  Found {len(short_blogs)} blogs that need content:")
        for blog in short_blogs:
            print(f"   • {blog}")
        print("\nThese blogs will be automatically blocked from publishing until fixed.")

    # Create pre-commit hook
    create_blog_validator_hook()

    # Update auto-publish script
    integrate_with_auto_publish()

    # Exit with error code if validation failed
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()