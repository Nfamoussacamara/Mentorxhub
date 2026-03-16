document.addEventListener("DOMContentLoaded", () => {
    /* Reveal-on-scroll animation - Selon context.md */
    const revealElements = document.querySelectorAll(".reveal");
    const revealStaggerElements = document.querySelectorAll(".reveal-stagger");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("active");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.18, rootMargin: "0px 0px -50px 0px" }
        );

        revealElements.forEach(element => observer.observe(element));
        revealStaggerElements.forEach(element => observer.observe(element));
    } else {
        revealElements.forEach(element => element.classList.add("active"));
        revealStaggerElements.forEach(element => element.classList.add("active"));
    }

    /* Parallax Hero Illustration */
    const heroIllustration = document.querySelector(".hero-illustration");
    if (heroIllustration) {
        const applyTilt = (xRatio, yRatio) => {
            heroIllustration.style.transform = `perspective(900px) rotateX(${(yRatio - 0.5) * -6}deg) rotateY(${(xRatio - 0.5) * 6}deg)`;
        };

        heroIllustration.addEventListener("mousemove", event => {
            const rect = heroIllustration.getBoundingClientRect();
            const xRatio = (event.clientX - rect.left) / rect.width;
            const yRatio = (event.clientY - rect.top) / rect.height;
            applyTilt(xRatio, yRatio);
        });

        heroIllustration.addEventListener("mouseleave", () => {
            heroIllustration.style.transform = "perspective(900px) rotateX(0deg) rotateY(0deg)";
        });
    }

    /* Auto-dismiss alerts after 5 seconds */
    document.querySelectorAll(".alert").forEach(alert => {
        const dismiss = () => {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-6px)";
            setTimeout(() => alert.remove(), 250);
        };

        setTimeout(dismiss, 5000);
        const closeBtn = alert.querySelector(".alert-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", dismiss);
        }
    });
});

