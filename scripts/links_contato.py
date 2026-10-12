import sys,os,json; sys.path.insert(0,os.path.dirname(__file__)); from wp import req
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=json.load(open(f'{S}/paginas.json'))
WA='<a href="https://wa.me/5584991519641" target="_blank" rel="noopener">(84) 99151-9641</a>'
ML='<a href="mailto:comercial@cromengenharia.com">comercial@cromengenharia.com</a>'
REP=[('<span>WhatsApp comercial</span>(84) 99151-9641','<span>WhatsApp comercial</span>'+WA),
 ('<span>Telefones</span>(84) 99650-7337 · (84) 99106-0289','<span>Telefones</span><a href="tel:+5584996507337">(84) 99650-7337</a> · <a href="tel:+5584991060289">(84) 99106-0289</a>'),
 ('<span>E-mail</span>comercial@cromengenharia.com','<span>E-mail</span>'+ML),
 ('<span>WhatsApp</span>(84) 99151-9641','<span>WhatsApp</span>'+WA)]
ids={26:'home',29:'quem-somos',31:'servicos',33:'contato',1509:'estruturas-metalicas',1510:'containers-metalicos',1511:'linha-de-vida',1512:'laudos-tecnicos-maquinas',1543:'obras'}
for pid,k in ids.items():
  c=P[k];n=c
  for a,b in REP: n=n.replace(a,b)
  if n!=c:
    P[k]=n;r=req('POST',f'wp/v2/pages/{pid}',{'content':n});print(k,r.get('id'),r.get('HTTPError',''))
json.dump(P,open(f'{S}/paginas.json','w'),ensure_ascii=False)
