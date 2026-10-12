"""Volta ao layout antigo. Uso: desfazer_novo.py <backup/pages.json> <alteracoes/fase2-paginas-servico/paginas.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from wp import req

print('ativo:', req('POST', 'wp/v2/settings', {'crom_novo_ativo': False}).get('crom_novo_ativo'))
orig = {p['id']: p for p in json.load(open(sys.argv[1]))}
for pid in (26, 29, 31, 33):
    p = orig[pid]
    r = req('POST', f'wp/v2/pages/{pid}', {'content': p['content']['raw'], 'template': p.get('template', ''),
                                           'meta': {'_elementor_edit_mode': p['meta'].get('_elementor_edit_mode', 'builder')}})
    print('restaurada', pid, r.get('template'), r.get('HTTPError', ''))
servs = {s['slug']: s for s in json.load(open(sys.argv[2]))}
for pid, slug in {1509: 'estruturas-metalicas', 1510: 'containers-metalicos', 1511: 'linha-de-vida', 1512: 'laudos-tecnicos-maquinas'}.items():
    r = req('POST', f'wp/v2/pages/{pid}', {'content': servs[slug]['content'], 'template': ''})
    print('restaurada', pid, r.get('HTTPError', ''))
