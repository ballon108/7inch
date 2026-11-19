(function () {
  'use strict';
  var root = document.documentElement;

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
  /* ── Mobile menu (hamburger) ─────────────────────────────────── */
  var menuBtn = document.querySelector('.menu-toggle');
  var siteHeader = document.querySelector('.site-header');
  if (menuBtn && siteHeader) {
    var setMenu = function (open) {
      siteHeader.classList.toggle('nav-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    menuBtn.addEventListener('click', function () { setMenu(!siteHeader.classList.contains('nav-open')); });
    siteHeader.querySelectorAll('.site-nav a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    matchMedia('(min-width: 783px)').addEventListener('change', function (e) { if (e.matches) setMenu(false); });
  }

  /* ── Card: quantity stepper + add to cart (AJAX, falls back to a normal POST) ── */
  document.querySelectorAll('.card-buy').forEach(function (f) {
    var input = f.querySelector('input[name=quantity]');
    f.querySelectorAll('.qty button').forEach(function (b) {
      b.addEventListener('click', function () {
        var min = parseInt(input.min, 10) || 1, max = parseInt(input.max, 10) || Infinity;
        var v = parseInt(input.value, 10) || min;
        input.value = Math.min(max, Math.max(min, v + parseInt(b.dataset.step, 10)));
      });
    });
    if (f.tagName !== 'FORM') return;
    f.addEventListener('submit', function (e) {
      var btn = f.querySelector('.card-add'), label = btn.textContent;
      e.preventDefault();
      var data = new FormData(f); data.append('add-to-cart', btn.value);
      btn.disabled = true;
      fetch(f.action, { method: 'POST', body: data, credentials: 'same-origin' }).then(function (r) {
        if (!r.ok) throw new Error('add failed');
        document.body.dispatchEvent(new CustomEvent('wc-blocks_added_to_cart', { bubbles: true, detail: { preserveCartData: false } }));
        btn.textContent = 'Added \u2713'; btn.classList.add('is-added');
        setTimeout(function () { btn.textContent = label; btn.classList.remove('is-added'); btn.disabled = false; }, 1800);
      }).catch(function () { f.submit(); });
    });
  });
})();
