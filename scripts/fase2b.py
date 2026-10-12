import sys,os,json; sys.path.insert(0,os.path.dirname(__file__)); from wp import req
R=sys.argv[1]
# Service pages as drafts
for p in json.load(open(f'{R}/alteracoes/fase2-paginas-servico/paginas.json')):
  o=req('POST','wp/v2/pages',{'title':p['title'],'slug':p['slug'],'status':'draft','content':p['content']})
  pid=o.get('id'); print('draft',p['slug'],pid,o.get('HTTPError',''))
  if pid: print('  meta',req('POST','rankmath/v1/updateMeta',{'objectType':'post','objectID':pid,'meta':{'rank_math_title':p['seo_title'],'rank_math_description':p['seo_desc'],'rank_math_focus_keyword':p['kw']}}))
# Elementor: remove fake testimonials (home) + typos (servicos)
for pid,f in [(26,'home-26.json'),(31,'servicos-31.json')]:
  o=req('POST',f'wp/v2/pages/{pid}',{'meta':{'_elementor_data':open(f'{R}/alteracoes/fase2-elementor/{f}').read()}})
  print('elementor',pid,o.get('id'),o.get('HTTPError',''))
# Post CTA wording
for p in req('GET','wp/v2/posts?per_page=100&context=edit&_fields=id,slug,content'):
  c=p['content']['raw'];n=c.replace('atendendo empresas no RN e em todo o Brasil','com fábrica em Parnamirim/RN e atendimento em todo o Brasil').replace('atua com soluções em containers metálicos','atua com fabricação de containers metálicos sob medida')
  if n!=c: print('cta',p['slug'],req('POST',f"wp/v2/posts/{p['id']}",{'content':n}).get('id'))
