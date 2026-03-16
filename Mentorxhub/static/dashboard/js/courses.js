/**
 * JavaScript pour la gestion des cours
 * Gestion de la progression, quiz, leçons
 */

// Utiliser l'API client global
const apiClient = window.apiClient;

const coursesApp = (function() {
    /**
     * Initialise l'application des cours
     */
    function init() {
        setupEventListeners();
        initProgressBars();
        console.log('Courses app initialized');
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Bouton d'inscription au cours
        const enrollBtn = document.querySelector('.enroll-btn');
        if (enrollBtn) {
            enrollBtn.addEventListener('click', handleCourseEnroll);
        }

        // Boutons de complétion de leçon
        const completeLessonBtns = document.querySelectorAll('.complete-lesson-btn');
        completeLessonBtns.forEach(btn => {
            btn.addEventListener('click', handleLessonComplete);
        });

        // Filtres de cours
        const filters = document.querySelectorAll('.course-filter');
        filters.forEach(filter => {
            filter.addEventListener('change', handleCourseFilter);
        });

        // Recherche de cours
        const searchInput = document.getElementById('course-search');
        if (searchInput) {
            searchInput.addEventListener('input', handleCourseSearch);
        }
    }

    /**
     * Initialise les barres de progression
     */
    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const fill = bar.querySelector('.progress-fill');
            if (fill) {
                const width = fill.style.width || '0%';
                // Animation de la barre
                setTimeout(() => {
                    fill.style.transition = 'width 0.5s ease';
                }, 100);
            }
        });
    }

    /**
     * Gère l'inscription à un cours
     */
    async function handleCourseEnroll(event) {
        const btn = event.target.closest('.enroll-btn');
        const courseId = btn.dataset.courseId;

        if (!courseId) return;

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Inscription...';

        try {
            // TODO: Créer une vue pour l'inscription
            // Pour l'instant, on redirige vers les détails
            window.location.href = `/dashboard/courses/${courseId}/`;
        } catch (error) {
            console.error('Error enrolling in course:', error);
            showToast('Erreur lors de l\'inscription', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-play"></i> Commencer le cours';
        }
    }

    /**
     * Gère la complétion d'une leçon
     */
    async function handleLessonComplete(event) {
        const btn = event.target.closest('.complete-lesson-btn');
        const courseId = btn.dataset.courseId;
        const lessonId = btn.dataset.lessonId;

        if (!courseId || !lessonId) return;

        btn.disabled = true;

        try {
            const response = await window.apiClient.post(
                `/dashboard/courses/${courseId}/lessons/${lessonId}/complete/`,
                {}
            );

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    // Mettre à jour l'UI
                    btn.closest('.lesson-item').classList.add('lesson-completed');
                    btn.innerHTML = '<i class="fas fa-check-circle"></i> Complétée';
                    btn.disabled = true;

                    // Mettre à jour la barre de progression
                    updateProgressBar(data.progress_percentage);
                    showToast('Leçon complétée !', 'success');
                }
            } else {
                showToast('Erreur lors de la complétion', 'error');
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Error completing lesson:', error);
            showToast('Erreur lors de la complétion', 'error');
            btn.disabled = false;
        }
    }

    /**
     * Met à jour la barre de progression
     */
    function updateProgressBar(percentage) {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${Math.round(percentage)}% complété`;
        }
    }

    /**
     * Gère le filtrage des cours
     */
    function handleCourseFilter(event) {
        const filterType = event.target.dataset.filter;
        const filterValue = event.target.value;
        
        // Filtrer les cartes de cours
        const courseCards = document.querySelectorAll('.course-card');
        courseCards.forEach(card => {
            const cardValue = card.dataset[filterType];
            if (!filterValue || cardValue === filterValue) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    /**
     * Gère la recherche de cours
     */
    function handleCourseSearch(event) {
        const searchTerm = event.target.value.toLowerCase();
        const courseCards = document.querySelectorAll('.course-card');
        
        courseCards.forEach(card => {
            const title = card.querySelector('.course-title')?.textContent.toLowerCase() || '';
            const description = card.querySelector('.course-description')?.textContent.toLowerCase() || '';
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    /**
     * Affiche un toast
     */
    function showToast(message, type = 'info') {
        if (window.showToast) {
            window.showToast(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }

    return {
        init: init,
    };
})();

// Auto-initialisation
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => coursesApp.init());
} else {
    coursesApp.init();
}

