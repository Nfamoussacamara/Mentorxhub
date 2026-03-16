/**
 * JavaScript pour le module Notifications
 */

(function() {
    'use strict';

    const apiClient = window.apiClient || {
        post: async (url, data) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(data)
            });
            return response.json();
        }
    };

    // Marquer une notification comme lue
    function markNotificationAsRead(notificationId) {
        const url = `/dashboard/notifications/${notificationId}/read/`;
        apiClient.post(url, {})
            .then(data => {
                if (data.success) {
                    const item = document.querySelector(`[data-notification-id="${notificationId}"]`);
                    if (item) {
                        item.classList.remove('unread');
                        updateUnreadCount();
                    }
                }
            })
            .catch(error => {
                console.error('Error marking notification as read:', error);
            });
    }

    // Marquer toutes les notifications comme lues
    function markAllAsRead() {
        const url = '/dashboard/notifications/mark-all-read/';
        apiClient.post(url, {})
            .then(data => {
                if (data.success) {
                    document.querySelectorAll('.notification-item.unread, .notification-item-dropdown.unread').forEach(item => {
                        item.classList.remove('unread');
                    });
                    updateUnreadCount();
                }
            })
            .catch(error => {
                console.error('Error marking all notifications as read:', error);
            });
    }

    // Mettre à jour le compteur de notifications non lues
    function updateUnreadCount() {
        fetch('/dashboard/notifications/count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.querySelector('.notification-badge');
                if (badge) {
                    if (data.count > 0) {
                        badge.textContent = data.count > 99 ? '99+' : data.count;
                        badge.style.display = 'inline-block';
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => {
                console.error('Error updating unread count:', error);
            });
    }

    // Initialisation
    document.addEventListener('DOMContentLoaded', function() {
        // Clic sur une notification
        document.querySelectorAll('.notification-item, .notification-item-dropdown').forEach(item => {
            item.addEventListener('click', function() {
                const notificationId = this.getAttribute('data-notification-id');
                if (notificationId && this.classList.contains('unread')) {
                    markNotificationAsRead(notificationId);
                }
            });
        });

        // Bouton "Tout marquer comme lu"
        const markAllReadBtn = document.getElementById('mark-all-read-btn') || 
                              document.getElementById('mark-all-read-dropdown');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', function(e) {
                e.preventDefault();
                markAllAsRead();
            });
        }

        // Mettre à jour le compteur toutes les 30 secondes
        setInterval(updateUnreadCount, 30000);
        
        // Mise à jour initiale
        updateUnreadCount();
    });

    // Exporter pour utilisation globale
    window.notificationsManager = {
        markAsRead: markNotificationAsRead,
        markAllAsRead: markAllAsRead,
        updateUnreadCount: updateUnreadCount
    };
})();

