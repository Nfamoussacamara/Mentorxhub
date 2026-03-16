/**
 * Router JavaScript - Navigation AJAX pour Dashboard
 * Gère la navigation sans rechargement de page
 */

class DashboardRouter {
    constructor() {
        this.currentUrl = window.location.pathname;
        this.contentContainer = document.getElementById('dashboard-content');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.init();
    }

    init() {
        // Intercepter les clics sur les liens de navigation
        this.interceptLinks();
        
        // Gérer le bouton retour/avant du navigateur
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.url) {
                this.loadPage(e.state.url, false);
            }
        });
    }

    interceptLinks() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            
            if (!link) return;
            
            // Ignorer les liens externes, les ancres, et les liens avec target="_blank"
            if (link.hostname !== window.location.hostname ||
                link.target === '_blank' ||
                link.href.includes('#') ||
                link.getAttribute('data-no-ajax') === 'true') {
                return;
            }

            // Vérifier si c'est un lien du dashboard
            const href = link.getAttribute('href');
            if (href && (href.startsWith('/dashboard/') || href.startsWith('/accounts/profile'))) {
                e.preventDefault();
                this.navigate(href);
            }
        });
    }

    navigate(url) {
        // Mettre à jour l'URL sans recharger
        if (url !== this.currentUrl) {
            window.history.pushState({ url: url }, '', url);
            this.currentUrl = url;
            this.loadPage(url, true);
        }
    }

    async loadPage(url, updateHistory = true) {
        try {
            // Afficher le loader
            this.showLoader();

            // Faire la requête AJAX
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html',
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Vérifier si la réponse est JSON (AJAX) ou HTML
            const contentType = response.headers.get('content-type');
            let html;
            
            if (contentType && contentType.includes('application/json')) {
                // Réponse JSON avec HTML dans la propriété 'html'
                const data = await response.json();
                html = data.html || data;
            } else {
                // Réponse HTML directe
                html = await response.text();
            }

            // Remplacer le contenu avec animation
            this.transitionContent(html);

            // Mettre à jour l'URL active dans la sidebar
            this.updateActiveNav(url);

            // Initialiser les composants de la nouvelle page
            this.initPageComponents();

            // Masquer le loader
            this.hideLoader();

        } catch (error) {
            console.error('Erreur lors du chargement de la page:', error);
            this.showError('Erreur lors du chargement de la page. Veuillez réessayer.');
            this.hideLoader();
        }
    }

    transitionContent(html) {
        // Créer un conteneur temporaire
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const newContent = tempDiv.querySelector('#dashboard-content') || tempDiv;

        // Animation fade out
        this.contentContainer.style.opacity = '0';
        this.contentContainer.style.transform = 'translateY(10px)';

        setTimeout(() => {
            // Remplacer le contenu
            this.contentContainer.innerHTML = newContent.innerHTML || newContent.outerHTML;

            // Animation fade in
            this.contentContainer.style.opacity = '1';
            this.contentContainer.style.transform = 'translateY(0)';
        }, 200);
    }

    showLoader() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'flex';
        }
    }

    hideLoader() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'none';
        }
    }

    updateActiveNav(url) {
        // Retirer la classe active de tous les liens
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Ajouter la classe active au lien correspondant
        document.querySelectorAll('.nav-item').forEach(item => {
            const href = item.getAttribute('href');
            if (href && url.startsWith(href)) {
                item.classList.add('active');
            }
        });
    }

    initPageComponents() {
        // Réinitialiser les composants JavaScript de la page
        // Par exemple, réinitialiser les tooltips, modales, etc.
        
        // Réinitialiser les event listeners si nécessaire
        // Cette fonction sera étendue selon les besoins
    }

    showError(message) {
        // Afficher un toast d'erreur
        if (window.showToast) {
            window.showToast(message, 'error');
        } else {
            alert(message);
        }
    }
}

// Exporter pour utilisation globale
window.DashboardRouter = DashboardRouter;

