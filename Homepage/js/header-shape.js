document.addEventListener('DOMContentLoaded', () => {
    let initialized = false;

    const setup = () => {
        if (initialized) return true;
        const header = document.querySelector('.header-container');
        if (!header) return false;

        const applyHeaderShape = () => {
            const atTop = window.scrollY <= 8;
            header.classList.toggle('is-rolling', !atTop);
        };

        window.addEventListener('scroll', applyHeaderShape, { passive: true });
        applyHeaderShape();
        initialized = true;
        return true;
    };

    if (setup()) return;
    document.addEventListener('partials:loaded', setup, { once: true });
});
