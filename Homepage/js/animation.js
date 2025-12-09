document.addEventListener('DOMContentLoaded', () => {

    // 1. Seleciona os elementos que queremos animar
    const selectors = [
        'section',          // Todas as seções principais
        'h1', 'h2', 'h3',   // Títulos
        'p',                // Parágrafos
        '.pricing-card',    // Cards de preço
        '.feature-cards > div', // Cards de features
        '.faq-item',        // Itens do FAQ
        'img',              // Imagens
        '.fishing-button',  // Botões grandes
        '.buttons-section'  // Grupo de botões
    ];

    const allElements = document.querySelectorAll(selectors.join(', '));

    // FILTRO: Remove elementos que estão dentro do Footer e do Carousel para evitar bugs visuais
    const elementsToAnimate = Array.from(allElements).filter(el => {
        return !el.closest('.footer-container') &&
            !el.closest('footer') &&
            !el.closest('.carousel-container') &&
            !el.closest('.rating-section');
    });

    // 2. Configuração do Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    // 3. Cria o Observer
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // 4. Inicializa apenas nos elementos filtrados
    elementsToAnimate.forEach(el => {
        el.classList.add('fade-on-scroll');
        observer.observe(el);
    });
});