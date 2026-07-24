// WebWeaveX Documentation Portal — Client Application v3.0.0

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initSDKTabs();
  initCopyButtons();
  initSearchEngine();
  initSidebarToggle();
  initMermaid();
  initScrollReveal();
  initNavbarScroll();
  initParticles();
  initKeyboardShortcuts();
  initActiveSidebarTracking();
});

// ═══ Theme Switcher ═══
function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const currentTheme = localStorage.getItem('wwx-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);
  updateMermaidTheme(currentTheme);

  toggleBtn.addEventListener('click', () => {
    const active = document.documentElement.getAttribute('data-theme');
    const next = active === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('wwx-theme', next);
    updateMermaidTheme(next);
  });
}

function updateMermaidTheme(theme) {
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: theme === 'dark' ? 'dark' : 'default',
      securityLevel: 'loose',
      fontFamily: 'Inter, -apple-system, sans-serif'
    });
  }
}

// ═══ SDK Tabs ═══
function initSDKTabs() {
  const tabBtns = document.querySelectorAll('.sdk-tab-btn');
  const tabContents = document.querySelectorAll('.sdk-tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(`sdk-${lang}`);
      if (target) target.classList.add('active');
    });
  });
}

// ═══ Copy Code ═══
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.closest('.code-wrapper')?.querySelector('code');
      if (!code) return;
      navigator.clipboard.writeText(code.textContent.trim()).then(() => {
        const orig = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.color = '#22c55e';
        setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 2000);
      });
    });
  });
}

// ═══ Search Engine ═══
function initSearchEngine() {
  const input = document.getElementById('search-input');
  const dropdown = document.getElementById('search-results');
  if (!input || !dropdown || typeof window.SEARCH_INDEX === 'undefined') return;

  input.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase().trim();
    if (q.length < 2) { dropdown.style.display = 'none'; return; }

    const matches = window.SEARCH_INDEX.filter(item =>
      item.title.toLowerCase().includes(q) ||
      item.keywords.toLowerCase().includes(q) ||
      item.excerpt.toLowerCase().includes(q)
    );

    if (matches.length === 0) {
      dropdown.innerHTML = '<div class="search-result-item"><span class="search-result-excerpt">No matching topics found</span></div>';
    } else {
      dropdown.innerHTML = matches.slice(0, 8).map(m => `
        <a class="search-result-item" href="${m.url}">
          <div class="search-result-title">${m.title}</div>
          <div class="search-result-excerpt">${m.excerpt}</div>
        </a>
      `).join('');
    }
    dropdown.style.display = 'block';
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
}

// ═══ Mobile Sidebar ═══
function initSidebarToggle() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  // Create mobile menu button if it doesn't exist
  let mobileBtn = document.getElementById('mobile-menu-btn');
  if (!mobileBtn) {
    mobileBtn = document.createElement('button');
    mobileBtn.id = 'mobile-menu-btn';
    mobileBtn.innerHTML = `<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>`;
    mobileBtn.style.cssText = 'display:none;background:none;border:1px solid var(--border-color);color:var(--text-primary);padding:8px;border-radius:8px;cursor:pointer;';
    const navControls = document.querySelector('.nav-controls');
    if (navControls) navControls.prepend(mobileBtn);
  }

  function checkMobile() {
    if (window.innerWidth <= 900) {
      mobileBtn.style.display = 'flex';
    } else {
      mobileBtn.style.display = 'none';
      sidebar.classList.remove('open');
    }
  }

  mobileBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  window.addEventListener('resize', checkMobile);
  checkMobile();

  // Close sidebar on link click (mobile)
  sidebar.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 900) sidebar.classList.remove('open');
    });
  });
}

// ═══ Mermaid ═══
function initMermaid() {
  if (typeof mermaid !== 'undefined') {
    const theme = document.documentElement.getAttribute('data-theme') || 'dark';
    mermaid.initialize({
      startOnLoad: true,
      theme: theme === 'dark' ? 'dark' : 'default',
      securityLevel: 'loose',
      fontFamily: 'Inter, -apple-system, sans-serif'
    });
  }
}

// ═══ Scroll Reveal ═══
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => observer.observe(el));
}

// ═══ Navbar Scroll ═══
function initNavbarScroll() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        navbar.classList.toggle('scrolled', window.scrollY > 10);
        ticking = false;
      });
      ticking = true;
    }
  });
}

// ═══ Particle Background ═══
function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animId;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function createParticles() {
    particles = [];
    const count = Math.min(Math.floor((canvas.width * canvas.height) / 25000), 60);
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.5 + 0.5,
        alpha: Math.random() * 0.5 + 0.1
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    const color = isDark ? '56, 189, 248' : '37, 99, 235';

    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${color}, ${p.alpha})`;
      ctx.fill();
    });

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(${color}, ${0.08 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    animId = requestAnimationFrame(draw);
  }

  resize();
  createParticles();
  draw();

  window.addEventListener('resize', () => {
    resize();
    createParticles();
  });

  // Pause when tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      cancelAnimationFrame(animId);
    } else {
      draw();
    }
  });
}

// ═══ Keyboard Shortcuts ═══
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ctrl+K or / to focus search
    if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && !isInputFocused())) {
      e.preventDefault();
      const input = document.getElementById('search-input');
      if (input) input.focus();
    }
    // Escape to close search
    if (e.key === 'Escape') {
      const dropdown = document.getElementById('search-results');
      const input = document.getElementById('search-input');
      if (dropdown) dropdown.style.display = 'none';
      if (input) input.blur();
    }
  });
}

function isInputFocused() {
  const el = document.activeElement;
  return el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable);
}

// ═══ Active Sidebar Tracking ═══
function initActiveSidebarTracking() {
  const sections = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.sidebar-link[href^="#"]');
  if (!sections.length || !links.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        links.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  }, { threshold: 0.2, rootMargin: '-80px 0px -60% 0px' });

  sections.forEach(s => observer.observe(s));
}
