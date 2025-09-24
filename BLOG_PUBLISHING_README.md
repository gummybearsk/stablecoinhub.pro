# StableCoin Hub Blog Auto-Publishing System

## Overview
This repository now includes an automated blog publishing system that publishes scheduled blog posts daily via GitHub Actions.

## How It Works

### 1. **Blog Schedule** (`../blog-schedule.md`)
Contains the complete publishing calendar with blog titles and dates.

### 2. **GitHub Actions Workflow** (`.github/workflows/publish-blogs.yml`)
- Runs daily at 9 AM UTC (1 AM PST / 4 AM EST)
- Can also be triggered manually from GitHub Actions tab
- Automatically publishes blogs scheduled for the current date
- Commits and pushes changes automatically

### 3. **Publishing Script** (`auto_publish_blogs.py`)
- Reads the blog schedule
- Creates blog posts for the current date
- Generates SEO-optimized HTML with proper meta tags
- Ensures no duplicate publishing

## Manual Publishing

To manually publish blogs for a specific date:

```bash
python3 auto_publish_blogs.py 2025-09-25
```

To publish today's blogs:

```bash
python3 auto_publish_blogs.py
```

## Monitoring

1. **GitHub Actions**: Check the Actions tab in GitHub to see workflow runs
2. **Blog Directory**: New blogs appear in `/blog/[url-slug]/index.html`
3. **Live Site**: Published blogs appear at `https://www.stablecoinhub.pro/blog/[url-slug]/`

## Schedule Format

The blog schedule uses this format:

```markdown
## September 2025

- **Sep 24**: Blog Title Here
- **Sep 25**: Another Blog Title
```

## Features

✅ **Automatic Daily Publishing**: Blogs go live automatically based on schedule
✅ **SEO Optimized**: Each blog includes proper meta tags and structured data
✅ **Mobile Responsive**: All blogs use responsive Tailwind CSS
✅ **Analytics Ready**: Google Analytics tracking included
✅ **Error Handling**: Prevents duplicate publishing and handles missing dates

## Troubleshooting

1. **Blogs not publishing?**
   - Check GitHub Actions logs
   - Verify the date format in blog-schedule.md
   - Ensure GitHub Actions are enabled

2. **Manual trigger needed?**
   - Go to Actions tab → "Auto-Publish Scheduled Blogs"
   - Click "Run workflow"

3. **Testing locally?**
   ```bash
   python3 auto_publish_blogs.py 2025-09-24
   git status  # Check created files
   ```

## Important Notes

- Blogs are published at 9 AM UTC daily
- The system checks for existing blogs to prevent duplicates
- All changes are automatically committed and pushed
- The blog index page may need manual updating for navigation

## Future Enhancements

- [ ] Auto-update blog index page
- [ ] Add blog preview functionality
- [ ] Include content generation
- [ ] Add social media auto-posting