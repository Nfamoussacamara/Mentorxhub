// Fonctionnalités pour les pages de mentor
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des disponibilités
    const availabilityItems = document.querySelectorAll('.availability-item');
    availabilityItems.forEach(item => {
        item.addEventListener('click', function() {
            // Ajouter la logique de sélection de disponibilité
            this.classList.toggle('selected');
        });
    });

    // Gestion du formulaire de réservation
    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Validation du formulaire
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Vérification des champs requis
            let isValid = true;
            for (let key in data) {
                if (!data[key]) {
                    isValid = false;
                    const input = this.querySelector(`[name="${key}"]`);
                    input.classList.add('is-invalid');
                }
            }

            if (isValid) {
                // Envoi des données au serveur
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
                        window.location.href = data.redirect_url;
                    } else {
                        showError(data.message);
                    }
                })
                .catch(error => {
                    showError('Une erreur est survenue. Veuillez réessayer.');
                });
            }
        });
    }

    // Gestion des évaluations
    const ratingInputs = document.querySelectorAll('.rating-input');
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const rating = this.value;
            const stars = document.querySelectorAll('.rating-star');
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
        });
    });
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
    
    const form = document.querySelector('.booking-form');
    form.insertBefore(errorDiv, form.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
} 