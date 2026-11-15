/* くらし比較ラボ — minimal progressive enhancement
   - 外部リンク（アフィリエイト）は新規タブ + rel="sponsored nofollow noopener"
   - フッターの年号を現在年に
*/
(function () {
  'use strict';

  function markExternalLinks() {
    document.querySelectorAll('a[data-aff]').forEach(function (a) {
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'sponsored nofollow noopener');
    });
  }

  function setYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      markExternalLinks();
      setYear();
    });
  } else {
    markExternalLinks();
    setYear();
  }
})();
