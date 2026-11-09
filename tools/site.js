(() => {
  const search = document.querySelector('#topic-search');
  if (!search) return;
  const branches = [...document.querySelectorAll('.branch')];
  const topics = [...document.querySelectorAll('.topic-list li')];
  const status = document.querySelector('#search-status');
  const empty = document.querySelector('#empty-results');
  const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const index = topics.map(element => ({element, text: normalize(element.dataset.search)}));
  search.addEventListener('input', () => {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    index.forEach(({element, text}) => {
      element.hidden = !terms.every(term => text.includes(term));
      if (!element.hidden) count++;
    });
    branches.forEach(branch => { branch.hidden = !branch.querySelector('li:not([hidden])'); });
    status.textContent = terms.length ? `${count} topic${count === 1 ? '' : 's'} found` : `${topics.length} topics · select a topic to read its concepts and sources`;
    empty.hidden = count > 0;
  });
  const map = document.querySelector('.markmap');
  const note = document.querySelector('#map-status');
  if (!map || !note) return;
  let ready = false;
  const observer = new MutationObserver(() => {
    if (map.querySelector('svg g')) {
      ready = true;
      note.textContent = 'Drag to pan, scroll to zoom, and select a circle to expand. Topic links open the full explanation.';
      observer.disconnect();
    }
  });
  observer.observe(map, {childList:true, subtree:true});
  setTimeout(() => {
    if (!ready) {
      note.textContent = 'The visual map needs an internet connection. Every topic remains readable using the index below.';
    }
  }, 8000);
})();
