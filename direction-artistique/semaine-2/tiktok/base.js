// Moteur commun des vidéos TikTok animées : setT(t) est appelé par render.js pour chaque image.
// .scene : visible entre data-s et data-e (secondes). .a : apparaît à data-t (fondu + montée).
// .g : se déploie de gauche à droite à partir de data-t, sur data-d secondes.
window.setT = function (t) {
  document.querySelectorAll('.scene').forEach(function (s) {
    var a = +s.dataset.s, b = +s.dataset.e;
    s.style.opacity = (t >= a && t < b) ? 1 : 0;
  });
  document.querySelectorAll('.a').forEach(function (el) {
    var t0 = +el.dataset.t;
    var p = Math.min(1, Math.max(0, (t - t0) / 0.45));
    el.style.opacity = p;
    el.style.transform = 'translateY(' + ((1 - p) * 36) + 'px)';
  });
  document.querySelectorAll('.g').forEach(function (el) {
    var t0 = +el.dataset.t, d = +el.dataset.d || 0.8;
    var p = Math.min(1, Math.max(0, (t - t0) / d));
    el.style.transform = 'scaleX(' + p + ')';
  });
};
