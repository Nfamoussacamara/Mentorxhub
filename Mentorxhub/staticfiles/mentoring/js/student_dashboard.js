/* ============================================
   JAVASCRIPT POUR DASHBOARD ÉTUDIANT
   Student Dashboard - MentorXHub
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
    console.log('Dashboard étudiant chargé');
    
    // Initialisation des interactions
    initDashboardInteractions();
});

/**
 * Initialise les interactions du dashboard
 */
function initDashboardInteractions() {
    // Animation des cartes de statistiques au scroll
    const statCards = document.querySelectorAll('.stat-card');
    
    if (statCards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, { threshold: 0.1 });
        
        statCards.forEach(card => observer.observe(card));
    }
}
