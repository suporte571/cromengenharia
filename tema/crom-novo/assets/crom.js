(function () {
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
