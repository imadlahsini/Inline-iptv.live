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
├── sitemap.xml       # Single-URL sitemap
├── .gitignore
└── README.md
```

## Two-domain note

This site (`inline-iptv.live`) is the marketing/SEO target.
Trial signups happen on `iptvfreetrial.live` (separate domain).

To prevent SEO competition between the two:
- This domain: indexed normally, canonical to self
- Trial domain: add `<meta name="robots" content="noindex, follow">` to the trial form page

The `Organization` schema in `index.html` already links the two via `sameAs`.
