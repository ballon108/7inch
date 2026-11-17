(function () {
  'use strict';
  var root = document.documentElement;

  /* ── Day / Night ─────────────────────────────────────────────── */
  var themeBtns = document.querySelectorAll('#themes button');
  function curTheme() {
    return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  function paintTheme() {
    var c = curTheme();
    themeBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.th === c); });
    window.dispatchEvent(new Event('themechange'));
  }
  themeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      root.dataset.theme = b.dataset.th;
      try { localStorage.setItem('theme', b.dataset.th); } catch (e) {}
      paintTheme();
    });
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', paintTheme);
  paintTheme();

  /* ── Hero carousel ───────────────────────────────────────────── */
  var hero = document.getElementById('home');
  var slides = hero ? Array.prototype.slice.call(hero.querySelectorAll('.hero-slide')) : [];
  if (slides.length) {
    var DUR = 6500, cur = 0, timer = null, paused = false;
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var ARROW_L = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>';
    var ARROW_R = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>';

    slides.forEach(function (s) {
      var box = s.querySelector('.dots');
      if (!box) return;
      box.style.setProperty('--dur', DUR + 'ms');
      slides.forEach(function (t, i) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'dot';
        b.setAttribute('aria-label', t.getAttribute('data-title') || ('Slide ' + (i + 1)));
        b.innerHTML = '<span><b></b></span>';
        b.addEventListener('click', function () { go(i); });
        box.appendChild(b);
      });
      var ar = document.createElement('div');
      ar.className = 'arrows';
      ar.innerHTML = '<button type="button" aria-label="Previous" data-dir="-1">' + ARROW_L + '</button><button type="button" aria-label="Next" data-dir="1">' + ARROW_R + '</button>';
      ar.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () { go(cur + parseInt(b.dataset.dir, 10)); });
      });
      box.appendChild(ar);
    });

    function go(i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, j) {
        s.classList.toggle('on', j === cur);
        s.setAttribute('aria-hidden', j === cur ? 'false' : 'true');
        s.querySelectorAll('.dot').forEach(function (d, k) {
          d.classList.toggle('on', k === cur && j === cur);
          d.classList.toggle('done', k < cur);
          var b = d.querySelector('b'); b.style.animation = 'none'; void b.offsetWidth; b.style.animation = '';
        });
      });
      schedule();
    }
    function schedule() {
      clearTimeout(timer);
      if (reduce || paused) return;
      timer = setTimeout(function () { go(cur + 1); }, DUR);
    }
    function pause(p) {
      paused = p; hero.classList.toggle('paused', p);
      if (p) clearTimeout(timer); else schedule();
    }
    hero.addEventListener('mouseenter', function () { pause(true); });
    hero.addEventListener('mouseleave', function () { pause(false); });
    hero.addEventListener('focusin', function () { pause(true); });
    hero.addEventListener('focusout', function () { pause(false); });
    var tx = null;
    hero.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (tx == null) return;
      var dx = e.changedTouches[0].clientX - tx;
      if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
      tx = null;
    });
    go(0);
  }

  /* ── Catalogue filter ────────────────────────────────────────── */
  var filterBtns = document.querySelectorAll('.filters .wp-block-button');
  var cards = document.querySelectorAll('#releases .card');
  function setFilter(f) {
    filterBtns.forEach(function (b) { b.classList.toggle('is-active', b.classList.contains('f-' + f)); });
    cards.forEach(function (c) { c.classList.toggle('is-hidden', f !== 'all' && !c.classList.contains('rel-' + f)); });
  }
  filterBtns.forEach(function (b) {
    var link = b.querySelector('a');
    link.addEventListener('click', function (e) {
      e.preventDefault();
      setFilter(b.classList.contains('f-mp') ? 'mp' : b.classList.contains('f-lr') ? 'lr' : 'all');
    });
  });
  document.querySelectorAll('.panel').forEach(function (p) {
    p.addEventListener('click', function () {
      setFilter(p.classList.contains('mp') ? 'mp' : 'lr');
      var t = document.getElementById('releases');
      if (t) t.scrollIntoView();
    });
  });
  /* ── Partner application: distributor-only fields ────────────── */
  var pForm = document.querySelector('.pf-form');
  if (pForm) {
    var syncType = function () {
      var r = pForm.querySelector('input[name="apply_as"]:checked');
      var dist = r && r.value === 'Distributor';
      pForm.querySelectorAll('.pf-dist').forEach(function (el) { el.hidden = !dist; });
    };
    pForm.addEventListener('change', function (e) { if (e.target.name === 'apply_as') syncType(); });
    syncType();
  }
})();
