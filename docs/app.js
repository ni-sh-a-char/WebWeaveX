// WebWeaveX Documentation Portal — Client Application v3.0.0
// Innovative · Dynamic · Professional

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initSDKTabs();
  initCopyButtons();
  initSearchEngine();
  initSidebarToggle();
  initMermaid();
  initScrollReveal();
  initNavbarScroll();
  initBackgroundCanvas();
  initKeyboardShortcuts();
  initActiveSidebarTracking();
  initAnimatedCounters();
  initInstallCopy();
  initCodeTypingEffect();
});

// ═══ Theme Toggle with Icon Swap ═══
function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;

  const saved = localStorage.getItem('wwx-theme') || 'dark';
  applyTheme(saved);

  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem('wwx-theme', next);
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const darkIcon = btn.querySelector('.theme-icon-dark');
    const lightIcon = btn.querySelector('.theme-icon-light');
    if (darkIcon && lightIcon) {
      darkIcon.style.display = theme === 'dark' ? 'block' : 'none';
      lightIcon.style.display = theme === 'light' ? 'block' : 'none';
    }
    if (typeof mermaid !== 'undefined') {
      mermaid.initialize({
        startOnLoad: true,
        theme: theme === 'dark' ? 'dark' : 'default',
        securityLevel: 'loose',
        fontFamily: 'Inter, -apple-system, sans-serif'
      });
    }
  }
}

// ═══ SDK Tabs ═══
function initSDKTabs() {
  document.querySelectorAll('.sdk-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      document.querySelectorAll('.sdk-tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.sdk-tab-content').forEach(c => c.classList.remove('active'));
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
        btn.style.color = '#34d399';
        setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 2000);
      });
    });
  });
}

// ═══ Search ═══
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
      dropdown.innerHTML = '<div class="search-result-item"><span class="search-result-excerpt">No results found</span></div>';
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

  let mobileBtn = document.getElementById('mobile-menu-btn');
  if (!mobileBtn) {
    mobileBtn = document.createElement('button');
    mobileBtn.id = 'mobile-menu-btn';
    mobileBtn.innerHTML = `<svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>`;
    mobileBtn.style.cssText = 'display:none;background:none;border:1px solid var(--border-default);color:var(--text-primary);padding:8px;border-radius:10px;cursor:pointer;transition:all 0.2s;';
    const nav = document.querySelector('.nav-controls');
    if (nav) nav.prepend(mobileBtn);
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
  }, { threshold: 0.06, rootMargin: '0px 0px -30px 0px' });

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

// ═══ Background Canvas — Mouse-reactive Particles ═══
function initBackgroundCanvas() {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animId;
  let mouse = { x: -1000, y: -1000 };

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function createParticles() {
    particles = [];
    const count = Math.min(Math.floor((canvas.width * canvas.height) / 20000), 70);
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: Math.random() * 1.8 + 0.4,
        alpha: Math.random() * 0.4 + 0.08,
        hue: Math.random() * 60 + 200 // blue-purple range
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';

    particles.forEach(p => {
      // Mouse repulsion
      const dx = p.x - mouse.x;
      const dy = p.y - mouse.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 150) {
        const force = (150 - dist) / 150 * 0.8;
        p.vx += (dx / dist) * force;
        p.vy += (dy / dist) * force;
      }

      // Damping
      p.vx *= 0.99;
      p.vy *= 0.99;

      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;

      const color = isDark ? `hsla(${p.hue}, 70%, 65%, ${p.alpha})` : `hsla(${p.hue}, 60%, 50%, ${p.alpha * 0.6})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    });

    // Connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          const alpha = (1 - dist / 100) * (isDark ? 0.06 : 0.03);
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = isDark ? `rgba(99, 102, 241, ${alpha})` : `rgba(99, 102, 241, ${alpha})`;
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

  document.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('resize', () => {
    resize();
    createParticles();
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(animId);
    else draw();
  });
}

// ═══ Keyboard Shortcuts ═══
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && !isInputFocused())) {
      e.preventDefault();
      const input = document.getElementById('search-input');
      if (input) input.focus();
    }
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
  }, { threshold: 0.15, rootMargin: '-80px 0px -60% 0px' });

  sections.forEach(s => observer.observe(s));
}

// ═══ Animated Counters ═══
function initAnimatedCounters() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-count'));
        const suffix = el.getAttribute('data-suffix') || '';
        animateCounter(el, 0, target, 1200, suffix);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}

function animateCounter(el, start, end, duration, suffix) {
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = Math.floor(start + (end - start) * eased);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ═══ Install Command Copy ═══
function initInstallCopy() {
  const cmd = document.getElementById('install-cmd');
  if (!cmd) return;
  cmd.addEventListener('click', () => {
    const text = cmd.textContent.replace(/\s+/g, ' ').trim();
    navigator.clipboard.writeText(text).then(() => {
      const icon = cmd.querySelector('.copy-icon');
      if (icon) {
        icon.style.color = '#34d399';
        setTimeout(() => { icon.style.color = ''; }, 2000);
      }
    });
  });
}

// ═══ Code Typing Effect ═══
function initCodeTypingEffect() {
  const codeBlocks = document.querySelectorAll('.code-wrapper code');
  if (!codeBlocks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const code = entry.target;
        const text = code.textContent;
        code.textContent = '';
        code.style.visibility = 'visible';
        let i = 0;
        const speed = Math.max(3, Math.min(8, text.length / 200));

        function type() {
          if (i < text.length) {
            code.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
          }
        }
        type();
        observer.unobserve(code);
      }
    });
  }, { threshold: 0.3 });

  codeBlocks.forEach(code => observer.observe(code));
}
