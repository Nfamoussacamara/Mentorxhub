/**
 * JavaScript pour le calendrier des sessions
 * Intégration FullCalendar v6
 */

const sessionsApp = (function () {
    let calendar = null;

    /**
     * Initialise l'application des sessions
     */
    function init() {
        console.log('Initializing Sessions Calendar...');

        // S'assurer que les éléments DOM sont présents
        const calendarEl = document.getElementById('sessions-calendar');
        if (!calendarEl) {
            console.warn('Calendar element #sessions-calendar not found');
            return;
        }

        // Charger FullCalendar si nécessaire
        if (typeof FullCalendar === 'undefined') {
            loadFullCalendar().then(() => {
                setupCalendar(calendarEl);
            });
        } else {
            setupCalendar(calendarEl);
        }

        setupEventListeners();
    }

    /**
     * Charge FullCalendar depuis CDN si non présent
     */
    function loadFullCalendar() {
        return new Promise((resolve, reject) => {
            // Charger JS
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/fullcalendar@6.1.10/index.global.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Configure le calendrier
     */
    function setupCalendar(calendarEl) {
        if (calendar) {
            calendar.destroy();
        }

        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'fr',
            firstDay: 1, // Lundi
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'
            },
            buttonText: {
                today: "Aujourd'hui",
                month: "Mois",
                week: "Semaine"
            },
            events: '/dashboard/sessions/events/',
            eventClick: function (info) {
                handleEventClick(info);
            },
            eventTimeFormat: {
                hour: '2-digit',
                minute: '2-digit',
                meridiem: false,
                hour12: false
            },
            height: 'auto',
            nowIndicator: true,
            dayMaxEvents: true,
            themeSystem: 'standard'
        });

        calendar.render();
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        const modalOverlay = document.getElementById('session-modal-overlay');
        const closeBtn = document.getElementById('modal-close-btn');

        if (closeBtn && modalOverlay) {
            closeBtn.onclick = () => {
                modalOverlay.style.display = 'none';
                document.body.classList.remove('modal-open');
            };

            modalOverlay.onclick = (e) => {
                if (e.target === modalOverlay) {
                    modalOverlay.style.display = 'none';
                    document.body.classList.remove('modal-open');
                }
            };
        }
    }

    /**
     * Gère le clic sur un événement
     */
    function handleEventClick(info) {
        const sessionId = info.event.id;
        const modalOverlay = document.getElementById('session-modal-overlay');
        const modalBody = document.getElementById('modal-body-content');

        if (!modalOverlay || !modalBody) return;

        // Afficher l'overlay et le loader
        modalOverlay.style.display = 'flex';
        document.body.classList.add('modal-open');
        modalBody.innerHTML = '<div class="premium-loading"><div class="premium-spinner"></div><p>Chargement...</p></div>';

        // Charger les détails via AJAX
        fetch(`/dashboard/sessions/${sessionId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.html) {
                    modalBody.innerHTML = data.html;
                    // Déclencher HTMX sur le nouveau contenu si nécessaire
                    if (typeof htmx !== 'undefined') {
                        htmx.process(modalBody);
                    }
                } else {
                    modalBody.innerHTML = '<p class="error-msg">Impossible de charger les détails.</p>';
                }
            })
            .catch(err => {
                console.error('Error fetching session details:', err);
                modalBody.innerHTML = '<p class="error-msg">Une erreur est survenue.</p>';
            });
    }

    return {
        init: init,
        refresh: () => calendar && calendar.refetchEvents()
    };
})();

// Initialisation globale
window.sessionsApp = sessionsApp;

// Auto-init si on est sur la page
if (document.getElementById('sessions-calendar')) {
    sessionsApp.init();
}
