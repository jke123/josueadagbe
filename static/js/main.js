// Toggle dark mode
const toggle = document.getElementById('theme-toggle');
const icon = document.getElementById('theme-icon');

if (localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    if (icon) icon.textContent = '☀️';
}

if (toggle) {
    toggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        const isDark = document.documentElement.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        icon.textContent = isDark ? '☀️' : '🌙';
    });
}