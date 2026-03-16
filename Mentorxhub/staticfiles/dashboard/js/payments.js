/**
 * JavaScript pour la gestion des paiements
 * Filtres, statistiques, téléchargement de factures
 */

// Utiliser l'API client global
const apiClient = window.apiClient;

const paymentsApp = (function() {
    /**
     * Initialise l'application des paiements
     */
    function init() {
        setupEventListeners();
        loadPaymentStats();
        console.log('Payments app initialized');
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Filtres de paiements
        const statusFilter = document.getElementById('status-filter');
        const typeFilter = document.getElementById('type-filter');

        if (statusFilter) {
            statusFilter.addEventListener('change', handlePaymentFilter);
        }

        if (typeFilter) {
            typeFilter.addEventListener('change', handlePaymentFilter);
        }

        // Boutons de téléchargement de facture
        const invoiceBtns = document.querySelectorAll('.download-invoice-btn');
        invoiceBtns.forEach(btn => {
            btn.addEventListener('click', handleInvoiceDownload);
        });
    }

    /**
     * Gère le filtrage des paiements
     */
    function handlePaymentFilter() {
        const statusFilter = document.getElementById('status-filter');
        const typeFilter = document.getElementById('type-filter');
        
        const statusValue = statusFilter ? statusFilter.value : '';
        const typeValue = typeFilter ? typeFilter.value : '';
        
        const paymentRows = document.querySelectorAll('.payment-row');
        
        paymentRows.forEach(row => {
            const rowStatus = row.dataset.status;
            const rowType = row.dataset.type;
            
            const statusMatch = !statusValue || rowStatus === statusValue;
            const typeMatch = !typeValue || rowType === typeValue;
            
            if (statusMatch && typeMatch) {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        });
    }

    /**
     * Charge les statistiques des paiements
     */
    async function loadPaymentStats(period = '30d') {
        try {
            const response = await fetch(`/dashboard/payments/stats/?period=${period}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                updateStatsDisplay(data);
            }
        } catch (error) {
            console.error('Error loading payment stats:', error);
        }
    }

    /**
     * Met à jour l'affichage des statistiques
     */
    function updateStatsDisplay(stats) {
        // Mettre à jour les cartes de stats si elles existent
        const totalPaidElement = document.getElementById('total-paid-stat');
        if (totalPaidElement) {
            totalPaidElement.textContent = `${stats.total_amount.toFixed(2)}€`;
        }

        const completedCountElement = document.getElementById('completed-count-stat');
        if (completedCountElement) {
            completedCountElement.textContent = stats.completed_count;
        }
    }

    /**
     * Gère le téléchargement d'une facture
     */
    async function handleInvoiceDownload(event) {
        const btn = event.target.closest('.download-invoice-btn');
        const paymentId = btn.dataset.paymentId;

        if (!paymentId) return;

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            const response = await fetch(`/dashboard/payments/${paymentId}/invoice/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                // Si c'est un PDF, le télécharger
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `invoice_${paymentId}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                showToast('Facture téléchargée', 'success');
            } else {
                showToast('Erreur lors du téléchargement', 'error');
            }
        } catch (error) {
            console.error('Error downloading invoice:', error);
            showToast('Erreur lors du téléchargement', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-download"></i>';
        }
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
        loadStats: loadPaymentStats,
    };
})();

// Auto-initialisation
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => paymentsApp.init());
} else {
    paymentsApp.init();
}

