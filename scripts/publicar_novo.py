"""Publica o layout novo. Uso: publicar_novo.py <paginas.json> [--so-obras]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from wp import req

P = json.load(open(sys.argv[1]))
so_obras = '--so-obras' in sys.argv

th = req('GET', 'wp/v2/themes?status=active')
ativo = th[0]['stylesheet'] if isinstance(th, list) and th else None
print('tema ativo:', ativo)
if ativo != 'crom-novo':
    sys.exit('PARADO: o tema CROM Novo ainda não está ativo.')

# 1) Página Obras (nova)
ex = req('GET', 'wp/v2/pages?slug=obras&status=publish,draft&context=edit&_fields=id')
dados = {'title': 'Obras', 'slug': 'obras', 'status': 'publish', 'template': 'tpl-crom.php', 'content': P['obras']}
o = req('POST', f"wp/v2/pages/{ex[0]['id']}" if ex else 'wp/v2/pages', dados)
print('obras', o.get('id'), o.get('link'), o.get('template'), o.get('HTTPError', ''), o.get('body', '')[:200])
if o.get('id'):
    req('POST', 'rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': o['id'], 'meta': {
        'rank_math_title': 'Obras Realizadas em Estruturas Metálicas | CROM Engenharia',
        'rank_math_description': 'Coberturas, estacionamentos, escadas, marquises e montagens metálicas executadas pela CROM Engenharia, com fábrica em Parnamirim/RN.',
        'rank_math_focus_keyword': 'obras estruturas metálicas'}})
if so_obras:
    sys.exit(0)

# 2) Páginas existentes (mesmas URLs)
MAP = {26: 'home', 29: 'quem-somos', 31: 'servicos', 33: 'contato',
       1509: 'estruturas-metalicas', 1510: 'containers-metalicos', 1511: 'linha-de-vida', 1512: 'laudos-tecnicos-maquinas'}
for pid, k in MAP.items():
    r = req('POST', f'wp/v2/pages/{pid}', {'content': P[k], 'template': 'tpl-crom.php', 'meta': {'_elementor_edit_mode': ''}})
    print('pagina', pid, k, r.get('template'), r.get('link'), r.get('HTTPError', ''), r.get('body', '')[:200])

# 3) Blog e posts no layout novo
print('ativo:', req('POST', 'wp/v2/settings', {'crom_novo_ativo': True}).get('crom_novo_ativo'))

# 4) Categoria correta do post de linha de vida
cats = {c['name']: c['id'] for c in req('GET', 'wp/v2/categories?per_page=50')}
lv = req('GET', 'wp/v2/posts?slug=linha-de-vida-nr-35&_fields=id,categories')
if lv and 'Linha de Vida' in cats:
    print('categoria', req('POST', f"wp/v2/posts/{lv[0]['id']}", {'categories': [cats['Linha de Vida']]}).get('categories'))
