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
