// Keep retired URLs crawlable so search engines can observe the 410 response.
// Add only confirmed old blog paths here, using their exact pathname.
const retiredBlogPaths = new Set([]);

export default function legacyCleanup(request) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, "") || "/";
  const isFeed = /(?:^|\/)feed(?:\/|$)/i.test(path);
  const isWordPressPost = (path === "/" || path === "/index.php") && url.searchParams.has("p");
  const isOldSitemap = path === "/sitemap_index.xml";

  if (!isFeed && !isWordPressPost && !isOldSitemap && !retiredBlogPaths.has(path)) {
    return; // Continue to Netlify's existing static routes and redirects.
  }

  const body = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page removed | Inline IPTV</title><h1>This page has been removed</h1><p>This URL belonged to the previous website and is no longer available.</p><p><a href="/">Visit Inline IPTV</a></p></html>';
  return new Response(request.method === "HEAD" ? null : body, {
    status: 410,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

export const config = { path: "/*" };
