document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const header = item.querySelector('.faq-header');

        header.addEventListener('click', () => {
            const body = item.querySelector('.faq-body');

            // 1. Verifica se já está aberto
            const isOpen = item.classList.contains('active');

            // 2. Fecha todos os outros itens (efeito Sanfona/Accordion)
            // Se quiser que fiquem vários abertos ao mesmo tempo, remova este bloco foreach abaixo
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-body').style.maxHeight = null;
                }
            });

            // 3. Toggle do item atual
            if (isOpen) {
                // Fecha
                item.classList.remove('active');
                body.style.maxHeight = null;
            } else {
                // Abre
                item.classList.add('active');
                // Define a altura exata do conteúdo para a animação funcionar
                body.style.maxHeight = body.scrollHeight + "px";
            }
        });
    });
});