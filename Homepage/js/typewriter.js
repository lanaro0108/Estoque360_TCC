document.addEventListener('DOMContentLoaded', () => {

    // -------------------------------------------------------------
    // 1. TYPEWRITER HERO (O loop "Somos...")
    // -------------------------------------------------------------
    const target = document.getElementById('typewriter-text');
    const cursor = document.querySelector('.typewriter-cursor');

    // Só roda se os elementos existirem na página
    if (target && cursor) {
        const steps = [
            { text: 'Somos especialistas em gestão.', eraseTo: 'Somos '.length, pauseAfter: 1200 },
            { text: 'Somos parceiros do seu time.', eraseTo: 'Somos '.length, pauseAfter: 800 },
            { text: 'Somos o Estoque360', eraseTo: 'Somos o Estoque360'.length, pauseAfter: 800 },
            { text: 'Somos o Estoque360°.', eraseTo: 0, pauseAfter: 5500 },
        ];

        const typeSpeed = 52;
        const eraseSpeed = 12;
        let stepIndex = 0;
        let charIndex = 0;
        let erasing = false;

        const getEraseTarget = (eraseTo) => {
            if (typeof eraseTo === 'number') return eraseTo;
            if (typeof eraseTo === 'string') return eraseTo.length;
            return 0;
        };

        const tick = () => {
            const { text, eraseTo, pauseAfter } = steps[stepIndex];
            const eraseTarget = getEraseTarget(eraseTo);

            if (!erasing) {
                target.textContent = text.slice(0, charIndex + 1);
                charIndex += 1;

                if (charIndex === text.length) {
                    erasing = true;
                    setTimeout(tick, pauseAfter);
                    return;
                }
                setTimeout(tick, typeSpeed);
            } else {
                if (eraseTarget === text.length) {
                    erasing = false;
                    stepIndex = (stepIndex + 1) % steps.length;
                    setTimeout(tick, 0);
                    return;
                }
                target.textContent = text.slice(0, charIndex - 1);
                charIndex -= 1;
                if (charIndex === eraseTarget) {
                    erasing = false;
                    stepIndex = (stepIndex + 1) % steps.length;
                    setTimeout(tick, 250);
                    return;
                }
                setTimeout(tick, eraseSpeed);
            }
        };
        tick();
    }

    // -------------------------------------------------------------
    // 2. TYPEWRITER TÍTULO HERO (Uma vez: "A automação...")
    // -------------------------------------------------------------
    const titleTarget = document.getElementById('title-typewriter-text');
    const titleCursor = titleTarget ? titleTarget.nextElementSibling : null;

    if (titleTarget && titleCursor) {
        const titleText = 'A automação está na moda.';
        const titleTypeSpeed = 90;
        let titleIndex = 0;

        const typeTitle = () => {
            titleTarget.textContent = titleText.slice(0, titleIndex + 1);
            titleIndex += 1;

            if (titleIndex === titleText.length) {
                titleCursor.style.visibility = 'hidden';
                return;
            }
            setTimeout(typeTitle, titleTypeSpeed);
        };
        typeTitle();
    }

    // -------------------------------------------------------------
    // 3. TYPEWRITER PRICING (Uma vez: "Escolha o plano...")
    // -------------------------------------------------------------
    const pricingTarget = document.getElementById('pricing-typewriter-text');
    const pricingCursor = pricingTarget ? pricingTarget.nextElementSibling : null;

    if (pricingTarget && pricingCursor) {
        const pricingText = 'Escolha o plano ideal para você.';
        const pricingSpeed = 50;
        let pricingIndex = 0;

        const typePricing = () => {
            pricingTarget.textContent = pricingText.slice(0, pricingIndex + 1);
            pricingIndex += 1;

            if (pricingIndex === pricingText.length) {
                pricingCursor.style.visibility = 'hidden';
                return;
            }
            setTimeout(typePricing, pricingSpeed);
        };

        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                typePricing();
                observer.disconnect();
            }
        });
        observer.observe(pricingTarget);
    }

    // -------------------------------------------------------------
    // 4. NOVO: TYPEWRITER FAQ ("Frequently..." -> Apaga -> "FAQ")
    // -------------------------------------------------------------
    const faqTarget = document.getElementById('faq-typewriter-text');
    const faqCursor = faqTarget ? faqTarget.nextElementSibling : null;

    if (faqTarget && faqCursor) {
        const textLong = 'Frequently Asked Questions';
        const textFinal = 'FAQ';

        const typeSpeed = 40;
        const eraseSpeed = 15;

        let charIndex = 0;
        let phase = 1; // 1 = Digitar Longo, 2 = Apagar, 3 = Digitar Curto

        const typeFaqSequence = () => {

            // FASE 1: Digita "Frequently Asked Questions"
            if (phase === 1) {
                faqTarget.textContent = textLong.slice(0, charIndex + 1);
                charIndex++;

                if (charIndex === textLong.length) {
                    phase = 2;
                    setTimeout(typeFaqSequence, 750); // Pausa 1s antes de apagar
                    return;
                }
                setTimeout(typeFaqSequence, typeSpeed);
            }

            // FASE 2: Apaga tudo
            else if (phase === 2) {
                faqTarget.textContent = textLong.slice(0, charIndex - 1);
                charIndex--;

                if (charIndex === 0) {
                    phase = 3;
                    setTimeout(typeFaqSequence, 300); // Pausa curtinha antes de escrever FAQ
                    return;
                }
                setTimeout(typeFaqSequence, eraseSpeed);
            }

            // FASE 3: Escreve "FAQ"
            else if (phase === 3) {
                faqTarget.textContent = textFinal.slice(0, charIndex + 1);
                charIndex++;

                if (charIndex === textFinal.length) {
                    // Fim da animação
                    faqCursor.style.visibility = 'hidden';
                    return;
                }
                setTimeout(typeFaqSequence, typeSpeed);
            }
        };

        // Observer para iniciar apenas quando chegar na tela
        const faqObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                typeFaqSequence();
                faqObserver.disconnect();
            }
        });
        faqObserver.observe(faqTarget);
    }
});