/**
 * MentorXHub - JavaScript pour la page de connexion
 * Login
 */

document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // VALIDATION EN TEMPS RÉEL DE L'EMAIL
    // ============================================
    const emailInput = document.getElementById('id_username');
    const emailValidator = document.getElementById('email-validator');
    const passwordInput = document.getElementById('id_password');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('loginForm');
    const formStatus = document.getElementById('formStatus');

    // Validation format email
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Validation en temps réel de l'email (si l'élément existe)
    if (emailInput && emailValidator) {
        emailInput.addEventListener('input', function () {
            const email = this.value.trim();

            if (email.length === 0) {
                emailValidator.textContent = '';
                emailValidator.className = 'validation-indicator';
                this.classList.remove('error');
            } else if (isValidEmail(email)) {
                emailValidator.textContent = '✓';
                emailValidator.className = 'validation-indicator valid';
                this.classList.remove('error');
            } else {
                emailValidator.textContent = '✗';
                emailValidator.className = 'validation-indicator invalid';
                this.classList.add('error');
            }
        });
    }

    // ============================================
    // TOGGLE PASSWORD VISIBILITY
    // ============================================
    window.togglePass = function() {
        const input = document.getElementById('id_password');
        const toggleBtn = document.getElementById('toggleBtn');

        if (!input || !toggleBtn) return;

        if (input.type === 'password') {
            input.type = 'text';
            toggleBtn.setAttribute('aria-label', 'Masquer le mot de passe');
            toggleBtn.classList.add('active');
            if (formStatus) formStatus.textContent = 'Mot de passe visible';

            // Changer en icône œil (visible)
            toggleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
            `;
        } else {
            input.type = 'password';
            toggleBtn.setAttribute('aria-label', 'Afficher le mot de passe');
            toggleBtn.classList.remove('active');
            if (formStatus) formStatus.textContent = 'Mot de passe masqué';

            // Changer en icône œil barré (masqué)
            toggleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                </svg>
            `;
        }
    };

    // ============================================
    // GESTION DU FORMULAIRE DE LOGIN
    // ============================================
    if (form) {
        // État de chargement du formulaire
        form.addEventListener('submit', function (e) {
            if (!emailInput || !passwordInput) return;

            const email = emailInput.value.trim();

            // Validation basique avant soumission
            if (!isValidEmail(email)) {
                e.preventDefault();
                emailInput.classList.add('error');
                emailInput.focus();
                if (formStatus) formStatus.textContent = 'Veuillez entrer une adresse email valide';
                return;
            }

            if (passwordInput.value.length === 0) {
                e.preventDefault();
                passwordInput.classList.add('error');
                passwordInput.focus();
                if (formStatus) formStatus.textContent = 'Veuillez entrer votre mot de passe';
                return;
            }

            // Animation de chargement (sauf si HTMX gère déjà)
            if (!form.hasAttribute('hx-post')) {
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.classList.add('loading');
                }
                if (formStatus) formStatus.textContent = 'Connexion en cours...';
            }
        });

        // Événements HTMX pour gérer le bouton de soumission
        form.addEventListener('htmx:beforeRequest', function () {
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
            }
            if (formStatus) formStatus.textContent = 'Connexion en cours...';
        });

        form.addEventListener('htmx:afterRequest', function () {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
            }
            if (formStatus) formStatus.textContent = '';
        });

        // Permettre la soumission avec Entrée depuis n'importe quel champ
        if (emailInput) {
            emailInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (passwordInput) passwordInput.focus();
                }
            });
        }

        if (passwordInput) {
            passwordInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    form.submit();
                }
            });
        }

        // Retirer les animations d'erreur après correction
        [emailInput, passwordInput].forEach(input => {
            if (input) {
                input.addEventListener('focus', function () {
                    this.classList.remove('error');
                });
            }
        });
    }

    // ============================================
    // ANIMATION DES PHRASES D'ACCROCHE
    // ============================================
    const taglines = [
        "Là où l'expérience rencontre l'ambition.",
        "Votre espace pour apprendre, guider et évoluer.",
        "Un pont entre passion et expertise.",
        "Progressez plus vite, ensemble.",
        "Chaque talent trouve un guide."
    ];

    const taglineElement = document.getElementById('tagline-text');
    if (taglineElement) {
        let currentTaglineIndex = 0;

        function rotateTagline() {
            taglineElement.style.opacity = '0';

            setTimeout(() => {
                currentTaglineIndex = (currentTaglineIndex + 1) % taglines.length;
                taglineElement.textContent = taglines[currentTaglineIndex];
                taglineElement.style.opacity = '1';
            }, 800);
        }

        // Changer de phrase toutes les 5 secondes
        setInterval(rotateTagline, 5000);
    }
});

