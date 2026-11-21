(function () {
  var root = document.documentElement;

  /* ---------- Varianten (nur Prototyp) ---------- */
  var KEY = 'assistentium-proto';
  var defaults = { farbe: 'waldgruen', schrift: 'atkinson' };
  var state = Object.assign({}, defaults);
  try { Object.assign(state, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
  var params = new URLSearchParams(location.search);
  ['farbe', 'schrift'].forEach(function (k) { if (params.get(k)) state[k] = params.get(k); });
  function apply() {
    root.setAttribute('data-farbe', state.farbe);
    root.setAttribute('data-schrift', state.schrift);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }
  apply();

  document.addEventListener('DOMContentLoaded', function () {
    /* Menü */
    var nav = document.getElementById('nav');
    var btn = document.querySelector('.menu-btn');
    var desktop = window.matchMedia('(min-width: 1040px)');
    function setMenu(open) {
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = open ? 'Schließen' : 'Menü';
      nav.hidden = !open && !desktop.matches;
    }
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    desktop.addEventListener('change', function () { setMenu(false); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && !desktop.matches) setMenu(false); });
    setMenu(false);

    /* Imagefilm: Zwei-Klick-Lösung, YouTube lädt erst nach Klick */
    var video = document.getElementById('video');
    var start = document.getElementById('video-start');
    if (video && start) {
      start.addEventListener('click', function () {
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + video.getAttribute('data-yt') + '?autoplay=1&rel=0&modestbranding=1';
        f.title = 'Imagefilm ASSISTENTIUM';
        f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
        f.allowFullscreen = true;
        f.referrerPolicy = 'strict-origin-when-cross-origin';
        video.innerHTML = '';
        video.appendChild(f);
        f.focus();
      });
    }

    /* Sprungmarken: aktiven Abschnitt markieren */
    var jumpLinks = document.querySelectorAll('.jump a[href^="#"]');
    if (jumpLinks.length && 'IntersectionObserver' in window) {
      var map = {};
      jumpLinks.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s) map[s.id] = a; });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            jumpLinks.forEach(function (a) { a.removeAttribute('aria-current'); });
            var a = map[en.target.id]; if (a) { a.setAttribute('aria-current', 'true'); a.scrollIntoView({ block: 'nearest', inline: 'nearest' }); }
          }
        });
      }, { rootMargin: '-40% 0px -55% 0px' });
      Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
    }

    /* Stellenanzeige per Anker öffnen */
    function openFromHash() {
      var t = location.hash && document.getElementById(location.hash.slice(1));
      if (t && t.tagName === 'DETAILS') { t.open = true; t.scrollIntoView(); }
    }
    window.addEventListener('hashchange', openFromHash);
    openFromHash();

    /* IBAN kopieren */
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      b.addEventListener('click', function () {
        var text = b.getAttribute('data-copy');
        var done = function () { var t = b.textContent; b.textContent = 'Kopiert'; setTimeout(function () { b.textContent = t; }, 1600); };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
      });
    });

    /* Varianten-Panel */
    var wrap = document.createElement('div');
    wrap.className = 'variants';
    wrap.innerHTML =
      '<div class="variants-panel" id="variants-panel" hidden>' +
        '<fieldset><legend>Farbe der dunklen Flächen</legend>' +
          '<label><input type="radio" name="farbe" value="waldgruen"><span class="sw" style="background:#1F3B2D"></span>Waldgrün</label>' +
          '<label><input type="radio" name="farbe" value="anthrazit"><span class="sw" style="background:#2E3236"></span>Anthrazit</label>' +
          '<label><input type="radio" name="farbe" value="hell"><span class="sw" style="background:#F1F4D6"></span>Hell, ohne dunkle Flächen</label>' +
        '</fieldset>' +
        '<fieldset><legend>Fließtext-Schrift</legend>' +
          '<label><input type="radio" name="schrift" value="atkinson">Atkinson Hyperlegible (Lesbarkeit)</label>' +
          '<label><input type="radio" name="schrift" value="hind">Hind (nah an Frutiger aus dem Logo)</label>' +
        '</fieldset>' +
        '<p>Nur im Prototyp. Die Auswahl bleibt beim Seitenwechsel erhalten. Alle Varianten erfüllen den Kontrast für Barrierefreiheit.</p>' +
      '</div>' +
      '<button class="variants-toggle" type="button" aria-expanded="false" aria-controls="variants-panel">Varianten</button>';
    document.body.appendChild(wrap);
    var panel = wrap.querySelector('.variants-panel');
    var toggle = wrap.querySelector('.variants-toggle');
    toggle.addEventListener('click', function () {
      var open = panel.hidden; panel.hidden = !open; toggle.setAttribute('aria-expanded', String(open));
    });
    wrap.querySelectorAll('input').forEach(function (inp) {
      inp.checked = state[inp.name] === inp.value;
      inp.addEventListener('change', function () { state[inp.name] = inp.value; apply(); });
    });
  });
})();
