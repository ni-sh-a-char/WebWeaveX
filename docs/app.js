// WebWeaveX Ecosystem Portal Client Application

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initSDKTabs();
  initCopyButtons();
  initSearchEngine();
  initSidebarToggle();
  initMermaid();
});

// Theme Switcher (Dark / Light)
function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const currentTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);

  toggleBtn.addEventListener('click', () => {
    const activeTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
}

// SDK Selector Tab Switcher
function initSDKTabs() {
  const tabBtns = document.querySelectorAll('.sdk-tab-btn');
  const tabContents = document.querySelectorAll('.sdk-tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetLang = btn.getAttribute('data-lang');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(`sdk-${targetLang}`);
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });
}

// Copy Code Button
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.copy-btn');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const codeBlock = btn.parentElement.nextElementSibling?.querySelector('code');
      if (!codeBlock) return;

      navigator.clipboard.writeText(codeBlock.textContent.trim()).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.color = '#22c55e';
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.color = '';
        }, 2000);
      });
    });
  });
}

// Fuzzy Search Engine
function initSearchEngine() {
  const searchInput = document.getElementById('search-input');
  const dropdown = document.getElementById('search-results');
  if (!searchInput || !dropdown || typeof window.SEARCH_INDEX === 'undefined') return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (query.length < 2) {
      dropdown.style.display = 'none';
      return;
    }

    const matches = window.SEARCH_INDEX.filter(item => 
      item.title.toLowerCase().includes(query) ||
      item.keywords.toLowerCase().includes(query) ||
      item.excerpt.toLowerCase().includes(query)
    );

    if (matches.length === 0) {
      dropdown.innerHTML = `<div class="search-result-item"><span class="search-result-excerpt">No matching topics found</span></div>`;
    } else {
      dropdown.innerHTML = matches.slice(0, 6).map(m => `
        <a class="search-result-item" href="${m.url}">
          <div class="search-result-title">${m.title}</div>
          <div class="search-result-excerpt">${m.excerpt}</div>
        </a>
      `).join('');
    }

    dropdown.style.display = 'block';
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
}

// Mobile Sidebar Toggle
function initSidebarToggle() {
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const sidebar = document.getElementById('sidebar');

  if (mobileBtn && sidebar) {
    mobileBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }
}

// Initialize Mermaid.js if present
function initMermaid() {
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      securityLevel: 'loose'
    });
  }
}
