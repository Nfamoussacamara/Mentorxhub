/**
 * Main JavaScript - Dashboard MentorXHub
 * Gestion de la sidebar, navbar et interactions de base
 */

(function () {
    'use strict';

    // ===== SIDEBAR TOGGLE =====
    const sidebar = document.getElementById('dashboard-sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navbarMobileToggle = document.getElementById('navbar-mobile-toggle');
    const sidebarCollapseBtn = document.getElementById('sidebar-collapse-btn');
    const sidebarResizer = document.getElementById('sidebar-resizer');
    const dashboardMain = document.querySelector('.dashboard-main');

    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
    }

    // Toggle mobile sidebar
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (navbarMobileToggle) {
        navbarMobileToggle.addEventListener('click', toggleSidebar);
    }

    // Toggle sidebar collapse (desktop)
    if (sidebarCollapseBtn) {
        sidebarCollapseBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (sidebar) {
                sidebar.classList.toggle('collapsed');

                // Sauvegarder l'état dans sessionStorage
                const isCollapsed = sidebar.classList.contains('collapsed');
                sessionStorage.setItem('sidebarCollapsed', isCollapsed);

                if (isCollapsed) {
                    // Si on réduit, on enlève le style inline pour laisser le CSS agir (70px)
                    sidebar.style.width = '';
                    if (dashboardMain) {
                        dashboardMain.style.marginLeft = ''; // Le CSS gérera la marge (70px)
                    }
                } else {
                    // Si on dé-collapse, restaurer la largeur depuis sessionStorage
                    const savedWidth = sessionStorage.getItem('sidebarWidth');
                    const width = savedWidth ? parseInt(savedWidth) : 260;

                    if (window.innerWidth > 1024) {
                        sidebar.style.width = width + 'px';
                        if (dashboardMain) {
                            dashboardMain.style.marginLeft = width + 'px';
                        }
                    }
                }
            }
        });
    }

    // ===== SIDEBAR RESIZE =====
    if (sidebarResizer && sidebar && dashboardMain) {
        let isResizing = false;
        let startX = 0;
        let startWidth = 0;

        // Désactiver le resize sur mobile/tablette
        function updateResizerState() {
            if (window.innerWidth <= 1024) {
                sidebarResizer.style.display = 'none';
            } else {
                sidebarResizer.style.display = 'block';
            }
        }

        updateResizerState();
        window.addEventListener('resize', updateResizerState);

        sidebarResizer.addEventListener('mousedown', function (e) {
            // Empêcher le resize sur mobile/tablette
            if (window.innerWidth <= 1024) return;

            isResizing = true;
            startX = e.clientX;
            startWidth = sidebar.offsetWidth;

            sidebar.classList.add('resizing');
            sidebarResizer.classList.add('resizing');
            if (dashboardMain) dashboardMain.classList.add('resizing');

            document.body.style.cursor = 'ew-resize';
            document.body.style.userSelect = 'none';

            e.preventDefault();
        });

        document.addEventListener('mousemove', function (e) {
            if (!isResizing) return;

            const deltaX = e.clientX - startX;
            let newWidth = startWidth + deltaX;

            // Limiter la largeur entre 70px et 221px (max-width de la sidebar)
            newWidth = Math.max(70, Math.min(221, newWidth));

            sidebar.style.width = newWidth + 'px';
            if (dashboardMain) {
                dashboardMain.style.marginLeft = newWidth + 'px';
            }

            // Ajouter/retirer la classe sidebar-narrow
            if (newWidth < 150) {
                sidebar.classList.add('sidebar-narrow');
            } else {
                sidebar.classList.remove('sidebar-narrow');
            }

            // Si la largeur est très petite (< 90px), passer en mode collapsed (bouton en bas)
            if (newWidth < 90) {
                if (!sidebar.classList.contains('collapsed')) {
                    sidebar.classList.add('collapsed');
                    sessionStorage.setItem('sidebarCollapsed', 'true');
                }
            } else {
                if (sidebar.classList.contains('collapsed')) {
                    sidebar.classList.remove('collapsed');
                    sessionStorage.setItem('sidebarCollapsed', 'false');
                }
            }

            // Masquer/afficher les labels progressivement
            const labels = sidebar.querySelectorAll('.nav-label, .brand-text');
            const badges = sidebar.querySelectorAll('.nav-badge');

            // Afficher complètement (géré par CSS pour scaling)
            labels.forEach(label => {
                label.style.opacity = '1';
                label.style.width = 'auto';
            });
            badges.forEach(badge => {
                badge.style.opacity = '1';
                badge.style.width = 'auto';
            });

            const navItems = sidebar.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.style.justifyContent = '';
                item.style.padding = '';
            });

            const brandLogo = sidebar.querySelector('.sidebar-brand');
            if (brandLogo) brandLogo.style.justifyContent = '';
        });

        document.addEventListener('mouseup', function () {
            if (!isResizing) return;

            isResizing = false;
            sidebar.classList.remove('resizing');
            sidebarResizer.classList.remove('resizing');
            if (dashboardMain) dashboardMain.classList.remove('resizing');

            document.body.style.cursor = '';
            document.body.style.userSelect = '';

            // Sauvegarder la largeur dans sessionStorage (reset à la déconnexion)
            sessionStorage.setItem('sidebarWidth', sidebar.offsetWidth);
        });
    }

    // Restaurer l'état de la sidebar au chargement
    if (sidebar) {
        // Largeur par défaut pour nouvelle session
        const defaultWidth = 260;

        // Restaurer l'état collapsed (sessionStorage pour reset à la déconnexion)
        const isCollapsed = sessionStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
        }

        // Restaurer la largeur depuis sessionStorage (persiste pendant les rafraîchissements)
        const savedWidth = sessionStorage.getItem('sidebarWidth');
        if (!isCollapsed) {
            const width = savedWidth ? parseInt(savedWidth) : defaultWidth;

            // Appliquer la largeur seulement sur desktop
            if (window.innerWidth > 1024) {
                sidebar.style.width = width + 'px';
                if (dashboardMain) {
                    dashboardMain.style.marginLeft = width + 'px';
                }

                // Sauvegarder la largeur dans sessionStorage
                if (!savedWidth) {
                    sessionStorage.setItem('sidebarWidth', width);
                }
            }

            // Ajouter/retirer la classe sidebar-narrow
            if (width < 150) {
                sidebar.classList.add('sidebar-narrow');
            } else {
                sidebar.classList.remove('sidebar-narrow');
            }

            // Appliquer l'état des labels selon la largeur
            const labels = sidebar.querySelectorAll('.nav-label, .brand-text');
            const badges = sidebar.querySelectorAll('.nav-badge');


        }
    }

    // Fermer la sidebar en cliquant en dehors (mobile uniquement)
    document.addEventListener('click', function (e) {
        if (window.innerWidth <= 1024 && sidebar && sidebar.classList.contains('open')) {
            // Vérifier si le clic est à l'intérieur de la sidebar ou sur le toggle
            if (!sidebar.contains(e.target) &&
                !navbarMobileToggle?.contains(e.target) &&
                !sidebarToggle?.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });

    // Support tactile pour mobile
    if (sidebar && window.innerWidth <= 1024) {
        let touchStartX = 0;
        let touchEndX = 0;

        sidebar.addEventListener('touchstart', function (e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        sidebar.addEventListener('touchend', function (e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            // Swipe vers la gauche pour fermer
            if (touchStartX - touchEndX > 50) {
                sidebar.classList.remove('open');
            }
        }
    }

    // ===== USER MENU DROPDOWN =====
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userMenuDropdown = document.getElementById('user-menu-dropdown');

    if (userMenuBtn && userMenuDropdown) {
        userMenuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            userMenuDropdown.style.display =
                userMenuDropdown.style.display === 'none' ? 'block' : 'none';
        });

        // Fermer en cliquant en dehors
        document.addEventListener('click', function (e) {
            if (!userMenuBtn.contains(e.target) &&
                !userMenuDropdown.contains(e.target)) {
                userMenuDropdown.style.display = 'none';
            }
        });
    }

    // ===== NOTIFICATIONS DROPDOWN =====
    const notificationBtn = document.getElementById('notification-btn');
    const notificationsDropdown = document.getElementById('notifications-dropdown');

    // Charger les notifications
    async function loadNotifications() {
        if (!notificationsDropdown) return;

        try {
            const response = await fetch('/dashboard/notifications/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();

            if (data.html) {
                const listContainer = notificationsDropdown.querySelector('.notifications-list');
                if (listContainer) {
                    listContainer.innerHTML = data.html;
                }
            }

            // Mettre à jour le badge
            const badge = document.querySelector('.notification-badge');
            if (badge) {
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count > 99 ? '99+' : data.unread_count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }

    if (notificationBtn && notificationsDropdown) {
        notificationBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const isVisible = notificationsDropdown.style.display !== 'none';
            notificationsDropdown.style.display = isVisible ? 'none' : 'block';

            // Charger les notifications si le dropdown s'ouvre
            if (!isVisible) {
                loadNotifications();
            }
        });

        // Fermer en cliquant en dehors
        document.addEventListener('click', function (e) {
            if (!notificationBtn.contains(e.target) &&
                !notificationsDropdown.contains(e.target)) {
                notificationsDropdown.style.display = 'none';
            }
        });

        // Charger les notifications au chargement de la page
        loadNotifications();

        // Recharger toutes les 30 secondes
        setInterval(loadNotifications, 30000);
    }

    // ===== SEARCH TOGGLE =====
    const searchToggle = document.getElementById('search-toggle');
    const searchBox = document.getElementById('search-box');
    const searchClose = document.getElementById('search-close');

    if (searchToggle && searchBox) {
        searchToggle.addEventListener('click', function () {
            searchBox.style.display = 'flex';
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.focus();
            }
        });
    }

    if (searchClose && searchBox) {
        searchClose.addEventListener('click', function () {
            searchBox.style.display = 'none';
        });
    }

    // Raccourci clavier Ctrl+K pour la recherche
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (searchToggle) {
                searchToggle.click();
            }
        }
    });

    // ===== THEME TOGGLE =====
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Charger le thème sauvegardé (par défaut: dark)
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            const text = themeToggle.querySelector('span');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
            if (text) {
                text.textContent = theme === 'dark' ? 'Mode clair' : 'Mode sombre';
            }
        }
    }

    // ===== LOADING OVERLAY =====
    const loadingOverlay = document.getElementById('loading-overlay');

    window.showLoading = function () {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    };

    window.hideLoading = function () {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    };

    // ===== RESPONSIVE SIDEBAR =====
    function handleResize() {
        if (window.innerWidth > 1024 && sidebar) {
            sidebar.classList.remove('open');
        } else if (window.innerWidth <= 1024 && sidebar) {
            // Sur mobile, réinitialiser les styles inline
            sidebar.style.width = '';
            if (dashboardMain) {
                dashboardMain.style.marginLeft = '';
            }
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Appel initial

    // ===== INITIALISER LE ROUTER AJAX =====
    if (window.DashboardRouter) {
        window.router = new DashboardRouter();
        console.log('Router AJAX initialisé');
    }

    // ===== INTÉGRER LE STATE MANAGER =====
    if (window.stateManager) {
        // Synchroniser le thème avec le state manager
        const currentTheme = html.getAttribute('data-theme');
        window.stateManager.setState('theme', currentTheme);

        // Écouter les changements de thème
        window.stateManager.subscribe('theme', (theme) => {
            html.setAttribute('data-theme', theme);
            updateThemeIcon(theme);
        });

        // Mettre à jour le state manager quand le thème change
        if (themeToggle) {
            themeToggle.addEventListener('click', function () {
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                window.stateManager.setState('theme', newTheme);
            });
        }
    }

    // ===== INITIALISER LES MODULES SPÉCIFIQUES =====
    // Les modules seront chargés dynamiquement via les scripts dans base.html
    // Cette fonction sera appelée après le chargement de chaque module

    function initPageModules() {
        const currentPath = window.location.pathname;

        // Les modules s'auto-initialisent via leurs propres scripts
        // On peut ajouter une logique supplémentaire ici si nécessaire
    }

    // Appeler après le chargement du DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPageModules);
    } else {
        initPageModules();
    }

    console.log('Dashboard JavaScript initialisé');
})();

