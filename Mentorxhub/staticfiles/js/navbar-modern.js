document.addEventListener("DOMContentLoaded", () => {
    const toggler = document.querySelector(".navbar-toggler-modern");
    const centerNav = document.querySelector(".navbar-center");
    const actions = document.querySelector(".navbar-actions-modern");
    const dropdowns = document.querySelectorAll(".nav-dropdown-modern");
    const alertCloses = document.querySelectorAll(".alert-close");

    // Mobile navigation toggle
    if (toggler) {
        toggler.addEventListener("click", () => {
            const isExpanded = toggler.getAttribute("aria-expanded") === "true";
            toggler.setAttribute("aria-expanded", (!isExpanded).toString());
            toggler.classList.toggle("active");
            centerNav?.classList.toggle("active");
            actions?.classList.toggle("active");
        });
    }

    // Dropdown interactions (click on mobile, hover on desktop)
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector(".dropdown-btn, .profile-chip, .user-chip-modern, .nav-item-modern");

        if (!trigger) {
            return;
        }

        // Keyboard accessibility
        trigger.addEventListener("keydown", event => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                dropdown.classList.toggle("open");
            }
            if (event.key === "Escape") {
                dropdown.classList.remove("open");
            }
        });

        trigger.addEventListener("click", event => {
            // avoid navigating for anchor buttons
            if (trigger.tagName === "A" && trigger.getAttribute("href") && trigger.getAttribute("href") !== "#") {
                return;
            }
            event.preventDefault();
            dropdown.classList.toggle("open");
        });

        // Hover effects (desktop only), but exclude user dropdown which should be click-only
        if (!dropdown.querySelector('.user-chip-modern')) {
            dropdown.addEventListener("mouseenter", () => {
                if (window.matchMedia("(min-width: 821px)").matches) {
                    dropdown.classList.add("open");
                }
            });

            dropdown.addEventListener("mouseleave", () => {
                if (window.matchMedia("(min-width: 821px)").matches) {
                    dropdown.classList.remove("open");
                }
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener("click", event => {
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(event.target)) {
                dropdown.classList.remove("open");
            }
        });
    });

    // Smooth closing for alerts
    alertCloses.forEach(button => {
        button.addEventListener("click", () => {
            const alert = button.closest(".alert");
            if (!alert) {
                return;
            }
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-6px)";
            setTimeout(() => alert.remove(), 250);
        });
    });

    // Elevate header on scroll
    const header = document.querySelector(".site-header");
    if (header) {
        const handleScroll = () => {
            if (window.scrollY > 10) {
                header.classList.add("is-scrolled");
            } else {
                header.classList.remove("is-scrolled");
            }
        };

        handleScroll();
        window.addEventListener("scroll", handleScroll);
    }
});
