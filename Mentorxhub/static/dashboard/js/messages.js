/**
 * JavaScript pour la messagerie en temps réel
 * Gestion des conversations, messages, polling
 */

// Utiliser l'API client global
const apiClient = window.apiClient;

const messagesApp = (function () {
    let pollingInterval = null;
    let currentConversationId = null;
    const POLLING_INTERVAL = 5000; // 5 secondes

    /**
     * Initialise la messagerie
     */
    function init() {
        // Vérifier si on est sur la page messages
        if (!document.querySelector('.messages-page-layout')) {
            return; // Ne pas initialiser si on n'est pas sur la page messages
        }

        setupEventListeners();
        // Démarrer le polling seulement si on est sur la page messages
        if (document.querySelector('.messages-list-panel')) {
            startUnreadCountPolling();
        }
    }

    /**
     * Configure les event listeners
     */
    function setupEventListeners() {
        // Formulaire d'envoi de message
        const messageForm = document.getElementById('message-form');
        if (messageForm) {
            messageForm.addEventListener('submit', handleMessageSend);
        }

        // Input de recherche de conversations
        const searchInput = document.getElementById('conversation-search');
        if (searchInput) {
            searchInput.addEventListener('input', handleConversationSearch);
        }

        // Bouton nouvelle conversation
        const newConversationBtn = document.getElementById('new-conversation-btn');
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', handleNewConversation);
        }

        // Bouton d'attachement
        const attachmentBtn = document.getElementById('attachment-btn');
        const attachmentInput = document.getElementById('attachment-input');
        if (attachmentBtn && attachmentInput) {
            attachmentBtn.addEventListener('click', () => attachmentInput.click());
            attachmentInput.addEventListener('change', handleAttachmentSelect);
        }

        // Bouton de fermeture de la notification
        const infoCloseBtn = document.getElementById('messages-info-close');
        if (infoCloseBtn) {
            infoCloseBtn.addEventListener('click', () => {
                const notification = document.getElementById('messages-info-notification');
                if (notification) {
                    notification.classList.add('hidden');
                    // Sauvegarder dans localStorage pour ne plus l'afficher
                    localStorage.setItem('messages-info-dismissed', 'true');
                }
            });
        }

        // Vérifier si la notification a déjà été fermée
        if (localStorage.getItem('messages-info-dismissed') === 'true') {
            const notification = document.getElementById('messages-info-notification');
            if (notification) {
                notification.classList.add('hidden');
            }
        }

        // Auto-scroll vers le bas dans les messages
        const messagesList = document.getElementById('messages-list');
        if (messagesList) {
            scrollToBottom(messagesList);
        }
    }

    /**
     * Gère l'envoi d'un message
     */
    async function handleMessageSend(event) {
        event.preventDefault();

        const form = event.target;
        const conversationId = form.dataset.conversationId;
        const messageInput = document.getElementById('message-input');
        const content = messageInput.value.trim();
        const attachmentInput = document.getElementById('attachment-input');

        if (!content && !attachmentInput.files[0]) {
            return;
        }

        // Afficher le message en local (optimistic update)
        if (content) {
            addMessageToUI(content, true);
            messageInput.value = '';
        }

        // Envoyer le message au serveur
        try {
            const formData = new FormData(form);

            const response = await window.apiClient.postForm(
                `/dashboard/messages/${conversationId}/send/`,
                formData
            );

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    // Le message a été ajouté, on peut rafraîchir la liste
                    loadMessages(conversationId);
                }
            } else {
                showToast('Erreur lors de l\'envoi du message', 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            showToast('Erreur lors de l\'envoi du message', 'error');
        }
    }

    /**
     * Ajoute un message à l'UI (optimistic update)
     */
    function addMessageToUI(content, isSent = true) {
        const messagesList = document.getElementById('messages-list');
        if (!messagesList) return;

        const messageItem = document.createElement('div');
        messageItem.className = `message-item ${isSent ? 'message-sent' : 'message-received'}`;
        messageItem.innerHTML = `
            <div class="message-avatar">
                <span>${getUserInitials()}</span>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="message-sender">Vous</span>
                    <span class="message-time">Maintenant</span>
                </div>
                <div class="message-text">${escapeHtml(content)}</div>
            </div>
        `;

        messagesList.appendChild(messageItem);
        scrollToBottom(messagesList);
    }

    /**
     * Charge les messages d'une conversation
     */
    async function loadMessages(conversationId) {
        try {
            const response = await fetch(`/dashboard/messages/${conversationId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                // Le router gère déjà le remplacement du contenu
                currentConversationId = conversationId;
                startMessagePolling(conversationId);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    /**
     * Démarre le polling des nouveaux messages
     */
    function startMessagePolling(conversationId) {
        // Arrêter le polling précédent
        stopMessagePolling();

        // Ne pas démarrer si on n'est pas sur une page de conversation
        if (!document.getElementById('messages-list')) {
            return;
        }

        currentConversationId = conversationId;
        let lastMessageId = getLastMessageId();

        pollingInterval = setInterval(async () => {
            // Vérifier que la page est toujours visible
            if (document.hidden) {
                return;
            }

            try {
                const response = await fetch(
                    `/dashboard/messages/poll/?last_message_id=${lastMessageId || ''}`,
                    {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }
                );

                if (response.ok) {
                    const data = await response.json();
                    if (data.messages && data.messages.length > 0) {
                        data.messages.forEach(message => {
                            if (message.conversation_id === conversationId) {
                                addMessageToUI(message.content, false);
                                lastMessageId = message.id;
                            }
                        });
                        updateUnreadCount();
                    }
                }
            } catch (error) {
                console.error('Error polling messages:', error);
            }
        }, POLLING_INTERVAL);
    }

    /**
     * Arrête le polling des messages
     */
    function stopMessagePolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    }

    /**
     * Récupère l'ID du dernier message
     */
    function getLastMessageId() {
        const messagesList = document.getElementById('messages-list');
        if (!messagesList) return null;

        const lastMessage = messagesList.lastElementChild;
        return lastMessage ? lastMessage.dataset.messageId : null;
    }

    /**
     * Gère la recherche de conversations
     */
    function handleConversationSearch(event) {
        const searchTerm = event.target.value.toLowerCase();
        const conversationItems = document.querySelectorAll('.conversation-item');

        conversationItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }

    /**
     * Gère la création d'une nouvelle conversation
     */
    async function handleNewConversation() {
        // TODO: Ouvrir un modal pour sélectionner le destinataire
        showToast('Fonctionnalité à venir', 'info');
    }

    /**
     * Gère la sélection d'un fichier attaché
     */
    function handleAttachmentSelect(event) {
        const file = event.target.files[0];
        if (file) {
            const fileName = file.name;
            const messageInput = document.getElementById('message-input');
            if (messageInput) {
                messageInput.placeholder = `Fichier sélectionné: ${fileName}`;
            }
        }
    }

    /**
     * Démarre le polling du compteur de messages non lus
     */
    function startUnreadCountPolling() {
        // Ne pas démarrer plusieurs fois
        if (window.unreadCountInterval) {
            return;
        }

        // Attendre que la page soit complètement chargée
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                startUnreadCountPolling();
            });
            return;
        }

        // Polling toutes les 30 secondes au lieu de 10 pour réduire la charge
        window.unreadCountInterval = setInterval(async () => {
            try {
                const response = await fetch('/dashboard/messages/unread-count/', {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    updateUnreadCountBadge(data.unread_count);
                }
            } catch (error) {
                console.error('Error fetching unread count:', error);
            }
        }, 30000); // Toutes les 30 secondes
    }

    /**
     * Met à jour le badge de messages non lus
     */
    function updateUnreadCountBadge(count) {
        const badge = document.getElementById('messages-unread-badge');
        if (badge) {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    /**
     * Met à jour le compteur de messages non lus
     */
    async function updateUnreadCount() {
        try {
            const response = await fetch('/dashboard/messages/unread-count/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                updateUnreadCountBadge(data.unread_count);
            }
        } catch (error) {
            console.error('Error updating unread count:', error);
        }
    }

    /**
     * Scroll vers le bas de la liste des messages
     */
    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }

    /**
     * Échappe le HTML pour éviter les XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Récupère les initiales de l'utilisateur
     */
    function getUserInitials() {
        // TODO: Récupérer depuis le contexte ou l'API
        return 'U';
    }

    /**
     * Affiche un toast
     */
    function showToast(message, type = 'info') {
        // Utiliser le système de toast existant ou créer un nouveau
        if (window.showToast) {
            window.showToast(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }

    return {
        init: init,
        loadMessages: loadMessages,
        stopPolling: stopMessagePolling,
    };
})();

// Auto-initialisation
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => messagesApp.init());
} else {
    messagesApp.init();
}

// Exposer globalement pour HTMX
window.messagesApp = messagesApp;

