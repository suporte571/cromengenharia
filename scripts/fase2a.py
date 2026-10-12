import sys,os,json; sys.path.insert(0,os.path.dirname(__file__)); from wp import req
# 1 Local SEO
print('module',req('POST','rankmath/v1/saveModule',{'module':'local-seo','state':'on'}))
r=req('POST','rankmath/v1/updateSettings',{'type':'titles','settings':{
 'knowledgegraph_type':'company','knowledgegraph_name':'CROM Engenharia','local_business_type':'GeneralContractor',
 'email':'comercial@cromengenharia.com','url':'https://cromengenharia.com/','phone':'+55 84 99151-9641',
 'local_address':{'streetAddress':'BR-304, Km 507, s/n - Encanto Verde','addressLocality':'Parnamirim','addressRegion':'RN','postalCode':'59146-750','addressCountry':'BR'},
 'local_address_format':'{address} {locality}, {region} {postalcode}',
 'phone_numbers':[{'type':'sales','number':'+55 84 99151-9641'},{'type':'customer support','number':'+55 84 99650-7337'}],
 'local_seo_about_page':'29','local_seo_contact_page':'33',
 'organization_description':'Projeto, fabricação e montagem de estruturas metálicas, fabricação de containers metálicos, linhas de vida e laudos técnicos de máquinas pesadas. Fábrica em Parnamirim/RN, atendimento em todo o Brasil. CREA-RN 200005964-2.'},
 'fieldTypes':{'local_address':'group','phone_numbers':'repeatableGroup','organization_description':'textarea'},'updated':[],'isReset':False})
s=r.get('settings',r) if isinstance(r,dict) else r
print('titles saved:',{k:s.get(k) for k in ['knowledgegraph_type','local_business_type','local_address','phone_numbers']} if isinstance(s,dict) else r)
# 2 Page metas
META={26:('Estruturas Metálicas e Containers em Parnamirim/RN | CROM','Projeto, fabricação e montagem de estruturas metálicas, containers metálicos, linha de vida e laudos de máquinas. Mais de 25 anos. Atendemos todo o Brasil.','estruturas metálicas'),
 31:('Serviços: Estruturas Metálicas, Containers e Linha de Vida','Galpões, coberturas, mezaninos, containers metálicos, linha de vida NR-35 e laudos de máquinas pesadas. Fábrica em Parnamirim/RN e atendimento em todo o Brasil.','serviços de estruturas metálicas'),
 29:('Quem Somos | CROM Engenharia, Parnamirim/RN','Há mais de 25 anos a CROM Engenharia projeta, fabrica e monta estruturas metálicas e containers. Equipe de 15 profissionais e registro CREA-RN 200005964-2.','CROM Engenharia'),
 33:('Contato e Orçamento | CROM Engenharia, Parnamirim/RN','Solicite orçamento de estruturas metálicas, containers, linha de vida ou laudos técnicos. BR-304, Km 507, Parnamirim/RN. WhatsApp (84) 99151-9641.','orçamento estrutura metálica')}
for i,(t,d,k) in META.items():
  print('meta',i,req('POST','rankmath/v1/updateMeta',{'objectType':'post','objectID':i,'meta':{'rank_math_title':t,'rank_math_description':d,'rank_math_focus_keyword':k}}))
# 3 Redirects + trash (trash is reversible from the WP Lixeira)
for slug,pid,ptype,to in [('hello-world',1,'posts','https://cromengenharia.com/blog/'),('sample-page',2,'pages','https://cromengenharia.com/')]:
  print('redirect',slug,req('POST','rankmath/v1/updateSettings',{'type':'redirections','settings':{'sources':[{'pattern':slug,'comparison':'exact'}],'url_to':to,'header_code':'301','status':'active'}}))
  o=req('DELETE',f'wp/v2/{ptype}/{pid}'); print('trash',slug,o.get('status'),o.get('HTTPError',''))
