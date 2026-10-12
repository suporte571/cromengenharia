"""Gera o conteúdo HTML (bloco wp:html) das páginas do layout novo.
Uso: python3 paginas.py <mediamap.json> <imagens_container.json> <saida.json>
"""
import json, sys, html

MM = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
CT = json.load(open(sys.argv[2]))  # {"escritorio": url, "almoxarifado": url}
U = 'https://cromengenharia.com'
WA = 'https://wa.me/5584991519641'
E = html.escape

def img(i, alt, size='large', cls='', eager=False, w=None):
    src = CT[i] if isinstance(i, str) else MM[i][size]
    a = '' if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}" alt="{E(alt)}"{a} decoding="async">'

def block(h):
    return '<!-- wp:html -->\n' + h.strip() + '\n<!-- /wp:html -->'

def phead(title, lead, crumbs, bg=None):
    cr = ' / '.join([f'<a href="{U}/">Início</a>'] + [f'<a href="{U}{c[1]}">{c[0]}</a>' if isinstance(c, tuple) else c for c in crumbs])
    b = img(bg, '', 'large', 'bg', eager=True) if bg else ''
    return f'<div class="phead">{b}<div class="wrap"><p class="crumbs">{cr}</p><h1>{title}</h1><p class="lead">{lead}</p></div></div>'

SVC = [
 ('estruturas-metalicas', 'Estruturas Metálicas', 'Projeto · fabricação · montagem', 1287, 'Cobertura em treliça metálica montada pela CROM',
  ['Galpões industriais e comerciais', 'Coberturas e estacionamentos', 'Mezaninos e escadas', 'Torres e suportes fotovoltaicos']),
 ('containers-metalicos', 'Containers Metálicos', 'Fabricação sob medida', 'escritorio', 'Container escritório de obra (ilustração)',
  ['Almoxarifado e depósito', 'Escritório de obra', 'Vestiário e apoio', 'Projetos personalizados']),
 ('linha-de-vida', 'Linha de Vida', 'NR-35 · trabalho em altura', 1286, 'Estrutura metálica em montagem sobre edifício',
  ['Projeto sob medida', 'Fornecimento e instalação', 'Inspeção inicial e periódica', 'Laudo e recertificação']),
 ('laudos-tecnicos-maquinas', 'Laudos de Máquinas', 'NR-12 · máquinas pesadas', 1272, 'Caminhão munck em operação de montagem',
  ['Caminhão munck', 'Escavadeiras e retroescavadeiras', 'Empilhadeiras', 'Plataformas elevatórias']),
]

def svc_cards():
    out = []
    for slug, name, tag, im, alt, bl in SVC:
        lis = ''.join(f'<li>{b}</li>' for b in bl)
        out.append(f'<a class="svc" href="{U}/{slug}/"><div class="ph">{img(im, alt, "ml")}</div><div class="tx"><span class="tag">{tag}</span><h3>{name}</h3><ul>{lis}</ul><span class="go">Ver serviço →</span></div></a>')
    return '<div class="svc-grid">' + ''.join(out) + '</div>'

OBRAS = [
 (1287, 'Cobertura em treliça metálica', 'Coberturas'), (952, 'Estacionamento coberto', 'Coberturas'),
 (1215, 'Escada metálica comercial', 'Escadas'), (1272, 'Içamento com caminhão munck', 'Montagem'),
 (1390, 'Cobertura de estacionamento', 'Coberturas'), (1259, 'Fabricação de treliças', 'Fabricação'),
 (1285, 'Cobertura com beiral metálico', 'Coberturas'), (1286, 'Estrutura sobre edifício', 'Montagem'),
 (1113, 'Montagem em terraço', 'Montagem'), (1394, 'Cobertura em área comercial', 'Coberturas'),
 (1399, 'Treliça pronta para montagem', 'Fabricação'), (1402, 'Marquise de fachada', 'Marquises'),
 (951, 'Cobertura com pilares metálicos', 'Coberturas'), (1288, 'Estrutura vista do alto', 'Montagem'),
 (1115, 'Cobertura em terraço', 'Coberturas'),
]

def obra(o):
    i, t, tipo = o
    return f'<figure class="obra" data-tipo="{E(tipo.lower())}">{img(i, t + " – obra da CROM Engenharia", "ml")}<figcaption><span class="t">{t}</span><span class="m">{tipo}</span></figcaption></figure>'

CLIENTES = [(364, 'SELF Engenharia'), (365, 'Shopping 10DEZ'), (367, 'Solar BR Coca-Cola'), (368, 'PROSENG Projetos e Serviços de Engenharia'), (369, 'CHJ Engenharia'), (748, 'Construtora Gaspar')]
def clientes():
    return '<div class="clients">' + ''.join(img(i, n, 'full') for i, n in CLIENTES) + '</div>'

REVIEW = f'''<div class="review-cta"><div><span class="stars" aria-hidden="true">★★★★★</span><h3>Já é cliente da CROM?</h3><p class="lead" style="font-size:1rem">Sua avaliação no Google ajuda outras empresas a conhecer nosso trabalho.</p></div>
<a class="btn btn-ink" href="https://www.google.com/maps/search/?api=1&amp;query=CROM+Engenharia+Parnamirim+RN" target="_blank" rel="noopener">Avaliar no Google</a></div>'''

NUMS = '''<div class="stripe" aria-hidden="true"></div><div class="nums"><div class="wrap">
<div><strong>+25</strong><span>anos de experiência</span></div><div><strong>ART</strong><span>em todos os projetos</span></div>
<div><strong>4</strong><span>linhas de serviço</span></div><div><strong>BR</strong><span>atendimento em todo o Brasil</span></div></div></div>'''

CTA_BAND = f'''<div class="band on-dark"><div class="wrap cta"><div><p class="eyebrow">Orçamento</p><h2>Não sabe qual solução é a ideal?</h2>
<p class="lead" style="margin-top:12px">Conte o que você precisa. Um engenheiro analisa e indica o caminho.</p></div>
<div class="btns"><a class="btn btn-y" href="{U}/contato/#orcamento">Falar com um engenheiro</a><a class="btn btn-o" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div></div></div>'''

# ---------------- HOME ----------------
home = f'''
<div class="hero">{img(1287, '', 'full', 'bg', eager=True)}<div class="wrap">
<p class="eyebrow">Estruturas metálicas · Containers · Linha de vida · Laudos</p>
<h1>Estruturas metálicas e containers <span>projetados, fabricados e montados</span> em Parnamirim/RN</h1>
<p class="lead">Engenharia própria, fábrica própria e equipe de montagem. Há mais de 25 anos atendendo indústrias, construtoras e empresas de todo o Brasil.</p>
<div class="btns"><a class="btn btn-y" href="{U}/contato/#orcamento">Solicitar orçamento</a><a class="btn btn-o" href="{U}/obras/">Ver obras realizadas</a></div>
<div class="spec"><span>CREA-RN <b>200005964-2</b></span><span>Projetos com <b>ART</b></span><span>Normas <b>NR-35 · NR-12 · ABNT</b></span></div>
</div></div>
{NUMS}
<div class="band band-mist"><div class="wrap"><div class="head"><p class="eyebrow">O que fazemos</p><h2>Soluções em aço, do projeto à entrega</h2>
<p class="lead">Cada serviço tem engenheiro responsável e documentação técnica. Escolha a solução e veja os detalhes.</p></div>{svc_cards()}</div></div>
<div class="band on-dark"><div class="wrap"><div class="head"><p class="eyebrow">Como trabalhamos</p><h2>Tudo dentro de casa</h2>
<p class="lead">Um único fornecedor do cálculo à montagem. Menos retrabalho, prazo controlado e responsabilidade técnica clara.</p></div>
<ol class="steps"><li><h3>Levantamento</h3><p>Visita técnica, medições e entendimento das cargas e do uso.</p></li><li><h3>Projeto e ART</h3><p>Modelagem, dimensionamento, detalhamento e ART do engenheiro.</p></li><li><h3>Fabricação</h3><p>Corte, dobra, solda e pintura na fábrica em Parnamirim/RN.</p></li><li><h3>Montagem</h3><p>Equipe própria em campo, com planejamento de içamento e segurança.</p></li></ol></div></div>
<div class="band"><div class="wrap"><div class="head"><p class="eyebrow">Obras realizadas</p><h2>Estruturas que já estão de pé</h2>
<p class="lead">Coberturas, escadas, estacionamentos e montagens executadas pela CROM.</p></div>
<div class="obras">{''.join(obra(o) for o in OBRAS[:6])}</div><p style="margin-top:28px"><a class="btn btn-ink" href="{U}/obras/">Ver todas as obras</a></p></div></div>
<div class="band band-mist"><div class="wrap why">{img(1259, 'Soldador fabricando treliça metálica na fábrica da CROM', 'large')}
<div><p class="eyebrow">Por que a CROM</p><h2>Fábrica e engenharia no mesmo endereço</h2><dl>
<div><dt>Fábrica própria</dt><dd>Controle de qualidade e prazo na fabricação, sem depender de terceiros.</dd></div>
<div><dt>Engenheiros responsáveis</dt><dd>Projetos, laudos e inspeções com ART e registro no CREA-RN.</dd></div>
<div><dt>Normas em dia</dt><dd>NR-35 para trabalho em altura, NR-12 para máquinas e normas ABNT de estruturas de aço.</dd></div>
<div><dt>Atendimento nacional</dt><dd>Base em Parnamirim/RN e equipe preparada para obras em todo o país.</dd></div></dl></div></div></div>
<div class="band"><div class="wrap"><div class="head"><p class="eyebrow">Clientes e parceiros</p><h2>Quem confia na CROM</h2></div>{clientes()}{REVIEW}</div></div>
<div class="band band-mist"><div class="wrap"><div class="head"><p class="eyebrow">Blog técnico</p><h2>Conteúdo para quem decide a obra</h2></div>
<!--POSTS--><p style="margin-top:28px"><a class="btn btn-ink" href="{U}/blog/">Ver todos os artigos</a></p></div></div>
{CTA_BAND}
'''

# ---------------- QUEM SOMOS ----------------
quem = f'''
{phead('Quem Somos', 'Engenharia mecânica e estruturas metálicas há mais de 25 anos, com fábrica em Parnamirim/RN.', ['Quem Somos'], 1272)}
<div class="band"><div class="wrap split"><div class="prose"><p class="eyebrow">Nossa empresa</p><h2>CROM Engenharia</h2>
<p>A CROM Engenharia oferece soluções para as mais diversas necessidades do mercado em <strong>estruturas metálicas e engenharia mecânica</strong>. Contamos com profissionais habilitados para atender, com segurança, projetos complexos e exigentes.</p>
<p>São mais de 25 anos de experiência atendendo empresas nacionais e multinacionais em todo o Brasil, a partir da nossa fábrica na BR-304, em Parnamirim/RN.</p>
<p class="note">CNPJ 34.629.759/0001-50 · CREA-RN 200005964-2</p></div>{img(1259, 'Fabricação de treliças metálicas na fábrica da CROM')}</div></div>
{NUMS}
<div class="band band-mist"><div class="wrap"><div class="mvv">
<div><h3>Missão</h3><p>Proporcionar aos nossos clientes soluções personalizadas, confiáveis e de qualidade superior, atendendo às suas necessidades e superando expectativas.</p></div>
<div><h3>Visão</h3><p>Ser reconhecida como empresa líder em engenharia mecânica, com ampla gama de serviços e um ambiente de trabalho onde a equipe é valorizada.</p></div>
<div><h3>Valores</h3><p>Profissionalismo, ética e integridade. Respeito a clientes, parceiros e colaboradores, transparência e busca constante pela excelência.</p></div></div></div></div>
<div class="band"><div class="wrap"><div class="head"><p class="eyebrow">Clientes e parceiros</p><h2>Quem confia na CROM</h2></div>{clientes()}</div></div>
<div class="band band-mist"><div class="wrap"><div class="head"><p class="eyebrow">Na prática</p><h2>Nossa equipe em obra</h2></div>
<div class="gallery">{img(1272, 'Montagem com caminhão munck', 'ml')}{img(1113, 'Montagem de estrutura em terraço', 'ml')}{img(1286, 'Estrutura metálica em montagem sobre edifício', 'ml')}</div></div></div>
{CTA_BAND}
'''

# ---------------- SERVIÇOS ----------------
servicos = f'''
{phead('Serviços', 'Estruturas metálicas, containers, linha de vida e laudos técnicos. Fábrica em Parnamirim/RN e atendimento em todo o Brasil.', ['Serviços'], 952)}
<div class="band"><div class="wrap">{svc_cards()}</div></div>
{CTA_BAND}
'''

# ---------------- PÁGINAS DE SERVIÇO ----------------
def faq(qs):
    return '<h2>Perguntas frequentes</h2><div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qs) + '</div>'

def svc_page(slug, h1, lead, bg, body, gallery, qs, nome):
    outros = ''.join(f'<a href="{U}/{s[0]}/">{s[1]}</a>' for s in SVC if s[0] != slug)
    gal = '<div class="gallery">' + ''.join(img(g[0], g[1], 'ml') for g in gallery) + '</div>'
    return f'''
<div class="phead">{img(bg, '', 'large', 'bg', eager=True)}<div class="wrap"><p class="crumbs"><a href="{U}/">Início</a> / <a href="{U}/servicos/">Serviços</a> / {nome}</p>
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="spec"><span>Fábrica em <b>Parnamirim/RN</b></span><span>Atendimento <b>em todo o Brasil</b></span><span>Engenheiro responsável com <b>ART</b></span></div></div></div>
<div class="band"><div class="wrap svc-detail"><div class="prose">{body}{gal}{faq(qs)}</div>
<aside class="aside"><div class="box"><p class="eyebrow">Orçamento</p><h3>Solicite uma proposta de {nome.lower()}</h3>
<div class="contact-lines"><div><span>WhatsApp</span>(84) 99151-9641</div><div><span>E-mail</span>comercial@cromengenharia.com</div></div>
<a class="btn btn-y" href="{U}/contato/#orcamento">Solicitar orçamento</a><a class="btn btn-o" href="{WA}" target="_blank" rel="noopener">Chamar no WhatsApp</a></div>
<div class="box-light"><p class="eyebrow">Outros serviços</p>{outros}</div></aside></div></div>
'''

def L(slug, t): return f'<a href="{U}/{slug}/">{t}</a>'

sp = {}
sp['estruturas-metalicas'] = svc_page('estruturas-metalicas', 'Estruturas metálicas em Parnamirim/RN',
 'Galpões, coberturas, mezaninos, marquises, escadas e torres. Do cálculo estrutural à montagem em campo, com ART.', 1287,
 f'''<p>A CROM Engenharia faz o <strong>projeto, a fabricação e a montagem de estruturas metálicas</strong> sob medida para indústrias, comércios, centros logísticos e obras em geral. Cuidamos de todas as etapas dentro de casa, sempre de acordo com as normas técnicas vigentes.</p>
<h2>O que fabricamos e montamos</h2><ul><li><strong>Galpões industriais e comerciais</strong>, com grandes vãos livres e possibilidade de ampliação</li><li><strong>Coberturas metálicas</strong> para áreas industriais, estacionamentos e pátios</li><li><strong>Mezaninos</strong> para ampliar a área útil sem nova construção</li><li><strong>Marquises</strong> e estruturas de fachada</li><li><strong>Escadas metálicas</strong> de diversos tipos</li><li><strong>Torres estaiadas e autoportantes</strong></li><li><strong>Suportes para placas fotovoltaicas</strong></li></ul>
<h2>Como funciona o nosso trabalho</h2><ol><li><strong>Levantamento e concepção:</strong> entendemos a necessidade, o local e as cargas.</li><li><strong>Projeto estrutural:</strong> modelagem, dimensionamento, ligações e detalhamento, com ART.</li><li><strong>Fabricação:</strong> corte, dobra, solda e tratamento anticorrosivo na nossa fábrica.</li><li><strong>Montagem:</strong> equipe própria em campo, com planejamento de içamento e segurança.</li></ol>
<p>Quer entender as etapas em detalhe? Leia {L('projeto-de-estrutura-metalica', 'Projeto de estrutura metálica: como funciona')}.</p>
<h2>Por que escolher estrutura metálica?</h2><p>Obra mais rápida, vãos maiores e canteiro mais limpo, porque boa parte do trabalho acontece na fábrica. Compare em {L('estrutura-metalica-ou-concreto', 'Estrutura metálica ou concreto: qual escolher')} e {L('galpao-metalico-vantagens-tipos', 'Galpão metálico: vantagens e tipos')}.</p>''',
 [(1390, 'Cobertura metálica de estacionamento'), (952, 'Estacionamento coberto com estrutura metálica'), (1215, 'Escada metálica comercial')],
 [('Quanto custa uma estrutura metálica?', f'O preço depende do tipo de estrutura, dos vãos, das cargas, do peso de aço e da montagem. Explicamos o cálculo em {L("quanto-custa-estrutura-metalica", "Quanto custa uma estrutura metálica")} e em {L("quanto-custa-galpao-estrutura-metalica", "Quanto custa um galpão metálico")}.'),
  ('Vocês atendem fora do Rio Grande do Norte?', 'Sim. A fábrica fica em Parnamirim/RN e atendemos empresas em todo o Brasil.'),
  ('O projeto acompanha ART?', 'Sim. Os projetos são desenvolvidos por engenheiros habilitados, com emissão de ART.')], 'Estruturas Metálicas')

sp['containers-metalicos'] = svc_page('containers-metalicos', 'Fabricação de containers metálicos',
 'Almoxarifado, escritório de obra, depósito, vestiário e projetos especiais. Também fazemos adaptações e reforços com projeto de engenharia.', 'escritorio',
 f'''<p>A CROM Engenharia <strong>fabrica containers metálicos</strong> sob medida para canteiros de obras, indústrias e empresas que precisam de espaços modulares resistentes e prontos para uso. Também fazemos <strong>adaptações e reforços estruturais</strong> com projeto de engenharia.</p>
<h2>Modelos que fabricamos</h2><ul><li><strong>Container almoxarifado</strong> para materiais e ferramentas: {L('container-almoxarifado-para-obra', 'veja medidas e como escolher')}</li><li><strong>Container escritório</strong> para obra: {L('container-escritorio-para-obra', 'o que ele precisa ter')}</li><li><strong>Container depósito</strong> para materiais e equipamentos</li><li><strong>Container vestiário e de apoio</strong> para equipes</li><li><strong>Containers personalizados</strong>, com layout, portas, janelas e instalações sob medida</li></ul>
<h2>Projeto e adaptação com engenharia</h2><p>Abrir portas e janelas, cortar painéis ou unir módulos altera a estrutura do container. Por isso, toda modificação passa por análise de engenharia. Entenda em {L('corte-container-maritimo-reforco-estrutural', 'Pode cortar container marítimo?')} e {L('container-com-porta-e-janela', 'Container com porta e janela')}.</p>
<h2>Medidas e instalação</h2><p>O modelo mais usado tem cerca de <span style="font-family:var(--mono)">6,00 × 2,40 m</span> ({L('container-6x240-medidas-capacidade', 'veja medidas e capacidade')}), mas fabricamos em outros tamanhos conforme a necessidade. A base também precisa ser planejada: saiba mais em {L('base-para-container-fundacao', 'Base para container: precisa de fundação?')}.</p>
<p class="note">Imagens de container: ilustração 3D.</p>''',
 [('escritorio', 'Container escritório de obra (ilustração)'), ('almoxarifado', 'Container almoxarifado com portas de carga (ilustração)'), (1259, 'Fabricação na fábrica da CROM')],
 [('Vocês fabricam containers sob medida?', 'Sim. Definimos tamanho, layout, aberturas e instalações de acordo com o uso: almoxarifado, escritório, depósito, vestiário ou projeto especial.'),
  ('Qual container é melhor para canteiro de obras?', f'Depende da função. Explicamos os principais modelos em {L("container-para-canteiro-de-obras", "Container para canteiro de obras")}.'),
  ('Vocês entregam fora do RN?', 'Sim. A fábrica fica em Parnamirim/RN e atendemos empresas em todo o Brasil.')], 'Containers Metálicos')

sp['linha-de-vida'] = svc_page('linha-de-vida', 'Linha de vida e sistemas de ancoragem',
 'Projeto, instalação, inspeção e recertificação de linhas de vida e pontos de ancoragem conforme a NR-35, com ART.', 1286,
 f'''<p>A <strong>linha de vida</strong> é um sistema de ancoragem que permite ao trabalhador se deslocar com segurança em altura, reduzindo o risco de quedas. A CROM faz o <strong>projeto, a instalação, a inspeção e a recertificação</strong> de linhas de vida e pontos de ancoragem, seguindo a NR-35 e as normas aplicáveis.</p>
<h2>Nossos serviços de linha de vida</h2><ul><li><strong>Projeto sob medida</strong> de linha de vida horizontal, vertical e para telhados</li><li><strong>Fornecimento e instalação</strong> de linhas de vida e pontos de ancoragem</li><li><strong>Inspeção inicial e periódica</strong></li><li><strong>Laudo técnico e recertificação</strong> de linhas existentes, com ART</li></ul>
<h2>Quando a linha de vida é obrigatória?</h2><p>Sempre que houver trabalho em altura e a análise de risco indicar um sistema de proteção contra quedas. Explicamos em {L('linha-de-vida-nr-35', 'Linha de vida NR-35: o que é e quando é obrigatória')}.</p>
<h2>Onde instalamos</h2><ul><li>Telhados e coberturas de galpões</li><li>Estruturas metálicas e plataformas industriais</li><li>Fachadas, escadas e acessos verticais</li><li>Áreas de manutenção de máquinas e equipamentos</li></ul>''',
 [(1286, 'Estrutura metálica em altura'), (1113, 'Montagem em terraço'), (1115, 'Cobertura metálica em terraço')],
 [('Quanto custa instalar uma linha de vida?', f'O valor depende do tipo de sistema, da extensão, da estrutura de fixação e da documentação. Veja os fatores em {L("quanto-custa-instalar-linha-de-vida", "Quanto custa instalar uma linha de vida")}.'),
  ('A linha de vida precisa de ART?', 'Sim. Projeto e instalação devem ser feitos sob responsabilidade de um profissional habilitado, com emissão de ART.'),
  ('Vocês fazem a inspeção de linhas já instaladas?', 'Sim. Fazemos inspeção periódica, laudo técnico e recertificação de linhas de vida existentes.')], 'Linha de Vida')

sp['laudos-tecnicos-maquinas'] = svc_page('laudos-tecnicos-maquinas', 'Laudo técnico de máquinas pesadas',
 'Laudos de caminhão munck, escavadeiras, retroescavadeiras, empilhadeiras e plataformas elevatórias, feitos por engenheiros mecânicos, com ART.', 1272,
 f'''<p>A CROM Engenharia emite <strong>laudos técnicos de máquinas pesadas</strong> elaborados por engenheiros mecânicos. Com fotos, vídeos e checklists, avaliamos as condições de <strong>segurança, desempenho e conformidade</strong> do equipamento com as normas vigentes, incluindo a NR-12.</p>
<h2>Equipamentos que avaliamos</h2><ul><li>Caminhão munck</li><li>Escavadeiras</li><li>Retroescavadeiras</li><li>Empilhadeiras</li><li>Plataformas elevatórias</li><li>Outras máquinas e equipamentos pesados</li></ul>
<h2>Quando o laudo é necessário?</h2><ul><li>Na compra ou venda de máquinas usadas</li><li>Depois de acidentes, impactos ou sinais de trincas e deformações</li><li>Após reparos estruturais ou modificações</li><li>Para adequação às normas de segurança e exigências de clientes e fiscalização</li></ul>
<p>Veja todos os casos em {L('laudo-tecnico-maquinas-pesadas', 'Laudo técnico de máquinas pesadas: quando é necessário')}.</p>
<h2>Laudo técnico e NR-12</h2><p>A NR-12 define requisitos de segurança para máquinas e equipamentos. O laudo ajuda a identificar o que precisa ser adequado e a planejar manutenções preventivas e corretivas. Saiba mais em {L('nr-12-para-maquinas', 'NR-12 para máquinas: quando é obrigatório')}.</p>''',
 [(1272, 'Caminhão munck em operação'), (1288, 'Estrutura metálica vista do alto'), (1259, 'Inspeção e solda de estrutura')],
 [('O laudo é emitido com ART?', 'Sim. Os laudos são elaborados por engenheiros mecânicos habilitados, com emissão de ART.'),
  ('Vocês atendem em outras cidades?', 'Sim. Estamos em Parnamirim/RN e atendemos empresas em todo o Brasil.')], 'Laudos de Máquinas')

# ---------------- OBRAS ----------------
tipos = ['Todas'] + sorted(set(o[2] for o in OBRAS), key=lambda t: [x[2] for x in OBRAS].index(t))
chips = ''.join(f'<button class="chip" type="button" data-tipo="{E(t.lower())}" aria-pressed="{"true" if t == "Todas" else "false"}">{t}</button>' for t in tipos)
obras = f'''
{phead('Obras realizadas', 'Coberturas, escadas, estacionamentos, marquises e montagens executadas pela CROM Engenharia.', ['Obras'], 1390)}
<div class="band"><div class="wrap"><div class="chips" id="obraChips" role="group" aria-label="Filtrar obras por tipo">{chips}</div>
<div class="obras" id="allObras">{''.join(obra(o) for o in OBRAS)}</div></div></div>
{CTA_BAND}
'''

# ---------------- CONTATO ----------------
contato_a = f'''
{phead('Contato e orçamento', 'Respondemos em horário comercial. Para agilizar, conte o tipo de serviço, a cidade e as medidas aproximadas.', ['Contato'], 951)}
<div class="band"><div class="wrap contact"><div>
'''
contato_b = f'''
</div><div style="display:grid;gap:20px">
<div class="box"><p class="eyebrow">Fale direto</p><div class="contact-lines">
<div><span>WhatsApp comercial</span>(84) 99151-9641</div><div><span>Telefones</span>(84) 99650-7337 · (84) 99106-0289</div>
<div><span>E-mail</span>comercial@cromengenharia.com</div><div><span>Fábrica</span>BR-304, Km 507, s/n · Encanto Verde<br>Parnamirim/RN · 59146-750</div></div>
<a class="btn btn-y" href="{WA}" target="_blank" rel="noopener">Chamar no WhatsApp</a></div>
<div class="map"><div><strong>Como chegar</strong><p class="note">BR-304, Km 507 · Parnamirim/RN</p><p style="margin-top:10px"><a class="btn btn-ink" href="https://www.google.com/maps/search/?api=1&amp;query=BR-304+Km+507+Encanto+Verde+Parnamirim+RN" target="_blank" rel="noopener">Abrir no Google Maps</a></p></div></div>
</div></div></div>
'''
contato = block(contato_a) + '\n\n<!-- wp:shortcode -->\n[crom_orcamento]\n<!-- /wp:shortcode -->\n\n' + block(contato_b)

out = {
 'home': block(home), 'quem-somos': block(quem), 'servicos': block(servicos), 'obras': block(obras), 'contato': contato,
 **{k: block(v) for k, v in sp.items()},
}
json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False)
for k, v in out.items():
    assert v.count('<!-- wp:') == v.count('<!-- /wp:'), k
    print(k, len(v))
