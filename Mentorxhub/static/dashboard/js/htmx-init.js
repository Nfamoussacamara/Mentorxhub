/**
 * HTMX Initialization - Orchestrateur Global (v2.0)
 * Gère la réinitialisation des composants après chaque swap HTMX.
 */

(function () {
    'use strict';

    /**
     * Fonction d'initialisation centrale
     * Appelle les init() de chaque module s'ils sont présents dans le DOM.
     */
    window.initComponents = function () {
        console.log('HTMX: Initialisation des composants...');

        // 1. Boutons et liens (Correction hx-boost pour éviter les rechargements complets)
        try {
            document.querySelectorAll('button:not([hx-get]):not([hx-post]), input[type="button"], input[type="submit"]').forEach(btn => {
                if (!btn.hasAttribute('hx-boost')) btn.setAttribute('hx-boost', 'false');
            });
        } catch (e) { console.error('Error init buttons:', e); }

        // 2. Navigation et Sidebar
        if (typeof window.updateActiveNav === 'function') {
            window.updateActiveNav(window.location.pathname);
        }
        if (typeof window.restoreSidebarState === 'function') {
            window.restoreSidebarState();
        }

        // 3. Modules Applicatifs
        // Un léger délai (50ms) permet au DOM de se stabiliser après l'injection HTMX
        setTimeout(() => {
            // Dashboard Charts
            if (typeof window.initDashboardCharts === 'function') {
                window.initDashboardCharts();
            }

            // Messagerie
            if (window.messagesApp && typeof window.messagesApp.init === 'function') {
                window.messagesApp.init();
            }

            // Analytics
            if (window.analyticsApp && typeof window.analyticsApp.init === 'function') {
                window.analyticsApp.init();
            }

            // Sessions / Calendrier
            if (window.sessionsApp && typeof window.sessionsApp.init === 'function') {
                window.sessionsApp.init();
            }

            console.log('HTMX: Composants réinitialisés.');
        }, 50);
    };

    /**
     * Utilitaires Sidebar & Nav
     */
    window.updateActiveNav = function (url) {
        document.querySelectorAll('.nav-item').forEach(item => {
            const href = item.getAttribute('href');
            item.classList.toggle('active', href && url.startsWith(href));
        });
    };

    window.restoreSidebarState = function () {
        const sidebar = document.getElementById('dashboard-sidebar');
        if (!sidebar || window.innerWidth <= 1024) return;

        const isCollapsed = sessionStorage.getItem('sidebarCollapsed') === 'true';
        const width = sessionStorage.getItem('sidebarWidth') || '260';

        sidebar.classList.toggle('collapsed', isCollapsed);
        if (!isCollapsed) {
            sidebar.style.width = width + 'px';
            const main = document.querySelector('.dashboard-main');
            if (main) main.style.marginLeft = width + 'px';
        }
    };

    /**
     * Écouteur HTMX Global
     */
    document.body.addEventListener('htmx:afterSwap', function (evt) {
        // On réinitialise si la cible est le contenu principal ou le polling
        if (evt.detail.target.id === 'dashboard-content' ||
            evt.detail.target.id === 'dashboard-overview-polling') {

            requestAnimationFrame(() => {
                window.initComponents();
            });
        }
    });

    /**
     * Initialisation au premier chargement
     */
    document.addEventListener('DOMContentLoaded', () => {
        window.initComponents();
    });

    /**
     * Gestion Visibility (Polling)
     */
    document.addEventListener('visibilitychange', () => {
        const polling = document.querySelectorAll('[hx-trigger*="every"]');
        if (document.hidden) {
            polling.forEach(el => window.htmx && window.htmx.trigger(el, 'htmx:abort'));
        } else {
            polling.forEach(el => window.htmx && window.htmx.process(el));
        }
    });

})();
