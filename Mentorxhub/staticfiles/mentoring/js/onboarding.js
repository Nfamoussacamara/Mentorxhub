/**
 * MentorXHub - JavaScript pour les pages d'onboarding
 * Mentor et Mentee Onboarding
 */

document.addEventListener('DOMContentLoaded', function() {
    // Gestion du bouton "Passer cette étape" (mentee_form)
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

