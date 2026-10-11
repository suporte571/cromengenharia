# Auditoria de SEO e Performance: cromengenharia.com

Data: 11/10/2026. Foram analisadas todas as 6 páginas e os 19 posts publicados, acessados direto do site e pela API do WordPress. A velocidade foi medida com o Lighthouse no modo celular.

## Resumo

O blog tem uma boa base: posts longos (2.500 a 3.700 palavras), títulos e meta descriptions bem escritos no Rank Math, Schema `BlogPosting`, sitemap e robots.txt corretos.
Os principais problemas são **links internos inexistentes**, **velocidade da Home no celular**, **páginas de serviço fracas** e **conteúdo de teste publicado**.

| Página | Nota mobile | LCP | Peso total |
|---|---|---|---|
| Home | **34/100** | 7,3 s | 5,4 MB |
| Post (linha-de-vida-nr-35) | 72/100 | 4,6 s | 774 KB |

Meta: nota acima de 80 e LCP abaixo de 2,5 s.

---

## 🔴 Crítico (corrigir primeiro)

1. **Depoimentos com "Lorem ipsum" na Home.** A seção "Feedback de nossos clientes" está com o texto de exemplo do modelo, o que passa uma imagem amadora. Troque por depoimentos reais ou remova a seção.
2. **Páginas de teste do WordPress indexadas no Google:**
   - `/hello-world/` ("Hello world!")
   - `/sample-page/` ("Sample Page")
   → Apagar as duas e criar um redirecionamento 301 para `/blog/` e `/` (Rank Math → Redirecionamentos).
3. **Nenhum link interno nos 18 posts.** Nenhum post linka para outro post nem para a página de Serviços/Contato. É a maior oportunidade de ganho rápido:
   - cada post deve linkar para a página do serviço relacionado e para 2 ou 3 posts do mesmo tema;
   - cada post deve terminar com um bloco de chamada: "Solicite um orçamento / Fale com um engenheiro".
4. **Home lenta no celular (34/100).** São 5,4 MB por visita, cerca de 1 MB só em imagens fora do formato WebP e 1,4 s de JavaScript bloqueando a página. Veja a seção "Performance" abaixo.
5. **100% das imagens estão sem texto alternativo (alt).** São 100 de 100 na biblioteca de mídia, incluindo as imagens de destaque de todos os posts.

## 🟠 Importante

6. **Páginas de serviço fracas.** Existe uma única página `/servicos/` para três serviços diferentes. O ideal é uma página para cada um:
   - `/estruturas-metalicas/` (galpões, coberturas, mezaninos, marquises, torres, suportes fotovoltaicos)
   - `/linha-de-vida/` (linha de vida e sistemas de ancoragem NR-35)
   - `/laudo-tecnico-maquinas-pesadas/` (laudos e NR-12)
   - **Containers:** 8 dos 18 posts falam de container, mas o site não oferece esse serviço em lugar nenhum. Se vocês fazem adaptação, reforço ou fabricação de containers, falta a página do serviço. Se não fazem, esses posts atraem visitas que não viram clientes.
7. **Título/H1 das páginas principais:**
   - Home: o H1 é "oferecemos soluções inovadoras e eficientes", sem nenhuma palavra-chave. Sugestão: "Estruturas Metálicas, Linha de Vida e Laudos Técnicos no RN".
   - Serviços, Quem Somos, Contato e Blog **não têm H1**.
   - Posts com mais de um H1: *estrutura-metalica-ou-concreto* (**18 H1**), *container-para-canteiro-de-obras* (3), *galpao-metalico-vantagens-tipos* (2), *container-6x240* (2). Os H1 extras devem virar H2.
8. **Meta descriptions ruins:**
   - Serviços: "conheça os serviços oferecidos pela crom engenharia" (51 caracteres, tudo em minúsculas)
   - Contato: gerada automaticamente com telefones misturados
   - Quem Somos: texto genérico cortado
9. **SEO local inexistente.** Não aparece endereço nem cidade em nenhuma página, apenas o DDD (84) e o CREA-RN.
   - Rank Math → Títulos e Meta → **Local SEO**: preencher como `LocalBusiness` com endereço, cidade, telefone, horário e área atendida.
   - Incluir "Natal/RN" (ou a cidade-base) e "atendemos todo o Brasil" nos títulos das páginas de serviço.
   - Criar e completar o **Perfil da Empresa no Google**.
10. **Imagem de compartilhamento (og:image) ausente** em Home, Blog e Contato. Isso afeta a aparência dos links no WhatsApp e no LinkedIn.
11. **Posts competindo pela mesma palavra-chave (canibalização):**
    - `quanto-custa-estrutura-metalica` × `estrutura-metalica-preco-m2`: o mesmo assunto em dois posts. Junte num só e redirecione o outro com 301.
    - `quanto-custa-galpao-estrutura-metalica` × `galpao-metalico-vantagens-tipos`: as intenções de busca são diferentes, então pode manter os dois, mas com links de um para o outro.

## 🟡 Ajustes rápidos

- Erro de digitação em Serviços: "Escadas de **divertimos** tipos" → "diversos tipos".
- Rodapé com "Copyright 2025" → usar o ano atual ou "2025–2026".
- Formatos das imagens: 59 PNG, 32 JPG e apenas 5 WebP.

---

## Performance (HostGator + Elementor)

O que pesa hoje: tema Astra + **Elementor + Elementor Pro + Premium Addons + Prime Slider**, com 29 a 33 scripts e 28 a 43 folhas de estilo por página. O servidor é Apache, sem cache de página e com resposta de cerca de 600 ms.

Em ordem de impacto:
1. **Cache de página:** LiteSpeed Cache, se o plano HostGator tiver LiteSpeed, ou WP Rocket / W3 Total Cache.
2. **Imagens:** converter tudo para WebP e redimensionar (ShortPixel, Imagify ou Converter for Media). Ganho estimado de cerca de 1,2 MB na Home.
3. **Trocar o slider (Prime Slider) da Home** por uma imagem fixa otimizada. Sliders costumam ser o maior vilão do LCP.
4. **Elementor → Configurações → Recursos:** ativar "Optimized DOM Output", "Improved Asset Loading", "Improved CSS Loading" e "Lazy Load Background Images".
5. **Premium Addons:** desativar todos os widgets que não estão em uso. Se der, remover o plugin.
6. **Cloudflare gratuito** (CDN + HTTP/3) e **PHP 8.2 ou mais novo** no cPanel.
7. Carregar as fontes (Inter e Plus Jakarta Sans) localmente, com `font-display: swap`.

---

## Plano de ação sugerido

| Etapa | O que | Quem |
|---|---|---|
| 1 | Remover Lorem ipsum, apagar Hello World/Sample Page + redirecionamentos 301, corrigir erro de digitação | Claude (com Senha de Aplicativo) ou você |
| 2 | Links internos + bloco de orçamento em todos os 18 posts, corrigir H1 duplicados, preencher alt das imagens | Claude, via API |
| 3 | Criar páginas individuais de serviço, otimizadas | Claude escreve, você aprova |
| 4 | Juntar os posts canibalizados + redirecionamento 301 | Claude |
| 5 | Cache, WebP, slider, configurações do Elementor, Cloudflare | Você no painel (com guia passo a passo) |
| 6 | Local SEO no Rank Math + Perfil da Empresa no Google | Você, com os dados da empresa |
| 7 | Novos posts sobre os serviços que faturam mais | Contínuo |
