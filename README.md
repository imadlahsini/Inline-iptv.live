# Inline IPTV — inline-iptv.live

Static landing page hosted on Netlify.

## Deploy to Netlify

1. Push this repo to GitHub
2. In Netlify: **Add new site → Import from Git → pick this repo**
3. Build settings: leave empty (no build command), publish directory = `.`
4. Click **Deploy site**

## Connect custom domain

1. Netlify dashboard → **Domain settings → Add custom domain → `inline-iptv.live`**
2. Update your DNS at the domain registrar:
   - Option A (Netlify DNS, easier): point nameservers to Netlify
   - Option B (external DNS): add A record → `75.2.60.5`, AAAA → Netlify IPv6, and CNAME for `www`
3. Enable **HTTPS** (Netlify provisions Let's Encrypt automatically — wait ~5 min)
4. Toggle **Force HTTPS** on

## Post-deploy SEO checklist

- [ ] Domain shows `https://inline-iptv.live/` (not `*.netlify.app`)
- [ ] HTTP redirects to HTTPS
- [ ] `www.inline-iptv.live` redirects to apex (or vice versa — pick one)
- [ ] `robots.txt` accessible at `/robots.txt`
- [ ] `sitemap.xml` accessible at `/sitemap.xml`
- [ ] Submit site to [Google Search Console](https://search.google.com/search-console)
- [ ] Submit sitemap in GSC
- [ ] Submit to [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ ] Verify all structured data with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Run [PageSpeed Insights](https://pagespeed.web.dev/) — aim for 90+ on mobile
- [ ] Test mobile-friendliness in GSC

## File structure

```
.
├── index.html        # Main landing page
├── netlify.toml      # Netlify build config + security headers
├── robots.txt        # Crawler instructions + AI bot blocking
├── sitemap.xml       # Sitemap for 23 public pages
├── netlify/edge-functions/legacy-cleanup.js # Retired WordPress URL responses
├── .gitignore
└── README.md
```

## Two-domain note

This site (`inline-iptv.live`) is the marketing/SEO target.
Trial signups happen on `iptvfreetrial.live` (separate domain).

To prevent SEO competition between the two:
- This domain: indexed normally, canonical to self
- Trial domain: add `<meta name="robots" content="noindex, follow">` to the trial form page

The Organization schema identifies this domain. Add `sameAs` only for verified official profiles; the trial form is not a social identity profile.

## SEO cleanup rollout

Deploy this folder through Netlify to activate the legacy cleanup edge function.
It returns HTTP 410 for `/feed/` and nested feed URLs, root WordPress `?p=`
links (including `/index.php?p=`), and `/sitemap_index.xml`. Other requests
continue through existing routing. These URLs remain allowed in robots.txt so
Google can crawl and observe their removal. Unrecognized URLs retain normal 404
behavior; do not retire every unknown path.

The audit's 50 former blog paths were not included. Add confirmed pathnames to
`retiredBlogPaths` in the edge function before expecting those paths to return
410. Verify that none is a current page or has a relevant replacement.

After deployment:

- Verify actual HTTP status codes for legacy URLs and current pages on Netlify.
- Remove the old `sitemap_index.xml` submission in Search Console and submit
  `https://inline-iptv.live/sitemap.xml`.
- Inspect and request indexing for `/`, `/iptv-subscription`, `/about`, `/devices`,
  `/iptv-guides`, `/iptv-for-firestick`, `/iptv-for-smart-tv`, `/iptv-for-android`,
  `/iptv-for-iphone`, and `/iptv-for-apple-tv`.
- Add verified official social profiles to Organization `sameAs` once available.
- Review Page Indexing and search performance after Google recrawls. Indexing
  and rankings are not guaranteed by these file changes.

Local validation: `python3 scripts/seo-audit.py`. This checks metadata, local
links, assets, structured-data JSON and sitemap targets, not live Netlify routing
or Search Console data.
