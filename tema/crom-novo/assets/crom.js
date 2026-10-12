(function () {
  // ---------- Medição de contatos (GA4) e origem do visitante ----------
  function ev(nome, params) {
    if (typeof window.gtag === 'function') window.gtag('event', nome, params || {});
  }
  function ler(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function gravar(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  // Origem: guardada na primeira visita (vale 30 dias) e enviada junto com o pedido de orçamento.
  (function () {
    var o = ler('crom_origem');
    if (o && Date.now() - o.t < 30 * 864e5) return;
    var q = new URLSearchParams(location.search), ref = document.referrer, fonte;
    var host = '';
    try { host = ref ? new URL(ref).hostname.replace(/^www\./, '') : ''; } catch (e) {}
    if (host === location.hostname.replace(/^www\./, '')) return;
    if (q.get('gclid')) fonte = 'Google Ads';
    else if (q.get('utm_source')) fonte = [q.get('utm_source'), q.get('utm_medium'), q.get('utm_campaign')].filter(Boolean).join(' / ');
    else if (!host) fonte = 'Direto (digitou o endereço ou link salvo)';
    else if (/google\./.test(host)) fonte = 'Google (busca)';
    else if (/bing\.|yahoo\.|duckduckgo/.test(host)) fonte = 'Outros buscadores (' + host + ')';
    else if (/instagram/.test(host)) fonte = 'Instagram';
    else if (/facebook|fb\./.test(host)) fonte = 'Facebook';
    else if (/linkedin|lnkd/.test(host)) fonte = 'LinkedIn';
    else if (/whatsapp|wa\.me/.test(host)) fonte = 'WhatsApp';
    else fonte = 'Site ' + host;
    gravar('crom_origem', { t: Date.now(), fonte: fonte, entrada: location.pathname });
  })();
  function origemTexto() {
    var o = ler('crom_origem');
    return o ? o.fonte + ' · entrou por ' + o.entrada : 'não identificada';
  }

  var fo = document.getElementById('f-origem');
  if (fo) fo.value = origemTexto();

  // Cliques em WhatsApp, telefone e e-mail contam como contato gerado.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '', m = null;
    if (/^https?:\/\/(api\.)?(wa\.me|whatsapp\.com)/.test(h)) m = 'whatsapp';
    else if (/^tel:/.test(h)) m = 'telefone';
    else if (/^mailto:/.test(h)) m = 'email';
    if (!m) return;
    var area = a.closest('header,footer,.box,.hero,.wa,form') ;
    ev('generate_lead', { contact_method: m, link_location: area ? (area.className || area.tagName).toString().split(' ')[0].toLowerCase() : 'conteudo' });
  }, true);

  // Pedido de orçamento enviado com sucesso (conta uma vez por envio).
  if (/[?&]enviado=1/.test(location.search) && document.querySelector('form.quote .ok')) {
    var marca = 'crom_lead_' + location.search;
    var ja = false;
    try { ja = sessionStorage.getItem(marca); sessionStorage.setItem(marca, '1'); } catch (e) {}
    if (!ja) ev('generate_lead', { contact_method: 'formulario', link_location: 'contato' });
  }

  var t = document.getElementById('menuToggle'), n = document.getElementById('mainNav');
  if (t && n) {
    t.addEventListener('click', function () {
      var o = n.classList.toggle('open');
      t.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
  }

  // Índice do post a partir dos H2 do conteúdo.
  var toc = document.getElementById('toc'), prose = document.getElementById('prose');
  if (toc && prose) {
    var hs = prose.querySelectorAll(':scope > h2, :scope > .wp-block-heading');
    var n2 = 0;
    hs.forEach(function (h, i) {
      if (h.tagName !== 'H2' || h.closest('.box')) return;
      if (!h.id) h.id = 'secao-' + (i + 1);
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent.trim();
      toc.appendChild(a);
      n2++;
    });
    if (!n2) toc.hidden = true;
  }

  // Envio do orçamento pelo navegador. A hospedagem às vezes responde ao primeiro envio com uma
  // verificação em JavaScript (define um cookie e recarrega); aqui aplicamos o cookie e reenviamos,
  // como o navegador faria, sem o aviso de "reenviar formulário".
  var form = document.querySelector('form.quote');
  if (form && window.fetch && window.FormData) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      if (btn) { btn.disabled = true; btn.textContent = 'Enviando…'; }
      var dados = new FormData(form);
      dados.set('origem', origemTexto());
      var enviar = function (tentativa) {
        return fetch(form.action, { method: 'POST', body: dados, credentials: 'same-origin', redirect: 'follow' })
          .then(function (r) {
            if (/[?&]enviado=/.test(r.url)) { window.location.href = r.url; return; }
            return r.text().then(function (t) {
              var m = t.match(/document\.cookie\s*=\s*"([^"]+)"/);
              if (m && tentativa < 2) { document.cookie = m[1] + '; path=/'; return enviar(tentativa + 1); }
              throw new Error('resposta inesperada');
            });
          });
      };
      enviar(0).catch(function () { form.submit(); });
    });
  }

  // Filtro da página de obras.
  var chips = document.getElementById('obraChips'), grid = document.getElementById('allObras');
  if (chips && grid) {
    chips.addEventListener('click', function (e) {
      var b = e.target.closest('.chip');
      if (!b) return;
      chips.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c === b ? 'true' : 'false'); });
      var tipo = b.getAttribute('data-tipo');
      grid.querySelectorAll('.obra').forEach(function (o) {
        o.hidden = !(tipo === 'todas' || o.getAttribute('data-tipo') === tipo);
      });
    });
  }
})();
