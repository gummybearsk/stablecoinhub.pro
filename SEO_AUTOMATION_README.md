# 🔍 SEO Automation System

This repository now includes a complete SEO automation system that ensures all HTML pages automatically have proper canonical tags and redirect scripts to prevent duplicate content issues.

## ✅ What's Protected Automatically

1. **Query Parameters** - All URLs with tracking parameters (`?utm_source=`, `?ref=`, `?fbclid=`, etc.) automatically canonical to clean URLs
2. **WWW to Non-WWW** - All www.stablecoinhub.pro requests redirect to stablecoinhub.pro
3. **HTTP to HTTPS** - GitHub Pages handles this automatically
4. **Future Pages** - New pages created with our tools automatically get SEO protection

## 🛠️ Tools Available

### 1. Create New Page with SEO (`create_new_page.py`)

Creates a new HTML page with all SEO optimizations pre-configured:

```bash
# Basic usage
python3 create_new_page.py "page-name"

# With custom title
python3 create_new_page.py "tools" "Stablecoin Tools - StableCoin Hub"

# With title and description
python3 create_new_page.py "products/defi" "DeFi Products" "Best DeFi products for stablecoins"
```

**Features included automatically:**
- ✅ Canonical tag
- ✅ WWW to non-www redirect
- ✅ Query parameter stripping
- ✅ Google Analytics
- ✅ Open Graph tags
- ✅ Mobile responsive template

### 2. SEO Monitor & Auto-Fixer (`auto_seo_monitor.py`)

Scans all HTML files and automatically fixes SEO issues:

```bash
# Check for issues without fixing
python3 auto_seo_monitor.py --check-only

# Automatically fix all issues
python3 auto_seo_monitor.py
```

**What it fixes:**
- Missing canonical tags
- Incorrect canonical URLs (with www or http)
- Missing redirect scripts
- Query parameter handling

### 3. Git Pre-Commit Hook

**Already installed!** Automatically runs before every commit to ensure SEO compliance.

Location: `.git/hooks/pre-commit`

The hook will:
1. Check all HTML files being committed
2. Fix any SEO issues automatically
3. Re-stage the fixed files
4. Continue with the commit

## 📋 Manual SEO Checklist (for reference)

If creating pages manually, include this in the `<head>`:

```html
<!-- Canonical URL -->
<link rel="canonical" href="https://stablecoinhub.pro/your-page/">

<!-- SEO Redirect Script -->
<script>
    // Redirect from www to non-www
    if (window.location.hostname === 'www.stablecoinhub.pro') {
        window.location.href = 'https://stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
    }
    // Remove query parameters from canonical URL dynamically
    if (window.location.search) {
        var canonicalTag = document.querySelector('link[rel="canonical"]');
        if (canonicalTag) {
            var cleanUrl = window.location.origin + window.location.pathname;
            if (window.location.pathname.endsWith('/index.html')) {
                cleanUrl = cleanUrl.replace('/index.html', '/');
            }
            canonicalTag.setAttribute('href', cleanUrl);
        }
    }
</script>
```

## 🚀 Quick Start for New Pages

1. **Use the automated tool:**
   ```bash
   python3 create_new_page.py "my-new-page" "My New Page - StableCoin Hub"
   ```

2. **Edit the content** in the created file

3. **Commit and push** - Pre-commit hook will verify SEO compliance

## 🔄 Regular Maintenance

Run periodically to ensure all pages are compliant:

```bash
python3 auto_seo_monitor.py
```

## ⚡ Benefits

- **Zero duplicate content** - Google won't penalize for URL variations
- **Better SEO rankings** - Clean canonical URLs improve search performance
- **Future-proof** - New marketing campaigns with any tracking parameters work automatically
- **Automated** - No manual intervention needed
- **Consistent** - All pages follow the same SEO standards

## 📊 Current Status

✅ **All 70 HTML pages** have been updated with:
- Canonical tags pointing to https://stablecoinhub.pro/...
- JavaScript redirects from www to non-www
- Dynamic query parameter removal
- CNAME configured for apex domain

## 🆘 Troubleshooting

If Google Search Console still shows errors:
1. Wait 5-10 days for Google to recrawl
2. Use "Validate Fix" button in Search Console
3. New errors should not appear for future URLs

## 📝 Notes

- GitHub Pages automatically handles HTTP → HTTPS redirects
- The apex domain (stablecoinhub.pro) is now the primary domain
- All variations redirect properly:
  - http://www.stablecoinhub.pro → https://stablecoinhub.pro
  - http://stablecoinhub.pro → https://stablecoinhub.pro
  - https://www.stablecoinhub.pro → https://stablecoinhub.pro

---
*Last updated: September 22, 2025*