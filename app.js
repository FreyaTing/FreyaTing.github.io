'use strict';
(() => {
  const tools = document.querySelector('.publication-tools');
  const papers = [...document.querySelectorAll('.publication')];
  const search = document.querySelector('#paper-search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const status = document.querySelector('#result-count');
  const empty = document.querySelector('#no-results');
  let filter = 'selected';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    papers.forEach(paper => {
      const category = filter === 'all' || (filter === 'selected' ? paper.dataset.selected === 'true' : paper.dataset.kind === filter);
      paper.hidden = !(category && paper.dataset.search.includes(query));
      if (!paper.hidden) count++;
    });
    empty.hidden = count !== 0;
    status.textContent = document.documentElement.lang === 'zh-CN' ? `显示 ${count} 篇论文` : `${count} publications shown`;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.filter;
    buttons.forEach(b => {
      const active = b === button;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', String(active));
    });
    update();
  }));
  search.addEventListener('input', update);
  tools.hidden = false;
  update();
  const language = document.querySelector('.language');
  language.addEventListener('click', () => {
    language.href = language.getAttribute('href').split('#')[0] + window.location.hash;
  });
})();
