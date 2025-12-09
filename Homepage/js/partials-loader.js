document.addEventListener('DOMContentLoaded', () => {
  const placeholders = Array.from(document.querySelectorAll('[data-partial]'));
  if (!placeholders.length) return;

  const INLINE_PARTIALS = {
    header: `<header class="header-container" id="header-container">
  <a href="#top" class="logo-link">
    <img class="logo" src="Assets/logo/Estoque360_Logos/estoque360_master.svg" alt="Estoque360&deg; Logo">
  </a>

  <nav class="nav-links">
    <a data-nav-target="#top" href="index.html#top">In&iacute;cio</a>
    <a data-nav-target="#price-section" href="#price-section">Planos</a>
    <a data-nav-target="#faq-section" href="#faq-section">FAQ</a>
    <a data-nav-target="#footer-section" href="#footer-section">Contatos</a>
    <a href="about.html">Sobre</a>
  </nav>

  <div class="fishing-section">
    <button class="fishing-button" id="fishing-button">Experimente 1 m&ecirc;s gr&aacute;tis!</button>
  </div>
</header>`,
    footer: `<footer class="footer-container" id="footer-section">
  <div class="footer-content">
    <div class="footer-brand">
      <img src="Assets/logo/Estoque360_Logos/estoque360_icon.png" alt="Logo do Estoque360&deg;" class="logo-footer">
    </div>

    <nav class="footer-nav">
      <a href="#top">In&iacute;cio</a>
      <a href="#feature-section">Recursos</a>
      <a href="#price-section">Pre&ccedil;os</a>
      <a href="#footer-section">Contato</a>
    </nav>

    <div class="footer-social">
      <a href="https://muskiguess.pages.dev" target="_blank" aria-label="Instagram" class="social-link instagram">
        <img src="Assets/icons/instagram-icon.svg" alt="Instagram" class="social-icon-img">
      </a>

      <a href="https://github.com/lanaro0108/Estoque360;" target="_blank" aria-label="GitHub" class="social-link">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
        </svg>
      </a>
    </div>
  </div>

  <div class="footer-bottom">
    <p>&copy; 2025 Estoque360&deg;. <br>Todos os direitos reservados.</p>
    <div class="legal-links">
      <a href="#">Pol&iacute;ticas de privacidade</a>
      <span>&bull;</span>
      <a href="#">Termos de servi&ccedil;o</a>
    </div>
  </div>
</footer>`,
  };

  const loadPartialContent = async (src) => {
    if (window.location.protocol === 'file:') {
      throw new Error('file-protocol fetch blocked');
    }
    const res = await fetch(src);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.text();
  };

  const loadPartial = async (el) => {
    const name = el.getAttribute('data-partial');
    if (!name) return;
    const src = el.getAttribute('data-src') || `partials/${name}.html`;
    try {
      const html = await loadPartialContent(src);
      el.innerHTML = html;
      el.dataset.loaded = 'true';
    } catch (error) {
      if (INLINE_PARTIALS[name]) {
        console.warn(`[partials] Falha ao carregar ${src}; usando fallback embutido.`, error);
        el.innerHTML = INLINE_PARTIALS[name];
        el.dataset.loaded = 'true';
        return;
      }
      console.error(`[partials] Falha ao carregar ${src}:`, error);
    }
  };

  Promise.all(placeholders.map(loadPartial)).finally(() => {
    document.dispatchEvent(new CustomEvent('partials:loaded'));
  });
});
