/**
 * JavaScript pour le calendrier des sessions
 * Intégration FullCalendar
 */

const sessionsApp = (function() {
    let calendar = null;

    /**
     * Initialise l'application des sessions
     */
    function init() {
        // Charger FullCalendar depuis CDN si pas déjà chargé
        if (typeof FullCalendar === 'undefined') {
            loadFullCalendar().then(() => {
                setupCalendar();
            });
        } else {
            setupCalendar();
        }
        
        setupEventListeners();
        console.log('Sessions app initialized');
    }

    /**
     * Charge FullCalendar depuis CDN
     */
    function loadFullCalendar() {
        return new Promise((resolve, reject) => {
            if (typeof FullCalendar !== 'undefined') {
                resolve();
                return;
            }

            // Charger CSS
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://cdn.jsdelivr.net/npm/fullcalendar@6.1.10/index.global.min.css';
            document.head.appendChild(link);

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
    function setupCalendar() {
        const calendarEl = document.getElementById('sessions-calendar');
        if (!calendarEl) return;

        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'fr',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: async function(fetchInfo, successCallback, failureCallback) {
                try {
                    const response = await fetch('/dashboard/sessions/events/', {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.ok) {
                        const events = await response.json();
                        successCallback(events);
                    } else {
                        failureCallback();
                    }
                } catch (error) {
                    console.error('Error loading sessions:', error);
                    failureCallback();
                }
            },
            eventClick: function(info) {
                handleEventClick(info);
            },
            eventColor: '#3b82f6',
            eventTextColor: '#ffffff',
            height: 'auto',
        });

        calendar.render();
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Bouton de création de session
        const createSessionBtn = document.getElementById('create-session-btn');
        if (createSessionBtn) {
            createSessionBtn.addEventListener('click', handleCreateSession);
        }
    }

    /**
     * Gère le clic sur un événement
     */
    function handleEventClick(info) {
        const sessionId = info.event.id;
        if (sessionId) {
            // Charger les détails de la session
            loadSessionDetails(sessionId);
        }
    }

    /**
     * Charge les détails d'une session
     */
    async function loadSessionDetails(sessionId) {
        try {
            const response = await fetch(`/dashboard/sessions/${sessionId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.html) {
                    // Afficher dans un modal
                    showSessionModal(data.html);
                }
            }
        } catch (error) {
            console.error('Error loading session details:', error);
        }
    }

    /**
     * Affiche un modal avec les détails de la session
     */
    function showSessionModal(html) {
        if (window.Modal) {
            window.Modal.show('Détails de la session', html, {
                size: 'large',
                closable: true,
            });
        } else {
            // Fallback: ouvrir dans une nouvelle page
            console.log('Modal not available');
        }
    }

    /**
     * Gère la création d'une nouvelle session
     */
    function handleCreateSession() {
        // TODO: Ouvrir un formulaire de création
        if (window.Modal) {
            window.Modal.show('Créer une session', '<p>Formulaire de création à venir</p>');
        }
    }

    /**
     * Rafraîchit le calendrier
     */
    function refresh() {
        if (calendar) {
            calendar.refetchEvents();
        }
    }

    return {
        init: init,
        refresh: refresh,
    };
})();

// Auto-initialisation
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => sessionsApp.init());
} else {
    sessionsApp.init();
}
