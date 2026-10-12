import sys,os,json; sys.path.insert(0,os.path.dirname(__file__)); from wp import req
PAGES=[(1509,'Estruturas Metálicas','Projeto, fabricação e montagem de estruturas metálicas: galpões, coberturas, mezaninos e torres. Fábrica em Parnamirim/RN, atendimento em todo o Brasil.'),
 (1510,'Containers Metálicos','Fabricamos containers metálicos sob medida: almoxarifado, escritório de obra, depósito e vestiário. Fábrica em Parnamirim/RN, entrega em todo o Brasil.'),
 (1511,'Linha de Vida','Projeto, instalação, inspeção e recertificação de linha de vida e ancoragem conforme a NR-35, com ART. Parnamirim/RN e atendimento em todo o Brasil.'),
 (1512,'Laudos de Máquinas','Laudos técnicos de caminhão munck, escavadeira, empilhadeira e plataforma elevatória, com ART e conforme a NR-12. Parnamirim/RN, atendemos todo o Brasil.')]
links={}
# 1 Publish pages
for pid,label,desc in PAGES:
  print('desc',req('POST','rankmath/v1/updateMeta',{'objectType':'post','objectID':pid,'meta':{'rank_math_description':desc}}))
  o=req('POST',f'wp/v2/pages/{pid}',{'status':'publish'}); links[pid]=o.get('link'); print('publish',pid,o.get('status'),o.get('link'),o.get('HTTPError',''))
# 2 Submenu under "Serviços" (item 39) in main menu (2)
existing={it['object_id'] for it in req('GET','wp/v2/menu-items?menus=2&per_page=100')}
for n,(pid,label,_) in enumerate(PAGES,1):
  if pid in existing: continue
  o=req('POST','wp/v2/menu-items',{'title':label,'menus':2,'parent':39,'menu_order':3+n,'object':'page','object_id':pid,'type':'post_type','status':'publish'})
  print('menu',label,o.get('id'),o.get('HTTPError',''),o.get('body',''))
# 3 Serviços page: link the three service headings to the new pages
p=req('GET','wp/v2/pages/31?context=edit&_fields=meta');data=json.loads(p['meta']['_elementor_data'])
target={'21be74f':1509,'10d6f4c':1511,'660fad4':1512}
def walk(els):
  for e in els:
    if e.get('id') in target: e['settings']['link']={'url':links[target[e['id']]],'is_external':'','nofollow':'','custom_attributes':''}; print('heading link',e['id'],links[target[e['id']]])
    walk(e.get('elements',[]))
walk(data)
o=req('POST','wp/v2/pages/31',{'meta':{'_elementor_data':json.dumps(data,ensure_ascii=False)}}); print('servicos saved',o.get('id'),o.get('HTTPError',''))
