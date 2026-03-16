/**
 * JavaScript pour le support client
 * Gestion des tickets, filtres, réponses
 */

// Utiliser l'API client global
const apiClient = window.apiClient;

const supportApp = (function() {
    /**
     * Initialise l'application du support
     */
    function init() {
        setupEventListeners();
        console.log('Support app initialized');
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Filtres de tickets
        const statusFilter = document.getElementById('status-filter');
        const priorityFilter = document.getElementById('priority-filter');

        if (statusFilter) {
            statusFilter.addEventListener('change', handleTicketFilter);
        }

        if (priorityFilter) {
            priorityFilter.addEventListener('change', handleTicketFilter);
        }

        // Formulaire de réponse à un ticket
        const replyForm = document.getElementById('ticket-reply-form');
        if (replyForm) {
            replyForm.addEventListener('submit', handleTicketReply);
        }

        // Bouton de fermeture de ticket
        const closeTicketBtn = document.getElementById('close-ticket-btn');
        if (closeTicketBtn) {
            closeTicketBtn.addEventListener('click', handleTicketClose);
        }
    }

    /**
     * Gère le filtrage des tickets
     */
    function handleTicketFilter() {
        const statusFilter = document.getElementById('status-filter');
        const priorityFilter = document.getElementById('priority-filter');
        
        const statusValue = statusFilter ? statusFilter.value : '';
        const priorityValue = priorityFilter ? priorityFilter.value : '';
        
        const ticketItems = document.querySelectorAll('.ticket-item');
        
        ticketItems.forEach(item => {
            const itemStatus = item.dataset.status;
            const itemPriority = item.dataset.priority;
            
            const statusMatch = !statusValue || itemStatus === statusValue;
            const priorityMatch = !priorityValue || itemPriority === priorityValue;
            
            if (statusMatch && priorityMatch) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    /**
     * Gère l'envoi d'une réponse à un ticket
     */
    async function handleTicketReply(event) {
        event.preventDefault();
        
        const form = event.target;
        const ticketId = form.dataset.ticketId;
        const contentInput = form.querySelector('textarea[name="content"]');
        const content = contentInput.value.trim();
        
        if (!content) {
            showToast('Le contenu est requis', 'error');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi...';

        try {
            const response = await window.apiClient.post(
                `/dashboard/support/tickets/${ticketId}/reply/`,
                {
                    content: content
                }
            );

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    // Ajouter la réponse à l'UI
                    addReplyToUI(data.reply);
                    contentInput.value = '';
                    showToast('Réponse envoyée', 'success');
                }
            } else {
                showToast('Erreur lors de l\'envoi', 'error');
            }
        } catch (error) {
            console.error('Error sending reply:', error);
            showToast('Erreur lors de l\'envoi', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Envoyer';
        }
    }

    /**
     * Ajoute une réponse à l'UI
     */
    function addReplyToUI(reply) {
        const repliesContainer = document.getElementById('ticket-replies');
        if (!repliesContainer) return;

        const replyElement = document.createElement('div');
        replyElement.className = 'ticket-reply';
        replyElement.innerHTML = `
            <div class="reply-header">
                <span class="reply-author">${reply.author}</span>
                <span class="reply-date">${formatDate(reply.created_at)}</span>
            </div>
            <div class="reply-content">${escapeHtml(reply.content)}</div>
        `;

        repliesContainer.appendChild(replyElement);
        replyElement.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Gère la fermeture d'un ticket
     */
    async function handleTicketClose(event) {
        const btn = event.target.closest('#close-ticket-btn');
        const ticketId = btn.dataset.ticketId;

        if (!ticketId) return;

        if (!confirm('Êtes-vous sûr de vouloir fermer ce ticket ?')) {
            return;
        }

        btn.disabled = true;

        try {
            const response = await window.apiClient.post(
                `/dashboard/support/tickets/${ticketId}/close/`,
                {}
            );

            if (response.ok) {
                showToast('Ticket fermé', 'success');
                // Rediriger vers la liste des tickets
                setTimeout(() => {
                    window.location.href = '/dashboard/support/';
                }, 1000);
            } else {
                showToast('Erreur lors de la fermeture', 'error');
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Error closing ticket:', error);
            showToast('Erreur lors de la fermeture', 'error');
            btn.disabled = false;
        }
    }

    /**
     * Formate une date
     */
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Échappe le HTML
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
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
    document.addEventListener('DOMContentLoaded', () => supportApp.init());
} else {
    supportApp.init();
}

