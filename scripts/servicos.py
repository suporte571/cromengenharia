import json,sys,html
OUT=sys.argv[1]; U='https://cromengenharia.com/'
def P(t): return f'<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->\n\n'
def H(t,l=2): return (f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n' if l==2 else f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n')
def UL(items): return '<!-- wp:list -->\n<ul class="wp-block-list">'+''.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->\n' for i in items)+'</ul>\n<!-- /wp:list -->\n\n'
def A(slug,t): return f'<a href="{U}{slug}/">{t}</a>'
WA='<a href="https://wa.me/5584991519641">WhatsApp (84) 99151-9641</a>'
def CTA(t): return P(f'<strong>{t}</strong> Fale com um engenheiro da CROM pelo {WA}, pelo e-mail <a href="mailto:comercial@cromengenharia.com">comercial@cromengenharia.com</a> ou pela {A("contato","página de contato")}.')
def FAQ(qs): return H('Perguntas frequentes')+''.join(H(q,3)+P(a) for q,a in qs)
SOBRE=P('A <strong>CROM Engenharia</strong> tem mais de 25 anos de experiência em estruturas metálicas e engenharia mecânica, equipe de 15 profissionais e registro no CREA-RN (200005964-2). Nossa fábrica fica na BR-304, Km 507, em <strong>Parnamirim/RN</strong>, e atendemos empresas em todo o Brasil.')
pages=[]
pages.append(dict(slug='estruturas-metalicas',title='Estruturas Metálicas em Parnamirim/RN',
 seo_title='Estruturas Metálicas em Parnamirim/RN: Projeto e Montagem | CROM',
 seo_desc='Projeto, fabricação e montagem de estruturas metálicas: galpões, coberturas, mezaninos, marquises e torres. Fábrica em Parnamirim/RN, atendimento em todo o Brasil.',
 kw='estruturas metálicas',
 content=P('A CROM Engenharia faz o <strong>projeto, a fabricação e a montagem de estruturas metálicas</strong> sob medida para indústrias, comércios, centros logísticos e obras em geral. Cuidamos de todas as etapas dentro de casa, do cálculo estrutural à montagem em campo, sempre de acordo com as normas técnicas vigentes.')
 +H('O que fabricamos e montamos')
 +UL(['<strong>Galpões industriais e comerciais</strong>, com grandes vãos livres e possibilidade de ampliação','<strong>Coberturas metálicas</strong> para áreas industriais, estacionamentos e pátios','<strong>Mezaninos</strong> para ampliar a área útil sem nova construção','<strong>Marquises</strong> e estruturas de fachada','<strong>Escadas metálicas</strong> de diversos tipos','<strong>Torres estaiadas e autoportantes</strong>','<strong>Suportes para placas fotovoltaicas</strong>'])
 +H('Como funciona o nosso trabalho')
 +UL(['<strong>Levantamento e concepção:</strong> entendemos a necessidade, o local e as cargas envolvidas.','<strong>Projeto estrutural:</strong> modelagem, dimensionamento, ligações e detalhamento, com ART.','<strong>Fabricação:</strong> corte, dobra, solda e tratamento anticorrosivo na nossa fábrica.','<strong>Montagem:</strong> equipe própria em campo, com planejamento de içamento e segurança.'])
 +P(f'Quer entender as etapas em detalhe? Leia {A("projeto-de-estrutura-metalica","Projeto de estrutura metálica: como funciona")}.')
 +H('Por que escolher estrutura metálica?')
 +P(f'A estrutura metálica permite obras mais rápidas, vãos maiores e um canteiro mais limpo, já que boa parte do trabalho é feita na fábrica. Para comparar com outras soluções, veja {A("estrutura-metalica-ou-concreto","Estrutura metálica ou concreto: qual escolher")} e {A("galpao-metalico-vantagens-tipos","Galpão metálico: vantagens e tipos")}.')
 +FAQ([('Quanto custa uma estrutura metálica?',f'O preço depende do tipo de estrutura, dos vãos, das cargas, do peso de aço e da montagem. Explicamos como esse valor é calculado em {A("quanto-custa-estrutura-metalica","Quanto custa uma estrutura metálica")} e em {A("quanto-custa-galpao-estrutura-metalica","Quanto custa construir um galpão de estrutura metálica")}.'),
  ('Vocês atendem fora do Rio Grande do Norte?','Sim. A fábrica fica em Parnamirim/RN e atendemos empresas em todo o Brasil.'),
  ('O projeto acompanha ART?','Sim. Nossos projetos são desenvolvidos por engenheiros habilitados, com emissão de ART.')])
 +SOBRE+CTA('Precisa de um galpão, cobertura ou mezanino?')))
pages.append(dict(slug='containers-metalicos',title='Fabricação de Containers Metálicos',
 seo_title='Fabricação de Containers Metálicos em Parnamirim/RN | CROM',
 seo_desc='Fabricamos containers metálicos sob medida: almoxarifado, escritório de obra, depósito, vestiário e projetos especiais. Fábrica em Parnamirim/RN, entrega em todo o Brasil.',
 kw='containers metálicos',
 content=P('A CROM Engenharia <strong>fabrica containers metálicos</strong> sob medida para canteiros de obras, indústrias e empresas que precisam de espaços modulares resistentes e prontos para uso. Também fazemos <strong>adaptações e reforços estruturais</strong> em containers, com projeto de engenharia.')
 +H('Modelos que fabricamos')
 +UL([f'<strong>Container almoxarifado</strong> para guardar materiais e ferramentas: {A("container-almoxarifado-para-obra","veja medidas e como escolher")}',f'<strong>Container escritório</strong> para obra: {A("container-escritorio-para-obra","o que ele precisa ter")}','<strong>Container depósito</strong> para materiais e equipamentos','<strong>Container vestiário e de apoio</strong> para equipes','<strong>Containers personalizados</strong>, com layout, portas, janelas e instalações sob medida'])
 +H('Projeto e adaptação com engenharia')
 +P(f'Abrir portas e janelas, cortar painéis ou unir módulos altera a estrutura do container. Por isso, toda modificação passa por análise de engenharia. Entenda melhor em {A("corte-container-maritimo-reforco-estrutural","Pode cortar container marítimo? Quando reforçar a estrutura")} e {A("container-com-porta-e-janela","Container com porta e janela: cuidados ao modificar")}.')
 +H('Medidas e instalação')
 +P(f'O modelo mais usado tem cerca de 6,00 x 2,40 m ({A("container-6x240-medidas-capacidade","veja medidas e capacidade")}), mas fabricamos em outros tamanhos conforme a necessidade. A base também precisa ser bem planejada: saiba mais em {A("base-para-container-fundacao","Base para container: precisa de fundação?")}.')
 +FAQ([('Vocês fabricam containers sob medida?','Sim. Definimos tamanho, layout, aberturas e instalações de acordo com o uso: almoxarifado, escritório, depósito, vestiário ou projeto especial.'),
  ('Qual container é melhor para canteiro de obras?',f'Depende da função. Explicamos os principais modelos em {A("container-para-canteiro-de-obras","Container para canteiro de obras: quais modelos utilizar")}.'),
  ('Vocês entregam fora do RN?','Sim. A fábrica fica em Parnamirim/RN e atendemos empresas em todo o Brasil.')])
 +SOBRE+CTA('Precisa de um container para sua obra ou empresa?')))
pages.append(dict(slug='linha-de-vida',title='Linha de Vida e Sistemas de Ancoragem',
 seo_title='Linha de Vida NR-35: Projeto, Instalação e Laudo | CROM',
 seo_desc='Projeto, instalação, inspeção e recertificação de linha de vida e sistemas de ancoragem conforme a NR-35, com ART. Parnamirim/RN e atendimento em todo o Brasil.',
 kw='linha de vida',
 content=P('A <strong>linha de vida</strong> é um sistema de ancoragem que permite ao trabalhador se deslocar com segurança em altura, reduzindo o risco de quedas. A CROM Engenharia faz o <strong>projeto, a instalação, a inspeção e a recertificação</strong> de linhas de vida e pontos de ancoragem, seguindo a NR-35 e as normas técnicas aplicáveis.')
 +H('Nossos serviços de linha de vida')
 +UL(['<strong>Projeto sob medida</strong> de linha de vida horizontal, vertical e para telhados','<strong>Fornecimento e instalação</strong> de linhas de vida e pontos de ancoragem','<strong>Inspeção inicial e periódica</strong>','<strong>Laudo técnico e recertificação</strong> de linhas existentes, com ART'])
 +H('Quando a linha de vida é obrigatória?')
 +P(f'Sempre que houver trabalho em altura e a análise de risco indicar a necessidade de um sistema de proteção contra quedas. Explicamos em detalhe em {A("linha-de-vida-nr-35","Linha de vida NR-35: o que é e quando é obrigatória")}.')
 +H('Onde instalamos')
 +UL(['Telhados e coberturas de galpões','Estruturas metálicas e plataformas industriais','Fachadas, escadas e acessos verticais','Áreas de manutenção de máquinas e equipamentos'])
 +FAQ([('Quanto custa instalar uma linha de vida?',f'O valor depende do tipo de sistema, da extensão, da estrutura de fixação e da documentação. Veja os fatores em {A("quanto-custa-instalar-linha-de-vida","Quanto custa instalar uma linha de vida")}.'),
  ('A linha de vida precisa de ART?','Sim. O projeto e a instalação devem ser feitos sob responsabilidade de um profissional habilitado, com emissão de ART.'),
  ('Vocês fazem a inspeção de linhas já instaladas?','Sim. Fazemos inspeção periódica, laudo técnico e recertificação de linhas de vida existentes.')])
 +SOBRE+CTA('Precisa instalar ou recertificar uma linha de vida?')))
pages.append(dict(slug='laudos-tecnicos-maquinas',title='Laudo Técnico de Máquinas Pesadas',
 seo_title='Laudo Técnico de Máquinas Pesadas e NR-12 | CROM Engenharia',
 seo_desc='Laudos técnicos de caminhão munck, escavadeiras, retroescavadeiras, empilhadeiras e plataformas elevatórias, com ART. Parnamirim/RN e atendimento em todo o Brasil.',
 kw='laudo técnico de máquinas pesadas',
 content=P('A CROM Engenharia emite <strong>laudos técnicos de máquinas pesadas</strong> elaborados por engenheiros mecânicos. Com fotos, vídeos e checklists, avaliamos as condições de <strong>segurança, desempenho e conformidade</strong> do equipamento com as normas vigentes, incluindo a NR-12.')
 +H('Equipamentos que avaliamos')
 +UL(['Caminhão munck','Escavadeiras','Retroescavadeiras','Empilhadeiras','Plataformas elevatórias','Outras máquinas e equipamentos pesados'])
 +H('Quando o laudo é necessário?')
 +UL(['Na compra ou venda de máquinas usadas','Depois de acidentes, impactos ou sinais de trincas e deformações','Após reparos estruturais ou modificações','Para adequação às normas de segurança e exigências de clientes e fiscalização'])
 +P(f'Veja todos os casos em {A("laudo-tecnico-maquinas-pesadas","Laudo técnico de máquinas pesadas: quando é necessário")}.')
 +H('Laudo técnico e NR-12')
 +P(f'A NR-12 define requisitos de segurança para máquinas e equipamentos. O laudo ajuda a identificar o que precisa ser adequado e a planejar manutenções preventivas e corretivas. Saiba mais em {A("nr-12-para-maquinas","NR-12 para máquinas: quando é obrigatório")}.')
 +FAQ([('O laudo é emitido com ART?','Sim. Os laudos são elaborados por engenheiros mecânicos habilitados, com emissão de ART.'),
  ('Vocês atendem em outras cidades?','Sim. Estamos em Parnamirim/RN e atendemos empresas em todo o Brasil.')])
 +SOBRE+CTA('Precisa de um laudo para sua máquina?')))
for p in pages:
  open(f"{OUT}/{p['slug']}.html",'w').write(p['content'])
  assert p['content'].count('<!-- wp:')==p['content'].count('<!-- /wp:'), p['slug']
  print(p['slug'],len(p['seo_title']),len(p['seo_desc']),len(p['content'].split()),'words')
json.dump(pages,open(f'{OUT}/paginas.json','w'),ensure_ascii=False,indent=1)
