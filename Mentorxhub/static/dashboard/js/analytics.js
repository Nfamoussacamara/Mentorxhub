/**
 * JavaScript pour les analytics et graphiques
 * Intégration Chart.js
 */

const analyticsApp = (function () {
    let charts = {};

    /**
     * Initialise l'application analytics
     */
    function init() {
        // Charger Chart.js depuis CDN si pas déjà chargé
        if (typeof Chart === 'undefined') {
            loadChartJS().then(() => {
                setupCharts();
            });
        } else {
            setupCharts();
        }

        setupEventListeners();
        console.log('Analytics app initialized');
    }

    /**
     * Charge Chart.js depuis CDN
     */
    function loadChartJS() {
        return new Promise((resolve, reject) => {
            if (typeof Chart !== 'undefined') {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Configure les graphiques
     */
    function setupCharts() {
        // Graphique des sessions
        const sessionsCtx = document.getElementById('sessions-chart');
        if (sessionsCtx) {
            charts.sessions = createSessionsChart(sessionsCtx);
        }

        // Graphique des revenus/heures
        const earningsCtx = document.getElementById('earnings-chart');
        if (earningsCtx) {
            charts.earnings = createEarningsChart(earningsCtx);
        }

        // Graphique des notes moyennes
        const ratingsCtx = document.getElementById('ratings-chart');
        if (ratingsCtx) {
            charts.ratings = createRatingsChart(ratingsCtx);
        }

        // Charger les données
        loadAnalyticsData();
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Sélecteur de période
        const periodSelect = document.getElementById('analytics-period');
        if (periodSelect) {
            periodSelect.addEventListener('change', handlePeriodChange);
        }
    }

    /**
     * Crée le graphique des sessions
     */
    function createSessionsChart(ctx) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Sessions',
                    data: [],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    }

    /**
     * Crée le graphique des revenus/heures
     */
    function createEarningsChart(ctx) {
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Revenus / Heures',
                    data: [],
                    backgroundColor: 'rgba(168, 85, 247, 0.8)',
                    borderColor: 'rgb(168, 85, 247)',
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    }

    /**
     * Crée le graphique des notes
     */
    function createRatingsChart(ctx) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Note moyenne',
                    data: [],
                    borderColor: 'rgb(16, 185, 129)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5,
                    }
                }
            }
        });
    }

    /**
     * Charge les données analytics
     */
    async function loadAnalyticsData(period = '7d') {
        try {
            const response = await fetch(`/dashboard/analytics/data/?period=${period}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                updateCharts(data);
                updateKPIs(data.kpis);
            }
        } catch (error) {
            console.error('Error loading analytics data:', error);
        }
    }

    /**
     * Met à jour les graphiques avec les nouvelles données
     */
    function updateCharts(data) {
        // Mettre à jour le graphique des sessions
        if (charts.sessions) {
            charts.sessions.data.labels = data.labels;
            charts.sessions.data.datasets[0].data = data.sessions_data;
            charts.sessions.update();
        }

        // Mettre à jour le graphique des revenus/heures
        if (charts.earnings) {
            charts.earnings.data.labels = data.labels;
            charts.earnings.data.datasets[0].data = data.earnings_data;
            charts.earnings.update();
        }

        // Mettre à jour le graphique des notes
        if (charts.ratings && data.avg_rating_data) {
            charts.ratings.data.labels = data.labels;
            charts.ratings.data.datasets[0].data = data.avg_rating_data;
            charts.ratings.update();
        }
    }

    /**
     * Met à jour les KPIs
     */
    function updateKPIs(kpis) {
        const kpiElements = {
            'total-sessions': kpis.total_sessions,
            'completed-sessions': kpis.completed_sessions,
            'total-earnings': kpis.total_earnings || kpis.total_hours,
            'avg-rating': kpis.avg_rating,
        };

        Object.entries(kpiElements).forEach(([id, value]) => {
            const element = document.getElementById(`kpi-${id}`);
            if (element) {
                element.textContent = typeof value === 'number'
                    ? value.toFixed(2)
                    : value;
            }
        });
    }

    /**
     * Gère le changement de période
     */
    function handlePeriodChange(event) {
        const period = event.target.value;
        loadAnalyticsData(period);
    }

    return {
        init: init,
        loadData: loadAnalyticsData,
    };
})();

// Auto-initialisation
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => analyticsApp.init());
} else {
    analyticsApp.init();
}

// Exposer globalement pour HTMX
window.analyticsApp = analyticsApp;
