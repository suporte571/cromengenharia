# Guia: Velocidade do site + Google Search Console

Situação medida no celular (Lighthouse): Home **34/100** (LCP 7,3 s, 5,4 MB) · páginas de serviço **64/100** · posts **72/100**.
Meta: acima de 80 e LCP abaixo de 2,5 s.

Faça **um passo de cada vez** e confira o site depois de cada um, sem esquecer da versão no celular. Se algo quebrar, desfaça só o último passo.

---

## Parte 1: Velocidade

### Passo 1: Atualize o PHP (5 min, ganho médio)
1. Entre no **cPanel da HostGator** → **Selecionar versão do PHP** (ou *MultiPHP Manager*).
2. Escolha **PHP 8.2** ou **8.3** para `cromengenharia.com` e salve.
3. Abra o site e confira se está tudo normal.

### Passo 2: Plugin de cache (10 min, ganho alto)
O servidor da HostGator é Apache, então o plugin *LiteSpeed Cache* não funciona nele.
1. **Plugins → Adicionar novo** → instale e ative o **WP Super Cache** (gratuito e simples).
2. **Configurações → WP Super Cache → Cache ativado → Atualizar status**.
3. Na aba **Avançado**, marque **"Comprimir páginas"** e **"Não colocar em cache para usuários conhecidos"**.
> Alternativa paga e mais completa: **WP Rocket**, que também faz o lazy load e a minificação dos passos 4 e 5.

### Passo 3: Imagens em WebP (15 min, o maior ganho)
1. Instale o **Converter for Media** (gratuito).
2. Em **Configurações → Converter for Media**: formato **WebP**, qualidade **80%**, depois clique em **"Iniciar otimização em massa"**.
3. As imagens dos posts são PNG de cerca de 1 MB. Daqui para frente, **antes de subir uma imagem**, salve em JPG/WebP com **no máximo 1600 px de largura**. Pode usar o site squoosh.app.

### Passo 4: Configurações do Elementor (5 min, ganho alto)
**Elementor → Configurações → Recursos** (*Features*). Ative:
- **Optimized DOM Output**
- **Improved Asset Loading**
- **Improved CSS Loading**
- **Lazy Load Background Images**
- **Element Caching** (se aparecer)

Depois vá em **Elementor → Configurações → Desempenho** (*Performance*), ative o carregamento local do **Google Fonts** e escolha `font-display: swap`.
Por fim, **Elementor → Ferramentas → Limpar arquivos e dados**.

### Passo 5: Troque o slider da Home (20 min, ganho alto no LCP)
O **Prime Slider** carrega várias imagens e scripts antes de mostrar a página. É o principal motivo da nota 34.
1. Edite a Home com o Elementor.
2. Troque o slider por uma **seção com UMA imagem de fundo otimizada** (WebP, até 200 KB), com o título e o botão "Solicite um orçamento".
3. O título principal (H1) da Home deve ser algo como: **"Estruturas Metálicas e Containers em Parnamirim/RN"**.
4. Depois, desative o plugin **Prime Slider** em Plugins.

### Passo 6: Limpe os plugins (10 min)
- **Premium Addons for Elementor:** em *Premium Addons → Widgets*, desative todos os que não estão em uso. A seção de depoimentos que usava esse plugin já foi removida.
- Apague plugins desativados que não serão mais usados.

### Passo 7: Cloudflare gratuito (30 min, ganho alto + segurança)
1. Crie uma conta em **cloudflare.com** → **Add a site** → `cromengenharia.com` → plano **Free**.
2. A Cloudflare mostra **2 nameservers**. No painel da HostGator, em **Domínios → cromengenharia.com → Nameservers**, troque pelos 2 da Cloudflare.
   - ⚠️ Antes, confira na Cloudflare se os registros de **e-mail (MX)** foram importados, para o e-mail `comercial@` não parar.
3. Na Cloudflare:
   - **SSL/TLS → Full**
   - **Speed → Optimization**: ative **Brotli**, **Early Hints** e **HTTP/3**
   - **Caching → Browser Cache TTL**: 1 mês
4. Opcional, cerca de US$ 5/mês: **Cloudflare APO para WordPress**. Faz cache da página inteira e costuma melhorar muito o tempo de resposta.

---

## Parte 2: Google Search Console (15 min)

Com o Search Console, você vê **quais buscas trazem visitas**, pede ao Google para ler as páginas novas e recebe alertas de erro.

1. Acesse **search.google.com/search-console** com a conta Google da empresa.
2. **Adicionar propriedade** → escolha **"Prefixo do URL"** → digite `https://cromengenharia.com/`.
3. Em métodos de verificação, escolha **"Tag HTML"** e copie o código que aparece. É o trecho dentro de `content="..."`, algo como `aBcD123...`.
4. **Me envie esse código.** Eu coloco no Rank Math, ou você mesmo cola em **Rank Math → Configurações gerais → Ferramentas para Webmasters → Google Search Console**.
5. Volte ao Search Console e clique em **Verificar**.
6. No menu **Sitemaps**, adicione `sitemap_index.xml` e clique em **Enviar**.
7. Em **Inspeção de URL**, cole cada página nova e clique em **"Solicitar indexação"**:
   - https://cromengenharia.com/estruturas-metalicas/
   - https://cromengenharia.com/containers-metalicos/
   - https://cromengenharia.com/linha-de-vida/
   - https://cromengenharia.com/laudos-tecnicos-maquinas/

**Extra (muito importante para SEO local):** crie ou revise o **Perfil da Empresa no Google** (business.google.com), com o endereço da BR-304, Km 507, em Parnamirim, fotos da fábrica e das obras, horário e o link do site. Peça avaliações aos clientes.
