#!/usr/bin/env python3
"""Small stdlib-only audit for the static Inline IPTV site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'iptv-guides').glob('*.html'))

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.description=''; self.canonicals=[]; self.h1=[]; self.hrefs=[]; self.srcs=[]; self.jsonld=[]; self.in_title=False; self.in_h1=False; self.in_desc=False; self.in_json=False; self.buf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.in_title=True
        if tag=='h1': self.in_h1=True
        if tag=='meta' and a.get('name','').lower()=='description': self.description=a.get('content','')
        if tag=='link' and a.get('rel','').lower()=='canonical': self.canonicals.append(a.get('href',''))
        if tag in ('a','link'): self.hrefs.append(a.get('href',''))
        if tag=='img': self.srcs.append(a.get('src',''))
        if tag=='script' and a.get('type')=='application/ld+json': self.in_json=True; self.buf=[]
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False; self.title=''.join(self.buf).strip(); self.buf=[]
        if tag=='h1': self.in_h1=False
        if tag=='script' and self.in_json: self.jsonld.append(''.join(self.buf)); self.in_json=False; self.buf=[]
    def handle_data(self, data):
        if self.in_title or self.in_json: self.buf.append(data)
        if self.in_h1: self.h1.append(data)

def is_local(value):
    if not value: return False
    parsed=urlparse(value)
    return not parsed.scheme and not parsed.netloc or parsed.netloc in ('inline-iptv.live','www.inline-iptv.live')

def route_file(path):
    path=path.split('#',1)[0].split('?',1)[0]
    if path in ('','/'): return ROOT/'index.html'
    path=path.lstrip('/')
    candidate=ROOT/path
    if candidate.is_file(): return candidate
    if (ROOT/(path+'.html')).is_file(): return ROOT/(path+'.html')
    if path.startswith('iptv-guides/') and (ROOT/(path+'.html')).is_file(): return ROOT/(path+'.html')
    return None

pages=[]; broken_links=[]; broken_assets=[]; invalid_jsonld=[]; internal_html=[]; multiple_h1=[]; missing=[]
for file in HTML_FILES:
    parser=PageParser(); parser.feed(file.read_text(errors='replace'))
    pages.append((file,parser))
    if len(parser.h1)!=1: multiple_h1.append(str(file.relative_to(ROOT)))
    for href in parser.hrefs:
        if not is_local(href): continue
        parsed=urlparse(href); target=route_file(parsed.path or '/')
        if target is None: broken_links.append(f'{file.relative_to(ROOT)} -> {href}')
        if '.html' in (parsed.path or ''): internal_html.append(f'{file.relative_to(ROOT)} -> {href}')
    for src in parser.srcs:
        if not is_local(src): continue
        parsed=urlparse(src); target=ROOT/(parsed.path.lstrip('/'))
        if not target.is_file(): broken_assets.append(f'{file.relative_to(ROOT)} -> {src}')
    for block in parser.jsonld:
        try: json.loads(block)
        except Exception as exc: invalid_jsonld.append(f'{file.relative_to(ROOT)}: {exc}')
    if file.name != '404.html' and (not parser.title or not parser.description or len(parser.canonicals)!=1): missing.append(str(file.relative_to(ROOT)))

def duplicates(index):
    seen={}; dup=[]
    for file,p in pages:
        value=index(p)
        if value: seen.setdefault(value,[]).append(str(file.relative_to(ROOT)))
    for value,files in seen.items():
        if len(files)>1: dup.append(' | '.join(files))
    return dup

titles=duplicates(lambda p:p.title); descriptions=duplicates(lambda p:p.description); canonicals=duplicates(lambda p:p.canonicals[0] if p.canonicals else '')
text='\n'.join(f.read_text(errors='replace') for f,_ in pages)
sitemap=re.findall(r'<loc>([^<]+)</loc>', (ROOT/'sitemap.xml').read_text())
missing_sitemap=[]
for url in sitemap:
    parsed=urlparse(url)
    if route_file(parsed.path) is None: missing_sitemap.append(url)

trust_token = 'trust' + 'pilot'
return_token = 'Return' + 'ByMail'
counts={
 'Broken internal links':len(broken_links), 'Broken assets':len(broken_assets), 'Invalid JSON-LD blocks':len(invalid_jsonld),
 'Duplicate titles':len(titles), 'Duplicate descriptions':len(descriptions), 'Duplicate canonicals':len(canonicals),
 'Multiple-H1 pages':len(multiple_h1), f'{return_token} occurrences':text.count(return_token), f'{trust_token.title()} occurrences':len(re.findall(trust_token,text,re.I)),
 'Internal .html links':len(internal_html), 'Sitemap URLs pointing to missing pages':len(missing_sitemap),
}
for key,value in counts.items(): print(f'{key}: {value}')
if any(counts.values()) or missing:
    print(f'Metadata/H1 issues: {len(missing)}')
    if broken_links: print('Broken links:', *broken_links, sep='\n  ')
    if broken_assets: print('Broken assets:', *broken_assets, sep='\n  ')
    if invalid_jsonld: print('Invalid JSON-LD:', *invalid_jsonld, sep='\n  ')
    if missing_sitemap: print('Missing sitemap routes:', *missing_sitemap, sep='\n  ')
    sys.exit(1)
print(f'Audited {len(pages)} HTML pages and {len(sitemap)} sitemap URLs: PASS')
