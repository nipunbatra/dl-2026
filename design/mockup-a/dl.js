/* Mockup behaviour: light and dark switch (defaults to the system), copy-link anchors, optional scroll-spy and lecture filter. */
(function () {
  var root = document.documentElement, KEY = 'dl-mock-theme';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { v == null ? localStorage.removeItem(KEY) : localStorage.setItem(KEY, v); } catch (e) {} }
  var mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : { matches: false };
  function apply() {
    var t = get();
    if (t === 'light' || t === 'dark') root.setAttribute('data-theme', t); else root.removeAttribute('data-theme');
    var dark = t ? t === 'dark' : mq.matches;
    document.querySelectorAll('.mode').forEach(function (b) {
      b.setAttribute('aria-checked', String(dark));
      b.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }
  apply();
  if (mq.addEventListener) mq.addEventListener('change', apply);

  document.addEventListener('DOMContentLoaded', function () {
    apply();
    document.querySelectorAll('.mode').forEach(function (b) {
      b.addEventListener('click', function () { set(b.getAttribute('aria-checked') === 'true' ? 'light' : 'dark'); apply(); });
    });

    // Copy the address the section would have on the live course site.
    document.querySelectorAll('.anchor').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        var url = a.dataset.url;
        function done() { a.classList.add('copied'); setTimeout(function () { a.classList.remove('copied'); }, 1600); }
        try {
          navigator.clipboard.writeText(url).then(done, function () {});
        } catch (e) {}
        var target = document.getElementById(a.dataset.target);
        if (target) target.scrollIntoView({ block: 'start' });
      });
    });

    // Scroll-spy for single-page layouts.
    var spy = document.querySelectorAll('[data-spy] a[href^="#"]');
    if (spy.length && 'IntersectionObserver' in window) {
      var map = {};
      spy.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          spy.forEach(function (a) { a.removeAttribute('aria-current'); });
          var a = map[e.target.id]; if (a) a.setAttribute('aria-current', 'location');
        });
      }, { rootMargin: '-10% 0px -80% 0px' });
      Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
    }

    // Lecture filter: module chips plus a text search.
    var q = document.getElementById('lecture-search');
    var chips = document.querySelectorAll('.chip[data-module]');
    if (q || chips.length) {
      var mod = 'all';
      function filter() {
        var term = q ? q.value.trim().toLowerCase() : '';
        var shown = 0;
        document.querySelectorAll('[data-lecture]').forEach(function (el) {
          var ok = (mod === 'all' || el.dataset.module === mod) && (!term || el.textContent.toLowerCase().indexOf(term) !== -1);
          el.hidden = !ok; if (ok) shown++;
        });
        document.querySelectorAll('[data-module-block]').forEach(function (b) {
          b.hidden = !b.querySelector('[data-lecture]:not([hidden])');
        });
        var c = document.getElementById('lecture-count'); if (c) c.textContent = shown + (shown === 1 ? ' lecture' : ' lectures');
      }
      chips.forEach(function (c) {
        c.addEventListener('click', function () {
          mod = c.dataset.module;
          chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
          filter();
        });
      });
      if (q) q.addEventListener('input', filter);
    }
  });
})();
