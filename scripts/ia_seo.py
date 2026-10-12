"""Melhorias para buscadores e IAs: schema Service + FAQPage nas páginas de serviço,
texto inicial limpo (para llms.txt), imagem de compartilhamento da Home e perfil social."""
import sys, os, json, re, html
sys.path.insert(0, os.path.dirname(__file__))
from wp import req

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(f'{S}/paginas.json'))
U = 'https://cromengenharia.com'
ORG = U + '/#organization'

def limpa(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()

SERV = {
    1509: ('estruturas-metalicas', 'Estruturas metálicas', 'Projeto, fabricação e montagem de estruturas metálicas'),
    1510: ('containers-metalicos', 'Fabricação de containers metálicos', 'Fabricação de containers metálicos'),
    1511: ('linha-de-vida', 'Linha de vida e sistemas de ancoragem', 'Projeto, instalação e recertificação de linha de vida NR-35'),
    1512: ('laudos-tecnicos-maquinas', 'Laudo técnico de máquinas pesadas', 'Laudo técnico de máquinas pesadas e NR-12'),
}
IDS = {26: 'home', 29: 'quem-somos', 31: 'servicos', 33: 'contato', 1543: 'obras', **{k: v[0] for k, v in SERV.items()}}

for pid, k in IDS.items():
    c = P[k]
    # breadcrumbs e "eyebrows" deixam de ser parágrafos: o primeiro <p> passa a ser o texto real da página
    c = re.sub(r'<p class="crumbs">(.*?)</p>', r'<nav class="crumbs" aria-label="Você está em">\1</nav>', c)
    c = re.sub(r'<p class="eyebrow">(.*?)</p>', r'<div class="eyebrow">\1</div>', c)
    if pid in SERV and 'application/ld+json' not in c:
        slug, nome, tipo = SERV[pid]
        lead = limpa(re.search(r'<p class="lead">(.*?)</p>', c, re.S).group(1))
        faqs = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', c, re.S)
        graph = [
            {'@type': 'Service', '@id': f'{U}/{slug}/#servico', 'name': nome, 'serviceType': tipo, 'description': lead,
             'url': f'{U}/{slug}/', 'provider': {'@id': ORG},
             'areaServed': [{'@type': 'State', 'name': 'Rio Grande do Norte'}, {'@type': 'Country', 'name': 'Brasil'}]},
            {'@type': 'FAQPage', '@id': f'{U}/{slug}/#faq',
             'mainEntity': [{'@type': 'Question', 'name': limpa(q), 'acceptedAnswer': {'@type': 'Answer', 'text': limpa(a)}} for q, a in faqs]},
        ]
        ld = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'
        c = c.replace('\n<!-- /wp:html -->', '\n' + ld + '\n<!-- /wp:html -->', 1)
    if c != P[k]:
        P[k] = c
        r = req('POST', f'wp/v2/pages/{pid}', {'content': c})
        print('pagina', k, r.get('id'), r.get('HTTPError', ''))
json.dump(P, open(f'{S}/paginas.json', 'w'), ensure_ascii=False)

# Imagem de compartilhamento (WhatsApp/LinkedIn/Facebook) da Home e de Obras
img = req('GET', 'wp/v2/media/1287?_fields=source_url')['source_url']
for pid in (26, 1543, 31):
    print('og', pid, req('POST', 'rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': pid, 'meta': {
        'rank_math_facebook_image': img, 'rank_math_facebook_image_id': 1287}}))

# Perfil social da empresa (sameAs no schema da organização)
r = req('POST', 'rankmath/v1/updateSettings', {'type': 'titles', 'settings': {
    'social_additional_profiles': 'https://www.instagram.com/cromengenhariaa/'}, 'fieldTypes': {'social_additional_profiles': 'textarea'}, 'updated': [], 'isReset': False})
print('social', (r.get('settings') or {}).get('social_additional_profiles') if isinstance(r, dict) else r)
