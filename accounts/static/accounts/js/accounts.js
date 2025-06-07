document.addEventListener('DOMContentLoaded', function() {
    // Gestion des messages flash
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // Validation des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Veuillez remplir tous les champs obligatoires.');
            }
        });
    });

    // Gestion des mots de passe
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'btn btn-link password-toggle';
        toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        
        field.parentNode.style.position = 'relative';
        field.parentNode.appendChild(toggleButton);

        toggleButton.addEventListener('click', () => {
            const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', type);
            toggleButton.innerHTML = `<i class="fas fa-eye${type === 'password' ? '' : '-slash'}"></i>`;
        });
    });

    // Validation de la force du mot de passe
    const passwordInput = document.querySelector('input[name="password1"]');
    if (passwordInput) {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'password-strength';
        passwordInput.parentNode.appendChild(strengthMeter);

        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;

            const strengthClasses = ['very-weak', 'weak', 'medium', 'strong', 'very-strong'];
            const strengthTexts = ['Très faible', 'Faible', 'Moyen', 'Fort', 'Très fort'];
            
            strengthMeter.className = `password-strength ${strengthClasses[strength - 1]}`;
            strengthMeter.textContent = `Force du mot de passe : ${strengthTexts[strength - 1]}`;
        });
    }

    // Gestion de la déconnexion
    const logoutButton = document.querySelector('.logout-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                window.location.href = this.href;
            }
        });
    }
}); 