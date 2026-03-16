/**
 * HTMX Initialization - Réinitialise les composants après swap HTMX
 * Ce fichier remplace la plupart du code AJAX par des événements HTMX
 */

(function() {
    'use strict';

    // Configuration globale HTMX
    document.addEventListener('DOMContentLoaded', function() {
        // Exclure certains liens du boost (liens externes, logout, etc.)
        document.querySelectorAll('a[href^="http"], a[href*="logout"], a[target="_blank"]').forEach(function(link) {
            link.setAttribute('hx-boost', 'false');
        });
    });

    // S'assurer que les boutons fonctionnent correctement
    document.addEventListener('DOMContentLoaded', function() {
        // Exclure tous les boutons de hx-boost (sauf ceux qui ont explicitement des attributs HTMX)
        document.querySelectorAll('button:not([hx-get]):not([hx-post]):not([hx-put]):not([hx-delete]), input[type="button"]:not([hx-get]):not([hx-post]), input[type="submit"]:not([hx-get]):not([hx-post])').forEach(function(btn) {
            if (!btn.hasAttribute('hx-boost')) {
                btn.setAttribute('hx-boost', 'false');
            }
        });
        
        // Réinitialiser après chaque swap HTMX
        document.body.addEventListener('htmx:afterSwap', function() {
            document.querySelectorAll('button:not([hx-get]):not([hx-post]):not([hx-put]):not([hx-delete]), input[type="button"]:not([hx-get]):not([hx-post]), input[type="submit"]:not([hx-get]):not([hx-post])').forEach(function(btn) {
                if (!btn.hasAttribute('hx-boost')) {
                    btn.setAttribute('hx-boost', 'false');
                }
            });
        });
    });

    // Réinitialiser les graphiques Chart.js après un swap HTMX
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        // Si on est sur le dashboard, réinitialiser les graphiques
        if (evt.detail.target.id === 'dashboard-content' || 
            evt.detail.target.closest('.dashboard-home')) {
            
            // Attendre un peu pour que le DOM soit prêt
            setTimeout(function() {
                if (typeof initCharts === 'function') {
                    initCharts();
                }
            }, 100);
        }
        
        // Réinitialiser les tooltips, modales, etc. si nécessaire
        // Par exemple, réinitialiser les event listeners pour les nouveaux éléments
    });

    // Gérer les erreurs HTMX
    document.body.addEventListener('htmx:responseError', function(evt) {
        console.error('Erreur HTMX:', evt.detail);
        if (window.showToast) {
            window.showToast('Une erreur est survenue. Veuillez réessayer.', 'error');
        }
    });

    // Afficher un indicateur de chargement personnalisé si nécessaire
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        // HTMX gère déjà les indicateurs via hx-indicator
        // Mais on peut ajouter des logs ou autres actions ici
    });

    // Mettre à jour l'URL active dans la sidebar après navigation
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        const url = window.location.pathname;
        updateActiveNav(url);
        
        // Restaurer l'état de la sidebar après chaque navigation
        restoreSidebarStateAfterSwap();
    });

    function updateActiveNav(url) {
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
    
    function restoreSidebarStateAfterSwap() {
        const sidebar = document.getElementById('dashboard-sidebar');
        const dashboardMain = document.querySelector('.dashboard-main');
        
        if (!sidebar || window.innerWidth <= 1024) return;
        
        const savedWidth = localStorage.getItem('sidebarWidth');
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
        } else if (savedWidth) {
            const width = parseInt(savedWidth);
            sidebar.style.width = width + 'px';
            if (dashboardMain) {
                dashboardMain.style.marginLeft = width + 'px';
            }
            
            // Ajouter/retirer la classe sidebar-narrow
            if (width < 150) {
                sidebar.classList.add('sidebar-narrow');
                
                // Appliquer l'opacité progressive
                const opacity = (width - 70) / 80;
                const labels = sidebar.querySelectorAll('.nav-label, .brand-text');
                const badges = sidebar.querySelectorAll('.nav-badge');
                
                labels.forEach(label => {
                    label.style.opacity = opacity;
                    label.style.width = opacity > 0.3 ? 'auto' : '0';
                });
                badges.forEach(badge => {
                    badge.style.opacity = opacity;
                    badge.style.width = opacity > 0.3 ? 'auto' : '0';
                });
                
                const navItems = sidebar.querySelectorAll('.nav-item');
                navItems.forEach(item => {
                    item.style.justifyContent = 'center';
                    item.style.padding = '0.875rem';
                });
                
                const brandLogo = sidebar.querySelector('.sidebar-brand');
                if (brandLogo) brandLogo.style.justifyContent = 'center';
            } else {
                sidebar.classList.remove('sidebar-narrow');
            }
        }
    }

    // Optimisation : Arrêter le polling quand la page n'est pas visible (Page Visibility API)
    document.addEventListener('visibilitychange', function() {
        const pollingElements = document.querySelectorAll('[hx-trigger*="every"]');
        
        if (document.hidden) {
            // Page non visible : suspendre le polling HTMX
            pollingElements.forEach(el => {
                if (window.htmx) {
                    window.htmx.trigger(el, 'htmx:abort');
                }
            });
        } else {
            // Page visible : reprendre le polling HTMX
            pollingElements.forEach(el => {
                if (window.htmx) {
                    window.htmx.process(el);
                }
            });
        }
    });

    // Éviter les duplications lors du swap
    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        // S'assurer que le swap remplace bien le contenu au lieu de le dupliquer
        if (evt.detail.shouldSwap) {
            // Forcer le swap innerHTML pour éviter les duplications
            if (evt.detail.target.id === 'dashboard-overview-polling') {
                evt.detail.shouldSwap = true;
                evt.detail.target.innerHTML = ''; // Vider avant le swap
            }
        }
    });
})();

