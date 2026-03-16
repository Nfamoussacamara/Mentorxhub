/**
 * MentorXHub - JavaScript pour la page d'onboarding mentoré
 * Mentee Onboarding
 * Basé sur login.js pour cohérence
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('onboardingForm');
    const submitBtn = document.getElementById('submitBtn');
    const formStatus = document.getElementById('formStatus');

    // ============================================
    // COMPTEUR DE CARACTÈRES POUR TEXTAREA
    // ============================================
    const learningGoalsField = document.querySelector('textarea[name="learning_goals"]');
    const charCounter = document.getElementById('learning-goals-counter');
    const charCount = document.getElementById('char-count');
    const maxChars = 500;

    if (learningGoalsField && charCounter && charCount) {
        function updateCharCounter() {
            const currentLength = learningGoalsField.value.length;
            charCount.textContent = currentLength;
            
            // Retirer les classes précédentes
            charCounter.classList.remove('warning', 'error');
            
            // Ajouter les classes selon le nombre de caractères
            if (currentLength > maxChars) {
                charCounter.classList.add('error');
            } else if (currentLength > maxChars * 0.9) {
                charCounter.classList.add('warning');
            }
        }

        learningGoalsField.addEventListener('input', updateCharCounter);
        learningGoalsField.addEventListener('focus', updateCharCounter);
        updateCharCounter(); // Initialiser le compteur
    }

    // ============================================
    // VALIDATION VISUELLE EN TEMPS RÉEL
    // ============================================
    if (form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Validation lors de la saisie
            input.addEventListener('blur', function() {
                if (this.value.trim() !== '' && !this.classList.contains('error')) {
                    this.closest('.input-group')?.classList.add('valid');
                } else {
                    this.closest('.input-group')?.classList.remove('valid');
                }
            });

            // Retirer les animations d'erreur après correction
            input.addEventListener('focus', function () {
                this.classList.remove('error');
            });

            // Retirer la validation visuelle si le champ est vidé
            input.addEventListener('input', function() {
                if (this.value.trim() === '') {
                    this.closest('.input-group')?.classList.remove('valid');
                }
            });
        });

        // État de chargement du formulaire
        form.addEventListener('submit', function (e) {
            // Animation de chargement
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
            }
            if (formStatus) formStatus.textContent = 'Sauvegarde en cours...';
        });
    }

    // ============================================
    // GESTION DU BOUTON "PASSER CETTE ÉTAPE"
    // ============================================
    const skipButton = document.querySelector('.skip-button');
    if (skipButton) {
        skipButton.addEventListener('mouseenter', function() {
            this.style.borderColor = '#CBD5E1';
            this.style.color = '#374151';
        });
        
        skipButton.addEventListener('mouseleave', function() {
            this.style.borderColor = '#E5E7EB';
            this.style.color = '#6B7280';
        });
    }
});

