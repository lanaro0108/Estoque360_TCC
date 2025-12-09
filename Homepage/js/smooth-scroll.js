(function () {
  if (typeof window === 'undefined' || window.__lenisInitialized) {
    return;
  }

  const LENIS_CDN = 'https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js';

  const ready = (fn) => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  };

  const ensureLenisStyles = () => {
    if (document.getElementById('lenis-inline-styles')) return;
    const style = document.createElement('style');
    style.id = 'lenis-inline-styles';
    style.textContent = [
      'html.lenis { height: auto; }',
      '.lenis.lenis-smooth { scroll-behavior: auto !important; }',
      '.lenis.lenis-stopped { overflow: hidden; }',
      '.lenis.lenis-smooth [data-lenis-prevent] { overscroll-behavior: contain; }',
    ].join('\n');
    document.head.appendChild(style);
  };

  const getScrollOffset = () => {
    const header = document.querySelector('[data-scroll-offset]') || document.querySelector('.header-container');
    if (!header) return 0;
    const style = window.getComputedStyle(header);
    const isSticky = style.position === 'sticky' || style.position === 'fixed';
    return isSticky ? header.getBoundingClientRect().height : 0;
  };

  const createParallaxManager = () => {
    const targets = [];

    const collect = () => {
      targets.length = 0;
      document.querySelectorAll('[data-parallax-factor]').forEach((el) => {
        const factor = parseFloat(el.getAttribute('data-parallax-factor'));
        if (!Number.isFinite(factor)) {
          return;
        }
        targets.push({ el, factor });
      });
    };

    const update = (scrollPos) => {
      if (!targets.length) {
        return;
      }
      for (let i = 0; i < targets.length; i += 1) {
        const item = targets[i];
        const offset = -(scrollPos * item.factor);
        item.el.style.setProperty('--parallax-offset', `${offset.toFixed(2)}px`);
      }
    };

    return { collect, update };
  };

  const attachCollectionWatchers = (parallaxManager, onResize) => {
    let resizeTimer = null;
    window.addEventListener(
      'resize',
      () => {
        if (resizeTimer) {
          window.clearTimeout(resizeTimer);
        }
        resizeTimer = window.setTimeout(() => {
          if (typeof onResize === 'function') {
            onResize();
          }
          parallaxManager.collect();
        }, 150);
      },
      { passive: true }
    );

    if (!document.body) return;

    const observer = new MutationObserver((mutations) => {
      for (let i = 0; i < mutations.length; i += 1) {
        if (mutations[i].type === 'childList') {
          parallaxManager.collect();
          break;
        }
      }
    });

    observer.observe(document.body, {
      subtree: true,
      childList: true,
    });
  };

  const wireAnchorLinks = (lenis) => {
    const links = document.querySelectorAll('a[href^="#"]');
    const scrollToTarget = (target) => {
      const offset = getScrollOffset();
      if (lenis) {
        lenis.scrollTo(target || 0, { offset: -offset });
      } else if (target instanceof HTMLElement) {
        const targetY = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetY, behavior: 'smooth' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };

    links.forEach((link) => {
      link.addEventListener('click', (event) => {
        const id = link.getAttribute('href');
        if (!id || id === '#') {
          return;
        }
        event.preventDefault();
        if (id === '#top') {
          scrollToTarget(null);
          return;
        }
        const target = document.querySelector(id);
        scrollToTarget(target);
      });
    });
  };

  const loadLenis = () =>
    new Promise((resolve) => {
      if (typeof window.Lenis === 'function') {
        resolve(window.Lenis);
        return;
      }

      const existing = document.querySelector('script[data-lenis-cdn]');
      if (existing) {
        existing.addEventListener('load', () => resolve(window.Lenis));
        existing.addEventListener('error', () => resolve(null));
        return;
      }

      const script = document.createElement('script');
      script.src = LENIS_CDN;
      script.async = true;
      script.dataset.lenisCdn = 'true';
      script.onload = () => resolve(window.Lenis || null);
      script.onerror = () => resolve(null);
      document.head.appendChild(script);
    });

  const initLenis = async () => {
    const parallaxManager = createParallaxManager();
    parallaxManager.collect();

    ensureLenisStyles();
    const prefersReducedMotion = window.matchMedia
      ? window.matchMedia('(prefers-reduced-motion: reduce)')
      : null;

    if (prefersReducedMotion && prefersReducedMotion.matches) {
      window.__lenisInitialized = true;
      console.info('[smooth-scroll] Reduced-motion preference detected; Lenis disabled.');
      const rewireAnchors = () => wireAnchorLinks(null);
      rewireAnchors();
      document.addEventListener('partials:loaded', rewireAnchors);
      attachCollectionWatchers(parallaxManager);
      window.addEventListener(
        'scroll',
        () => parallaxManager.update(window.scrollY || window.pageYOffset),
        { passive: true }
      );
      return;
    }

    const LenisCtor = await loadLenis();
    if (typeof LenisCtor !== 'function') {
      window.__lenisInitialized = true;
      console.warn('[smooth-scroll] Lenis library was not loaded; falling back to native smooth scroll.');
      const rewireAnchors = () => wireAnchorLinks(null);
      rewireAnchors();
      document.addEventListener('partials:loaded', rewireAnchors);
      attachCollectionWatchers(parallaxManager);
      window.addEventListener(
        'scroll',
        () => parallaxManager.update(window.scrollY || window.pageYOffset),
        { passive: true }
      );
      return;
    }

    let lenis;
    try {
      lenis = new LenisCtor({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        direction: 'vertical',
        gestureDirection: 'vertical',
        smoothWheel: true,
        smoothTouch: true,
        touchMultiplier: 2,
        infinite: false,
      });
    } catch (error) {
      window.__lenisInitialized = true;
      console.error('[smooth-scroll] Failed to initialize Lenis; using native scroll.', error);
      const rewireAnchors = () => wireAnchorLinks(null);
      rewireAnchors();
      document.addEventListener('partials:loaded', rewireAnchors);
      attachCollectionWatchers(parallaxManager);
      window.addEventListener(
        'scroll',
        () => parallaxManager.update(window.scrollY || window.pageYOffset),
        { passive: true }
      );
      return;
    }

    window.__lenisInitialized = true;
    window.__lenisInstance = lenis;

    const raf = (time) => {
      lenis.raf(time);
      requestAnimationFrame(raf);
    };
    requestAnimationFrame(raf);

    lenis.on('scroll', ({ scroll }) => {
      parallaxManager.update(scroll);
    });

    const rewireAnchors = () => wireAnchorLinks(lenis);
    rewireAnchors();
    document.addEventListener('partials:loaded', rewireAnchors);
    attachCollectionWatchers(parallaxManager, () => lenis.resize());

    if (prefersReducedMotion) {
      prefersReducedMotion.addEventListener('change', (event) => {
        if (event.matches) {
          lenis.stop();
          console.info('[smooth-scroll] Reduced-motion preference enabled; Lenis stopped.');
        } else {
          lenis.start();
          console.info('[smooth-scroll] Reduced-motion preference disabled; Lenis restarted.');
        }
      });
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        lenis.stop();
      } else if (!prefersReducedMotion || !prefersReducedMotion.matches) {
        lenis.start();
      }
    });
  };

  ready(initLenis);
})();
