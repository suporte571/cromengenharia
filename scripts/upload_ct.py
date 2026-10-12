import sys, os, json, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
from wp import req, H

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
existing = req('GET', 'wp/v2/media?search=container-ilustracao&per_page=20&_fields=id,slug,source_url')
have = {m['slug']: m['source_url'] for m in existing} if isinstance(existing, list) else {}
for v, alt in [('escritorio', 'Container escritório de obra fabricado pela CROM Engenharia (ilustração)'),
               ('almoxarifado', 'Container almoxarifado com portas de carga (ilustração)')]:
    name = f'container-ilustracao-{v}.jpg'
    if name[:-4] in have:
        out[v] = have[name[:-4]]
        print('já existe', v)
        continue
    data = open(f'{S}/prototipo/img/container-{v}.jpg', 'rb').read()
    h = dict(H)
    h['Content-Type'] = 'image/jpeg'
    h['Content-Disposition'] = f'attachment; filename="{name}"'
    r = urllib.request.Request('https://cromengenharia.com/wp-json/wp/v2/media', data=data, headers=h, method='POST')
    m = json.load(urllib.request.urlopen(r, timeout=120))
    req('POST', f"wp/v2/media/{m['id']}", {'alt_text': alt, 'title': alt})
    out[v] = m['source_url']
    print('enviado', v, m['id'], m['source_url'])
json.dump(out, open(f'{S}/containers.json', 'w'))

# últimos 3 posts para a Home (estático)
posts = req('GET', 'wp/v2/posts?per_page=3&_embed=wp:featuredmedia,wp:term&_fields=link,title,_links,_embedded')
cards = []
for p in posts:
    fm = p['_embedded']['wp:featuredmedia'][0]
    sz = fm.get('media_details', {}).get('sizes', {})
    src = (sz.get('medium_large') or sz.get('large') or {'source_url': fm['source_url']})['source_url']
    cat = p['_embedded']['wp:term'][0][0]['name']
    t = p['title']['rendered']
    cards.append(f'<a class="post-card" href="{p["link"]}"><div class="ph"><img src="{src}" alt="" loading="lazy"></div><span class="meta">{cat}</span><h3>{t}</h3></a>')
open(f'{S}/home_posts.html', 'w').write('<div class="posts">' + ''.join(cards) + '</div>')
print('posts', len(cards))
