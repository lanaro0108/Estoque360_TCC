// Seleciona todos os cards de feature
const cards = document.querySelectorAll('.hero-image, .team-photo');

cards.forEach((card) => {
    // Configurações de "Física"
    const state = {
        mouseX: 0,
        mouseY: 0,
        height: card.clientHeight,
        width: card.clientWidth,
        // Posição atual (para o Lerp)
        currentMouseX: 0,
        currentMouseY: 0,
        currentScale: 1
    };

    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        
        // Pega a posição do mouse relativa ao centro do card
        // Valores vão de -width/2 até +width/2
        state.mouseX = e.clientX - rect.left - state.width / 2;
        state.mouseY = e.clientY - rect.top - state.height / 2;
    });

    card.addEventListener('mouseenter', () => {
        // Recalcula tamanho caso a janela tenha mudado
        state.width = card.clientWidth;
        state.height = card.clientHeight;
    });

    card.addEventListener('mouseleave', () => {
        // Quando o mouse sai, o alvo volta a ser o centro (0,0)
        state.mouseX = 0;
        state.mouseY = 0;
    });

    // Função de animação (Loop constante)
    function animate() {
        // LERP (Linear Interpolation)
        // Fórmula: atual = atual + (alvo - atual) * fricção
        // 0.1 é a "suavidade" (menor = mais lento/pesado, maior = mais rápido)
        state.currentMouseX += (state.mouseX - state.currentMouseX) * 0.1;
        state.currentMouseY += (state.mouseY - state.currentMouseY) * 0.1;

        // Calcular a rotação baseada na posição suavizada
        // Dividimos por um valor (ex: 20) para a rotação não ser exagerada
        const rotateY = state.currentMouseX / 70; 
        const rotateX = -state.currentMouseY / 70; // Invertido para parecer natural

        // Calcular escala
        // Se o mouse estiver longe do centro (0), aumentamos a escala
        // Se estiver em 0 (fora do card), escala volta a 1
        const targetScale = (state.mouseX !== 0 || state.mouseY !== 0) ? 1.05 : 1;
        state.currentScale += (targetScale - state.currentScale) * 0.08;

        // Aplica o transform
        card.style.transform = `
            perspective(1000px)
            scale3d(${state.currentScale}, ${state.currentScale}, ${state.currentScale})
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
        `;

        requestAnimationFrame(animate);
    }

    animate();
});