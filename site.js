const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');

function closeMenu() {
  nav?.classList.remove('open');
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', 'Open navigation');
}

menuButton?.addEventListener('click', () => {
  const willOpen = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(willOpen));
  menuButton.setAttribute('aria-label', willOpen ? 'Close navigation' : 'Open navigation');
  nav?.classList.toggle('open', willOpen);
});

nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});

