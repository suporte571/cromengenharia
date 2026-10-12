"""Troca a imagem de destaque PNG dos posts por uma versão JPG otimizada (mesmo visual)."""
import sys, os, json, io, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from wp import req, H
from PIL import Image

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
posts = req('GET', 'wp/v2/posts?per_page=100&_fields=id,slug,title,featured_media')
log = []
for p in posts:
    fm = p['featured_media']
    if not fm:
        continue
    m = req('GET', f'wp/v2/media/{fm}?_fields=id,source_url,mime_type,alt_text')
    if m.get('mime_type') != 'image/png':
        print('pula', p['slug'], m.get('mime_type'))
        continue
    raw = urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(m['source_url'], safe=':/%'), headers={'User-Agent': 'Mozilla/5.0'}), timeout=120).read()
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    im.thumbnail((1600, 1600))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=80, optimize=True, progressive=True)
    name = p['slug'] + '.jpg'
    h = dict(H)
    h['Content-Type'] = 'image/jpeg'
    h['Content-Disposition'] = f'attachment; filename="{name}"'
    r = urllib.request.Request('https://cromengenharia.com/wp-json/wp/v2/media', data=buf.getvalue(), headers=h, method='POST')
    new = json.load(urllib.request.urlopen(r, timeout=180))
    alt = m.get('alt_text') or p['title']['rendered']
    req('POST', f"wp/v2/media/{new['id']}", {'alt_text': alt})
    req('POST', f"wp/v2/posts/{p['id']}", {'featured_media': new['id']})
    log.append({'post': p['id'], 'antes': fm, 'depois': new['id']})
    print('ok', p['slug'], len(raw) // 1024, 'KB ->', len(buf.getvalue()) // 1024, 'KB')
json.dump(log, open(f'{S}/featured_troca.json', 'w'))
