/* くらし比較ラボ — minimal progressive enhancement
   - 外部リンク（アフィリエイト）は新規タブ + rel="sponsored nofollow noopener"
   - フッターの年号を現在年に
   - カテゴリページの絞り込みチップ（[data-filter-group] → [data-cat]）
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

  function initFilters() {
    document.querySelectorAll('[data-filter-group]').forEach(function (bar) {
      var list = document.getElementById(bar.getAttribute('data-filter-group'));
      if (!list) return;
      var chips = Array.prototype.slice.call(bar.querySelectorAll('[data-filter]'));
      if (!chips.length) return;

      chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          var value = chip.getAttribute('data-filter');
          chips.forEach(function (c) {
            c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
          });
          var cards = list.querySelectorAll('[data-cat]');
          Array.prototype.forEach.call(cards, function (card) {
            var show = value === 'all' || card.getAttribute('data-cat') === value;
            if (show) {
              card.removeAttribute('hidden');
            } else {
              card.setAttribute('hidden', '');
            }
          });
        });
      });
    });
  }

  function init() {
    markExternalLinks();
    setYear();
    initFilters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
