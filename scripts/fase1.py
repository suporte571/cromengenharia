import json,re,sys,html
R=sys.argv[1]; OUT=sys.argv[2]
P=[p for p in json.load(open(f'{R}/backup/posts.json')) if p['slug']!='hello-world']
cats={c['id']:c['name'] for c in json.load(open(f'{R}/backup/categories.json'))}
U='https://cromengenharia.com/'
# anchor phrase (regex, case-insensitive) -> target slug ; ordered by specificity
LINKS=[
 (r'linha de vida', 'linha-de-vida-nr-35'),
 (r'NR-12', 'nr-12-para-maquinas'),
 (r'laudo técnico', 'laudo-tecnico-maquinas-pesadas'),
 (r'projeto de estrutura metálica|projeto estrutural', 'projeto-de-estrutura-metalica'),
 (r'galpão metálico|galpões metálicos', 'galpao-metalico-vantagens-tipos'),
 (r'estrutura metálica ou concreto|aço ou concreto', 'estrutura-metalica-ou-concreto'),
 (r'preço por m²|preço da estrutura metálica', 'estrutura-metalica-preco-m2'),
 (r'reforço estrutural', 'corte-container-maritimo-reforco-estrutural'),
 (r'container almoxarifado', 'container-almoxarifado-para-obra'),
 (r'container escritório', 'container-escritorio-para-obra'),
 (r'canteiro de obras?', 'container-para-canteiro-de-obras'),
 (r'base (?:para|do) container|fundação', 'base-para-container-fundacao'),
 (r'portas? e janelas?', 'container-com-porta-e-janela'),
 (r'6x2,40|6×2,40', 'container-6x240-medidas-capacidade'),
]
SERV={'Containers Metálicos':('soluções em containers metálicos','servicos'),
 'Estruturas Metálicas':('projeto, fabricação e montagem de estruturas metálicas','servicos'),
 'Linha de Vida':('projeto e instalação de linha de vida e sistemas de ancoragem','servicos'),
 'Máquinas e Equipamentos':('laudos técnicos de máquinas pesadas','servicos')}
G={'C':['base-para-container-fundacao','container-com-porta-e-janela','corte-container-maritimo-reforco-estrutural','container-para-guardar-ferramentas','container-6x240-medidas-capacidade','container-escritorio-para-obra','container-para-canteiro-de-obras','container-almoxarifado-para-obra'],
 'E':['projeto-de-estrutura-metalica','galpao-metalico-vantagens-tipos','quanto-custa-galpao-estrutura-metalica','estrutura-metalica-ou-concreto','estrutura-metalica-preco-m2','quanto-custa-estrutura-metalica'],
 'L':['linha-de-vida-nr-35','quanto-custa-instalar-linha-de-vida','projeto-de-estrutura-metalica','galpao-metalico-vantagens-tipos'],
 'M':['laudo-tecnico-maquinas-pesadas','nr-12-para-maquinas','linha-de-vida-nr-35','projeto-de-estrutura-metalica']}
GOF={s:k for k in 'CEML' for s in G[k][:{'C':8,'E':6,'L':2,'M':2}[k]]}
CATN={'C':'Containers Metálicos','E':'Estruturas Metálicas','L':'Linha de Vida','M':'Máquinas e Equipamentos'}
BYS={p['slug']:p for p in P}
# link targets allowed per group
ALLOW={'C':set(G['C']),'E':set(G['E'])|{'linha-de-vida-nr-35'},'L':set(G['L'])|{'nr-12-para-maquinas'},'M':set(G['M'])}
def h1fix(c):
  c=re.sub(r'<!-- wp:heading \{"level":1\} -->','<!-- wp:heading -->',c)
  c=re.sub(r'<!-- wp:heading \{"level":1,','<!-- wp:heading {',c)
  return re.sub(r'<h1( [^>]*)?>(.*?)</h1>',lambda m:f'<h2{m.group(1) or ""}>{m.group(2)}</h2>',c,flags=re.S)
def link(c,slug):
  used=set();n=0
  parts=re.split(r'(<p>.*?</p>)',c,flags=re.S)
  for i,part in enumerate(parts):
    if not part.startswith('<p>') or n>=4: continue
    for rx,t in LINKS:
      if t==slug or t in used or n>=4 or t not in ALLOW[GOF[slug]]: continue
      # don't link inside existing anchors; only text segments outside tags
      segs=re.split(r'(<a\b.*?</a>|<[^>]+>)',part,flags=re.S)
      done=False
      for j,s in enumerate(segs):
        if done or s.startswith('<'): continue
        m=re.search(r'(?<![\w-])('+rx+r')(?![\w-])',s,flags=re.I)
        if m:
          segs[j]=s[:m.start()]+f'<a href="{U}{t}/">{m.group(1)}</a>'+s[m.end():];done=True
      if done: part=''.join(segs);used.add(t);n+=1
    parts[i]=part
  return ''.join(parts),used
def related(p,used):
  g=GOF[p['slug']]
  pool=[BYS[x] for x in G[g] if x!=p['slug']]
  pool=[q for q in pool if q['slug'] not in used]+[q for q in pool if q['slug'] in used]
  return CATN[g],pool[:3]
TS={html.unescape(q['title']['raw']).replace('×','x'):q['slug'] for q in P}
def L(title): return f'<a href="{U}{TS[title.replace("×","x")]}/">{title}</a>'
def Q(t): return '<strong>“'+t+'”</strong>'
NOTES=[
 ('<p>Para conhecer melhor esse formato, vale consultar o conteúdo '+Q('Container 6x2,40: medidas, capacidade e principais aplicações')+'.</p>',
  '<p>Para conhecer melhor esse formato, leia '+L('Container 6x2,40: medidas, capacidade e principais aplicações')+'.</p>'),
 ('<p><strong>Link interno recomendado:</strong> no trecho sobre reforços, inserir o conteúdo '+Q('Pode cortar container marítimo? Veja quando é necessário reforço estrutural')+'.</p>',
  '<p>Para entender melhor quando o reforço é necessário, leia '+L('Pode cortar container marítimo? Veja quando é necessário reforço estrutural')+'.</p>'),
 ('<p>Para aprofundar o assunto em aplicações administrativas, pode ser inserido um link para '+Q('Container escritório para obra: medidas, estrutura e o que precisa ter')+'.</p>',
  '<p>Para aprofundar o assunto em aplicações administrativas, leia '+L('Container escritório para obra: medidas, estrutura e o que precisa ter')+'.</p>'),
 ('<p>Vale inserir links internos para '+Q('Container almoxarifado para obra: medidas, estrutura e como escolher')+' e '+Q('Container para guardar ferramentas e materiais na obra: qual escolher?')+'.</p>',
  '<p>Veja também: '+L('Container almoxarifado para obra: medidas, estrutura e como escolher')+' e '+L('Container para guardar ferramentas e materiais na obra: qual escolher?')+'</p>'),
 ('<!-- wp:paragraph -->\n<p>Este conteúdo pode futuramente receber um link interno para o artigo '+Q('Como unir dois containers? Cuidados estruturais antes de fazer a modificação')+'.</p>\n<!-- /wp:paragraph -->',''),
 ('<p>Para aplicações em canteiros, vale criar links internos para '+Q('Container escritório para obra: medidas, estrutura e o que precisa ter')+' e '+Q('Container para canteiro de obras: quais modelos podem ser utilizados?')+'.</p>',
  '<p>Para aplicações em canteiros, leia também '+L('Container escritório para obra: medidas, estrutura e o que precisa ter')+' e '+L('Container para canteiro de obras: quais modelos podem ser utilizados?')+'</p>'),
 ('<p>Para aprofundar esse tipo de aplicação, o conteúdo '+Q('Container almoxarifado para obra: medidas, estrutura e como escolher')+' deve ser utilizado como link interno no blog da Crom Engenharia.</p>',
  '<p>Para aprofundar esse tipo de aplicação, leia '+L('Container almoxarifado para obra: medidas, estrutura e como escolher')+'.</p>'),
 ('<p>A Crom também pode direcionar o leitor para o conteúdo '+Q('Container 6x2,40: medidas, capacidade e principais aplicações')+'.</p>',
  '<p>Veja também: '+L('Container 6x2,40: medidas, capacidade e principais aplicações')+'.</p>'),
 ('<p>Esse ponto permite criar futuramente um link interno para o conteúdo '+Q('Base para container: precisa de fundação para instalar?')+'.</p>',
  '<p>Saiba mais em '+L('Base para container: precisa de fundação para instalar?')+'</p>'),
 ('<p>Esse trecho permite futuramente um link para '+Q('Base para container: precisa de fundação para instalar?')+'.</p>',
  '<p>Saiba mais em '+L('Base para container: precisa de fundação para instalar?')+'</p>'),
]
NOTEHITS=0
res=[]
for p in P:
  c=p['content']['raw']; orig=c
  for a,b in NOTES:
    if a in c: c=c.replace(a,b); NOTEHITS+=1
  if 'Leia também' in c: print('skip',p['slug']); continue
  c=h1fix(c)
  c=re.sub(r'(\s*<!-- wp:paragraph -->\s*<p></p>\s*<!-- /wp:paragraph -->)+\s*$','',c)
  c,used=link(c,p['slug'])
  cat,rel=related(p,used)
  items=''.join(f'<!-- wp:list-item -->\n<li><a href="{U}{q["slug"]}/">{html.escape(q["title"]["raw"],quote=False)}</a></li>\n<!-- /wp:list-item -->\n' for q in rel)
  sv,ss=SERV.get(cat,('soluções de engenharia','servicos'))
  c=c.rstrip()+f'''

<!-- wp:heading -->
<h2 class="wp-block-heading">Leia também</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">{items}</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>A <strong>CROM Engenharia</strong> atua com {sv}, atendendo empresas no RN e em todo o Brasil. <a href="{U}{ss}/">Conheça nossos serviços</a> ou <a href="{U}contato/">fale com um engenheiro</a> e solicite um orçamento.</p>
<!-- /wp:paragraph -->
'''
  res.append(dict(id=p['id'],slug=p['slug'],content=c,inlinks=sorted(used),related=[q['slug'] for q in rel],h1_before=orig.count('<h1'),h1_after=c.count('<h1'),fm=p['featured_media'],title=p['title']['raw']))
json.dump(res,open(OUT,'w'),ensure_ascii=False); print('notes fixed',NOTEHITS)
for r in res: print(r['slug'][:38].ljust(38),'h1',r['h1_before'],'->',r['h1_after'],'| links:',r['inlinks'],'| rel:',r['related'])
