document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector(".site-header");
    const revealElements = document.querySelectorAll("[data-reveal]");
    const faqButtons = document.querySelectorAll(".faq-question");
    const ctaButton = document.querySelector("[data-cta]");

    /**
     * Sticky header state
     */
    const handleScroll = () => {
        if (!header) {
            return;
        }
        header.classList.toggle("is-scrolled", window.scrollY > 16);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });

    /**
     * Reveal on scroll animation
     */
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        obs.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.2,
                rootMargin: "0px 0px -10% 0px",
            }
        );

        revealElements.forEach((element) => observer.observe(element));
    } else {
        revealElements.forEach((element) => element.classList.add("is-visible"));
    }

    /**
     * FAQ accordion interactions
     */
    faqButtons.forEach((button) => {
        const parent = button.closest(".faq-item");
        const answerId = button.getAttribute("aria-controls");
        const answer = answerId ? document.getElementById(answerId) : null;

        button.addEventListener("click", () => {
            const isExpanded = button.getAttribute("aria-expanded") === "true";

            button.setAttribute("aria-expanded", String(!isExpanded));
            parent?.classList.toggle("open", !isExpanded);

            if (answer) {
                if (!isExpanded) {
                    answer.style.maxHeight = `${answer.scrollHeight}px`;
                } else {
                    answer.style.maxHeight = "0px";
                }
            }

            // collapse other items
            if (!isExpanded) {
                faqButtons.forEach((otherButton) => {
                    if (otherButton === button) return;
                    otherButton.setAttribute("aria-expanded", "false");
                    const otherParent = otherButton.closest(".faq-item");
                    const otherAnswerId = otherButton.getAttribute("aria-controls");
                    const otherAnswer = otherAnswerId ? document.getElementById(otherAnswerId) : null;

                    otherParent?.classList.remove("open");
                    if (otherAnswer) {
                        otherAnswer.style.maxHeight = "0px";
                    }
                });
            }
        });
    });

    /**
     * Micro-interaction for CTA button
     */
    if (ctaButton) {
        const resetCTA = () => {
            ctaButton.style.setProperty("--cta-x", "50%");
            ctaButton.style.setProperty("--cta-y", "50%");
        };

        ctaButton.addEventListener("pointermove", (event) => {
            const rect = ctaButton.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width) * 100;
            const y = ((event.clientY - rect.top) / rect.height) * 100;
            ctaButton.style.setProperty("--cta-x", `${x}%`);
            ctaButton.style.setProperty("--cta-y", `${y}%`);
        });

        ctaButton.addEventListener("pointerleave", resetCTA);
        resetCTA();
    }
});
