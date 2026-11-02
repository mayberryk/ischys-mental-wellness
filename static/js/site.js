(() => {
  const toggle = document.querySelector('.menu-toggle');
  const mobile = document.querySelector('.mobile-nav');
  const closeMobile = () => { mobile.hidden = true; toggle.setAttribute('aria-expanded', 'false'); };
  toggle?.addEventListener('click', () => {
    const opening = mobile.hidden;
    mobile.hidden = !opening;
    toggle.setAttribute('aria-expanded', String(opening));
  });
  const groups = [...document.querySelectorAll('.nav-group')];
  groups.forEach(group => {
    let timer;
    group.addEventListener('toggle', () => {
      if (group.open) groups.filter(other => other !== group).forEach(other => other.open = false);
    });
    group.addEventListener('mouseenter', () => {
      if (!group.closest('.desktop-nav') || !matchMedia('(hover:hover) and (pointer:fine)').matches) return;
      clearTimeout(timer); group.open = true;
    });
    group.addEventListener('mouseleave', () => {
      if (!group.closest('.desktop-nav')) return;
      timer = setTimeout(() => { if (!group.contains(document.activeElement)) group.open = false; }, 170);
    });
    group.addEventListener('focusout', () => setTimeout(() => {
      if (!group.contains(document.activeElement) && !group.matches(':hover')) group.open = false;
    }, 0));
  });
  document.addEventListener('click', event => {
    groups.filter(group => !group.contains(event.target)).forEach(group => group.open = false);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const open = groups.find(group => group.open);
    if (open) { open.open = false; open.querySelector('summary').focus(); }
    else if (mobile && !mobile.hidden) { closeMobile(); toggle.focus(); }
  });
  matchMedia('(min-width:1101px)').addEventListener('change', event => { if (event.matches) closeMobile(); });
  const input = document.querySelector('#article-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const requestedTopic = new URLSearchParams(location.search).get('topic');
  let category = filters.some(button => button.dataset.filter === requestedTopic) ? requestedTopic : 'all';
  function filterArticles() {
    const term = (input?.value || '').toLocaleLowerCase().trim();
    let count = 0;
    document.querySelectorAll('[data-article]').forEach(card => {
      const match = (!term || card.textContent.toLocaleLowerCase().includes(term)) &&
        (category === 'all' || card.dataset.categories.split(' ').includes(category));
      card.hidden = !match; if (match) count++;
    });
    const result = document.querySelector('#search-results');
    if (result) result.textContent = `${count} article${count === 1 ? '' : 's'}`;
    const empty = document.querySelector('#no-results'); if (empty) empty.hidden = count !== 0;
  }
  input?.addEventListener('input', filterArticles);
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    filterArticles();
  }));
  if (input) {
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    filterArticles();
  }
  const resourceSections = [...document.querySelectorAll('.resource-fold')];
  const expandResources = document.querySelector('[data-resource-expand]');
  function updateResourceToggle() {
    if (expandResources) expandResources.textContent = resourceSections.every(section => section.open) ? 'Collapse all sections' : 'Expand all sections';
  }
  expandResources?.addEventListener('click', () => {
    const open = !resourceSections.every(section => section.open);
    resourceSections.forEach(section => section.open = open);
    updateResourceToggle();
  });
  resourceSections.forEach(section => section.addEventListener('toggle', updateResourceToggle));
  function revealResourceAnchor() {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.classList.contains('resource-fold')) target.open = true;
  }
  window.addEventListener('hashchange', revealResourceAnchor);
  revealResourceAnchor();
  let resourcePrintState;
  window.addEventListener('beforeprint', () => {
    resourcePrintState = resourceSections.map(section => section.open);
    resourceSections.forEach(section => section.open = true);
  });
  window.addEventListener('afterprint', () => {
    if (resourcePrintState) resourceSections.forEach((section, i) => section.open = resourcePrintState[i]);
    resourcePrintState = undefined;
    updateResourceToggle();
  });
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  // Conversion hooks deliberately contain no page URLs, titles, query strings, form values,
  // search terms, health topics, referrers, or patient identifiers. No network calls here.
  const allowed = new Set(['schedule_click', 'consultation_click', 'phone_click', 'portal_click', 'referral_click']);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-event]');
    if (!link || !allowed.has(link.dataset.event)) return;
    window.dispatchEvent(new CustomEvent('ischys:conversion', {detail: {event: link.dataset.event}}));
  });
})();
