/**
 * Dashboard Overview - Graphiques et visualisations (v2.0)
 * Gère UNIQUEMENT l'initialisation des graphiques Chart.js.
 * Le rafraîchissement des données est géré par HTMX.
 */

(function () {
    'use strict';

    // Verrou pour éviter les exécutions multiples
    if (window.dashboardOverviewInitialized) return;
    window.dashboardOverviewInitialized = true;

    // Stockage global des instances pour destruction propre
    window.dashboardChartInstances = window.dashboardChartInstances || {
        sessions: null,
        revenue: null
    };

    /**
     * Initialise le graphique des sessions
     */
    function initSessionsChart() {
        const canvas = document.getElementById('sessionsStatusChart');
        if (!canvas) return;

        // Détruire l'ancienne instance si elle existe
        if (window.dashboardChartInstances.sessions) {
            window.dashboardChartInstances.sessions.destroy();
        }

        const data = {
            labels: ['Planifiées', 'En cours', 'Terminées', 'Annulées'],
            datasets: [{
                data: [
                    parseInt(canvas.getAttribute('data-scheduled') || 0),
                    parseInt(canvas.getAttribute('data-in-progress') || 0),
                    parseInt(canvas.getAttribute('data-completed') || 0),
                    parseInt(canvas.getAttribute('data-cancelled') || 0)
                ],
                backgroundColor: ['#3b82f6', '#f59e0b', '#10b981', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 15
            }]
        };

        window.dashboardChartInstances.sessions = new Chart(canvas, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: { size: 13, weight: '600' },
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: true
                    }
                }
            }
        });
    }

    /**
     * Initialise le graphique des revenus/heures
     */
    function initRevenueChart() {
        const canvas = document.getElementById('revenueChart');
        if (!canvas) return;

        if (window.dashboardChartInstances.revenue) {
            window.dashboardChartInstances.revenue.destroy();
        }

        try {
            const rawData = canvas.getAttribute('data-chart-data') || '[]';
            const rawLabels = canvas.getAttribute('data-chart-labels') || '[]';
            const dataValues = JSON.parse(rawData);
            const labels = JSON.parse(rawLabels);

            window.dashboardChartInstances.revenue = new Chart(canvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Activité',
                        data: dataValues,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                        x: { grid: { display: false } }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: { mode: 'index', intersect: false }
                    }
                }
            });
        } catch (e) {
            console.error('Erreur parsing données graphique:', e);
        }
    }

    /**
     * Point d'entrée global pour l'initialisation (appelé par htmx-init.js)
     */
    window.initDashboardCharts = function () {
        console.log('Dashboard: Initialisation des graphiques...');
        initSessionsChart();
        initRevenueChart();
    };

    // Auto-initialisation au chargement initial
    if (document.readyState === 'complete') {
        window.initDashboardCharts();
    } else {
        window.addEventListener('load', window.initDashboardCharts);
    }

})();
