document.addEventListener('DOMContentLoaded', function () {
    const track = document.getElementById('ratingTrack');
    const originalCards = Array.from(document.querySelectorAll('.rating-card'));
    const btnPrev = document.querySelector('.prev-btn');
    const btnNext = document.querySelector('.next-btn');
    const container = document.querySelector('.carousel-container'); // Seleciona o container pai

    // --- NOVO: CURSOR DESFOCADOR (BLUR SPOT) ---
    if (container) {
        // Cria o elemento do spot via JS para não sujar o HTML
        const blurSpot = document.createElement('div');
        blurSpot.classList.add('blur-spot');
        container.appendChild(blurSpot);

        // Faz o spot seguir o mouse
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            blurSpot.style.left = `${x}px`;
            blurSpot.style.top = `${y}px`;
        });
    }
    // --------------------------------------------

    // Configurações
    const cardWidth = 340; // Largura do card (igual ao CSS)
    const gap = 32; // Gap (igual ao CSS 2rem)
    const totalItemWidth = cardWidth + gap;

    // Quantos cards clonar para o buffer (2 é suficiente para garantir a visualização)
    const clonesCount = 2;

    // Estado
    let currentIndex = clonesCount; // Começa no primeiro card REAL (pula os clones iniciais)
    let isTransitioning = false;
    let allCards = [];

    // 1. INICIALIZAÇÃO: CLONAGEM
    function setupInfiniteCarousel() {
        // Clona os últimos para o começo
        const clonesStart = originalCards.slice(-clonesCount).map(card => {
            const clone = card.cloneNode(true);
            clone.classList.add('clone');
            return clone;
        });

        // Clona os primeiros para o final
        const clonesEnd = originalCards.slice(0, clonesCount).map(card => {
            const clone = card.cloneNode(true);
            clone.classList.add('clone');
            return clone;
        });

        // Insere no DOM
        clonesStart.forEach(clone => track.insertBefore(clone, track.firstChild));
        clonesEnd.forEach(clone => track.appendChild(clone));

        // Atualiza lista de todos os cards
        allCards = Array.from(document.querySelectorAll('.rating-card'));

        // Adiciona evento de clique em TODOS os cards (incluindo clones)
        allCards.forEach((card, index) => {
            card.addEventListener('click', () => {
                if (currentIndex !== index && !isTransitioning) {
                    currentIndex = index;
                    updateCarousel();
                }
            });
        });

        // Posiciona inicialmente sem animação
        track.classList.remove('smooth-transition');
        updatePosition();
        updateClasses();

        // Ativa transição suave após renderização inicial
        setTimeout(() => {
            track.classList.add('smooth-transition');
        }, 50);
    }

    // 2. FUNÇÃO DE MOVIMENTO
    function updatePosition() {
        const containerWidth = document.querySelector('.carousel-viewport').offsetWidth;
        // Centraliza o card ativo
        const centerOffset = (containerWidth / 2) - (cardWidth / 2);
        const newPosition = -(currentIndex * totalItemWidth) + centerOffset;

        track.style.transform = `translateX(${newPosition}px)`;
    }

    function updateClasses() {
        allCards.forEach((card, index) => {
            if (index === currentIndex) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });
    }

    function updateCarousel() {
        if (isTransitioning) return;
        isTransitioning = true;

        track.classList.add('smooth-transition');
        updatePosition();
        updateClasses();
    }

    // 3. CONTROLE DO LOOP INFINITO (Teletransporte)
    track.addEventListener('transitionend', () => {
        isTransitioning = false;

        const totalRealCards = originalCards.length;

        // Se chegou nos clones do final (depois do último real)
        if (currentIndex >= totalRealCards + clonesCount) {
            track.classList.remove('smooth-transition'); // Desliga animação
            currentIndex = currentIndex - totalRealCards; // Pula para o início real
            updatePosition();
            updateClasses();
        }
        // Se chegou nos clones do início (antes do primeiro real)
        else if (currentIndex < clonesCount) {
            track.classList.remove('smooth-transition'); // Desliga animação
            currentIndex = currentIndex + totalRealCards; // Pula para o final real
            updatePosition();
            updateClasses();
        }
    });

    // 4. BOTÕES
    btnNext.addEventListener('click', () => {
        if (isTransitioning) return;
        currentIndex++;
        updateCarousel();
    });

    btnPrev.addEventListener('click', () => {
        if (isTransitioning) return;
        currentIndex--;
        updateCarousel();
    });

    // Recalcular no resize (para manter centralizado)
    window.addEventListener('resize', () => {
        track.classList.remove('smooth-transition');
        updatePosition();
    });

    // Iniciar
    setupInfiniteCarousel();
});