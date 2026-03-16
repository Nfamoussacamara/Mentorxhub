/**
 * MentorXHub - JavaScript pour les pages de mise à jour de profil
 * Profile Update - Version pour student et mentor
 */

document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // ÉLÉMENTS DU FORMULAIRE
    // ============================================
    const form = document.querySelector('form');
    const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

    // ============================================
    // VALIDATION EN TEMPS RÉEL
    // ============================================
    if (form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Retirer les classes d'erreur au focus
            input.addEventListener('focus', function() {
                this.classList.remove('error');
                const errorList = this.closest('.form-group')?.querySelector('.errorlist');
                if (errorList) {
                    errorList.style.display = 'none';
                }
            });

            // Validation basique en temps réel
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    }

    // ============================================
    // FONCTION DE VALIDATION
    // ============================================
    function validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        const fieldType = field.type;
        let isValid = true;

        // Validation pour les champs requis
        if (isRequired && !value) {
            isValid = false;
        }

        // Validation pour les URLs
        if (fieldType === 'url' && value) {
            try {
                new URL(value);
            } catch (e) {
                isValid = false;
            }
        }

        // Validation pour les nombres
        if (fieldType === 'number' && value) {
            const num = parseFloat(value);
            if (isNaN(num) || num < 0) {
                isValid = false;
            }
        }

        // Appliquer les classes CSS
        if (isValid) {
            field.classList.remove('error');
            field.classList.add('valid');
        } else {
            field.classList.remove('valid');
            field.classList.add('error');
        }

        return isValid;
    }

    // ============================================
    // VALIDATION AVANT SOUMISSION
    // ============================================
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                
                // Afficher un message d'erreur
                let errorContainer = form.querySelector('.client-validation-errors');
                if (!errorContainer) {
                    errorContainer = document.createElement('div');
                    errorContainer.className = 'alert alert-error client-validation-errors';
                    form.insertBefore(errorContainer, form.firstChild);
                }
                
                errorContainer.textContent = 'Veuillez corriger les erreurs dans le formulaire avant de soumettre.';
                errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                // Animation de chargement
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.classList.add('loading');
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enregistrement...';
                    
                    // Réactiver après 5 secondes au cas où la soumission échoue
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.classList.remove('loading');
                        submitBtn.innerHTML = originalText;
                    }, 5000);
                }
            }
        });
    }

    // ============================================
    // AMÉLIORATION UX - AUTO-HIDE MESSAGES
    // ============================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success')) {
            // Masquer les messages de succès après 5 secondes
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }, 5000);
        }
    });
});

