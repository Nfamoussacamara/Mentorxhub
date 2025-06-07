// Initialisation des animations et interactions de la page d'accueil
document.addEventListener('DOMContentLoaded', function() {
    // Animation des cartes de mentors
    const mentorCards = document.querySelectorAll('.mentor-card');
    mentorCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animation des statistiques
    const statsItems = document.querySelectorAll('.stats-item');
    statsItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 200);
    });

    // Gestion des boutons d'action
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.getAttribute('href')) {
                e.preventDefault();
                // Ajouter ici la logique pour les boutons sans lien
            }
        });
    });
}); 