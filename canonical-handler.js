// Canonical URL and Query Parameter Handler
(function() {
    'use strict';

    // Function to get clean URL without parameters
    function getCleanUrl() {
        var url = window.location.protocol + '//' + 'www.stablecoinhub.pro' + window.location.pathname;

        // Remove index.html from URL
        url = url.replace(/\/index\.html$/, '/');

        // Ensure trailing slash for directories
        if (!url.match(/\.[a-z]{2,4}$/i) && !url.endsWith('/')) {
            url += '/';
        }

        return url;
    }

    // Function to handle query parameters
    function handleQueryParameters() {
        if (window.location.search) {
            // Extract tracking parameters
            var urlParams = new URLSearchParams(window.location.search);
            var trackingParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref', 'gclid', 'fbclid'];

            // Store tracking info in sessionStorage
            trackingParams.forEach(function(param) {
                var value = urlParams.get(param);
                if (value) {
                    sessionStorage.setItem(param, value);

                    // Send to analytics if available
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'page_view', {
                            [param]: value
                        });
                    }
                }
            });

            // Clean URL in address bar
            var cleanUrl = getCleanUrl();
            window.history.replaceState({}, document.title, cleanUrl);
        }
    }

    // Function to update or create canonical tag
    function updateCanonicalTag() {
        var canonicalTag = document.querySelector('link[rel="canonical"]');
        var cleanUrl = getCleanUrl();

        if (canonicalTag) {
            canonicalTag.setAttribute('href', cleanUrl);
        } else {
            canonicalTag = document.createElement('link');
            canonicalTag.rel = 'canonical';
            canonicalTag.href = cleanUrl;
            document.head.appendChild(canonicalTag);
        }
    }

    // Function to ensure www subdomain
    function ensureWwwSubdomain() {
        if (window.location.hostname === 'stablecoinhub.pro') {
            var newUrl = 'https://www.stablecoinhub.pro' + window.location.pathname + window.location.search + window.location.hash;
            window.location.replace(newUrl);
            return true; // Redirecting, stop further execution
        }
        return false;
    }

    // Execute functions
    if (!ensureWwwSubdomain()) {
        handleQueryParameters();
        updateCanonicalTag();
    }
})();
