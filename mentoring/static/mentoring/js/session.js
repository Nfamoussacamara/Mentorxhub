// Fonctionnalités pour les pages de session
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du formulaire de feedback
    const feedbackForm = document.querySelector('.feedback-form');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validation du formulaire
            const rating = document.querySelector('#rating').value;
            const comment = document.querySelector('#comment').value;
            
            if (!rating || !comment) {
                showError('Veuillez remplir tous les champs requis.');
                return;
            }

            // Envoi des données au serveur
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccess('Merci pour votre feedback !');
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                } else {
                    showError(data.message);
                }
            })
            .catch(error => {
                showError('Une erreur est survenue. Veuillez réessayer.');
            });
        });
    }

    // Gestion des actions de session
    const sessionActions = document.querySelectorAll('.session-btn');
    sessionActions.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.classList.contains('session-btn-danger')) {
                e.preventDefault();
                if (confirm('Êtes-vous sûr de vouloir annuler cette session ?')) {
                    window.location.href = this.href;
                }
            }
        });
    });

    // Gestion du lien de réunion
    const meetingLink = document.querySelector('.session-detail a');
    if (meetingLink) {
        meetingLink.addEventListener('click', function(e) {
            e.preventDefault();
            const link = this.href;
            
            // Copier le lien dans le presse-papiers
            navigator.clipboard.writeText(link).then(() => {
                showSuccess('Lien copié dans le presse-papiers !');
            }).catch(() => {
                window.open(link, '_blank');
            });
        });
    }
});

// Fonction utilitaire pour récupérer le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fonction pour afficher les messages d'erreur
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.session-container');
    container.insertBefore(errorDiv, container.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Fonction pour afficher les messages de succès
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.textContent = message;
    
    const container = document.querySelector('.session-container');
    container.insertBefore(successDiv, container.firstChild);
    
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
} 