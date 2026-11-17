(function () {
  'use strict';
  /* Audio previews on the product page — drives the 3D viewer through "rec-play" events. */
  var list = document.querySelector('.tracks');
  if (!list) return;
  var series = list.dataset.series || 'mp';
  var playL = list.dataset.play || 'Play preview', pauseL = list.dataset.pause || 'Pause';
  var audio = new Audio(); audio.preload = 'none';
  var playing = null;
  var P = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg>';
  var Z = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 2.5h3v11H4zM9 2.5h3v11H9z"/></svg>';
  var btns = [].slice.call(list.querySelectorAll('.play'));

  function paint() {
    btns.forEach(function (b) {
      var on = playing === b.dataset.side;
      b.classList.toggle('on', on);
      b.innerHTML = (on ? Z : P) + '<span class="ring"></span>';
      b.setAttribute('aria-label', (on ? pauseL : playL) + ' – Side ' + b.dataset.side.toUpperCase());
    });
  }
  function stop() {
    audio.pause(); playing = null; paint();
    window.dispatchEvent(new CustomEvent('rec-play', { detail: null }));
  }
  audio.addEventListener('ended', stop);
  audio.addEventListener('timeupdate', function () {
    var r = list.querySelector('.play.on .ring');
    if (r && audio.duration) {
      var deg = audio.currentTime / audio.duration * 360;
      r.style.background = 'conic-gradient(var(--' + series + ') ' + deg + 'deg,transparent 0)';
      r.style.webkitMask = r.style.mask = 'radial-gradient(circle,transparent 19px,#000 20px)';
    }
  });
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var sd = b.dataset.side;
      if (playing === sd) { stop(); return; }
      audio.src = b.dataset.audio;
      audio.play().then(function () {
        playing = sd; paint();
        window.dispatchEvent(new CustomEvent('rec-play', { detail: sd }));
      }).catch(function () {});
    });
  });
  paint();
})();
