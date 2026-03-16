/* ============================================
   JAVASCRIPT POUR FORMULAIRE DE FEEDBACK
   Session Feedback - MentorXHub
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('ratingInput');
    const ratingText = document.getElementById('ratingText');
    const submitBtn = document.getElementById('submitBtn');

    if (!stars.length || !ratingInput || !ratingText || !submitBtn) {
        return;
    }

    const ratingLabels = {
        1: 'Décevant',
        2: 'Moyen',
        3: 'Bien',
        4: 'Très bien',
        5: 'Excellent !'
    };

    // Gestion du clic sur les étoiles
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.dataset.rating;
            ratingInput.value = rating;
            submitBtn.disabled = false;

            // Mise à jour des étoiles
            updateStars(rating, stars);

            // Mise à jour du texte
            ratingText.textContent = ratingLabels[rating];
            ratingText.style.color = '#fbbf24';
            ratingText.style.fontWeight = '600';
        });

        // Effet hover
        star.addEventListener('mouseenter', function () {
            const rating = this.dataset.rating;
            updateStars(rating, stars);
        });
    });

    // Réinitialisation au survol de la zone
    const starRating = document.getElementById('starRating');
    if (starRating) {
        starRating.addEventListener('mouseleave', function () {
            const currentRating = ratingInput.value;
            if (currentRating) {
                updateStars(currentRating, stars);
            } else {
                resetStars(stars);
            }
        });
    }
});

/**
 * Met à jour l'affichage des étoiles
 * @param {string} rating - La note sélectionnée
 * @param {NodeList} stars - La liste des étoiles
 */
function updateStars(rating, stars) {
    stars.forEach(s => {
        const starRating = s.dataset.rating;
        if (starRating <= rating) {
            s.classList.remove('far');
            s.classList.add('fas', 'active');
        } else {
            s.classList.remove('fas', 'active');
            s.classList.add('far');
        }
    });
}

/**
 * Réinitialise l'affichage des étoiles
 * @param {NodeList} stars - La liste des étoiles
 */
function resetStars(stars) {
    stars.forEach(s => {
        s.classList.remove('fas', 'active');
        s.classList.add('far');
    });
}

