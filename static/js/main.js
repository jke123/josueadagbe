(() => {
  const root = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');
  const setTheme = (dark) => { root.classList.toggle('dark', dark); if (themeIcon) themeIcon.textContent = dark ? '☾' : '☼'; localStorage.setItem('theme', dark ? 'dark' : 'light'); };
  const savedTheme = localStorage.getItem('theme'); setTheme(savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches));
  themeToggle?.addEventListener('click', () => setTheme(!root.classList.contains('dark')));
  menuToggle?.addEventListener('click', () => { const open = navLinks.classList.toggle('open'); menuToggle.setAttribute('aria-expanded', open); });
  navLinks?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => navLinks.classList.remove('open')));
  const observer = new IntersectionObserver((entries) => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }), { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  setTimeout(() => document.querySelectorAll('.flash').forEach(el => el.remove()), 6000);
})();
