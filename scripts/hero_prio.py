import sys,os,json; sys.path.insert(0,os.path.dirname(__file__)); from wp import req
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=json.load(open(f'{S}/paginas.json'))
ids={26:'home',29:'quem-somos',31:'servicos',33:'contato',1509:'estruturas-metalicas',1510:'containers-metalicos',1511:'linha-de-vida',1512:'laudos-tecnicos-maquinas'}
ob=req('GET','wp/v2/pages?slug=obras&_fields=id')[0]['id']; ids[ob]='obras'
for pid,k in ids.items():
  c=P[k]
  n=c.replace('class="bg" src=','class="bg" fetchpriority="high" src=',1)
  if n!=c:
    P[k]=n; r=req('POST',f'wp/v2/pages/{pid}',{'content':n}); print(k,r.get('id'),r.get('HTTPError',''))
json.dump(P,open(f'{S}/paginas.json','w'),ensure_ascii=False)
