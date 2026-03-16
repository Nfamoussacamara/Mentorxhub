/**
 * MentorXHub - JavaScript pour la page d'inscription
 * Signup - Version améliorée
 */

document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // ÉLÉMENTS DU FORMULAIRE
    // ============================================
    const signupForm = document.getElementById('signupForm');
    const firstNameInput = document.getElementById('first_name');
    const lastNameInput = document.getElementById('last_name');
    const emailInput = document.getElementById('email');
    const password1Input = document.getElementById('password1');
    const password2Input = document.getElementById('password2');
    const roleInputs = document.querySelectorAll('input[name="role"]');
    const submitBtn = document.querySelector('.submit-btn');

    // ============================================
    // FONCTIONS UTILITAIRES
    // ============================================
    
    // Validation format email
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Calcul de la force du mot de passe
    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[^a-zA-Z\d]/.test(password)) strength++;
        return Math.min(strength, 4); // 0-4 (faible à très fort)
    }

    // Obtenir le texte de la force du mot de passe
    function getPasswordStrengthText(strength) {
        const texts = ['Très faible', 'Faible', 'Moyen', 'Fort', 'Très fort'];
        return texts[strength] || '';
    }

    // Obtenir la classe CSS pour la force
    function getPasswordStrengthClass(strength) {
        const classes = ['very-weak', 'weak', 'medium', 'strong', 'very-strong'];
        return classes[strength] || '';
    }

    // Afficher/masquer l'indicateur de validation
    function showValidationIndicator(input, isValid, message = '') {
        let indicator = input.parentElement.querySelector('.validation-indicator');
        if (!indicator) {
            indicator = document.createElement('span');
            indicator.className = 'validation-indicator';
            input.parentElement.appendChild(indicator);
        }

        if (isValid) {
            indicator.textContent = '✓';
            indicator.className = 'validation-indicator valid';
            input.classList.remove('error');
            input.classList.add('valid');
        } else if (input.value.length > 0) {
            indicator.textContent = '✗';
            indicator.className = 'validation-indicator invalid';
            input.classList.remove('valid');
            input.classList.add('error');
        } else {
            indicator.textContent = '';
            indicator.className = 'validation-indicator';
            input.classList.remove('error', 'valid');
        }
    }

    // ============================================
    // TOGGLE PASSWORD VISIBILITY
    // ============================================
    window.togglePass = function(fieldId) {
        const input = document.getElementById(fieldId);
        const toggleBtn = input?.parentElement.querySelector('.password-toggle');
        
        if (!input || !toggleBtn) return;

        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        
        // Mettre à jour l'icône
        if (isPassword) {
            toggleBtn.setAttribute('aria-label', 'Masquer le mot de passe');
            toggleBtn.classList.add('active');
            toggleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
            `;
        } else {
            toggleBtn.setAttribute('aria-label', 'Afficher le mot de passe');
            toggleBtn.classList.remove('active');
            toggleBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                </svg>
            `;
        }
    };

    // ============================================
    // VALIDATION EN TEMPS RÉEL - PRÉNOM
    // ============================================
    if (firstNameInput) {
        firstNameInput.addEventListener('input', function() {
            const value = this.value.trim();
            const isValid = value.length >= 2 && /^[a-zA-ZÀ-ÿ\s-']+$/.test(value);
            showValidationIndicator(this, isValid);
        });

        firstNameInput.addEventListener('blur', function() {
            const value = this.value.trim();
            if (value.length > 0 && value.length < 2) {
                this.classList.add('error');
            }
        });
    }

    // ============================================
    // VALIDATION EN TEMPS RÉEL - NOM
    // ============================================
    if (lastNameInput) {
        lastNameInput.addEventListener('input', function() {
            const value = this.value.trim();
            const isValid = value.length >= 2 && /^[a-zA-ZÀ-ÿ\s-']+$/.test(value);
            showValidationIndicator(this, isValid);
        });

        lastNameInput.addEventListener('blur', function() {
            const value = this.value.trim();
            if (value.length > 0 && value.length < 2) {
                this.classList.add('error');
            }
        });
    }

    // ============================================
    // VALIDATION EN TEMPS RÉEL - EMAIL
    // ============================================
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            const email = this.value.trim();
            const isValid = email.length > 0 && isValidEmail(email);
            showValidationIndicator(this, isValid);
        });
    }

    // ============================================
    // INDICATEUR DE FORCE DU MOT DE PASSE
    // ============================================
    if (password1Input) {
        // Créer l'indicateur de force si il n'existe pas
        let strengthIndicator = document.getElementById('password-strength');
        if (!strengthIndicator) {
            strengthIndicator = document.createElement('div');
            strengthIndicator.id = 'password-strength';
            strengthIndicator.className = 'password-strength';
            password1Input.parentElement.parentElement.appendChild(strengthIndicator);
        }

        password1Input.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            const strengthText = getPasswordStrengthText(strength);
            const strengthClass = getPasswordStrengthClass(strength);

            // Mettre à jour l'indicateur
            if (password.length > 0) {
                strengthIndicator.style.display = 'block';
                strengthIndicator.className = `password-strength ${strengthClass}`;
                strengthIndicator.innerHTML = `
                    <div class="strength-bar">
                        <div class="strength-fill" style="width: ${(strength + 1) * 20}%"></div>
                    </div>
                    <span class="strength-text">${strengthText}</span>
                `;
            } else {
                strengthIndicator.style.display = 'none';
            }

            // Valider la correspondance si password2 existe
            if (password2Input && password2Input.value.length > 0) {
                validatePasswordMatch();
            }
        });
    }

    // ============================================
    // VALIDATION CORRESPONDANCE MOTS DE PASSE
    // ============================================
    function validatePasswordMatch() {
        if (!password1Input || !password2Input) return;

        const match = password1Input.value === password2Input.value;
        const hasValue = password2Input.value.length > 0;

        if (hasValue) {
            showValidationIndicator(password2Input, match);
            
            // Afficher un message d'erreur personnalisé
            let matchMessage = password2Input.parentElement.parentElement.querySelector('.password-match-message');
            if (!matchMessage && hasValue) {
                matchMessage = document.createElement('span');
                matchMessage.className = 'password-match-message';
                password2Input.parentElement.parentElement.appendChild(matchMessage);
            }

            if (matchMessage) {
                if (match && hasValue) {
                    matchMessage.textContent = 'Les mots de passe correspondent';
                    matchMessage.className = 'password-match-message valid';
                } else if (hasValue && !match) {
                    matchMessage.textContent = 'Les mots de passe ne correspondent pas';
                    matchMessage.className = 'password-match-message invalid';
                } else {
                    matchMessage.textContent = '';
                }
            }
        }
    }

    if (password2Input) {
        password2Input.addEventListener('input', validatePasswordMatch);
    }

    // ============================================
    // VALIDATION RÔLE
    // ============================================
    if (roleInputs.length > 0) {
        roleInputs.forEach(radio => {
            radio.addEventListener('change', function() {
                const roleSelector = document.querySelector('.role-selector');
                if (roleSelector) {
                    roleSelector.classList.add('role-selected');
                }
            });
        });
    }

    // ============================================
    // VALIDATION COMPLÈTE AVANT SOUMISSION
    // ============================================
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            let isValid = true;
            const errors = [];

            // Valider prénom
            if (firstNameInput && (!firstNameInput.value.trim() || firstNameInput.value.trim().length < 2)) {
                isValid = false;
                firstNameInput.classList.add('error');
                errors.push('Le prénom doit contenir au moins 2 caractères');
            }

            // Valider nom
            if (lastNameInput && (!lastNameInput.value.trim() || lastNameInput.value.trim().length < 2)) {
                isValid = false;
                lastNameInput.classList.add('error');
                errors.push('Le nom doit contenir au moins 2 caractères');
            }

            // Valider email
            if (emailInput && (!emailInput.value.trim() || !isValidEmail(emailInput.value.trim()))) {
                isValid = false;
                emailInput.classList.add('error');
                errors.push('Veuillez entrer une adresse email valide');
            }

            // Valider rôle
            const roleSelected = Array.from(roleInputs).some(radio => radio.checked);
            if (!roleSelected) {
                isValid = false;
                const roleSelector = document.querySelector('.role-selector');
                if (roleSelector) {
                    roleSelector.classList.add('error');
                }
                errors.push('Veuillez sélectionner un rôle');
            }

            // Valider mots de passe
            if (password1Input && password1Input.value.length < 8) {
                isValid = false;
                password1Input.classList.add('error');
                errors.push('Le mot de passe doit contenir au moins 8 caractères');
            }

            if (password1Input && password2Input && password1Input.value !== password2Input.value) {
                isValid = false;
                password2Input.classList.add('error');
                errors.push('Les mots de passe ne correspondent pas');
            }

            if (!isValid) {
                e.preventDefault();
                
                // Afficher les erreurs
                let errorContainer = document.querySelector('.client-validation-errors');
                if (!errorContainer) {
                    errorContainer = document.createElement('div');
                    errorContainer.className = 'error-box client-validation-errors';
                    signupForm.insertBefore(errorContainer, signupForm.firstChild.nextSibling);
                }
                
                errorContainer.innerHTML = `
                    <strong>Veuillez corriger les erreurs suivantes :</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem; padding: 0;">
                        ${errors.map(err => `<li>${err}</li>`).join('')}
                    </ul>
                `;
                errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

                // Focus sur le premier champ en erreur
                const firstError = signupForm.querySelector('.error');
                if (firstError) {
                    firstError.focus();
                }

                return false;
            }

            // Animation de chargement
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = '<span>Création du compte...</span>';
            }
        });
    }

    // ============================================
    // RETIRER LES ERREURS AU FOCUS
    // ============================================
    [firstNameInput, lastNameInput, emailInput, password1Input, password2Input].forEach(input => {
        if (input) {
            input.addEventListener('focus', function() {
                this.classList.remove('error');
                const errorContainer = document.querySelector('.client-validation-errors');
                if (errorContainer) {
                    errorContainer.remove();
                }
            });
        }
    });
});

