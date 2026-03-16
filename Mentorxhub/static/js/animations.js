/* =========
   Animations Modernes - MentorXHub
   Selon context.md - Gestion complète des animations
   ========= */

document.addEventListener("DOMContentLoaded", () => {
    /* 6. Scroll-Triggered Animations */
    initScrollReveal();
    
    /* 7. Staggered Reveal */
    initStaggeredReveal();
    
    /* 9. Skeleton Loader */
    initSkeletonLoaders();
    
    /* 10. Micro-Interactions - Ripple effect */
    initRippleEffects();
    
    /* 10. Micro-Interactions - Hover effects */
    initHoverEffects();
    
    /* 5. Parallax Scrolling */
    initParallax();
    
    /* 8. Text Animation - Typewriter effect */
    initTypewriter();
});

/* Scroll-Triggered Animations avec Intersection Observer */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(".reveal");
    
    if (!("IntersectionObserver" in window)) {
        revealElements.forEach(el => el.classList.add("active"));
        return;
    }
    
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: "0px 0px -50px 0px" }
    );
    
    revealElements.forEach(el => observer.observe(el));
}

/* Staggered Reveal - Apparition progressive */
function initStaggeredReveal() {
    const staggerElements = document.querySelectorAll(".reveal-stagger");
    
    if (!("IntersectionObserver" in window)) {
        staggerElements.forEach(el => el.classList.add("active"));
        return;
    }
    
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );
    
    staggerElements.forEach(el => observer.observe(el));
}

/* Skeleton Loader - Masquer après chargement */
function initSkeletonLoaders() {
    const skeletons = document.querySelectorAll(".skeleton");
    
    // Simuler le chargement (à remplacer par de vrais appels API)
    setTimeout(() => {
        skeletons.forEach(skeleton => {
            skeleton.classList.remove("skeleton");
            skeleton.classList.add("fade-in");
        });
    }, 1000);
}

/* Ripple Effect sur les boutons */
function initRippleEffects() {
    const buttons = document.querySelectorAll(".btn, .ripple");
    
    buttons.forEach(button => {
        if (!button.classList.contains("ripple")) {
            button.classList.add("ripple");
        }
        
        button.addEventListener("click", function(e) {
            const ripple = document.createElement("span");
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + "px";
            ripple.style.left = x + "px";
            ripple.style.top = y + "px";
            ripple.classList.add("ripple-effect");
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

/* Hover Effects - Lift et Scale */
function initHoverEffects() {
    // Les classes CSS .hover-lift et .hover-scale gèrent déjà les effets
    // On ajoute juste des listeners pour des animations supplémentaires si besoin
    const cards = document.querySelectorAll(".card, .feature-card");
    
    cards.forEach(card => {
        if (!card.classList.contains("hover-lift")) {
            card.classList.add("hover-lift");
        }
    });
}

/* Parallax Scrolling */
function initParallax() {
    const parallaxElements = document.querySelectorAll(".parallax");
    
    if (parallaxElements.length === 0) return;
    
    window.addEventListener("scroll", () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/* Typewriter Effect */
function initTypewriter() {
    const typewriterElements = document.querySelectorAll(".typewriter");
    
    typewriterElements.forEach(element => {
        const text = element.textContent;
        element.textContent = "";
        element.style.borderRight = "2px solid";
        
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
                setTimeout(() => {
                    element.style.borderRight = "none";
                }, 500);
            }
        }, 50);
    });
}

/* Utility: Animate element on scroll */
export function animateOnScroll(element, animationClass = "fade-in-up") {
    if (!("IntersectionObserver" in window)) {
        element.classList.add(animationClass);
        return;
    }
    
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add(animationClass);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );
    
    observer.observe(element);
}

/* Utility: Trigger animation manually */
export function triggerAnimation(element, animationClass) {
    element.classList.remove(animationClass);
    void element.offsetWidth; // Force reflow
    element.classList.add(animationClass);
}
