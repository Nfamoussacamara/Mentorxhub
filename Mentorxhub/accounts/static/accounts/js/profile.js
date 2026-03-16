/* ============================================
   JAVASCRIPT POUR PAGE DE PROFIL MODERNE
   Modern Profile Page - MentorXHub
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Animation d'entrée pour les sections
    const sections = document.querySelectorAll('.profile-section, .profile-card');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        
        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Animation pour les cartes de stats
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.9)';
        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
        }, 200 + index * 100);
    });

    // Animation pour les activités
    const activities = document.querySelectorAll('.activity-item');
    activities.forEach((activity, index) => {
        activity.style.opacity = '0';
        activity.style.transform = 'translateX(-20px)';
        activity.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        
        setTimeout(() => {
            activity.style.opacity = '1';
            activity.style.transform = 'translateX(0)';
        }, 300 + index * 100);
    });

    // Gestion du formulaire (pour profile_edit.html)
    const profileForm = document.getElementById('profileForm');
    const submitBtn = document.getElementById('submitBtn');
    const learningGoalsTextarea = document.getElementById('id_learning_goals');
    const charCounter = document.getElementById('learning-goals-counter');
    const charCount = document.getElementById('char-count');

    // Compteur de caractères pour les objectifs d'apprentissage
    if (learningGoalsTextarea && charCounter && charCount) {
        function updateCharCounter() {
            const length = learningGoalsTextarea.value.length;
            charCount.textContent = length;
            
            // Mettre à jour la classe selon la longueur
            charCounter.classList.remove('warning', 'error');
            if (length > 450) {
                charCounter.classList.add('error');
            } else if (length > 400) {
                charCounter.classList.add('warning');
            }
        }

        // Initialiser le compteur
        updateCharCounter();
        
        // Mettre à jour lors de la saisie
        learningGoalsTextarea.addEventListener('input', updateCharCounter);
    }

    // Gestion de la soumission du formulaire
    if (profileForm && submitBtn) {
        profileForm.addEventListener('submit', function(e) {
            // Désactiver le bouton et afficher le loading
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            
            // Le formulaire sera soumis normalement
            // Le bouton sera réactivé si le formulaire est invalide (via le rechargement de la page)
        });
    }

    // Effet de parallaxe léger sur le scroll
    let lastScroll = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        const profileHeader = document.querySelector('.profile-header-card');
        
        if (profileHeader && currentScroll < 300) {
            const parallax = currentScroll * 0.3;
            profileHeader.style.transform = `translateY(${parallax}px)`;
        }
        
        lastScroll = currentScroll;
    });

    // Animation au survol des badges de compétences
    const skillBadges = document.querySelectorAll('.skill-badge');
    skillBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.05)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Animation des liens sociaux
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
});
