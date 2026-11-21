(function () {
  'use strict';
  var root = document.documentElement;

  /* ── Day / Night (default Night; choice saved in localStorage) ─ */
  var themeBtns = document.querySelectorAll('#themes button');
  function curTheme() { return root.dataset.theme === 'light' ? 'light' : 'dark'; }
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
  paintTheme();

  /* ── Hero carousel ───────────────────────────────────────────── */
  var hero = document.getElementById('home');
  var slides = hero ? Array.prototype.slice.call(hero.querySelectorAll('.hero-slide')) : [];
  if (slides.length) {
    var DUR = 6500, cur = 0, timer = null, paused = false;
    slides[0].parentNode.classList.add('ready'); // hands the first slide's visibility over to .on (CSS shows it without JS)
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

  /* ── Scroll reveal (home page, below the first screen) ───────── */
  if (hero && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var targets = [];
    ['series', 'releases', 'trade'].forEach(function (id) {
      var sec = document.getElementById(id);
      var wrap = sec && sec.querySelector('.wrap');
      if (!wrap) return;
      var items = wrap.classList.contains('trade') ? Array.prototype.slice.call(wrap.children) : Array.prototype.slice.call(wrap.children).filter(function (c) { return !c.querySelector('.card, .panel') && !c.classList.contains('series'); });
      items.forEach(function (c) { targets.push(c); });
      Array.prototype.forEach.call(sec.querySelectorAll('.card, .panel'), function (c) { targets.push(c); });
    });
    var vh = window.innerHeight;
    targets = targets.filter(function (el) { return el.getBoundingClientRect().top > vh * 0.92; });
    if (targets.length) {
      root.classList.add('js-rv');
      targets.forEach(function (el) { el.classList.add('rv'); });
      var io = new IntersectionObserver(function (entries) {
        var n = 0;
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          io.unobserve(el);
          el.style.setProperty('--rv-d', Math.min(n++ * 0.07, 0.35) + 's');
          el.classList.add('rv-in');
          setTimeout(function () { el.classList.remove('rv', 'rv-in'); el.style.removeProperty('--rv-d'); }, 1300);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      targets.forEach(function (el) { io.observe(el); });
    }
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

  /* ── B2BKing bulk order form (My account): refresh the header mini-cart after "Add" ──
     B2BKing signals via jQuery events (wc_fragment_refresh / added_to_cart); the block mini-cart only
     listens to the DOM event "wc-blocks_added_to_cart". */
  var bridgeTimer;
  function refreshMiniCart() {
    clearTimeout(bridgeTimer);
    bridgeTimer = setTimeout(function () {
      document.body.dispatchEvent(new CustomEvent('wc-blocks_added_to_cart', { bubbles: true, detail: { preserveCartData: false } }));
    }, 150);
  }
  if (window.jQuery && document.querySelector('.woocommerce-MyAccount-content, .account-page')) {
    window.jQuery(document.body).on('wc_fragment_refresh added_to_cart', refreshMiniCart);
  }

  /* ── Bulk order form: minimum quantity per line = one pack of 10 ── */
  var BULK_MIN = 10, BULK_QTY = '.b2bking_bulkorder_form_container_content_line_qty';
  function bulkClamp(i) {
    var max = parseInt(i.max, 10);
    if (i.disabled || i.type === 'hidden' || (!isNaN(max) && max < BULK_MIN)) { return; } // sold out / less than a pack in stock
    var v = parseInt(i.value, 10);
    if (isNaN(v) || v < BULK_MIN) { i.value = BULK_MIN; }
    i.min = BULK_MIN;
  }
  var isPartner = function () { return document.body.classList.contains('i7-partner'); }; // shops & distributors only
  function bulkInit() { if (isPartner()) { document.querySelectorAll(BULK_QTY).forEach(bulkClamp); } }
  bulkInit();
  new MutationObserver(function (m) { if (isPartner() && document.querySelector(BULK_QTY + ':not([min="' + BULK_MIN + '"])')) { bulkInit(); } })
    .observe(document.body, { childList: true, subtree: true });
  // Before B2BKing reads the quantity on "Add" (capture phase runs ahead of its delegated handler).
  document.addEventListener('click', bulkInit, true);
})();
